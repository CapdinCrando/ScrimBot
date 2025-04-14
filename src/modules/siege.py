## Imports
# Local
import bot_module

# Discord
from discord.ext import commands

# Third Party
import os
import json
from random import randint, choice

## Module
class SiegeCommands(bot_module.Module):
    '''Commands for Rainbow Six: Siege.'''

    # Set module name
    __cog_name__ = 'Siege Commands'

    def init_module(self):

        # Initialize attack and defense strategy lists
        with open(self.get_resource_path('strats.json', 'r')) as strat_file:
            self.strat_data = json.load(strat_file)

        random_file_name = self.get_resource_path('operators.json')

        ## Read config file
        if(not os.path.exists(random_file_name)):
            print('[WARNING] {} does not exist!'.format(random_file_name))
            exit(1)

        operator_file_data = open(random_file_name)
        operator_json = json.load(operator_file_data)

        self.attackers = operator_json['attackers']
        self.defenders = operator_json['defenders']

        ## Check lengths
        if(not self.attackers):
            print('[WARNING] No attackers defined!')
            exit(1)
        if(not self.defenders):
            print('[WARNING] No defenders defined!')
            exit(1)

    def getAttackers(self):
        usedOps = []   # Array to keep track of operators already used
        msg = "Generated 5 Random Attackers:\n\n"
        attackerCount = len(self.attackers)
        for i in range(5):
            operatorIdx = randint(0,attackerCount-1)   # Get random operator index (priming read)
            while(operatorIdx in usedOps):   # Has this operator been used already?
                operatorIdx = randint(0,attackerCount-1)   # If yes, get new random operator index
            usedOps.append(operatorIdx)   # Add operator to list of used operators
            attackerName = self.attackers[operatorIdx]   # Get name of the operator
            msg += "\t- " + attackerName + '\n'

        return msg

    def getDefenders(self):
        usedOps = []   # Array to keep track of operators already used
        msg = "Generated 5 Random Defenders:\n\n"
        defenderCount = len(self.defenders)
        for i in range(5):
            operatorIdx = randint(0,defenderCount-1)   # Get random operator index (priming read)
            while(operatorIdx in usedOps):   # Has this operator been used already?
                operatorIdx = randint(0,defenderCount-1)   # If yes, get new random operator index
            usedOps.append(operatorIdx)   # Add operator to list of used operators
            defenderName = self.defenders[operatorIdx]   # Get name of the operator
            msg += "\t- " + defenderName + '\n'

        return msg

    def getStrat(self, type: str):

        # Pick strat
        strat = choice(self.strat_data[type])

        # Build strat string
        strat_string = f"**{ type.capitalize() }: { strat['stratName'] }**\n- \"*{ strat['quote'] }*\"\n- { strat['teamName'] }"
        if len(strat) == 4:
            strat_string += ":"
            for member in strat['teamMembers']:
                strat_string += f"\n\t- { member }"

        return strat_string

    @commands.command()
    async def siege(self, ctx: commands.Context):
        '''Game commands for Rainbow Six: Siege'''
        pass

    @siege.command()
    async def random(self, ctx: commands.Context, type: str ='both'):
        '''Generate 5 random attackers or defenders. Include "attack" or "defend" to only generate for one side.'''

        pick_string = ''
        if(type == 'attack'):
            pick_string += self.getAttackers()

        elif(type == 'defend'):
            pick_string += self.getDefenders()

        elif(type == 'both'):
            pick_string += self.getAttackers()
            pick_string += '\n\n'
            pick_string += self.getDefenders()

        else:
            await ctx.send('Please use command with "attack", "defend", or "both".')
            return

        # Send string if has content
        if(pick_string):
            await ctx.send(pick_string)

    @siege.command()
    async def strat(self, ctx: commands.Context, type=''):
        '''Generate a random strat. Must include either "attack" or "defense" as an argument.'''

        valid_types = list(self.strat_data.keys())

        strat_string = ''
        if(type in valid_types):
            strat_string += f'Random Strat Generated for {type}:\n\n'
            strat_string += self.getStrat(type)

        else:
            await ctx.send('Please use command with "attack" or "defend"')
            return

        # Send strat string if has content
        if(strat_string):
            await ctx.send(strat_string)

async def setup(bot: commands.Bot):
    await SiegeCommands.add_to_bot('siege', bot)
