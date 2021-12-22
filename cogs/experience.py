# -*- coding: utf-8 -*-

from discord import colour
from discord.ext import commands
import discord
import typing
import json

from constants import levelsDict


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

    async def checkUserLevelUp(self, id):
        currLevel = self.experience[id]["level"]
        currXp = self.experience[id]["xp"]

        if currXp >= levelsDict[currLevel + 1]:

            self.experience[id]["level"] += 1

            with open("database/experience.json", "w") as f:

                json.dump(self.experience, f, indent=2)

            return currLevel + 1

        return -1

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

                newLevel = await self.checkUserLevelUp(str(message.author.id))

                if newLevel != -1:

                    levelUpEmbed = discord.Embed(
                        title="Level Up!",
                        description=f"🏅Congratulations {message.author.mention}! The Primordial Panda recognizes your hard work and has blessed you! You are now level {newLevel}!🏅",
                        colour=0xE7841B,
                    )

                    levelUpEmbed.set_footer(text="Mystical Forest")
                    levelUpEmbed.set_thumbnail(url=message.author.avatar_url)

                    await self.bot.get_channel(912392441670291527).send(
                        embed=levelUpEmbed
                    )

    @commands.command(name="addXP", aliases=["giveXP"])
    @commands.has_any_role("Shrine Priestess", "Red Panda Priest")
    async def addXP(self, ctx, user: discord.User, xp: int):

        await self.updateUserExperience(str(user.id), xp)

        newLevel = await self.checkUserLevelUp(str(user.id))

        if newLevel != -1:

            levelUpEmbed = discord.Embed(
                title="Level Up!",
                description=f"🏅Congratulations {user.mention}! The Primordial Panda recognizes your hard work and has blessed you! You are now level {newLevel}!🏅",
                colour=0xE7841B,
            )

            levelUpEmbed.set_footer(text="Mystical Forest")
            levelUpEmbed.set_thumbnail(url=user.avatar_url)

            await self.bot.get_channel(912392441670291527).send(embed=levelUpEmbed)

        await ctx.send(f"Added {xp} experience to {user.mention}!")


def setup(bot):
    bot.add_cog(Experience(bot))
