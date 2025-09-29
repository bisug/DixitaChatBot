import asyncio
import importlib
import subprocess

from pyrogram import idle

from NoxxNetwork import LOGGER, NoxxBot
from NoxxNetwork.modules import ALL_MODULES
from config import WEB_APP

if WEB_APP:
    subprocess.Popen(['python3', 'web.py'])

async def anony_boot():
    try:
        await NoxxBot.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("NoxxNetwork.modules." + all_module)

    LOGGER.info(f"@{NoxxBot.username} Started.")
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("Stopping NoxxNetwork Bot...")
