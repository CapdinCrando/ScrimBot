## Imports
# Local
import bot_module

# Discord
from discord.ext import commands

# Third Party
from random import choice, randint

## Module
class GeneralCommands(bot_module.Module):
    '''Commands for general bot stuff.'''

    # Set module name
    __cog_name__ = 'General Commands'

    # Module fields
    issue_page_link: str

    def init_module(self):

        # Open and load README
        with open('README.md', 'r') as readme_file:
            self.readme_data = readme_file.read()

    @commands.command
    async def about(self, ctx: commands.Context):
        '''Get general information about ScrimBot'''
        await ctx.send(self.readme_data)

    @commands.command
    async def issues(self, ctx: commands.Context):
        '''Get the link to report issues or suggestions regarding ScrimBot.'''
        await ctx.send(self.issue_page_link)
