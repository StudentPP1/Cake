import discord
import os

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}

settings = {
    "INTENTS": intents,
    "TOKEN": os.environ["BOT_TOKEN"],
    "NAME": "Cake",
    "ID": os.environ["BOT_ID"],
    "PREFIX": '?',
    "YDL_OPTIONS": YDL_OPTIONS
}