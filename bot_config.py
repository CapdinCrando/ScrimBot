import os
import json

config_file_name = 'config/config.json'

needed_parameters = ['bot_id']
optional_parameters = ['bigunnn_id', 'chin_id', 'pog_id']

class BotConfig():
    def __init__(self):

        ## Read config file
        if(not os.path.exists(config_file_name)):
            print('[WARNING] config.json does not exist!')
            exit(1)

        config_file_data = open(config_file_name)
        config_json = json.load(config_file_data)

        for p in needed_parameters:
            if(p in config_json):
                setattr(self, p, config_json[p])
            else:
                print('[WARNING] bot_id is not defined in config.json!')
                exit(1)

        for p in optional_parameters:
            if(p in config_json):
                setattr(self, p, config_json[p])

## Instantiate Bot Config
bot_config = BotConfig()