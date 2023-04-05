from T3SF import T3SF
import asyncio

async def main():
    await T3SF.start(MSEL="../MSEL_EXAMPLE.json", platform="Discord", gui=True)

if __name__ == '__main__':
    asyncio.run(main())