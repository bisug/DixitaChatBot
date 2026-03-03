from pyrogram import filters
from dixitabot import app

@app.on_message(filters.command("id"))
async def getid(client, message):
    """Handles the /id command to retrieve Telegram IDs for users, messages, and chats."""
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    # Initial response text including command message and sender IDs
    text = f"<b><a href='{message.link}'>Message id:</a></b> <code>{message_id}</code>\n"
    text += f"<b><a href='tg://user?id={your_id}'>Your id:</a></b> <code>{your_id}</code>\n"

    # Support for retrieving another user's ID via username or numeric ID argument
    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"<b><a href='tg://user?id={user_id}'>User id:</a></b> <code>{user_id}</code>\n"
        except Exception:
            return await message.reply_text("This user doesn't exist.", quote=True)

    # Append current chat ID to the output
    text += f"<b><a href='https://t.me/{chat.username}'>Chat id:</a></b> <code>{chat.id}</code>\n\n"

    # If the command is a reply, append IDs related to the replied-to message and its sender
    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"<b><a href='{reply.link}'>Replied message id:</a></b> <code>{reply.id}</code>\n"
        text += f"<b><a href='tg://user?id={reply.from_user.id}'>Replied user id:</a></b> <code>{reply.from_user.id}</code>\n\n"

    # Handle forwarded channel information
    if reply and reply.forward_from_chat:
        text += f"The forwarded channel, <b>{reply.forward_from_chat.title}</b>, has an id of <code>{reply.forward_from_chat.id}</code>\n\n"

    # Handle replies from anonymous channels or linked groups
    if reply and reply.sender_chat:
        text += f"Id of the replied chat/channel, is <code>{reply.sender_chat.id}</code>"

    # Send the final ID summary back to the user
    await message.reply_text(
        text,
        disable_web_page_preview=True,
    )
