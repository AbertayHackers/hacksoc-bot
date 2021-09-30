import discord, re, time as t
from discord.ext import commands
from libs.loadconf import config, formatHelp


time = lambda: int(t.time())

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cryptoLastRun = 0

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot and time() - self.cryptoLastRun > config["cryptoCooldown"] and re.search("crypto(?!( +)?graphy)", msg.content, re.IGNORECASE):
            self.cryptoLastRun = time()
            await msg.reply("Crypto means cryptography!")


def setup(bot):
    bot.add_cog(Crypto(bot))
