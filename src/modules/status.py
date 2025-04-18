## Imports
# Local
import bot_module

# Discord
import discord
from discord.ext import commands, tasks

# Third Party
import attrs
import threading

@attrs.define(eq=False, hash=False)
class StatusMessageInfo():
    '''Class for storing information regarding status messages.'''

    guild_id: int
    status_channel_id: int
    status_message_id: str
    status_timeout_seconds: int

    def __hash__(self):
        '''Override hash to allow to be used as dict key.'''

        return hash(self.guild_id)

    def __eq__(self, other):
        '''Override eq to allow to be used as dict key.'''

        if isinstance(other, StatusMessageInfo):
            return self.guild_id == other.guild_id
        return False
    
    async def get_status_content(self) -> discord.Embed:
        '''Function called to get status content. Meant to be overridden.'''

        return discord.Embed()
    
    async def update_message(self, new_embed: discord.Embed):
        '''Fetch the message object and edit it wit new embed.'''

        message: discord.Message = await self._fetch_message()
        if message is not None:
            await message.edit(embed=new_embed)
        
    async def delete_message(self):
        '''Fetch the message object and delete the message.'''

        message: discord.Message = await self._fetch_message()
        if message is not None:
            await message.delete()

    async def _fetch_message(self, bot: commands.Bot) -> discord.Message:
        '''Fetch the message object from Discord using the saved ids.'''

        channel = bot.get_channel(self.status_channel_id)
        if channel is not None:

            if isinstance(channel, discord.TextChannel):
                return await channel.fetch_message(self.status_message_id)
        
        return None
    
class StatusMessageList():
    '''Class used for storing and managing status messages of the same type.'''

    _dict: dict[int, StatusMessageInfo]
    _lock: threading.Lock

    def _make_new_status_info(self, info_dict: dict):
        '''Called to generate a new info class from the given dict'''

        return self._status_info_class(**info_dict)
    
    @tasks.loop()
    async def _update_status_messages(self):
        '''Main status update loop.'''

        with self._lock:
            for _, info in self._dict.items():
                if isinstance(info, self._status_info_class):
                    await self._update_message(info)
        
    def __init__(self, status_dict: dict, refresh: int, timeout: int, status_info_type: type = StatusMessageInfo):
        '''List initialization.'''

        self._dict = {}
        self._lock = threading.Lock()

        # Save info type
        self._status_info_class = status_info_type

        # Lock
        with self._lock:

            # Convert dict to status message info
            for _, info in status_dict.items():
                if isinstance(info, dict):
                    message_info: StatusMessageInfo = self._make_new_status_info(info)
                    message_info.status_timeout_seconds = timeout
                    self._dict[message_info.guild_id] = message_info
            
        # Start status thread
        self._update_status_messages.change_interval(seconds=refresh)
        self._update_status_messages.start()

    def get_dict(self):
        '''Called to retrive the internal dict and elements as dicts.'''

        # Lock
        formatted_dict = self._dict
        with self._lock:
            for key, value in formatted_dict.items():
                formatted_dict[key] = attrs.asdict(value) # TODO: Add filter here
            return formatted_dict

    async def _update_message(self, message_info: StatusMessageInfo):
        '''Called to update a message within the internal dict.
        '''
        status_message = await message_info.get_status_content()

        try:
            await message_info.update_message(status_message)
        except discord.errors.NotFound:
            del self._dict[message_info.guild_id]

    async def add_status_message(self, message_info: StatusMessageInfo):
        '''Add a new status message to the list.'''

        with self._lock:

            # Check if already in dict
            if message_info.guild_id in self._dict:

                # If in dict, get and delete old message
                old_message: StatusMessageInfo = self._dict[message_info.guild_id]
                await old_message.delete_message()

            # Add message info
            self._dict[message_info.guild_id] = message_info

            try:
                # Do initial message update
                await self._update_message(message_info)

            except:
                print('Error')
                return
        
## Module
class StatusCommands(bot_module.Module):
    '''Commands for reporting the statuses of game servers.'''

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: commands.Context):
        '''Create a message to display the status of a game server.'''
        pass

async def setup(bot: commands.Bot):
    await StatusCommands.add_to_bot('status', bot)
