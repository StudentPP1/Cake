import discord
import os
from discord.ext import commands
import asyncio
from config import settings
from web import keep_alive

PREFIX = settings["PREFIX"]

client = commands.Bot(command_prefix=PREFIX, intents=settings["INTENTS"], help_command=None)


# команда help
@client.command(aliases=["help"])
async def __help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Перелік команд')
    emb.add_field(name=f'{PREFIX}tic_toe', value='Хрестики-Нолики', inline=False)
    emb.add_field(name=f'{PREFIX}joke', value='Розказати жарт', inline=False)
    emb.add_field(name=f'{PREFIX}mute', value='Кинути в мут', inline=False)
    emb.add_field(name=f'{PREFIX}un_mute', value='Зняти мут', inline=False)
    emb.add_field(name=f'{PREFIX}clear', value='Очищення чату', inline=False)
    emb.add_field(name=f'{PREFIX}hello', value='Привітання', inline=False)
    emb.add_field(name=f'{PREFIX}exchange', value='Курс валют', inline=False)
    emb.add_field(name=f'{PREFIX}create_role', value='Створити нову роль', inline=False)
    emb.add_field(name=f'{PREFIX}get_role', value='Видати роль', inline=False)
    emb.add_field(name=f'{PREFIX}send', value='Написати повідомлення', inline=False)
    emb.add_field(name=f'{PREFIX}timer', value='Таймер на n хв', inline=False)
    emb.add_field(name=f'{PREFIX}del_role', value='Видалити роль', inline=False)
    emb.add_field(name=f'{PREFIX}spam', value='Спам', inline=False)
    emb.add_field(name=f'{PREFIX}lesson', value='Наступний урок', inline=False)
    emb.add_field(name=f'{PREFIX}play', value='Програвання музики', inline=False)
    emb.add_field(name=f'{PREFIX}disconnect', value='Видаляє бота з голосового каналу', inline=False)
    await ctx.send(embed=emb)


# загрузка
@client.command()
@commands.is_owner()
async def load(ctx, extension):  # !load main (загружаем файл в проект)
    print(f"cogs.{extension} is loaded")
    await client.load_extension(f"cogs.{extension}")


# выгрузка
@client.command()
@commands.is_owner()
async def unload(ctx, extension):  # !unload main (выгружаем файл)
    print(f"cogs.{extension} is unloaded")
    await client.unload_extension(f"cogs.{extension}")


# перезагрузка
@client.command()
@commands.is_owner()
async def reload(ctx, extension):  # !reload main (перезагружаем файл)
    print(f"cogs.{extension} is reloaded")
    await client.reload_extension(f"cogs.{extension}")


# цикл для перебора файлов
async def main():
    async with client:
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.start(settings["TOKEN"])


asyncio.run(main())


# подключение
keep_alive()
