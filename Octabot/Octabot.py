import discord, logging, os, os.path, random
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
logging.basicConfig(format= '%(asctime)s:%(levelname)s:%(name)s: %(message)s',filename='Octalog.log',level=logging.INFO)
cwd = os.getcwd()
intents = discord.Intents.default()
client = commands.Bot(command_prefix = commands.when_mentioned_or("oct$"), intents=intents, case_insensitive=True, owner_id = (232574143818760192)) # Allows you to mention the bot instead of prefix and ignores caps, for better user experience
client.remove_command('help')

try: # Catch any errors when loading cogs, can be extremely useful when debugging
    for filename in os.listdir(f'{cwd}\\Cogs'):
        if filename.endswith(".py"):
           client.load_extension(f"Cogs.{filename[:-3]}")
except Exception as e:
    print(f"Possible fatal error:\n{e}\nThis means that the cogs have not started correctly!")
    logging.info (f"Possible fatal error:\n{e}\nThis means that the cogs have not started correctly!")
        
@client.event
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

@client.event
async def on_guild_join(guild):
    servers = list(client.guilds)
    logging.info(f"Bot has joined a new guild. The bot is now connected to {servers}")
    try: # Posts a greeting message in the guild's system channel. This won't work if the bot doesn't have permissions to post messages in the system channel.
        await guild.system_channel.send("**Hey, How's it going? I'm Octabot. Use ``oct$help`` to get started!** 🛑")
    except:
        pass

@client.event
async def on_guild_remove(ctx):
    servers = list(client.guilds)
    logging.info(f"Bot has been removed from a guild. The bot is now connected to {servers}")

File = open("Token.txt", "r")
Token = File.read()
File.close()
client.run(Token) #I've made it so the token is read from an external file. This is just so I don't have to edit out the token whenever uploading to the github registory
