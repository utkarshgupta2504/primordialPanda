# -*- coding: utf-8 -*-

from discord.ext import commands, tasks
from discord.utils import get
import discord
import datetime
import json
import os
import io

from constants import *


class TimedTasks(commands.Cog):
    """The description for TimedTasks goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer.start()
        self.backupTimer.start()

    @tasks.loop(minutes=5)
    async def timer(self):
        utcPlus12 = datetime.datetime.utcnow() + datetime.timedelta(hours=12)

        if not isTesting:
            try:
                await self.bot.get_channel(926802636685082654).edit(
                    name=utcPlus12.strftime("%#I:%M %p on %a %b %#d")
                )

            except Exception as e:

                print(e)

            for i in pathLevelRoles:

                await self.bot.get_channel(927615922921938944).edit(
                    name=f"{i}s: {len(get(self.bot.get_guild(911016512574341140).roles, id=pathLevelRoles[i][0]).members)}"
                )

    @timer.before_loop
    async def before_timer(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=12)
    async def backupTimer(self):

        if not isTesting:
            await self.bot.get_channel(927305899171803176).purge()

            for i in next(os.walk(os.getcwd() + "/database"), (None, None, []))[2]:

                with open(f"database/{i}", "r") as f:

                    tempStringIO = io.StringIO()
                    json.dump(json.load(f), tempStringIO, indent=2)

                    tempStringIO.seek(0)

                    fileToSend = discord.File(tempStringIO, filename=i)

                    await self.bot.get_channel(927305899171803176).send(file=fileToSend)

    @backupTimer.before_loop
    async def beforeBackupTimer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TimedTasks(bot))
