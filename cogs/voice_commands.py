# all public functions for voice chat of guild
import asyncio
import datetime
import os
import re

from pytube import Playlist
import discord
import yt_dlp
from discord.ext import commands
# python -m pip install -U discord.py[voice]


class VoiceCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        try:
            await ctx.channel.purge(limit=1)
            await member.edit(mute=True)
            emb = discord.Embed(title="Threw into the mute",
                                description=f"{member.mention}",
                                color=discord.Color.orange())
            await ctx.send(embed=emb)
        except Exception as ex:
            print(ex)
            emb = discord.Embed(title="I'm in trouble",
                                description=f"{member.mention} not in voice chat",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    @commands.command()
    async def un_mute(self, ctx, member: discord.Member):
        try:
            await ctx.channel.purge(limit=1)
            await member.edit(mute=False)
            emb = discord.Embed(title="Thrown out of the mute",
                                description=f"{member.mention}",
                                color=discord.Color.green())
            await ctx.send(embed=emb)
        except Exception as ex:
            print(ex)
            emb = discord.Embed(title="I'm in trouble",
                                description=f"{member.mention} doesn't in mute",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    @commands.command()
    async def play(self, ctx, url):
        def play_music(current_url, ydl_opts):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(current_url)

            audio_source = discord.FFmpegPCMAudio(executable=ydl_opts["ffmpeg_location"],
                                                  source=ydl_opts["outtmpl"]['default'])

            voice_channel.play(audio_source)
        try:
            voice_channel = await ctx.message.author.voice.channel.connect()

            if voice_channel.is_playing():
                await ctx.send(f'{ctx.message.author.mention}, is already playing.')

            else:
                if url.startswith('https://www.youtube.com/watch?'):
                    ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True',
                                'outtmpl': f"{re.sub('[^0-9]', '', str(datetime.datetime.now()))}_play.mp3",
                                # your way to ffmpeg
                                "ffmpeg_location": r"E:\Projects\Python\Cake\FFmpeg\ffmpeg-20140905-git-720c21d-win32-static\bin\ffmpeg.exe"}
                    play_music(url, ydl_opts)

                elif url.startswith('https://www.youtube.com/playlist?'):
                    print("Getting playlist...")
                    videos = Playlist(url)
                    video_urls = [video_url for video_url in videos.video_urls]
                    for video_url in video_urls:
                        ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True',
                                    'outtmpl': f"{re.sub('[^0-9]', '', str(datetime.datetime.now()))}_play.mp3",
                                    # your way to ffmpeg
                                    "ffmpeg_location": r"E:\Projects\Python\Cake\FFmpeg\ffmpeg-20140905-git-720c21d-win32-static\bin\ffmpeg.exe"}
                        play_music(video_url, ydl_opts)

        except Exception as ex:
            print(ex)
            await ctx.send('Already connected or failed to connect')

    @commands.command(name="pause")
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
        except:
            await ctx.send("Currently no audio is playing.")

    @commands.command(name="resume")
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
        except:
            await ctx.send("The audio is not paused.")


async def setup(client):
    await client.add_cog(VoiceCommands(client))
