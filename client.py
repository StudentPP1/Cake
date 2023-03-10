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
    emb.add_field(name=f'{PREFIX}tic_toe', value=f'Хрестики-Нолики\nПриклад: {PREFIX}tic_toe <@user> <@user>',
                  inline=False)
    emb.add_field(name=f'{PREFIX}joke', value='Розказати жарт', inline=False)
    emb.add_field(name=f'{PREFIX}mute', value=f'Кинути в мут\nПриклад: {PREFIX}mute <@user>', inline=False)
    emb.add_field(name=f'{PREFIX}un_mute', value=f'Зняти мут\nПриклад: {PREFIX}un_mute <@user>', inline=False)
    emb.add_field(name=f'{PREFIX}clear', value=f'Очищення чату\nПриклад: {PREFIX}clear <count>, {PREFIX}clear',
                  inline=False)
    emb.add_field(name=f'{PREFIX}hello', value='Привітання', inline=False)
    emb.add_field(name=f'{PREFIX}exchange', value='Курс валют', inline=False)
    emb.add_field(name=f'{PREFIX}create_role', value=f'Створити нову роль\nПриклад: {PREFIX} <role_name> <hex_color>, '
                                                     f'{PREFIX} <role_name>', inline=False)
    emb.add_field(name=f'{PREFIX}get_role', value=f'Видати роль\nПриклад: {PREFIX}get_role <@user> <role_name>',
                  inline=False)
    emb.add_field(name=f'{PREFIX}send', value=f'Написати повідомлення\nПриклад: {PREFIX}send <@user> <message>',
                  inline=False)
    emb.add_field(name=f'{PREFIX}timer', value='Таймер на n хв', inline=False)
    emb.add_field(name=f'{PREFIX}del_role', value=f'Видалити роль\nПриклад: {PREFIX}del_role <@user> <role_name>',
                  inline=False)
    emb.add_field(name=f'{PREFIX}spam', value=f'Спам\nПриклад: {PREFIX}spam <@user> <message> <count>', inline=False)
    emb.add_field(name=f'{PREFIX}lesson', value=f'Наступний урок\nПриклад: {PREFIX}lesson <week number>', inline=False)
    emb.add_field(name=f'{PREFIX}play', value=f'Програвання музики\nПриклад: {PREFIX}play <url video on YouTube or '
                                              f'key words for searching>', inline=False)
    emb.add_field(name=f'{PREFIX}disconnect', value='Видаляє бота з голосового каналу', inline=False)
    emb.add_field(name=f'{PREFIX}find',
                  value=f'Скачування відео з YouTube\nПриклад: {PREFIX}play <key words for searching or url>',
                  inline=False)
    emb.add_field(name=f"{PREFIX}tags", value="Перелік пошукових тегів")
    emb.add_field(name=f"{PREFIX}find-tags", value="Знайти хентай по тегам")
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


while True:
    try:
        keep_alive()
        asyncio.run(main())
        # подключение
    except discord.errors.HTTPException as e:
        print(e)
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system('kill 1')
        os.system('python main.py')