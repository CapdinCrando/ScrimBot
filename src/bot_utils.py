## Imports
# Discord
import discord

def get_nickname(user: discord.Member):
	'''get_nickname function

	Used to get a user's nickname and return it.
	If user does not have a nickname, it will return their username.
	'''

	if user.nick == None:
		return user.name
	return user.nick