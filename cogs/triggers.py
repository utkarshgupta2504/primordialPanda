# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import app_commands
import discord

from utils.constants import MY_GUILD


class Triggers(commands.Cog):
    """The description for Triggers goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @app_commands.guild_only()
    async def flowers(self, ctx):
        '''
        Makes a flower line,
        Can be used as an ending
        '''
        await ctx.send("<a:flowers:1100188266201882736>" * 16)
        await ctx.message.delete()

    @commands.hybrid_command()
    @app_commands.guild_only()
    async def catline(self, ctx):
        await ctx.send(
            "<:catLine1:1100188277421649990>"
            + "<:catLine2:1100188286531666063>" * 10
            + "<:catLine3:1100188296514113658>"
        )
        await ctx.message.delete()

    @commands.hybrid_command()
    @app_commands.guild_only()
    async def line(self, ctx):
        await ctx.send("<a:rainbowLine:1100188252515860611>" * 16)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Triggers(bot))
