## Imports
# Local
import bot_module

# Discord
from discord.ext import commands

# Third Party
from random import choice, randint

## Module
class FunnyCommands(bot_module.Module):
    '''Commands that are, put simply, funny.'''

    # Module fields
    pog_id: str

    # Class constants
    invalid_two_person_command_message = \
        'You and at least one other person must be in a voice channel to use this command!'

    @commands.command()
    async def sugg(self, ctx: commands.Context):
        '''Sends a "SCHLORP SCHLORP SCHLORP SCHLORP" message'''

        await ctx.send('SCHLORP SCHLORP SCHLORP SCHLORP')

    @commands.command()
    async def killmenow(self, ctx: commands.Context):
        '''Choose a random person in the voice channel to kill you (in game)'''

        target = ctx.author
        voice = target.voice
        if voice is None:
            await ctx.send(self.invalid_two_person_command_message)
        else:
            member_list = list(voice.channel.members)
            member_list.remove(target)
            if len(member_list) == 0:
                await ctx.send(self.invalid_two_person_command_message)
            else:
                hitman = choice(member_list)
                await hitman.send(f"{ target.name } has requested to be assassinated.\n"
                                    "You have been assigned to this task.\n"
                                    "In the next video game you play, take them out whenever they least expect it.\n"
                                    "Good luck, and don't get caught.")

    @commands.command()
    async def fugg(self, ctx: commands.Context):
        '''Insult a random server member'''

        fugg_member = choice(ctx.guild.members)
        await ctx.send(f'Fugg you, <@{fugg_member.id}>')

    @commands.command()
    async def poggers(self, ctx: commands.Context):
        '''Mimic a large crowd of users spamming the "pog" emoji'''
        PogAmount = randint(5,8)
        for i in range(PogAmount):
            await ctx.send(self.pog_id * randint(1, 10))

    @commands.command()
    async def pick(self, ctx: commands.Context):
        '''Picks a random person in the user's voice channel'''

        clsVoice = ctx.author.voice
        if clsVoice is None:
            ctx.send(self.invalid_two_person_command_message)
        else:
            members = clsVoice.channel.members
            choice_member = choice(members)
            await ctx.send(f'<@{choice_member.id}>, I choose you!')


async def setup(bot: commands.Bot):
    await FunnyCommands.add_to_bot('funny', bot)
