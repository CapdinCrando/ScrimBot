import discord
from discord.ext import commands

from os import urandom
from base64 import b64encode
from random import randint

from bot_config import bot_config

class CustomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chinsignal(self, ctx):
        """!chinsignal command

        Sends a picture of the Crimson Chin and calls for a specifed user
        """
        if(hasattr(bot_config, 'chin_id')):
            await ctx.send(file=discord.File("chin_signal.PNG"))
            await ctx.send(f"Calling <@{ bot_config.chin_id }>!")

    @commands.command()
    async def noballs(self, ctx):
        """!noballs command

        Challenges a particular user
        """
        if(hasattr(bot_config, 'chin_id')):
            await ctx.send(f"<@{ bot_config.chin_id }>\'s Honor has been challenged!")
    
    """!poggers Command
    incredibly advanced ai mimics a large crowd of users spamming the 
    "pog" emoji """
    @commands.command()
    async def poggers(self, ctx):
        if(hasattr(bot_config, 'pog_id')):
            PogAmount = randint(5,8)
            for i in range(PogAmount):
                await ctx.send(bot_config.pog_id * randint(1, 10))

    @commands.command()
    async def QjmschLizoardQjmschWizoard(self, ctx):
        """!QjmschLizoardQjmschWizoard command

        Changes a specific user's to a random string of characters
        Fun fact: the random string is cryptographically strong, too!
        """
        if(hasattr(bot_config, 'bigunnn_id')):
            big = ctx.guild.get_member(bot_config.bigunnn_id)
            name = b64encode(urandom(24)).decode('utf-8')
            await big.edit(nick=name)

async def setup(bot):
    await bot.add_cog(CustomCog(bot))