## ScrimBot
# Made for the DeathSquad Discord Server by CapdinCrando
# Has many useful features, such as team selection and name changing
# Licensed under the GNU General Public License v3.0

## Imports
import csv
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

attackersFile = open("attackers.txt","r")   # Initialize attackers and defenders input files
defendersFile = open("defenders.txt","r")

attackers = []   # Initialize attackers and defenders arrays
defenders = []

attackerCount = 0
defenderCount = 0
for attacker in attackersFile:  # Fill attackers and defenders arrays with operators from input files
	attackers.append(attacker)
	attackerCount += 1

for defender in defendersFile:
	defenders.append(defender)
	defenderCount += 1

# Initialize attack and defense strategy lists
strat_list_attack = []
with open("strats_attack.txt") as strat_attack_file:
	strat_reader = csv.reader(strat_attack_file, delimiter="\t")
	for row in strat_reader:
		strat_list_attack.append(row)

strat_list_defense = []
with open("strats_defense.txt") as strat_defend_file:
	strat_reader = csv.reader(strat_defend_file, delimiter="\t")
	for row in strat_reader:
		strat_list_defense.append(row)

@bot.command()
async def scrim(ctx):
	"""!scrim command

	When called, the bot will take a list of all users in the voice channel of the author
	It will take this list and randomly assign them to two teams, and save and print the teams
	Warning: Currently each bot instance only works with one Discord server!	
	"""
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
	"""!move command

	When called, the move command will take the last saved team configuration,
	and move team 2 to a different channel
	"""
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
	"""!back command

	When called, the move command will take the last saved team configuration,
	and move team 2 back to the original channel
	"""
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
	"""!quote command

	The quote command will find a channel called quotes,
	pull a random message, and send it to the channel
	"""
	for channel in ctx.guild.text_channels:
		if(channel.name == "quotes"):
			quotes = []
			quoteCount = 0
			async for quote in channel.history(limit=None):
				quotes.append(quote.content)
				quoteCount += 1
			if(quoteCount > 0): await ctx.send(quotes[randint(0, quoteCount - 1)])

@bot.command()
async def quotetts(ctx):
	"""!quotetts command

	The quote command will find a channel called quotes,
	pull a random message, and send it to the channel with tts
	"""
	for channel in ctx.guild.text_channels:
		if(channel.name == "quotes"):
			quotes = []
			quoteCount = 0
			async for quote in channel.history(limit=None):
				quotes.append(quote.content)
				quoteCount += 1
			if(quoteCount > 0): await ctx.send(quotes[randint(0, quoteCount - 1)], tts=True)

@bot.command()
async def sugg(ctx):
	"""!sugg command

	Sends a 'SCHLORP SCHLORP SCHLORP SCHLORP' message to Discord channel
	"""
	await ctx.send('SCHLORP SCHLORP SCHLORP SCHLORP')

@bot.command()
async def killmenow(ctx):
	"""!killmenow command
	Chooses a random member in the author's text channel
	That member is sent a message telling them to "assasinate" the message author
	Disclaimer: 	The message specifies for this to be done in a video game,
					as we do not condone murder or contract killing
	"""
	target = ctx.author
	voice = target.voice
	if(voice != None):
		member_list = list(voice.channel.members)
		member_list.remove(target)
		if(len(member_list) > 0):
			hitman = choice(member_list)
			await hitman.send(f"{ target.name } has requested to be assassinated.\n"
								"You have been assigned to this task.\n"
								"In the next video game you play, take them out whenever they least expect it.\n"
								"Good luck, and don't get caught.")

@bot.command()
async def fugg(ctx):
	"""!fugg command

	Insults a random server member
	"""
	fugg_member = choice(ctx.guild.members)
	await ctx.send(f'Fugg you, <@{fugg_member.id}>')

@bot.command()
async def QjmschLizoardQjmschWizoard(ctx):
	"""!QjmschLizoardQjmschWizoard command

	Changes a specific user's to a random string of characters
	Fun fact: the random string is cryptographically strong, too!
	"""
	big = ctx.guild.get_member(bigunnn_id)
	name = b64encode(urandom(24)).decode('utf-8')
	await big.edit(nick=name)

@bot.command()
async def RandomAttackers(ctx):
	"""!RandomAttackers command
	
	Generates 5 random attackers from Siege
	"""
	usedOps = []   # Array to keep track of operators already used
	for i in range(5):
		operatorIdx = randint(0,attackerCount-1)   # Get random operator index (priming read)
		while(operatorIdx in usedOps):   # Has this operator been used already?
			operatorIdx = randint(0,attackerCount-1)   # If yes, get new random operator index
		usedOps.append(operatorIdx)   # Add operator to list of used operators
		attackerName = attackers[operatorIdx]   # Get name of the operator
		await ctx.send(attackerName)

@bot.command()
async def RandomDefenders(ctx):
	"""!RandomDefenders command

	Generates 5 random defenders from Siege
	"""
	usedOps = []   # Array to keep track of operators already used
	for i in range(5):
		operatorIdx = randint(0,defenderCount-1)   # Get random operator index (priming read)
		while(operatorIdx in usedOps):   # Has this operator been used already?
			operatorIdx = randint(0,defenderCount-1)   # If yes, get new random operator index
		usedOps.append(operatorIdx)   # Add operator to list of used operators
		defenderName = defenders[operatorIdx]   # Get name of the operator
		await ctx.send(defenderName)

@bot.command()
async def stratattack(ctx):
	"""!stratattack command

	Picks a random strategy from a list of attack strats and displays it
	"""
	strat = choice(strat_list_attack)
	strat_string = f"Random Strat Generated:\n\n**{ strat[0] }**\n- \"*{ strat[1] }*\"\n- { strat[2] }:"
	if len(strat) == 4:
		strat_string += ":"
		for op in strat[3].split(","):
			strat_string += f"\n\t- { op }"
	await ctx.send(strat_string)

@bot.command()
async def stratdefend(ctx):
	"""!stratdefend command

	Picks a random strategy from a list of defense strats and displays it
	"""
	strat = choice(strat_list_defense)
	strat_string = f"Random Strat Generated:\n\n**{ strat[0] }**\n- *\"{ strat[1] }\"*\n- { strat[2] }"
	if len(strat) == 4:
		strat_string += ":"
		for op in strat[3].split(","):
			strat_string += f"\n\t- { op }"
	await ctx.send(strat_string)

## Turn on the bot
bot.run(bot_id)