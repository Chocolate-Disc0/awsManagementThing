import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler =  logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=':3', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "ashfur" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} dont use no no words /ᐠ ¬`‸´¬マ")
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello hru {ctx.author.mention}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)