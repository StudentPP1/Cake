# secret commands for developers

import discord
from discord.ext import commands


class SecretCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # kick участников (через упоминание)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)

    # ban участников (через упоминание)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.ban(reason=reason)


async def setup(client):
    await client.add_cog(SecretCommands(client))
