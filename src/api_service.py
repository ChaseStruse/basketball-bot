import http.client
import json


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
        return self.convert_team_stats_json_to_dict(json_data)

    def get_nba_standings(self):
        self.conn.request('GET', '/standings?league=12&season=2021-2022', headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        return self.convert_standings_json_to_dict(json_data)

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
    def convert_standings_json_to_dict(json_data):
        data = json_data['response'][0][0]
        standings = {}
        team_stats = []
        team_key = ''
        for key, value in data.items():
            if key == 'position':
                team_key = value
            elif key == 'team':
                team_stats.append(value['name'])
            elif key == 'games':
                team_stats.append(value['win']['total'])
                team_stats.append(value['lose']['total'])
            elif key == 'description':
                standings = {team_key: team_stats}
                team_stats.clear()
            elif key == 'position' and value == 15:
                break
        return standings

    def close(self):
        self.conn.close()
