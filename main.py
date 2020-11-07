import random, time, json, asyncio
import discord
import re
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from config.variables import *

#Cargar el token del archivo json
with open("token.json") as file:
    data = json.load(file)
token = data['token']

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True
bot = commands.Bot(command_prefix = '?', description = "Bot para diversos propositos")

#Comandos
@bot.command(
    name = "filloas",
    description = "Mustra fotos de filloas",
    brief = "Muestra fotos de filloas aleatorioas, por lo demas, no sirve para nada",
    pass_context = True
)
async def filloas(ctx):
    number = random.randint(0, 2)
    await ctx.send(urls[number])

#Eventos
@bot.event
async def on_ready():
    game = discord.Game("Usa ? para invocar al filloa bot")
    await bot.change_presence(status = discord.Status.idle, activity = game)
    print("Filloa bot encendio")
    print("\nLogged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
<<<<<<< HEAD
    references = json.load(open("config/references.json"))["references"]
    for reference in references:
        if references.search(reference["regex"], message.content) != None:
=======
    references = json.load(open('config/references.json'))["references"]
    for reference in references:
        if re.search(reference["regex"], message.content) != None:
>>>>>>> 85ba6845f12e7c2ceb4f5e38d1e3d59c66bfdfa3
            await message.channel.send(reference["answer"])
            for reaction in reference["reactions"]:
                await message.add_reaction(reaction)
            await bot.process_commands(message)

bot.run(token)