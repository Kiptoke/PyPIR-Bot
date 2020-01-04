# Python Price is Right (PyPIR) Bot 
# Version 0.1

# by Andrew Zhou (Kiptoke)

import logging
import discord
import os
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# MAIN BODY CODE

load_dotenv()

bot = commands.Bot(command_prefix='$')
token = os.getenv('DISCORD_TOKEN')

guesses = {}

gameActive = False
channel = 0

title = ''
price = ''

@bot.event
async def on_ready():
    print('Waking up! Hello world!')

@bot.command(name = 'init')
async def initialize(ctx):
    global gameActive

    print("initialize called")

    await ctx.send("Hello there! Let's play the Price is Right!")
    await ctx.send(ctx.author.mention + " will send me an Amazon product link - you all will try to guess what its price is!")

    global channel
    channel = ctx.message.channel
    print(channel)

    await ctx.author.send("Please send me an Amazon link!")
    await ctx.author.send("Type `$link [amazon url]`")

    gameActive = True

    pass

@bot.command(name = 'link')
async def link(ctx, url):
    print(url)
    if(ctx.message.channel.type == discord.ChannelType.private):
        global title
        global price

        user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

        page = requests.get(url,headers=user_agent)
        print(page.status_code)
        soup = BeautifulSoup(page.content,'html.parser')
        soup2 = BeautifulSoup(soup.prettify(),"html.parser")

        title = soup2.find(id="productTitle")
        title = title.get_text().strip()

        price = soup2.find(id="price_inside_buybox")
        price = float(price.get_text().strip()[1:])

        await ctx.send("Alright! Let's play \"The Price is Right\" with this item and price:")
        await ctx.send(title)
        await ctx.send(str(price))

        print("game started:")
        print(title)
        print(str(price))

        await channel.send(ctx.author.mention + " has sent me a link! Let's play!")
        await channel.send("The item in question is the: ")
        await channel.send("**" + title + "**")
        await channel.send("Type `$guess [number]` to make a guess!")

    else:
        await ctx.send("Hey " + ctx.author.mention + ", that's not where the link goes!")
        await ctx.send("Type `$link` with your amazon link in a direct message to me!")
        await ctx.send("*PS: you should probably pick a different link...*")


@bot.command(name = 'guess')
async def make_guess(ctx, input):
    global gameActive
    global guesses

    if(ctx.message.channel == channel):
        if gameActive:
            print(ctx.author.name + " guess = " + input)
            guesses[ctx.author] = float(input)
        else:
            await ctx.send("Game not active! Type `$init` to start!")

    pass

@bot.command(name = 'stop')
async def stop_game(ctx):
    global gameActive
    global guesses
    global price

    closest = 0.0
    closestUser = ''

    if(ctx.message.channel == channel):
        if gameActive:
            for user in guesses:
                print("user: " + user.name + " guess: " + str(guesses[user]))
                if(guesses[user] > closest and guesses[user] <= price):
                    closest = guesses[user]
                    closestUser = user.mention

            await ctx.send(closestUser + " wins with a guess of " + str(closest))
            await ctx.send("The correct price was: " + str(price))
        else:
            await ctx.send("Game not active! Type `$init` to start!")

    pass

@bot.command(name = "rules")
async def rules(ctx):
    string = """
    **How to Play:** ***Python Price is Right***\n
One person will initiate PyPIR Bot (that's me) and will submit an Amazon product.
You'll then be told what that product is. Your goal is to guess how much it costs to buy it.
However, you **cannot** guess above the actual price of the product, or else you lose.
    """

    await ctx.send(string)

    pass

@bot.command(name = 'cmds')
async def commands(ctx):
    string = """
    ----------**PyPIR BOT COMMANDS**----------\n
`$init` - begins a session of the Price is Right
`$link [amazon url]` - sends me an Amazon product link (in DM only)
`$guess [number]` - Make a guess
`$cmds` - Lists all commands.
`$rules` - Prints out the rules of Python Price is Right.
`$stop` - Ends the guessing period, and calculates a winner.
    """

    await ctx.author.send(string)

    pass

bot.run(token)