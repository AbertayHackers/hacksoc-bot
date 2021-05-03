#!/usr/bin/python3
import discord, asyncio, json, re
from discord.ext import commands


prefix="!"
bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
	print("Connected")
	print(bot.user)



@bot.command()
async def ping(ctx):
	await ctx.send("Pong!")



@bot.listen()
async def on_message(message):
	
	if "crypto" in message.content.lower().replace(" ", "") and message.author != bot.user:
		for index, i in enumerate(message.content.lower().split()):
			if "crypto" in i and "cryptography" not in i and "!cryptocallout" not in i:	
				await message.channel.send("Crypto means Cryptography!")
				return
			elif i == "c" and message.content.split()[index+1] == "r":
				await message.channel.send("You're really trying to get around the filter? Git\nCRYPTO MEANS CRYPTOGRAPHY!!!!")
				return


@bot.command()
async def cryptocallout(ctx):
	await ctx.send("Crypto means Cryptography!")


#@bot.command()
#async def welcome(ctx):
#	await ctx.send("""
#Hello there! :wave:

#Welcome to the Abertay Ethical Hacking Society Discord! :woman_technologist::man_technologist:

#You should have already been assigned an appropriate role by the bot when you joined; however, if this is not the case then you must first be assigned an appropriate role before gaining access to associated channels. If the bot hasn't assigned you roles (or has made a mistake) please reach out to one of our <@&722774983058784277> members via private message :slight_smile:

#Each role corresponds to a unique colour, so make sure to request the one appropriate for you!
 
#      Role - Colour 
#:red_circle: Committee - Pink 
#:blue_circle: Society Member - Blue 
#:green_circle: Fresher - Green 
#:orange_circle: Graduate - Orange 
#:purple_circle: Abertay Staff - Purple 

#To ensure all members of the Discord are part of the Abertay Ethical Hacking Society community, we request you use an easily identifiable alias (i.e. first name, initials, handle). Hopefully, this will help provide a more welcoming atmosphere, allowing community members to get to know you better.

#Before you join the server, make sure you have reviewed the rules outlined in <#722780450476785735> :pencil:. By joining you are agreeing to follow these rules and guidelines. Anyone found to be in violation of these rules will face the consequences set forth in the Abertay Ethical Hacking Society constitution, which can be found here: https://wiki.hacksoc.co.uk/newconstitution. 

#Here are some other ways you can keep up to date with the Abertay Ethical Hacking Society: 
#:bird: Twitter: @AbertayHackers :bird: 
#:desktop: Website: <https://www.hacksoc.co.uk> :desktop:""")



#Rules
@bot.command()
async def rules(ctx):
	with open("strings/rules.json", "r") as data:
		rules=json.load(data)
	rulesList = ""
	for index, value in enumerate(rules[1::]):
		rulesList += f"__**Rule {index+1}:**__ {value}\n\n"

	rulesList += f"Anyone found to be in violation of these rules will face the consequences set forth in the Abertay Ethical Hacking constitution which can be found here: {rules[0]}"
	embed = discord.Embed(colour=discord.Colour.green(), title="Abertay Hackers Rules", description=rulesList)
	await ctx.send(embed=embed)

#@bot.command()
#async def rule(ctx, ruleNum=None):
#	if not ruleNum:
#		await ctx.send("You haven't specified a rule number. Maybe you're looking for `!rules`?")
#		return
	
#	try:
#		ruleNum = int(ruleNum)
#	except:
#		await ctx.send("In what world is that an integer...?")
#		return

#	with open("strings/rules.json") as data:
#		rules=json.load(data)

#	if ruleNum > len(rules)-1:
#		await ctx.send(f"There are only {len(rules) - 1} rules... Thank God")
#		return
#	elif ruleNum < 1:
#		await ctx.send(f"You really want me to send rule number {ruleNum}? Think about this for a second...")
#		return

#	await ctx.send(f"__Rule {ruleNum}:__ ```{rules[ruleNum]}```")

if __name__ == "__main__":
	with open("token") as data:
		token = data.read()

	bot.run(token)
