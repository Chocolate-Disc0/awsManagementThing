import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import time
import datetime
from supabase import create_client, Client

load_dotenv()
supabaseUrl = os.getenv('SUPABASE_URL')
supabaseKey = os.getenv('SUPABASE_KEY')
supabaseClient = create_client(supabaseUrl, supabaseKey)
token = os.getenv('DISCORD_TOKEN') 
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=':3', intents=intents)

utc = datetime.timezone.utc
times = [datetime.time(hour=9, tzinfo=utc), datetime.time(hour=13, minute=20, tzinfo=utc)]

try:
    test = supabaseClient.table('feedingrun').select('*').execute()
    print(test.data)
except Exception as e:
    print(f"Error connecting to Supabase: {e}")

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    remind.start()

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

# @bot.command()
# async def reminder(ctx):
#     await ctx.send("OKAAY I WILL REMINDS >^. .^<")
#     await asyncio.sleep((18 - time.localtime()[3] - 1) * 3600 + (60 - time.localtime()[4]) * 60)
#     print((17 - time.localtime()[3] - 1) * 3600 + (60 - time.localtime()[4]) * 60)
#     await bot.get_channel(1527421490520133652).send(f"HAY {bot.get_user(485499418817200169).mention} ITD TIMED TO FEED TEH CARS ≽^•⩊•^≼ ")

@tasks.loop(time=times)
async def remind():
    dayLetter = datetime.datetime.now().strftime("%A")
    day = datetime.datetime.now().weekday()
    await bot.get_channel(1527421490520133652).send(f"HAY {bot.get_user(485499418817200169).mention} ITD TIMED TO FEED TEH CARS ≽^•⩊•^≼ ")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)