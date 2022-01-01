# -*- coding: utf-8 -*-

from typing import Union
from discord.ext import commands
import discord
import json
import emoji
from constants import isTesting

from discord.utils import get


class CustomPerks(commands.Cog):
    """The description for CustomPerks goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.customReacts = {}
        self.isInitialised = False

    @commands.Cog.listener()
    async def on_ready(self):
        with open("database/customReacts.json", "r") as f:
            self.customReacts = json.load(f)

            self.isInitialised = True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if not self.isInitialised:
            print("Custom Reacts not initialised")
            return

        if (isTesting and message.channel.id != 912387794821861396) or (
            not isTesting and message.channel.id == 912387794821861396
        ):
            return

        for react in self.customReacts:

            if react in message.content.lower():
                await message.add_reaction(self.customReacts[react])

    @commands.group(
        name="customReact", case_insensitive=True, invoke_without_command=True
    )
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def customReact(self, ctx):
        await ctx.send(str(self.customReacts))

    @customReact.command(name="add")
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def add(
        self,
        ctx: commands.Context,
        trigger: str = None,
        react: Union[discord.Emoji, str] = None,
    ):

        if trigger is None:
            await ctx.reply("Need a trigger!")
            return

        if react is None:
            await ctx.reply("Need an emote to react!")
            return

        reactString = ""

        if type(react) == str:
            emojiList = emoji.emoji_lis(react)

            if len(emojiList) == 0 or emojiList[0]["location"] != 0:
                await ctx.reply("Need an emote to react!")
                return

            else:
                reactString = emojiList[0]["emoji"]

        else:
            reactString = str(react)

        self.customReacts[trigger] = reactString

        with open("database/customReacts.json", "w") as f:
            json.dump(self.customReacts, f, indent=2)

        await ctx.reply("Successfully added custom react!")

    @customReact.command(name="remove", aliases=["rem", "delete", "del"])
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def remove(self, ctx: commands.Context, trigger: str = None):

        if trigger is None:
            await ctx.reply("Need a trigger!")
            return

        if trigger in self.customReacts:
            self.customReacts.pop(trigger)

        else:
            await ctx.reply("No such trigger!")
            return

        with open("database/customReacts.json", "w") as f:
            json.dump(self.customReacts, f, indent=2)

        await ctx.reply("Successfully removed custom react!")

    @commands.group(name="customChannel", case_insensitive=True)
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def customChannel(self, ctx: commands.Context):

        pass

    @customChannel.command(name="create", aliases=["add", "cr", "make"])
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def createCustomChannel(
        self, ctx: commands.Context, name: str = None, user: discord.User = None
    ):

        if name is None:
            await ctx.reply("Need a channel name!")
            return

        if user is None:
            await ctx.reply("Need a user to provide admin perms to!")
            return

        sentMessage: discord.Message = await ctx.send("Creating custom channel")

        spamCategory: discord.CategoryChannel = get(
            ctx.guild.categories, id=911024015693479967
        )

        createdChannel: discord.TextChannel = await spamCategory.create_text_channel(
            name
        )

        perms: discord.PermissionOverwrite = createdChannel.overwrites_for(user)
        perms.manage_messages = True
        perms.manage_channels = True

        await createdChannel.set_permissions(user, overwrite=perms)

        await sentMessage.edit(content="Channel created successfully!")


def setup(bot):
    bot.add_cog(CustomPerks(bot))
