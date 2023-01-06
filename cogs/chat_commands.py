# public functions for chat of guild

from selenium import webdriver
from selenium.webdriver.common.by import By
from Cybernator import Paginator
from random import shuffle
import json
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import img2pdf
from pytube import YouTube
import discord
import requests
import sqlite3
import datetime
import random
import string
import sqlite3
import os
import lxml
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
from discord.ext import commands
from config import settings
import time

list_tags = None
PREFIX = settings["PREFIX"]
headers = {"User-Agent": f"{UserAgent().random}"}
url_head = "https://hentaichan.live"
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={UserAgent().random}")
options.headless = True
driver = webdriver.Chrome(
    executable_path="D:\Projects\Python\chromedriver.exe",
    options=options)


class ChatCommands(commands.Cog):
    jokes = None

    def __init__(self, client):
        self.client = client

    # скачать видео
    @commands.command()
    async def find(self, ctx, *, arg):
        await ctx.send("Loading...")
        if 'https://www.youtube.com/watch?' in arg:
            link = arg
            try:
                yt = YouTube(link)
                print(yt.streams.filter(file_extension='mp4'))
                stream = yt.streams.get_by_itag(22)
                name = str(stream.title)
                try:
                    stream.download("D:\\", filename=f'{name}.mp4')
                except Exception as ex:
                    print(ex)
                    name = "видео"
                    stream.download("D:\\", filename=f'{name}.mp4')
                print("done")
                while True:
                    try:
                        await ctx.send(file=discord.File(fp=f'D:\\{name}.mp4'))
                        time.sleep(1)
                        os.remove(f'D:\\{name}.mp4')
                        break
                    except Exception as ex:
                        continue
            except Exception as ex:
                print(ex)
                await ctx.send("Помилка скачування")
        else:
            await ctx.send("Введи посилання на відео з ютубу!")

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

    # теги
    @commands.command()
    async def tags(self, ctx):
        global list_tags

        if list_tags is None:
            with open("tags.txt", "r", encoding='utf-8') as f:
                list_tags = f.readlines()
            list_tags = [i.replace('\n', '') for i in list_tags]

        await ctx.send("Доступні теги:")
        block_tags = [list_tags[i:i + 25] for i in range(0, 200, 25)]

        for i in block_tags:
            embed = discord.Embed()
            for j in i:
                embed.add_field(name=f"{j}", value="-" * 10)
            await ctx.send("Доступні теги:", embed=embed)

    # найти по тегам
    @commands.command(aliases=["find-tags"])
    async def find_tags(self, ctx):
        global list_tags
        await ctx.send('Напиши шукані теги: ')
        if list_tags is None:
            with open("tags.txt", "r", encoding='utf-8') as f:
                list_tags = f.readlines()
            list_tags = [i.replace('\n', '') for i in list_tags]

        def check(m):
            return m.author.id == ctx.author.id

        try:
            # Ожидание ответа от пользователя. timeout - время ожидания.
            answer = await self.client.wait_for("message", check=check, timeout=30)
            answer = answer.content
            print(answer)
        except TimeoutError:
            return await ctx.send('Дуже довго думаеш, спробуй ще раз')

        if ' ' in answer:
            user_tags = answer.split()
        else:
            user_tags = answer

        ready_tags = []
        ready = False
        for i in list_tags:
            if ' ' in i:
                tag = i.split()
                for j in tag:
                    if (j in user_tags or j == user_tags) and len(j) != 1:
                        ready = True
                        ready_tags.append(i)
            else:
                if i in user_tags or i == user_tags and len(i) != 1:
                    ready = True
                    ready_tags.append(i)

        if ready:
            titles = []

            print(ready_tags)
            await ctx.send('Пошук...')

            with open("hentai.json", "r", encoding="utf-8") as f:
                for i in json.load(f):
                    json_tags = ''
                    for k in i['tags']:
                        json_tags += k + ' '
                    if ready_tags in json_tags[:-1].replace('_', ' ').split():
                        titles.append([i['name'], i['url']])
                    else:
                        for user_tag in ready_tags:
                            if user_tag in json_tags[:-1].replace('_', ' ').split():
                                titles.append([i['name'], i['url']])
            if titles is []:
                await ctx.send('По твоїм тегам нічого не знайшов, спробуй інші')
            else:
                shuffle(titles)
                titles = titles[:11]
                titles_dict = {}

                for i in range(len(titles)):
                    val = re.sub("[-+=.]", "", titles[i][0])
                    if len(val) >= 100:
                        val = val[:len(val) - 100]
                    titles_dict[val] = titles[i][1]
                print(titles_dict.keys())

                class Dropdown(discord.ui.Select):
                    def __init__(self):
                        options = [discord.SelectOption(label=i) for i in titles_dict.keys()]
                        super().__init__(placeholder="Вибери хентай", options=options)

                    async def callback(self, inter: discord.Message):
                        print(self.values[0])
                        url = titles_dict[self.values[0]]
                        print(url)

                        def request_page(name_url, retry_page=5):
                            try:
                                read = requests.get(url=name_url, headers=headers)
                                soup = BeautifulSoup(read.text, "lxml")
                                read_url = soup.find_all("p", class_="extra_off")[-1].find('a').get("href")
                                read_url = url_head + read_url
                                return read_url
                            except Exception as ex:
                                time.sleep(0.5)
                                if retry_page:
                                    print(f"[INFO] retry={retry_page} => {name_url}")
                                    return request_page(name_url, retry_page=(retry_page - 1))
                                else:
                                    return None

                        def request_images(url, retry_page=5):
                            try:
                                print("Loading...")
                                driver.get(url)
                                img = driver.find_element(By.XPATH, '//*[@id="image"]/a/img').get_attribute("src")
                                return img
                            except Exception as ex:
                                time.sleep(0.5)
                                if retry_page:
                                    print(f"[INFO] retry={retry_page} => {url}")
                                    return request_images(url, retry_page=(retry_page - 1))
                                else:
                                    return None

                        await ctx.send("Підключення до сайту...")
                        url_page = request_page(url)
                        if url_page is None:
                            await ctx.send("Помилка підключення до сайту, спробуй знову")
                        else:
                            url_list = []
                            for page in range(1, 41):
                                url_list.append(url_page + f"#page={page}")
                            await ctx.send("Збирання зображень...")
                            img_list = []
                            for i in url_list:
                                if url_list.index(i) % 10 == 0:
                                    await ctx.send("Загрузка зображень...")
                                img = request_images(i)
                                if img is None:
                                    print(False)
                                    continue
                                else:
                                    print(True)
                                    img_list.append(img)
                            img_list = sorted(set(img_list))
                            driver.quit()

                            print(img_list)
                            main_embed = discord.Embed(title=f"{self.values[0]}",
                                                       description=f"Теги: {' '.join(ready_tags)}",
                                                       color=discord.Color.random())
                            main_embed.url = url
                            await ctx.send(embed=main_embed)

                            images_content = [requests.get(url=i, headers=headers).content for i in img_list]
                            img_list = []
                            for i in range(len(images_content)):
                                with open(f"{i}.jpg", "wb") as file:
                                    file.write(images_content[i])
                                    img_list.append(f"{i}.jpg")

                            print(img_list)
                            for i in img_list:
                                await ctx.send(file=discord.File(fp=i))
                            for i in img_list:
                                os.remove(i)

                class DropdownView(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.add_item(Dropdown())

                await ctx.send(view=DropdownView())
        else:
            await ctx.send(f'Не знайдено жодного тега, спробуй {PREFIX}tags')


async def setup(client):
    await client.add_cog(ChatCommands(client))
