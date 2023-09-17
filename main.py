import discord
import os
import random
from discord.ext import commands
import asyncio
from config import settings
from web import keep_alive
import sys
import time

PREFIX = settings["PREFIX"]

client = commands.Bot(command_prefix=PREFIX, intents=settings["INTENTS"], help_command=None)


@client.command(aliases=["help"])
async def __help(ctx):
    emb = discord.Embed(title="List of commands")

    emb.add_field(name=f'{PREFIX}clear',
                  value=f'Cleaning the chat\nExample: {PREFIX}clear <count>\n{PREFIX}clear MAX: 50', inline=False)

    emb.add_field(name=f'{PREFIX}hello',
                  value='Greeting', inline=False)

    emb.add_field(name=f'{PREFIX}exchange',
                  value='Exchange rate', inline=False)

    emb.add_field(name=f'{PREFIX}nick',
                  value=f"Change the name of the person\nExample: {PREFIX}nick <@user> <new nick>", inline=False)

    emb.add_field(name=f'{PREFIX}tic_toe',
                  value=f'Tic Tac Toe\nExample: {PREFIX}tic_toe <@user> <@user>', inline=False)

    emb.add_field(name=f'{PREFIX}joke',
                  value='Tell a joke', inline=False)

    emb.add_field(name=f'{PREFIX}mute',
                  value=f'Threw into the mute\nExample: {PREFIX}mute <@user>', inline=False)

    emb.add_field(name=f'{PREFIX}un_mute',
                  value=f'Thrown out of the mute\nExample: {PREFIX}un_mute <@user>', inline=False)

    emb.add_field(name=f'{PREFIX}send',
                  value=f'Write a message\nExample: {PREFIX}send <@user>', inline=False)

    emb.add_field(name=f'{PREFIX}spam',
                  value=f'Example: {PREFIX}spam <@user> <count> MAX: 100', inline=False)

    emb.add_field(name=f'{PREFIX}timer',
                  value='Timer for minutes', inline=False)

    emb.add_field(name=f'{PREFIX}t',
                  value=f'Translator\nExample: {PREFIX}t <language>', inline=False)

    emb.add_field(name=f'{PREFIX}g',
                  value='Google query', inline=False)

    emb.add_field(name=f'{PREFIX}create_role',
                  value=f'Create a new role\nExample: '
                        f'{PREFIX}create_role <role_name> <hex_color>'
                        f'\n{PREFIX}create_role <role_name>',
                  inline=False)

    emb.add_field(name=f'{PREFIX}get_role',
                  value=f'Issue a role\nExample: {PREFIX}get_role <@user> <role_name>', inline=False)

    emb.add_field(name=f'{PREFIX}del_role',
                  value=f'Delete role\nExample: {PREFIX}del_role <@user> <role_name>', inline=False)

    emb.add_field(name=f'{PREFIX}find',
                  value=f'Download video from YouTube\nExample: {PREFIX}find <key words for searching or url>',
                  inline=False)

    emb.add_field(name=f'{PREFIX}play',
                  value=f'Play the video from YouTube in voice channel\nExample: {PREFIX}play <url>', inline=False)

    emb.add_field(name=f'{PREFIX}pause',
                  value=f'Pause the music', inline=False)

    emb.add_field(name=f'{PREFIX}resume',
                  value=f'Resume the music', inline=False)

    emb.add_field(name=f"{PREFIX}surprise",
                  value="Get a surprise (every day at 10:30 am)", inline=False)

    emb.add_field(name=f"{PREFIX}create-img",
                  value="Image generation according to Tupper's formula", inline=False)

    await ctx.send(embed=emb)


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    print(f"cogs.{extension} is loaded")
    await client.load_extension(f"cogs.{extension}")


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    print(f"cogs.{extension} is unloaded")
    await client.unload_extension(f"cogs.{extension}")


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    print(f"cogs.{extension} is reloaded")
    await client.reload_extension(f"cogs.{extension}")


async def main():
    async with client:
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.start(settings["TOKEN"])


while True:
    try:
        try:
            os.remove("members.db")
        except:
            pass
        for f in os.listdir():
            if f.endswith(".mp3"):
                os.remove(f)
        keep_alive()
        asyncio.run(main())
    except discord.errors.HTTPException:
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        time.sleep(random.choice([i for i in range(1, 10)]))
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as ex:
        print(ex)
        time.sleep(random.choice([i for i in range(1, 10)]))
        os.execl(sys.executable, sys.executable, *sys.argv)
