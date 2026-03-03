import asyncio
import importlib


async def anony_boot():
    from dixitabot import LOGGER, app, mongo, redis_db
    from dixitabot.modules import ALL_MODULES
    from pyrogram import idle

    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(f"Failed to start: {ex}")
        return

    for all_module in ALL_MODULES:
        importlib.import_module("dixitabot.modules." + all_module)

    from config import WEB_SERVICE
    if WEB_SERVICE:
        from dixitabot.web import start_web_server
        asyncio.create_task(start_web_server())

    LOGGER.info(f"@{app.username} Started.")
    await idle()

    LOGGER.info("Stopping dixitabot Bot...")
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
