from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

from T3SF import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

T3SF = T3SF(bot=bot)

@bot.event
async def on_ready():
    """
    Print some infomation about the bot when it connects succesfully.
    """
    print(f'{bot.user.name} has connected to Discord!')
    print('------')
    print(f'{bot.user}')
    print('------')
    print(f'{bot.user.id}')
    print('------')

@bot.event
async def on_interaction(interaction):
    await T3SF.PollAnswerHandler(payload=interaction)

@bot.command(name='ping', help='Responds with pong to know if the bot is up! Usage -> !ping')
async def ping(ctx):
    """
    Retrieves the !ping command and replies with the latency.
    """
    description = f"""
    **Pong!**

    :stopwatch: `{round(bot.latency*1000)}ms`
    """
    response = await ctx.send(embed=discord.Embed(colour=discord.Colour.blue(), description=description))

@bot.command(name="start", help='Starts the Incidents Game. Usage -> !start')
@commands.has_role("Game Master")
async def start(ctx, *, query=None):
    """
    Retrieves the !start command and starts to fetch and send the incidents.
    """
    try:
        await T3SF.ProcessIncidents(function_type = "start", ctx=ctx)

    except Exception as e:
        print("ERROR - Start function")
        print(e)
        raise

@bot.command(name="resume", pass_context=True, help='Resumes the Game from the desired Incident Id. Usage -> !resume [ID (#)] / !resume 4')
@commands.has_role("Game Master")
async def resume(ctx, *, query):
    """
    Retrieves the !resume command and starts to fetch and
    send incidents from the desired starting point.
    """
    try:
        flags = query.split(" ")

        itinerator = int(flags[0])  # Gets the starting point.

        await T3SF.ProcessIncidents(function_type = "resume", ctx=ctx, itinerator=itinerator)

    except Exception as e:
        print("ERROR - Resume function")
        print(e)
        raise

bot.run(TOKEN)