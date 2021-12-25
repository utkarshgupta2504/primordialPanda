# -*- coding: utf-8 -*-

from discord import colour
from discord.ext import commands
from discord.utils import get
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

    async def checkUserLevelUp(
        self, message: discord.Message, user: discord.User = None
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

        while currXp >= levelsDict[currLevel + 1]:
            currLevel += 1
            self.experience[id]["level"] += 1

            isLeveledUp = True

            if currLevel == 10:
                await user.add_roles(get(message.guild.roles, id=923622800508465303))

                await user.send(
                    embed=discord.Embed(
                        description=f"Ah, you've been working hard I see. I think it's time for you to become a more permanent member of the Forest. Please head to the {self.bot.get_channel(923646299797078096).mention} channel that I've opened for you to find your own way through my Mystical Forest, choose wisely as your choice is permanent. Good luck my servant",
                        colour=0xE7841B,
                    ).set_footer(text="Mystical Forest")
                )

                embedDescription += f"\n\nYou have reached the first milestone! You may now participate in giveaways, polls, and pick your path in the {self.bot.get_channel(923646299797078096).mention} channel."

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

            await self.bot.get_channel(912392441670291527).send(embed=levelUpEmbed)

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

    @commands.command(name="addXP", aliases=["giveXP"])
    @commands.has_any_role("Shrine Priestess", "Red Panda Priest")
    async def addXP(self, ctx, user: discord.User, xp: int):

        await self.updateUserExperience(str(user.id), xp)
        await self.checkUserLevelUp(ctx.message, user)

        await ctx.send(f"Added {xp} experience to {user.mention}!")

    # @commands.command()
    # async def addXPLocal(self, ctx, user: discord.User, xp: int):

    #     await self.updateUserExperience(str(user.id), xp)
    #     await self.checkUserLevelUp(ctx.message, user)

    #     await ctx.send(f"Added {xp} experience to {user.mention}!")


def setup(bot):
    bot.add_cog(Experience(bot))
