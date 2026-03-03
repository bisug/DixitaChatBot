import psutil
import os
import time
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram.errors import MessageDeleteForbidden

from config import OWNER_ID
from dixitabot import app, boot, db
from dixitabot.database.chats import add_served_chat
from dixitabot.database.users import add_served_user
from dixitabot.modules.helpers import PNG_BTN
from dixitabot.modules.helpers.assets import IMG

@app.on_message(filters.command("ping"))
async def ping(_, message: Message):
    """Calculates and displays system performance metrics, database latency, and bot uptime."""
    start = datetime.now()

    # Send initial placeholder message to measure API latency
    loda = await message.reply_photo(
        photo="https://graph.org/file/210751796ff48991b86a3.jpg",
        caption="Pinging...",
    )
    
    # Calculate round-trip API latency in milliseconds
    ms = (datetime.now() - start).microseconds / 1000
    
    # Measure MongoDB database ping latency
    db_start = time.time()
    await db.command("ping")
    db_ms = round((time.time() - db_start) * 1000, 2)
    
    # Calculate human-readable uptime string from boot time
    uptime_seconds = int(time.time() - boot)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    
    # Retrieve system resource usage for the current process
    process = psutil.Process(os.getpid())
    ram = round(process.memory_info().rss / (1024 * 1024), 2)  # Memory usage in MB
    cpu = process.cpu_percent(interval=0.1) # CPU usage percentage

    # Attempt to clean up the user's command message
    try:
        await message.delete()
    except MessageDeleteForbidden:
        pass
    
    # Update the response with actual performance data
    await loda.edit_text(
        text=f"""Hey Baby!!
{app.name} is alive and working fine!

<b>Bot stats:</b>
<b>Latency:</b> <code>{ms}</code> ms
<b>Db latency:</b> <code>{db_ms}</code> ms
<b>Uptime:</b> <code>{uptime_str}</code>
<b>Ram:</b> <code>{ram}</code> MB
<b>Cpu:</b> <code>{cpu}</code>%""",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )

    # Record the chat or user in the database for tracking statistics
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
