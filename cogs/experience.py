# -*- coding: utf-8 -*-

import asyncio
from os import environ
from discord import Interaction, colour, app_commands
from discord.ext import commands, tasks
from discord.utils import get
import discord
from typing import Literal, Optional
import json
import time

from utils.constants import *


class Experience(commands.Cog):
    """The description for Experience goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 8.0, commands.BucketType.member
        )
        self.isInitialised = False
        self.experience = {}
        self.weeklyLeaderboard = {}
        self.config = {}

        self.resetWeeklyLeaderboard.start()

    def get_ratelimit(self, message: discord.Message) -> Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def updateUserExperience(self, id, xp=1):
        if id not in self.experience:
            self.experience[id] = {"xp": 0, "level": 0}

        if id not in self.weeklyLeaderboard["leaderboard"]:
            self.weeklyLeaderboard["leaderboard"][id] = 0

        xp = int(xp * self.config.get("multiplier", 1))

        self.experience[id]["xp"] += xp
        self.weeklyLeaderboard["leaderboard"][id] += xp

        with open("database/experience.json", "w") as f:
            json.dump(self.experience, f, indent=2)

            with open("database/weeklyLeaderboard.json", "w") as f1:
                json.dump(self.weeklyLeaderboard, f1, indent=2)

    async def checkUserLevelUp(
        self, message: discord.Message, user: discord.Member = None
    ):
        if user is None:
            user = message.author

        id = str(user.id)

        currLevel = self.experience[id]["level"]
        currXp = self.experience[id]["xp"]

        isLeveledUp = False

        rolesToAdd = []
        embedsToSend = []

        embedDescription = f"🏅Congratulations {user.mention}! The Primordial Panda recognizes your hard work and has blessed you! You are now level <level>!🏅"

        userXP = self.experience[id]

        while (currLevel + 1) in levelsDict and currXp >= levelsDict[currLevel + 1]:
            currLevel += 1
            self.experience[id]["level"] += 1

            userXP = self.experience[id]

            isLeveledUp = True

            if currLevel == 10:
                rolesToAdd.append(get(message.guild.roles, id=923622800508465303))

                embedsToSend.append(
                    discord.Embed(
                        description=f"Ah, you've been working hard I see. I think it's time for you to become a more permanent member of the Forest. Please head to the {self.bot.get_channel(923646299797078096).mention} channel that has been opened for you to find your own way through the Mystical Forest, choose wisely as your choice is **__permanent__**. Good luck servant of the forest",
                        colour=0xE7841B,
                    ).set_footer(text="Mystical Forest")
                )

                embedDescription += f"\n\nThe Primordial Panda is pleased with your hard work! You have received, in addition to level 10, the following blessings: participate in giveaways, polls, and can pick your path in the {self.bot.get_channel(923646299797078096).mention} channel!"

            if currLevel > 19 and "path" in self.experience[id]:
                if currLevel in pathLevelRoles[self.experience[id]["path"]]:
                    rolesToAdd.append(
                        get(
                            message.guild.roles,
                            id=pathLevelRoles[self.experience[id]["path"]][currLevel],
                        )
                    )

            if currLevel == 20:
                if "path" in userXP:
                    rolesToAdd.append(
                        get(
                            message.guild.roles,
                            id=pathLevelRoles[userXP["path"]][20],
                        )
                    )

                embedDescription += f"\n\nThe Primordial Panda is pleased with your hard work! You have received, in addition to level {currLevel}, the following blessings: choose a role color, change your nickname, receive OwO manual hunt rewards, and access solitary channels!"

            if currLevel == 40:
                if "path" in userXP:
                    rolesToAdd.append(
                        get(
                            message.guild.roles,
                            id=pathLevelRoles[userXP["path"]][40],
                        )
                    )

                embedDescription += f"\n\nThe Primordial Panda is pleased with your hard work! You have received, in addition to level {currLevel}, the following blessings: choose from the level 40 role color list and have a ONE time use XP boost!"

            if currLevel == 60:
                if "path" in userXP:
                    rolesToAdd.append(
                        get(
                            message.guild.roles,
                            id=pathLevelRoles[userXP["path"]][60],
                        )
                    )

                embedDescription += f"\n\nThe Primordial Panda is pleased with your hard work! You have received, in addition to level {currLevel}, the following blessings: A custom reaction!"

            if currLevel == 80:
                if "path" in userXP:
                    rolesToAdd.append(
                        get(
                            message.guild.roles,
                            id=pathLevelRoles[userXP["path"]][80],
                        )
                    )

                embedDescription += f"\n\nThe Primordial Panda is pleased with your hard work! You have received, in addition to level {currLevel}, the following blessings: You're own channel!"

            if currLevel == 100:
                if "path" in userXP:
                    rolesToAdd.append(
                        get(
                            message.guild.roles,
                            id=pathLevelRoles[userXP["path"]][80],
                        )
                    )

                embedDescription += f"\n\nThe Primordial Panda is pleased with your hard work! You have received, in addition to level {currLevel}, the following blessings: A custom command!"

        if isLeveledUp:
            with open("database/experience.json", "w") as f:
                json.dump(self.experience, f, indent=2)

            levelUpEmbed = (
                discord.Embed(
                    title="Level Up!",
                    description=embedDescription.replace("<level>", str(currLevel)),
                    colour=0xE7841B,
                )
                .set_footer(text="Mystical Forest")
                .set_thumbnail(url=user.avatar.url)
            )

            await user.add_roles(*rolesToAdd)

            for e in embedsToSend:
                await user.send(
                    embed=e.set_thumbnail(
                        url="https://cdn.discordapp.com/emojis/925101102242865297.png?size=1024"
                    )
                )

            if environ["BOT_ENV"] != "development":
                await self.bot.get_channel(912392441670291527).send(embed=levelUpEmbed)

            else:
                await self.bot.get_channel(926136930066911314).send(embed=levelUpEmbed)

    async def addPathRoles(self, level, roles, interaction: discord.Interaction):
        for lvl in roles:
            if level >= lvl:
                await interaction.user.add_roles(interaction.guild.get_role(roles[lvl]))

    @commands.Cog.listener()
    async def on_ready(self):
        print("ON READY EXPERIENCE")

        with open("database/experience.json", "r") as f:
            self.experience = json.load(f)

            with open("database/weeklyLeaderboard.json", "r") as f1:
                self.weeklyLeaderboard = json.load(f1)

                with open("database/config.json", "r") as f2:
                    self.config = json.load(f2)
                    self.isInitialised = True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.isInitialised:
            print("Experience not initialised")
            return

        if message.author != self.bot.user and not message.author.bot:
            # Getting the ratelimit left
            ratelimit = self.get_ratelimit(message)
            if ratelimit is None:
                await self.updateUserExperience(str(message.author.id))
                await self.checkUserLevelUp(message)

    @app_commands.command(
        name="choose-path", description="Choose a Guardian path to follow"
    )
    @app_commands.guild_only()
    async def choosePath(
        self,
        interaction: Interaction,
        path: Literal["Overseer", "Architect", "Ranger", "Hermit", "Caregiver"],
    ):
        if self.experience[str(interaction.user.id)]["level"] < 10:
            await interaction.response.send_message(
                content="You're still looking a little green, come see me at level 10"
            )
            return

        if interaction.guild.get_role(923622800508465303) not in interaction.user.roles:
            await interaction.response.send_message(
                content=f"{interaction.user.mention}, you are already on the **Path of the {self.experience[str(interaction.user.id)]['path']}**, this choice is __permanent__"
            )
            return

        if not isTesting and interaction.channel.id != 923646299797078096:
            await interaction.response.send_message(
                content=f".. but there is no one here, please see me in {self.bot.get_channel(923646299797078096).mention}"
            )
            return

        if path is None or path.lower() not in [
            "overseer",
            "architect",
            "hermit",
            "caregiver",
            "ranger",
        ]:
            await interaction.response.send_message(
                content="That is not a proper path, please select from Overseer | Architect | Hermit | Caregiver | Ranger"
            )
            return

        path = path.lower()
        currLevel = self.experience[str(interaction.user.id)]["level"]

        if path == "overseer":
            await self.addPathRoles(
                currLevel,
                {
                    0: 923624607091658803,  # Path of The Overseer
                    1: 923999016218406942,  # Apprentice of the Overseer
                },
                interaction,
            )

            self.experience[str(interaction.user.id)]["path"] = "Overseer"

        elif path == "architect":
            await self.addPathRoles(
                currLevel,
                {
                    0: 923635122840940625,  # Path of The Architect
                    1: 924008140205338664,  # Apprentice of the Architect
                },
                interaction,
            )

            self.experience[str(interaction.user.id)]["path"] = "Architect"

        elif path == "hermit":
            await self.addPathRoles(
                currLevel,
                {
                    0: 923626226906701845,  # Path of The Hermit
                    1: 924010222517891092,  # Apprentice of the Hermit
                },
                interaction,
            )

            self.experience[str(interaction.user.id)]["path"] = "Hermit"

        elif path == "ranger":
            await self.addPathRoles(
                currLevel,
                {
                    0: 923633643761594459,  # Path of The Ranger
                    1: 924009432344567848,  # Apprentice of the Ranger
                },
                interaction,
            )

            self.experience[str(interaction.user.id)]["path"] = "Ranger"

        elif path == "caregiver":
            await self.addPathRoles(
                currLevel,
                {
                    0: 923633634160836619,  # Path of The Caregiver
                    1: 924006409102827552,  # Apprentice of the Caregiver
                },
                interaction,
            )

            self.experience[str(interaction.user.id)]["path"] = "Caregiver"

        response = f"You have successfully chosen the path of the {path.capitalize()}"

        if currLevel > 19:
            response += "\nBecause you chose your path at a later stage, the primordial panda takes away your experience to start at the begin of the path you've chosen to follow."

            self.experience[str(interaction.user.id)]["xp"] = 6515
            self.experience[str(interaction.user.id)]["level"] = 19

        with open("database/experience.json", "w") as f:
            json.dump(self.experience, f, indent=2)

        await self.bot.get_channel(
            926455957737852988 if isTesting else 925821155019980830
        ).send(
            f"{interaction.user.mention} has chosen to walk along the **Path of the {path.capitalize()}**"
        )

        await self.bot.get_channel(
            926455957737852988 if isTesting else 923016846863634442
        ).send(
            f"{interaction.user.mention} now walks the **Path of the {path.capitalize()}**"
        )

        await self.bot.get_channel(
            926455957737852988 if isTesting else dormID[path.capitalize()]
        ).send(
            f"{interaction.user.mention} has joined our superior path, <@&{pathLevelRoles[path.capitalize()][0]}>, come welcome them!"
        )

        await interaction.response.send_message(content=response, delete_after=5)

        await asyncio.sleep(5)

        await interaction.user.remove_roles(
            interaction.guild.get_role(923622800508465303)
        )

        await interaction.message.delete()

    @commands.hybrid_command(name="rank", aliases=["level", "r", "lvl"])
    @app_commands.guild_only()
    async def rank(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if str(user.id) not in self.experience:
            await ctx.send("This user has not yet begun their journey!")
            return

        userXP = self.experience[str(user.id)]

        userRank = next(
            (
                pos
                for pos, xp in enumerate(
                    sorted(
                        self.experience.items(),
                        key=lambda item: item[1]["xp"],
                        reverse=True,
                    ),
                    1,
                )
                if xp[0] == str(user.id)
            ),
            None,
        )

        weeklyRank = next(
            (
                pos
                for pos, xp in enumerate(
                    sorted(
                        self.weeklyLeaderboard["leaderboard"].items(),
                        key=lambda item: item[1],
                        reverse=True,
                    ),
                    1,
                )
                if xp[0] == str(user.id)
            ),
            None,
        )

        rankEmbed = (
            discord.Embed(
                title=str(user), description="Your Experience Details", color=0xE7841B
            )
            .add_field(name="Server Rank", value=f"{userRank}", inline=True)
            .add_field(name="Weekly Rank", value=f"{weeklyRank}", inline=True)
            .add_field(
                name="XP",
                value=f"{userXP['xp']}/{str(levelsDict[userXP['level']+1]) if (userXP['level']+1) in levelsDict else 'MAX'}",
                inline=False,
            )
            .add_field(name="Level", value=f"{userXP['level']}", inline=False)
            .add_field(
                name="Path",
                value=f"{userXP['path'] if 'path' in userXP else 'Freeloader' if userXP['level'] >= 10 else 'None'}",
            )
            .set_footer(text="Mystical Forest")
            .set_thumbnail(url=user.avatar.url)
        )

        await ctx.send(embed=rankEmbed)

    @commands.group(name="leaderboard", aliases=["lb"], invoke_without_command=True)
    async def leaderboard(self, ctx: commands.Context):
        leaderboardXP = sorted(
            self.experience.items(), key=lambda item: item[1]["xp"], reverse=True
        )

        mappedLeaderboardXP = enumerate(
            map(
                lambda xp: (f"<@!{xp[0]}>", xp[1]),
                leaderboardXP,
            ),
            1,
        )

        leaderBoardEmbed = (
            discord.Embed(title="Leaderboard", colour=0xE7841B)
            .set_footer(text="Mystical Forest")
            .set_thumbnail(url=ctx.guild.icon.url)
        )

        for pos, xp in mappedLeaderboardXP:
            if pos > 10:
                break

            leaderBoardEmbed.add_field(
                name="\u200b",
                value=f"**{f'#{pos}' if pos > 3 else ':first_place:' if pos == 1 else ':second_place:' if pos == 2 else ':third_place:'} <:pinkdot:913881657994543184> {xp[0]}**\n<:AAblank:926416287054323773> Level {xp[1]['level']}\n<:AAblank:926416287054323773> Path: {xp[1]['path'] if 'path' in xp[1] else 'Freeloader' if xp[1]['level'] >= 10 else 'None'}\n<:AAblank:926416287054323773> Total Exp: {xp[1]['xp']}",
                inline=False,
            )

        await ctx.send(embed=leaderBoardEmbed)

    @leaderboard.command(name="weekly", aliases=["w"])
    async def weekly(self, ctx):
        weeklyLeaderboardXP = sorted(
            self.weeklyLeaderboard["leaderboard"].items(),
            key=lambda item: item[1],
            reverse=True,
        )

        mappedWeeklyLeaderboardXP = enumerate(
            map(
                lambda xp: (f"<@!{xp[0]}>", xp[1]),
                weeklyLeaderboardXP,
            ),
            1,
        )

        weeklyLeaderBoardEmbed = (
            discord.Embed(title="Weekly Leaderboard", colour=0xE7841B)
            .set_footer(text="Mystical Forest")
            .set_thumbnail(url=ctx.guild.icon.url)
        )

        for pos, xp in mappedWeeklyLeaderboardXP:
            if pos > 10:
                break

            weeklyLeaderBoardEmbed.add_field(
                name="\u200b",
                value=f"**{f'#{pos}' if pos > 3 else ':first_place:' if pos == 1 else ':second_place:' if pos == 2 else ':third_place:'} <:pinkdot:913881657994543184> {xp[0]}**\n<:AAblank:926416287054323773> Exp: {xp[1]}",
                inline=False,
            )

        await ctx.send(embed=weeklyLeaderBoardEmbed)

    @commands.hybrid_command(name="multi", description="Set the XP multiplier")
    @commands.has_any_role("Shrine Priestess", "Red Panda Priest")
    @app_commands.guild_only()
    async def multi(self, ctx: commands.Context, multiplier: float):
        if multiplier < 1:
            await ctx.send("Multiplier cannot be less than 1")
            return

        self.config["multiplier"] = multiplier

        with open("database/config.json", "w") as f:
            json.dump(self.config, f, indent=2)

        await ctx.send(f"XP multiplier set to {multiplier}")

    @tasks.loop(minutes=10)
    async def resetWeeklyLeaderboard(self):
        if not self.isInitialised:
            return

        while int(time.time()) - self.weeklyLeaderboard["lastTime"] >= 604800:
            print("Resetting weekly leaderboard")

            self.weeklyLeaderboard["lastTime"] += 604800
            self.weeklyLeaderboard["leaderboard"] = {}

        with open("database/weeklyLeaderboard.json", "w") as f1:
            json.dump(self.weeklyLeaderboard, f1, indent=2)

    @resetWeeklyLeaderboard.before_loop
    async def beforeReset(self):
        await self.bot.wait_until_ready()

    @commands.hybrid_command(name="addxp", aliases=["giveXP"])
    @commands.has_any_role("Shrine Priestess", "Red Panda Priest")
    @app_commands.guild_only()
    async def addXP(self, ctx, user: discord.Member, xp: int):
        await self.updateUserExperience(str(user.id), xp)
        await self.checkUserLevelUp(ctx.message, user)

        await ctx.send(f"Added {xp} experience to {user.mention}!")


async def setup(bot):
    await bot.add_cog(Experience(bot))
