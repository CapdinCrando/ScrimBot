## Imports
# Local
import bot_module

# Discord
import discord
from discord.ext import commands

# Third Party
import json
import attrs
from datetime import datetime
from mcstatus import JavaServer, status_response
from status import StatusCommands, StatusMessageInfo, StatusMessageList

@attrs.define()
class MinecraftServerInfo(StatusMessageInfo):
    '''Class to hold Minecraft status message information.'''

    server_name: str
    ip_address: str

    def __attrs_post_init__(self):
        '''Post init. Used to create JavaServer object.'''

        self.server = JavaServer.lookup(self.ip_address, self.status_timeout_seconds)
    
    async def get_status_content(self) -> discord.Embed:
        '''Overridden function to return Minecraft status message.'''

        try:
            server_status: status_response.JavaStatusResponse = await self.server.async_status()
            server_online = True
        except:
            server_online = False

        status_message = discord.Embed(title=self.server_name, color=discord.Color('1F8B4C'))
        status_message.add_field(name='Server IP: ', value=self.ip_address, inline=False)
        if server_online:
            status_message.add_field(name='Status: ', value='Online', inline=False)

            status_message.set_thumbnail(server_status.icon)

            player_status = f'{server_status.players.online}/{server_status.players.max}'
            status_message.add_field(name='Players: ', value=player_status, inline=False)

            status_message.add_field(name='MOTD', value=server_status.motd, inline=False)
            status_message.add_field(name='Version', value=server_status.version, inline=False)
            status_message.add_field(name='Latency: ', value=server_status.latency, inline=False)

            time = datetime.now()
            time_str = time.strftime('%m/%d/%y at %I:%M %p %Z')
            status_message.add_field(name='Last Checked: ', value=time_str, inline=False)

        return status_message

## Module
class MinecraftCommands(bot_module.Module):
    '''Commands for Minecraft.'''

    # Module settings
    mc_status_timeout_s: int
    mc_status_refresh_s: int

    def init_module(self):

        # Load data from file
        status_data_path = self.get_cache_file_path('mc_status_data.json')
        with open(status_data_path, 'r') as cache_file:
            status_data_raw = json.load(cache_file)

        # Create message list
        self.mc_status_server_info = StatusMessageList(
            status_data_raw, self.mc_status_refresh_s, self.mc_status_timeout_s, MinecraftServerInfo)
        
    @StatusCommands.status.command()
    async def minecraft(self, ctx: commands.Context, 
                        server_name: str = commands.parameter(displayed_name='Server Name', description='Localized server name'),
                        ip_address: str = commands.parameter(displayed_name='Server IP', description='IP Address of the Server (ex. 127.0.0.1:25565)')):
        '''Create a message to display the status of a Minecraft server.'''

        # Create initial message
        message = await ctx.send(f'Fetching status for {server_name} at {ip_address}...')
        
        # Create info
        status_info = MinecraftServerInfo(guild_id=ctx.guild.id, status_channel_id=ctx.channel.id, 
                            status_message_id=message.id, status_timeout_seconds=self.mc_status_timeout_s,
                            server_name=server_name, ip_address=ip_address)

        # Add to server info
        await self.mc_status_server_info.add_status_message(status_info)

        # Save data to file (in case of reboot)
        server_info_as_dict = attrs.asdict(self.mc_status_server_info)
        status_data_path = self.get_cache_file_path('mc_status_data.json')
        with open(status_data_path, 'w') as cache_file:
            json.dump(server_info_as_dict, cache_file)

async def setup(bot: commands.Bot):
    await MinecraftCommands.add_to_bot('minecraft', bot)