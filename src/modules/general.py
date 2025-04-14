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

    # Module fields
    issue_page_link: str

    def init_module(self):

        # Open and load README
        with open('README.md', 'r') as readme_file:
            self.readme_data = readme_file.read()

    @commands.command()
    async def about(self, ctx: commands.Context):
        '''Get general information about ScrimBot'''
        await ctx.send(self.readme_data)

    @commands.command()
    async def list(self, ctx: commands.Context):
        '''Get a list of all available commands.'''
        pass

    @commands.command()
    async def issues(self, ctx: commands.Context):
        '''Get the link to report issues or suggestions regarding ScrimBot.'''
        await ctx.send(f'Please send all ScrimBot issues and suggestions here:\n{self.issue_page_link}')

async def setup(bot: commands.Bot):
    await GeneralCommands.add_to_bot('general', bot)
