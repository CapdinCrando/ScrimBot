from discord.ext import commands
import bot_module

import os
import json
from random import randint, choice

class SiegeCog(bot_module.Module):

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

    def getStrat(self, type):

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
    async def random(self, ctx, type='both'):
        """!random command

        Generates 5 random attackers or defenders from Siege
        """

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
            await ctx.send('Invalid input! Please input either attack or defend (or don\'t input anything at all)')
            return

        # Send string if has content
        if(pick_string):
            await ctx.send(pick_string)

    @commands.command()
    async def strat(self, ctx, type='all'):
        """!strat command

        Picks a random strategy from a list of strats and displays it.
        Will do either attack, defense, or both.
        """

        valid_types = list(self.strat_data.keys())

        strat_string = ''
        if(type in valid_types):
            strat_string += 'Random Strat Generated:\n\n'
            strat_string += self.getStrat(type)

        elif(type == 'all'):
            strat_string += 'Random Strats Generated:\n\n'
            for stratType in valid_types:
                strat_string += self.getStrat(stratType)
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
    await SiegeCog.add_to_bot('siege', bot)
