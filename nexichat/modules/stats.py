from pyrogram import filters, Client
from pyrogram.types import Message

from nexichat import OWNER, app, mongo, redis_db
from nexichat.database.chats import get_served_chats
from nexichat.database.users import get_served_users


@app.on_message(filters.command("stats"))
async def stats(cli: Client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    
    # Detailed DB Stats
    word_count = await mongo["Word"]["WordDb"].count_documents({})
    daxx_count = await mongo["DAXXDb"]["DAXX"].count_documents({})
    
    # Redis Stats
    redis_status = "<b>✅ ᴏɴʟɪɴᴇ</b>" if redis_db and redis_db.ping() else "<b>❌ ᴏғғʟɪɴᴇ</b>"
    
    await message.reply_text(
        f"""<b>OVERALL sᴛᴀᴛs ᴏғ {(await cli.get_me()).mention} :</b>

<b>ʙᴏᴛ'S ʀᴇᴀᴄʜ:</b>
➻ <b>ᴄʜᴀᴛs :</b> <code>{chats}</code>
➻ <b>ᴜsᴇʀs :</b> <code>{users}</code>

<b>ᴅᴀᴛᴀʙᴀsᴇ:</b>
➻ <b>ʀᴇsᴘᴏɴsᴇs sᴀᴠᴇᴅ :</b> <code>{word_count}</code>
➻ <b>ᴅɪsᴀʙʟᴇᴅ ᴄʜᴀᴛs :</b> <code>{daxx_count}</code>

<b>ᴄᴀᴄʜᴇ:</b>
➻ <b>sᴛᴀᴛᴜs :</b> {redis_status}"""
    )
