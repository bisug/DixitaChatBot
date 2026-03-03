import asyncio
import orjson
import random

from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatMemberStatus
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message

from dixitabot import LOGGER, app, mongo, redis_db
from dixitabot.modules.helpers.inline import CHATBOT_ON

def adminsOnly(permission: str):
    """Decorator to restrict command usage to chat administrators and owners."""
    def decorator(func):
        async def wrapper(client: Client, message: Message):
            try:
                # Check the sender's member status in the current chat
                user = await client.get_chat_member(message.chat.id, message.from_user.id)
                if user.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                    return await func(client, message)
                return
            except UserNotParticipant:
                # Handle cases where the sender is not a member of the group
                return
            except Exception as e:
                LOGGER.error(f"Error in adminsOnly decorator: {e}")
        return wrapper
    return decorator

async def smart_match(user_message, database):
    """Matches a user message to a response using Redis caching, exact matching, and fuzzy matching."""
    user_message_lower = user_message.lower().strip()
    
    # Check Redis for a pre-cached response for this exact message
    cache_key = f"word_cache_{user_message_lower}"
    if redis_db:
        cached = redis_db.get(cache_key)
        if cached:
            return orjson.loads(cached)
            
    # Attempt an exact match directly in the MongoDB collection
    exact = await database.find_one({"word": user_message_lower})
    if exact:
        # Retrieve all responses for this word and cache them for future use
        results = await database.find({"word": user_message_lower}).to_list(length=None)
        clean_results = [{"text": r["text"], "check": r["check"]} for r in results]
        
        if redis_db:
            redis_db.set(cache_key, orjson.dumps(clean_results), ex=86400) # 24-hour cache
            
        return clean_results
    
    # Check common text variations for matching
    variations = [user_message_lower, user_message.strip(), user_message.capitalize()]
    for var in variations:
        result = await database.find_one({"word": var})
        if result:
            return await database.find({"word": var}).to_list(length=None)
    
    # Split the message into individual words for broader partial matching
    words = user_message_lower.split()
    if len(words) > 1:
        for word in words:
            if len(word) > 3:
                result = await database.find_one({"word": word})
                if result:
                    return await database.find({"word": word}).to_list(length=None)
    
    # Fallback to regex-based fuzzy matching for longer words
    for word in words:
        if len(word) > 3:
            regex_result = await database.find({"word": {"$regex": word, "$options": "i"}}).to_list(length=5)
            if regex_result:
                return regex_result
    
    return None

async def process_ai_response(client: Client, message: Message, chatai):
    """Finds and sends an AI response message or sticker, with optional reactions."""
    if not message.text:
        return
        
    # Visual typing indicator to simulate human behavior
    asyncio.create_task(client.send_chat_action(message.chat.id, ChatAction.TYPING))
    
    # Retrieve matching responses from the database/cache
    matches = await smart_match(message.text, chatai)
    
    if matches:
        # Randomly select one response from the list of matches
        response_data = random.choice(matches)
        response_text = response_data["text"]
        response_type = response_data["check"]
        
        # Add a random Telegram reaction to the trigger message (30% probability)
        if random.random() < 0.3:
            reactions = ["👍", "❤️", "🔥", "😊", "👏"]
            try:
                await message.react(random.choice(reactions))
            except Exception:
                pass
        
        # Send the response, handling both text and stickers while ignoring FloodWait errors
        try:
            if response_type == "sticker":
                await message.reply_sticker(response_text)
            else:
                await message.reply_text(response_text)
        except FloodWait:
            pass

@app.on_message(filters.command("chatbot") & filters.group)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    """Handles the /chatbot command to present an inline menu for group settings."""
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n<b>ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.</b>",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

@app.on_message(
    (filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot & ~filters.regex(r"^[!/?@#]"), group=4
)
async def chatbot_smart(client: Client, message: Message):
    """Monitors chat activity to generate AI responses and implement self-learning."""
    chatai = mongo["Word"]["WordDb"]
    DAXX = mongo["DAXXDb"]["DAXX"]
    
    # Determine if the chatbot is disabled for this specific chat ID
    is_DAXX = False
    cache_key = f"chatbot_disabled_{message.chat.id}"
    
    if redis_db:
        # Check Redis first for current disabled status
        cached_status = redis_db.get(cache_key)
        if cached_status is not None:
            is_DAXX = int(cached_status) == 1
        else:
            is_DAXX_doc = await DAXX.find_one({"chat_id": message.chat.id})
            is_DAXX = bool(is_DAXX_doc)
            redis_db.set(cache_key, "1" if is_DAXX else "0", ex=3600) # One-hour cache
    else:
        # Direct MongoDB query if Redis is not available
        is_DAXX_doc = await DAXX.find_one({"chat_id": message.chat.id})
        is_DAXX = bool(is_DAXX_doc)
    
    # Exit early if the bot is disabled in this group
    if is_DAXX:
        return
    
    # Determine how to respond based on message context
    if not message.reply_to_message:
        # Standard processing for non-replies
        await process_ai_response(client, message, chatai)
    elif message.reply_to_message:
        # Respond specifically if a user replies to the bot's own message
        if message.reply_to_message.from_user and message.reply_to_message.from_user.id == client.id:
            await process_ai_response(client, message, chatai)
        else:
            # Self-learning: store user-to-user conversational patterns
            if message.reply_to_message.text and not message.reply_to_message.text.startswith(("/", "!", "?", "@", "#")):
                word = message.reply_to_message.text.lower().strip()
                if message.text:
                    # Save new text trigger-response pair to DB if it doesn't already exist
                    exists = await chatai.find_one({"word": word, "text": message.text, "check": "text"})
                    if not exists:
                        await chatai.insert_one({"word": word, "text": message.text, "check": "text"})
                        if redis_db:
                            redis_db.delete(f"word_cache_{word}")
                elif message.sticker:
                    # Save new sticker response for a text trigger
                    exists = await chatai.find_one({"word": word, "text": message.sticker.file_id, "check": "sticker"})
                    if not exists:
                        await chatai.insert_one({"word": word, "text": message.sticker.file_id, "check": "sticker"})
                        if redis_db:
                            redis_db.delete(f"word_cache_{word}")
