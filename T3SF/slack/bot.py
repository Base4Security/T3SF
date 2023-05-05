from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from .slack import Slack
import warnings
import asyncio
import os, re
import json
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

async def create_environment():
	global T3SF_instance

	T3SF_instance = T3SF.T3SF(platform="slack", app=app_slack)
	areas_msel = T3SF_instance.IncidentsFetcher(MSEL = config_MSEL)
	
	admins_users = await get_admins()

	await create_gm_channels(admins=admins_users)

	try:
		inbox_name = "inbox"
		extra_chnls = ['chat','decision-log']
		players_list_local = areas_msel

		channels_ids = []

		for player in players_list_local:
			inbox =  inbox_name + "-" + player.lower().replace(" ", "-")
			try:
				channel_id_inbox = await create_channel_if_not_exists(channel_name=inbox, private=True)
				
				if channel_id_inbox:
					await app_slack.client.conversations_invite(channel=channel_id_inbox, users=admins_users)
				
					channels_ids.append(channel_id_inbox)

					T3SF.T3SF_Logger.emit(message=f'Player [{player}] - Channel {inbox_name} created', message_type="DEBUG")

				for extra in extra_chnls:
					channel = extra + "-" + player.lower().replace(" ", "-")
				
					channel_id_extra = await create_channel_if_not_exists(channel_name=channel, private=True)
					if channel_id_extra:
						await app_slack.client.conversations_invite(channel=channel_id_extra, users=admins_users)
				
						channels_ids.append(channel_id_extra)

						T3SF.T3SF_Logger.emit(message=f'Player [{player}] - Channel {channel} created', message_type="DEBUG")

			except Exception as e:
				print("ERROR - Create function")
				print(e)
				pass
		
		T3SF.T3SF_Logger.emit(message=f"Player's Channels created!", message_type="INFO")
		print(channels_ids)
		T3SF.T3SF_Logger.emit(message=f'Channels IDs: {channels_ids}', message_type="DEBUG")

	except Exception as e:
		print("ERROR - Create function")
		print(e)
		raise

async def get_admins():
	admins_users = []
	try:
		response = await app_slack.client.users_list()
		# Loop through the list of users and check if they're an admin
		for user in response["members"]:
			try:
				if user["is_admin"]:
					# Store the user ID of the workspace admin
					admins_users.append(user['id'])
			except KeyError:
				pass
		return admins_users

	except SlackApiError as e:
		if e.response["error"] == "ratelimited":
			T3SF.T3SF_Logger.emit(message=f'Slack is rate limiting us. Please wait a few seconds and try again.', message_type="ERROR")

	except Exception as e:
		print("ERROR - Get Admins function")
		print(e)
		raise
	
async def create_channel_if_not_exists(channel_name, private=True):
	try:
		# Call the conversations_list method using the app client
		response = await app_slack.client.conversations_list()

		# Check if a channel with the given name already exists
		channel_id = None
		for channel in response["channels"]:
			if channel["name"] == channel_name:
				channel_id = channel["id"]
				break

		# If the channel doesn't exist, create it using the conversations_create method
		if not channel_id:
			response = await app_slack.client.conversations_create(name=channel_name ,is_private=private)
			channel_id = response["channel"]["id"]

		# Return the ID of the channel
		return channel_id

	except SlackApiError as e:
		if e.response["error"] == "name_taken":
			T3SF.T3SF_Logger.emit(message=f'Channel {channel_name} already taken.', message_type="WARN")
		else:
			print(f"Error: {e}")
		return False

async def create_gm_channels(admins):
	channels = ['gm-chat','gm-logs']
	for channel in channels:
		channel_id = await create_channel_if_not_exists(channel)
		if channel_id:
			await app_slack.client.conversations_invite(channel=channel_id, users=admins)

	T3SF.T3SF_Logger.emit(message=f'Game Master channels created.', message_type="INFO")

	return True