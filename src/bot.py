## ScrimBot
# Made for the DeathSquad Discord Server by CapdinCrando
# Has many useful features, such as team selection and name changing
# Licensed under the GNU General Public License v3.0

## Imports
import discord
from discord.ext import commands

import asyncio
from bot_config import bot_config

## Create intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

## Bot Setup
bot = commands.Bot(command_prefix='!', intents = intents)

## Add bot modules
async def load_extensions():
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
