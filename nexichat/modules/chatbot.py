import random
from Abg.chat_status import adminsOnly
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, MessageEntityType
from pyrogram.types import InlineKeyboardMarkup, Message
from config import MONGO_URL
from nexichat import nexichat
from nexichat.modules.helpers import CHATBOT_ON, is_admins

def smart_match(user_message, database):
    """Smart matching: exact, fuzzy, and keyword-based"""
    user_message_lower = user_message.lower().strip()
    
    # 1. Try exact match first
    exact = database.find_one({"word": user_message_lower})
    if exact:
        return list(database.find({"word": user_message_lower}))
    
    # 2. Try lowercase variations
    variations = [
        user_message_lower,
        user_message.strip(),
        user_message.capitalize(),
    ]
    
    for var in variations:
        result = database.find_one({"word": var})
        if result:
            return list(database.find({"word": var}))
    
    # 3. Try partial matching (contains)
    words = user_message_lower.split()
    if len(words) > 1:
        # Try each word
        for word in words:
            if len(word) > 3:  # Skip short words
                result = database.find_one({"word": word})
                if result:
                    return list(database.find({"word": word}))
    
    # 4. Try regex search (fuzzy)
    for word in words:
        if len(word) > 3:
            regex_result = list(database.find({"word": {"$regex": word, "$options": "i"}}).limit(10))
            if regex_result:
                return regex_result
    
    return None

@nexichat.on_cmd("chatbot", group_only=True)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

@nexichat.on_message(
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
    
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    
    # Check if chatbot is disabled for this chat
    DAXXdb = MongoClient(MONGO_URL)
    DAXX = DAXXdb["DAXXDb"]["DAXX"]
    is_DAXX = DAXX.find_one({"chat_id": message.chat.id})
    
    if is_DAXX:
        return  # Chatbot disabled
    
    # Handle non-reply messages
    if not message.reply_to_message:
        if message.text:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            
            # Smart matching
            matches = smart_match(message.text, chatai)
            
            if matches:
                # Pick random response
                response_data = random.choice(matches)
                response_text = response_data["text"]
                response_type = response_data["check"]
                
                # Auto reaction (random chance)
                if random.random() < 0.3:  # 30% chance
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
                
                matches = smart_match(message.text, chatai)
                
                if matches:
                    response_data = random.choice(matches)
                    response_text = response_data["text"]
                    response_type = response_data["check"]
                    
                    if response_type == "sticker":
                        await message.reply_sticker(response_text)
                    else:
                        await message.reply_text(response_text)
