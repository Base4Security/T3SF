import importlib
import asyncio
import signal
import json
import time
import re
import os

# Internal logging
from .logger import T3SF_Logger
# / Internal logging

def keyboard_interrupt_handler(signal_num, frame):
	T3SF_Logger.emit(message=f"KeyboardInterrupt (ID: {signal_num}) has been caught. Exiting...", message_type="WARN")
	os.kill(os.getpid(), signal.SIGTERM)

# Associate the signal handler function with SIGINT (keyboard interrupt)
signal.signal(signal.SIGINT, keyboard_interrupt_handler)


class T3SF(object):
	def __init__(self, bot = None, app = None, platform = None):
		self.response = None
		self.process_wait = False
		self.process_quit = False
		self.regex_ready = None
		self.incidents_running = False
		self.poll_answered = False
		self.ch_names_list = []
		self.players_list = []
		self.platform = platform.lower()
		self.guild_id = None

		try:
			if os.path.isfile(os.getcwd() + f"/inboxes_{self.platform}.json"):
				self.inboxes_all = json.load(open(f"inboxes_{self.platform}.json", encoding='utf-8-sig'))
				self.fetch_inboxes = False

				T3SF_Logger.emit(message="Locally retrieved Inboxes", message_type="DEBUG")
			else:
				self.fetch_inboxes = True 
				self.inboxes_all = {}

		except Exception:
			self.fetch_inboxes = True
			self.inboxes_all = {}

		if self.platform == "discord":
			from .discord import Discord
			self.bot = bot
			self.discord = Discord(bot)

		elif self.platform == "slack":
			from .slack import Slack
			self.app = app
			self.slack = Slack(app)

	async def TimeDifference(self, actual_real_time, previous_real_time, itinerator=int, resumed=bool):
		"""
		This function is used to Get the difference between two injects. It will make the bot sleep and inform the Game Masters.
		"""
		try:
			self.diff = int(actual_real_time) - int(previous_real_time)
			
			if self.diff < 0:
				self.diff_no_real = int(previous_real_time) - int(actual_real_time)
				self.diff = 60 - self.diff_no_real 
			
			self.diff_secs = self.diff * 60
			
			if resumed != True:     
				itinerator = itinerator + 1

			description = f"The bot is Up and running!\n\nIncident: {itinerator}/{len(self.data)}\n\nWaiting {self.diff} minute(s) ({self.diff_secs} sec.) to send it."

			# await self.EditMessage(style="simple", color = "CYAN", title="⚙️ Bot running...", description=description, response=self.msg_gm)

			T3SF_Logger.emit(f'We have a difference of {self.diff} minute(s) - {self.diff_secs} seconds', message_type="INFO")
			
			await asyncio.sleep(self.diff_secs)

			if "Poll" in self._inject and self._inject['Poll'] != '' and self.poll_answered == False:
				description = self._inject["Script"] + f"\n\n@channel Poll not answered within {self.diff} minute(s), Time's Up!"
				await self.EditMessage(style="custom", variable="T3SF_instance.response_poll", color = "RED", title="Poll time ended!", description=description, response=self.response_poll)
				await self.NotifyGameMasters(type_info="poll_unanswered", data={'msg_poll':self._inject["Script"]}) 

		except Exception as e:
			print("Get Time Difference")
			print(e)
			T3SF_Logger.emit("Get Time Difference", message_type="ERROR")
			T3SF_Logger.emit(e, message_type="ERROR")
			raise

	def IncidentsFetcher(self, MSEL:str):
		"""
		Retrieves the incidents from the desired source, chosen in the config file.
		"""
		T3SF_Logger.emit(message="Reading MSEL", message_type="DEBUG")
		if MSEL:
			self.data = json.load(open(MSEL, encoding='utf-8-sig'))

			for inject in self.data:
				player = inject['Player']
				if player not in self.players_list:
					self.players_list.append(player)
			T3SF_Logger.emit(message="We have the inboxes right now", message_type="DEBUG")
			T3SF_Logger.emit(message="Incidents ready", message_type="DEBUG")
			return self.players_list
		else:
			raise RuntimeError("Please set a method to retrieve the TTXs with the argument `MSEL` inside the `start` function.")

	async def start(MSEL:str, platform, gui=False):
		if gui == True:
			T3SF_Logger.emit(message="Starting GUI", message_type="DEBUG")
			gui_module = importlib.import_module("T3SF.gui.core")
			gui_module.GUI(platform_run=platform, MSEL=MSEL)
		
		if platform.lower() == "slack":
			bot_module = importlib.import_module("T3SF.slack.bot")

		elif platform.lower() == "discord":
			bot_module = importlib.import_module("T3SF.discord.bot")

		else:
			raise ValueError("Invalid platform")

		T3SF_Logger.emit(message="Starting BOT", message_type="DEBUG")
		bot_module.create_bot(MSEL=MSEL)
		await bot_module.start_bot()

	async def NotifyGameMasters(self, type_info=str, data=None):
		"""
		Notify the Game Masters of the different states of the bot, through messages.
		"""
		try:
			if type_info == "start_normal":
				title = "⚙ Starting bot..."
				description = "The bot it's heating up!\n\nGive us just a second!!"
				# self.msg_gm = await self.SendMessage(title = title, description = description, color="YELLOW")

			elif type_info == "started_normal":
				title = "Bot succesfully started! 🎈"
				description = "The bot is Up and running!\n\nLets the game begin!!"
				# self.msg_gm = await self.EditMessage(title = title, description = description, color="GREEN", response=self.msg_gm)
			
			elif type_info == "start_resumed":
				title = "⚙ Resuming bot..."
				description = "The bot it's trying to resume from the desired point!\n\nGive us just a few seconds!!"
				# self.msg_gm = await self.SendMessage(title = title, description = description, color="YELLOW")
			
			elif type_info == "started_resumed":
				title = "Bot succesfully started! 🎈"
				description = "The bot is Up and running!\n\nLets the game begin!!"
				# self.msg_gm = await self.EditMessage(title = title, description = description, color="GREEN", response=self.msg_gm)
			
			elif type_info == "finished_incidents":
				title = "🎉 Bot Finished succesfully! 🎉"
				description = "The bot've just completed the entire game!\n\nHope to see you again soon!!"
				# self.msg_gm = await self.EditMessage(title = title, description = description, color="GREEN", response=self.msg_gm)

			elif type_info == "poll_answered":
				title = "📊 Poll Answered"
				description = f"Poll Question: {data['msg_poll']}\nSelected Answer: {data['answer']}\nBy: @{data['user']}"
				# await self.SendMessage(title = title, description = description, color="GREEN", unique=True)

			elif type_info == "poll_unanswered":
				title = "📊 Poll Not Answered"
				description = f"Poll Question: {data['msg_poll']}\nNot answered by anyone."
				# await self.SendMessage(title = title, description = description, color="RED", unique=True)

			T3SF_Logger.emit(message=description, message_type="INFO")
			return True

		except Exception as e:
			print("NotifyGameMasters")
			print(e)
			T3SF_Logger.emit("NotifyGameMasters", message_type="ERROR")
			T3SF_Logger.emit(e, message_type="ERROR")
			raise

	async def ProcessIncidents(self, MSEL:str, ctx, function_type:str=None, itinerator:int=0):
		"""
		Process the incidents from the MSEL file.
		"""
		self.IncidentsFetcher(MSEL)
		try:
			self._ctx = ctx

			await self.InboxesAuto()

			while self.regex_ready == False:
				await asyncio.sleep(2)

			if function_type == "start":
				await self.NotifyGameMasters(type_info="start_normal")  # Sends a message regarding the bot's start procedure.
			else:
				await self.NotifyGameMasters(type_info="start_resumed")  # Sends a message regarding the bot's restart procedure.
			
			bypass_time = True

			for information in self.data:
				if self.process_quit == True:
					break
				
				if self.process_wait == True:
					while self.process_wait == True:
						await asyncio.sleep(5)

				if itinerator == 0: # Set a variable to get the actual timestamp and the past one, after that checks for differences.
					itinerator_loop = itinerator
				else:
					if function_type == "resume":
						itinerator_loop = itinerator - 2
					else:
						itinerator_loop = itinerator - 1
				
				if int(information["#"]) != itinerator and function_type == "resume": # Checks if the incident ID is the same as the desired starting point.
					pass
				
				else:
					actual_real_time = re.sub("([^0-9])", "", information["Real Time"])[-2:]
					
					previous_real_time = re.sub("([^0-9])", "", self.data[itinerator_loop]["Real Time"])[-2:]
					
					T3SF_Logger.emit(f"Previous {previous_real_time} - Actual {actual_real_time}", message_type="DEBUG")

					if previous_real_time != actual_real_time and function_type == "start":
						await self.TimeDifference(actual_real_time, previous_real_time, resumed=False, itinerator=itinerator) # Check the amount of seconds between both timestamps.

					elif previous_real_time != actual_real_time and bypass_time != True:
						await self.TimeDifference(actual_real_time, previous_real_time, resumed=True, itinerator=itinerator) # Check the amount of seconds between both timestamps.

					T3SF_Logger.emit(f'Inject {information["#"]}/{len(self.data)}', message_type="INFO")

					if "Poll" in information and information['Poll'] != '':
						await self.SendPoll(inject = information)
						
					else:
						await self.SendIncident(inject = information) # Sends the incident to the desired chats.

					if function_type == "start":
						if itinerator == 0:
							await self.NotifyGameMasters(type_info="started_normal") # Informs that the bot succesfully started.
					else:
						if bypass_time == True:
							await self.NotifyGameMasters(type_info="started_resumed") # Informs that the bot succesfully restarted.
							bypass_time = False

					itinerator += 1
			
			await self.NotifyGameMasters(type_info="finished_incidents") # Informs that the script is completed and there's no remaining incidents.
			self.process_quit = False
			self.process_wait = False
			self.incidents_running = False

		except Exception as e:
			print("ProcessIncidents function")
			print(e)
			T3SF_Logger.emit("ProcessIncidents function", message_type="ERROR")
			T3SF_Logger.emit(e, message_type="ERROR")
			raise

	async def SendIncident(self, inject):
		try:
			self._inject = inject

			if self.platform == "discord":
				await self.discord.InjectHandler(T3SF_instance=self)

			elif self.platform == "slack":
				await self.slack.InjectHandler(T3SF_instance=self)

			return True

		except Exception as e:
			print("SendIncident")
			print(e)
			T3SF_Logger.emit("SendIncident", message_type="ERROR")
			T3SF_Logger.emit(e, message_type="ERROR")
			raise

	async def SendPoll(self, inject):
		try:
			self._inject = inject

			if self.platform == "discord":
				await self.discord.PollHandler(T3SF_instance=self)

			elif self.platform == "slack":
				await self.slack.PollHandler(T3SF_instance=self)

			return True

		except Exception as e:
			print("SendPoll")
			print(e)
			T3SF_Logger.emit("SendPoll", message_type="ERROR")
			T3SF_Logger.emit(e, message_type="ERROR")
			raise

	async def InboxesAuto(self, message=None):
		if self.platform == "discord":
			await self.discord.InboxesAuto(T3SF_instance=self)

		elif self.platform == "slack":
			await self.slack.InboxesAuto(T3SF_instance=self, regex=None)
	
	async def RegexHandler(self, ack=None, body=None, payload=None, inbox=None):
		if self.platform == "slack":
			await ack()
			text_input = None
			image = None
			regex = None

			if payload['action_id'] == "regex_yes":
				regex = body['actions'][0]['value']
				color="GREEN"
				title = "✨ Regex detected succesfully! ✨"
				description = f"Thanks for confirming the regex detected for the channels (I'm going to tell my creator he is so good coding :D ), we are going to use `{regex}` to match the inboxes"

			elif payload['action_id'] == "regex_no":
				color="RED"
				title = "ℹ️ Regex needed!"
				description = "Got it!\n Unluckily, but here we go...\nPlease send me the regex for the channels, so we can get the inboxes!\n\nExample:\ninbox-legal\nThe regex should be `inbox-`"
				text_input = {"action_id": "regex_custom", "label": "Please type the desired regex. EG: inbox-", "dispatch_action": True}
				image = {"image_url":"https://i.ibb.co/34rTqMH/image.png", "name": "regex"}

			elif payload['action_id'] == "regex_custom":
				regex = body['actions'][0]['value']
				color="GREEN"
				title="✅ Regex accepted!"
				description=f"Thanks for confirming the regex for the channels, we are going to use `{user_regex}` to match the inboxes!"

			self.response_auto = await self.EditMessage(title = title, description = description, color=color, image=image, text_input=text_input, response=self.response_auto)

			if regex != None:
				await self.slack.InboxesAuto(T3SF_instance=self, regex=regex)

	async def PollAnswerHandler(self, ack=None, body=None, payload=None, query=None):
		if self.platform == "discord":
			await self.discord.PollAnswerHandler(T3SF_instance=self, interaction=payload)
			return True

		elif self.platform == "slack":
			await ack()
			await self.slack.PollAnswerHandler(T3SF_instance=self, body=body, payload=payload)
			return True

	async def SendMessage(self,
		color=None, 
		title:str=None, 
		description:str=None, 
		channel=None, 
		image=None, 
		author=None, 
		buttons=None, 
		text_input=None, 
		checkboxes=None,
		view=None,
		unique=False,
		reply_markup=None):

		if self.platform == "discord":
			if unique == True:
				self.gm_poll_msg = await self.discord.SendMessage(T3SF_instance=self, color=color, title=title, description=description, view=view, unique=unique)
				return self.gm_poll_msg
			else:
				self.response = await self.discord.SendMessage(T3SF_instance=self, color=color, title=title, description=description, view=view)
				return self.response

		elif self.platform == "slack":
			self.response = await Slack.SendMessage(self=self.slack, channel = channel, title=title, description=description, color=color, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes)
			return self.response

	async def EditMessage(self,
		color=None, 
		style:str="simple", 
		title:str=None, 
		description:str=None,
		response=None, 
		variable=None, 
		image=None, 
		author=None, 
		buttons=None, 
		text_input=None, 
		checkboxes=None,
		view=None,
		reply_markup=None):

		if self.platform == "discord":
			if style == "simple":
				self.response = await self.discord.EditMessage(T3SF_instance=self, color=color, title=title, description=description, view=view)
				return self.response
			else:
				self.response = await self.discord.EditMessage(T3SF_instance=self, color=color, title=title, description=description, view=view, variable=variable, style="custom")
				return self.response

		elif self.platform == "slack":
			self.response = await self.slack.EditMessage(response=response, title=title, description=description, color=color, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes)
			return self.response