import discord, threading, waitress
from discord.ext import commands
from libs.loadconf import config, formatHelp
from inviteSite.app import app


class Site(commands.Cog):
    def __init__(self, bot):
        #thread = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=8080))
        thread = threading.Thread(target=lambda: waitress.serve(app, host="127.0.0.1", port=8080))
        thread.setDaemon(True)
        thread.start()

def setup(bot):
    bot.add_cog(Site(bot))
