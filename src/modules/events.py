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
class CustomEvents(bot_module.Module):
    '''Custom event handlers.'''

    # Module fields
    ffmpeg_location: str

    def init_module(self):
        self.intro_timestamp_dict = {}
        self.intro_timestamp_mutex = threading.Lock()

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
    await CustomEvents.add_to_bot('events', bot)
