import os
import discord
from dotenv import load_dotenv
from src.enums import enum_nba_team_ids
from api_service import ApiService

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
API_KEY = os.getenv('API_KEY')

client = discord.Client(intents=discord.Intents.all())
api_service = ApiService(API_KEY)


@client.event
async def on_ready():
    try:
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print('Successfully connected')
    except:
        print('Exception when connecting')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:21] == '!basketball teamstats':
        team_name = message.content[22:]
        team_id = enum_nba_team_ids.NbaTeamId[team_name].value
        stats = api_service.get_current_team_stats(team_id)
        await message.channel.send(stats)

    if message.content == '!basketball standings':
        await message.channel.send(api_service.get_current_nba_standings())

    if message.content == '!basketball todaysgames':
        await message.channel.send(api_service.get_todays_games())

    if message.content == '!basketball help':
        bot_message = ('Current Working Commands \n'
                       '`!basketball teamstats` TEAM_NAME \n'
                       'ex: `!basketball teamstats` BOSTON_CELTICS'
                       '\n'
                       '!basketball standings \n'
                       'Gives you the current standings for this season \n'
                       '\n'
                       '!basketball todaysgames \n'
                       'Gives you the scores of todays games')
        await message.channel.send(bot_message)


client.run(TOKEN)
