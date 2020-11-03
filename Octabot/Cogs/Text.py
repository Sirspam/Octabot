import discord, logging, os, os.path,random, asyncio
from discord.ext import commands
from discord.utils import get
cwd = os.getcwd()
def Octasearch(dir_in, dir_out):
    os.system(f'octagon -i "{dir_in}" -o "{dir_out}" --nogui')

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
        #embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/726579710254907493/3e749e3736c2d175aeabc4a21c2a5dcc.webp?size=256") the bot's pfp, just in case.
        embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/newsfeed/001/850/863/e5d.gif")
        embed.add_field(name="help", value="> Summons this message", inline = False)
        embed.add_field(name="ping", value="> Pings Octabot and displays the latency", inline = False)
        embed.add_field(name="search",value="> Looks for an octagon in a given image attachment", inline = False)  
        embed.add_field(name="list", value="> Directly messages you a list of all the octagon tunes which some dumb autist has collected", inline = False)
        embed.add_field(name="join", value="> Has Octabot join the voice channel you're currently in", inline = False)
        embed.add_field(name="leave", value="> Has Octabot leave the voice channel he's currently in", inline= False)
        embed.add_field(name="play <song>", value="> Plays a specified song. Only the listed songs shown in the list command will work", inline = False)
        embed.add_field(name="shuffle", value="> Plays a random octagon song", inline = False)                
        embed.add_field(name="shuffleall", value="> Adds every song at a random order into a queue", inline = False)
        embed.add_field(name="shuffleinfo",value="> Post the name of the song currently playing in the shuffle queue", inline = False)
        embed.add_field(name="shuffleclear",value="> Clears all songs in the shuffle queue", inline = False)
        embed.add_field(name="pause",value="> Pauses the song currently playing")
        embed.add_field(name="resume",value="> Resumes the current song if paused")
        embed.add_field(name="stop",value="> Stops the song currently playing. This will skip to the next song if using shuffleall")   
        embed.set_footer(text="Got any feedback or recommendations for Octabot? DM Sirspam#7765")
        await ctx.send(embed=embed)
       
    @commands.command()
    @commands.is_owner()
    async def embedt(self, ctx): #I kept this here just because I find it funny
        embed = discord.Embed(
            title = "Holy **fuck**", #please excuse my foul langauge
            description = "I am in so much pain",
            colour = discord.Colour.lighter_gray()
        )
        embed.set_footer(text='Put me down like a stray dog uwu')
        embed.set_image(url="https://images-ext-1.discordapp.net/external/vmJTDHWjyNjhiDcVFg64v46EHZU4lFjemiAjJ509Lbk/https/media.discordapp.net/attachments/461381136661217283/759857423736897586/image0-2-1-1.gif?width=593&height=703") #Link might die, idk how long Discord keeps these files for
        await ctx.send(embed=embed, delete_after=8.8) #it's funny because 8 is the funny octagon sides and angles number

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user: #Checks that the author isn't the bot so it doesn't get stuck in some dumb loop or something idk the nice youtube tutorial told me to do this
            return
        if message.content.startswith ('Octagon') or message.content.startswith ('octagon'): #Reacts to the word 'octagon' beacuse why not lol
            await message.add_reaction('\U0001f6d1')

    @commands.command()
    async def search(self, ctx):
        dir_in = (cwd+"\\in_temp.jpg")
        dir_out = (cwd+"\\out_temp.jpg")
        try:
            await ctx.message.attachments[0].save(dir_in)
            await ctx.send (f"{ctx.author.mention} I'll look for an octagon!")
            Octasearch(dir_in, dir_out)
            await ctx.send(file=discord.File(dir_out)) #I'd like to add an "We've found an octagon!" message with this but I don't think the image classification module returns anything if it doesn't find an octagon. So the bot may say that it's found an octagon despite not finding an octagon
            os.remove(dir_in)
            os.remove(dir_out)
        except:
            await ctx.send(f"**Without an attachment how can I find an octagon? How {ctx.author.name}? How?**\nYou need to include an attachment with your message!") #Personally I love this error response message

def setup(client):    
    client.add_cog(Text(client))
