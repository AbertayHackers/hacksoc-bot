import discord
from discord.ext import commands
from libs.loadconf import config, strings, formatHelp, getResponse, LoadRules, getGuild, getEnv
from libs.colours import Colours

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	#Check for Committee Role
	async def cog_check(self, ctx):
		committee = discord.utils.get(ctx.guild.roles, name="Committee")
		if not committee in ctx.author.roles:
			Colours.warn(f"{ctx.message.author} tried to use an admin command")
			await ctx.send(getResponse("error", "improperPermissions"))
			return False
		return True

	
	@commands.command(name="rules", description=formatHelp("rules", "desc"), usage=formatHelp("rules", "usage"), aliases=["rule"])
	async def rules(self, ctx, ruleNum=None):
		rules = LoadRules()
		if not ruleNum:
			rulesList = ""
			for index, value in enumerate(rules.rules, start=1):
				rulesList += f"__**{rules.ruleWord} {index}:**__ {value}\n\n"

			rulesList += rules.footer
			embed = discord.Embed(colour=discord.Colour.green(), title=rules.title, description=rulesList)
			await ctx.send(embed=embed)
			return

		#Assume a specific rule has been requested
		try:
			ruleNum = int(ruleNum)
		except:
			await ctx.send(getResponse("error", "notAnInt"))
			return

		if ruleNum > rules.getNumRules():
			await ctx.send(getResponse("error", "ruleOutOfBounds").format(rules.getNumRules()))
			return
		elif ruleNum < 1:
			await ctx.send(getResponse("error", "ruleLessThanZero").format(ruleNum))
			return

		await ctx.send(rules.getRule(ruleNum))

	@commands.command(name="welcome", description=formatHelp("welcome", "desc"), usage=formatHelp("rules", "usage"))
	async def welcome(self, ctx):
		channel = self.bot.get_channel(getEnv("channel", "welcome"))	
		rulesChannel = getEnv("channel", "rules")
		committeeRole = getGuild(self.bot).get_role(getEnv("role", "committee"))
		with open("prewrittenText/welcome.txt") as msg:
			await channel.send(msg.read().format(rulesChannel=rulesChannel, committeeRole=committeeRole.mention))
	


def setup(bot):
	bot.add_cog(Admin(bot))
