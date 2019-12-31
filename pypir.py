# Python Price is Right (PyPIR) Bot 
# Version 0.1

# by Andrew Zhou (Kiptoke)

import logging
import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

class Game():
    def __init__(self):
        self.players = []

    def get_players(self):
        i = 1
        name = ""
        while (name != "start"):
            print("What is the name of player " + str(i) + "?")
            name = input("Name of player " + str(i) + ": ")
            if(name != "start"):
                self.players.append(Player(name))
            i += 1

        for var in self.players:
            print(var.name)

class Player():
    """Class object to store player data"""

    def __init__(self,name):
        """Initialize object with name, points, guess"""
        self.name = name
        self.pts = 0
        self.guess = 0

    def make_guess(self,num):
        self.guess = num

    def update_points(self,num):
        self.pts += num

    def points(self):
        return self.pts

    def name(self):
        return self.name

    def guess(self):
        return self.guess

# MAIN BODY CODE

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='$')
token = os.getenv('DISCORD_TOKEN')

num = 0

@bot.event
async def on_ready():
    print('Waking up! Hello world!')

#@client.event
#async def on_message(message):
# if not message.author.bot:
#     if message.content.startswith(':0'):
#         await message.channel.send('0:')
#     elif message.content.startswith('0:'):
#         await message.channel.send(':0')

@bot.command(name = 'init')
async def initialize(ctx):
    print("initialize called")
    await ctx.send("Hello there! Let's play a game!")
    await ctx.send("I'm thinking of a number from 1-100. Try guessing what it is!")
    await ctx.send("Type `$guess [number]` to make a guess!")
    global num
    num = random.randint(1,100)
    print(str(num))
    pass

@bot.command(name = 'guess')
async def make_guess(ctx, input):
    print("make_guess called, num = " + str(num) + " guess = " + input)

    if(int(input) > num):
        await ctx.send("Too big! Guess lower!")
    elif(int(input) < num):
        await ctx.send("Too low! Guess higher!")
    else:
        await ctx.send("That's it!")

    pass

bot.run(token)