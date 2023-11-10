import time
import httpx
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio


#Discord
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)
TOKEN = 'MTE0MzY0NjA4MDM0NTU5MTg3OA.GuZyOc.hULKYoRs4qxHt8P5AqywVn3uqm2ZxEAlUagbIM'
channelID = 1156578431065137243


#text to speech
voiceKey = '200b849543f842c79d6d86167dcc7945'
voiceID = 'Cwbia66vfaPQJQOmF708xFOszsg2'
headers = {'Authorization': voiceKey, 'X-User-Id': voiceID, 'content-type': 'application/json', "accept": "text/event-stream"}
tts_url = 'https://play.ht/api/v2/tts'


#chatbot
chat_url = 'https://www.botlibre.com/rest/json/chat'
botID = '49467149'
appID = '8281860679139832729'




@client.event
async def on_ready():
    print('solbot is ready for action')


@client.event
async def on_member_join(member):
    channel = client.get_channel(channelID)
    await channel.send('Hello there >:)')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(channelID)
    await channel.send(member + ' cant handle the heat')

@client.command(pass_context = True)
async def menu(ctx):
    file = discord.File("sol bot.png", filename="sol bot.png")
    embed = discord.Embed(title='Sol-bot Commands', description='unlike the real Sol, sol-bot is not very smart and does not respond to profanities, so please treat him like the failed experiment he is.', colour=discord.Colour.dark_embed())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1101268045676163146/1155869490874155048/sol_bot.png")
    embed.add_field(name='!join', value='add me to your discord call!')
    embed.add_field(name='!leave', value='kick me from your discord call!', inline=False)
    embed.add_field(name='chat!', value='type "chat!" followed by whatever you like to say and get a text response', inline=False)
    embed.add_field(name='voice!', value='type "voice!" followed by whatever you like to say and get a voice response', inline=True)
    embed.set_footer(text='note that the "!" symbol is placed on the end of the commands "chat" and "voice".')
    await ctx.send(embed=embed)
    
@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('pillarManTheme.mp3')
        player = voice.play(source)
    else:
        await ctx.send('nope')

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        channel = ctx.message.author.voice.channel
        source = FFmpegPCMAudio('mario goodbye.mp3')
        player = ctx.guild.voice_client.pause()
        player = ctx.guild.voice_client.play(source)
        time.sleep(1.9)
        await ctx.guild.voice_client.disconnect()
        await ctx.send('teletubbie bye bye')
    else:
        await ctx.send('you leave')


@client.event
async def on_message(message):
    text_channel = client.get_channel(channelID)
    if message.content.split('!')[0] == 'chat':
        print('processing chat...')
        user_input = message.content.split('! ')[1]
        chat_params = {
            'application': appID,
            'instance': botID,
            'message': user_input
        }
        async with httpx.AsyncClient() as http_client:
            chat_response = await http_client.post(url=chat_url, json=chat_params)
            answer = chat_response.text.split('"')[3]
            await text_channel.send(answer)
    if message.content.split('!')[0] == 'voice':
        await text_channel.send('processing...')
        user_input = message.content.split('! ')[1]
        chat_params = {
            'application': appID,
            'instance': botID,
            'message': user_input
        }
        async with httpx.AsyncClient() as http_client:
            chat_response = await http_client.post(url=chat_url, json=chat_params)
            answer = chat_response.text.split('"')[3]
            speech_params = {"text": answer, "voice": "s3://voice-cloning-zero-shot/b08aecc0-588c-41d5-b8f7-be6e279201a8/sol/manifest.json"}
        try:
            async with httpx.AsyncClient() as http_client2:
                voice_response = await http_client2.post(url=tts_url, headers=headers, json=speech_params)
                voice_url = voice_response.text.split('url":')[1]
                final_voice_url = voice_url.split(',"duration"')[0]
                await text_channel.send('voice response: ' + final_voice_url)
                print('sent voice')
        except Exception:
            await text_channel.send('voice response generation failed, try again')
    await client.process_commands(message)

client.run(TOKEN)