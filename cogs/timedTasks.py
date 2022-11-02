# -*- coding: utf-8 -*-

from mimetypes import init
import time
from discord.ext import commands, tasks
from discord.utils import get
import discord
import datetime
import pytimeparse
import json
import os
import io

from utils.constants import *


class TimedTasks(commands.Cog):
    """The description for TimedTasks goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.isInitialised = False
        self.reminders = {}
        self.timer.start()
        self.backupTimer.start()
        self.reminderLoop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        with open("database/reminders.json", "r") as f:
            self.reminders = json.load(f)

            self.isInitialised = True

    @commands.group(name="reminder", aliases=["remind", "rmd"], case_insensitive=True)
    async def reminder(self, ctx):
        pass

    @reminder.command(name="add")
    async def reminderAdd(self, ctx: commands.Context, duration: str, *reminder_text):

        user = ctx.author.id
        rem = " ".join(reminder_text)

        parsedTime = pytimeparse.parse(duration)

        if not parsedTime:
            await ctx.reply("Invalid time format, use `*w*d*h*m*s`")
            return

        parsedTime = str(int(time.time()) + parsedTime)

        if parsedTime not in self.reminders:
            self.reminders[parsedTime] = []

        self.reminders[parsedTime].append(
            {"reminder": rem, "user": user, "repeat": None, "channel": str(ctx.channel.id)})

        with open("database/reminders.json", "w") as f:

            json.dump(self.reminders, f, indent=2)

        await ctx.reply("Reminder added!")

    @reminder.command(name="repeat", aliases=["rep", "recurring", "recur"])
    async def repeatingReminder(self, ctx, initialDuration, repeatingDuration, *reminder_text):

        user = ctx.author.id
        rem = " ".join(reminder_text)

        parsedTime = pytimeparse.parse(initialDuration)

        if not parsedTime:
            await ctx.reply("Invalid initial time format, use `*w*d*h*m*s`")
            return

        parsedRepeatingTime = pytimeparse.parse(repeatingDuration)

        if not parsedRepeatingTime:
            await ctx.reply("Invalid repeating time format, use `*w*d*h*m*s`")
            return

        parsedTime = str(int(time.time()) + parsedTime)

        if parsedTime not in self.reminders:
            self.reminders[parsedTime] = []

        self.reminders[parsedTime].append(
            {"reminder": rem, "user": user, "repeat": parsedRepeatingTime, "channel": str(ctx.channel.id)})

        with open("database/reminders.json", "w") as f:

            json.dump(self.reminders, f, indent=2)

        await ctx.reply("Repeating Reminder added!")

    @reminder.command(name="delete", aliases=["del", "remove", "rem"])
    async def deleteTimer(self, ctx, *deleteReminder):

        found = False

        for rem in self.reminders:

            for pos, reminder_data in enumerate(self.reminders[rem]):

                if reminder_data["user"] == ctx.author.id and " ".join(deleteReminder) in reminder_data["reminder"]:

                    found = True
                    self.reminders[rem].pop(pos)
                    break

            else:

                continue

            break

        with open("database/reminders.json", "w") as f:

            json.dump(self.reminders, f, indent=2)

        await ctx.reply("Reminder removed!" if found else "No such reminder!")

    @reminder.command(name="list", aliases=["show"])
    async def reminderList(self, ctx):

        id = ctx.author.id

        reminders = []

        for rem in self.reminders:
            for reminder_data in self.reminders[rem]:

                if(reminder_data["user"] == id):
                    reminders.append(reminder_data)

        if len(reminders) > 0:

            await ctx.send("Your reminders\n\n>>> " + "\n".join(map(str, reminders)))

        else:

            await ctx.reply("You have no pending reminders")

    @tasks.loop(seconds=5)
    async def reminderLoop(self):
        if not self.isInitialised:
            return

        currTime = int(time.time())
        remindersToAdd = {}

        for key in self.reminders:

            if int(key) < currTime:

                for reminderData in self.reminders[key]:
                    await self.bot.get_channel(int(reminderData["channel"])).send("<@!" + str(reminderData["user"]) + ">" + " Reminder: " + reminderData["reminder"])

                    if reminderData["repeat"]:
                        updatedTime = str(
                            int(time.time()) + reminderData["repeat"])

                        if updatedTime not in remindersToAdd:
                            remindersToAdd[updatedTime] = []

                        remindersToAdd[updatedTime].append(reminderData)

                self.reminders[key] = []

        self.reminders.update(remindersToAdd)

        self.reminders = {k: v for (k, v) in self.reminders.items() if v}

        with open("database/reminders.json", "w") as f:

            json.dump(self.reminders, f, indent=2)

    @reminderLoop.before_loop
    async def beforeReminder(self):
        await self.bot.wait_until_ready()

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

                await self.bot.get_channel(
                    {
                        "Overseer": 927615922921938944,
                        "Architect": 927615714620244058,
                        "Caregiver": 927615800985133178,
                        "Ranger": 927615763639062539,
                        "Hermit": 927615878592352286,
                    }[i]
                ).edit(
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


async def setup(bot):
    await bot.add_cog(TimedTasks(bot))
