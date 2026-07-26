import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import datetime
import io
import aiohttp
from zoneinfo import ZoneInfo
from supabase import create_client, Client

load_dotenv()
supabaseUrl = os.getenv('SUPABASE_URL')
supabaseKey = os.getenv('SUPABASE_KEY')
token = os.getenv('DISCORD_TOKEN') 
supabaseClient = create_client(supabaseUrl, supabaseKey)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=':3', intents=intents)

localTime = ZoneInfo("Asia/Karachi")
times = [datetime.time(hour=9, tzinfo=localTime), datetime.time(hour=18, minute=20, tzinfo=localTime)]
FEEDING_CHANNEL_ID = 1527421490520133652
WELCOME_CHANNEL_ID = 1530693475761127425
EMERGENCIES_CHANNEL_ID = 1527325468007731360
TALLY_BOT_ID = 1427635858604949667

try:
    test = supabaseClient.table('feedingrun').select('*').execute()
except Exception as e:
    print(f"Error connecting to Supabase: {e}")

@bot.event
async def on_ready():
    print(f"I THE GREAT {bot.user.name} AM READY TO GO RAHHHHHH >⩊<")
    remind.start()

@bot.event
async def on_member_join(member):
    await bot.get_channel(WELCOME_CHANNEL_ID).send(f"WELCOME TO THE SERVER {member.mention}!!!!!!!  ฅ^•ﻌ•^ฅ")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id == TALLY_BOT_ID:
        embedMessage = (message.embeds[0].description).split("\n")
        supabaseClient.table("reports").insert(
            {"description": embedMessage[0], "location": embedMessage[1], "photos": "\n\n".join(embedMessage[4:]), "reporter_contact": embedMessage[3]}).execute()
        photos = []
        async with aiohttp.ClientSession() as session:
            for index in range(4, len(embedMessage)):
                async with session.get(embedMessage[index]) as resp:
                    if resp.status != 200:
                        return await bot.get_channel(FEEDING_CHANNEL_ID).send('Could not download file :(')
                    data = io.BytesIO(await resp.read())
                    photos.append(discord.File(data, (embedMessage[index][33:].split("?"))[0]))
        if embedMessage[2] == "Yes":
            await bot.get_channel(EMERGENCIES_CHANNEL_ID).send(f"@everyone THERE IS AN INJURED ANIMAL AT {embedMessage[1]}\n{embedMessage[0]}\nYOU CAN CONTACT THE PERSON AT: {embedMessage[3]}", files=photos)
        else:
            await bot.get_channel(EMERGENCIES_CHANNEL_ID).send(f"THERE IS AN INJURED ANIMAL AT {embedMessage[1]}\n{embedMessage[0]}\nYou can contact the person at: {embedMessage[3]}", files=photos)
    elif "ashfur" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} dont use no no words /ᐠ ¬`‸´¬マ")
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"HELLO HRU {ctx.author.mention} OMGOMGOMG  ฅ^>⩊<^ฅ")

@bot.command()
async def goodgirl(ctx):
    await ctx.send(f"YES I AM YES I AM  (๑ > ᴗ < ๑)")

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
    feeders = len(response)

    for index in range(feeders):
        feedingMessage = await bot.get_channel(FEEDING_CHANNEL_ID).send(
            f"HAY {bot.get_user(response.data[index]['discord_id']).mention} ITD TIMED TO FEED TEH CARS AT BKOLCK {response.data[index]['block_num']} (react when you are done)  ≽^•⩊•^≼ ")
        await feedingMessage.add_reaction("😋")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)