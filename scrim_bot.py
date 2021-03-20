import discord
from constants import bigunnn_id, bot_id
from discord.ext import commands
from discord import HTTPException
from random import randint
from random import shuffle
from math import ceil
from os import urandom
from base64 import b64encode

bot = commands.Bot(command_prefix='!')

team2members = []

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

@bot.command()
async def sugg(ctx):
	await ctx.send('SCHLORP SCHLORP SCHLORP SCHLORP')

@bot.command()
async def QjmschLizoardQjmschWizoard(ctx):
	big = ctx.guild.get_member(bigunnn_id)
	name = b64encode(urandom(24)).decode('utf-8')
	await big.edit(nick=name)

bot.run(bot_id)