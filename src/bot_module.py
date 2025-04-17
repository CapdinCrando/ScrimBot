## Imports
# Local
from bot_config import bot_config

# Discord
from discord.ext import commands

# Third Party
import os
import attrs

@attrs.define()
class Module(commands.Cog):
    '''Module class

    Used as a base for custom bot modules.
    '''

    # Common Module fields
    module_name: str
    bot: commands.Bot
    _extra_fields: dict

    def init_module(self):
        '''init_module function

        Initialization function for bot modules. Meant to be overridden.
        '''
        None

    def __attrs_post_init__(self):
        '''__attrs_post_init__ function

        Called by attrs after __init__ is called.
        Used to set custom variables and call custom init_module function.
        '''
        # Set cog display name
        self.__cog_name__ = self.module_name.capitalize()

        # Set config items
        for key, value in self._extra_fields.items():
            setattr(self, key, value)

        # Call subclass init
        self.init_module()

    def __hash__(self):
        return hash(self.module_name)

    def get_resource_path(self, resource_name: str):
        '''get_resource_path function

        Used to get the appropriate resource path for the given module resource.
        '''
        return f'resources/{self.module_name}/{resource_name}'
    
    def get_cache_file_path(self, file_name: str):
        cache_folder_path = f'cache/{self.module_name}'
        os.makedirs(cache_folder_path, exist_ok=True)
        return f'{cache_folder_path}/{file_name}'

    @classmethod
    def add_to_bot(cls, module_name: str, bot: commands.Bot):
        '''add_to_bot function

        Used to instantiate a bot module and add it to the bot.
        '''

        module_config = bot_config.get_module_config(module_name)
        module_cog = cls(module_name, bot, module_config)
        return bot.add_cog(module_cog)

