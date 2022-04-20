from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatType
from dotenv import load_dotenv
from T3SF import *
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.WARNING)

bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
dp = Dispatcher(bot)

T3SF = T3SF(bot=bot)

@dp.message_handler(commands="ping")
async def ping(message):
	"""
	Retrieves the !ping command and replies with this message.
	"""
	description = """```
	PING localhost (127.0.0.1): 56 data bytes\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=113 time=37.758 ms\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=113 time=50.650 ms\n64 bytes from 127.0.0.1: icmp_seq=2 ttl=113 time=42.493 ms\n64 bytes from 127.0.0.1: icmp_seq=3 ttl=113 time=37.637 ms\n--- localhost ping statistics ---\n4 packets transmitted, 4 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 37.637/42.135/50.650/5.292 ms```\n\n_This is not real xD_"""
	response = await message.reply(description, parse_mode = 'Markdown')

@dp.message_handler(commands='start')
async def start(message: types.Message):
	"""
	Retrieves the !start command and starts to fetch and send the incidents.
	"""
	await T3SF.ProcessIncidents(function_type = "start", ctx=message)

@dp.message_handler(commands='resume')
async def resume(message: types.Message):
	"""
	Retrieves the !resume command and starts to fetch and
	send incidents from the desired starting point.
	"""
	itinerator = int(message['text'].split(" ")[1])

	await T3SF.ProcessIncidents(function_type = "resume", ctx=message, itinerator=itinerator)

@dp.channel_post_handler()
async def inboxes_fetcher(message):
	"""
	This handler will be called when user sends a message in a channel
	to add it to the inboxes list.
	"""	
	await T3SF.InboxesAuto(message=message)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)