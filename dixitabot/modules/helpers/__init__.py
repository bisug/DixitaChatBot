from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from dixitabot import OWNER, app, NexiChat

def is_admins(func: Callable) -> Callable:
    """Decorator to allow only chat administrators or the bot owner to execute a function."""
    async def non_admin(c: NexiChat, m: Message):
        # The bot owner bypasses all administrative checks
        if m.from_user.id == OWNER:
            return await func(c, m)

        # Retrieve the user's status within the chat and verify administrative rights
        admin = await c.get_chat_member(m.chat.id, m.from_user.id)
        if admin.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await func(c, m)

    return non_admin

# Import UI assets and text constants from helper sub-modules
from .inline import *
from .read import *
