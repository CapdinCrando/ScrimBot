## Imports
# Local
import bot_module

# Discord
import discord
from discord.ext import commands

# Third Party
from os import urandom
from base64 import b64encode
from random import randint

## Module
class CustomCommands(bot_module.Module):
    '''Adds commands which utilize custom ids, such as user and emote ids.'''

    # Module fields
    chin_id: int
    bigunnn_id: int
    pog_id: str

    @commands.command()
    async def chinsignal(self, ctx: commands.Context):
        '''Call the Crimson Chin to action!'''
        await ctx.send(file=discord.File("chin_signal.PNG"))
        await ctx.send(f"Calling <@{ self.chin_id }>!")

    @commands.command()
    async def noballs(self, ctx: commands.Context):
        '''Challenge the Crimson Chin's honor!'''
        await ctx.send(f"<@{ self.chin_id }>\'s Honor has been challenged!")

    @commands.command()
    async def poggers(self, ctx: commands.Context):
        '''Mimic a large crowd of users spamming the "pog" emoji'''
        PogAmount = randint(5,8)
        for i in range(PogAmount):
            await ctx.send(self.pog_id * randint(1, 10))

    @commands.command()
    async def QjmschLizoardQjmschWizoard(self, ctx: commands.Context):
        '''Change Bigunnn's nickname to a random string of (cryptographically strong) characters'''
        big = ctx.guild.get_member(self.bigunnn_id)
        name = b64encode(urandom(24)).decode('utf-8')
        await big.edit(nick=name)

async def setup(bot: commands.Bot):
    await CustomCommands.add_to_bot('custom', bot)
