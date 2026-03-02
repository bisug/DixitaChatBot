import asyncio
import importlib


async def anony_boot():
    from dixitabot import LOGGER, app, mongo, redis_db
    from dixitabot.modules import ALL_MODULES
    from pyrogram import idle

    # kurigram's session uses self.client.loop.create_task() to schedule
    # recv_worker. That `loop` attribute is set during Client.__init__ via
    # asyncio.get_event_loop(), but asyncio.run() creates a *new* loop,
    # so they differ. Patching it here (inside the running loop) guarantees
    # session tasks are created on the correct loop.
    app.loop = asyncio.get_running_loop()

    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(f"Failed to start: {ex}")
        return

    for all_module in ALL_MODULES:
        importlib.import_module("dixitabot.modules." + all_module)

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
