# secret commands for developers

import discord
from discord.ext import commands
from config import settings
import asyncio
import os

PREFIX = settings["PREFIX"]


class SecretCommands(commands.Cog):

    def __init__(self, client):
      self.client = client

    # kick участников (через упоминание)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.id == 860064253964845116 or ctx.author.id == 487274088805564417:
            await member.kick(reason=reason)
            await ctx.author.send(embed=discord.Embed(
              title=f"Кікнув {member.mention}", color=discord.Color.orange()))
        await ctx.channel.purge(limit=1)

    # ban участников (через упоминание)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, time: int):
      if ctx.author.id == 860064253964845116 or ctx.author.id == 487274088805564417:

        await member.send(f'Тебе забанили на сервері {ctx.guild.name}')
        await ctx.author.send(embed=discord.Embed(
          title=f"Забанив {member.mention}", color=discord.Color.orange()))

        if time:
          try:
            seconds = int(time) * 60
            await member.ban()
            await asyncio.sleep(seconds)
            await member.unban()

            await ctx.send(f'*У {member.mention} занічився бан*')
            link = await ctx.channel.create_invite(max_age=300)
            await member.send(f"Заходь в сім'ю {ctx.guild.name}! {link}")
          except Exception as ex:
            print(ex)
            await ctx.send("time указувати в хв")
        else:
          await member.ban()

    @commands.command()
    async def add(self, ctx, name: str):
      if ctx.author.id == 860064253964845116 or ctx.author.id == 487274088805564417:
        if name:
          is_txt = False
          for i in os.listdir():
            if i == "roles.txt":
              is_txt = True
          if not is_txt:
            with open("roles.txt", "w") as file:
              file.write(name + '\n')
          else:
            with open("roles.txt", "a") as file:
              file.write(name + '\n')
            await ctx.author.send(embed=discord.Embed(
              title=f"Добавив роль {name}", color=discord.Color.green()))
        else:
          await ctx.author.send(
            embed=discord.Embed(title="Я поламався",
                                description="Вкажи назву ролі",
                                color=discord.Color.red()))
      await ctx.channel.purge(limit=1)

    @commands.command()
    async def delete(self, ctx, name: str):
      if ctx.author.id == 860064253964845116 or ctx.author.id == 487274088805564417:
        if name:
          is_txt = False
          for i in os.listdir():
            if i == "roles.txt":
              is_txt = True
          if is_txt:
            with open("roles.txt", "r") as file:
              roles = list(file.read().split('\n')[:-1])
            if name in roles:
              roles.remove(name)
              print(roles)
              with open("roles.txt", "w") as file:
                for i in roles:
                  file.write(i + '\n')
              await ctx.author.send(embed=discord.Embed(
                title=f"Видалив роль {name}", color=discord.Color.green()))
            else:
              await ctx.author.send(
                embed=discord.Embed(title="Я поламався",
                                    description="Нема такої ролі",
                                    color=discord.Color.red()))
          else:
            await ctx.author.send(
              embed=discord.Embed(title="Я поламався",
                                  description="Вкажи назву ролі",
                                  color=discord.Color.red()))
      await ctx.channel.purge(limit=1)

    @commands.command()
    async def view(self, ctx):
      if ctx.author.id == 860064253964845116 or ctx.author.id == 487274088805564417:
        with open("roles.txt", "r") as file:
          roles = list(file.read().split('\n')[:-1])
        for i in roles:
          embed = discord.Embed(color=discord.Color.random()).add_field(
            name=i, value="-" * 10, inline=False)
          await ctx.author.send(embed=embed)
        await ctx.channel.purge(limit=1)

    @commands.command(aliases=["help+"])
    async def secret_help(self, ctx):
      if ctx.author.id == 860064253964845116 or ctx.author.id == 487274088805564417:
        embed = discord.Embed(title="Секретні команди",
                              color=discord.Color.random())
        embed.add_field(name=f"{PREFIX}kick", value="пу-пу-пу", inline=False)
        embed.add_field(name=f"{PREFIX}ban", value="пу-пу-пу", inline=False),
        embed.add_field(name=f"{PREFIX}get+ <@user> <role_name>",
                        value="добавити права на сервері",
                        inline=False),
        embed.add_field(name=f"{PREFIX}add",
                        value="добавити роль для сюрпризу",
                        inline=False)
        embed.add_field(name=f"{PREFIX}delete",
                        value="видалити роль для сюрпризу",
                        inline=False)
        embed.add_field(name=f"{PREFIX}view",
                        value="список ролей в сюрпризі",
                        inline=False)
        await ctx.author.send(embed=embed)
      await ctx.channel.purge(limit=1)


async def setup(client):
  await client.add_cog(SecretCommands(client))
