from T3SF import T3SF
import asyncio, os
from dotenv import load_dotenv
load_dotenv()

MSEL_PATH = os.environ['MSEL_PATH']

async def main():
	await T3SF.start(MSEL=MSEL_PATH, platform="slack", gui=True)

if __name__ == '__main__':
	asyncio.run(main())