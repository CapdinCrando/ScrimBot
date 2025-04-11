## Imports
# Local
import bot_module

# Discord
from discord.ext import commands

# Third Party
from random import choice

## Module
class FunnyCommands(bot_module.Module):
    '''FunnyCommands module

    Adds commands that are, put simply, funny.
    '''

    @commands.command()
    async def sugg(self, ctx: commands.Context):
        """!sugg command

        Sends a 'SCHLORP SCHLORP SCHLORP SCHLORP' message to Discord channel
        """
        await ctx.send('SCHLORP SCHLORP SCHLORP SCHLORP')

    @commands.command()
    async def killmenow(self, ctx: commands.Context):
        """!killmenow command
        Chooses a random member in the author's text channel
        That member is sent a message telling them to "assassinate" the message author
        Disclaimer: 	The message specifies for this to be done in a video game,
                        as we do not condone murder or contract killing
        """
        target = ctx.author
        voice = target.voice
        if(voice != None):
            member_list = list(voice.channel.members)
            member_list.remove(target)
            if(len(member_list) > 0):
                hitman = choice(member_list)
                await hitman.send(f"{ target.name } has requested to be assassinated.\n"
                                    "You have been assigned to this task.\n"
                                    "In the next video game you play, take them out whenever they least expect it.\n"
                                    "Good luck, and don't get caught.")

    @commands.command()
    async def fugg(self, ctx: commands.Context):
        """!fugg command

        Insults a random server member
        """
        fugg_member = choice(ctx.guild.members)
        await ctx.send(f'Fugg you, <@{fugg_member.id}>')

    @commands.command()
    async def pick(self, ctx: commands.Context):
        """!pick command

        Picks a random person in the user's voice channel
        """
        clsVoice = ctx.author.voice
        if(clsVoice != None):
            members = clsVoice.channel.members
            choice_member = choice(members)
            await ctx.send(f'<@{choice_member.id}>, I choose you!')


async def setup(bot: commands.Bot):
    await FunnyCommands.add_to_bot('funny', bot)
