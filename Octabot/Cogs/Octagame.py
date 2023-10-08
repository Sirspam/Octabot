#I've got the feeling that this cog is an inefficent mess
#Also I learnt SQLite just for this, so expect the most smartest code you've ever seen
import discord, logging, random, asyncio, sqlite3
from discord.ext import commands
from discord.utils import get
emotes = ["🛑","🟥","⛔","🔴","🏮","<:weary_octagonal_sign:776004948810661890>"] #Annoyingly there's not many emotes that look similar to an octagon. I may add custom emotes to this later
xgrid = ("1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣")
class Octagame(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info ("Octagame cog loaded")

    #I found out about subcommands just after finishing this. For now it works fine so I might change it to subcommands later
    @commands.command()
    async def game(self, ctx, message):
        guild = int(ctx.guild.id)
        user = int(ctx.author.id)
        db = sqlite3.connect("Octagame.db")
        cursor = db.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{guild}"
        (user INT PRIMARY KEY, easy INT , normal INT, hard INT)''')
        cursor.execute(f'SELECT user FROM "{guild}" WHERE user={user}')
        check = cursor.fetchone()
        if check is None:
            cursor.execute(f'INSERT INTO "{guild}" VALUES ("{user}", "0", "0", "0")')
        db.commit()
        #
        cursor.execute(f'SELECT easy, normal, hard FROM "{guild}"')
        rows = cursor.fetchall()
        db.close()
        if message.lower() == "help":
            embed = discord.Embed(
                title = "OctaGame Help",
                description = "Octabot needs your help to find an octagon! This simple game's goal is to find an octagon emote in a field full of similar looking emotes!\n\nTo play, choose a difficulty and then post the ``x,y`` values of the Octagon!\n\nThe oct$game command works with the following arguments:",
                colour = 0xff0000,
            )
            embed.set_thumbnail(url="https://thumbs.gfycat.com/PresentOilyErin-max-1mb.gif")
            embed.add_field(name="Help", value="> Summons this message!")
            embed.add_field(name="Stats", value="> Posts your OctaGame stats!")
            embed.add_field(name="Easy", value="> Features a single row of 8 emotes! (Only requires the X coordinate)\n1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣\n🛑🛑🛑🛑🛑🛑🛑🛑", inline = False)
            embed.add_field(name="Normal", value ="> Features four rows of 32 emotes! \n⬛1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣\n1️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n2️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n3️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n4️⃣🛑🛑🛑🛑🛑🛑🛑🛑", inline = False)
            embed.add_field(name="Hard", value ="> Features eight rows of 64 emotes! \n⬛1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣\n1️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n2️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n3️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n4️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n5️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n6️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n7️⃣🛑🛑🛑🛑🛑🛑🛑🛑\n8️⃣🛑🛑🛑🛑🛑🛑🛑🛑", inline = False) #What a funny and long line 
            embed.add_field(name="Response Formatting", value="> Make sure to format your response messages as ``x,y``! The x value is shown at the top of the graph while the y value is shown on the left side. As easy only has the x value, the y value isn't needed", inline = False)
            await ctx.send(embed=embed)
        
        elif message.lower() == "easy":
            random_emotes = "".join(random.choices(emotes[1]+emotes[2]+emotes[3]+emotes[4], k = 8))
            pos = random.randint(0,7)
            chance = random.randint(0,9)
            if chance == 8:
                random_emotes = random_emotes [:pos] + emotes[5] + random_emotes[pos+1:]
            else:
                random_emotes = random_emotes [:pos] + emotes[0] + random_emotes[pos+1:]
            embed = discord.Embed(
                title = "Help me find an Octagon!",
                description = xgrid+"\n"+random_emotes,
                colour = 0xff0000,
            )
            embed.set_footer(text="Format your answer as 'x'!")
            await ctx.send(embed=embed)     
            
            pos = str((pos + 1))
            try: 
                msg = await self.client.wait_for("message", timeout = 30.0,check=lambda message: message.author == ctx.author)
                if pos == msg.content:
                    await ctx.send ("**You've found an Octagon!**\nYou can use ``oct$game stats`` for statistics!")
                    db = sqlite3.connect("Octagame.db")
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE "{guild}" SET easy=easy+1 WHERE user={user}')
                    db.commit()
                    db.close()
                else:
                    await ctx.send ("That's not an Octagon!")
            except asyncio.TimeoutError:
                return await ctx.send ("Sorry, you took too long to respond! Use ``oct$game`` to try again!")
        
        elif message.lower() == "normal":
            random_emotes = []
            count = 0
            while count != 4:
                random_emotes.append ("".join(random.choices(emotes[1]+emotes[2]+emotes[3]+emotes[4], k = 8)))
                count = count + 1
            pos = random.randint(0,7)
            random_line = random.randint(0,3)
            chance = random.randint(0,9)
            temp = random_emotes[random_line] #For whatever reason I couldn't directly use random_emotes[] so I used this method instead 
            if chance == 8:
                temp = (temp [:pos] + emotes[5] + temp[pos+1:])
            else:
                temp = (temp [:pos] + emotes[0] + temp[pos+1:])
            random_emotes[random_line] = temp
            embed = discord.Embed(
                title = "Help me find an Octagon!",
                description = "⬛"+xgrid+"\n1️⃣"+random_emotes[0]+"\n2️⃣"+random_emotes[1]+"\n3️⃣"+random_emotes[2]+"\n4️⃣"+random_emotes[3],
                colour = 0xff0000,
            )
            embed.set_footer(text="Format your answer as 'x,y'!")
            await ctx.send(embed=embed)
            xpos = str((pos + 1))
            ypos = str((random_line + 1))
            pos = (f"{xpos},{ypos}")
            try:
                msg = await self.client.wait_for("message", timeout = 30.0,check=lambda message: message.author == ctx.author)
                if pos == msg.content:
                    await ctx.send ("**You've found an Octagon!**\nYou can use ``oct$game stats`` for statistics!")
                    db = sqlite3.connect("Octagame.db")
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE "{guild}" SET normal=normal+1 WHERE user={user}')
                    db.commit()
                    db.close()
                else:
                    await ctx.send ("That's not an Octagon!")
            except asyncio.TimeoutError:
                return await ctx.send ("Sorry, you took too long to respond! Use ``oct$game`` to try again!")

        elif message.lower() == "hard":
            random_emotes = []
            count = 0
            while count != 8:
                random_emotes.append ("".join(random.choices(emotes[1]+emotes[2]+emotes[3]+emotes[4], k = 8)))
                count = count + 1
            pos = random.randint(0,7)
            random_line = random.randint(0,7)
            chance = random.randint(0,9)
            temp = random_emotes[random_line]
            if chance == 8:
                temp = (temp [:pos] + emotes[5] + temp[pos+1:])
            else:
                temp = (temp [:pos] + emotes[0] + temp[pos+1:])
            random_emotes[random_line] = temp
            embed = discord.Embed(
                title = "Help me find an Octagon!",
                description = "⬛"+xgrid+"\n1️⃣"+random_emotes[0]+"\n2️⃣"+random_emotes[1]+"\n3️⃣"+random_emotes[2]+"\n4️⃣"+random_emotes[3]+"\n5️⃣"+random_emotes[4]+"\n6️⃣"+random_emotes[5]+"\n7️⃣"+random_emotes[6]+"\n8️⃣"+random_emotes[7],
                colour = 0xff0000,
            )
            embed.set_footer(text="Format your answer as 'x,y'!")
            await ctx.send(embed=embed)

            xpos = str((pos + 1))
            ypos = str((random_line + 1))
            pos = (f"{xpos},{ypos}")
            try:
                msg = await self.client.wait_for("message", timeout = 30.0,check=lambda message: message.author == ctx.author)
                if pos == msg.content:
                    await ctx.send ("**You've found an Octagon!**\nYou can use ``oct$game stats`` for statistics!")
                    db = sqlite3.connect("Octagame.db")
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE "{guild}" SET hard=hard+1 WHERE user={user}')
                    db.commit()
                    db.close()
                else:
                    await ctx.send ("That's not an Octagon!")
            except asyncio.TimeoutError:
                return await ctx.send ("Sorry, you took too long to respond! Use ``oct$game`` to try again!")
        
        elif message.lower() == "stats":
            db = sqlite3.connect("Octagame.db")
            cursor = db.cursor()
            cursor.execute(f'SELECT easy, normal, hard FROM "{guild}" WHERE user={user}')
            rows = cursor.fetchone()
            db.close()
            embed = discord.Embed(
                title = f"{ctx.author.display_name}'s OctaGame Stats",
                colour = 0xff0000,
                timestamp = ctx.message.created_at
            )
            embed.add_field(name="Easy", value = f"Found {rows[0]} Octagons!", inline = False)
            embed.add_field(name="Normal", value = f"Found {rows[1]} Octagons!", inline = False)
            embed.add_field(name="Hard", value = f"Found {rows[2]} Octagons!", inline = False)
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            embed.set_footer(text=ctx.guild)
            await ctx.send(embed=embed)
        else:
            await ctx.send("That's not a valid command! Use ``oct$game help`` for help!")

async def setup(client):    
    await client.add_cog(Octagame(client))
