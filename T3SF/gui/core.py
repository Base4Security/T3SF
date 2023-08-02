from flask import Flask, render_template, Response, Blueprint, request, jsonify, after_this_request
import os, signal, time
import threading
import logging
import uuid
import queue
from datetime import datetime
import json
from T3SF import utils

import sqlite3

bp = Blueprint('t3sf', __name__)

platform = None
msel_file = None

class GUI(Flask):
	def __init__(self, platform_run, MSEL, import_name=__name__, *args, **kwargs):
		global platform, msel_file
		msel_file = MSEL
		platform = platform_run
		super().__init__(import_name, *args, **kwargs)
		self.config['SECRET_KEY'] = uuid.uuid4().hex
		self.register_blueprint(bp)
		self.start()

	def start_flask_app(self):
		log = logging.getLogger('werkzeug')
		log.setLevel(logging.WARNING)
		if utils.is_docker():
			print(" * GUI active on - http://0.0.0.0:5000")
			self.run(debug=False, threaded=True, use_reloader=False, host="0.0.0.0")
		else:
			print(" * GUI active on - http://127.0.0.1:5000")
			self.run(debug=False, threaded=True, use_reloader=False)

	def start(self):
		flask_app_thread = threading.Thread(target=self.start_flask_app)
		flask_app_thread.start()

listeners = [] 
class MessageAnnouncer:
	def listen(self):
		global listeners
		listeners.append(queue.Queue(maxsize=10))
		return listeners[-1]

	def announce(self, msg):
		global listeners
		# We go in reverse order because we might have to delete an element, which will shift the
		# indices backward
		for i in reversed(range(len(listeners))):
			try:
				listeners[i].put_nowait(msg)
			except queue.Full:
				del listeners[i]

# Global variables for the template engine
@bp.context_processor
def actual_platform():
	def get_platform():
		# Return the platform value here
		return platform
	
	return dict(platform=get_platform())

# SSE 
@bp.route('/stream', methods=['GET'])
def listen():
	def stream():
		# Yield the previous logs
		try:
			with open('logs.txt', 'r+') as f:
				for line in f:
					yield line
		except FileNotFoundError:
			with open('logs.txt', 'a+') as f:
				for line in f:
					yield line

		messages = MessageAnnouncer().listen()  # returns a queue.Queue
		messages.put("New client connected\n\n")  # Send a message when a client connects
		while True:
			msg = messages.get()  # blocks until a new message arrives
			yield msg

	return Response(stream(), mimetype='text/event-stream')

@bp.route('/stream_news', methods=['GET'])
def listen_news():
	def stream():
		messages = MessageAnnouncer().listen()  # returns a queue.Queue
		while True:
			msg = messages.get()  # blocks until a new message arrives
			yield msg

	return Response(stream(), mimetype='text/event-stream')

# Views 
@bp.route('/')
def index():
	return render_template('index.html', active_page="logs_viewer")

@bp.route('/msel-playground')
def msel_playground():
	return render_template('msel_playground.html', active_page="msel_playground")

@bp.route('/env-creation')
def env_creation():
	from T3SF import T3SF
	T3SF = T3SF(platform=platform.lower())
	T3SF.IncidentsFetcher(MSEL=msel_file)

	return render_template('env_creation.html', active_page="env_creation", T3SF=T3SF)

# Actions
@bp.route('/start')
async def start_exercise():
	# Start the async task

	if platform.lower() == "discord":
		from T3SF.discord.bot import run_async_incidents
		try:
			server_id = int(request.args.get("server"))
			
			# Setting variables for GUI
			utils.process_quit = False
			utils.process_wait = False
			utils.process_started = True

			await run_async_incidents(server=server_id)

		except (ValueError, TypeError):
			msg = {
				"id": str(uuid.uuid4()),
				"type": "ERROR",
				"content": "The Token was not provided or is not an integer.",
				"timestamp": datetime.now().strftime("%H:%M:%S")
			}
			MessageAnnouncer().announce(msg=f"data: {json.dumps(msg)}\n\n")
			return Response("Failed, Token was not provided or is not an integer.", mimetype='text/plain')

	elif platform.lower() == "slack":
		from T3SF.slack.bot import run_async_incidents
		
		# Setting variables for GUI
		utils.process_quit = False
		utils.process_wait = False
		utils.process_started = True
		
		await run_async_incidents()

	# Return an immediate response
	return Response("Started", mimetype='text/plain')

@bp.route('/pause')
def pause_exercise():
	utils.process_wait = True

	return "We are waiting"

@bp.route('/resume')
def resume_exercise():
	utils.process_wait = False
	utils.process_quit = False
	utils.process_started = True

	return "We are processing again"

@bp.route('/stop')
def stop_exercise():
	utils.process_quit = True

	return "We are Stoping"

@bp.route('/abort')
def abort_exercise():
	# Return a response first
	response = 'Shutting down...'

	# Define a function to be executed after the response is sent
	@after_this_request
	def shutdown(response):
		# Start a new thread to kill the script
		t = threading.Thread(target=kill_script)
		t.start()
		
		# Announce the exiting message
		msg = {
			"id": str(uuid.uuid4()),
			"type": "INFO",
			"content": "Exiting...",
			"timestamp": datetime.now().strftime("%H:%M:%S")
		}
		MessageAnnouncer().announce(msg=f"data: {json.dumps(msg)}\n\n")

		return response

	def kill_script():
		time.sleep(0.5)  # Wait for the client to receive response
		os._exit(0)  # Kill the script

	return response

@bp.route('/create')
async def create_env():
	if platform.lower() == "discord":
		from T3SF.discord.bot import create_environment
		try:
			server_id = int(request.args.get("server"))
			await create_environment(server=server_id)

		except (ValueError, TypeError):
			msg = {
				"id": str(uuid.uuid4()),
				"type": "ERROR",
				"content": "The Token was not provided or is not an integer.",
				"timestamp": datetime.now().strftime("%H:%M:%S")
			}
			MessageAnnouncer().announce(msg=f"data: {json.dumps(msg)}\n\n")
			return jsonify({"status":"error","msg":"Failed, Token was not provided or is not an integer."})

	elif platform.lower() == "slack":
		from T3SF.slack.bot import create_environment
		await create_environment()

	return jsonify({"status":"ok","msg":"Environment created!"})

@bp.route('/clear')
def clear_logs():
	# Clear the logs
	open('logs.txt', 'w').close()

	# Return a response
	return 'Logs cleared...'

# APIs
@bp.route('/data', methods=['POST'])
def get_data():
	# Connect to the SQLite database
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__)) + '/t3sf.sqlite3')
	cursor = conn.cursor()

	# Get the DataTables request parameters
	draw = int(request.form.get('draw', 0))
	start = int(request.form.get('start', 0))
	length = int(request.form.get('length', 0))
	search_value = request.form.get('search[value]', '')

	# Get the selected filters from the dropdowns
	filter_phase = request.form.get('phaseFilter', '')
	filter_sector = request.form.get('sectorFilter', '')

	# Construct the SQL query with search, pagination, and filter
	# columns = ['id', 'RelatedThreat', 'Receptor', 'Event', 'TypeOfScenario', 'TPP', 'ExercisePhase', Subject', 'Sector', 'Poll'] // Enable this if you want search to be global
	columns = ['id', 'RelatedThreat', 'Receptor', 'Event']
	conditions = []
	params = []
	
	# Generate the WHERE conditions for each column
	for column in columns:
		conditions.append(f"{column} LIKE ?")
		params.append(f'%{search_value}%')

	# Combine the conditions with OR operator
	where_clause = " OR ".join(conditions)

	query = f"SELECT id, RelatedThreat, Receptor, Event, TypeOfScenario, TPP, ExercisePhase, Subject, Sector, Poll FROM events WHERE "

	# Add the filters to the query
	if filter_phase and filter_sector:
		query += f" ExercisePhase = ? AND Sector LIKE ? AND ( {where_clause} )"
		params.insert(0, f"%{filter_sector}%")
		params.insert(0, filter_phase)
	elif filter_phase:
		query += f" ExercisePhase = ? AND ( {where_clause} )"
		params.insert(0, filter_phase)
	elif filter_sector:
		query += f" Sector LIKE ? AND ( {where_clause} )"
		params.insert(0, f"%{filter_sector}%")
	else:
		query += f" {where_clause}"

	# Order By
	column_index = int(request.form.get('order[0][column]', 0))
	order_direction = request.form.get('order[0][dir]', 'asc')

	columns = ['id', 'RelatedThreat', 'Receptor', 'Event', 'TypeOfScenario', 'TPP', 'ExercisePhase', 'Subject', 'Sector', 'Poll']

	# Validate the column index
	if column_index >= 0 and column_index < len(columns):
		column_name = columns[column_index]
		query += f" ORDER BY {column_name} {order_direction}"

	# Add pagination
	query += " LIMIT ? OFFSET ?"
	params.extend([length, start])

	cursor.execute(query, params)
	rows = cursor.fetchall()

	# Get the total count of filtered records
	query = f"SELECT COUNT(*) FROM events WHERE "
	
	# Add the filters to the query
	if filter_phase and filter_sector:
		query += f" ExercisePhase = ? AND Sector LIKE ? AND ( {where_clause} )"
	elif filter_phase:
		query += f" ExercisePhase = ? AND ( {where_clause} )"
	elif filter_sector:
		query += f" Sector LIKE ? AND ( {where_clause} )"
	else:
		query += f" {where_clause}"

	cursor.execute(query, params[:-2])
	total_filtered_records = cursor.fetchone()[0]

	# Get the total count of all records
	cursor.execute(f"SELECT COUNT(*) FROM events")
	total_records = cursor.fetchone()[0]

	# Prepare the data in JSON format
	data = []
	for row in rows:
		# Create a dictionary for each row
		row_dict = dict(zip(columns, row))

		# Append the row dictionary to the data list
		data.append(row_dict)

	# Close the database connection
	cursor.close()
	conn.close()

	# Prepare the response for DataTables
	response = {
		"draw": draw,
		"recordsTotal": total_records,
		"recordsFiltered": total_filtered_records,
		"data": data
	}

	return jsonify(response)

@bp.route('/msels-data', methods=['POST'])
def get_msels():
	# Connect to the SQLite database
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__)) + '/t3sf.sqlite3')
	cursor = conn.cursor()

	# Get the DataTables request parameters
	draw = int(request.form.get('draw', 0))
	start = int(request.form.get('start', 0))
	length = int(request.form.get('length', 0))
	search_value = request.form.get('search[value]', '')

	# Construct the SQL query with search, pagination, and filter
	columns = ['id', 'Topic', 'Sector', 'Description']
	conditions = []
	params = []
	
	# Generate the WHERE conditions for each column
	for column in columns:
		conditions.append(f"{column} LIKE ?")
		params.append(f'%{search_value}%')

	# Combine the conditions with OR operator
	where_clause = " OR ".join(conditions)

	query = f"SELECT id, Topic, Sector, Description FROM MSELS_info WHERE {where_clause}"

	# Order By
	column_index = int(request.form.get('order[0][column]', 0))
	order_direction = request.form.get('order[0][dir]', 'asc')

	columns = ['id', 'Topic', 'Sector', 'Description']

	# Validate the column index
	if column_index >= 0 and column_index < len(columns):
		column_name = columns[column_index]
		query += f" ORDER BY {column_name} {order_direction}"

	# Add pagination
	query += " LIMIT ? OFFSET ?"
	params.extend([length, start])

	cursor.execute(query, params)
	rows = cursor.fetchall()

	# Get the total count of filtered records
	query = f"SELECT COUNT(*) FROM MSELS_info WHERE {where_clause}"

	cursor.execute(query, params[:-2])
	total_filtered_records = cursor.fetchone()[0]

	# Get the total count of all records
	cursor.execute(f"SELECT COUNT(*) FROM MSELS_info")
	total_records = cursor.fetchone()[0]

	# Prepare the data in JSON format
	data = []
	for row in rows:
		# Create a dictionary for each row
		row_dict = dict(zip(columns, row))

		query = f"SELECT COUNT(*), GROUP_CONCAT(id), GROUP_CONCAT(receptor) FROM MSELS_events WHERE MSEL_ID = ?"

		cursor.execute(query, [row[0]])
		results = cursor.fetchall()

		events_amount = [option[0] for option in results]
		events_ids = [option[1] for option in results]
		receptors_dirt = [option[2] for option in results]

		receptors = ", ".join(list(set(receptors_dirt[0].split(","))))

		row_dict['EventsAmount'] = events_amount
		row_dict['EventsIDs'] = events_ids
		row_dict['Receptors'] = receptors

		# Append the row dictionary to the data list
		data.append(row_dict)

	# Close the database connection
	cursor.close()
	conn.close()

	# Prepare the response for DataTables
	response = {
		"draw": draw,
		"recordsTotal": total_records,
		"recordsFiltered": total_filtered_records,
		"data": data
	}

	return jsonify(response)

@bp.route('/get-injects', methods=['POST'])
def get_injects():
	ids = request.json.get('ids', [])  # Get the IDs from the request body
	source = request.json.get('from', "")  # Get the source/from from the request body

	table = "events"

	if source == "MSEL":
		table = "MSELS_events"

	# Connect to the SQLite database
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__)) + '/t3sf.sqlite3')
	conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row

	cursor = conn.cursor()

	injects = []

	for id in ids:
		# Create a JSON object for each ID based on the data on the DB
		query = f"SELECT Receptor, Event, Subject, Poll FROM {table} WHERE id = ?"

		try:
			# Convert the input to an integer and avoid SQLi
			sanitized_input = int(id)
		except ValueError:
			break
			return None

		cursor.execute(query, [sanitized_input])

		rows = cursor.fetchone()

		if rows is not None:
			inject = {
				'#': '',
				'Real Time': '', 	# We will not provide this info
				'Date': '',		 	# We will not provide this info
				'Subject': rows['Subject'],
				'From': '', 	 	# We will not provide this info
				'Player': rows['Receptor'], 		
				'Script': rows['Event'],
				'Photo': '',	 	# We will not provide this info for now
				'Picture Name': '', # We will not provide this info for now
				'Profile': '',	 	# We will not provide this info for now
				'Poll': rows['Poll']
			}
			injects.append(inject)

	# Close the database connection
	cursor.close()
	conn.close()

	return Response(json.dumps(injects), mimetype='application/json')

@bp.route('/get-filters', methods=['GET'])
def get_data_for_dropdowns():
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__)) + '/t3sf.sqlite3')
	cursor = conn.cursor()
	
	# Execute the query to retrieve the options for ExercisePhase
	cursor.execute("SELECT DISTINCT ExercisePhase FROM events")
	
	# Fetch all the options for ExercisePhase
	phases_options = cursor.fetchall()
	
	# Execute the query to retrieve the options for Sector
	cursor.execute("SELECT DISTINCT Sector FROM events")
	
	# Fetch all the options for Sector
	sector_options = cursor.fetchall()
	
	# Close the database connection
	cursor.close()
	conn.close()
	
	# Convert the options to a list of strings
	phases_options = [option[0] for option in phases_options]
	
	# Convert the comma-separated sectors to individual sectors
	sector_options = [sector[0].split(", ") for sector in sector_options]
	sector_options = [sector for sublist in sector_options for sector in sublist]
	
	# Logical Order for Phases
	phases_order = [
		"Initial Events",
		"Detection Events",
		"Details Events",
		"Exposure Events",
		"Business Events",
		"Communication Events",
		"Decision Events",
		"Resolution Events"
	]

	# Remove duplicates and sort the options
	phases_options = sorted(list(set(phases_options)), key=lambda x: phases_order.index(x))
	sector_options = sorted(list(set(sector_options)))


	
	# Return the options as a JSON response
	return jsonify({'ExercisePhase': phases_options, 'Sector': sector_options})

@bp.route('/framework-status', methods=['GET'])
def framework_status():
	stopped = utils.process_quit
	paused = utils.process_wait
	started = utils.process_started

	if(stopped):
		status = "stop"

	elif(paused):
		status = "pause"

	elif(started):
		status = "start"

	else:
		status = "active"

	# Return the status as a JSON response
	return jsonify({'status': status})