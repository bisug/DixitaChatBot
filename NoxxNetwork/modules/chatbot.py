import random
from Abg.chat_status import adminsOnly

from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message

from config import MONGO_URL
from NoxxNetwork import NoxxBot
from NoxxNetwork.modules.helpers import CHATBOT_ON, is_admins


@NoxxBot.on_cmd("chatbot", group_only=True)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )
    return


# Global variable to store previous message for each chat
chat_previous_messages = {}


def get_random_database_reply(chatai):
    """Get a random reply from the database"""
    try:
        # Get all replies from database
        all_replies = list(chatai.find({}))
        
        if all_replies:
            chosen = random.choice(all_replies)
            return chosen["text"]
        else:
            return None
    except Exception as e:
        print(f"Error getting random reply: {e}")
        return None


@NoxxBot.on_message(
    (filters.text | filters.group) & ~filters.private & ~filters.bot, group=4
)
async def chatbot_universal(client: Client, message: Message):
    global chat_previous_messages
    
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
    
    # Check if chatbot is enabled
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    is_vick = vick.find_one({"chat_id": message.chat.id})
    
    chat_id = message.chat.id
    
    # LEARNING PHASE - Save word-reply pairs
    if message.reply_to_message:
        # Reply to a message - save word-reply pair
        word = None
        reply_text = None
        
        # Get the word (what was replied to)
        if message.reply_to_message.text:
            word = message.reply_to_message.text
            
        # Get the reply
        if message.text:
            reply_text = message.text
            
        # Save to database
        if word and reply_text:
            try:
                existing = chatai.find_one({"word": word, "text": reply_text})
                if not existing:
                    chatai.insert_one({
                        "word": word,
                        "text": reply_text
                    })
            except Exception as e:
                print(f"Database error: {e}")
                
    else:
        # Direct message - check if previous message exists and save pair
        if chat_id in chat_previous_messages:
            prev_msg = chat_previous_messages[chat_id]
            
            word = None
            reply_text = None
            
            # Get previous word
            if prev_msg.get("type") == "text":
                word = prev_msg.get("content")
                
            # Get current reply
            if message.text:
                reply_text = message.text
                
            # Save word-reply pair
            if word and reply_text:
                try:
                    existing = chatai.find_one({"word": word, "text": reply_text})
                    if not existing:
                        chatai.insert_one({
                            "word": word,
                            "text": reply_text
                        })
                except Exception as e:
                    print(f"Database error: {e}")
    
    # Store current message as previous for next iteration
    if message.text:
        chat_previous_messages[chat_id] = {
            "type": "text",
            "content": message.text,
            "user_id": message.from_user.id
        }
    
    # RESPONSE PHASE - Only if chatbot is enabled
    if not is_vick:
        should_respond = False
        search_word = None
        
        if message.reply_to_message and message.reply_to_message.from_user.id == client.id:
            # Reply to bot
            should_respond = True
            if message.text:
                search_word = message.text
                
        elif not message.reply_to_message:
            # Direct message - respond randomly or if bot mentioned
            if message.text:
                if f"@{client.me.username}" in message.text.lower() or "bot" in message.text.lower():
                    should_respond = True
                    search_word = message.text.replace(f"@{client.me.username}", "").strip()
                else:
                    # Random response (10% chance)
                    if random.randint(1, 10) == 1:
                        should_respond = True
                        search_word = message.text
        
        if should_respond and search_word:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            
            # Find exact responses first
            responses = []
            matches = list(chatai.find({"word": search_word}))
            
            for match in matches:
                responses.append(match["text"])
            
            if responses:
                # Found exact match
                reply = random.choice(responses)
                try:
                    await message.reply_text(reply)
                except Exception:
                    pass
            else:
                # No exact match found, get random reply from database
                random_reply = get_random_database_reply(chatai)
                
                if random_reply:
                    try:
                        await message.reply_text(random_reply)
                    except Exception:
                        pass


@NoxxBot.on_message(
    filters.private & filters.text & ~filters.bot, group=5
)
async def chatbot_private(client: Client, message: Message):
    """Handle private messages - always respond"""
    try:
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
    
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    
    search_word = None
    if message.text:
        search_word = message.text
    
    if search_word:
        # First try to find exact match
        responses = list(chatai.find({"word": search_word}))
        
        if responses:
            # Found exact match
            chosen = random.choice(responses)
            try:
                await message.reply_text(chosen["text"])
            except Exception:
                pass
        else:
            # No exact match, get random reply from database
            random_reply = get_random_database_reply(chatai)
            
            if random_reply:
                try:
                    await message.reply_text(random_reply)
                except Exception:
                    pass


@NoxxBot.on_cmd("chatstats")
async def chatbot_stats(_, message: Message):
    """Show total learned words"""
    try:
        chatdb = MongoClient(MONGO_URL)
        chatai = chatdb["Word"]["WordDb"]
        
        total_words = chatai.count_documents({})
        
        stats_text = f"""
📊 **Universal Chatbot Stats**

🧠 Total Learned Words: `{total_words}`
💬 Text Responses: `{total_words}`

✨ **Learning:** Active everywhere
🌍 **Scope:** Universal (all chats)
        """
        
        await message.reply_text(stats_text)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
