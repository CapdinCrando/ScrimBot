## Imports
# Local
import bot_module

# Discord
from discord.ext import commands

## Module
class MinecraftCommands(bot_module.Module):
    '''Commands for Minecraft.'''

    def init_module():
        pass

    @commands.command()
    async def minecraft(self, ctx: commands.Context):
        '''Status'''
        pass
        
    @minecraft.command()
    async def status(self, ctx: commands.Context, arg):
        if not ctx.author.guild_permissions.administrator:
            ctx.send('This command can only be used by a server admin!')
            return

async def setup(bot: commands.Bot):
    await MinecraftCommands.add_to_bot('minecraft', bot)
