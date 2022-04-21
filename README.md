<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://user-images.githubusercontent.com/103124157/164258966-7a049d6c-4012-49ca-8f7d-2bb814c24009.png" alt="WhaBot Logo"></a>
</p>

<h3 align="center">T3SF</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![PyPI version](https://badge.fury.io/py/T3SF.svg)](https://badge.fury.io/py/T3SF)
  [![Documentation Status](https://readthedocs.org/projects/t3sf/badge/?version=latest)](https://t3sf.readthedocs.io/en/latest/?badge=latest)
  [![License](https://img.shields.io/badge/license-GPL-blue.svg)](/LICENSE)

</div>

<p align="center"> Technical Tabletop Exercises Simulation Framework
    <br> 
</p>

## Table of Contents
- [About](#About)
- [Getting Things Ready](#Starting)
- [TODO](./TODO.md)
- [Contributing](./CONTRIBUTING.md)
- [Authors](#Authors)

## About <a name = "About"></a>
T3SP is a framework that offers a modular structure for the orchestration of events from a master scenario events list (MSEL) together with a set of rules defined for each exercise (optional) and a configuration that allows defining the parameters of the correspondent platform. The main module performs the communication with the specific module (Discord, Slack, Telegram, etc.) which allows the events to be presented in the input channels as injects for each platform. Also, the framework supports different use cases: "single organization, multiple areas", "multiple organization, single area" and "multiple organization, multiple areas".

## Getting Things Ready <a name = "Starting"></a>
Platform-independant, you will need to install the framework itself!

To do this, you can follow this easy step-by-step guide, or if you're already comfortable installing packages with `pip`, you can skip to the last step!

```bash
# Python 3.6+ required
python -m venv .venv       # We will create a python virtual enviroment
source .venv/bin/activate  # Let's get inside it

pip install -U pip         # Upgrade pip
pip install T3SF           # Install the framework!
```

We strongly recommend following the platform-specific guidance within our Read The Docs! Here you have the links:

  - [Discord](https://t3sf.readthedocs.io/en/latest/Discord.html#installation)
  - [Slack](https://t3sf.readthedocs.io/en/latest/Slack.html#installation)
  - [Telegram](https://t3sf.readthedocs.io/en/latest/Telegram.html#installation)
  - [WhatsApp](https://t3sf.readthedocs.io/en/latest/WhatsApp.html#installation)

## Usage <a name="Usage"></a>
We created this framework to simplify all your work!

You will need to edit the `config.ini` file with your desired platform and the file to fetch your incidents.

Here is an example if you want to run the framework with the `Discord` bot.

```ini
[General]
Platform : Discord

TTX_File : MSEL_BASE4.json
```

Here is a code snippet used as an example of the [Discord bot](./Discord/bot.py):

```python
from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

from T3SF import T3SF

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

T3SF = T3SF(bot=bot) # We need to pass the bot's object to the framework.

@bot.command(name="start", help='Starts the Incidents Game. Usage -> !start')
async def start(ctx):
        # When the bot receives the command !start,
        # we are going to start the game!
        await T3SF.ProcessIncidents(function_type = "start", ctx=ctx) 

bot.run(TOKEN)

```

Here is another code snippet for the [Slack bot](./Slack/bot.py)

```python
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp
from dotenv import load_dotenv
import asyncio
import os

from T3SF import *

load_dotenv()

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

T3SF = T3SF(app=app) # We need to pass the app's object to the framework.

@app.message("!start")
async def start(message, say):
    # When the bot receives the command !start,
    # we are going to start the game!
    await T3SF.ProcessIncidents(function_type = "start", ctx=message)

# Let's start the bot!
async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())
```

If you need more help, you can always check our documentation [here](https://t3sf.readthedocs.io/en/latest/)!

## Authors <a name = "Authors"></a>
- [@FedeQuarkB4](https://github.com/FedeQuarkB4) - Idea
- [@lanfranB4](https://github.com/lanfranB4) - Main developer
