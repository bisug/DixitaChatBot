from dixitabot import db

# Reference to the chats collection within the asynchronous database interface
chatsdb = db.chatsdb

async def get_served_chats() -> list:
    """Retrieves a list of all group chats registered in the database (IDs less than 0)."""
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    # Iteratively build the list from the database cursor
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    """Checks if a specific chat ID already exists in the registered chats collection."""
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

async def add_served_chat(chat_id: int):
    """Registers a new group chat ID in the database if it is not already served."""
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})

async def remove_served_chat(chat_id: int):
    """Removes a group chat ID from the registered chats collection."""
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"chat_id": chat_id})
