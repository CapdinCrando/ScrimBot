
import discord
from discord.ext import commands

import os
import asyncio
from random import choice

## Events
class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    on_voice_state_update event

    Called when someone joins, leaves, is muted, or is defeaned
    """
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        '''
        Plays an intro sound when someone joins a voice channel
        '''
        
        # Check for join event
        if before.channel is None and after.channel is not None:

            # Check if intro folder exists
            intro_folder = 'intros/' + str(member.id)
            if(os.path.isdir(intro_folder)):
                
                # Folder exists, get all available files
                sound_files = [f for f in os.listdir(intro_folder) if f.endswith('.mp3') and os.path.isfile(intro_folder + '/' + f) ]

                # Check to make sure good files exist
                if(len(sound_files) != 0):
                    
                    # Pick random file
                    intro_file_name = intro_folder + '/' + choice(sound_files)

                    # Connect to voice
                    voice_client = await after.channel.connect()
                
                    # Play sound and leave when done
                    voice_client.play(discord.FFmpegPCMAudio(executable='bin/ffmpeg.exe', source=intro_file_name), 
                        after=lambda error: asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop))
                    
async def setup(bot):
    await bot.add_cog(EventsCog(bot))