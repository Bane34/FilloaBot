import pyjokes

import discord
from discord.ext import commands

class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "chiste",
        description = "Te dice un chiste de programadores. Si el mensaje incluye \"chuck\" o \"norris\" obliga a que la broma sea de Chuck Norris",
        brief = "Chistes de programadores",
        pass_context = True
    )
    async def chiste(self, ctx, extraShit="-"):
        lang="es"
        category = "all"
        # if re.search("chuck|norris", ctx.message.content.lower()):
        #     category = "chuck"
        await ctx.send(pyjokes.get_joke(lang, category))

def setup(bot):
    bot.add_cog(Jokes(bot))