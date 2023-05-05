from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import re,os
import T3SF 

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
bot_discord = commands.Bot(command_prefix='!', intents=intents)

# Defining global variables and events
T3SF_instance = None
start_incidents_gui = asyncio.Event()
create_env = asyncio.Event()
config_MSEL = None
class create_bot():
	def __init__(self, MSEL):
		global config_MSEL
		config_MSEL = MSEL
		self.define_commands()

	def define_commands(self):
		global bot_discord
		
		@bot_discord.event
		async def on_ready():
			"""
			Print some infomation about the bot when it connects succesfully.
			"""
			print(f'\n * Discord Bot - {bot_discord.user} is ready!')
			T3SF.T3SF_Logger.emit(message=f'Discord Bot - {bot_discord.user} is ready!', message_type="DEBUG")

		@bot_discord.event
		async def on_interaction(interaction):
			await T3SF.T3SF.PollAnswerHandler(self=T3SF_instance, payload=interaction)

		@bot_discord.command(name='ping', help='Responds with pong to know if the bot is up! Usage -> !ping')
		async def ping_command(ctx):
			"""
			Retrieves the !ping command and replies with the latency.
			"""
			description = f"""
			**Pong!**

			:stopwatch: `{round(bot_discord.latency*1000)}ms`
			"""
			response = await ctx.send(embed=discord.Embed(colour=discord.Colour.blue(), description=description))

		@bot_discord.command(name="start", help='Starts the Incidents Game. Usage -> !start')
		@commands.has_role("Game Master")
		async def start_command(ctx, *, query=None):
			"""
			Retrieves the !start command and starts to fetch and send the incidents.
			"""
			try:
				global T3SF_instance
				T3SF_instance = T3SF.T3SF(platform="discord", bot=bot_discord)
				await T3SF_instance.ProcessIncidents(MSEL = config_MSEL, function_type = "start", ctx=ctx)

			except Exception as e:
				print("ERROR - Start function")
				print(e)
				raise

async def start_bot():
	T3SF_instance = T3SF.T3SF(platform="discord", bot=bot_discord)
	task1 = asyncio.create_task(bot_discord.start(TOKEN))
	task2 = asyncio.create_task(async_handler_exercise())
	task3 = asyncio.create_task(create_environment_task())

	# wait for the coroutines to finish
	await asyncio.gather(task1, task2, task3)

async def async_handler_exercise():
	global T3SF_instance
	while True:
		try:
			await asyncio.wait_for(start_incidents_gui.wait(), timeout=0.1)
		except asyncio.TimeoutError:
			pass
		else:
			T3SF_instance = T3SF.T3SF(platform="discord", bot=bot_discord)
			T3SF_instance.guild_id = server_id
			asyncio.create_task(T3SF_instance.ProcessIncidents(MSEL = config_MSEL, function_type="start", ctx=None))

			start_incidents_gui.clear()

async def run_async_incidents(server):
	global server_id
	server_id = server
	start_incidents_gui.set()

async def create_environment(server):
	global server_id
	server_id = server
	create_env.set()

async def create_environment_task():
	global T3SF_instance
	while True:
		try:
			await asyncio.wait_for(create_env.wait(), timeout=0.1)
		except asyncio.TimeoutError:
			pass
		else:
			create_env.clear()

			T3SF_instance = T3SF.T3SF(platform="discord", bot=bot_discord)
			areas_msel = T3SF_instance.IncidentsFetcher(MSEL = config_MSEL)

			# Set the GUILD To the user's input server
			guild = bot_discord.get_guild(int(server_id))

			inbox_name = "inbox"
			extra_chnls = ['chat','decision-log']
			players_list_local = areas_msel

			await create_gm_channels(guild=guild)

			for player in players_list_local:

				player_normalized = player.lower().replace(" ", "-")

				role = await create_role_if_not_exists(guild=guild, name=player_normalized)

				if role:
					category_name =  "Group - " + player
					category = await create_category_if_not_exists(guild=guild, name=category_name, private=True, role=role)

					if category:
						await create_channel_if_not_exists(category=category, name=inbox_name)
						T3SF.T3SF_Logger.emit(message=f'Player [{player}] - Channel {inbox_name} created', message_type="DEBUG")

						for channel in extra_chnls:
							await create_channel_if_not_exists(category=category, name=channel)
							T3SF.T3SF_Logger.emit(message=f'Player [{player}] - Channel {channel} created', message_type="DEBUG")
						
						await create_voice_if_not_exists(category=category, name="office")
						T3SF.T3SF_Logger.emit(message=f'Player [{player}] - Voice Channel created', message_type="DEBUG")

			T3SF.T3SF_Logger.emit(message=f"Player's Channels created!", message_type="INFO")

async def create_role_if_not_exists(guild, name):
	try:
		role = discord.utils.get(guild.roles, name=name)

		if role is None:
			general = discord.Permissions(view_channel=True)
			text = discord.Permissions.text()
			voice = discord.Permissions.voice()
			role = await guild.create_role(name=name, permissions=general | text | voice, colour=discord.Colour.red())
			return role
		else:
			return role

	except Exception as e:
		print(e)
		raise

async def create_category_if_not_exists(guild, name, private=False, role=None):
	try:
		category = discord.utils.get(guild.categories, name=name)

		if category is None:
			category = await guild.create_category(name)

			if private:
				await category.set_permissions(guild.default_role, read_messages=False)
				await category.set_permissions(role, read_messages=True)

			return category
		else:
			return category

	except Exception as e:
		print(e)
		raise

async def create_channel_if_not_exists(category, name):
	try:
		channel = discord.utils.get(category.channels, name=name)
		if channel is None:
			channel = await category.create_text_channel(name)
			return channel	
		else:
			return channel
	except Exception as e:
		print(e)
		raise

async def create_voice_if_not_exists(category, name):
	try:
		channel = discord.utils.get(category.channels, name=name)
		if channel is None:
			channel = await category.create_voice_channel(name)
			return channel	
		else:
			return channel
	except Exception as e:
		print(e)
		raise

async def create_gm_channels(guild):

	role = discord.utils.get(guild.roles, name="Game Master")
	
	if role is None:
		all_perms = discord.Permissions.all()
		role = await guild.create_role(name="Game Master", permissions=all_perms, colour=discord.Colour.green())

	category = await create_category_if_not_exists(guild=guild, name="Control Room", private=True, role=role)
	channels = ['chat','logs']

	for channel in channels:
		await create_channel_if_not_exists(category=category, name=channel)
	
	await create_voice_if_not_exists(category=category, name="Game Masters")

	T3SF.T3SF_Logger.emit(message=f'Game Master channels created.', message_type="INFO")

	return True