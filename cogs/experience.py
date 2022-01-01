# -*- coding: utf-8 -*-

import asyncio
from os import environ
from discord import colour
from discord.ext import commands
from discord.utils import get
import discord
import typing
import json

from constants import *


class Experience(commands.Cog):
    """The description for Experience goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 8.0, commands.BucketType.member
        )
        self.isInitialised = False
        self.experience = {}

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def updateUserExperience(self, id, xp=1):
        if id not in self.experience:
            self.experience[id] = {"xp": 0, "level": 0}

        self.experience[id]["xp"] += xp

        with open("database/experience.json", "w") as f:

            json.dump(self.experience, f, indent=2)

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
                .set_thumbnail(url=user.avatar_url)
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

    async def addPathRoles(self, level, roles, ctx: commands.Context):

        for lvl in roles:
            if level >= lvl:
                await ctx.author.add_roles(ctx.guild.get_role(roles[lvl]))

    @commands.Cog.listener()
    async def on_ready(self):
        with open("database/experience.json", "r") as f:
            self.experience = json.load(f)

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

    @commands.command(name="choosePath")
    async def choosePath(self, ctx: commands.Context, path: str = None):

        if self.experience[str(ctx.author.id)]["level"] < 10:
            await ctx.reply(
                "You're still looking a little green, come see me at level 10"
            )
            return

        if ctx.guild.get_role(923622800508465303) not in ctx.author.roles:
            await ctx.send(
                f"{ctx.author.mention}, you are already on the **Path of the {self.experience[str(ctx.author.id)]['path']}**, this choice is __permanent__"
            )
            return

        if not isTesting and ctx.channel.id != 923646299797078096:
            await ctx.reply(
                f".. but there is no one here, please see me in {self.bot.get_channel(923646299797078096).mention}"
            )
            return

        if path is None or path.lower() not in [
            "overseer",
            "architect",
            "hermit",
            "caregiver",
            "ranger",
        ]:
            await ctx.reply(
                "That is not a proper path, please select from Overseer | Architect | Hermit | Caregiver | Ranger"
            )
            return

        path = path.lower()
        currLevel = self.experience[str(ctx.author.id)]["level"]

        if path == "overseer":

            await self.addPathRoles(
                currLevel,
                {
                    0: 923624607091658803,  # Path of The Overseer
                    1: 923999016218406942,  # Apprentice of the Overseer
                },
                ctx,
            )

            self.experience[str(ctx.author.id)]["path"] = "Overseer"

        elif path == "architect":

            await self.addPathRoles(
                currLevel,
                {
                    0: 923635122840940625,  # Path of The Architect
                    1: 924008140205338664,  # Apprentice of the Architect
                },
                ctx,
            )

            self.experience[str(ctx.author.id)]["path"] = "Architect"

        elif path == "hermit":

            await self.addPathRoles(
                currLevel,
                {
                    0: 923626226906701845,  # Path of The Hermit
                    1: 924010222517891092,  # Apprentice of the Hermit
                },
                ctx,
            )

            self.experience[str(ctx.author.id)]["path"] = "Hermit"

        elif path == "ranger":

            await self.addPathRoles(
                currLevel,
                {
                    0: 923633643761594459,  # Path of The Ranger
                    1: 924009432344567848,  # Apprentice of the Ranger
                },
                ctx,
            )

            self.experience[str(ctx.author.id)]["path"] = "Ranger"

        elif path == "caregiver":

            await self.addPathRoles(
                currLevel,
                {
                    0: 923633634160836619,  # Path of The Caregiver
                    1: 924006409102827552,  # Apprentice of the Caregiver
                },
                ctx,
            )

            self.experience[str(ctx.author.id)]["path"] = "Caregiver"

        response = f"You have successfully chosen the path of the {path.capitalize()}"

        if currLevel > 19:
            response += "\nBecause you chose your path at a later stage, the primordial panda takes away your experience to start at the begin of the path you've chosen to follow."

            self.experience[str(ctx.author.id)]["xp"] = 6515
            self.experience[str(ctx.author.id)]["level"] = 19

        with open("database/experience.json", "w") as f:

            json.dump(self.experience, f, indent=2)

        await self.bot.get_channel(
            926455957737852988 if isTesting else 925821155019980830
        ).send(
            f"{ctx.author.mention} has chosen to walk along the **Path of the {path.capitalize()}**"
        )

        await self.bot.get_channel(
            926455957737852988 if isTesting else 923016846863634442
        ).send(
            f"{ctx.author.mention} now walks the **Path of the {path.capitalize()}**"
        )

        await self.bot.get_channel(
            926455957737852988 if isTesting else dormID[path.capitalize()]
        ).send(
            f"{ctx.author.mention} has joined our superior path, <@&{pathLevelRoles[path.capitalize()][0]}>, come welcome them!"
        )

        await ctx.reply(response, delete_after=5)

        await asyncio.sleep(5)

        await ctx.author.remove_roles(ctx.guild.get_role(923622800508465303))

        await ctx.message.delete()

    @commands.command(name="rank", aliases=["level", "r", "lvl"])
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

        rankEmbed = (
            discord.Embed(
                title=str(user), description="Your Experience Details", color=0xE7841B
            )
            .add_field(name="Rank", value=f"{userRank}", inline=False)
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
            .set_thumbnail(url=user.avatar_url)
        )

        await ctx.send(embed=rankEmbed)

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context, args: str = None):

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
            .set_thumbnail(url=ctx.guild.icon_url)
        )

        for pos, xp in mappedLeaderboardXP:
            if pos > 10:
                break

            leaderBoardEmbed.add_field(
                name="\u200b",
                value=f"**#{pos} <:pinkdot:913881657994543184> {xp[0]}**\n<:AAblank:926416287054323773> Level {xp[1]['level']}\n<:AAblank:926416287054323773> Path: {xp[1]['path'] if 'path' in xp[1] else 'Freeloader' if xp[1]['level'] >= 10 else 'None'}\n<:AAblank:926416287054323773> Total Exp: {xp[1]['xp']}",
                inline=False,
            )

        await ctx.send(embed=leaderBoardEmbed)

    @commands.command(name="addXP", aliases=["giveXP"])
    @commands.has_any_role("Shrine Priestess", "Red Panda Priest")
    async def addXP(self, ctx, user: discord.Member, xp: int):

        await self.updateUserExperience(str(user.id), xp)
        await self.checkUserLevelUp(ctx.message, user)

        await ctx.send(f"Added {xp} experience to {user.mention}!")

    @commands.command()
    async def addXPLocal(self, ctx, user: discord.Member, xp: int):

        if environ["BOT_ENV"] != "development":
            return

        await self.updateUserExperience(str(user.id), xp)
        await self.checkUserLevelUp(ctx.message, user)

        await ctx.send(f"Added {xp} experience to {user.mention}!")


def setup(bot):
    bot.add_cog(Experience(bot))
