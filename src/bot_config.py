## Imports
# Third Party
import os
import json
import attr
import attrs

config_file_name = 'config/config.json'

@attrs.define
class BotModuleConfig():
    enabled: bool
    config: dict

@attrs.define
class BotConfig():

    bot_id: str
    debug_mode: bool
    modules: dict[str, BotModuleConfig] = attr.ib(
        converter=lambda d: {
            k: BotModuleConfig(**v) for k,v in d.items()
        }
    )

    def get_module_config(self, module_name: str):
        return self.modules[module_name].config if module_name in self.modules else {}


## Read config file
if(not os.path.exists(config_file_name)):
    print('[WARNING] config.json does not exist!')
    exit(1)

with open(config_file_name) as config_file:
    config_json = json.load(config_file)

## Instantiate Bot Config
bot_config = BotConfig(**config_json)
