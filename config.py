import discord
import os

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True

YDL_OPTIONS = {
  'format': '[height<=360][filesize<200M]',
  'outtmpl': 'video.mp4',
  'noplaylist': True,
  'nocheckcertificate': True,
  'ignoreerrors': False,
  'logtostderr': False,
  'quiet': True,
  'no_warnings': True,
  'default_search': 'auto'
}

settings = {
  "INTENTS": intents,
  "TOKEN": os.getenv("BOT_TOKEN"),
  "NAME": "Cake",
  "ID": os.getenv("BOT_ID"),
  "PREFIX": '?',
  "YDL_OPTIONS": YDL_OPTIONS,
}
