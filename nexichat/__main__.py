import asyncio
import importlib

# Install uvloop BEFORE importing nexichat so that pyrogram's Client
# is constructed under the correct event loop policy.
try:
    import uvloop
    uvloop.install()
    import logging
    logging.getLogger(__name__).info("uvloop enabled successfully.")
except ImportError:
    import logging
    logging.getLogger(__name__).info("uvloop not installed, using standard asyncio.")

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
        asyncio.run(anony_boot())
    except KeyboardInterrupt:
        pass
