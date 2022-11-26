import http.client
import json
from datetime import date


class ApiService:
    def __init__(self, api_key):
        self.conn = http.client.HTTPSConnection('v1.basketball.api-sports.io')
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'v1.basketball.api-sports.io'
        }

    def get_current_team_stats(self, team_id):
        self.conn.request('GET', f'/standings?league=12&season=2022-2023&team={team_id}', headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        team_stats = self.convert_team_stats_json_to_dict(json_data)
        return self.convert_team_stats_to_message(team_stats)

    def get_current_nba_standings(self):
        self.conn.request('GET', '/standings?league=12&season=2022-2023', headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        east, west = self.convert_standings_json_to_lists(json_data)
        return self.convert_standings_to_message(east, west)

    def get_todays_games(self):
        # "America/Chicago"
        self.conn.request('GET', f'/games?league=12&season=2022-2023&date={date.today()}', headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        return self.convert_games_to_string(json_data)

    @staticmethod
    def convert_team_stats_json_to_dict(json_data):
        response = json_data['response'][0][0]
        team_stats = {
            'standings_rank': response['position'],
            'team_name': response['team']['name'],
            'games_played': response['games']['played'],
            'games_won': response['games']['win']['total'],
            'games_lost': response['games']['lose']['total'],
        }
        return team_stats

    @staticmethod
    def convert_team_stats_to_message(team_stats):
        message = (f'{team_stats["team_name"]} \n'
                   f"Standings Rank: {team_stats['standings_rank']} \n"
                   f"Games Played: {team_stats['games_played']} \n"
                   f"Record (Wins/Losses): {team_stats['games_won']} - {team_stats['games_lost']} \n")

        return message

    @staticmethod
    def convert_standings_json_to_lists(json_data):
        data = json_data['response'][0]
        eastern_conference = []
        western_conference = []
        for data_set in data:
            conference = data_set['group']['name']
            if conference == 'Western Conference':
                western_conference.append(data_set)
            elif conference == 'Eastern Conference':
                eastern_conference.append(data_set)

        return eastern_conference, western_conference

    @staticmethod
    def convert_standings_to_message(eastern_conf, western_conf):
        message = 'EASTERN CONFERENCE STANDINGS \n'
        for team in eastern_conf:
            append_message = f'{team["position"]}. {team["team"]["name"]} {team["games"]["win"]["total"]} - {team["games"]["lose"]["total"]} \n'
            message += append_message
        message += '\nWESTERN CONFERENCE \n'
        for team in western_conf:
            append_message = f'{team["position"]}. {team["team"]["name"]} {team["games"]["win"]["total"]} - {team["games"]["lose"]["total"]} \n'
            message += append_message
        return message

    @staticmethod
    def convert_games_to_string(json_data):
        data = json_data['response']
        message = 'Todays Games \n'
        for data_set in data:
            message_to_append = f'{data_set["teams"]["home"]["name"]}: {data_set["scores"]["home"]["total"]} vs. ' \
                                f'{data_set["teams"]["away"]["name"]}: {data_set["scores"]["away"]["total"]} \n'
            message += message_to_append
        return message

    def close(self):
        self.conn.close()
