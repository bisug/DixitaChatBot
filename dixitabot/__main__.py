import asyncio
import importlib

async def anony_boot():
    """Initializes and starts the DixitaChatBot and its modules."""
    from dixitabot import LOGGER, app, mongo, redis_db
    from dixitabot.modules import ALL_MODULES
    from pyrogram import idle

    # Patch the app loop to ensure session tasks use the correct running event loop
    app.loop = asyncio.get_running_loop()

    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(f"Failed to start: {ex}")
        return

    # Dynamically import all modules defined in ALL_MODULES
    for all_module in ALL_MODULES:
        importlib.import_module("dixitabot.modules." + all_module)

    # Start the web server if enabled in the configuration
    from config import WEB_SERVICE
    if WEB_SERVICE:
        from dixitabot.web import start_web_server
        asyncio.create_task(start_web_server())

    LOGGER.info(f"@{app.username} Started.")
    await idle()

    LOGGER.info("Stopping dixitabot Bot...")

    # Gracefully close database connections
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
