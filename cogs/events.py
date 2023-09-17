# all events for bot
import discord
from config import settings
from discord.ext import commands
import sqlite3


class Events(commands.Cog):
    PREFIX = settings["PREFIX"]

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The bot has connected")
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Game(f"Cake | {self.PREFIX}help"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.author.mention} such a command does not exist")

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        with sqlite3.connect("members.db") as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO members VALUES (?, ?)""", (str(member.id), 1))


async def setup(client):
    await client.add_cog(Events(client))
