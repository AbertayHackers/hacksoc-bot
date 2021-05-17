import discord
from discord.ext import commands
from libs.loadconf import config, formatHelp


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="version",
        description=formatHelp("version", "desc"),
        usage=formatHelp("version", "usage"),
    )
    async def contributors(self, ctx):
        await ctx.channel.send(config["version"])


def setup(bot):
    bot.add_cog(Misc(bot))
