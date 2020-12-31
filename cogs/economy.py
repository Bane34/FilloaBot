import random
from typing import Optional
from discord import Color

import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, BadArgument

from cogs.utils.database import *

database = main_db("./database.db")

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context = True
    )
    @cooldown(1, 30, BucketType.user)
    async def farm(self, ctx):
        user = str(ctx.author)
        money = random.randint(200, 600)
        database.add_user_balance(user, money)
        
        await ctx.send(f"Has farmeado esta cantidad de dinero `{money}`")

    @commands.command()
    async def balance(self, ctx, user: Optional[Member]):

        user = user or ctx.message.author
        userStr = str(user)
        embed = Embed(
            title = f"Balance económico [{user.name}]",
            colour = Color(0xFFFFFF)
        )

        if not database.user_exist(userStr):
            await ctx.send("El usuario no existe")
            return 
                
        money = str(database.get_user_balance(userStr))
        bank = str(database.get_user_bank(userStr))

        embed.add_field(name = "_**Cartera**_", value = f"El dinero actual en la cartera de {user.mention} es: **{money}**")
        embed.add_field(name = "-**Banco**_", value = f"El dinero actual en el banco de {user.mention} es : **{bank}**")

        await ctx.send(embed = embed)

    @balance.error
    async def balance_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("El usuario no existe melon")

    @commands.command()
    @cooldown(1, 60, BucketType.user)
    async def steal(self, ctx, target: Optional[Member]):
        if target == None:
            await ctx.send("Tienes que poner al usuario al que quieres robar fetido")
            return

        targetStr = str(target)
        userStr = str(ctx.message.author)
        current_balance = database.get_user_balance(userStr)
        target_balance = database.get_user_balance(targetStr)
        if current_balance < 500 or current_balance == None:
           await ctx.send("No puedes robar dinero hasta que tengas mas de 500 monedas manin")
           return
        if target_balance == 0 or target_balance == None:
            await ctx.send(f"{target.mention} ya está seco")
            return

        probabilidad = random.randint(1, 8)#1/2 of probability to steal, 1/8 to pay and 3/8 to nothing
        if probabilidad <= 4:
            money_to_substract = random.randint(1, target_balance)
            database.exchange_balance(targetStr, userStr, money_to_substract)
            await ctx.send(f"Has robado con exito `{money_to_substract}` de {target.mention}!")
        elif probabilidad == 5:
            money_to_substract = random.randint(1, 500)
            database.exchange_balance(userStr, targetStr, money_to_substract)
            await ctx.send(f"Te han pillado al robar :(\nPagas una multa de `{money_to_substract}` a {target.mention}")
        else:
            await ctx.send(f"Te han pillado al robar :(\nPero {target.mention} te perdonan y no pagas multa.")

        return

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def give(self, ctx, target: Member, cantidad: int or str):
        if target == None:
            await ctx.send("Tienes que poner a quien vas a darle la pasta crack")
            return

        if type(cantidad) == int and cantidad == 0:
            await ctx.send("Tienes que poner la cantidad dinero que quieres dar manin")
            return
        
        targetStr = str(target)
        userStr  = str(ctx.message.author)
        current_balance = database.get_user_balance(userStr)

        if current_balance == 0:
            await ctx.send("No tienes dinero para dar crack")
            return None

        if cantidad == "all" or cantidad == "ALL":
            cantidad = database.get_user_balance(userStr)

        database.exchange_balance(userStr, targetStr, cantidad)
        await ctx.send(f"Le has dado al usuario {target.mention} `{cantidad}` de monedas. Joder, ni que fueras bolsonaro")

        return 0

    @commands.command()
    async def dep(self, ctx, cantidad):
        userStr = str(ctx.message.author)
        print("Tratando de depositar dineros")
        if cantidad == 0:
            await ctx.send("A ver manin, vas a depositar 0 dineros en tu cuenta?")
            return
        
        database.add_bank(userStr, cantidad)
        print("Dineros depositados")

        await ctx.send(f"Has depositado {cantidad} en tu cuenta de banco. Momento bolsonaro")
        return

    async def with(self, ctx, cantidad):
        userStr = str(ctx.message.author)
        print("Tratando de susbtraer dineros")
        if cantidad == 0:
            await ctx.send("A ver manin, vas a sacar de tu cuena 0 dineros?")
            return

        database.substract_bank(userStr, cantidad)
        database.add_user_balance(userStr, cantidad)
        print("Dineros sacados de la cuenta")
        await ctx.send(f"Has sacado de tu cuenta {cantidad} dineros, ten cuidado que no te lo roben manin")
        return

def setup(bot):
    bot.add_cog(Economy(bot))