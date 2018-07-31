'''
Created on Jul 29, 2018

@author: Eli Gearheard
'''
import os
import discord
import bs4
from random import randint
import string
from googletrans import Translator
import dbl
from time import sleep
from test._test_multiprocessing import SayWhenError
from discord import guild
from discord import Role
from discord import utils
from asyncio.tasks import wait

#Directory stuff
root_dir = os.path.dirname(__file__)

#Auth tokens
tokenfile = open("auth_token.txt", "r")
rawtoken = tokenfile.read().splitlines()
token = rawtoken[0]

bltokenfile = open("dbl_token.txt", "r")
rawbltoken = bltokenfile.read().splitlines()
bltoken = rawbltoken[0]
shardCount = 1 #Keeping it simple with 1 for now.

client = discord.Client()
translator = Translator()
botlist = dbl.Client(client, bltoken)

defaultPrefix = ";"

def getServerPrefix(guild):
    #Returns the server prefix.
    #If there is no server prefix set, it returns the defaultPrefix.
    prefixFile = open("server_prefixes.txt", "r+")
    prefixList = prefixFile.read().splitlines()
    prefixFile.close()
    serverInList = False
    for line in prefixList:
        splitLine = line.split()
        if guild.id == int(splitLine[0]):
            serverInList = True
            return splitLine[1]
    if serverInList == False:
        #If server does not have default prefix set
        return defaultPrefix

def command(string, message):
    #Builds a command out of the given string.
    serverPrefix = getServerPrefix(message.channel.guild)
    return serverPrefix + string

def getArgument(command, message):
    #Gets the argument text as a string.
    argument = message.content.replace(command + " ", "")
    argument = argument.encode("ascii", "ignore")
    return argument

def getRawArgument(command, message):
    argument = message.content.replace(command + " ", "")
    return argument

eyebleach_relPath = "Lists/eyebleach.list"
eyebleach_absPath = os.path.join(root_dir, eyebleach_relPath)
eyefile = open(eyebleach_absPath)
eyelist = eyefile.read().splitlines()
eyeCount = len(eyelist) -1
eyefile.close()

hug_relPath = "Lists/hug.list"
hug_absPath = os.path.join(root_dir, hug_relPath)
hugfile = open(hug_absPath)
huglist = hugfile.read().splitlines()
hugCount = len(huglist) -1
hugfile.close()

insult1_relPath = "Lists/insult1.list"
insult1_absPath = os.path.join(root_dir, insult1_relPath)
insult1file = open(insult1_absPath)
insult1list = insult1file.read().splitlines()
insult1Count = len(insult1list) -1
insult1file.close()

insult3_relPath = "Lists/insult3.list"
insult3_absPath = os.path.join(root_dir, insult3_relPath)
insult3file = open(insult3_absPath)
insult3list = insult3file.read().splitlines()
insult3Count = len(insult3list) -1
insult3file.close()

insult2_relPath = "Lists/insult2.list"
insult2_absPath = os.path.join(root_dir, insult2_relPath)
insult2file = open(insult2_absPath)
insult2list = insult2file.read().splitlines()
insult2Count = len(insult2list) -1
insult2file.close()

gay_relPath = "Lists/gay.list"
gay_absPath = os.path.join(root_dir, gay_relPath)
gayfile = open(gay_absPath)
gaylist = gayfile.read().splitlines()
gayCount = len(gaylist) -1
gayfile.close()

xbox = 473687682334195733
playstation = 473687698893176842
pc = 473687715607478283

'''
commands
'''
@client.event
async def on_message(message):
    if message.content.upper().startswith(command("HELP", message)):
        msg = "Hello, {0.author.mention}! I am ***TBD***. I am an unfinished bot thereby having no working commands.".format(message)
        await message.channel.send(msg)
            
    elif message.content.upper().startswith(command('RELAX', message)):
        msg = eyelist[randint(0,eyeCount)]
        await message.channel.send(msg)
        
    elif message.content.upper().startswith(command("HUG",message)):
        msg = "{0.author.mention} hugs {0.mentions[0].mention}".format(message)
        await message.channel.send(msg)
        msg = huglist[randint(0,hugCount)]
        await message.channel.send(msg)
        await message.delete()
        
    elif message.content.upper().startswith(command('INSULT', message)):
        msg = "{0.author.mention} says to {0.mentions[0].mention} ".format(message) + insult1list[randint(0,insult1Count)] + insult2list[randint(0,insult2Count)] + insult3list[randint(0,insult3Count)]
        await message.channel.send(msg)
        await message.delete()
        
    elif message.content.upper().startswith(command("NO U", message)):
        msg = "{0.mentions[0].mention} ".format(message) + gaylist[randint(0,gayCount)]
        await message.channel.send(msg)
        await message.delete()
        
    elif message.content.upper().startswith(command("XBOX", message)):
        role = discord.Role(xbox)
        user = message.author
        await user.add_roles(role)
    
    elif message.content.upper().startswith(command('PC',message)):
        await client.add_role(message.author, pc)
        return await message.channel.send("The role @PC has been given to {0.author.mention}".format(message))
    
    elif message.content.upper().startswith(command("PLAYSTATION", message)):
        await client.add_role(message.author, playstation)
        return await message.channel.send("The role @playstation has been given to {0.author.mention}".format(message))
    '''
    admin commands
    '''
    if message.content.upper().startswith(command('WARN', message)):        
        if message.channel.permissions_for(message.author).administrator == True:
            msg = "{0.mentions[0].mention}, you have been warned by {0.author.mention}. Too many warning will result in a ban".format(message)
            await message.channel.send(msg)
        elif message.channel.permissions_for(message.author).administrator == False:
            msg = "Sorry {0.author.mention}. You do not have permission to use this command. DM an admin to report this player.".format(message)
            await message.channel.send(msg)
    async def kick(ctx, userName: discord.User):
        if message.content.upper().startswith(command("KICK",message)):
            if message.channel.permissions_for(message.author).administrator == True:
                await client.kick(userName)
                msg = "{0.mentions[0].mention} has been kicked.".format(message)
                await message.channel.send(msg)
            elif message.channel.permissions_for(message.author).administrator == False:
                msg = "Sorry {0.author.mention}. You do not have permission to use this command. DM an admin to report this player.".format(message)
                await message.channel.send(msg)
'''
Autonomous commands
'''
            
@client.event
async def on_member_join(member):
        await member.send("Welcome to The Gaming Corner! Use ;xbox, ;pc, or ;playstation to receive the role to your respected platform. Enjoy your stay! :)")
    
@client.event
async def on_ready():
    print (discord.__version__)
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------")
    serversConnected = str(len(client.guilds))
    print("Guilds connected: " + serversConnected)#Returns number of guilds connected to
    game=discord.Game('Helping you game faster.')
    await client.change_presence(activity=game)
    try:
        await botlist.post_server_count(serversConnected, shardCount)
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to dbl.")

while True:
    client.run(token) #runs the bot.