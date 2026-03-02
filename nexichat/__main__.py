import asyncio
import importlib
import logging

# Step 1: Create the event loop FIRST — before any nexichat imports.
# Pyrogram's Client.__init__ calls asyncio.get_event_loop() internally and
# caches it. By setting the loop here, both pyrogram and run_until_complete
# share the exact same loop object, preventing "attached to a different loop".
try:
    import uvloop
    loop = uvloop.new_event_loop()
    logging.getLogger(__name__).info("uvloop enabled successfully.")
except ImportError:
    loop = asyncio.new_event_loop()
    logging.getLogger(__name__).info("uvloop not installed, using standard asyncio.")

# Step 2: Register it as the current event loop.
asyncio.set_event_loop(loop)

# Step 3: Now safe to import nexichat — Client.__init__ calls get_event_loop()
# and gets our loop, not some other default loop.
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
        loop.run_until_complete(anony_boot())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
