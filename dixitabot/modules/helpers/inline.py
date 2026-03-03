from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

from config import SUPPORT_GRP, UPDATE_CHNL
from dixitabot import OWNER
from dixitabot import app

# Navigation menu for the developer/owner and support options
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
        InlineKeyboardButton(text="About", callback_data="ABOUT", style=ButtonStyle.DANGER),
    ],
]

# Simple buttons for the ping command response
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

# Standard back button configuration
BACK = [
    [
        InlineKeyboardButton(text="Back", callback_data="BACK", style=ButtonStyle.DEFAULT),
    ],
]

# Multi-option help menu buttons
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

# Simple close button
CLOSE_BTN = [
    [
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]

# Controls for enabling or disabling the chatbot in a group
CHATBOT_ON = [
    [
        InlineKeyboardButton(text="Enable", callback_data=f"addchat", style=ButtonStyle.SUCCESS),
        InlineKeyboardButton(text="Disable", callback_data=f"rmchat", style=ButtonStyle.DANGER),
    ],
]

# Placeholder for future music-related functionality
MUSIC_BACK_BTN = [
    [
        InlineKeyboardButton(text="Soon", callback_data=f"soom", style=ButtonStyle.PRIMARY),
    ],
]

# Alternative back and close buttons
S_BACK = [
    [
        InlineKeyboardButton(text="Back", callback_data="SBACK", style=ButtonStyle.DEFAULT),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]

# Back button specific to the chatbot help menu
CHATBOT_BACK = [
    [
        InlineKeyboardButton(text="Back", callback_data="CHATBOT_BACK", style=ButtonStyle.DEFAULT),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]

# Basic help and close buttons for the start command in groups
HELP_START = [
    [
        InlineKeyboardButton(text="Help", callback_data="HELP", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]

# Direct link to private message help from a group chat
HELP_BUTN = [
    [
        InlineKeyboardButton(
            text="Help", url=f"https://t.me/{app.username}?start=help", style=ButtonStyle.PRIMARY
        ),
        InlineKeyboardButton(text="Close", callback_data="CLOSE", style=ButtonStyle.DANGER),
    ],
]

# Detailed 'About' menu with multiple external links and navigation
ABOUT_BTN = [
    [
        InlineKeyboardButton(text="Support", url=f"https://t.me/{SUPPORT_GRP}", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Help", callback_data="HELP", style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton(text="Owner", user_id=OWNER, style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton(text="Updates", url=f"https://t.me/{UPDATE_CHNL}", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="Back", callback_data="BACK", style=ButtonStyle.DEFAULT),
    ],
]
