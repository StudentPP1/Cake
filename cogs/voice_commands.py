# all public functions for voice chat of guild

import discord
from youtube_dl import YoutubeDL
from discord.ext import commands
from config import settings


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
            emb = discord.Embed(title="Я поламався",
                                description=f"{member.mention} не в муті",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    # старт проигрывания музыки
    @commands.command()
    async def play(self, ctx, *, arg):
        voice = await ctx.author.voice.channel.connect()
        await ctx.channel.purge(limit=1)

        with YoutubeDL(settings["YDL_OPTIONS"]) as ydl:
            if 'https://' in arg:
                info = ydl.extract_info(arg, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

        url = info['formats'][0]['url']
        voice.play(
            discord.FFmpegPCMAudio(executable=r"FFmpeg\ffmpeg-20140905-git-720c21d-win32-static\bin\ffmpeg.exe",
                                   source=url))

    # конец проигрывания музыки
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.channel.purge(limit=1)


async def setup(client):
    await client.add_cog(VoiceCommands(client))
