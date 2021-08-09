import discord, threading, waitress, os
from discord.ext import commands
from libs.loadconf import config
from inviteSite.app import app


class Site(commands.Cog):
    def __init__(self, bot):
        if os.environ.get("DEV"):
            thread = threading.Thread(target=lambda: app.run(host=config['site']['host'], port=config['site']['port']))
        else:
            thread = threading.Thread(target=lambda: waitress.serve(app, host=config['site']['host'], port=config['site']['port']))
        thread.setDaemon(True)
        thread.start()

def setup(bot):
    bot.add_cog(Site(bot))
