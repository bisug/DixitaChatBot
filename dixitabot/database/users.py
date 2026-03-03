from dixitabot import db

# Reference to the users collection in the asynchronous database interface
usersdb = db.usersdb

async def is_served_user(user_id: int) -> bool:
    """Checks if a user ID is already present in the registered users collection."""
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    """Retrieves a list of all individual user IDs registered in the database (IDs greater than 0)."""
    users_list = []
    # Cursor through all matching user records in MongoDB
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    """Registers a new user ID in the database if they are not already served."""
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})
