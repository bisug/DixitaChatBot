import asyncio
import importlib

from pyrogram import idle

from nexichat import LOGGER, app, mongo, redis_db
from nexichat.modules import ALL_MODULES


async def anony_boot():
    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("nexichat.modules." + all_module)

    LOGGER.info(f"@{app.username} Started.")
    await idle()

    LOGGER.info("Stopping nexichat Bot...")
    try:
        mongo.close()
        LOGGER.info("MongoDB connection closed.")
    except Exception:
        pass

    if redis_db:
        try:
            redis_db.close()
            LOGGER.info("Redis connection closed.")
        except Exception:
            pass


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
        LOGGER.info("uvloop enabled successfully.")
    except ImportError:
        LOGGER.info("uvloop not installed, using standard asyncio.")

    try:
        asyncio.run(anony_boot())
    except KeyboardInterrupt:
        pass
