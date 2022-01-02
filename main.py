import discord
from discord.enums import TeamMembershipState
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.getcwd())

intents = discord.Intents.default()
intents.members = True

load_dotenv()

from constants import *

bot = commands.Bot(command_prefix="?", intents=intents, case_insensitive=True)

for i in next(os.walk(os.getcwd() + "/cogs"), (None, None, []))[2][::-1]:
    bot.load_extension("cogs." + i[:-3])


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member: discord.Member):
    await member.add_roles(member.guild.get_role(911077094803537930))


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):

    beforeRoles = list(map(lambda role: role.id, before.roles))
    afterRoles = list(map(lambda role: role.id, after.roles))

    # await bot.get_channel(926455957737852988).send(
    #     "Before: \n>>> "
    #     + "\n".join(map(str, beforeRoles))
    #     + "\n\nAfter: \n>>> "
    #     + "\n".join(map(str, afterRoles))
    # )

    # print(beforeRoles)
    # print(afterRoles)

    if 926714233691975691 in beforeRoles and 926714233691975691 not in afterRoles:
        await bot.get_channel(926455957737852988).send(
            f"{before} has stopped boosting the server <a:swalk:926814125215076424>"
        )
    elif 926714233691975691 not in beforeRoles and 926714233691975691 in afterRoles:
        await bot.get_channel(926455957737852988).send(
            f"{before} **Thank you for boosting!** <:MFredpandaheart:925570592646787172> The Primordial Panda is pleased and grants you your own custom channel, custom reaction, and you can pick a role color!"
        )

    # print("Testing: " + str(isTesting))

    if not isTesting:
        if 924960403346296902 in beforeRoles and 924960403346296902 not in afterRoles:
            await bot.get_channel(922990287251456081).send(
                f"{before} has stopped boosting the server <a:swalk:926814125215076424>"
            )
        elif 924960403346296902 not in beforeRoles and 924960403346296902 in afterRoles:
            await bot.get_channel(923016846863634442).send(
                f"{before} **Thank you for boosting!** <:MFredpandaheart:925570592646787172> The Primordial Panda is pleased and grants you your own custom channel, custom reaction, and you can pick a role color!"
            )

            await bot.get_channel(922990287251456081).send(
                f"{before} has started boosting the server <a:BlankiesDance:926111686874791996>"
            )


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if (
        os.environ["BOT_ENV"] == "development"
        and message.channel.id == 912387794821861396
    ) or (
        os.environ["BOT_ENV"] == "production"
        and message.channel.id != 912387794821861396
    ):
        await bot.process_commands(message)


@bot.command()
@commands.has_role("Entering Pandas")
async def verify(ctx: commands.Context):
    if ctx.channel.id != 914929118682943549:
        return

    await ctx.message.add_reaction("\u2705")
    await ctx.author.add_roles(
        ctx.guild.get_role(914924258906497124),  # Temple Servant
        ctx.guild.get_role(924011788893315132),  # Levels
        ctx.guild.get_role(913798613879111691),  # Panda Facts
        ctx.guild.get_role(922973788713402368),  # Pingable Roles
        ctx.guild.get_role(922977639017369650),  # My bots
        ctx.guild.get_role(925770755344588850),  # Stuff and Things
    )
    await ctx.message.delete()
    await ctx.author.remove_roles(ctx.guild.get_role(911077094803537930))

    await ctx.author.send(
        embed=discord.Embed(
            description=f"As you finally make your way along the path to the meadow of the temple, a man approaches you. He looks gruff. Leisurely he glances at you then at a paper in your hand.\n\n\"Ah {ctx.author.mention}, there you are. Just in time for the morning session. If you're unsure what you should do, you could head to the {bot.get_channel(923016846863634442).mention} to meet and talk to other servants of the forest. Tell us about yourself by visiting the {bot.get_channel(912723730214563901).mention} channel. If you can't remember all the rules on the sign, you can find them in the {bot.get_channel(912196522433732618).mention} channel. If that isn't quite striking your fancy, look for the ones with red emblems just like I have on my shirt, they may be able to guide your way, as they are the direct subordinates of the pink hatted shrine priestess.\"\n\nHmm, you're looking a little green to get started right away, come see me when you're level 10. I hope you can find your peace here like I have, I quite like to spend my time alone in my {bot.get_channel(911630633036546058).mention}. Why don't you come tell me what you like once you get some experience. \"",
            colour=0xE7841B,
        )
        .set_footer(text="Mystical Forest")
        .set_thumbnail(
            url="https://cdn.discordapp.com/emojis/925101102242865297.png?size=1024"
        ),
    )

    await bot.get_channel(923016846863634442).send(
        f"A new servant, {ctx.author.mention}, has pledged their loyalty to the mystical forest. Join me in welcoming them. <@&923602007649026078>"
    )


bot.run(os.environ["BOT_TOKEN"])
