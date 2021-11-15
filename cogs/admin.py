import discord, re, qrcode
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
from io import BytesIO

cleanID = lambda x: re.sub("[^0-9]", "", x)

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
        aliases=["rule"]
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
        invite = await channel.create_invite(max_age=0)
        await ctx.send(invite)
        conn.manualInvite(invite.code, target)


    @commands.command(name="perma", description=formatHelp("perma", "desc"), usage=formatHelp("perma", "usage"))
    async def perma(self, ctx, target=None):
        channel = self.bot.get_channel(getEnv("channel", "welcome"))
        roles, roleList = getAvailableRoles()
        #Validate input
        if target not in roles:
            await ctx.send(getResponse("error", "invalidInviteRole").format(target=target, roleList=roleList))
            return

        conn = SignupConn()
        invite = await channel.create_invite(max_age=0, max_uses=0)
        conn.storePerma(invite.code, target)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2
        )
        qr.add_data(invite)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        with BytesIO() as imgBin:
            img.save(imgBin, "PNG")
            imgBin.seek(0)
            await ctx.send(invite)
            await ctx.send(file=discord.File(fp=imgBin, filename="image.png"))

    @commands.command(name="delPerma", description=formatHelp("delPerma", "desc"), usage=formatHelp("delPerma", "usage"))
    async def delPerma(self, ctx, code=None):
        conn = SignupConn()
        code = str(code)
        if not conn.delPerma(str(code)):
            await ctx.send(f"No invites found with the code: `{code}`")
        else:
            for i in await ctx.guild.invites():
                if i.code == code:
                    await i.delete()
            await ctx.send(f"Invite deleted")

    @commands.command(name="listPermaInvites", description=formatHelp("listPermaInvites", "desc"), usage=formatHelp("listPermaInvites", "usage"))
    async def listPermaInvites(self, ctx):
        conn = SignupConn()
        invites = conn.getPermaInvites(withPerms=True)
        if len(invites) == 0:
            await ctx.send("No perma invites")
            return
        embed = discord.Embed(title="List of Perma Invites:")
        for i in invites:
            embed.add_field(name="​", value=f"""**Code:** `{i[0]}`\n**Type:** {i[1].capitalize()}""", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="getInviteQR", description=formatHelp("getInviteQR", "desc"), usage=formatHelp("getInviteQR", "usage"))
    async def getInviteQR(self, ctx, code=None):
        if not code:
            await ctx.send("No code provided")
            return
        
            
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2
        )
        qr.add_data(f"https://discord.gg/{code}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        with BytesIO() as imgBin:
            img.save(imgBin, "PNG")
            imgBin.seek(0)
            await ctx.send(file=discord.File(fp=imgBin, filename="image.png"))

    @commands.command(name="updateuser", description=formatHelp("updateuser", "desc"), usage=formatHelp("updateuser", "usage"))
    async def updateuser(self, ctx, target="", role=None):
        roles, roleList = getAvailableRoles()
        if role not in roles:
            await ctx.send(getResponse("error", "invalidInviteRole").format(target=target, roleList=roleList))
            return 

        target = cleanID(target)
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
        if not currentRole:
            await ctx.send(getResponse("error", "memberPredatesRoleManagement").format(config["prefix"], user.id, role))
            return
        elif currentRole == role:
            await ctx.send(getResponse("error", "newRoleSameAsCurrent"))
            return
        conn.updateUserRole(target, role)
        
        for i in config["perms"][currentRole]:
            await user.remove_roles(getRole(self.bot, i))
        for i in config["perms"][role]:
            await user.add_roles(getRole(self.bot, i))

        await ctx.send(getResponse("success","userRolesUpdated"))

    @commands.command(name="adduser", description=formatHelp("adduser", "desc"), usage=formatHelp("adduser", "usage"))
    async def adduser(self, ctx, userID = None, role = None):
        roles, roleList = getAvailableRoles()
        if not userID:
            await ctx.send(getResponse("error", "invalidArgument").format("a user ID"))
            return
        elif role not in roles:
            await ctx.send(getResponse("error", "invalidInviteRole").format(target=role, roleList=roleList))
            return
        userID = cleanID(userID)
        if len(userID) < 1:
            await ctx.send(getResponse("error", "invalidArgument").format("a user ID"))
            return
        userID = int(userID)
        user = getGuild(self.bot).get_member(userID)
        if not user:
            await ctx.send(getResponse("error", "invalidUser"))
            return
         
        conn = SignupConn()
        if conn.checkRoleFromID(userID):
            await ctx.send(getResponse("error", "userAlreadyInDB").format(config["prefix"]))
            return

        #Checks done -- add the user
        msg = await ctx.send(getResponse("await", "addingUser"))
        if not conn.manualUserInsert(userID, role):
            await ctx.send(getResponse("error", "manualAddFail"))
            return
        for i in config["perms"]:
            for j in config["perms"][i]:
                await user.remove_roles(getRole(self.bot, j))
        for i in config["perms"][role]:
            await user.add_roles(getRole(self.bot, i))

        await msg.edit(content=getResponse("success", "manualAddSuccess")) 
        

def setup(bot):
    bot.add_cog(Admin(bot))
