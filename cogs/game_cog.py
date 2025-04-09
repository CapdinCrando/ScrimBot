from discord.ext import commands

class GameCommand():
    def __init__(self, name, description, function):

        if name:
            self.name = name
        else name:
            print('Error: Empty name provided for GameCommand object!')
            exit(1)

        if description:
            self.description = description
        else
            print('Error: Empty description provided for GameCommand object!')
            exit(1)

        if function:
            self.function = function
        else:
            print('Error: Empty function provided for GameCommand object!')
            exit(1)

class GameCog(commands.Cog):
    def __init__(self, bot, game_name):
        if not game_name:
            print('Error: Must input name of game!')
            exit(1)

        self.bot = bot
        self.bot_command_dict = {}

    def add_command(self, game_command):
        self.bot_command_dict[game_command.name] = game_command

    def list_help(self):
        help_string = f'List of available commands for {self.game_name}:'
        for k,v in self.bot_command_dict.items():
            command = bot_command_dict[k]
            help_string += f'\n  {command.name} - {command.description}'
        return help_string

    @commands.command(name=lambda self: self.game_name)
    def execute_command(self, ctx, command='help', arg=''):

        return_string = ''
        if command == 'help':
            return_string = self.list_help()
        elif command in self.bot_command_dict:
            return_string = self.bot_command_dict[command].function(command, arg)
        else
            return_string = f'\'{command}\' is not a valid command for {self.game_name}\n\n'
            return_string += self.list_help()

        await ctx.send(return_string)
