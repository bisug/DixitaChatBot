from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# Initialize an asynchronous MongoDB client for chat-related data
mongo = MongoCli(MONGO_URL)
# This module appears to use a separate database/collection hierarchy than dixitabot.database.chats
db = mongo.chats
db = db.chatsdb

async def get_chats():
  """Retrieves a list of all numeric chat IDs stored in this specific collection."""
  chat_list = []
  # Cursor through documents with a chat ID less than 0 (typical for groups)
  async for chat in db.chats.find({"chat": {"$lt": 0}}):
    chat_list.append(chat['chat'])
  return chat_list

async def get_chat(chat):
  """Checks if a specific chat ID exists within the local chat list."""
  chats = await get_chats()
  return chat in chats

async def add_chat(chat):
  """Registers a new chat ID if it doesn't already exist in the collection."""
  chats = await get_chats()
  if chat in chats:
    return
  else:
    await db.chats.insert_one({"chat": chat})

async def del_chat(chat):
  """Removes a chat ID from the collection if it exists."""
  chats = await get_chats()
  if not chat in chats:
    return
  else:
    await db.chats.delete_one({"chat": chat})
