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

T3SF_instance = None
start_incidents_gui = asyncio.Event()
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

	# wait for the coroutines to finish
	await asyncio.gather(task1, task2)


async def async_handler_exercise():
	global T3SF_instance
	while True:
		try:
			await asyncio.wait_for(start_incidents_gui.wait(), timeout=0.1)
		except asyncio.TimeoutError:
			pass
		else:
			T3SF_instance = T3SF.T3SF(platform="discord", bot=bot_discord)
			asyncio.create_task(T3SF_instance.ProcessIncidents(MSEL = config_MSEL, function_type="start", ctx=None))

			start_incidents_gui.clear()

async def run_async_incidents():
	start_incidents_gui.set()