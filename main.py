import discord
import os
from dotenv import load_dotenv
from get_departure_time import get_departure_time

load_dotenv()


TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')

@client.event
async def on_message(message):

    if message.content.lower().startswith("!train"):
        # So I don't doxx myself lol
        my_station = os.getenv("MY_STATION")
        my_platform = os.getenv("MY_PLATFORM")
        minutes_to_station = int(os.getenv("MINUTES_TO_STATION"))

        minutes_left, seconds_left = get_departure_time(my_station, my_platform)

        leave_in = minutes_left - minutes_to_station

        await message.channel.send(f"The next train arrives in {minutes_left} minutes and {seconds_left} seconds. Please leave in {leave_in} minutes!")

client.run(TOKEN)
