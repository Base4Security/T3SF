from difflib import SequenceMatcher
import discord
import asyncio
import random
import json
import re 

class Discord(object):

		def __init__(self, bot):
			self.bot = bot

		async def InboxesAuto(self, T3SF_instance):
			mensaje_inboxes = ""
			image_example = "https://i.ibb.co/NCrPD3Y/discord-exp.png"

			if T3SF_instance.fetch_inboxes == True:
				if T3SF_instance._ctx == None:
					# Exercise started from the GUI
					guild = self.bot.get_guild(int(T3SF_instance.guild_id))
					channels = guild.text_channels

					for channel in channels:
						if "chat" in channel.name:
							accuracy = similar(str(channel.name).lower(),"gm-chat")
							if accuracy >= 0.8:
								inbox = channel.id
								T3SF_instance._ctx = self.bot.get_channel(channel.id)

				T3SF_instance.response_auto = await self.SendMessage(T3SF_instance=T3SF_instance, title="⚙️ Fetching inboxes...", description=f"Please wait while we fetch all the inboxes in this server!", color="BLUE")

				channels_itinerator = 0
				player_itinerator = 0
				regex = ""

				try:
					channels = T3SF_instance._ctx.message.guild.channels
					categories = T3SF_instance._ctx.message.guild.categories
					started_from_gui = False

				except Exception:
					channels = T3SF_instance._ctx.guild.channels
					categories = T3SF_instance._ctx.guild.categories
					started_from_gui = True

				while regex == "" and len(T3SF_instance.players_list) > player_itinerator:
					for category in categories:
						if channels_itinerator == 0:
							past_channel = category.name
							pass
						
						match_channel = similar(str(category).lower(), str(T3SF_instance.players_list[0]).lower())
						
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

				await T3SF_instance.response_auto.edit(embed=discord.Embed(
				 title = "ℹ️ Regex detected!",
				 description = f"Please confirm if the regex detected for the channels, is correct so we can get the inboxes!\n\nExample:\nGroup - Legal\nThe regex should be `Group -`\n\nDetected regex: `{regex}`",
				 color = 0x77B255).set_image(url=image_example).set_footer(text="Please answer with [Yes(Y)/No(N)]"))

				def check_regex_channels(msg):
					if started_from_gui:
						return msg.content.lower() in ["y", "yes", "n", "no"]

					else:
						return msg.author == T3SF_instance._ctx.author and msg.channel == T3SF_instance._ctx.channel and msg.content.lower() in ["y", "yes", "n", "no"]

				try:
					msg = await self.bot.wait_for("message", check=check_regex_channels, timeout=50)

					if msg.content.lower() in ["y", "yes"]:
						await self.EditMessage(T3SF_instance=T3SF_instance, style="custom", variable="T3SF_instance.response_auto", color="GREEN", title = "✨ Regex detected succesfully! ✨", description = f"Thanks for confirming the regex detected for the channels (I'm going to tell my creator he is so good coding :D ), we are going to use `{regex}` to match the inboxes")

					elif msg.content.lower() in ["n", "no"]:
						await T3SF_instance.response_auto.edit(embed=discord.Embed(
						 title = "ℹ️ Regex needed!",
						 description = "Got it!\n Unluckily, but here we go...\nPlease send me the regex for the channels, so we can get the inboxes!\n\nExample:\nGroup - Legal\nThe regex should be `Group -`",
						 color = discord.Colour.red()).set_image(url=image_example).set_footer(text="Please answer with the desired regex. EG: `Groups -`"))

						def get_regex_channels(msg_regex_user):
							# return msg_regex_user.author == T3SF_instance._ctx.author and msg_regex_user.channel == T3SF_instance._ctx.channel and 

							if started_from_gui:
								return msg_regex_user.content != ""

							else:
								return msg_regex_user.author == T3SF_instance._ctx.author and msg_regex_user.channel == T3SF_instance._ctx.channel and msg_regex_user.content != ""
						
						msg_regex_user = await self.bot.wait_for("message", check=get_regex_channels, timeout=50)

						if msg_regex_user.content != "":
							regex = msg_regex_user
							await self.EditMessage(T3SF_instance=T3SF_instance, style="custom", variable="T3SF_instance.response_auto", color="GREEN", title="✅ Regex accepted!", description=f"Thanks for confirming the regex for the channels, we are going to use `{msg_regex_user.content}` to match the inboxes!")

				except asyncio.TimeoutError:
					await self.EditMessage(T3SF_instance=T3SF_instance, style="custom", variable="T3SF_instance.response_auto", color="RED", title = ":x: Sorry, you didn't reply on time", description = "Please start the process again.")
					raise RuntimeError("We didn't detect any regex, time's up.")

				for player in T3SF_instance.players_list:
					for channel in channels:
						category = channel.category
						if "inbox" in channel.name :
							accuracy = similar(re.sub(f"({regex})", "",str(category)).lower(),str(player).lower())
							if accuracy >= 0.4:
								T3SF_instance.inboxes_all[player] = channel.id
				
				json.dump(T3SF_instance.inboxes_all,open(f"inboxes_{T3SF_instance.platform}.json", "w"))

				for player in T3SF_instance.inboxes_all:
					mensaje_inboxes += f"**Inbox** {player}[{T3SF_instance.inboxes_all[player]}]\n"

				await self.EditMessage(T3SF_instance=T3SF_instance, style="custom", variable="T3SF_instance.response_auto", color="GREEN", title=f"📩  Inboxes fetched! [{len(T3SF_instance.inboxes_all)}]", description=mensaje_inboxes)

			return True

		async def InjectHandler(self, T3SF_instance):
			all_data = f'Date: {T3SF_instance._inject["Date"]}\n\n{T3SF_instance._inject["Script"]}'

			player = T3SF_instance._inject['Player']

			inbox = self.bot.get_channel(T3SF_instance.inboxes_all[player])

			embed = discord.Embed(title = T3SF_instance._inject['Subject'], description = all_data, color = discord.Colour.blue())
			
			if "Photo" in T3SF_instance._inject and T3SF_instance._inject['Photo'] != '':
				embed.set_image(url=T3SF_instance._inject['Photo'])
			
			if "Profile" in T3SF_instance._inject and T3SF_instance._inject['Profile'] != '':
				profile_pic = T3SF_instance._inject['Profile']
			else:
				profile_pic = random.choice([
					"https://ssl.gstatic.com/ui/v1/icons/mail/profile_mask2.png",
					"https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg",
					"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTt8Dg9RL4IGOjsJ2Fr-lXThf-DGM5YgPB6j5rD8tHQ9RLrU-03H4dYeskL01FNajqL_0&usqp=CAU"
				])

			embed.set_author(name=T3SF_instance._inject["From"], icon_url=profile_pic)

			T3SF_instance.response_poll = await inbox.send(embed = embed)

			return embed

		async def PollHandler(self, T3SF_instance):
			T3SF_instance.poll_answered = False

			all_data = T3SF_instance._inject["Script"]

			poll_options = T3SF_instance._inject['Poll'].split('|')
			
			actual_real_time = re.sub("([^0-9])", "", T3SF_instance._inject['Real Time'])[-2:]
			
			next_real_time = re.sub("([^0-9])", "", T3SF_instance.data[int(T3SF_instance._inject['#'])]['Real Time'])[-2:]

			diff = int(next_real_time) - int(actual_real_time)
			if diff < 0:
				diff_no_real = int(actual_real_time) - int(next_real_time)
				diff = 60 - diff_no_real 

			diff_secs = diff * 60

			view = discord.ui.View()
			view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary,label=poll_options[0], custom_id="poll|"+poll_options[0]))
			view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary,label=poll_options[1], custom_id="poll|"+poll_options[1]))

			all_data = all_data+ f"\n\nYou have {diff} minute(s) to answer this poll!"

			player = T3SF_instance._inject['Player']

			inbox = self.bot.get_channel(T3SF_instance.inboxes_all[player])

			embed = discord.Embed(title = T3SF_instance._inject['Subject'], description = all_data, color = discord.Colour.yellow())

			if "Photo" in T3SF_instance._inject and T3SF_instance._inject['Photo'] != '':
				embed.set_image(url=T3SF_instance._inject['Photo'])

			T3SF_instance.response_poll = await inbox.send(embed = embed, view=view)

			return embed

		async def PollAnswerHandler(self, T3SF_instance, interaction=None):
			if "poll" in interaction.data['custom_id']:
				poll_msg_og = interaction.message.embeds.copy()[0]

				title =  poll_msg_og.title

				poll_msg = poll_msg_og.description
				poll_msg = poll_msg[: poll_msg.rfind('\n')]

				action_user = interaction.user

				selected_option = interaction.data['custom_id'].split('|')[1]
				description = f'{poll_msg}\n\n@{action_user} selected: {selected_option}'               

				T3SF_instance.poll_answered = True
				T3SF_instance.response_poll = await interaction.response.edit_message(embed=discord.Embed(colour=discord.Colour.green(), title=title, description=description),view=None)
				await T3SF_instance.NotifyGameMasters(type_info="poll_answered", data={'msg_poll':poll_msg,'answer':selected_option,'user':action_user})
				return True
			else:
				pass

		async def SendMessage(self, T3SF_instance, color="CYAN", title:str=None, description:str=None, view=None, unique=False):
			colors = {'BLUE' : discord.Colour.dark_blue(), 'RED' : discord.Colour.red(), 'CYAN' : discord.Colour.blue(), 'GREEN' : discord.Colour.green(), 'YELLOW' : discord.Colour.yellow()}

			if unique == True:
				T3SF_instance.gm_poll_msg = await T3SF_instance._ctx.send(embed=discord.Embed(color=colors[color], title = title, description = description), view=view)
				return T3SF_instance.gm_poll_msg
			
			else:
				T3SF_instance.response = await T3SF_instance._ctx.send(embed=discord.Embed(color=colors[color], title = title, description = description), view=view)
				return T3SF_instance.response

		async def EditMessage(self, T3SF_instance=None, color="CYAN", title:str=None, description:str=None, view=None, style="simple", variable=None):

			if style == "simple":
				T3SF_instance.response = T3SF_instance.response.edit(embed=discord.Embed(color=colors[color], title = title, description = description), view=view)
				return T3SF_instance.response
			else:
				colors = {'BLUE' : discord.Colour.dark_blue(), 'RED' : discord.Colour.red(), 'CYAN' : discord.Colour.blue(), 'GREEN' : discord.Colour.green(), 'YELLOW' : discord.Colour.yellow()}
				variable = eval(variable)
				await variable.edit(embed=discord.Embed(color=colors[color], title = title, description = description), view=view)

def similar(a, b):
	"""
	Based in graphics, find the similarity between 2 strings.
	"""
	return SequenceMatcher(None, a, b).ratio()