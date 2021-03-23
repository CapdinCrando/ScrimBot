## ScrimBot
# Made for the DeathSquad Discord Server by CapdinCrando
# Has many useful features, such as team selection and name changing
# Licensed under the GNU General Public License v3.0

## Imports
import discord
from constants import bigunnn_id, bot_id	## Used for privacy reasons
from discord.ext import commands
from discord import HTTPException
from random import randint, shuffle, choice
from math import ceil
from os import urandom
from base64 import b64encode

intents = discord.Intents.default()
intents.members = True

## Bot Setup
bot = commands.Bot(command_prefix='!', intents = intents)

team2members = []	# Initalize team members array

## !scrim command
# When called, the bot will take a list of all users in the voice channel of the author
# It will take this list and randomly assign them to two teams, and save and print the teams
# Warning: Currently each bot instance only works with one Discord server!
@bot.command()
async def scrim(ctx):
	channel = ctx.author.voice.channel
	if(channel != None):
		team2members.clear()
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
					team1 += "- " + str(member.nick) + "\n"
					size1 += 1
					if(size1 == team_max): s = 1
				else:
					team2 += "- " + str(member.nick) + "\n"
					team2members.append(member)
					size2 +=1
					if(size2 == team_max): s = 2
			elif(s == 1):
				team2 += "- " + str(member.nick) + "\n"
				team2members.append(member)
			else:
				team1 += "- " + str(member.nick) + "\n"

		await ctx.send(team1 + team2)

## !move command
# When called, the move command will take the last saved team configuration,
# and move team 2 to a different channel
@bot.command()
async def move(ctx):
	channel = ctx.author.voice.channel
	if(channel != None):
		newChannel = ctx.guild.voice_channels[1]
		for member in team2members:
			try:
				await member.move_to(newChannel)
			except HTTPException:
				await ctx.send('ERROR: Cannot move ' + member.nick)

## !back command
# When called, the move command will take the last saved team configuration,
# and move team 2 back to the original channel
@bot.command()
async def back(ctx):
	channel = ctx.author.voice.channel
	if(channel != None):
		newChannel = ctx.guild.voice_channels[0]
		for member in team2members:
			try:
				await member.move_to(newChannel)
			except HTTPException:
				await ctx.send('ERROR: Cannot move ' + member.nick)

## !quote command
# The quote command will find a channel called quotes,
# pull a random message, and send it to the channel
@bot.command()
async def quote(ctx):
	for channel in ctx.guild.text_channels:
		if(channel.name == "quotes"):
			quotes = []
			quoteCount = 0
			async for quote in channel.history(limit=None):
				quotes.append(quote.content)
				quoteCount += 1
			if(quoteCount > 0): await ctx.send(quotes[randint(0, quoteCount - 1)])

## !sugg command
# Sends a 'SCHLORP SCHLORP SCHLORP SCHLORP' message to Discord channel
@bot.command()
async def sugg(ctx):
	await ctx.send('SCHLORP SCHLORP SCHLORP SCHLORP')

## !fugg command
# Insults a random server member
@bot.command()
async def fugg(ctx):
	fugg_member = choice(ctx.guild.members)
	await ctx.send(f'Fugg you, <@{fugg_member.id}>')

## !QjmschLizoardQjmschWizoard command
# Changes a specific user's to a random string of characters
# Fun fact: the random string is cryptographically strong, too!
@bot.command()
async def QjmschLizoardQjmschWizoard(ctx):
	big = ctx.guild.get_member(bigunnn_id)
	name = b64encode(urandom(24)).decode('utf-8')
	await big.edit(nick=name)

## Turn on the bot
bot.run(bot_id)