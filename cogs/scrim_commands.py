from discord.ext import commands
from discord import HTTPException

from math import ceil
from random import randint

team2members = {}	# Initalize team members array

def get_nickname(user):
	'''get_nickname function

	Used to get a user's nickname and return it.
	If user does not have a nickname, it will return their username.
	'''
	if user.nick == None:
		return user.name
	return user.nick

class ScrimCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scrim(self, ctx):
        """!scrim command

        When called, the bot will take a list of all users in the voice channel of the author
        It will take this list and randomly assign them to two teams, and save and print the teams
        Warning: Currently each bot instance only works with one Discord server!	
        """
        channel = ctx.author.voice.channel
        if(channel != None):
            guild_id = ctx.message.guild.id
            if guild_id in team2members:
                del team2members[guild_id]
            team2members[guild_id] = {}
            team2members[guild_id]['members'] = []
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
                        team1 += "- " + str(get_nickname(member)) + "\n"
                        size1 += 1
                        if(size1 == team_max): s = 1
                    else:
                        team2 += "- " + str(get_nickname(member)) + "\n"
                        team2members[guild_id]['members'].append(member)
                        size2 +=1
                        if(size2 == team_max): s = 2
                elif(s == 1):
                    team2 += "- " + str(get_nickname(member)) + "\n"
                    team2members[guild_id]['members'].append(member)
                else:
                    team1 += "- " + str(get_nickname(member)) + "\n"

            await ctx.send(team1 + team2)

    @commands.command()
    async def move(self, ctx):
        """!move command

        When called, the move command will take the last saved team configuration,
        and move team 2 to a different channel
        """
        channel = ctx.author.voice.channel
        if(channel != None):
            guild_id = ctx.message.guild.id
            if guild_id in team2members:
                channel_count = len(ctx.guild.voice_channels)
                if channel_count == 1:
                    await ctx.send('ERROR: Cannot find channel to move others to!')
                else:
                    if channel.position == channel_count - 1:
                        newChannelIndex = channel.position - 1
                    else:
                        newChannelIndex = channel.position + 1
                    team2members[guild_id]['old_channel_index'] = channel.position
                    for member in team2members[guild_id]['members']:
                        try:
                            await member.move_to(ctx.guild.voice_channels[newChannelIndex])
                        except HTTPException:
                            await ctx.send('ERROR: Cannot move ' + get_nickname(member))
            else:
                await ctx.send('ERROR: No saved team configuration. Run !scrim first')

    @commands.command()
    async def back(self, ctx):
        """!back command

        When called, the move command will take the last saved team configuration,
        and move team 2 back to the original channel
        """
        channel = ctx.author.voice.channel
        if(channel != None):
            guild_id = ctx.message.guild.id
            if guild_id in team2members:
                    newChannelIndex = team2members[guild_id]['old_channel_index']
                    for member in team2members[guild_id]['members']:
                        try:
                            await member.move_to(ctx.guild.voice_channels[newChannelIndex])
                        except HTTPException:
                            await ctx.send('ERROR: Cannot move ' + get_nickname(member))
            else:
                await ctx.send('ERROR: No saved team configuration. Run !scrim first')

async def setup(bot):
    await bot.add_cog(ScrimCog(bot))