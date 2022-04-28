# -*- coding: utf-8 -*-

import json
import os
from discord.ext import commands
import discord

from constants import isTesting


class Highlights(commands.Cog):
    """Manage Highlights"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.isInitialised = False
        self.highlights = {}

    @commands.Cog.listener()
    async def on_ready(self):

        if not os.path.isfile("database/highlights.json"):
            with open("database/highlights.json", "w") as f:
                f.write("{}")

        with open("database/highlights.json", "r") as f:
            self.highlights = json.load(f)

            self.isInitialised = True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        if isTesting and message.channel.id != 912387794821861396:
            return

        if not isTesting and message.channel.id == 912387794821861396:
            return

        for id, triggers in self.highlights.items():

            if id == str(message.author.id):
                continue

            for trigger in triggers:
                if trigger.lower() in message.content.lower():
                    await self.bot.get_user(int(id)).send(f"You have been mentioned with keyword **{trigger}** in channel <#{message.channel.id}>\nLink: {message.jump_url}")
                    break

    @commands.group(name="highlight", aliases=["hl"], case_insensitive=True, invoke_without_command=False)
    async def highlight(self, ctx: commands.Context):

        pass

    @highlight.command(name="add")
    async def addHighlight(self, ctx: commands.Context, trigger: str):

        if str(ctx.author.id) not in self.highlights:
            self.highlights[str(ctx.author.id)] = []

        self.highlights[str(ctx.author.id)].append(trigger)

        with open("database/highlights.json", "w") as f:
            json.dump(self.highlights, f, indent=2)

        await ctx.reply("Highlight added successfully")

    @highlight.command(name="list", aliases=["show"])
    async def listHighlights(self, ctx: commands.Context):

        if str(ctx.author.id) not in self.highlights:
            await ctx.reply("You have no highlights set! Use `?hl add <trigger>` to add highlights")
            return

        await ctx.reply("Your Highlights:\n>>> " + "\n".join(self.highlights[str(ctx.author.id)]))

    @highlight.command(name="remove", aliases=["rem", "delete", "del"])
    async def removeHighlight(self, ctx: commands.Context, trigger: str):

        if trigger not in self.highlights[str(ctx.author.id)]:
            await ctx.reply("No such highlight")
            return

        self.highlights[str(ctx.author.id)].remove(trigger)

        with open("database/highlights.json", "w") as f:
            json.dump(self.highlights, f, indent=2)

        await ctx.reply("Highlight removed successfully")


async def setup(bot):
    await bot.add_cog(Highlights(bot))
