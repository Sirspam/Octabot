import discord, logging, os, os.path, random
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
logging.basicConfig(format= '%(asctime)s:%(levelname)s:%(name)s: %(message)s',filename='Octalog.log',level=logging.INFO)
client = commands.Bot(command_prefix = 'oct$')
cwd = os.getcwd()
client.remove_command('help')

for filename in os.listdir(f'{cwd}\\Cogs'): #Loads all the py files in the cogs directory
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")
        
@client.event #Logs that the bot is online and changes the bot's presence
async def on_ready():
    logging.info ("Bot successfully logged in as {0.user}".format(client))
    print ("Bot successfully logged in as {0.user}".format(client))
    servers = list(client.guilds)
    logging.info(f"Bot is connected to {servers}")
    await client.change_presence(activity=discord.Game(name='Looking for an Octagon! | oct$help'))

@client.event
async def on_command_error(ctx, error):
    if isinstance (error, commands.CommandNotFound): #Gives an error if an invalid command is given
        await ctx.send("This command doesn't exist! use oct$help to check the available commands")
        client.remove_command('on_command_error')
    if isinstance(error, commands.MissingRequiredArgument): #Gives a message if the required arguments aren't given with a command
        await ctx.send('Please pass in all required arguments')
        client.remove_command('on_command_error')
        
@client.event #These two log whenever the bot is connected or disconnected from a guild. I mainly made this for fun, they aren't that useful.
async def on_guild_join(ctx):
    servers = list(client.guilds)
    logging.info(f"Bot has joined a new guild. The bot is now connected to {servers}")

@client.event
async def on_guild_remove(ctx):
    servers = list(client.guilds)
    logging.info(f"Bot has been removed from a guild. The bot is now connected to {servers}")

client.run('Token') #The bot's actual token has been removed from this version of the bot. 
