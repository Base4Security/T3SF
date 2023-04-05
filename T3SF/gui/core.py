from flask import Flask, render_template, Response, stream_with_context, Blueprint
from T3SF import T3SF_Logger
import os, signal, time
import threading
import logging
import uuid

bp = Blueprint('t3sf', __name__)

platform = None


class GUI(Flask):
	def __init__(self, platform_run, import_name=__name__, *args, **kwargs):
		global platform
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

@bp.route('/stream')
def stream():
	def generate_logs():
		with open('logs.txt') as f:
			for line in f:
				yield line
	return Response(stream_with_context(generate_logs()), mimetype='text/event-stream')

@bp.route('/')
def index():
	return render_template('index.html')

@bp.route('/start')
async def start_exercise():
	# Start the async task

	if platform.lower() == "discord":
		from T3SF.discord.bot import run_async_incidents
	elif platform.lower() == "slack":
		from T3SF.slack.bot import run_async_incidents

	await run_async_incidents()

	# Return an immediate response
	return Response("Started", mimetype='text/plain')

@bp.route('/stop')
def stop_exercise():
	# Kill the slack bot
	T3SF_Logger.emit(message="Exiting...", message_type="INFO")
	time.sleep(3)
	os.kill(os.getpid(), signal.SIGTERM)

	# Return a response that triggers the WSGI server to shutdown the application
	return 'Shutting down...'

@bp.route('/clear')
def clear_logs():
	# Clear the logs
	open('logs.txt', 'w').close()

	# Return a response
	return 'Logs cleared...'