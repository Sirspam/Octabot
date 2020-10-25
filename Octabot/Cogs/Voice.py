import discord, logging, os, os.path,random, asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
cwd = os.getcwd()
shuffleallqueue = {}
song = []

def shuffleallnext (voice):
    global nextsong
    cwd = os.getcwd()
    if voice in shuffleallqueue:
        songvoice = (shuffleallqueue[voice])
        nextsong = (songvoice[0])
        del songvoice[0]
        nextsongdir = FFmpegPCMAudio(f"{cwd}\\Octagon\\"+nextsong)
        voice.play (nextsongdir, after= lambda e: shuffleallnext(voice))  
    else:
        for filename in os.listdir(f"{cwd}\\Octagon"):
            if filename.endswith(".mp3"):
                song.append(filename)
        random.shuffle(song)
        shuffleallqueue[voice] = song
        songvoice = (shuffleallqueue[voice])
        nextsong = (songvoice[0])
        del songvoice[0]
        nextsongdir = FFmpegPCMAudio(f"{cwd}\\Octagon\\"+nextsong)
        return (nextsongdir)

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Voice cog loaded")
    
    @commands.command()
    async def list(self, ctx):
        message = (str(""))
        filecount = 0
        loopcount = 0 
        for filename in os.listdir("{}\\Octagon".format(cwd)): #This tumour of code here splits the message into 2 to get around the character limit. I'm honestly surprised it works and it's probably hella inefficent but whatever
            filecount = filecount + 1
        fileC_half = filecount / 2
        fileC_rounded = int(fileC_half + 1)
        for filename in os.listdir("{}\\Octagon".format(cwd)):
            loopcount = loopcount + 1
            if filename.endswith(".mp3"):
                fileshort = (str(filename[:-4]))
            message = (message+fileshort+"\n")
            if loopcount == fileC_rounded:
                embed = discord.Embed(
                    title = "Octabot Song List",
                    description = message,
                    colour = 0xff0000,
                )
                await ctx.author.send(embed=embed)
                message = (str(""))
        embed = discord.Embed(
            description = message,
            colour = 0xff0000,
        )    
        embed.set_footer(text=f"Octabot currently has {filecount} glorious songs!\nAny recommendations for this list? DM Sirspam#7765")
        await ctx.author.send(embed=embed)
        dmcheck = ctx.channel.guild
        try:
            if dmcheck:
                await ctx.send ("I've sent you a DM of the song list!")
        except discord.Forbidden:
            await ctx.send("I can't DM you the list, Check that you've got DMs enabled!")
    
    @commands.command(pass_context=True)
    async def join(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        channel = ctx.author.voice.channel
        if ctx.author.voice is None: #For whatever reason this line didn't want to work while channel = was above it
            await ctx.send ("You need to be in a voice channel for me to join!")
            return
        #elif voice.is_playing(): This doesn't work, likely because the bot is always outputting silent audio for some reason.
        #    await ctx.send ("I'm currently playing something! Join the channel I'm currently in or wait for me to finish before trying oct$join")
        elif voice and voice.is_connected():
            channel = ctx.author.voice.channel
            await voice.move_to(channel)
        else: 
            channel = ctx.author.voice.channel
            voice = await channel.connect()
    
    @commands.command()
    async def leave(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if ctx.message.author.voice:
            if voice.is_playing():
                voice.stop()
                await asyncio.sleep(1)
            elif voice in shuffleallqueue:
                del shuffleallqueue[voice]
            await ctx.voice_client.disconnect()
    
    @commands.command(pass_context=True)
    async def play(self, ctx, *, song):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice == None:
            await ctx.send ("I'm not in a voice channel! Try using oct$join")
            return
        elif voice.is_playing():
            voice.stop()
        song = (song+'.mp3')
        if not os.path.exists(f"{cwd}\\Octagon\\"+song): #"{}\\Songs".format(cwd)
            await ctx.send ("That song doesn't exist! Do oct$list to check what songs can be played.")
            return
        source = FFmpegPCMAudio(f"{cwd}\\Octagon\\"+song)
        voice.play(source)
        song = song[:-4]
        await ctx.send ("Now playing "+song)
        logging.info (f"Bot playing {song} in guild id:{ctx.client.guild.id}")

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send ("Song paused!")
        if voice == None:
            print ("I'm not in a voice channel!")

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.resume()
            await ctx.send ("Song resumed!")
        if voice == None:
            print ("I'm not in a voice channel!")

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.send ("Song stopped!")
            await ctx.send ("<:JackBlackStop:754302092016877589>")
        if ctx.voice_client is None:
            await ctx.send ("I'm not in a voice channel!")

    @commands.command(pass_context=True)
    async def shuffle(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
        elif channel is None:
            await ctx.send("You need to be in a voice chat for me to join!")
            return
        elif voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        song = (random.choice(os.listdir(f"{cwd}\\Octagon")))
        source = FFmpegPCMAudio(f"{cwd}\\Octagon\\"+song)
        voice.play(source)
        song = song[:-4]
        await ctx.send ("Now playing "+song)

    @commands.command(pass_context=True) #This is still a bit of a mess from me trying to debug it, I'm not 100% certain that it works so I'll leave it alone
    async def shuffleall(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
        elif channel is None:
            await ctx.send("You need to be in a voice chat for me to join!")
            return
        elif voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        source = (shuffleallnext(voice))
        await ctx.send ("Now playing all songs!\nYou can use 'shuffleinfo' to see what song is playing.")
        voice.play (source, after=lambda e: shuffleallnext(voice))

    @commands.command(pass_context=True)
    async def shuffleinfo(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice not in shuffleallqueue:
            await ctx.send("There's nothing in the shuffle queue!")
            return
        songvoice = (shuffleallqueue[voice])
        nextestsong = (songvoice[0]) #Yes, my variable naming is great!
        snextsong = (str(nextsong[:-4]))
        snextestsong = (str(nextestsong[:-4]))
        await ctx.send(f"{snextsong} is currently playing!\n{snextestsong} is next in the queue!")
    
    @commands.command(pass_context=True)
    async def shuffleclear(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice in shuffleallqueue:
            del shuffleallqueue[voice]
            await ctx.send("Shuffle queue cleared!")
        if voice not in shuffleallqueue: 
            await ctx.send("The shuffle queue is already cleared!")

def setup(client):
    client.add_cog(Voice(client))