# all public functions for voice chat of guild

import discord
from discord.ext import commands


class VoiceCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # mute участников (через упоминание)
    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        try:
            await ctx.channel.purge(limit=1)
            await member.edit(mute=True)
            emb = discord.Embed(title="Кинули в мут",
                                description=f"{member.mention}",
                                color=discord.Color.orange())
            await ctx.send(embed=emb)
        except Exception as ex:
            print(ex)
            emb = discord.Embed(title="Я поламався",
                                description=f"{member.mention} не в голосовому чаті",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    # un mute участников (через упоминание)
    @commands.command()
    async def un_mute(self, ctx, member: discord.Member):
        try:
            await ctx.channel.purge(limit=1)
            await member.edit(mute=False)
            emb = discord.Embed(title="Викинули з муту",
                                description=f"{member.mention}",
                                color=discord.Color.green())
            await ctx.send(embed=emb)
        except Exception as ex:
            print(ex)
            emb = discord.Embed(title="Я поламався",
                                description=f"{member.mention} не в муті",
                                color=discord.Color.red())
            await ctx.send(embed=emb)


async def setup(client):
    await client.add_cog(VoiceCommands(client))
