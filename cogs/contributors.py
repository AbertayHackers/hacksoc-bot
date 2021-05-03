import discord
from discord.ext import commands
from libs.loadconf import config, strings, contributors as contributorList, formatHelp

class Contributors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Send the contributors list
	@commands.command(name="contributors", description=formatHelp("contributors", "desc"), usage=formatHelp("contributors", "usage"))
	async def contributors(ctx):
		embed = discord.Embed(colour=discord.Colour.green())
		embed.title = "Bot Contributor List"
		for i in contributorList.keys():
			text = ""
			for j in contributorList[i].keys():
				text += f"__*{j}:*__ {contributorList[i][j]}\n"
			if len(text) == 0:
				text="No socials available"
				embed.add_field(
				name=i,
				value=text,
				inline=False
			)
		await ctx.channel.send(embed=embed)
				


def setup(bot):
	bot.add_cog(Contributors(bot))
