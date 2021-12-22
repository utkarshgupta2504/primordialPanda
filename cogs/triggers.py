# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Triggers(commands.Cog):
    """The description for Triggers goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flowers(self, ctx):
        await ctx.send("<a:flowers:922167600438444112>" * 21)
        await ctx.message.delete()

    @commands.command()
    async def catline(self, ctx):
        await ctx.send(
            "<:catLine1:922141508029804564>"
            + "<:catLine2:922141539289935872>" * 19
            + "<:catLine3:922141563075833887>"
        )
        await ctx.message.delete()

    @commands.command()
    async def line(self, ctx):
        await ctx.send("<a:rainbowLine:922163822549168148>" * 21)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Triggers(bot))
