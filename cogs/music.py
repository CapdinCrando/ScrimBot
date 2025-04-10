from discord import PCMVolumeTransformer, FFmpegPCMAudio
from discord.ext import commands

import yt_dlp as youtube_dl
import asyncio
from random import choice
import re

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, executable='bin/ffmpeg.exe', **ffmpeg_options), data=data)
    
async def fade_out(ctx):
    """Gradually decreases the volume of the currently playing audio."""
    voice_client = ctx.voice_client
    
    if voice_client and voice_client.is_playing():
        # Start at the current volume and decrease to 0
        for volume in range(10, -1, -1):
            voice_client.source.volume = volume / 10
            await asyncio.sleep(0.5)  # Wait half a second between each volume decrease

async def fade_in(ctx):
    """Gradually decreases the volume of the currently playing audio."""
    voice_client = ctx.voice_client
    
    if voice_client and voice_client.is_playing():
        # Start at the current volume and decrease to 0
        for volume in range(10, -1, -1):
            voice_client.source.volume = volume / 10
            await asyncio.sleep(0.5)  # Wait half a second between each volume decrease

class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays audio from a YouTube URL"""
        
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()



        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            # Stop current audio if it's playing
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(MusicCog(bot))