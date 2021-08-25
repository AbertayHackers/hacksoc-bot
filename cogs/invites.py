import discord
from discord.ext import commands
from libs.loadconf import config, getGuild, getRole
from libs.db import SignupConn
from libs.colours import Colours


class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        conn = SignupConn()
        permaInvites = conn.getPermaInvites()
        for invite in await getGuild(self.bot).invites():
            if invite.uses > 0:
                code = invite.code
                if code in permaInvites:
                    role = conn.getPermaInviteRole(code)
                    for i in config["perms"][role]:
                        await member.add_roles(getRole(self.bot, i))
                    return

                conn.setUsed(code)
                conn.setDiscordID(member.id, code)
                role = conn.checkRoleFromInvite(code)
                if not role:
                    Colours.warn("Invalid Invite used")
                    return
                for i in config["perms"][role]:
                    await member.add_roles(getRole(self.bot, i))

                await invite.delete()
                break
 

def setup(bot):
    bot.add_cog(Invites(bot))
