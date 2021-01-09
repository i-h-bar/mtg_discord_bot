import os
import io
import discord

from requests_handler.scryfall import get_card
from table_top_items.calculator import calculate
from table_top_items.coin import flip_coin
from table_top_items.dice import roll_dice
from discord.ext import commands


client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    print("Bot initialised")


@client.event
async def on_message(message):
    if message.content.startswith("/r") or message.content.startswith("/roll"):
        await roll_dice(message)

    elif message.content.startswith("/c"):
        channel = message.channel
        reply = f"{message.author.mention} `{message.content.replace(' ', '').replace('/c', '').strip()}` = "
        reply += str(await calculate(message.content.replace("/c", "")))
        await channel.send(reply)

    elif message.content.startswith("/flip"):
        await flip_coin(message)

    elif message.content.startswith("/s") or message.content.startswith("/search"):
        channel = message.channel
        reply = f"{message.author.mention}\n"
        card_name = message.content.replace("/search", "").replace("/s", "").strip()
        card_info, card_image = await get_card(card_name)
        await channel.send(reply, file=discord.File(io.BytesIO(card_image), f"{card_name.replace(' ', '_')}.png"))

    elif message.content.startswith("/help") or message.content.startswith("/h"):
        channel = message.channel
        reply = f"{message.author.mention}\n"

        await channel.send(reply)


client.run(os.getenv("mtg_bot_token"))
