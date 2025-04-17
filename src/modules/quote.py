## Imports
# Local
import bot_module

# Discord
import discord
from discord.ext import commands

# Third Party
import csv
import threading
from random import choice
from pyairtable import Api

## Module
class QuoteCommands(bot_module.Module):
    '''Commands for retrieving and adding quotes.'''

    # Set module name
    __cog_name__ = 'QuoteCommands'

    # Module settings
    airtable_api_token: str
    airtable_base_id: str
    airtable_table_name: str
    add_quote_form_link: str

    def init_module(self):

        # Get table and store table cache
        self.api = Api(self.airtable_api_token)
        self.quote_table = self.api.table(self.airtable_base_id, self.airtable_table_name)
        self.table_cache = self.quote_table.all()
        self.is_csv_dirty = True
        self.csv_file_mutex = threading.Lock()
        self.table_mutex = threading.Lock()

    def get_table_cache(self):
        '''
        Helper function that utilizes a mutex to ensure
        table_cache is not affected by race conditions.
        '''

        # Lock mutex
        self.table_mutex.acquire()

        # Get cache
        table_cache = self.table_cache

        # Unlock mutex
        self.table_mutex.release()

        # Return cache
        return table_cache

    @commands.group()
    async def quote(self, ctx: commands.Context):
        '''Access the quote api.

        Use !quote to pick a random funny quote!'''

        # Skip this command when subcommands used
        if ctx.invoked_subcommand is None:

            # Get quote data
            fields = choice(self.get_table_cache())['fields']
            quote = fields['Quote']
            author = fields['Author']
            year = fields['Year']

            # Build and send quote
            full_quote = f'> {quote}'
            if author:
                full_quote += f'\n>\t— {author}, *{str(year)}*'
            await ctx.send(full_quote, tts=True)

    @quote.command()
    async def add(self, ctx: commands.Context):
        '''Show link to form to add a new quote'''

        # Send quote form link
        await ctx.send(f'Please send in new quotes with the following form:\n{self.add_quote_form_link}')

    @quote.command()
    async def update(self, ctx: commands.Context):
        '''Update the local quote cache from the remote database'''

        # Lock mutex
        self.table_mutex.acquire()

        # Try finally to prevent error from not freeing the mutex
        try:

            # Update quote cache
            self.table_cache = self.quote_table.all()
            update_msg = 'Local quote cache updated!'

        except:

            # Log error
            update_msg = 'Local quote cache failed to update!'

        finally:

            # Unlock mutex
            self.table_mutex.release()

        # Since quotes cache has been updated, the quotes csv is
        # now out of date and must be marked dirty
        self.is_csv_dirty = True

        # Send status update
        await ctx.send(update_msg)

    @quote.command()
    async def all(self, ctx: commands.Context):
        '''Get a CSV file with all quotes'''

        # Get csv with all quotes and upload it
        # Uses a mutex to prevent file read while writing
        self.csv_file_mutex.acquire()

        # Try finally to prevent error from not freeing the mutex
        try:
            quote_csv_filename = self.get_cache_file_path('all_quotes.csv')

            # Check if csv has not been updated since last
            if self.is_csv_dirty:
                table_cache = self.get_table_cache()
                headers = list(table_cache[0]['fields'].keys())
                with open(quote_csv_filename, "w",newline='', encoding='utf-8') as out_file:
                    writer = csv.DictWriter(out_file, fieldnames=headers)
                    writer.writeheader()
                    for quote in table_cache:
                        writer.writerow(quote['fields'])

                # Since quote csv have been updated, no longer dirty
                self.is_csv_dirty = False
            await ctx.send(file=discord.File(quote_csv_filename))

        finally:
            # Unlock mutex
            self.csv_file_mutex.release()

async def setup(bot: commands.Bot):
    await QuoteCommands.add_to_bot('quote', bot)
