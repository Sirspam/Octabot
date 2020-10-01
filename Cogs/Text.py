import discord, logging, os, os.path,random
from discord.ext import commands
from discord.utils import get
class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info ("Text cog loaded")

    @commands.command() #Ping command
    async def ping(self, ctx):
        await ctx.send(f'Pong! ``{round(self.client.latency * 1000)}ms``')

    @commands.command() #Help command
    async def help(self, ctx):
        embed = discord.Embed(
            title = "Octabot Commands",
            description = "*Use the prefix 'oct$' at the start of all of these commands!* 🛑",
            colour = 0xff0000,
        )
        #embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/726579710254907493/3e749e3736c2d175aeabc4a21c2a5dcc.webp?size=256")
        embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/newsfeed/001/850/863/e5d.gif")
        embed.add_field(name="help", value="> Summons this message", inline = False)
        embed.add_field(name="ping", value="> Pings Octabot and displays the latency", inline = False)
        embed.add_field(name="list", value="> Directly messages you a list of all the octagon tunes which some dumb autist has collected", inline = False)
        embed.add_field(name="join", value="> Has Octabot join the voice channel you're currently in", inline = False)
        embed.add_field(name="leave", value="> Has Octabot leave the voice channel he's currently in", inline= False)
        embed.add_field(name="play <song>", value="> Plays a specified song. Only the listed songs shown in the list command will work", inline = False)
        embed.add_field(name="pause",value="> Pauses the song currently playing")
        embed.add_field(name="resume",value="> Resumes the current song if paused")
        embed.add_field(name="stop",value="> Stops the song currently playing. This will skip to the next song if using shuffleall")
        embed.add_field(name="shuffle", value="> Plays a random octagon song", inline = False)
        embed.add_field(name="shuffleall", value="> Adds every song at a random order into a queue (WIP)", inline = False)
        embed.set_footer(text="Got any feedback or recommendations for Octabot? DM Sirspam#7765")
        await ctx.send(embed=embed)
        
            
    @commands.command()
    async def embedt(self, ctx): #I kept this here just because I find it funny lel
        embed = discord.Embed(
            title = "Holy **fuck**",
            description = "I am in so much pain",
            colour = discord.Colour.lighter_gray()
        )
        embed.set_footer(text='Put me down like a stray dog uwu')
        embed.set_image(url="https://images-ext-1.discordapp.net/external/vmJTDHWjyNjhiDcVFg64v46EHZU4lFjemiAjJ509Lbk/https/media.discordapp.net/attachments/461381136661217283/759857423736897586/image0-2-1-1.gif?width=593&height=703") #Link might die, idk how long Discord keeps these files for
        #https://cdn.discordapp.com/attachments/493836827887796225/754493482726326393/Ehv1QqhWAAY0Tfa.png
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user: #Checks that the poster isn't the bot so it doesn't get stuck in some dumb endless loop or something idk
            return
        if message.content.startswith ('Octagon') or message.content.startswith ('octagon'): #Reacts to the word 'octagon' beacuse why not lol
            await message.add_reaction('\U0001f6d1')
    #    await self.client.process_commands(message)

def setup(client):    
    client.add_cog(Text(client))
