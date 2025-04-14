## Imports
# Local
import bot_module

# Discord
import discord
from discord.ext import commands

# Third Party
from os import urandom
from base64 import b64encode
from random import choice

## Module
class UserCommands(bot_module.Module):
    '''Commands regarding specific users.'''

    # Module fields
    chin_id: int
    wizard_id: int
    stinky_id: int
    stinky_lines: list[str]

    @commands.command()
    async def chinsignal(self, ctx: commands.Context):
        '''Call the Crimson Chin to action!'''
        await ctx.send(f"Calling <@{ self.chin_id }>!",
                       file=discord.File(self.get_resource_path('chin_signal.PNG')))

    @commands.command()
    async def noballs(self, ctx: commands.Context):
        '''Challenge the Crimson Chin's honor!'''
        await ctx.send(f"<@{ self.chin_id }>\'s Honor has been challenged!")

    @commands.command()
    async def stinky(self, ctx: commands.Context):
        '''Call out the smell of a certain person.'''
        stinky_line = choice(self.stinky_lines)
        await ctx.send(f"<@{ self.stinky_id }> {stinky_line}")

    @commands.command()
    async def QjmschLizoardQjmschWizoard(self, ctx: commands.Context):
        '''Generate a new Discord name for the Lizard Wizard.'''
        name = b64encode(urandom(24)).decode('utf-8')
        await ctx.send(f'<@{self.wizard_id}>\'s new Discord nickname is {str(name)}')

async def setup(bot: commands.Bot):
    await UserCommands.add_to_bot('user', bot)
