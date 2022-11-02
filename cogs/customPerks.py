# -*- coding: utf-8 -*-

from typing import Union
from discord.ext import commands, tasks
import discord
import json
import emoji
from utils.constants import isTesting
import time

from discord.utils import get


class CustomPerks(commands.Cog):
    """The description for CustomPerks goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.customReacts = {}
        self.customChannels = {}
        self.channelsToBeDeleted = {}
        self.isInitialised = False

        self.checkChannelsToDelete.start()

    @commands.Cog.listener()
    async def on_ready(self):
        with open("database/customReacts.json", "r") as f:
            self.customReacts = json.load(f)

            with open("database/customChannels.json", "r") as f1:
                self.customChannels = json.load(f1)

                with open("database/channelsToBeDeleted.json", "r") as f2:
                    self.channelsToBeDeleted = json.load(f2)

                    self.isInitialised = True

    @tasks.loop(seconds=10)
    async def checkChannelsToDelete(self):

        currTime = int(time.time())

        keys = list(self.channelsToBeDeleted.keys())[:]

        for i in keys:
            if int(i) <= currTime:

                retiredCategory = get(
                    self.bot.get_guild(911016512574341140).categories,
                    id=925016314236514355,
                )

                boostedChannel: discord.TextChannel = self.bot.get_channel(
                    self.channelsToBeDeleted[i]["channel"]
                )

                await boostedChannel.edit(category=retiredCategory)

                await boostedChannel.set_permissions(
                    self.bot.get_user(self.channelsToBeDeleted[i]["user"]),
                    overwrite=None,
                )

                await boostedChannel.set_permissions(
                    self.bot.get_guild(911016512574341140).default_role,
                    send_messages=False,
                )

                self.customChannels.pop(
                    str(self.channelsToBeDeleted[i]["user"]))

                self.channelsToBeDeleted.pop(i)

        with open("database/customChannels.json", "w") as f:
            json.dump(self.customChannels, f, indent=2)

        with open("database/channelsToBeDeleted.json", "w") as f:
            json.dump(self.channelsToBeDeleted, f, indent=2)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if not self.isInitialised:
            print("Custom Reacts not initialised")
            return

        if (isTesting and message.channel.id != 912387794821861396) or (
            not isTesting and message.channel.id == 912387794821861396
        ):
            return

        for react in self.customReacts:

            if react in message.content.lower():
                await message.add_reaction(self.customReacts[react])

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        beforeRoles = list(map(lambda role: role.id, before.roles))
        afterRoles = list(map(lambda role: role.id, after.roles))

        # await self.bot.get_channel(926455957737852988).send(
        #     "Before: \n>>> "
        #     + "\n".join(map(str, beforeRoles))
        #     + "\n\nAfter: \n>>> "
        #     + "\n".join(map(str, afterRoles))
        # )

        # print(beforeRoles)
        # print(afterRoles)
        if isTesting:
            if (
                926714233691975691 in beforeRoles
                and 926714233691975691 not in afterRoles
            ):
                await self.bot.get_channel(926455957737852988).send(
                    f"{before.mention} has stopped boosting the server <a:swalk:926814125215076424>"
                )

                if str(before.id) in self.customChannels:
                    await before.send(
                        embed=discord.Embed(
                            colour=0xE7841B,
                            description=f"In about 3 days we will send the archivist to collect your tomes of the channel {self.bot.get_channel(self.customChannels[str(before.id)]).mention}, thank you for having boosted our server, the archivist will take great care of them until you choose to take them out again.",
                        )
                        .set_thumbnail(
                            url="https://cdn.discordapp.com/emojis/925101102242865297.png?size=1024"
                        )
                        .set_footer(text="Mystical Forest"),
                    )

                    self.channelsToBeDeleted[str(int(time.time() + 10))] = {
                        "channel": self.customChannels[str(before.id)],
                        "user": before.id,
                    }

                    with open("database/channelsToBeDeleted.json", "w") as f:
                        json.dump(self.channelsToBeDeleted, f, indent=2)

            elif (
                926714233691975691 not in beforeRoles
                and 926714233691975691 in afterRoles
            ):
                await self.bot.get_channel(926455957737852988).send(
                    f"{before.mention} **Thank you for boosting!** <:MFredpandaheart:925570592646787172> The Primordial Panda is pleased and grants you your own custom channel, custom reaction, and you can pick a role color!"
                )

        # print("Testing: " + str(isTesting))

        else:
            if (
                924960403346296902 in beforeRoles
                and 924960403346296902 not in afterRoles
            ):
                await self.bot.get_channel(922990287251456081).send(
                    f"{before.mention} has stopped boosting the server <a:swalk:926814125215076424>"
                )

                if str(before.id) in self.customChannels:
                    await before.send(
                        embed=discord.Embed(
                            colour=0xE7841B,
                            description=f"In about 3 days we will send the archivist to collect your tomes of the channel {self.bot.get_channel(self.customChannels[str(before.id)]).mention}, thank you for having boosted our server, the archivist will take great care of them until you choose to take them out again.",
                        )
                        .set_thumbnail(
                            url="https://cdn.discordapp.com/emojis/925101102242865297.png?size=1024"
                        )
                        .set_footer(text="Mystical Forest"),
                    )

                    self.channelsToBeDeleted[str(int(time.time() + 259200))] = {
                        "channel": self.customChannels[str(before.id)],
                        "user": before.id,
                    }

                    with open("database/channelsToBeDeleted.json", "w") as f:
                        json.dump(self.channelsToBeDeleted, f, indent=2)

            elif (
                924960403346296902 not in beforeRoles
                and 924960403346296902 in afterRoles
            ):
                await self.bot.get_channel(923016846863634442).send(
                    f"{before.mention} **Thank you for boosting!** <:MFredpandaheart:925570592646787172> The Primordial Panda is pleased and grants you your own custom channel, custom reaction, and you can pick a role color!"
                )

                await self.bot.get_channel(922990287251456081).send(
                    f"{before.mention} has started boosting the server <a:BlankiesDance:926111686874791996>"
                )

    @commands.group(
        name="customReact", case_insensitive=True, invoke_without_command=True
    )
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def customReact(self, ctx):
        await ctx.send(str(self.customReacts))

    @customReact.command(name="add")
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def add(
        self,
        ctx: commands.Context,
        trigger: str = None,
        react: Union[discord.Emoji, str] = None,
    ):

        if trigger is None:
            await ctx.reply("Need a trigger!")
            return

        if react is None:
            await ctx.reply("Need an emote to react!")
            return

        reactString = ""

        if type(react) == str:
            emojiList = emoji.emoji_lis(react)

            if len(emojiList) == 0 or emojiList[0]["location"] != 0:
                await ctx.reply("Need an emote to react!")
                return

            else:
                reactString = emojiList[0]["emoji"]

        else:
            reactString = str(react)

        self.customReacts[trigger] = reactString

        with open("database/customReacts.json", "w") as f:
            json.dump(self.customReacts, f, indent=2)

        await ctx.reply("Successfully added custom react!")

    @customReact.command(name="remove", aliases=["rem", "delete", "del"])
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def remove(self, ctx: commands.Context, trigger: str = None):

        if trigger is None:
            await ctx.reply("Need a trigger!")
            return

        if trigger in self.customReacts:
            self.customReacts.pop(trigger)

        else:
            await ctx.reply("No such trigger!")
            return

        with open("database/customReacts.json", "w") as f:
            json.dump(self.customReacts, f, indent=2)

        await ctx.reply("Successfully removed custom react!")

    @commands.group(name="customChannel", case_insensitive=True)
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def customChannel(self, ctx: commands.Context):

        pass

    @customChannel.group(
        name="create", aliases=["add", "cr", "make"], invoke_without_command=True
    )
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def createCustomChannel(
        self, ctx: commands.Context, name: str = None, user: discord.User = None
    ):

        if name is None:
            await ctx.reply("Need a channel name!")
            return

        if user is None:
            await ctx.reply("Need a user to provide admin perms to!")
            return

        sentMessage: discord.Message = await ctx.send("Creating custom channel")

        theMoorsCategory: discord.CategoryChannel = get(
            ctx.guild.categories, id=927302268431265843
        )

        createdChannel: discord.TextChannel = (
            await theMoorsCategory.create_text_channel(name)
        )

        perms: discord.PermissionOverwrite = createdChannel.overwrites_for(
            user)
        perms.manage_messages = True
        perms.manage_channels = True

        await createdChannel.set_permissions(user, overwrite=perms)

        await sentMessage.edit(content="Channel created successfully!")

    @createCustomChannel.command(name="boost", aliases=["booster"])
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def createBoostChannel(
        self, ctx: commands.Context, name: str, user: discord.Member
    ):

        if name is None:
            await ctx.reply("Need a channel name!")
            return

        if user is None:
            await ctx.reply("Need a user to provide admin perms to!")
            return

        boostRole = get(
            ctx.guild.roles, id=926714233691975691 if isTesting else 924960403346296902
        )

        if boostRole not in user.roles:
            await ctx.reply("This user is not a booster!")
            return

        sentMessage: discord.Message = await ctx.send("Creating custom channel...")

        theMoorsCategory: discord.CategoryChannel = get(
            ctx.guild.categories, id=927302268431265843
        )

        createdChannel: discord.TextChannel = (
            await theMoorsCategory.create_text_channel(name)
        )

        perms: discord.PermissionOverwrite = createdChannel.overwrites_for(
            user)
        perms.manage_messages = True
        perms.manage_channels = True

        await createdChannel.set_permissions(user, overwrite=perms)

        self.customChannels[str(user.id)] = createdChannel.id

        with open("database/customChannels.json", "w") as f:
            json.dump(self.customChannels, f, indent=2)

        await sentMessage.edit(content="Booster Channel created successfully!")

    @customChannel.group(name="revive", aliases=["rev"], invoke_without_command=True)
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def reviveCustomChannel(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel = None,
        user: discord.Member = None,
    ):

        if channel is None:
            await ctx.reply("Please mention a channel!")
            return

        if user is None:
            await ctx.reply("Please mention a user for perms!")
            return

        if channel.category_id != 925016314236514355:
            await ctx.reply("The channel is not archived!")
            return

        sentMessage = await ctx.send("Reviving channel...")

        perms: discord.PermissionOverwrite = channel.overwrites_for(user)
        perms.manage_messages = True
        perms.manage_channels = True

        await channel.set_permissions(user, overwrite=perms)

        theMoorsCategory: discord.CategoryChannel = get(
            ctx.guild.categories, id=927302268431265843
        )

        await channel.edit(category=theMoorsCategory)

        await sentMessage.edit(content="Channel revived successfully!")

    @reviveCustomChannel.command(name="boost", aliases=["booster"])
    @commands.has_any_role(
        "Shrine Priestess",
        "Red Panda Priest",
        "Ninja Cat",
        "Utkarsh",
        "Venster",
        "Local Hermit",
    )
    async def reviveChannelAsBooster(
        self, ctx: commands.Context, channel: discord.TextChannel, user: discord.Member
    ):

        if channel is None:
            await ctx.reply("Please mention a channel!")
            return

        if user is None:
            await ctx.reply("Please mention a user for perms!")
            return

        if channel.category_id != 925016314236514355:
            await ctx.reply("The channel is not archived!")
            return

        boostRole = get(
            ctx.guild.roles, id=926714233691975691 if isTesting else 924960403346296902
        )

        if boostRole not in user.roles:
            await ctx.reply("This user is not a booster!")
            return

        sentMessage = await ctx.send("Reviving channel...")

        perms: discord.PermissionOverwrite = channel.overwrites_for(user)
        perms.manage_messages = True
        perms.manage_channels = True

        await channel.set_permissions(user, overwrite=perms)

        theMoorsCategory: discord.CategoryChannel = get(
            ctx.guild.categories, id=927302268431265843
        )

        await channel.edit(category=theMoorsCategory)

        self.customChannels[str(user.id)] = channel.id

        with open("database/customChannels.json", "w") as f:
            json.dump(self.customChannels, f, indent=2)

        await sentMessage.edit(content="Channel revived as booster successfully!")


async def setup(bot):
    await bot.add_cog(CustomPerks(bot))
