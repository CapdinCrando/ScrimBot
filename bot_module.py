from bot_config import bot_config
import attrs
from discord.ext import commands

@attrs.define
class Cog(commands.Cog):

    module_name: str
    bot: commands.Bot

    def init_module(self):
        None

    def __attrs_post_init__(self):
        self.init_module()

    def get_resource_path(self, resource_name):
        return f'resource/{self.module_name}/{resource_name}'

    @classmethod
    def add_to_bot(cls, module_name, bot):
        get_module_config = bot_config.get_module_config(cls.module_name)
        module_cog = cls(module_name, bot, get_module_config)
        bot.add_cog(module_cog)

