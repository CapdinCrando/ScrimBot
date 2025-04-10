## Imports
# Local
from bot_config import bot_config

# Discord
from discord.ext import commands

# Third Party
import attrs

@attrs.define
class Module(commands.Cog):
    '''Module class

    Used as a base for custom bot modules.
    '''

    # Module fields
    module_name: str
    bot: commands.Bot

    def init_module(self):
        '''init_module function

        Initialization function for bot modules. Meant to be overridden.
        '''
        None

    def __attrs_post_init__(self):
        '''__attrs_post_init__ function

        Called by attrs after __init__ is called.
        Used to call custom init_module function.
        '''
        self.init_module()

    def get_resource_path(self, resource_name: str):
        '''get_resource_path function

        Used to get the appropriate resource path for the given module resource.
        '''
        return f'resource/{self.module_name}/{resource_name}'

    @classmethod
    def add_to_bot(cls, module_name: str, bot: commands.Bot):
        '''add_to_bot function

        Used to instantiate a bot module and add it to the bot.
        '''

        get_module_config = bot_config.get_module_config(cls.module_name)
        module_cog = cls(module_name, bot, get_module_config)
        bot.add_cog(module_cog)

