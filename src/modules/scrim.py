## Imports
# Local
import bot_module
from bot_utils import get_nickname

# Discord
from discord.ext import commands
from discord import HTTPException

# Third Party
from math import ceil
from random import randint

## Module
class ScrimCommands(bot_module.Module):
    '''Commands for creating and managing scrim teams.'''

    # Class constants
    invalid_two_person_command_message = 'You and at least one other person must be in a voice channel to use this command!'

    def init_module(self):
        '''
        Initialization function for bot modules.
        '''
        self.team2members = {} # Initialize team members array

    @commands.group()
    async def scrim(self, ctx: commands.Context):
        '''Commands for hosting scrimmage (scrim) matches.

        !scrim will generate two teams from the members in the user's voice channel.'''

        # Skip this command when subcommands used
        if ctx.invoked_subcommand is None:
            channel = ctx.author.voice.channel
            if channel is None:
                ctx.send(self.invalid_two_person_command_message)
            else:
                guild_id = ctx.message.guild.id
                if guild_id in self.team2members:
                    del self.team2members[guild_id]
                self.team2members[guild_id] = {}
                self.team2members[guild_id]['members'] = []
                members = channel.members

                team_max = ceil(len(members)/2)
                size1 = 0
                size2 = 0
                s = 0

                team1 = "Team 1:\n"
                team2 = "Team 2:\n"
                for member in members:
                    if(s == 0):
                        r = randint(0, 1)
                        if(r == 0):
                            team1 += "* " + str(get_nickname(member)) + "\n"
                            size1 += 1
                            if(size1 == team_max): s = 1
                        else:
                            team2 += "* " + str(get_nickname(member)) + "\n"
                            self.team2members[guild_id]['members'].append(member)
                            size2 +=1
                            if(size2 == team_max): s = 2
                    elif(s == 1):
                        team2 += "* " + str(get_nickname(member)) + "\n"
                        self.team2members[guild_id]['members'].append(member)
                    else:
                        team1 += "* " + str(get_nickname(member)) + "\n"

                await ctx.send(team1 + team2)

    @scrim.command()
    async def move(self, ctx: commands.Context):
        '''Move Team 2 to a different voice channel (must use !scrim first!)'''

        channel = ctx.author.voice.channel
        if channel is None:
            ctx.send(self.invalid_two_person_command_message)
        else:
            guild_id = ctx.message.guild.id
            if guild_id in self.team2members:
                channel_count = len(ctx.guild.voice_channels)
                if channel_count == 1:
                    await ctx.send('ERROR: Cannot find channel to move others to!')
                else:
                    if channel.position == channel_count - 1:
                        newChannelIndex = channel.position - 1
                    else:
                        newChannelIndex = channel.position + 1
                    self.team2members[guild_id]['old_channel_index'] = channel.position
                    for member in self.team2members[guild_id]['members']:
                        try:
                            await member.move_to(ctx.guild.voice_channels[newChannelIndex])
                        except HTTPException:
                            await ctx.send('ERROR: Cannot move ' + get_nickname(member))
            else:
                await ctx.send('ERROR: No saved team configuration. Run !scrim first')

    @scrim.command()
    async def back(self, ctx: commands.Context):
        '''Move Team 2 back to original voice channel (must use !move first!)'''
        channel = ctx.author.voice.channel
        if channel is None:
            ctx.send(self.invalid_two_person_command_message)
        else:
            guild_id = ctx.message.guild.id
            if guild_id in self.team2members:
                    newChannelIndex = self.team2members[guild_id]['old_channel_index']
                    for member in self.team2members[guild_id]['members']:
                        try:
                            await member.move_to(ctx.guild.voice_channels[newChannelIndex])
                        except HTTPException:
                            await ctx.send('ERROR: Cannot move ' + get_nickname(member))
            else:
                await ctx.send('ERROR: No saved team configuration. Run !scrim first')

async def setup(bot: commands.Bot):
    await ScrimCommands.add_to_bot('scrim', bot)
