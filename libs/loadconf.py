import json

#Open all the config files
with open("config/secrets.json") as secretData,\
	 	open("config/config.json") as configData,\
	 	open("config/contributors.json") as contribData,\
	 	open("config/strings.json") as stringData:
	secrets = json.load(secretData)
	config = json.load(configData)
	strings = json.load(stringData)
	contributors = json.load(contribData)


def formatHelp(cmd, arg, lang="en"):
	return strings[lang]["help"][cmd][arg].format(config["prefix"])
