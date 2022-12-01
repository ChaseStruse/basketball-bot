import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from src.enums import enum_nba_team_ids
from src.services.api_service import ApiService

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')

bot = Bot(command_prefix="!", intents=discord.Intents.all())
api_service = ApiService(API_KEY)


@bot.command('basketball_teamstats')
async def basketball_team_stats(ctx, *args):
    team_name = '_'.join(args).upper()
    team_id = enum_nba_team_ids.NbaTeamId[team_name].value
    stats = api_service.get_current_team_stats(team_id)
    await ctx.send(stats)


@bot.command()
async def basketball_standings(ctx):
    await ctx.send(api_service.get_current_nba_standings())


@bot.command('basketball_todaysgames')
async def basketball_todays_games(ctx):
    await ctx.send(api_service.get_todays_games())


@bot.command()
async def basketball_help(ctx):
    bot_message = ('Current Working Commands \n'
                   '`!basketball_teamstats` Team Name \n'
                   'ex: `!basketball teamstats` Boston Celtics'
                   '\n'
                   '`!basketball_standings` \n'
                   'Gives you the current standings for this season \n'
                   '\n'
                   '`!basketball_todaysgames` \n'
                   'Gives you the scores of todays games')
    await ctx.send(bot_message)


bot.run(TOKEN)
