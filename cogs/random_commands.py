from discord.ext import commands

import os
import json
from random import randint

# For future expansion
game = 'games/siege/'

random_file_name = game + 'operators.json'

## Read config file
if(not os.path.exists(random_file_name)):
    print('[WARNING] {} does not exist!'.format(random_file_name))
    exit(1)

operator_file_data = open(random_file_name)
operator_json = json.load(operator_file_data)

attackers = operator_json['attackers']
defenders = operator_json['defenders']

attackerCount = len(attackers)
defenderCount = len(defenders)

## Check lengths
if(not attackers):
    print('[WARNING] No attackers defined!')
    exit(1)
if(not defenders):
    print('[WARNING] No defenders defined!')
    exit(1)

def getAttackers():
    usedOps = []   # Array to keep track of operators already used
    msg = "Generated 5 Random Attackers:\n\n"
    for i in range(5):
        operatorIdx = randint(0,attackerCount-1)   # Get random operator index (priming read)
        while(operatorIdx in usedOps):   # Has this operator been used already?
            operatorIdx = randint(0,attackerCount-1)   # If yes, get new random operator index
        usedOps.append(operatorIdx)   # Add operator to list of used operators
        attackerName = attackers[operatorIdx]   # Get name of the operator
        msg += "\t- " + attackerName + '\n'

    return msg

def getDefenders():
    usedOps = []   # Array to keep track of operators already used
    msg = "Generated 5 Random Defenders:\n\n"
    for i in range(5):
        operatorIdx = randint(0,defenderCount-1)   # Get random operator index (priming read)
        while(operatorIdx in usedOps):   # Has this operator been used already?
            operatorIdx = randint(0,defenderCount-1)   # If yes, get new random operator index
        usedOps.append(operatorIdx)   # Add operator to list of used operators
        defenderName = defenders[operatorIdx]   # Get name of the operator
        msg += "\t- " + defenderName + '\n'
    
    return msg
	
class RandomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx, type='both'):
        """!random command
        
        Generates 5 random attackers or defenders from Siege
        """

        pick_string = ''
        if(type == 'attack'):
            pick_string += getAttackers()
        
        elif(type == 'defend'):
            pick_string += getDefenders()

        elif(type == 'both'):
            pick_string += getAttackers()
            pick_string += '\n\n'
            pick_string += getDefenders()

        else:
            await ctx.send('Invalid input! Please input either attack or defend (or don\'t input anything at all)')
            return

        # Send string if has content
        if(pick_string):
            await ctx.send(pick_string)

async def setup(bot):
    await bot.add_cog(RandomCog(bot))