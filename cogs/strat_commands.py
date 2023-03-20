from discord.ext import commands

import json
from random import choice

# For future expansion
game = 'games/siege/'

# Initialize attack and defense strategy lists
with open(game + 'strats.json', 'r') as strat_file:
    strat_data = json.load(strat_file)

def getStrat(type):

    # Pick strat
    strat = choice(strat_data[type])

    # Build strat string
    strat_string = f"**{ type.capitalize() }: { strat['stratName'] }**\n- \"*{ strat['quote'] }*\"\n- { strat['teamName'] }"
    if len(strat) == 4:
        strat_string += ":"
        for member in strat['teamMembers']:
            strat_string += f"\n\t- { member }"

    return strat_string
    

class StratCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def strat(self, ctx, type='all'):
        """!strat command

        Picks a random strategy from a list of strats and displays it.
        Will do either attack, defense, or both.
        """

        valid_types = list(strat_data.keys())

        strat_string = ''
        if(type in valid_types):
            strat_string += 'Random Strat Generated:\n\n'
            strat_string += getStrat(type)

        elif(type == 'all'):
            strat_string += 'Random Strats Generated:\n\n'
            for stratType in valid_types:
                strat_string += getStrat(stratType)
                strat_string += '\n\n'
            
            strat_string = strat_string[:-2]

        else:
            err_string = 'Invalid input! List of valid commands:'
            err_string += '\n- !strat (will display all)'
            for strat in valid_types:
                err_string += '\n- !strat ' + strat
            await ctx.send(err_string)
            return

        # Send strat string if has content
        if(strat_string):
            await ctx.send(strat_string)
	
async def setup(bot):
    await bot.add_cog(StratCog(bot))