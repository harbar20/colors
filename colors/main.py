import discord
from discord.ext import commands
import re
import requests
from dotenv import load_dotenv
import os
from PIL import Image, ImageColor
from io import BytesIO

load_dotenv()
bot = commands.Bot(command_prefix="c!")
token = os.environ.get("TOKEN")

@bot.event
async def on_ready():
    print("Colors is ready!")
    await bot.change_presence(activity=discord.Game(name=f"with colors in {len(bot.guilds)} servers."))

@bot.event
async def on_message(message):
    if message.author != bot.user:
        hexRegexs = re.findall("#[A-Fa-f0-9]{6}", message.content)
        if hexRegexs:
            files = []
            for hexCode in hexRegexs:
                img = Image.new("RGB", (32, 32), ImageColor.getrgb(hexCode))
                with BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    files.append(discord.File(fp=image_binary, filename=f'{hexCode[1:]}.png'))
            
            await message.channel.send(files=files)

        await bot.process_commands(message)

@bot.command()
async def color(ctx, *args):
    files = []
    for hexCode in args:
        img = Image.new("RGB", (32, 32), ImageColor.getrgb(hexCode))
        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            files.append(discord.File(fp=image_binary, filename=f'{hexCode[1:]}.png'))
            
    await ctx.message.channel.send(files=files)

bot.run(token)