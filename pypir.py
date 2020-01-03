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

#client = discord.Client()
bot = commands.Bot(command_prefix='$')
token = os.getenv('DISCORD_TOKEN')

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
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="productTitle")
        print(title)
        title = title.get_text().strip()

        #price = soup.find(id="price_inside_buybox")
        #print(price)
        #price = float(price.get_text()[1:])

        await ctx.send("Alright! Let's play \"The Price is Right\" with this item and price:")
        await ctx.send(title)
        #await ctx.send(str(price))

        print("game started:")
        print(title)
        #print(str(price))

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

    print("make_guess called, num = " + str(price) + " guess = " + input)

    if(ctx.message.channel == channel):
        if gameActive:
            if(float(input) > price):
                await ctx.send("Too big! Guess lower!")
            elif(float(input) < price):
                await ctx.send("Too low! Guess higher!")
            else:
                await ctx.send("That's it!")
                gameActive = False
        else:
            await ctx.send("Game not active! Type `$init` to start!")

    pass

@bot.command(name = 'cmds')
async def commands(ctx):
    await ctx.author.send("Testing! Hello there!")
    pass

bot.run(token)