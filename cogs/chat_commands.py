# public functions for chat of guild

import openai
import discord
from threading import Thread
import threading
import requests
import re
import yt_dlp as youtube_dl
# python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
# pip install googletrans==3.1.0a0
# from youtube_dl import YoutubeDL
import googlesearch
from googletrans import Translator
import googletrans
import random
import os
import sqlite3
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
from discord.ext import commands
from config import settings
import schedule

list_tags = None
video_find = False
PREFIX = settings["PREFIX"]


class ScheduledFunction(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def set_surprise(self):
        try:
            os.remove("members.db")
        except:
            pass

    def run(self):
        # .day.at("10:30")
        schedule.every().day.at("10:30").do(self.set_surprise)
        while True:
            schedule.run_pending()


class ChatCommands(commands.Cog):
    jokes = None

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nick(self, ctx, member: discord.Member, nickname):
        await member.edit(nick=nickname)

    # очистка сообщений
    @commands.command()
    async def clear(self, ctx, count=50):
        try:
            if int(count) <= 50:
                await ctx.channel.purge(limit=count + 1)
            else:
                await ctx.send("Ти абоба?")
                await ctx.send("Ліміт 50 повідомлень")
        except:
            await ctx.send("Ти абоба?")

    @commands.command(aliases=["create-img"])
    async def create_img(self, ctx):
        f = lambda x, y: int(1 / 2 < ((y // 17) // (1 << (17 * x + (y % 17)))) % 2)

        def check(m):
            return m.author.id == ctx.author.id

        def from_k_to_bin(k: int) -> list:
            lists = [[] for x in range(17)]
            for y in range(16, -1, -1):
                for x in range(105, -1, -1):
                    lists[y].append(f(x, y + k))
            return lists

        try:
            await ctx.send("Введи k (ціле число) для генерації заображення: ")

            try:
                k = await self.client.wait_for("message", check=check, timeout=30)
                k = k.content
                k = int(re.sub(r"[^0-9]", '', k))
                print(k)
            except TimeoutError:
                return await ctx.send('Дуже довго думаеш, спробуй ще раз')

            lists = from_k_to_bin(k)
            image = Image.new("1", (106, 17))
            for y in range(17):
                for x in range(106):
                    image.putpixel(xy=(105 - x, 16 - y), value=(int(lists[y][x]),))
            image.save("k.png")

            embed = discord.Embed(title="Твоя картинка", description=f"k = {k}", color=discord.Colour.gold())
            embed.set_image(url="attachment://k.png")
            await ctx.send(file=discord.File(fp="k.png"), embed=embed)

        except Exception as ex:
            print(ex)
            await ctx.send("Введи ціле число наступного разу")

    # приветствие
    @commands.command()
    async def hello(self, ctx):
        # await ctx.send(ctx.channel.id)
        # await ctx.send(ctx.guild.id)
        await ctx.channel.purge(limit=1)
        author = ctx.message.author
        emb = discord.Embed(color=discord.Color.green())
        emb.set_author(name=author.name, icon_url=author.avatar)
        emb.set_footer(text="Привіт")
        await ctx.send(embed=emb)

    # скачать видео
    @commands.command()
    async def find(self, ctx, *, arg):
        global video_find
        if not video_find:
            await ctx.send("Loading...")
            try:
                video_find = True

                with youtube_dl.YoutubeDL(settings["YDL_OPTIONS"]) as ydl:
                    if 'https://' in arg:
                        ydl.extract_info(arg, download=True)
                    else:
                        ydl.extract_info(f"ytsearch:{arg}", download=True)

                    await ctx.send(file=discord.File('video.mp4'))
                    video_find = False

                os.system("rm video.mp4")
            except Exception as ex:
                await ctx.send("Розмір відео за великий")
        else:
            await ctx.send("Хтось уже щось качає!")

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

    @commands.command()
    async def surprise(self, ctx):
        gif_list = "s.gif"
        user_id = ctx.author.id
        flag = True

        for file in os.listdir():
            if file == "members.db":
                flag = False

        print("Is not db:", flag)
        if flag:
            print("Make db")
            member_list = [str(user.id) for user in ctx.guild.members]
            surprise_list = [1 for _ in range(len(member_list))]
            post = [(member_list[i], surprise_list[i]) for i in range(len(surprise_list))]

            with sqlite3.connect("members.db") as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS members (
        user_id TEXT NOT NULL,
        surprise INTEGER NOT NULL)""")
                cur.executemany("INSERT OR IGNORE INTO members VALUES (?, ?)", post)

        with sqlite3.connect("members.db") as con:
            cur = con.cursor()
            for i in cur.execute("""SELECT * FROM members"""):
                print(i)
            user_surprise = int(
                cur.execute(f"""SELECT surprise FROM members WHERE user_id == '{user_id}';""").fetchone()[0])

        print("User_surprise:", user_surprise)

        if user_surprise == 1:
            try:
                user_roles_list = [(role.id, role.name) for role in ctx.author.roles]

                with open("roles.txt", "r") as file:
                    roles = list(file.read().split('\n')[:-1])
                    print(roles)

                if set(user_roles_list) == set(roles):
                    await ctx.send(f"{ctx.author.mention} ти зібрав всі ролі!")
                else:
                    user_roles_list = [role[1] for role in user_roles_list]
                    print(user_roles_list)

                    for role in user_roles_list:
                        try:
                            roles.remove(role)
                        except Exception as ex:
                            print(ex)

                    random_role = random.choice(roles)

                    await ctx.guild.create_role(name=random_role, color=discord.Color.gold())
                    file = discord.File(gif_list, filename="SU1.gif")
                    embed = discord.Embed(color=0xff9900, title="Сюрприз",
                                              description=f"{ctx.author.mention}\nотримує роль **{random_role}**")
                    embed.set_image(url="attachment://SU1.gif")

                    with sqlite3.connect("members.db") as con:
                        cur = con.cursor()
                        cur.execute(f"""UPDATE members SET surprise = {0} WHERE user_id == '{user_id}';""")

                    await ctx.send(embed=embed, file=file)
                    role = discord.utils.get(ctx.message.guild.roles, name=random_role)
                    await ctx.author.add_roles(role)

                    currently_threads = [i.name for i in threading.enumerate()]
                    if not "Surpise_Update" in currently_threads:
                        ScheduledFunction("Surpise_Update").start()

                    print([i.name for i in threading.enumerate()])

            except Exception as ex:
                print(ex)
                with sqlite3.connect("members.db") as con:
                    cur = con.cursor()
                    cur.execute(f"""UPDATE members SET surprise = {1} WHERE user_id == '{user_id}';""")
                await ctx.send("Вибачай, нема ролей, try again")
        else:
            await ctx.send(f"{ctx.author.mention} приходи завтра!")
        print()

    @commands.command(aliases=["t", "transl", "translate"])
    async def tt(self, ctx, dest="en"):
        translator = Translator(service_urls=['translate.googleapis.com'])
        await ctx.send(": ")

        def check(m):
            return m.author.id == ctx.author.id

        try:
            answer = await self.client.wait_for("message", check=check, timeout=120)
            print(answer.content)
            await ctx.send(translator.translate(answer.content, dest=dest).text)

        except TimeoutError:
            return await ctx.send('Дуже довго думаеш, спробуй ще раз')
        except Exception as ex:
            print(ex)
            return await ctx.send(f"укажи мову на яку переводити: {googletrans.LANGUAGES}")

    @commands.command(aliases=["g", "google", "gl"])
    async def gg(self, ctx):
        await ctx.send("Напиши шуканий запрос: ")

        def check(m):
            return m.author.id == ctx.author.id

        try:
            # Ожидание ответа от пользователя. timeout - время ожидания.
            answer = await self.client.wait_for("message", check=check, timeout=120)
            query = answer.content
            print(query)

            # list_url = []
            # for search_url in googlesearch.search(answer, num=1, stop=5):
            #   list_url.append(search_url)

            def google_scrape(url):
                try:
                    page = requests.get(url=url).text
                    soup = BeautifulSoup(page, "html.parser")
                    return soup.title.text
                except:
                    return " "

            i = 1

            for url in googlesearch.search(query, stop=5):
                a = google_scrape(url)
                if a == " ":
                    emb = discord.Embed(title=f"{i}. {url}", color=discord.Color.random())
                else:
                    emb = discord.Embed(title=f"{i}. {a}", color=discord.Color.random())
                emb.url = url
                await ctx.send(embed=emb)

                print(str(i) + ". " + a)
                print(url)
                print()
                i += 1

            # for url in list_url:
            #   emb = discord.Embed(title=f"Ось шо знайшлось, #{list_url.index(url)+1}:", color=discord.Color.random())
            #   emb.url = url
            #   await ctx.send(embed=emb)

        except TimeoutError:
            return await ctx.send('Дуже довго думаеш, спробуй ще раз')


async def setup(client):
    await client.add_cog(ChatCommands(client))
