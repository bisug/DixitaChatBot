from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from config import SUPPORT_GRP
from dixitabot import app, redis_db
from dixitabot.database import DAXX
from dixitabot.modules.helpers import (
    ABOUT_BTN,
    ABOUT_READ,
    ADMIN_READ,
    BACK,
    CHATBOT_BACK,
    CHATBOT_READ,
    DEV_OP,
    HELP_BTN,
    HELP_READ,
    MUSIC_BACK_BTN,
    SOURCE_READ,
    START,
    TOOLS_DATA_READ,
)

@app.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    """Global callback query handler for all inline button interactions."""
    # Navigation and static content handlers
    if query.data == "HELP":
        await query.message.edit_text(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
            disable_web_page_preview=True,
        )
    elif query.data == "CLOSE":
        await query.message.delete()
        await query.answer("Closed menu!", show_alert=True)
    elif query.data == "BACK":
        await query.message.edit(
            text=START,
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
    elif query.data == "SOURCE":
        await query.message.edit(
            text=SOURCE_READ,
            reply_markup=InlineKeyboardMarkup(BACK),
            disable_web_page_preview=True,
        )
    elif query.data == "ABOUT":
        await query.message.edit(
            text=ABOUT_READ,
            reply_markup=InlineKeyboardMarkup(ABOUT_BTN),
            disable_web_page_preview=True,
        )
    elif query.data == "ADMINS":
        await query.message.edit(
            text=ADMIN_READ,
            reply_markup=InlineKeyboardMarkup(MUSIC_BACK_BTN),
        )
    elif query.data == "TOOLS_DATA":
        await query.message.edit(
            text=TOOLS_DATA_READ,
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )
    elif query.data == "BACK_HELP":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
    elif query.data == "CHATBOT_CMD":
        await query.message.edit(
            text=CHATBOT_READ,
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )
    elif query.data == "CHATBOT_BACK":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )

    # Logic to enable chatbot functionality in a group
    elif query.data == "addchat":
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        # Verification to ensure only admins can modify group settings
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer(
                "You're not even an admin, don't try this explosive shit!",
                show_alert=True,
            )
            
        # Check if the chat is currently in the 'disabled' list (DAXX)
        is_DAXX = DAXX.find_one({"chat_id": query.message.chat.id})
        if not is_DAXX:
            await query.edit_message_text("<b>Chat-bot already enabled.</b>")
        else:
            # Remove chat from disabled list and update Redis cache
            DAXX.delete_one({"chat_id": query.message.chat.id})
            if redis_db:
                redis_db.set(f"chatbot_disabled_{query.message.chat.id}", "0", ex=3600)
            await query.edit_message_text(f"<b>Chat-bot enabled by</b> {query.from_user.mention}.")

    # Logic to disable chatbot functionality in a group
    elif query.data == "rmchat":
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer(
                "You're not even an admin, don't try this explosive shit!",
                show_alert=True,
            )
            
        # Check if the chat is already disabled
        is_DAXX = DAXX.find_one({"chat_id": query.message.chat.id})
        if is_DAXX:
            await query.edit_message_text("<b>Chat-bot already disabled.</b>")
        else:
            # Add chat to disabled list (DAXX) and update Redis cache
            DAXX.insert_one({"chat_id": query.message.chat.id})
            if redis_db:
                redis_db.set(f"chatbot_disabled_{query.message.chat.id}", "1", ex=3600)
            await query.edit_message_text(f"<b>Chat-bot disabled by</b> {query.from_user.mention}.")
