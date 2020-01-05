# PyPIR-Bot

A bot for Discord that allows server users to play the price guessing game from "The Price is Right" using prices scraped from Amazon product links.

Written using Python 3.8, discord.py, requests, and BeautifulSoup 4

## Commands

`$init` - Begins a session of the Price is Right  
`$link [amazon url]` - Sends the bot an Amazon product link (in DM only)  
`$guess [number]` - Make a guess  
`$cmds` - Lists all commands.  
`$rules` - Prints out the rules of Python Price is Right.  
`$stop` - Ends the current game, and calculates a winner.  