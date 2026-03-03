from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

from config import SUPPORT_GRP, UPDATE_CHNL
from dixitabot import OWNER
from dixitabot import app

DEV_OP = [
    [
        InlineKeyboardButton(text="Owner", user_id=OWNER, style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Support", url=f"https://t.me/{SUPPORT_GRP}", style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton(
            text="Add Me Baby",
            url=f"https://t.me/{app.username}?startgroup=true",
            style=ButtonStyle.SUCCESS
        ),
    ],
    [
        InlineKeyboardButton(text="Help", callback_data="HELP", style=ButtonStyle.PRIMARY),
    ],
    [
       # InlineKeyboardButton(text="Source", callback_data="SOURCE", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="About", callback_data="ABOUT", style=ButtonStyle.DANGER),
    ],
]

PNG_BTN = [
    [
        InlineKeyboardButton(
            text="Add Me Baby",
            url=f"https://t.me/{app.username}?startgroup=true",
            style=ButtonStyle.SUCCESS
        ),
    ],
    [
        InlineKeyboardButton(
            text="Close",
            callback_data="CLOSE",
            style=ButtonStyle.DANGER
        ),
    ],
]


BACK = [
    [
        InlineKeyboardButton(text="Back", callback_data="BACK", style=ButtonStyle.DEFAULT),
    ],
]


HELP_BTN = [
    [
        InlineKeyboardButton(text="Chatbot", callback_data="CHATBOT_CMD", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Tools", callback_data="TOOLS_DATA", style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton(text="Back", callback_data="BACK", style=ButtonStyle.DEFAULT),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]


CLOSE_BTN = [
    [
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]


CHATBOT_ON = [
    [
        InlineKeyboardButton(text="Enable", callback_data=f"addchat", style=ButtonStyle.SUCCESS),
        InlineKeyboardButton(text="Disable", callback_data=f"rmchat", style=ButtonStyle.DANGER),
    ],
]


MUSIC_BACK_BTN = [
    [
        InlineKeyboardButton(text="Soon", callback_data=f"soom", style=ButtonStyle.PRIMARY),
    ],
]

S_BACK = [
    [
        InlineKeyboardButton(text="Back", callback_data="SBACK", style=ButtonStyle.DEFAULT),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]


CHATBOT_BACK = [
    [
        InlineKeyboardButton(text="Back", callback_data="CHATBOT_BACK", style=ButtonStyle.DEFAULT),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]


HELP_START = [
    [
        InlineKeyboardButton(text="Help", callback_data="HELP", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]


HELP_BUTN = [
    [
        InlineKeyboardButton(
            text="Help", url=f"https://t.me/{app.username}?start=help", style=ButtonStyle.PRIMARY
        ),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]


ABOUT_BTN = [
    [
        InlineKeyboardButton(text="Support", url=f"https://t.me/{SUPPORT_GRP}", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Help", callback_data="HELP", style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton(text="Owner", user_id=OWNER, style=ButtonStyle.PRIMARY),
     #   InlineKeyboardButton(text="Source", callback_data="SOURCE", style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton(text="Updates", url=f"https://t.me/{UPDATE_CHNL}", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Back", callback_data="BACK", style=ButtonStyle.DEFAULT),
    ],
]
