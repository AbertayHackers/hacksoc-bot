import discord, threading, waitress
from discord.ext import commands
from libs.loadconf import config
from inviteSite.app import app


class Site(commands.Cog):
    def __init__(self, bot):
        #thread = threading.Thread(target=lambda: app.run(host=config['site']['host'], port=config['site']['port']))
        thread = threading.Thread(target=lambda: waitress.serve(app, host=config['site']['host'], port=config['site']['port']))
        thread.setDaemon(True)
        thread.start()

def setup(bot):
    bot.add_cog(Site(bot))
