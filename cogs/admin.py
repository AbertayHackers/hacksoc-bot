import discord, re
from discord.ext import commands
from libs.loadconf import (
    config,
    strings,
    formatHelp,
    getResponse,
    getAvailableRoles,
    LoadRules,
    getGuild,
    getEnv,
    getRole,
)
from libs.db import SignupConn
from libs.colours import Colours


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Check for Committee Role
    async def cog_check(self, ctx):
        committee = discord.utils.get(ctx.guild.roles, name="Committee")
        if not committee in ctx.author.roles:
            Colours.warn(f"{ctx.message.author} tried to use an admin command")
            await ctx.send(getResponse("error", "improperPermissions"))
            return False
        return True

    @commands.command(
        name="rules",
        description=formatHelp("rules", "desc"),
        usage=formatHelp("rules", "usage"),
        aliases=["rule"],
    )
    async def rules(self, ctx, ruleNum=None):
        rules = LoadRules()
        if not ruleNum:
            rulesList = ""
            for index, value in enumerate(rules.rules, start=1):
                rulesList += f"__**{rules.ruleWord} {index}:**__ {value}\n\n"

            rulesList += rules.footer
            embed = discord.Embed(
                colour=discord.Colour.green(), title=rules.title, description=rulesList
            )
            await ctx.send(embed=embed)
            return

        # Assume a specific rule has been requested
        try:
            ruleNum = int(ruleNum)
        except:
            await ctx.send(getResponse("error", "notAnInt"))
            return

        if ruleNum > rules.getNumRules():
            await ctx.send(
                getResponse("error", "ruleOutOfBounds").format(rules.getNumRules())
            )
            return
        elif ruleNum < 1:
            await ctx.send(getResponse("error", "ruleLessThanZero").format(ruleNum))
            return

        await ctx.send(rules.getRule(ruleNum))

    @commands.command(
        name="welcome",
        description=formatHelp("welcome", "desc"),
        usage=formatHelp("rules", "usage"),
    )
    async def welcome(self, ctx, messageID=None):
        rulesChannel = getEnv("channel", "rules")
        channel = self.bot.get_channel(getEnv("channel", "welcome"))
        committeeRole = getRole(self.bot, "Committee")
        with open("prewrittenText/welcome.txt") as msg:
            if not messageID:
                await channel.send(
                    msg.read().format(
                        rulesChannel=rulesChannel,
                        committeeRole=committeeRole.mention,
                        constitution=strings["links"]["constitution"],
                        site=strings["links"]["site"],
                    )
                )
            else:
                try:
                    message = await channel.fetch_message(messageID)
                    await message.edit(
                        content=msg.read().format(
                            rulesChannel=rulesChannel,
                            committeeRole=committeeRole.mention,
                            constitution=strings["links"]["constitution"],
                            site=strings["links"]["site"],
                        )
                    )
                    await ctx.send("Updated the welcome message")
                except Exception as e:
                    await ctx.send(f"Couldn't edit the message: `{e}`")


    @commands.command(name="invite", description=formatHelp("invite", "desc"), usage=formatHelp("invite", "usage"))
    async def invite(self, ctx, target=None):
        channel = self.bot.get_channel(getEnv("channel", "welcome"))
        roles, roleList = getAvailableRoles()
        #Validate input
        if target not in roles:
            await ctx.send(getResponse("error", "invalidInviteRole").format(target=target, roleList=roleList))
            return
    
        #Get an ORM session
        conn = SignupConn()
        #Gen the invite
        invite = await channel.create_invite(max_age=1800)
        await ctx.send(invite)
        conn.manualInvite(invite.code, target)

    @commands.command(name="updateuser", description=formatHelp("updateuser", "desc"), usage=formatHelp("updateuser", "usage"))
    async def updateuser(self, ctx, target="", role=None):
        roles, roleList = getAvailableRoles()
        if role not in roles:
            await ctx.send(getResponse("error", "invalidInviteRole").format(target=target, roleList=roleList))
            return 

        target = re.sub("[^0-9]", "", target)
        if len(target) < 1:
            await ctx.send(getResponse("error", "invalidArgument").format("a user ID"))
            return
        target = int(target)
        try:
            user = getGuild(self.bot).get_member(target)
        except:
            await ctx.send(getResponse("error", "invalidUser"))
            return

        conn = SignupConn()
        currentRole = conn.checkRoleFromID(target)
        if currentRole == role:
            await ctx.send(getResponse("error", "newRoleSameAsCurrent"))
            return
        conn.updateUserRole(target, role)
        
        for i in config["perms"][currentRole]:
            await user.remove_roles(getRole(self.bot, i))
        for i in config["perms"][role]:
            await user.add_roles(getRole(self.bot, i))

        await ctx.send(getResponse("success","userRolesUpdated"))
        

def setup(bot):
    bot.add_cog(Admin(bot))
