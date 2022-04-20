from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp
from dotenv import load_dotenv
import logging
import asyncio
import os
import re

from T3SF import *

logging.basicConfig(level=logging.WARNING)

load_dotenv()

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

T3SF = T3SF(app=app)

@app.action(re.compile("regex"))
async def regex_handler(ack, body, payload):
    await T3SF.RegexHandler(ack=ack,body=body,payload=payload)

@app.message('!ping')
async def ping(message, say):
    """
    Retrieves the !ping command and replies with this message.
    """
    description = """
    PING localhost (127.0.0.1): 56 data bytes\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=113 time=37.758 ms\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=113 time=50.650 ms\n64 bytes from 127.0.0.1: icmp_seq=2 ttl=113 time=42.493 ms\n64 bytes from 127.0.0.1: icmp_seq=3 ttl=113 time=37.637 ms\n--- localhost ping statistics ---\n4 packets transmitted, 4 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 37.637/42.135/50.650/5.292 ms\n\n_This is not real xD_"""
    await app.client.chat_postMessage(channel = message['channel'], attachments = T3SF.Slack.Formatter(color="CL_GREEN", title="🏓 Pong!", description=description))

@app.message("!start")
async def start(message, say):
    """
    Retrieves the !start command and starts to fetch and send the incidents.
    """
    try:
        await T3SF.ProcessIncidents(function_type = "start", ctx=message)

    except Exception as e:
        print("ERROR - Start function")
        print(e)
        raise

@app.message(re.compile("(!resume|!re)"))
async def resume(message, say):
    """
    Retrieves the !resume command and starts to fetch and
    send incidents from the desired starting point.
    """
    try:
        itinerator = int(message['text'].split(" ")[1])  # Gets the starting point.

        await T3SF.ProcessIncidents(function_type = "resume", ctx=message, itinerator=itinerator)

    except Exception as e:
        print("ERROR - Resume function")
        print(e)
        raise

@app.event("message")
async def handle_message_events(body, logger):
    """
    Handling the received messages.
    DEPRECATED/DEBUG FUNCTION
    """
    logger.info(body)

@app.error
async def custom_error_handler(error, body, logger):
    """
    Errror handling function
    """
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")

# Let's start the bot!
async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())