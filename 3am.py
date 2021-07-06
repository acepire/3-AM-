import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl

from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix='?')

status = ['We Jamming out with my bot fellas!', 'Eating lyrics!', 'Chillin in peican town!', 'Doing assignments','studying rn','Attending Online Lectures!']
queue = []

@client.event
async def on_ready():
    change_status.start()
    print('Bot is online!')


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')

#CHATBOT

@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'yo what we sayin !', 'Hello, how you doing mate?', 'Hi', '**Wasssuup!**']
    await ctx.send(choice(responses))

@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))

@client.command(name='dev', help='This command returns the name of developer')
async def dev(ctx):
    await ctx.send('Made by `Aakarsh Aryan Kautilya`')


@client.command(name='credits', help='This command returns the TRUE credits')
async def credits(ctx):
    await ctx.send('**JUIT for the opportunity & Aakarsh Aryan Kautilya with the execution  **')

 #attendance      	
@client.command(name='attendance', help='This command returns the attendance')
async def attendance(ctx, filename):
    voice_channel = client.get_channel(800008029722116166)
    member_ids = voice_channel.voice_states.keys()

    with open(filename, 'w') as file:
        for member in voice_channel.members:
            file.write(member_ids + '\n')

import asyncio

#timer

@client.command()
async def count(ctx, number:int):
    try:
        if number < 0:
            await ctx.send('number cant be a negative')
        elif number > 600:
            await ctx.send('number must be under 600')
        else:
            message = await ctx.send(number)
            while number != 0:
                number -= 1
                await message.edit(content=number)
                await asyncio.sleep(1)
            await message.edit(content='Ended!')

    except ValueError:
        await ctx.send('time was not a number')

#calculator    

@client.command() 
async def add(ctx, *nums):
    operation = " + ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def sub(ctx, *nums): 
    operation = " - ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def multiply(ctx, *nums): 
    operation = " * ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def divide(ctx, *nums): 
    operation = " / ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

#reminder

from datetime import datetime

datetime.utcnow()

@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 60:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)
            

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='queue', help='This command adds a song to the queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@client.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')

    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')

@client.command(name='play', help='This command plays songs')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))
    del(queue[0])

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run('ODIxMDEzNTQwMzczNjU5Njg4.YE9icQ.yQvweXfrMiGOIihKHFr2muyBcoE')

