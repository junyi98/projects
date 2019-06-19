import discord
from random import *
import random
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
import requests
from bs4 import BeautifulSoup

BOT_PREFIX = ("?", "!")
TOKEN = 'NTEyMDY3NzI5MDI5ODU3MzEx.Ds0H0Q.jLoyPVy-2BFsBvr--o2RRtnPPGw'

#client = discord.Client()

client = Bot(command_prefix=BOT_PREFIX)


# @client.event
# async def on_message(message):
#     #dont want the bot to reply itself
#     if message.author == client.user:
#         return

#     if message.content.startswith('!hello'):
#         msg = 'Hello {0.author.mention}'.format(message)
#         await client.send_message(message.channel, msg)

#     if message.content.startswith('!roll'):
#         msg = '{0.author.mention} rolled number '+randint(1,100).__str__()
#         await client.send_message(message.channel, msg.format(message))

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.command()
async def bitcoin():
    url = 'http://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command(pass_context = True)
async def hello(context):
    await client.say("Hello "+ context.message.author.mention)

@client.command()
async def exchange():
    url = 'https://api.exchangeratesapi.io/latest'
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response =  await raw_response.text()
        response = json.loads(response)
        ans = response['rates']['USD']
        await client.say("Exchange rate of EUR to USD: "+ str(ans))

@client.command(pass_context=True)
async def roll(context):
    ans = randint(1,100)
    await client.say(context.message.author.mention+" rolled "+str(ans))


@client.command()
async def lyrics(message):
    SONGTOKEN = 'pjFgK42iwmjReYuLhCjjVj8HldIjQfXIe99aqPKjmKHNSWIzoy6qBWKxpYLw4_ny'
    url = "http://api.genius.com"
    headers = {'Authorization':'Bearer '+SONGTOKEN}
    song_title = "All Too Well"
    artist_name = "Taylor Swift"
    def lyrics_from_song_api_path(song_api_path):
        song_url = url + song_api_path
        response = requests.get(song_url, headers=headers)
        json = response.json()
        path = json["response"]["song"]["path"]
        #gotta go regular html scraping... come on Genius
        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        html = BeautifulSoup(page.text, "html.parser")
        #remove script tags that they put in the middle of the lyrics
        [h.extract() for h in html('script')]
        #at least Genius is nice and has a tag called 'lyrics'!
        lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
        return lyrics

    if __name__ == "__main__":
        search = url + "/search"
        params = {'q':song_title}
        response = requests.get(search,params=params,headers=headers)
        json = response.json()
        song_info = None
        for hit in json["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"] == artist_name:
                song_info = hit
                print(song_info)
                break
        if song_info:
            song_api_path = song_info["result"]["api_path"]
            print(lyrics_from_song_api_path(song_api_path))
            msg = "Lyrics is: "+lyrics_from_song_api_path(song_api_path)
                       
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with your feelings"))
# @client.event
# async def on_ready():
#     print('Logged in as')
#     print(client.user.name)
#     print(client.user.id)
#     print('------')


client.run(TOKEN)