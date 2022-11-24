import os
import discord
from dotenv import load_dotenv
import NbaTeamIdEnum
from ApiService import ApiService

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
API_KEY = os.getenv('API_KEY')

client = discord.Client(intents=discord.Intents.all())
api_service = ApiService(API_KEY)


def convert_team_stats_to_message(team_stats):
    message = (f'{team_stats["team_name"]} \n'
               f"Standings Rank: {team_stats['standings_rank']} \n"
               f"Games Played: {team_stats['games_played']} \n"
               f"Record (Wins/Losses): {team_stats['games_won']} - {team_stats['games_lost']} \n")

    return message

def convert_standings_to_message(standings):
    message = ''
    for key, value in standings.items():
        print(key)
        message += f'{key} {value[0]}  {value[1]} - {value[2]} \n'

    return message


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
        team_id = NbaTeamIdEnum.NbaTeamId[team_name].value
        stats = api_service.get_team_stats(team_id)
        await message.channel.send(convert_team_stats_to_message(stats))

    if message.content[0:21] == '!basketball standings':
        standings = api_service.get_nba_standings()
        await message.channel.send(convert_standings_to_message(standings))

    if message.content == '!basketball help':
        bot_message = ('Current Working Commands \n'
                       '`!basketball teamstats` TEAM_NAME \n'
                       'ex: `!basketball teamstats` BOSTON_CELTICS')
        await message.channel.send(bot_message)


client.run(TOKEN)
