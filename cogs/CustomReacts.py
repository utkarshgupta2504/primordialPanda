# -*- coding: utf-8 -*-

from typing import Union
from discord.ext import commands
import discord
import json
import emoji
from constants import isTesting

from discord.utils import get


class CustomReacts(commands.Cog):
    """The description for CustomReacts goes here."""

    def __init__(self, bot):
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

    @commands.command(name="addCustomReact")
    @commands.has_any_role(
        "Shrine Priestess", "Red Panda Priest", "Ninja Cat", "Utkarsh"
    )
    async def addCustomReact(
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
            reactString = str(react).replace("<a:", "<:")

        self.customReacts[trigger] = reactString

        with open("database/customReacts.json", "w") as f:
            json.dump(self.customReacts, f, indent=2)

        await ctx.reply("Successfully added custom react!")

    @commands.command(name="removeCustomReact")
    @commands.has_any_role(
        "Shrine Priestess", "Red Panda Priest", "Ninja Cat", "Utkarsh"
    )
    async def removeCustomReact(self, ctx: commands.Context, trigger: str = None):

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


def setup(bot):
    bot.add_cog(CustomReacts(bot))
