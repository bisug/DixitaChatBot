from pyrogram import filters, Client
from pyrogram.types import Message

from dixitabot import OWNER, app, mongo, redis_db
from dixitabot.database.chats import get_served_chats
from dixitabot.database.users import get_served_users


@app.on_message(filters.command("stats"))
async def stats(cli: Client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    
    # Detailed DB Stats
    word_count = await mongo["Word"]["WordDb"].count_documents({})
    daxx_count = await mongo["DAXXDb"]["DAXX"].count_documents({})
    
    # Redis Stats
    redis_status = "<b>Online</b>" if redis_db and redis_db.ping() else "<b>Offline</b>"
    
    await message.reply_text(
        f"""<b>Overall stats of {(await cli.get_me()).mention} :</b>

<b>Bot's reach:</b>
<b>Chats:</b> <code>{chats}</code>
<b>Users:</b> <code>{users}</code>

<b>Database:</b>
<b>Responses saved:</b> <code>{word_count}</code>
<b>Disabled chats:</b> <code>{daxx_count}</code>

<b>Cache:</b>
<b>Status:</b> {redis_status}"""
    )
