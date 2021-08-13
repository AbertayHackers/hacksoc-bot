import discord
from discord.ext import commands
from libs.loadconf import config, strings, contributors as contributorList, formatHelp


class Contributors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Send the contributors list
    @commands.command(
        name="contributors",
        description=formatHelp("contributors", "desc"),
        usage=formatHelp("contributors", "usage"),
    )
    async def contributors(self, ctx):
        embed = discord.Embed(colour=discord.Colour.green())
        embed.title = "Bot Contributor List"
        for i in contributorList.keys():
            text = ""
            for j in contributorList[i].keys():
                text += f"__*{j}:*__ {contributorList[i][j]}\n"
            if len(text) == 0:
                text = "No socials available"
            embed.add_field(name=i, value=text, inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command(name="github", description=formatHelp("github", "desc"), usage=formatHelp("github", "usage"))
    async def github(self, ctx):
        embed = discord.Embed(colour=discord.Color.blue())
        embed.set_thumbnail(url="https://github.com/fluidicon.png")
        embed.title = "Contribute to the Bot:"
        embed.description = strings["links"]["botGithub"]
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Contributors(bot))
