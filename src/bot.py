## ScrimBot
# Made for the DeathSquad and CMT Discord Servers by CapdinCrando
# Has many useful features, such as team selection and name changing
# Licensed under the GNU General Public License v3.0

## Imports
# Local
from bot_config import bot_config

# Discord
import discord
from discord.ext import commands

# Third Party
import asyncio

## Create intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

## Bot Setup
bot = commands.Bot(command_prefix='!', intents = intents)

# If debug mode enabled, relay errors
if bot_config.debug_mode:
    @bot.event
    async def on_command_error(ctx, error):
        await ctx.send(f'Error {error}')

## Add bot modules
async def load_extensions():
    '''
    Goes through the module list from the config and loads
    the ones that have the 'enabled' field set to 'true'.
    '''

    # Go through module list and, if enabled, load modules
    for bot_module_name, bot_module_config in bot_config.modules.items():
        if bot_module_config.enabled:
            await bot.load_extension(f'modules.{bot_module_name}')

## Main function
async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_config.bot_id)

## Turn on the bot
asyncio.run(main())
