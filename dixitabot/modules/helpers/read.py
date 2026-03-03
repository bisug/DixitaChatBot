from config import OWNER_ID, SUPPORT_GRP
from dixitabot import app

# Welcome message template for the /start command in groups
START = f"""
<b>Hey, I am <a href='https://t.me/{app.username}'>{app.name}</a></b>
<b>An AI based chatbot</b>
<b>──────────────</b>
<b>Usage /chatbot [on/off]</b>
<b><spoiler>Hit help button for help.</spoiler></b>
"""

# Base help menu text template
HELP_READ = f"""
<u><b>Commands for {app.name}</b></u>
<u><b>Are given below!</b></u>
<b>All the commands can be used with:/</b>
<b>──────────────</b>
<b><spoiler>©️ <a href='tg://user?id={OWNER_ID}'>Owner</a></spoiler></b>
"""

# Description of the various diagnostic and utility tools available
TOOLS_DATA_READ = f"""
<u><b>Tools for {app.name} are:</b></u>
<b>Use /repo for getting source code!</b>
<b>──────────────</b>
<b>Use /ping for checking the ping of {app.name}</b>
<b>──────────────</b>
<b>Use /id to get your user id, chat id and message id all in a single message.</b>
<b>──────────────</b>
<b><spoiler>©️ <a href='tg://user?id={OWNER_ID}'>Owner</a></spoiler></b>
"""

# Specific help instructions for the chatbot toggle command
CHATBOT_READ = f"""
<u><b>Commands for {app.name}</b></u>
<b>Use /chatbot to enable/disable the chatbot.</b>
<b>Note: The above command for chatbot work in group only!!</b>
<b>───────────────</b>
<b><spoiler>©️ <a href='tg://user?id={OWNER_ID}'>Owner</a></spoiler></b>
"""

# Information regarding the bot's source code and repository
SOURCE_READ = f"<b>Hey, the source code of <a href='https://t.me/{app.username}'>{app.name}</a> is given below.</b>\n<b>Please fork the repo &amp; give the star ✯</b>\n<b>──────────────────</b>\n<b>Here is the <a href='https://github.com/bisug/DAXXCHATBOT'>source code</a></b>\n<b>──────────────────</b>\n<b>If you face any problem then contact at <a href='https://t.me/{SUPPORT_GRP}'>support chat</a>.</b>\n<b><spoiler>©️ <a href='tg://user?id={OWNER_ID}'>Owner</a></spoiler></b>"

# Placeholder for administrator-specific help content
ADMIN_READ = f"Soon"

# General overview and purpose of the DixitaChatBot
ABOUT_READ = f"""
<b><a href='https://t.me/{app.username}'>{app.name}</a> is an AI based chat-bot.</b>
<b><a href='https://t.me/{app.username}'>{app.name}</a> replies automatically to a user.</b>
<b>Helps you in activating your groups.</b>
<b>Written in <a href='https://www.python.org'>Python</a> with <a href='https://www.mongodb.com'>Mongo-db</a> as a database</b>
<b>──────────────</b>
<b>Click on the buttons given below for getting basic help and info about <a href='https://t.me/{app.username}'>{app.name}</a></b>
"""
