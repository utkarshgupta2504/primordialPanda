import asyncio
from discord.ext import commands
import io
import traceback
import aiohttp
import sys
import os
import discord
from dotenv import load_dotenv
load_dotenv()

from constants import *

sys.path.append(os.getcwd())

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class MyBot(commands.Bot):
    async def setup_hook(self):
        for i in next(os.walk(os.getcwd() + "/cogs"), (None, None, []))[2][::-1]:
            await bot.load_extension("cogs." + i[:-3])


bot = MyBot(command_prefix="?", intents=intents, case_insensitive=True)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member: discord.Member):
    await member.add_roles(member.guild.get_role(911077094803537930))


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
        f"A new servant, {ctx.author.mention}, has pledged their loyalty to the Mystical Forest. Join me in welcoming them. <@&923602007649026078>"
    )


# @bot.command(name="rename")
# async def renameEmoji(ctx: commands.Context):

#     sentMessage = await ctx.send("Renaming emojis, please wait...")

#     for emote in ctx.guild.emojis:

#         if emote.name[-3:] != "OwO":
#             await emote.edit(name=emote.name + "OwO")

#     await sentMessage.edit(content="Rename Successful")

# These exceptions are ignored.
filter_excs = (commands.CommandNotFound, commands.CheckFailure)
# These are exception types you want to handle explicitly.
handle_excs = (commands.UserInputError,)


async def try_hastebin(content):
    """Upload to Hastebin, if possible."""
    payload = content.encode('utf-8')
    async with aiohttp.ClientSession(raise_for_status=True) as cs:
        async with cs.post('https://hastebin.com/documents', data=payload) as res:
            post = await res.json()
    uri = post['key']
    return f'https://hastebin/{uri}'


async def send_to_owner(content):
    """Send content to owner. If content is small enough, send directly.
    Otherwise, try Hastebin first, then upload as a File."""
    owner = bot.get_user(bot.owner_id)
    log_channel = bot.get_channel(941054428314738738)
    if owner is None:
        return
    if len(content) < 1990:
        await owner.send(f'```\ncontent\n```')
        await log_channel.send(f'```\ncontent\n```')
    else:
        try:
            hastebinResponse = await try_hastebin(content)
            await owner.send(hastebinResponse)
            await log_channel.send(hastebinResponse)
        except aiohttp.ClientResponseError:
            await owner.send(file=discord.File(io.StringIO(content), filename='traceback.txt'))
            await log_channel.send(file=discord.File(io.StringIO(content), filename='traceback.txt'))


@bot.event
async def on_error(event, *args, **kwargs):
    """Error handler for all events."""
    print("Error", event)
    s = traceback.format_exc()
    content = f'Ignoring exception in {event}\n{s}'
    print(content, file=sys.stderr)
    await send_to_owner(content)


async def handle_command_error(ctx: commands.Context, exc: Exception):
    """Handle specific exceptions separately here"""
    pass


@bot.event
async def on_command_error(ctx: commands.Context, exc: Exception):
    """Error handler for commands"""
    if isinstance(exc, filter_excs):
        # These exceptions are ignored completely.
        return

    # if isinstance(exc, handle_excs):
    #     # Explicitly handle these exceptions.
    #     return await handle_command_error(ctx, exc)

    # print("Error", exc.__traceback__)

    # Log the error and bug the owner.
    exc = getattr(exc, 'original', exc)
    lines = ''.join(traceback.format_exception(
        exc.__class__, exc, exc.__traceback__))
    lines = f'Ignoring exception in command {ctx.command}:\n{lines}'
    print(lines)
    await send_to_owner(lines)


@bot.command()
async def syncCommands(ctx):
    await bot.tree.sync()


async def main():

    async with bot:
        await bot.start(os.getenv("BOT_TOKEN"))

asyncio.run(main())
