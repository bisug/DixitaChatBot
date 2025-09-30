from pyrogram import Client, enums, filters
import asyncio
from NoxxNetwork import NoxxBot 
from pyrogram.handlers import MessageHandler


@NoxxBot.on_message(filters.command("dice"))
async def dice(bot, message):
    x = await bot.send_dice(message.chat.id)
    m = x.dice.value
    await message.reply_text(f"🎲 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@NoxxBot.on_message(filters.command("dart"))
async def dart(bot, message):
    x = await bot.send_dice(message.chat.id, "🎯")
    m = x.dice.value
    await message.reply_text(f"🎯 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@NoxxBot.on_message(filters.command("basket"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🏀")
    m = x.dice.value
    await message.reply_text(f"🏀 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@NoxxBot.on_message(filters.command(["jackpot", "slot"]))
async def jackpot(bot, message):
    x = await bot.send_dice(message.chat.id, "🎰")
    m = x.dice.value
    await message.reply_text(f"🎰 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@NoxxBot.on_message(filters.command(["ball", "bowling"]))
async def ball(bot, message):
    x = await bot.send_dice(message.chat.id, "🎳")
    m = x.dice.value
    await message.reply_text(f"🎳 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@NoxxBot.on_message(filters.command("football"))
async def football(bot, message):
    x = await bot.send_dice(message.chat.id, "⚽")
    m = x.dice.value
    await message.reply_text(f"⚽ Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@NoxxBot.on_message(filters.command("toss"))
async def toss(bot, message):
    result = "Heads 🪙" if bool(asyncio.get_event_loop().time() % 2 < 1) else "Tails 🪙"
    await message.reply_text(f"🪙 Coin Toss Result: `{result}`", quote=True)


@NoxxBot.on_message(filters.command("roll"))
async def roll(bot, message):
    from random import randint
    result = randint(1, 6)
    await message.reply_text(f"🎲 You rolled a `{result}`!", quote=True)
