from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# Initialize an asynchronous MongoDB client for user-specific data tracking
mongo = MongoCli(MONGO_URL)
# This module likely provides an alternative interface for managing user data
db = mongo.users
db = db.usersdb

async def get_users():
  """Retrieves a list of all numeric user IDs stored in this specific collection."""
  user_list = []
  # Cursor through all documents with user IDs greater than 0
  async for user in db.users.find({"user": {"$gt": 0}}):
    user_list.append(user['user'])
  return user_list

async def get_user(user):
  """Checks if a user ID is currently tracked in this user list."""
  users = await get_users()
  return user in users

async def add_user(user):
  """Adds a new user ID to the tracking collection if not already present."""
  users = await get_users()
  if user in users:
    return
  else:
    await db.users.insert_one({"user": user})

async def del_user(user):
  """Removes a user ID from the tracking collection."""
  users = await get_users()
  if not user in users:
    return
  else:
    await db.users.delete_one({"user": user})
