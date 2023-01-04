# commands or functions for roles and personal messages

import discord
import random
import string
import asyncio
from config import settings
from discord.ext import commands


class RolesMessagesCommands(commands.Cog):
    PREFIX = settings["PREFIX"]

    def __init__(self, client):
        self.client = client

    # создание ролей
    @commands.command()
    async def create_role(self, ctx, name, color=None):
        if color is None:
            letters = string.ascii_lowercase.split()
            nums = [str(i) for i in range(10)]
            random_color_list = letters + nums
            color = '#'
            for _ in range(6):
                color += random.choice(random_color_list)
            await ctx.guild.create_role(name=name, color=discord.Color.from_str(str(color)))
            emb = discord.Embed(title='Роль зроблено',
                                color=discord.Color.green())
            await ctx.send(embed=emb)
        elif not str(color).startswith('#') or name is None:
            emb = discord.Embed(title="Я поламався",
                                description=f"Треба указувати назву ролі без пробілів та колір\nПриклад: "
                                            f"{self.PREFIX}create_role test #428af5",
                                color=discord.Color.red())
            emb.url = 'https://www.google.com/search?q=google+%D0%BF%D0%B0%D0%BB%D0%B8%D1%82%D1%80%D0%B0&sxsrf=ALiCzsbE-BjOJkn1B4Ep1sOflkoEkfxDrg%3A1672010892134&ei=jNyoY6DjB6PLrgS6obrgCw&oq=google+%D0%BF%D0%B0%D0%BB&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMggIABCABBCxAzIICAAQFhAeEAoyCAgAEBYQHhAKMggIABAWEB4QDzIICAAQFhAeEA8yCAgAEBYQHhAPMggIABAWEB4QDzIICAAQFhAeEA8yCAgAEBYQHhAPMggIABAWEB4QCjoECCMQJzoLCAAQgAQQsQMQgwE6EAguELEDEIMBEMcBENEDEEM6DgguEIAEELEDEMcBENEDOgUIABCABDoHCAAQsQMQQzoKCAAQsQMQgwEQQzoECAAQQzoICAAQgAQQywFKBAhBGABKBAhGGABQAFiRGGDwKWgAcAF4AIABbogBygeSAQM3LjOYAQCgAQHAAQE&sclient=gws-wiz-serp'
            await ctx.send(embed=emb)
        else:
            await ctx.guild.create_role(name=name, color=discord.Color.from_str(str(color)))
            emb = discord.Embed(title='Роль зроблено',
                                color=discord.Color.green())
            await ctx.send(embed=emb)

    # выдача ролей (через упоминание)
    @commands.command()
    async def get_role(self, ctx, member: discord.Member, name):
        try:
            if name != "mute":
                role = discord.utils.get(ctx.message.guild.roles, name=name)
                await member.add_roles(role)
                emb = discord.Embed(title="Роль видано",
                                    description=f"{member.mention}",
                                    color=discord.Color.green())
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title="Я поламався",
                                    description="Неможна так робити",
                                    color=discord.Color.red())
                await ctx.send(embed=emb)
        except Exception as ex:
            emb = discord.Embed(title="Я поламався",
                                description="Такої ролі не існує",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    # удаление ролей участникам (через упоминание)
    @commands.command()
    async def del_role(self, ctx, member: discord.Member, name):
        await ctx.channel.purge(limit=1)
        roles = discord.utils.get(ctx.message.guild.roles, name=name)
        if roles and name != "mute":
            await member.remove_roles(roles)
            emb = discord.Embed(title="Роль видалено",
                                color=discord.Color.green())
            await ctx.send(embed=emb)
        elif name == "mute":
            emb = discord.Embed(title="Я поламався",
                                description="Неможна так робити",
                                color=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="Я поламався",
                                description=f" {name} такої ролі не існує",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    # отправка личных сообщений участникам
    @commands.command()
    async def send(self, ctx, member: discord.Member, message):
        await ctx.channel.purge(limit=1)
        emb1 = discord.Embed(title="Повідомлення відіслано",
                             color=discord.Color.green())
        await ctx.send(embed=emb1)
        await member.send(f'{member.name}, {message}, from {ctx.author.name}')

    # напоминания
    @commands.command()
    async def timer(self, ctx, time):
        emb1 = discord.Embed(title="Час пішов",
                             description=f"Таймер поставлено на {time} хв",
                             color=discord.Color.green())
        emb2 = discord.Embed(title="Час закінчився",
                             color=discord.Color.red())
        await ctx.author.send(embed=emb1)
        await asyncio.sleep(float(time) * 60)
        await ctx.author.send(embed=emb2)

    # спам (через упоминание)
    @commands.command()
    async def spam(self, ctx, member: discord.Member, message: str, count: str):
        await ctx.channel.purge(limit=1)
        if int(count) > 100:
            emb1 = discord.Embed(title="Я поламався",
                                 description=f"{count} - це дуже багато",
                                 color=discord.Color.red())
            await ctx.send(embed=emb1)
        else:
            for _ in range(int(count)):
                await member.send(str(message))


async def setup(client):
    await client.add_cog(RolesMessagesCommands(client))
