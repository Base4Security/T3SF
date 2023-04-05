from WhaBot import *
from T3SF import T3SF
import asyncio
import time


whatsapp = WhaBot(reloaded=False,
	binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
	driver_location = "/Users/XXXXXX/Desktop/chromedriver",
	)


T3SF = T3SF(bot=whatsapp)

async def handle_commands(ctx):
	for contact in ctx:
		if whatsapp.CommandHandler(ctx=contact, command="!ping"):
			description = "🏓 Pong!\n\nPING localhost (127.0.0.1): 56 data bytes\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=113 time=37.758 ms\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=113 time=50.650 ms\n64 bytes from 127.0.0.1: icmp_seq=2 ttl=113 time=42.493 ms\n64 bytes from 127.0.0.1: icmp_seq=3 ttl=113 time=37.637 ms\n--- localhost ping statistics ---\n4 packets transmitted, 4 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 37.637/42.135/50.650/5.292 ms\n\n_This is not real xD_"
			whatsapp.SendMessage(chat=contact["Chat_Name"], message=description)

		elif whatsapp.CommandHandler(ctx=contact, command="!start"):
			await T3SF.ProcessIncidents(function_type = "start", ctx=contact)

		elif whatsapp.CommandHandler(ctx=contact, command="!resume"):
			itinerator = int(contact["Last_Message"].split(" ")[1])
			await T3SF.ProcessIncidents(function_type = "resume", ctx=contact, itinerator=itinerator)

		elif whatsapp.CommandHandler(ctx=contact, command="!add"):
			await T3SF.RegexHandler(inbox=contact)

async def main():
	while True:
		unreads = whatsapp.GetUnreadChats(scrolls=10)
		await handle_commands(ctx=unreads)
		await asyncio.sleep(0.5)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()