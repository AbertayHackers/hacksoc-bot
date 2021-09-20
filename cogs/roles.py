import discord, asyncio
from discord.ext import commands
from libs.loadconf import config, getResponse, formatHelp


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role", description=formatHelp("role", "desc"), usage=formatHelp("role", "usage"))
    async def role(self, ctx, reqRole=None):
        if not reqRole:
            await ctx.send(getResponse("error", "invalidArgumentOptions").format("\n".join(config["selfAssignables"])))
            return

        try:
            pos = [i.lower() for i in config["selfAssignables"]].index(reqRole.lower())
        except ValueError:
            await ctx.send(getResponse("error", "roleAssignNotAllowed").format(reqRole, "\n".join(config["selfAssignables"])))
            try:
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
                return
            except:
                return


        reqRole = discord.utils.get(ctx.guild.roles, name=config["selfAssignables"][pos])
        if reqRole in ctx.author.roles:
            try:
                await ctx.author.remove_roles(reqRole)
                msg = await ctx.send(getResponse("success", "roleRemoved"))
            except:
                msg = await ctx.send(getResponse("error", "roleOpFailed"))
        else:
            try:
                await ctx.author.add_roles(reqRole)
                msg = await ctx.send(getResponse("success", "roleAdded"))
            except:
                msg = await ctx.send(getResponse("error", "roleOpFailed"))

        try:
            await asyncio.sleep(5)
            await msg.delete()
            await ctx.message.delete()
        except:
            return

def setup(bot):
    bot.add_cog(Roles(bot))
