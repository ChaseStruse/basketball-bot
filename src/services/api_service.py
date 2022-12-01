import http.client
import json
from datetime import date

from src.services.data_conversion_service import DataConversionService


class ApiService:
    def __init__(self, api_key, data_conversion_service=DataConversionService()):
        self.data_conversion_service = data_conversion_service
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
        team_stats = self.data_conversion_service.convert_team_stats_json_to_dict(json_data)
        return self.data_conversion_service.convert_team_stats_to_message(team_stats)

    def get_current_nba_standings(self):
        self.conn.request('GET', '/standings?league=12&season=2022-2023', headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        east, west = self.data_conversion_service.convert_standings_json_to_lists(json_data)
        return self.data_conversion_service.convert_standings_to_message(east, west)

    def get_todays_games(self):
        self.conn.request('GET', f'/games?league=12&season=2022-2023&date={date.today()}', headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        return self.data_conversion_service.convert_todays_games_to_string(json_data)

    def close(self):
        self.conn.close()
