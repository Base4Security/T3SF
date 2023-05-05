from flask import Flask, render_template, Response, stream_with_context, Blueprint, request
import os, signal, time
import threading
import logging
import uuid
import queue
from datetime import datetime
import json

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
		print(" * GUI active on - http://127.0.0.1:5000")
		self.run(debug=False, threaded=True, use_reloader=False)

	def start(self):
		flask_app_thread = threading.Thread(target=self.start_flask_app)
		flask_app_thread.start()

listeners = [] 
class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

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

@bp.route('/')
def index():
	return render_template('index.html', active_page="logs_viewer", platform=platform.lower())

@bp.route('/msel-viewer')
def msel_viewer():
	return render_template('msel_viewer.html', active_page="msel_viewer")

@bp.route('/env-creation')
def env_creation():
	from T3SF import T3SF
	T3SF = T3SF(platform=platform.lower())
	T3SF.IncidentsFetcher(MSEL=msel_file)

	return render_template('env_creation.html', active_page="env_creation", T3SF=T3SF)

@bp.route('/start')
async def start_exercise():
	# Start the async task

	if platform.lower() == "discord":
		from T3SF.discord.bot import run_async_incidents
		server_id = request.args.get("server")
		await run_async_incidents(server=server_id)

	elif platform.lower() == "slack":
		from T3SF.slack.bot import run_async_incidents
		await run_async_incidents()

	# Return an immediate response
	return Response("Started", mimetype='text/plain')

@bp.route('/stop')
def stop_exercise():
	# Kill the slack bot
	msg = {"id" : str(uuid.uuid4()),"type" : "INFO","content": "Exiting...","timestamp": datetime.now().strftime("%H:%M:%S")}
	MessageAnnouncer().announce(msg=f"data: {json.dumps(msg)}\n\n")
	time.sleep(1)
	os.kill(os.getpid(), signal.SIGTERM)

	# Return a response that triggers the WSGI server to shutdown the application
	return 'Shutting down...'

@bp.route('/create')
async def create_env():
	if platform.lower() == "discord":
		from T3SF.discord.bot import create_environment
		server_id = request.args.get("server")
		await create_environment(server=server_id)

	elif platform.lower() == "slack":
		from T3SF.slack.bot import create_environment
		await create_environment()

	return "Created"

@bp.route('/clear')
def clear_logs():
	# Clear the logs
	open('logs.txt', 'w').close()

	# Return a response
	return 'Logs cleared...'