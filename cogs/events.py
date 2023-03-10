# all events for bot

import discord
from config import settings
from discord.ext import commands


class Events(commands.Cog):
    PREFIX = settings["PREFIX"]

    def __init__(self, client):
        self.client = client

    # сообщение об подключение бота
    @commands.Cog.listener()
    async def on_ready(self):
        print("Бот підключився")
        # задать статус бота (online, activity - что делает)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f"тортик | {self.PREFIX}help"))

    # если не существует команды
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.author.mention} такої команди не існує")


async def setup(client):
    await client.add_cog(Events(client))
