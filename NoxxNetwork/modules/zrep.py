import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import IMG
from NoxxNetwork import NoxxBot

start_txt = """<b>
✪ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ @sʜʀᴜᴛɪʙᴏᴛs ✪

➲ ᴇᴀsʏ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ  
➲ ɴᴏ ʙᴀɴ ɪssᴜᴇs  
➲ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs  
➲ 𝟸𝟺/𝟽 ʟᴀɢ-ғʀᴇᴇ  

⟢ ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴍʏ ʀᴇᴘᴏs  
⟢ sᴛᴀʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴍᴍᴜɴɪᴛʏ!
</b>"""

repo_buttons = [
    [InlineKeyboardButton("⋆ ɴᴏʀᴍᴀʟ ᴄʜᴀᴛʙᴏᴛ ⋆", url="https://github.com/bisug/DixitaChatBot")],
    [InlineKeyboardButton("⋆ ᴄᴏᴍᴍᴜɴɪᴛʏ ⋆", url="https://t.me/dear_sumi")],
]


async def send_repo(_, m: Message):
    reply_markup = InlineKeyboardMarkup(repo_buttons)
    await m.reply_photo(
        photo="https://telegra.ph/file/d17d1400b565e38b66fac-9d44ccc0096290276a.jpg",
        caption=start_txt,
        reply_markup=reply_markup,
    )


@NoxxBot.on_cmd(["repo", "repos", "source", "repo_source"])
async def repo_handler(client, message: Message):
    await send_repo(client, message)
