import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(command_prefix="?")

bot.load_extension("cogs.triggers")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        await message.channel.send(f"Hello {message.author.mention}")

    await bot.process_commands(message)


@bot.command()
@commands.has_role("Entering Pandas")
async def verify(ctx: commands.Context):
    if ctx.channel.id != 914929118682943549:
        return

    await ctx.message.add_reaction("\u2705")
    await ctx.author.add_roles(ctx.guild.get_role(914924258906497124))
    await ctx.message.delete()
    await ctx.author.remove_roles(ctx.guild.get_role(911077094803537930))


bot.run(os.environ["BOT_TOKEN"])
