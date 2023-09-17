# commands or functions for roles and personal messages
import discord
import time
import asyncio
from config import settings
from discord.ext import commands


class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="kick_members"),
            discord.SelectOption(label="ban_members"),
            discord.SelectOption(label="manage_channels"),
            discord.SelectOption(label="manage_guild"),
            discord.SelectOption(label="administrator"),
            discord.SelectOption(label="manage_roles")
        ]

        super().__init__(placeholder="Select rights:", min_values=1, max_values=6, options=options,
                         custom_id="list_permissions")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{self.values}")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


class RolesMessagesCommands(commands.Cog):
    PREFIX = settings["PREFIX"]

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def create_role(self, ctx, name, color=None):
        print(name, color)
        if color is None:
            await ctx.guild.create_role(name=name, color=discord.Color.random())
            emb = discord.Embed(title="The role is done",
                                color=discord.Color.green())
            await ctx.send(embed=emb)
        elif not str(color).startswith('#') or name is None:
            emb = discord.Embed(title="I broke down",
                                description=f"You must specify the name of the role without spaces and the color"
                                            f"\nExample:"
                                            f"{self.PREFIX}create_role test #428af5",
                                color=discord.Color.red())
            emb.url = 'https://www.google.com/search?q=google+%D0%BF%D0%B0%D0%BB%D0%B8%D1%82%D1%80%D0%B0&sxsrf=ALiCzsbE-BjOJkn1B4Ep1sOflkoEkfxDrg%3A1672010892134&ei=jNyoY6DjB6PLrgS6obrgCw&oq=google+%D0%BF%D0%B0%D0%BB&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMggIABCABBCxAzIICAAQFhAeEAoyCAgAEBYQHhAKMggIABAWEB4QDzIICAAQFhAeEA8yCAgAEBYQHhAPMggIABAWEB4QDzIICAAQFhAeEA8yCAgAEBYQHhAPMggIABAWEB4QCjoECCMQJzoLCAAQgAQQsQMQgwE6EAguELEDEIMBEMcBENEDEEM6DgguEIAEELEDEMcBENEDOgUIABCABDoHCAAQsQMQQzoKCAAQsQMQgwEQQzoECAAQQzoICAAQgAQQywFKBAhBGABKBAhGGABQAFiRGGDwKWgAcAF4AIABbogBygeSAQM3LjOYAQCgAQHAAQE&sclient=gws-wiz-serp'
            await ctx.send(embed=emb)
        else:
            try:
                await ctx.guild.create_role(name=name, color=discord.Color.from_str(str(color)))
                emb = discord.Embed(title='Роль зроблено',
                                    color=discord.Color.green())
                await ctx.send(embed=emb)
            except:
                await ctx.send("Неправильно вказаний колір")

    @commands.command()
    async def get_role(self, ctx, member: discord.Member, name):
        try:
            if name != "mute":
                role = discord.utils.get(ctx.message.guild.roles, name=name)
                await member.add_roles(role)
                emb = discord.Embed(title="The role has been issued",
                                    description=f"{member.mention}",
                                    color=discord.Color.green())
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title="I broke down",
                                    description="You can't do that",
                                    color=discord.Color.red())
                await ctx.send(embed=emb)
        except Exception as ex:
            emb = discord.Embed(title="I broke down",
                                description="Such a role does not exist",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete_roles(self, ctx, count: int):
        if count != 0:
            stop_count = 0
            for role in ctx.message.guild.roles:
                if stop_count <= count:
                    try:
                        await ctx.send(f"Deleted {role}")
                        await role.delete()
                        stop_count += 1
                    except Exception as ex:
                        print(ex)
                else:
                    break
        else:
            for role in ctx.message.guild.roles:
                try:
                    print(f"Deleted {role}")
                    await role.delete()
                except:
                    continue

    @commands.command()
    async def del_role(self, ctx, member: discord.Member, name):
        await ctx.channel.purge(limit=1)
        roles = discord.utils.get(ctx.message.guild.roles, name=name)
        if roles and name != "mute":
            await member.remove_roles(roles)
            emb = discord.Embed(title="The role has been deleted",
                                color=discord.Color.green())
            await ctx.send(embed=emb)
        elif name == "mute":
            emb = discord.Embed(title="I broke down",
                                description="You can't do that",
                                color=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="Я поламався",
                                description=f"{name} such a role does not exist",
                                color=discord.Color.red())
            await ctx.send(embed=emb)

    @commands.command()
    async def send(self, ctx, member: discord.Member):
        await ctx.send("Write a message:")

        def check(m):
            return m.author.id == ctx.author.id

        try:
            message = await self.client.wait_for("message", check=check, timeout=120)
            emb1 = discord.Embed(title="The message has been sent",
                                 color=discord.Color.green())
            await ctx.send(embed=emb1)
            await member.send(f'{member.name}, {message.content}, from {ctx.author.name}')
        except TimeoutError:
            return await ctx.send("Think too long, try again")

    @commands.command()
    async def timer(self, ctx, time):
        emb1 = discord.Embed(title="Time has passed",
                             description=f"The timer is set to {time} minutes",
                             color=discord.Color.green())
        emb2 = discord.Embed(title="Time is up",
                             color=discord.Color.red())
        await ctx.author.send(embed=emb1)
        await asyncio.sleep(float(time) * 60)
        await ctx.author.send(embed=emb2)

    @commands.command(aliases=["spam", "mention"])
    async def spam_mention(self, ctx, member: discord.Member, count: str):
        await ctx.channel.purge(limit=1)
        if int(count) > 100:
            emb1 = discord.Embed(title="I broke down",
                                 description=f"{count} - that's a lot",
                                 color=discord.Color.red())
            await ctx.send(embed=emb1)
        else:
            for _ in range(int(count)):
                await ctx.send(member.mention)

    @commands.command(aliases=["get+"])
    @commands.has_permissions(administrator=True)
    async def get_role_plus(self, ctx, member: discord.Member, name=None):
        if name is not None:
            try:
                permissions = discord.Permissions()
                await ctx.send(view=DropdownView())

                def check(msg):
                    return msg.author.id == 1055963371868004382

                list_permissions = await self.client.wait_for("message", check=check, timeout=60)
                list_permissions = [i.strip() for i in
                                    list_permissions.content.replace("'", " ").replace("[", " ").replace("]",
                                                                                                         " ").split(
                                        ',')]
                print(list_permissions)
                for i in list_permissions:
                    if i == "kick_members":
                        permissions.update(kick_members=True)
                    if i == "ban_members":
                        permissions.update(ban_members=True)
                    if i == "manage_channels":
                        permissions.update(manage_channels=True)
                    if i == "manage_guild":
                        permissions.update(manage_guild=True)
                    if i == "administrator":
                        permissions.update(administrator=True)
                    if i == "manage_roles":
                        permissions.update(manage_roles=True)

                await ctx.guild.create_role(name=name, color=discord.Color.random(), permissions=permissions)
                role = discord.utils.get(ctx.message.guild.roles, name=name)
                await member.add_roles(role)

                emb = discord.Embed(title="The role is done", color=discord.Color.green())
                await ctx.send(embed=emb)
                time.sleep(1)
                await ctx.channel.purge(limit=4)
            except:
                emb = discord.Embed(title="I broke down",
                                    description="You're thinking too long, try again", color=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="I broke down",
                                description=f"You must specify the name of the role without spaces\nПриклад: "
                                            f"{self.PREFIX}get+ <@mention> test", color=discord.Color.red())
            await ctx.send(embed=emb)


async def setup(client):
    await client.add_cog(RolesMessagesCommands(client))
