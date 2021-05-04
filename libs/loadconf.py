import json, discord

#Open all the config files
with open("config/secrets.json") as secretData,\
	 	open("config/config.json") as configData,\
	 	open("config/contributors.json") as contribData,\
	 	open("config/env.json") as envData,\
	 	open("config/strings.json") as stringData:
	secrets = json.load(secretData)
	config = json.load(configData)
	config["env"] = json.load(envData)
	strings = json.load(stringData)
	contributors = json.load(contribData)


def formatHelp(cmd, arg, lang="en"):
	return strings[lang]["commands"][cmd][arg].format(config["prefix"])

def getResponse(resType, res, lang="en"):
	return strings[lang]["responses"][resType][res]

def getEnv(envType, envVal):
	return config["env"][envType][envVal]

def getGuild(bot):
	return bot.get_guild(config["env"]["guild"])

def getRole(bot, roleName):
	return discord.utils.get(getGuild(bot).roles, name=roleName)

class LoadRules():
	def __init__(self, lang="en"):
		self.lang = lang
		self.rules = strings[self.lang]["rules"]["rules"]
		self.title = strings[self.lang]["rules"]["title"]
		self.footer = strings[self.lang]["rules"]["footer"].format(strings["links"]["constitution"])
		self.ruleWord = strings[self.lang]["rules"]["ruleWord"]

	def getRule(self, num):
		return f"**{self.ruleWord} {num}:** {self.rules[num-1]}"

	def getNumRules(self):
		return len(self.rules)	

	
