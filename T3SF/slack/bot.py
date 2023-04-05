from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp
from dotenv import load_dotenv
from .slack import Slack
import warnings
import asyncio
import os, re
import T3SF

load_dotenv()


# Disable the UserWarning message
warnings.filterwarnings("ignore", category=UserWarning)

app_slack = None
T3SF_instance = None
config_MSEL = None


class create_bot():
	def __init__(self, MSEL=None):
		global config_MSEL
		config_MSEL = MSEL
		pass

	async def slack_main(self):
		global app_slack
		app_slack = self.app_slack = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

		handler = AsyncSocketModeHandler(self.app_slack, os.environ["SLACK_APP_TOKEN"])

		@app_slack.action(re.compile("regex"))
		async def regex_handler(ack, body, payload):
			await T3SF.T3SF.RegexHandler(self=T3SF_instance,ack=ack,body=body,payload=payload)

		@app_slack.action(re.compile("option"))
		async def poll_handler(ack, body, payload):
			await T3SF.T3SF.PollAnswerHandler(self=T3SF_instance,ack=ack,body=body,payload=payload)

		@app_slack.message("!start")
		async def start(message, say):
			"""
			Retrieves the !start command and starts to fetch and send the incidents.
			"""
			try:
				global T3SF_instance
				T3SF_instance = T3SF.T3SF(platform="slack", app=app_slack)
				await T3SF_instance.ProcessIncidents(MSEL = config_MSEL, function_type = "start", ctx=message)

			except Exception as e:
				print("ERROR - Start function")
				print(e)
				raise

		@app_slack.message('!ping')
		async def ping(message, say):
			"""
			Retrieves the !ping command and replies with this message.
			"""
			description = """
			PING localhost (127.0.0.1): 56 data bytes\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=113 time=37.758 ms\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=113 time=50.650 ms\n64 bytes from 127.0.0.1: icmp_seq=2 ttl=113 time=42.493 ms\n64 bytes from 127.0.0.1: icmp_seq=3 ttl=113 time=37.637 ms\n--- localhost ping statistics ---\n4 packets transmitted, 4 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 37.637/42.135/50.650/5.292 ms\n\n_This is not real xD_"""
			await app_slack.client.chat_postMessage(channel = message['channel'], attachments = Slack.Formatter(color="GREEN", title="🏓 Pong!", description=description))


		@app_slack.event("message")
		async def not_interesting_messages(body, logger):
			pass

		await handler.start_async()

async def start_bot():
	task1 = asyncio.create_task(create_bot(config_MSEL).slack_main())
	T3SF.T3SF_Logger.emit(message=f'Slack Bot is ready!', message_type="DEBUG")
	await asyncio.gather(task1)

async def run_async_incidents():
	global T3SF_instance
	T3SF_instance = T3SF.T3SF(platform="slack", app=app_slack)
	await T3SF_instance.ProcessIncidents(MSEL = config_MSEL, function_type = "start", ctx={"channel":"gm-chat"})