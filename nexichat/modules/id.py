from pyrogram import filters

from nexichat import app


@app.on_message(filters.command("id"))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"<b><a href='{message.link}'>ᴍᴇssᴀɢᴇ ɪᴅ:</a></b> <code>{message_id}</code>\n"
    text += f"<b><a href='tg://user?id={your_id}'>ʏᴏᴜʀ ɪᴅ:</a></b> <code>{your_id}</code>\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"<b><a href='tg://user?id={user_id}'>ᴜsᴇʀ ɪᴅ:</a></b> <code>{user_id}</code>\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"<b><a href='https://t.me/{chat.username}'>ᴄʜʜᴀᴛ ɪᴅ:</a></b> <code>{chat.id}</code>\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"<b><a href='{reply.link}'>ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:</a></b> <code>{reply.id}</code>\n"
        text += f"<b><a href='tg://user?id={reply.from_user.id}'>ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:</a></b> <code>{reply.from_user.id}</code>\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, <b>{reply.forward_from_chat.title}</b>, ʜᴀs ᴀɴ ɪᴅ ᴏғ <code>{reply.forward_from_chat.id}</code>\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs <code>{reply.sender_chat.id}</code>"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
    )
