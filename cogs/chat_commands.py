# public functions for chat of guild

import discord
import requests
import sqlite3
import datetime
import random
import string
import sqlite3
import lxml
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
from discord.ext import commands
from config import settings
import time

PREFIX = settings["PREFIX"]


class ChatCommands(commands.Cog):
    jokes = None

    def __init__(self, client):
        self.client = client

    # скачать видео
    @commands.command()
    async def find(self, ctx, *, arg):
        await ctx.send("loading...")
        with YoutubeDL(settings["YDL_OPTIONS"]) as ydl:
            if 'https://' in arg:
                info = ydl.extract_info(arg, download=True)
            else:
                info = ydl.extract_info(f"ytsearch:{arg}",
                                        download=True)
        file = 'video.mp4'
        await ctx.send(file=discord.File(file))
        os.system(f"rm {file}")

    # очистка сообщений
    @commands.command()
    async def clear(self, ctx, count=100):
        await ctx.channel.purge(limit=count + 1)

    # приветствие
    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.purge(limit=1)
        author = ctx.message.author
        emb = discord.Embed(color=discord.Color.green())
        emb.set_author(name=author.name, icon_url=author.avatar)
        emb.set_footer(text="Привіт")
        await ctx.send(embed=emb)

    # курс доллара и евро
    @commands.command()
    async def exchange(self, ctx):
        await ctx.channel.purge(limit=1)
        req = requests.get('https://bank.gov.ua/ua/markets/exchangerates')
        soup = BeautifulSoup(req.text, 'lxml')
        dollar_value, euro_value = [i.find_all('td')[-1].text for i in soup.find(class_="inner").find_all('tr')[8:10]]
        emb = discord.Embed(title='Курс валют',
                            color=discord.Color.green())
        emb.add_field(name='$', value=dollar_value)
        emb.add_field(name='€', value=euro_value)
        await ctx.send(embed=emb)

    # следующий урок
    @commands.command()
    async def lesson(self, ctx, week: str):
        if week == '1' or week == '2':
            days = [i for i in range(5)]
            time_now = datetime.datetime.now()
            currently_day = datetime.datetime.weekday(time_now)
            currently_time = float(str(time_now).split()[-1][:5].replace(':', '.'))
            if not currently_day in days:
                emb = discord.Embed(title="Я поламався",
                                    description="Зараз вихідні",
                                    color=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                c = sqlite3.connect("lessons.db")
                c1 = c.cursor()
                currently_day = days[currently_day]
                table = c1.execute("SELECT * FROM week{0} WHERE day = {1}".format(int(week), currently_day))
                day = {i[1:-1]: i[-1] for i in table}

                print_time = False

                for i in day.keys():
                    start_lesson, end_lesson = i
                    if float(start_lesson) > currently_time:
                        if int(str(start_lesson).split('.')[-1]) > 10:
                            start_lesson = str(start_lesson).replace('.', ':')
                        else:
                            start_lesson = str(start_lesson).replace('.', ':') + '0'
                        emb = discord.Embed(title=f"Наступний урок {i.lower()}",
                                            description=f"Початок в {start_lesson}",
                                            color=discord.Color.green())
                        await ctx.send(embed=emb)
                        print_time = True
                        break
                if not print_time:
                    emb = discord.Embed(title="Уроків не буде",
                                        color=discord.Color.red())
                    await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="Я поламався",
                                description="Вкажи номер неділі",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    # рандомные шутки из сталкера
    @commands.command()
    async def joke(self, ctx):
        if self.jokes is None:
            url = "https://stalker.fandom.com/ru/wiki/%D0%90%D0%BD%D0%B5%D0%BA%D0%B4%D0%BE%D1%82%D1%8B"
            req = requests.get(url).text
            soup = BeautifulSoup(req, parser="lxml")
            names = [i.text for i in soup.find_all(class_="mw-headline") if "Шутка" in i.text]
            jokes = [i.find("p").text for i in soup.find_all(class_="poem")][:len(names)]
            self.jokes = [i for i in zip(names, jokes)]
        else:
            pass
        name, joke = random.choice(self.jokes)
        await ctx.send(embed=discord.Embed(title=name, description=joke, color=discord.Color.random()))

    # крестики - нолики
    @commands.command()
    async def tic_toe(self, ctx, x: discord.Member, o: discord.Member):

        channel = ctx.channel
        win_code = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],

            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],

            [1, 5, 9],
            [3, 5, 7],
        ]
        field = {str(i + 1): str(i + 1) for i in range(9)}

        img = Image.new("RGBA", (200, 200), '#ffffff')
        draw_img = ImageDraw.Draw(img)
        draw_img.line([60, 0, 60, 200], fill='#000000', width=5)
        draw_img.line([140, 0, 140, 200], fill='#000000', width=5)
        draw_img.line([0, 60, 200, 60], fill='#000000', width=5)
        draw_img.line([0, 140, 200, 140], fill='#000000', width=5)
        embed = discord.Embed()
        img.save("tic_toe.png")

        def draw(figure, place):
            if figure == 1:
                if place in [0, 1, 2]:
                    draw_img.line([5 + place * 70, 5, 50 + place * 70, 50], fill='#000000', width=5)
                    draw_img.line([50 + place * 70, 5, 5 + place * 70, 50], fill='#000000', width=5)
                    img.save("tic_toe.png")
                elif place in [3, 4, 5]:
                    draw_img.line([5 + (place - 3) * 70, 5 + 70, 50 + (place - 3) * 70, 50 + 70], fill='#000000',
                                  width=5)
                    draw_img.line([50 + (place - 3) * 70, 5 + 70, 5 + (place - 3) * 70, 50 + 70], fill='#000000',
                                  width=5)
                    img.save("tic_toe.png")
                elif place in [6, 7, 8]:
                    draw_img.line([5 + (place - 6) * 70, 5 + 140, 50 + (place - 6) * 70, 50 + 140], fill='#000000',
                                  width=5)
                    draw_img.line([50 + (place - 6) * 70, 5 + 140, 5 + (place - 6) * 70, 50 + 140], fill='#000000',
                                  width=5)
                    img.save("tic_toe.png")
            else:
                if place in [0, 1, 2]:
                    draw_img.ellipse([5 + place * 70, 5, 50 + place * 70, 50], fill='#000000', width=5)
                    img.save("tic_toe.png")
                elif place in [3, 4, 5]:
                    draw_img.ellipse([5 + (place - 3) * 70, 5 + 70, 50 + (place - 3) * 70, 50 + 70], fill='#000000',
                                     width=5)
                    img.save("tic_toe.png")
                elif place in [6, 7, 8]:
                    draw_img.ellipse([5 + (place - 6) * 70, 5 + 140, 50 + (place - 6) * 70, 50 + 140], fill='#000000',
                                     width=5)
                    img.save("tic_toe.png")

        def verify_win(side, play_field):
            side_places = set(sorted([int(i) for i in play_field.keys() if play_field[i] == side]))
            print(side, side_places)
            flag = False
            for i in win_code:
                print(i, side_places, set(i), side_places.intersection(set(i)))
                if len(side_places.intersection(set(i))) == 3:
                    flag = True
            return flag

        def verify_draw(play_field):
            free_places = [i for i in play_field.values() if i != 'x' and i != 'o']
            print(free_places)
            return free_places == []

        while True:
            await ctx.send("Хрестики-Нолики", file=discord.File(fp="tic_toe.png"))
            await ctx.send(f"X: {x}, твій хід:")
            while True:
                m = [message.content async for message in channel.history(limit=1)][0]
                _id = int([message.author.id async for message in channel.history(limit=1)][0])
                if m in field.values() and x.id == _id:
                    field[m] = 'x'
                    break

            draw(1, int(m) - 1)
            if verify_win('x', field):
                await ctx.send(f"{x} - win")
                break
            if verify_draw(field):
                await ctx.send("Нічия")
                break

            await ctx.send("Хрестики-Нолики", file=discord.File(fp="tic_toe.png"))
            await ctx.send(f"O: {o}, твій хід:")
            while True:
                m = [message.content async for message in channel.history(limit=1)][0]
                _id = int([message.author.id async for message in channel.history(limit=1)][0])
                if m in field.values() and o.id == _id:
                    field[m] = 'o'
                    break

            draw(0, int(m) - 1)
            if verify_win('o', field):
                await ctx.send(f"{o} - win")
                break
            if verify_draw(field):
                await ctx.send("Нічия")
                break


async def setup(client):
    await client.add_cog(ChatCommands(client))

