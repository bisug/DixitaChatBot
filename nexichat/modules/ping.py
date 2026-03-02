

import psutil
import os
import time
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message

from config import OWNER_ID
from nexichat import app, boot, db
from nexichat.database.chats import add_served_chat
from nexichat.database.users import add_served_user
from nexichat.modules.helpers import PNG_BTN


#----------------IMG-------------#



# Random Start Images
IMG = [
    "https://graph.org/file/210751796ff48991b86a3.jpg",
    "https://graph.org/file/7b4924be4179f70abcf33.jpg",
    "https://graph.org/file/f6d8e64246bddc26b4f66.jpg",
    "https://graph.org/file/63d3ec1ca2c965d6ef210.jpg",
    "https://graph.org/file/9f12dc2a668d40875deb5.jpg",
    "https://graph.org/file/0f89cd8d55fd9bb5130e1.jpg",
    "https://graph.org/file/e5eb7673737ada9679b47.jpg",
    "https://graph.org/file/2e4dfe1fa5185c7ff1bfd.jpg",
    "https://graph.org/file/36af423228372b8899f20.jpg",
    "https://graph.org/file/c698fa9b221772c2a4f3a.jpg",
    "https://graph.org/file/61b08f41855afd9bed0ab.jpg",
    "https://graph.org/file/744b1a83aac76cb3779eb.jpg",
    "https://graph.org/file/814cd9a25dd78480d0ce1.jpg",
    "https://graph.org/file/e8b472bcfa6680f6c6a5d.jpg",
]


#----------------IMG-------------#

#---------------STICKERS---------------#

# Random Stickers
STICKER = [
    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA",
    "CAACAgUAAx0CYlaJawABBy4rZaid77Tf70SV_CfjmbMgdJyVD8sAApwLAALGXCFXmCx8ZC5nlfQeBA",
    "CAACAgUAAx0CYlaJawABBy4jZaidvIXNPYnpAjNnKgzaHmh3cvoAAiwIAAIda2lVNdNI2QABHuVVHgQ",
]

#---------------STICKERS---------------#



@app.on_message(filters.command("ping"))
async def ping(_, message: Message):
    start = datetime.now()
    loda = await message.reply_photo(
        photo="https://graph.org/file/210751796ff48991b86a3.jpg",
        caption="ᴘɪɴɢɪɴɢ...",
    )
    
    # Latency
    ms = (datetime.now() - start).microseconds / 1000
    
    # DB Latency
    db_start = time.time()
    await db.command("ping")
    db_ms = round((time.time() - db_start) * 1000, 2)
    
    # Uptime
    uptime_seconds = int(time.time() - boot)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    
    # System Info
    process = psutil.Process(os.getpid())
    ram = round(process.memory_info().rss / (1024 * 1024), 2)  # MB
    cpu = process.cpu_percent(interval=0.1)
    try:
        await message.delete()
    except Exception:
        pass
    
    await loda.edit_text(
        text=f"""нey вαву!!
{app.name} ιѕ alιve 🥀 αnd worĸιng ғιne!

**ʙᴏᴛ sᴛᴀᴛs:**
➻ **ʟᴀᴛᴇɴᴄʏ:** `{ms}` ms
➻ **ᴅʙ ʟᴀᴛᴇɴᴄʏ:** `{db_ms}` ms
➻ **ᴜᴘᴛɪᴍᴇ:** `{uptime_str}`
➻ **ʀᴀᴍ:** `{ram}` MB
➻ **ᴄᴘᴜ:** `{cpu}`%""",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
