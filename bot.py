#all in one bot(beta). made by redknight:-

#here u need to add the import items:-

import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import asyncio
import random
import youtube_dl
import os

intents=discord.Intents.default()
intents.members=True
client=discord.Client(intents=intents)

client=commands.Bot(command_prefix='-')
client.remove_command("help")

#write event commands here:-

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle,activity=discord.Game('Python'))
	print("the bot is ready[made by redknight]")

@client.event
async def on_member_join(member):
    embed=discord.Embed(title="Welcome!", description=f"{member.metion}just joined the server!",value="Use -cmd for commands-list",colour=0x9208ea)
    embed.set_footer(text=f"made by redknight!")
    msg=await client.send_message(discord.Object(id="814090184836120589"),embed=embed)

@client.event
async def on_member_remove(member):
    embed=discord.Embed(title="Bye-Bye!", description=f"{member.metion}just left the server!",value="Use -cmd for commands-list",colour=0x9208ea)
    embed.set_footer(text=f"made by redknight!") 
    msg=await client.send_message(discord.Object(id="814090184836120589"),embed=embed)   
    
#write commands here:-

@client.command(pass_context=True)
async def help(ctx):
     await client.say("Use -cmd for commands :partying_face:")    

@client.command()
async def hi(ctx):
    embed=discord.Embed(title=f"Hello", description=f"----------",colour=0x9208ea)
    embed.add_field(name="**How can i help you!**",value="Use -cmd for commands-list")
    embed.set_footer(text=f"made by redknight!")
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    embed=discord.Embed(title=f"Ping of the bot", description=f"----------",colour=0x9208ea)
    embed.add_field(name="**PONG**",value=f"{round (client.latency * 1000)}ms")
    embed.set_footer(text=f"made by redknight!")
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member):
    await ctx.guild.ban(member)
    embed=discord.Embed(title=f"MODERATION", description=f"----------",colour=0x9208ea)
    embed.add_field(name="**BANNED**",value=f"{member.mention} has been **banned** from the server")
    embed.set_footer(text=f"made by redknight!")
    await ctx.send(embed=embed)


@client.command()
async def unban(ctx, *, member):
	banned_users=await ctx.guild.bans()
	member_name,member_discriminator=member.split('#')

	for ban_entry in banned_users:
		user=ban_entry.user

		if (user.name,user.discriminator)==(member_name,member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'{user.mention} is **Unbanned**')

			return

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member:discord.Member):
    await ctx.guild.kick(member)
    embed=discord.Embed(title=f"MODERATION", description=f"----------",colour=0x9208ea)
    embed.add_field(name="**KICKED**",value=f"{member.mention} has been **kicked** from the server")
    embed.set_footer(text=f"made by redknight!")
    await ctx.send(embed=embed)

@client.command()
async def clear(ctx, amount=2):
	await ctx.channel.purge(limit=amount)

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def announce(ctx,*,message):
     embed=discord.Embed(title=f"**Information**",description=message,colour=0x9208ea)
     embed.set_footer(text=f"made by redknight")
     await ctx.send(embed=embed)  

@client.command()
async def cmd(ctx):
    embed=discord.Embed(title=f"Bot commands!", description=f"----------",colour=0x9208ea)
    embed.add_field(name="**MODERATION COMMANDS**",value="ban,mute,warn,kick and clear")
    embed.add_field(name="**OTHER COMMANDS**",value="hi,ping,announce and giveaway")
    embed.set_footer(text=f"made by redknight!")
    await ctx.send(embed=embed)
        
@client.command()
@commands.has_role("Owner")
async def giveaway(ctx,mins:int,*,prize:str):
    embed=discord.Embed(title="Giveaway!", description=f"{prize}",color=0x9208ea)

    end=datetime.datetime.utcnow()+datetime.timedelta(seconds=mins*60)

    embed.add_field(name="Ends At:",value=f"{end}UTC")
    embed.set_footer(text=f"Ends in {mins} minutes from now!")

    my_msg=await ctx.send(embed=embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(mins*60)

    new_msg=await ctx.channel.fetch_message(my_msg.id)

    users= await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner=random.choice(users)

    await ctx.send(f"Congratulations! {winner.mention} won {prize}!")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()   
    
#write ur bot token here:-

client.run("YOUR TOKEN")
