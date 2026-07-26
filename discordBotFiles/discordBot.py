import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import datetime
from zoneinfo import ZoneInfo
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

localTime = ZoneInfo("Asia/Karachi")
times = [datetime.time(hour=9, tzinfo=localTime), datetime.time(hour=18, minute=0, tzinfo=localTime)]
FEEDING_CHANNEL_ID = 1527421490520133652
WELCOME_CHANNEL_ID = 1530693475761127425

try:
    test = supabaseClient.table('feedingrun').select('*').execute()
except Exception as e:
    print(f"Error connecting to Supabase: {e}")

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    remind.start()

@bot.event
async def on_member_join(member):
    await bot.get_channel(WELCOME_CHANNEL_ID).send(f"WELCOME TO THE SERVER {member.mention}!!!!!!!  ฅ^•ﻌ•^ฅ")

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

@tasks.loop(time=times)
async def remind():
    day = datetime.datetime.now(localTime).strftime("%a")
    hour = datetime.datetime.now(localTime).hour
    response = (
    supabaseClient.table("feedingrun")
    .select("*")
    .match({"feeding_day": day, "feeding_time": hour})
    .execute()
    )
    await bot.get_channel(FEEDING_CHANNEL_ID).send(f"HAY {bot.get_user(response.data[0]['discord_id']).mention} ITD TIMED TO FEED TEH CARS AT BKOLCK {response.data[0]['block_num']}  ≽^•⩊•^≼ ")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)