import random
from Abg.chat_status import adminsOnly
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message
from config import MONGO_URL
from nexichat import nexichat
from nexichat.modules.helpers import CHATBOT_ON, is_admins

# Import AI handler
try:
    from nexichat.ai_handler import ai_handler
    AI_ENABLED = True
    print("✅ AI Handler loaded!")
except Exception as e:
    AI_ENABLED = False
    print(f"⚠️ AI disabled: {e}")

def smart_match(user_message, database):
    """Smart matching with AI fallback"""
    user_message_lower = user_message.lower().strip()
    
    # 1. Try exact match
    exact = database.find_one({"word": user_message_lower})
    if exact:
        return list(database.find({"word": user_message_lower}))
    
    # 2. Try variations
    variations = [user_message_lower, user_message.strip(), user_message.capitalize()]
    for var in variations:
        result = database.find_one({"word": var})
        if result:
            return list(database.find({"word": var}))
    
    # 3. Try partial matching
    words = user_message_lower.split()
    if len(words) > 1:
        for word in words:
            if len(word) > 3:
                result = database.find_one({"word": word})
                if result:
                    return list(database.find({"word": word}))
    
    # 4. Try regex (fuzzy)
    for word in words:
        if len(word) > 3:
            regex_result = list(database.find({"word": {"$regex": word, "$options": "i"}}).limit(5))
            if regex_result:
                return regex_result
    
    return None

def get_ai_response(message_text, chatai_db):
    """Get response from AI and save to database"""
    if not AI_ENABLED:
        return None
    
    try:
        # Get AI response
        ai_reply = ai_handler.generate_response(message_text)
        
        # Save to database for future use
        chatai_db.insert_one({
            "word": message_text.lower().strip(),
            "text": ai_reply,
            "check": "text",
            "source": "ai"
        })
        
        return ai_reply
    except Exception as e:
        print(f"AI error: {e}")
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
    
    # Check if chatbot is disabled
    DAXXdb = MongoClient(MONGO_URL)
    DAXX = DAXXdb["DAXXDb"]["DAXX"]
    is_DAXX = DAXX.find_one({"chat_id": message.chat.id})
    
    if is_DAXX:
        return
    
    # Handle non-reply messages
    if not message.reply_to_message:
        if message.text:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            
            # Try smart matching first
            matches = smart_match(message.text, chatai)
            
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
            else:
                # Not found - use AI
                ai_response = get_ai_response(message.text, chatai)
                if ai_response:
                    # Add random reaction for AI responses too
                    if random.random() < 0.2:
                        reactions = ["🤖", "💡", "✨", "🎯"]
                        try:
                            await message.react(random.choice(reactions))
                        except:
                            pass
                    
                    await message.reply_text(ai_response)
    
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
                else:
                    # Use AI for unknown replies
                    ai_response = get_ai_response(message.text, chatai)
                    if ai_response:
                        await message.reply_text(ai_response)
