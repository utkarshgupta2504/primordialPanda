# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import app_commands
import discord

from constants import MY_GUILD


class Triggers(commands.Cog):
    """The description for Triggers goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def flowers(self, ctx):
        '''
        Makes a flower line,
        Can be used as an ending
        '''
        await ctx.send("<a:flowers:922167600438444112>" * 16)
        await ctx.message.delete()

    @commands.command()
    async def catline(self, ctx):
        await ctx.send(
            "<:catLine1:922141508029804564>"
            + "<:catLine2:922141539289935872>" * 4
            + "<:catLine3:922141563075833887>"
        )
        await ctx.message.delete()

    @commands.command()
    async def line(self, ctx):
        await ctx.send("<a:rainbowLine:922163822549168148>" * 16)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Triggers(bot))
