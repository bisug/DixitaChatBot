import asyncio
import traceback
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    UserIsBlocked,
    PeerIdInvalid
)

from dixitabot import app
from dixitabot.database.chats import get_served_chats
from dixitabot.database.users import get_served_users


async def send_msg(user_id, message: Message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.value + 1)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"
    return 200, "Success"


@app.on_message(filters.command("br"))
async def broadcast(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ɪᴛ.")
        return    
    
    all_chats = await get_served_chats() or []
    all_users = await get_served_users() or []
    
    done_chats = 0
    done_users = 0
    failed_chats = 0
    failed_users = 0
    
    for chat in all_chats:
        chat_id = chat.get("chat_id")
        if not chat_id:
            continue
        try:
            status, _ = await send_msg(chat_id, message.reply_to_message)
            if status == 200:
                done_chats += 1
            else:
                failed_chats += 1
        except Exception:
            failed_chats += 1
        await asyncio.sleep(0.1)

    for user in all_users:
        user_id = user.get("user_id")
        if not user_id:
            continue
        try:
            status, _ = await send_msg(user_id, message.reply_to_message)
            if status == 200:
                done_users += 1
            else:
                failed_users += 1
        except Exception:
            failed_users += 1
        await asyncio.sleep(0.1)
        
    if failed_users == 0 and failed_chats == 0:
        await message.reply_text(
            f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ✅</b>\n\n<b>sᴇɴᴛ ᴍᴇssᴀɢᴇ ᴛᴏ</b> <code>{done_chats}</code> <b>ᴄʜᴀᴛs ᴀɴᴅ</b> <code>{done_users}</code> <b>ᴜsᴇʀs</b>",
        )
    else:
        await message.reply_text(
            f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ✅</b>\n\n<b>sᴇɴᴛ ᴍᴇssᴀɢᴇ ᴛᴏ</b> <code>{done_chats}</code> <b>ᴄʜᴀᴛs</b> <code>{done_users}</code> <b>ᴜsᴇʀs</b>\n\n<b>ɴᴏᴛᴇ:-</b> <code>ᴅᴜᴇ ᴛᴏ sᴏᴍᴇ ɪssᴜᴇ ᴄᴀɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ</code> <code>{failed_users}</code> <b>ᴜsᴇʀs ᴀɴᴅ</b> <code>{failed_chats}</code> <b>ᴄʜᴀᴛs</b>",
        )


@app.on_message(filters.command("an"))
async def announced(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To Some Post To Broadcast")
        
    to_send = message.reply_to_message.id
    chats = await get_served_chats() or []
    users = await get_served_users() or []
    
    failed = 0
    for chat in chats:
        chat_id = chat.get("chat_id")
        if not chat_id:
            continue
        try:
            await app.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=to_send)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            try:
                await app.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=to_send)
            except Exception:
                failed += 1
        except Exception:
            failed += 1
    
    failed_user = 0
    for user in users:
        user_id = user.get("user_id")
        if not user_id:
            continue
        try:
            await app.forward_messages(chat_id=user_id, from_chat_id=message.chat.id, message_ids=to_send)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            try:
                await app.forward_messages(chat_id=user_id, from_chat_id=message.chat.id, message_ids=to_send)
            except Exception:
                failed_user += 1
        except Exception:
            failed_user += 1

    await message.reply_text(
        "Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ. {} ɢʀᴏᴜᴘs ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ᴅᴜᴇ ᴛᴏ ʙᴇɪɴɢ ᴋɪᴄᴋᴇᴅ. {} ᴜsᴇʀs ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ᴅᴜᴇ ᴛᴏ ʙᴇɪɴɢ ʙᴀɴɴᴇᴅ.".format(failed, failed_user)
    )
