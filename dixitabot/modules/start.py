import asyncio
import random

from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message

from dixitabot import app
from dixitabot.database.chats import add_served_chat
from dixitabot.database.users import add_served_user
from dixitabot.modules.helpers.assets import IMG, STICKER, EMOJIOS
from dixitabot.modules.helpers import (
    CLOSE_BTN,
    DEV_OP,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    HELP_START,
    SOURCE_READ,
    START,
)

@app.on_message(filters.command(["start", "aistart"]))
async def start(_, m: Message):
    """Handles the /start command, displaying a welcome message and tracking the user/chat."""
    if m.chat.type == ChatType.PRIVATE:
        # Personal welcome message for users in private messages
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=f"<b>Hey, I am {app.name}</b>\n<b>An AI based chatbot.</b>\n<b>──────────────</b>\n<b>Usage /chatbot [on/off]</b>\n<b>||Hit help button for help||</b>",
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
        await add_served_user(m.from_user.id)
    else:
        # Generic welcome message for groups
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=START,
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)

@app.on_message(filters.command("help"))
async def help(client: Client, m: Message):
    """Provides usage instructions for the bot's features."""
    if m.chat.type == ChatType.PRIVATE:
        # Full help guide for private messages
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
        await add_served_user(m.from_user.id)
    else:
        # Encourages group members to check help in private messages
        await m.reply_photo(
            photo=random.choice(IMG),
            caption="<b>Hey, PM me for help commands!</b>",
            reply_markup=InlineKeyboardMarkup(HELP_BUTN),
        )
        await add_served_chat(m.chat.id)

@app.on_message(filters.command("repo"))
async def repo(_, m: Message):
    """Responds with the source code link for the bot."""
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )

@app.on_message(filters.new_chat_members)
async def welcome(_, m: Message):
    """Welcomes new members joined to the group chat with a photo and start message."""
    for member in m.new_chat_members:
        await m.reply_photo(photo=random.choice(IMG), caption=START)
