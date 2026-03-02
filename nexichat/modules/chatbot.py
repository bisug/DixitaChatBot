import random
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message
import html

from nexichat import app, mongo

# Custom adminsOnly decorator
def adminsOnly(permission):
    def decorator(func):
        async def wrapper(client, message):
            try:
                user = await client.get_chat_member(message.chat.id, message.from_user.id)
                if user.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                    # In a full implementation, you'd check `permission` against `user.privileges`.
                    # For simplicity, we just check if they are an admin.
                    return await func(client, message)
                else:
                    await message.reply_text("Only admins can use this command.")
            except UserNotParticipant:
                await message.reply_text("You are not in this chat.")
            except Exception as e:
                print(f"Error in adminsOnly: {e}")
        return wrapper
    return decorator

async def smart_match(user_message, database):
    """Smart matching with AI fallback"""
    user_message_lower = user_message.lower().strip()
    
    # 1. Try exact match
    exact = await database.find_one({"word": user_message_lower})
    if exact:
        return await database.find({"word": user_message_lower}).to_list(length=None)
    
    # 2. Try variations
    variations = [user_message_lower, user_message.strip(), user_message.capitalize()]
    for var in variations:
        result = await database.find_one({"word": var})
        if result:
            return await database.find({"word": var}).to_list(length=None)
    
    # 3. Try partial matching
    words = user_message_lower.split()
    if len(words) > 1:
        for word in words:
            if len(word) > 3:
                result = await database.find_one({"word": word})
                if result:
                    return await database.find({"word": word}).to_list(length=None)
    
    # 4. Try regex (fuzzy)
    for word in words:
        if len(word) > 3:
            regex_result = await database.find({"word": {"$regex": word, "$options": "i"}}).to_list(length=5)
            if regex_result:
                return regex_result
    
    return None



@app.on_message(filters.command("chatbot") & filters.group)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {html.escape(m.chat.title)}\n<b>ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.</b>",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

@app.on_message(
    (filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot, group=4
)
async def chatbot_smart(client: Client, message: Message):
    try:
        # Skip commands
        if message.text and (
            message.text.startswith("!")
            or message.text.startswith("/")
            or message.text.startswith("?")
            or message.text.startswith("@")
            or message.text.startswith("#")
        ):
            return
    except Exception:
        pass
    
    chatai = mongo["Word"]["WordDb"]
    
    # Check if chatbot is disabled
    DAXX = mongo["DAXXDb"]["DAXX"]
    is_DAXX = await DAXX.find_one({"chat_id": message.chat.id})
    
    if is_DAXX:
        return
    
    # Handle non-reply messages
    if not message.reply_to_message:
        if message.text:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            
            # Try smart matching first
            matches = await smart_match(message.text, chatai)
            
            if matches:
                # Found in database
                response_data = random.choice(matches)
                response_text = response_data["text"]
                response_type = response_data["check"]
                
                # Auto reaction (30% chance)
                if random.random() < 0.3:
                    reactions = ["👍", "❤️", "🔥", "😊", "👏"]
                    try:
                        await message.react(random.choice(reactions))
                    except:
                        pass
                
                # Send response
                if response_type == "sticker":
                    await message.reply_sticker(response_text)
                else:
                    await message.reply_text(response_text)

    
    # Handle replies to bot
    elif message.reply_to_message:
        if message.reply_to_message.from_user.id == client.id:
            if message.text:
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)
                
                matches = await smart_match(message.text, chatai)
                
                if matches:
                    response_data = random.choice(matches)
                    response_text = response_data["text"]
                    response_type = response_data["check"]
                    
                    if response_type == "sticker":
                        await message.reply_sticker(response_text)
                    else:
                        await message.reply_text(response_text)

