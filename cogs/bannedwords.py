import discord
import re
from discord.ext import commands
from libs.loadconf import config, formatHelp



class BannedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if re.match(".*quidd?itch.*", message.content, re.IGNORECASE | re.DOTALL):
            await message.delete()

def setup(bot):
    bot.add_cog(BannedWords(bot))
