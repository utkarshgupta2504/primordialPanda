# -*- coding: utf-8 -*-

from discord.ext import commands, tasks
import discord
import datetime


class TimedTasks(commands.Cog):
    """The description for TimedTasks goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer.start()

    @tasks.loop(minutes=4)
    async def timer(self):
        utcPlus12 = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        await self.bot.get_channel(926802636685082654).edit(
            name=utcPlus12.strftime("%#I:%M %p on %a %b %#d")
        )

    @timer.before_loop
    async def before_timer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TimedTasks(bot))
