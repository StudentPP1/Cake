# secret commands for developers
import sqlite3
import discord
from discord.ext import commands
from config import settings
import asyncio

PREFIX = settings["PREFIX"]


class SecretCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.author.send(embed=discord.Embed(title=f"Kicked {member.mention}", color=discord.Color.orange()))
        await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, time: int):
        await member.send(f"You have been banned from the server {ctx.guild.name}")
        await ctx.author.send(embed=discord.Embed(title=f"Banned {member.mention}", color=discord.Color.orange()))

        if time:
          try:
            seconds = int(time) * 60
            await member.ban()
            await asyncio.sleep(seconds)
            await member.unban()

            await ctx.send(f"*{member.mention}: ban expired*")
            link = await ctx.channel.create_invite(max_age=300)
            await member.send(f"Enter the family {ctx.guild.name}! {link}")
          except Exception as ex:
            print(ex)
            await ctx.send("Specify time in minutes")
        else:
          await member.ban()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, name: str):
        if name:
            with sqlite3.connect("roles.db") as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS roles (
                        guild_id INTEGER NOT NULL,
                        role TEXT NOT NULL)""")
                roles = list(
                    i[0] for i in cur.execute(f"""SELECT role FROM roles WHERE guild_id == '{ctx.guild.id}';"""))
                if len(roles) >= 250:
                    await ctx.author.send(
                        embed=discord.Embed(title="I broke down", description="Role limit reached",
                                            color=discord.Color.red()))
                if name not in roles:
                    cur.execute("INSERT INTO roles VALUES (?, ?)", (ctx.guild.id, name))
                    await ctx.author.send(embed=discord.Embed(title=f"Added a role {name}",
                                                              color=discord.Color.green()))
                else:
                    await ctx.author.send(
                        embed=discord.Embed(title="I broke down", description="Enter a unique new role",
                                            color=discord.Color.red()))
        else:
            await ctx.author.send(embed=discord.Embed(title="I broke down", description="Enter the name of the role",
                                                      color=discord.Color.red()))

        await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, name: str):
        if name:
            with sqlite3.connect("roles.db") as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS roles (
                        guild_id INTEGER NOT NULL,
                        role TEXT NOT NULL)""")
                roles = list(
                    i[0] for i in cur.execute(f"""SELECT role FROM roles WHERE guild_id == '{ctx.guild.id}';"""))

                if name in roles:
                    cur.execute(f"DELETE FROM roles WHERE guild_id == '{ctx.guild.id}' AND role == {name}")
                    await ctx.author.send(embed=discord.Embed(title=f"Deleted a role {name}",
                                                              color=discord.Color.green()))
                else:
                    await ctx.author.send(
                        embed=discord.Embed(title="I broke down", description="There isn't current role",
                                            color=discord.Color.red()))
        else:
            await ctx.author.send(embed=discord.Embed(title="I broke down", description="Enter the name of the role",
                                                      color=discord.Color.red()))

        await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def view(self, ctx):
        with sqlite3.connect("roles.db") as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS roles (
                    guild_id INTEGER NOT NULL,
                    role TEXT NOT NULL)""")
            roles = list(
                i[0] for i in cur.execute(f"""SELECT role FROM roles WHERE guild_id == '{ctx.guild.id}';"""))

        embed = discord.Embed(color=discord.Color.random())
        for i in roles:
            print(i)
            embed.add_field(name=i, value="--------------", inline=False)

        await ctx.author.send(embed=embed)
        await ctx.channel.purge(limit=1)

    @commands.command(aliases=["help+"])
    @commands.has_permissions(administrator=True)
    async def secret_help(self, ctx):
        embed = discord.Embed(title="Secret commands",
                              color=discord.Color.random())
        embed.add_field(name=f"{PREFIX}kick", value="kick member", inline=False)
        embed.add_field(name=f"{PREFIX}ban", value="ban member", inline=False),
        embed.add_field(name=f"{PREFIX}get+ <@user> <role_name>",
                        value="add rights to the person on the server",
                        inline=False),
        embed.add_field(name=f"{PREFIX}add",
                        value="add role for the surprise function",
                        inline=False)
        embed.add_field(name=f"{PREFIX}delete",
                        value="delete role for the surprise function",
                        inline=False)
        embed.add_field(name=f"{PREFIX}view",
                        value="list of roles in the surprise function",
                        inline=False)
        await ctx.author.send(embed=embed)
        await ctx.channel.purge(limit=1)


async def setup(client):
    await client.add_cog(SecretCommands(client))
