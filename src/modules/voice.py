## Imports
# Local
import bot_module

# Discord
import discord
from discord.ext import commands

# Third Party
import os
import asyncio
import threading
from random import choice
from datetime import datetime, timedelta

## Module
class VoiceCommands(bot_module.Module):
    '''Commands that utilize the voice channel.'''

    # Module fields
    ffmpeg_location: str
    react_file_ext: str

    def init_module(self):
        self.intro_timestamp_dict = {}
        self.intro_timestamp_mutex = threading.Lock()

        # Get reactions
        react_folder = self.get_resource_path('reactions')
        if(os.path.isdir(react_folder)):

            # Folder exists, get all available files
            self.react_file_names = \
                [f'{react_folder}/{f}' for f in os.listdir(react_folder) if f.endswith(self.react_file_ext) and os.path.isfile(react_folder + '/' + f) ]

    @commands.command()
    async def react(self, ctx: commands.Context):
        '''Get a genuine reaction from ScrimBot'''
        
        # Verify voice channel
        channel = ctx.author.voice.channel
        if channel is None:

            ctx.send('Must be in a voice channel to use this command!')

        else:

            # Check to make sure good files exist
            if(len(self.react_file_names) != 0):

                # Choose file
                chosen_react_file = choice(self.react_file_names)

                # Connect to voice
                voice_client: discord.VoiceProtocol = await channel.connect()

                # Prevent overriding current voice
                if voice_client.is_playing():
                    return

                # Play sound and leave when done
                voice_client.play(
                    discord.FFmpegPCMAudio(executable=self.ffmpeg_location, source=chosen_react_file),
                    after=lambda error: asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        '''Called when someone joins, leaves, is muted, or is deafened'''

        # Check for join event
        if before.channel is None and after.channel is not None:

            # Get last time the intro was played
            self.intro_timestamp_mutex.acquire()
            old_timestamp = self.intro_timestamp_dict.get(member.id)
            self.intro_timestamp_mutex.release()

            # Make sure time isn't None
            if old_timestamp is not None:

                # Compare last time the intro was played
                if(datetime.now() - old_timestamp) < timedelta(minutes=5):

                    # If played in last 5 minutes, return and skip playing intro
                    return

            # Check if intro folder exists
            intro_folder = self.get_resource_path('intros/' + str(member.id))
            if(os.path.isdir(intro_folder)):

                # Folder exists, get all available files
                sound_files = [f for f in os.listdir(intro_folder) if f.endswith('.mp3') and os.path.isfile(intro_folder + '/' + f) ]

                # Check to make sure good files exist
                if(len(sound_files) != 0):

                    # Pick random file
                    intro_file_name = intro_folder + '/' + choice(sound_files)

                    # Connect to voice
                    voice_client: discord.VoiceProtocol = await after.channel.connect()

                    # Prevent overriding current voice
                    if voice_client.is_playing():
                        return

                    # Play sound and leave when done
                    voice_client.play(
                        discord.FFmpegPCMAudio(executable=self.ffmpeg_location, source=intro_file_name),
                        after=lambda error: asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop))

                    # Log sound played
                    timestamp = datetime.now()
                    self.intro_timestamp_mutex.acquire()
                    self.intro_timestamp_dict[member.id] = timestamp
                    self.intro_timestamp_mutex.release()

async def setup(bot: commands.Bot):
    await VoiceCommands.add_to_bot('voice', bot)
