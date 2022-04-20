from difflib import SequenceMatcher
from collections import Counter
from datetime import datetime
import configparser
import asyncio
import random
import json
import time
import os
import re

config = configparser.ConfigParser()
config.read(os.getcwd() + "/config.ini")
platform = config.get('General', 'Platform')

if platform.lower() == "discord":
	try:
		import discord
		from blurple import ui
	except Exception as e:
		print(e)

class T3SF(object):
	def __init__(self, bot = None, app = None):
		self.response = None
		self.process_wait = False
		self.process_quit = False
		self.regex_ready = None
		self.incidents_running = False
		self.ch_names_list = []
		self.players_list = []

		self.config = configparser.ConfigParser()
		self.config.read(os.getcwd() + "/config.ini")
		self.platform = self.config.get('General', 'Platform').lower()
		try:
			if os.path.isfile(os.getcwd() + f"/inboxes_{self.platform}.json"):
				self.inboxes_all = json.load(open(f"inboxes_{self.platform}.json", encoding='utf-8-sig'))
				self.fetch_inboxes = False
			else:
				self.fetch_inboxes = True 
				self.inboxes_all = {}
		
		except Exception:
			self.fetch_inboxes = True
			self.inboxes_all = {}

		if bot != None:
			self.bot = bot
			if self.platform != "discord" and self.platform != "telegram" and self.platform != "whatsapp":
				raise RuntimeError("Please set the correct platform in the config file or choose the correct bot.")

		elif app != None:
			self.app = app
			if self.platform != "slack":
				raise RuntimeError("Please set the correct platform in the config file or choose the correct bot.")

		self.IncidentsFetcher()

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

			await self.EditMessage(style="simple", color_ds = "ui.Style.INFO", color_sl = "CL_CYAN", title="⚙️ Bot running...", description=description, response=self.msg_gm)

			print(f'We have a difference of {self.diff} minute(s) - {self.diff_secs} seconds (Actual time: {datetime.now().strftime("%H:%M:%S")})')
			
			await asyncio.sleep(self.diff_secs)

		except Exception as e:
			print("ERROR - Get Time Difference")
			print(e)
			raise

	def IncidentsFetcher(self):
		"""
		Retrieves the incidents from the desired source, chosen in the config file.
		"""
		if self.config.get('General', 'TTX_File') != "" :
			self.data = json.load(open(self.config.get('General', 'TTX_File'), encoding='utf-8-sig'))

			for inject in self.data:
				player = inject['Player']
				if player not in self.players_list:
					self.players_list.append(player)

			return True

		else:
			raise RuntimeError("Please set a method to retrieve the TTXs from in the config.ini file.")

	def similar(self, a, b):
		"""
		Based in graphics, find the similarity between 2 strings.
		"""
		return SequenceMatcher(None, a, b).ratio()

	def regex_finder(self, input):
		"""
		Matches repeated words counting the 
		amount of times the word is being repeated.
		"""
		words = input.split('-')
		dict = Counter(words)
		for key in words:
			if dict[key]>1:
				return key
		return False

	async def NotifyGameMasters(self, type_info=str):
		"""
		Notify the Game Masters of the different states of the bot, through messages.
		"""
		try:
			if type_info == "start_normal":
				title = "⚙ Starting bot..."
				description = "The bot it's heating up!\n\nGive us just a second!!"
				self.msg_gm = await self.SendMessage(title = title, description = description, color_ds="ui.Style.WARNING", color_sl="CL_YELLOW")

			elif type_info == "started_normal":
				title = "Bot succesfully started! 🎈"
				description = "The bot is Up and running!\n\nLets the game begin!!"
				self.msg_gm = await self.EditMessage(title = title, description = description, color_ds="ui.Style.SUCCESS", color_sl="CL_GREEN", response=self.msg_gm)
			
			elif type_info == "start_resumed":
				title = "⚙ Resuming bot..."
				description = "The bot it's trying to resume from the desired point!\n\nGive us just a few seconds!!"
				self.msg_gm = await self.SendMessage(title = title, description = description, color_ds="ui.Style.WARNING", color_sl="CL_YELLOW")
			
			elif type_info == "started_resumed":
				title = "Bot succesfully started! 🎈"
				description = "The bot is Up and running!\n\nLets the game begin!!"
				self.msg_gm = await self.EditMessage(title = title, description = description, color_ds="ui.Style.SUCCESS", color_sl="CL_GREEN", response=self.msg_gm)
			
			elif type_info == "finished_incidents":
				title = "🎉 Bot Finished succesfully! 🎉"
				description = "The bot've just completed the entire game!\n\nHope to see you again soon!!"
				self.msg_gm = await self.EditMessage(title = title, description = description, color_ds="ui.Style.SUCCESS", color_sl="CL_GREEN", response=self.msg_gm)

			return True

		except Exception as e:
			print("ERROR - NotifyGameMasters")
			print(e)
			raise

	async def ProcessIncidents(self, ctx, function_type:str=None, itinerator:int=0):
		"""
		Process the incidents from the MSEL file.
		"""
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
					
					print(f"Previous {previous_real_time} - Actual {actual_real_time}")

					if previous_real_time != actual_real_time and function_type == "start":
						await self.TimeDifference(actual_real_time, previous_real_time, resumed=False, itinerator=itinerator) # Check the amount of seconds between both timestamps.

					elif previous_real_time != actual_real_time and bypass_time != True:
						await self.TimeDifference(actual_real_time, previous_real_time, resumed=True, itinerator=itinerator) # Check the amount of seconds between both timestamps.

					print(f'{information["#"]}\n------------\n')
					
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
			print("ERROR - ProcessIncidents function")
			print(e)
			raise

	async def SendIncident(self, inject):
		try:
			self._inject = inject

			if self.platform == "discord":
				await self.Discord.InjectHandler(self=self)

			elif self.platform == "slack":
				await self.Slack.InjectHandler(self=self)

			elif self.platform == "telegram":
				await self.Telegram.InjectHandler(self=self)

			elif self.platform == "whatsapp":
				await self.Whatsapp.InjectHandler(self=self)

			return True

		except Exception as e:
			print("ERROR - SendIncident")
			print(e)
			raise

	async def InboxesAuto(self, message=None):
		if self.platform == "discord":
			await self.Discord.InboxesAuto(self=self)

		elif self.platform == "slack":
			await self.Slack.InboxesAuto(self=self, regex=None)

		elif self.platform == "telegram":
			await self.Telegram.InboxesAuto(self=self,message=message)

		elif self.platform == "whatsapp":
			await self.Whatsapp.InboxesAuto(self=self)
	
	async def RegexHandler(self, ack=None, body=None, payload=None, inbox=None):
		if self.platform == "slack":
			await ack()
			text_input = None
			image = None
			regex = None

			if payload['action_id'] == "regex_yes":
				regex = body['actions'][0]['value']
				color="CL_GREEN"
				title = "✨ Regex detected succesfully! ✨"
				description = f"Thanks for confirming the regex detected for the channels (I'm going to tell my creator he is so good coding :D ), we are going to use `{regex}` to match the inboxes"

			elif payload['action_id'] == "regex_no":
				color="CL_RED"
				title = "ℹ️ Regex needed!"
				description = "Got it!\n Unluckily, but here we go...\nPlease send me the regex for the channels, so we can get the inboxes!\n\nExample:\ninbox-legal\nThe regex should be `inbox-`"
				text_input = {"action_id": "regex_custom", "label": "Please type the desired regex. EG: inbox-", "dispatch_action": True}
				image = {"image_url":"https://i.ibb.co/34rTqMH/image.png", "name": "regex"}

			elif payload['action_id'] == "regex_custom":
				regex = body['actions'][0]['value']
				color="CL_GREEN"
				title="✅ Regex accepted!"
				description=f"Thanks for confirming the regex for the channels, we are going to use `{user_regex}` to match the inboxes!"

			self.response_auto = await self.EditMessage(title = title, description = description, color_sl=color, image=image, text_input=text_input, response=self.response_auto)

			if regex != None:
				await self.Slack.InboxesAuto(self=self,regex=regex)
		
		elif self.platform == "whatsapp":
			self._ctx = inbox
			await self.Whatsapp.InboxFetcher(self=self, inbox=inbox)

	async def SendMessage(self,
		color_sl=None,
		color_ds=None, 
		title:str=None, 
		description:str=None, 
		channel=None, 
		image=None, 
		author=None, 
		buttons=None, 
		text_input=None, 
		checkboxes=None):

		if self.platform == "discord":
			self.response = await self.Discord.SendMessage(self=self, color_ds=color_ds, title=title, description=description)
			return self.response

		elif self.platform == "slack":
			self.response = await self.Slack.SendMessage(self=self, channel = channel, title=title, description=description, color_sl=color_sl, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes)
			return self.response

		elif self.platform == "telegram":
			response = await self.Telegram.SendMessage(self=self, title=title, description=description, ctx=self._ctx)
			return response

		elif self.platform == "whatsapp":
			await self.Whatsapp.SendMessage(self=self, title=title, description=description, chat=self._ctx["Chat_Name"])

	async def EditMessage(self, 
		color_sl=None, 
		color_ds=None, 
		style:str="simple", 
		title:str=None, 
		description:str=None,
		response=None, 
		variable=None, 
		image=None, 
		author=None, 
		buttons=None, 
		text_input=None, 
		checkboxes=None):

		if self.platform == "discord":
			if style == "simple":
				self.response = await self.Discord.EditMessage(self=self, color_ds=color_ds, title=title, description=description)
				return self.response
			else:
				variable = eval(variable)
				await variable.edit(embed=ui.Alert(eval(color_ds), title = title, name=False, emoji=False, description = description))

		elif self.platform == "slack":
			self.response = await self.Slack.EditMessage(self=self, response=response, title=title, description=description, color_sl=color_sl, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes)
			return self.response

		elif self.platform == "telegram":
			response = await self.Telegram.EditMessage(self=self, title=title, description=description, response=response)
			return response

		elif self.platform == "whatsapp":
			#Whatsapp doesn't have the option to edit messages, so we are just going to send another message...
			await self.Whatsapp.SendMessage(self=self, title=title, description=description, chat=self._ctx["Chat_Name"])

	class Telegram():

		async def InboxesAuto(self, message=None):
			if self.fetch_inboxes == True or len(self.players_list) != len(self.inboxes_all):
				if message == None:
					if len(self.players_list) != len(self.inboxes_all):
						title="❌ Not enough inboxes ❌"
						description=f"We don't have enough inboxes to start the bot.\nPlease add the Inbox Channels for players sending the command `!add` to the channel.\n\nWe have {len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).\n\nAll the inboxes:\n{self.inboxes_all}"
						await self.Telegram.SendMessage(self=self, ctx=self._ctx, title=title, description=description)
					else:
						title="✅ Ready to play!"
						description=f"We collected enough inboxes to start the bot.\nPlease start the bot one more time!"
						await self.Telegram.SendMessage(self=self, ctx=self._ctx, title=title, description=description)

						self.fetch_inboxes = False
				
				elif "!add" in message.text:
					for player in self.players_list:
						accuracy = self.similar(str(message.chat.title).lower(),str(player).lower())
						if accuracy >= 0.4:
							self.inboxes_all[player] = message.chat.id
							json.dump(self.inboxes_all,open(f"inboxes_{self.platform}.json", "w"))
							await message.reply(f"Got it!\nChannel added!\n{player}[{message.chat.id}]\nWe have {len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).\n\nAll the inboxes:\n{self.inboxes_all}")

				self.regex_ready = False
			
			elif len(self.players_list) == len(self.inboxes_all):
				mensaje_inboxes = ""
				for player in self.inboxes_all:
					mensaje_inboxes += f"*Inbox* {player} \[{self.inboxes_all[player]}]\n"
				await self.Telegram.SendMessage(self=self, ctx=self._ctx, title=f"📩 Inboxes fetched! \n{len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).", description=mensaje_inboxes)
				self.regex_ready = True
			
			else:
				mensaje_inboxes = ""
				for player in self.inboxes_all:
					mensaje_inboxes += f"*Inbox* {player} \[{self.inboxes_all[player]}]\n"
				await self.Telegram.SendMessage(self=self, ctx=self._ctx, title=f"📩 Inboxes fetched! \n{len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).", description=mensaje_inboxes)
				self.regex_ready = True

		async def InjectHandler(self):
			all_data = f'*Date*: {self._inject["Date"]}\n*From*: {self._inject["From"]}\n\n{self._inject["Script"]}'

			player = self._inject['Player']
			image = None
			if not (self._inject.get('Photo') is None):
				image = self._inject['Photo']
				
			await self.Telegram.SendMessage(self=self, title=self._inject["Subject"], description=all_data, player=self.inboxes_all[player], image=image)

		async def SendMessage(self, title, description, ctx=None, player=None, image=None):
			data = f"*{title}*\n\n{description}"

			if player != None:
				chat_id = player
			else:
				chat_id = self._ctx.chat.id

			if image != None:
				response = await self.bot.send_photo(chat_id=chat_id, caption=data, photo=image, parse_mode = 'Markdown')
			else:
				response = await self.bot.send_message(chat_id, data, parse_mode = 'Markdown')
			return response

		async def EditMessage(self, title, description, response, image=None):
			text = f"*{title}*\n\n{description}"
			response = await response.edit_text(text=text, parse_mode = 'Markdown')
			return response

	class Discord():

		async def InboxesAuto(self):
			mensaje_inboxes = ""
			image_example = "https://i.ibb.co/NCrPD3Y/discord-exp.png"

			if self.fetch_inboxes == True:

				self.response_auto = await self.SendMessage(title="⚙️ Fetching inboxes...", description=f"Please wait while we fetch all the inboxes in this server!", color_ds="ui.Style.INFO")

				channels = self._ctx.message.guild.channels

				channels_itinerator = 0
				player_itinerator = 0
				regex = ""

				while regex == "" and len(self.players_list) > player_itinerator:
					for category in self._ctx.message.guild.categories:
						if channels_itinerator == 0:
							past_channel = category.name
							pass
						
						match_channel = self.similar(str(category).lower(), str(self.players_list[0]).lower())
						
						if match_channel >= 0.4:
							for character in past_channel:
								if character in category.name:
									regex += character
								else:
									break
						else:
							player_itinerator += 1
							channels_itinerator += 1
							past_channel = category.name
							pass

				await self.response_auto.edit(embed=discord.Embed(
				 title = "ℹ️ Regex detected!",
				 description = f"Please confirm if the regex detected for the channels, is correct so we can get the inboxes!\n\nExample:\nGroup - Legal\nThe regex should be `Group -`\n\nDetected regex: `{regex}`",
				 color = 0x77B255).set_image(url=image_example).set_footer(text="Please answer with [Yes(Y)/No(N)]"))

				def check_regex_channels(msg):
					return msg.author == self._ctx.author and msg.channel == self._ctx.channel and msg.content.lower() in ["y", "yes", "n", "no"]
				
				try:
					msg = await self.bot.wait_for("message", check=check_regex_channels, timeout=50)

					if msg.content.lower() in ["y", "yes"]:
						await self.EditMessage(style="custom", variable="self.response_auto", color_ds="ui.Style.SUCCESS", title = "✨ Regex detected succesfully! ✨", description = f"Thanks for confirming the regex detected for the channels (I'm going to tell my creator he is so good coding :D ), we are going to use `{regex}` to match the inboxes")

					elif msg.content.lower() in ["n", "no"]:
						await self.response_auto.edit(embed=discord.Embed(
						 title = "ℹ️ Regex needed!",
						 description = "Got it!\n Unluckily, but here we go...\nPlease send me the regex for the channels, so we can get the inboxes!\n\nExample:\nGroup - Legal\nThe regex should be `Group -`",
						 color = discord.Colour.red()).set_image(url=image_example).set_footer(text="Please answer with the desired regex. EG: `Groups -`"))

						def get_regex_channels(msg_regex_user):
							return msg_regex_user.author == self._ctx.author and msg_regex_user.channel == self._ctx.channel and msg_regex_user.content != ""
						
						msg_regex_user = await self.bot.wait_for("message", check=get_regex_channels, timeout=50)

						if msg_regex_user.content != "":
							regex = msg_regex_user
							await self.EditMessage(style="custom", variable="self.response_auto", color_ds="ui.Style.SUCCESS", title="✅ Regex accepted!", description=f"Thanks for confirming the regex for the channels, we are going to use `{msg_regex_user.content}` to match the inboxes!")

				except asyncio.TimeoutError:
					await self.EditMessage(style="custom", variable="self.response_auto", color_ds="ui.Style.DANGER", title = ":x: Sorry, you didn't reply on time", description = "Please start the process again.")
					raise RuntimeError("We didn't detect any regex, time's up.")

				for player in self.players_list:
					for channel in channels:
						category = channel.category
						if "inbox" in channel.name :
							accuracy = self.similar(re.sub(f"({regex})", "",str(category)).lower(),str(player).lower())
							if accuracy >= 0.4:
								self.inboxes_all[player] = channel.id
				
				json.dump(self.inboxes_all,open(f"inboxes_{self.platform}.json", "w"))

				for player in self.inboxes_all:
					mensaje_inboxes += f"**Inbox** {player}[{self.inboxes_all[player]}]\n"

				await self.EditMessage(style="custom", variable="self.response_auto", color_ds="ui.Style.SUCCESS", title=f"📩  Inboxes fetched! [{len(self.inboxes_all)}]", description=mensaje_inboxes)

			return True

		async def InjectHandler(self):
			all_data = f'Date: {self._inject["Date"]}\n\n{self._inject["Script"]}'

			player = self._inject['Player']

			inbox = self.bot.get_channel(self.inboxes_all[player])

			embed = discord.Embed(title = self._inject['Subject'], description = all_data, color = discord.Colour.blue())
			
			if not (self._inject.get('Photo') is None):
				embed.set_image(url=self._inject['Photo'])
			
			if not (self._inject.get('Profile') is None):
				profile_pic = self._inject['Profile']
			else:
				profile_pic = random.choice([
					"https://ssl.gstatic.com/ui/v1/icons/mail/profile_mask2.png",
					"https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg",
					"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTt8Dg9RL4IGOjsJ2Fr-lXThf-DGM5YgPB6j5rD8tHQ9RLrU-03H4dYeskL01FNajqL_0&usqp=CAU"
				])

			embed.set_author(name=self._inject["From"], icon_url=profile_pic)

			await inbox.send(embed = embed)

			return embed

		async def SendMessage(self, color_ds=None, title:str=None, description:str=None):
			self.response = await self._ctx.send(embed=ui.Alert(eval(color_ds), title = title, name=False, emoji=False, description = description))
			return self.response

		async def EditMessage(self, color_ds=None, title:str=None, description:str=None):
			await self.response.edit(embed=ui.Alert(eval(color_ds), title = title, name=False, emoji=False, description = description))
			return self.response

	class Slack():

		def Formatter(title=None, description=None, color="#5bc0de", image=None, author=None, buttons=None, text_input=None, checkboxes=None):
			CL_BLUE = "#428bca"
			CL_RED = "#d9534f"
			CL_WHITE = "#f9f9f9"
			CL_CYAN = "#5bc0de"
			CL_GREEN = "#5cb85c"
			CL_ORANGE = "#ffa700"
			CL_YELLOW = "#ffff00"

			fallback_text = ""
			color = eval(color)
			result =[
						{
							"color": color,
							"blocks": []
						}
					]

			if title != None:
				title_list = [
								{
									"type": "header",
									"text": {
										"type": "plain_text",
										"text": title
									}
								},
								{
									"type": "divider"
								}
							]

				result[0]["blocks"] = title_list

			if description != None:
				desc_list = {
								"type": "section",
								"text": {
									"type": "mrkdwn",
									"text": description
								}
							}
				result[0]["blocks"].append(desc_list)

			else:
				description = "Preview not available."

			if image != None:
				fallback_text = "🖼 "
				image_list = {
								"type": "image",
								"title": {
									"type": "plain_text",
									"text": image["name"],
									"emoji": True
								},
								"image_url": image["image_url"],
								"alt_text": "image"
							}
				result[0]["blocks"].append(image_list)

			if author != None:
				author_list = [{
								"type": "context",
								"elements": [
									{
										"type": "image",
										"image_url": author["image_url"],
										"alt_text": author["name"]
									},
									{
										"type": "mrkdwn",
										"text": author["name"],
									},
									{
										"type": "mrkdwn",
										"text": " |  *" + author["date"] + "*",
									}
								]
							  }]
				result[0]["blocks"][1:1] = author_list

			if text_input != None:
				input_list = {
								"block_id": "input_texto",
								"dispatch_action": text_input['dispatch_action'],
								"type": "input",
								"element": {
									"type": "plain_text_input",
									"action_id": text_input["action_id"]
								},
								"label": {
									"type": "plain_text",
									"text": text_input["label"]
								}
							}
				result[0]["blocks"].append(input_list)

			if checkboxes != None:
				chk_boxes_list = {
					"block_id": "checkboxes",
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": checkboxes['title'],
						"emoji": True
					},
					"element": {
						"type": "checkboxes",
						"options": []
					}
				}
				if 'action_id' in checkboxes:
					chk_boxes_list['element']["action_id"] = checkboxes['action_id']

				for checkbox in checkboxes['checkboxes']:
					boxes_list = {
								"text": {
									"type": "plain_text",
									"text": checkbox['text'],
									"emoji": True
								},
								"value": checkbox['value']
								}
					chk_boxes_list['element']['options'].append(boxes_list)

				result[0]["blocks"].append(chk_boxes_list)

			if buttons != None:
				actions_list = {
								"type": "actions",
								"elements": []
							   }
				
				for button in buttons:
					button_list = {
									"type": "button",
									"text": {
										"type": "plain_text",
										"text": button['text']
									},
									"style": button['style'],
									"value": button['value'],
									"action_id": button['action_id']
									}
					actions_list['elements'].append(button_list)

				result[0]["blocks"].append(actions_list)

			result[0]["fallback"] = (fallback_text + description)

			return result

		async def InboxesAuto(self, regex=None):
			if regex != None:
				mensaje_inboxes = ""
				for player in self.players_list:
					for channel in self.ch_names_list:
						if regex in channel:
							accuracy = self.similar(re.sub(f"({regex})", "", str(channel)).lower(), str(player).lower().replace(" ", "-"))
							if accuracy >= 0.4:
								self.inboxes_all[player] = channel
						
				json.dump(self.inboxes_all,open(f"inboxes_{self.platform}.json", "w"))

				for player in self.inboxes_all:
					mensaje_inboxes += f"Inbox {player} [{self.inboxes_all[player]}]\n"

				self.response_auto = await self.EditMessage(response=self.response_auto, color_sl="CL_YELLOW", title = f"📩 Inboxes fetched! [{len(self.inboxes_all)}]", description=mensaje_inboxes)
				
				self.regex_ready = True

			elif self.fetch_inboxes == True:

				self.response_auto = await self.SendMessage(channel = self._ctx['channel'], color_sl="CL_CYAN", title="💬 Fetching inboxes...", description=f"Please wait while we fetch all the inboxes in this server!")

				channels = await self.app.client.conversations_list(types="public_channel,private_channel")

				for channel in channels['channels']:
					self.ch_names_list.append(channel['name'])

				channels_itinerator = 0
				regex = ""
				past_channel = None

				while regex == "":
					for channel in self.ch_names_list:
						if channels_itinerator == 0 and channel == past_channel:
							past_channel = channel
							channels_itinerator += 1
							continue
						
						match_channel = self.regex_finder(str(channel).lower() + "-" + str(past_channel).lower())

						if match_channel != False:
							for character in past_channel:
								if character in channel:
									regex += character
								else:
									break
							break
						else:
							channels_itinerator += 1
							past_channel = channel
							continue

				image = {"image_url":"https://i.ibb.co/34rTqMH/image.png", "name": "regex"}
				buttons = [{"text":"Yes!", "style": "primary", "value": regex, "action_id": "regex_yes"},{"text":"No.", "style": "danger", "value": "click_me_456", "action_id": "regex_no"}]
				
				self.response_auto = await self.EditMessage(response=self.response_auto, color_sl="CL_GREEN", title = "ℹ️ Regex detected!", description = f"Please confirm if the regex detected for the channels, is correct so we can get the inboxes!\n\nExample:\ninbox-legal\nThe regex should be `inbox-`\n\n*Detected regex:* `{regex}`\n\n\nPlease select your answer below.", image=image, buttons = buttons)
				self.regex_ready = False

			else:
				mensaje_inboxes = ""
				self.response_auto = await self.SendMessage(channel = self._ctx['channel'], color_sl="CL_CYAN", title="💬 Fetching inboxes...", description=f"Please wait while we fetch all the inboxes in this server!")

				for player in self.inboxes_all:
					mensaje_inboxes += f"Inbox {player} [{self.inboxes_all[player]}]\n"

				self.response_auto = await self.EditMessage(response=self.response_auto, color_sl="CL_YELLOW", title = f"📩 Inboxes fetched! [{len(self.inboxes_all)}]", description=mensaje_inboxes)

				self.regex_ready = True

		async def InjectHandler(self):
			image = None

			author = {"name": self._inject["From"], "date": self._inject["Date"]}

			player = self._inject['Player']

			if not (self._inject.get('Photo') is None):
				image = {"name": self._inject['Picture Name'], "image_url": self._inject['Photo']}
			
			if not (self._inject.get('Profile') is None):
				author["image_url"] = self._inject['Profile']
				
			else:
				profile_pic = random.choice([
					"https://ssl.gstatic.com/ui/v1/icons/mail/profile_mask2.png",
					"https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg",
					"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTt8Dg9RL4IGOjsJ2Fr-lXThf-DGM5YgPB6j5rD8tHQ9RLrU-03H4dYeskL01FNajqL_0&usqp=CAU"
				])
				author["image_url"] = profile_pic
			
			await self.SendMessage(channel = self.inboxes_all[player], title= self._inject['Subject'], description=self._inject["Script"], image=image, author=author, color_sl="CL_CYAN")

			return True

		async def SendMessage(self, color_sl=None, title:str=None, description:str=None, channel=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None):
			if channel == None:
				channel = self._ctx['channel']
			self.response = await self.app.client.chat_postMessage(channel = channel, attachments = self.Slack.Formatter(title=title, description=description, color=color_sl, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes))
			return self.response

		async def EditMessage(self, color_sl=None, title:str=None, description:str=None, response=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None):
			self.response = await self.app.client.chat_update(channel=response['channel'], ts=response['ts'], attachments = self.Slack.Formatter(title=title, description=description, color=color_sl, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes))
			return self.response

	class Whatsapp():

		async def InboxFetcher(self, inbox):
			for player in self.players_list:
				accuracy = self.similar(str(inbox['Chat_Name']).lower(),str(player).lower())
				if accuracy >= 0.4:
					self.inboxes_all[player] = inbox['Chat_Name']
					json.dump(self.inboxes_all,open(f"inboxes_{self.platform}.json", "w"))

					mensaje_inboxes = ""

					for x in self.inboxes_all:
						mensaje_inboxes += f"*Inbox* {x} [{self.inboxes_all[x]}]\n"

					await self.SendMessage(title = f"Got it!*\nChannel added!\n{player}[{inbox['Chat_Name']}]\n*We have {len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).", description=f"All the inboxes:\n{mensaje_inboxes}")

		async def InboxesAuto(self, message=None):
			if self.fetch_inboxes == True or len(self.players_list) != len(self.inboxes_all):
				if message == None:
					title="❌ Not enough inboxes ❌"
					description=f"We don't have enough inboxes to start the bot.\nPlease add the Inbox Channels for players sending the command \`\`\`\!add\`\`\` to the channel.\n*Restart the bot before sending this messages!*\n\nWe have {len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).\n\nAll the inboxes:\n{self.inboxes_all}"
					await self.Whatsapp.SendMessage(self=self, chat=self._ctx["Chat_Name"], title=title, description=description)

				self.regex_ready = False
			
			elif len(self.players_list) == len(self.inboxes_all):
				mensaje_inboxes = ""
				for player in self.inboxes_all:
					mensaje_inboxes += f"*Inbox* {player} [{self.inboxes_all[player]}]\n"
				await self.Whatsapp.SendMessage(self=self, chat=self._ctx["Chat_Name"], title=f"📩 Inboxes fetched!*\n*{len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).", description=mensaje_inboxes)
				self.regex_ready = True
			
			else:
				mensaje_inboxes = ""
				for player in self.inboxes_all:
					mensaje_inboxes += f"*Inbox* {player} [{self.inboxes_all[player]}]\n"
				await self.Whatsapp.SendMessage(self=self, chat=self._ctx["Chat_Name"], title=f"📩 Inboxes fetched!*\n*{len(self.inboxes_all)} inbox(es) for {len(self.players_list)} player(s).", description=mensaje_inboxes)
				self.regex_ready = True

		async def InjectHandler(self):
			all_data = f'*Date*: {self._inject["Date"]}\n*From*: {self._inject["From"]}\n\n{self._inject["Script"]}'

			player = self._inject['Player']
			image = None
			if not (self._inject.get('Photo') is None):
				image = self._inject['Photo']
				
			await self.Whatsapp.SendMessage(self=self, title=self._inject["Subject"], description=all_data, chat=self.inboxes_all[player], image=image)
			await asyncio.sleep(0.5)

		async def SendMessage(self, title, description, chat, image=None):
			message = f"*{title}*\n\n{description}"
			
			if image == None:
				self.bot.SendMessage(chat=chat, message=message)
			else:
				self.bot.SendImage(chat=chat, message=message, image=image)

			return True