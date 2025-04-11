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
from pyairtable import Table

## Module
class QuoteCommands(bot_module.Module):
    '''QuoteCommands module

    Adds commands for retrieving and adding quotes.
    '''

    # Module fields
    airtable_api_key: str
    airtable_base_id: str
    airtable_table_name: str
    add_quote_form_link: str

    def init_module(self):

        # Get table and store table cache
        self.quote_table = Table(self.airtable_api_key, self.airtable_base_id, self.airtable_table_name)
        self.table_cache = self.quote_table.all()
        self.is_csv_dirty = True
        self.csv_file_mutex = threading.Lock()
        self.table_mutex = threading.Lock()

    def get_table_cache(self):
        '''get_table_cache function

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

    @commands.command()
    async def quote(self, ctx: commands.Context, arg: str = ''):
        """!quote command

        The quote command has several sub commands to access the quote api.
        """

        if arg is '':

            # Choose and send random quote
            fields = choice(self.get_table_cache())['fields']
            quote = fields['Quote']
            if 'Author' in fields:
                quote += '\n\t- ' + fields['Author']
            await ctx.send(quote, tts=True)

        elif arg is 'add':

            # Send quote form link
            await ctx.send(self.add_quote_form_link)

        elif arg is 'update':

            # Update the local quote cache from the remote database

            # Lock mutex
            self.table_mutex.acquire()

            # Try finally to prevent error from not freeing the mutex
            try:
                # Update quote cache
                self.table_cache = self.quote_table.all()

            finally:

                # Unlock mutex
                self.table_mutex.release()

            # Since quotes cache has been updated, the quotes csv is
            # now out of date and must be marked dirty
            self.is_csv_dirty = True

        elif arg is 'all':

            # Get csv with all quotes and upload it
            # Uses a mutex to prevent file read while writing
            self.csv_file_mutex.acquire()

            # Try finally to prevent error from not freeing the mutex
            try:
                quote_csv_filename = 'all_quotes.csv'

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

        else:

            # Send help message with all quote sub-commands
            help_msg =  '!quote - Get a random funny quote!\n' + \
                        '!quote add - Display link to add a new quote\n' + \
                        '!quote all - Get a CSV file with all quotes!\n' + \
                        '!quote help - List quote commands\n' + \
                        '!quote update - Update the local quote cache'
            await ctx.send(help_msg, tts=True)

async def setup(bot: commands.Bot):
    await QuoteCommands.add_to_bot('quote', bot)
