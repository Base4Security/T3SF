from T3SF import T3SF
import asyncio

MSEL = "path/to/your/MSEL.json"    # Indicate where's your MSEL stored.

platform = "Slack" or "Discord"    # Choose your platform

gui = True or False                # Do you want a GUI?

async def main():
    await T3SF.start(MSEL=MSEL, platform=platform, gui=gui)

if __name__ == '__main__':
    asyncio.run(main())