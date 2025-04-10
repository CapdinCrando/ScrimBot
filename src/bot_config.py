## Imports
# Third Party
import os
import json
import attrs

config_file_name = 'config/config.json'

@attrs.define
class BotModuleConfig():
    enabled: bool
    config: dict

@attrs.define
class BotConfig():

    bot_id: str
    modules: dict[str, BotModuleConfig]

    def get_module_config(self, module_name: str):
        self.modules.get(module_name, {})

## Read config file
if(not os.path.exists(config_file_name)):
    print('[WARNING] config.json does not exist!')
    exit(1)

with open(config_file_name) as config_file:
    config_json = json.load(config_file)

## Instantiate Bot Config
bot_config = BotConfig(**config_json)
