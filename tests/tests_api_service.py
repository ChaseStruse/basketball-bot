import json
import unittest
from unittest.mock import MagicMock

from src.services.api_service import ApiService


class ApiServiceTests(unittest.TestCase):
    def setUp(self):
        self.apiService = ApiService('TEST_KEY')
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'team': 'team'
        }
        mock_response.get.return_value = mock_response

    def test_get_current_team_stats_returns_message_from_static_method(self):
        team_stats = {
            'standings_rank': '1',
            'team_name': 'Boston Celtics',
            'games_played': '10',
            'games_won': '9',
            'games_lost': '1',
        }
        self.apiService.data_conversion_service.convert_team_stats_json_to_dict = MagicMock(return_value=team_stats)
        expected = ((f'{team_stats["team_name"]} \n'
                     f"Standings Rank: {team_stats['standings_rank']} \n"
                     f"Games Played: {team_stats['games_played']} \n"
                     f"Record (Wins/Losses): {team_stats['games_won']} - {team_stats['games_lost']} \n"))
        self.apiService.data_conversion_service.convert_team_stats_to_message = MagicMock(return_value=expected)
        actual = self.apiService.get_current_team_stats(1)
        self.assertEqual(actual, expected)

    def test_get_current_nba_standings_returns_message_from_static_method(self):
        self.apiService.data_conversion_service.convert_standings_json_to_lists = MagicMock(return_value=([1],[2]))
        expected = 'EASTERN CONFERENCE STANDINGS \n1. Boston Celtics 10 - 1 \n' \
                   '\nWESTERN CONFERENCE \n1. Golden State Warriors 2 - 9 \n'
        self.apiService.data_conversion_service.convert_standings_to_message = MagicMock(return_value=expected)
        actual = self.apiService.get_current_nba_standings()
        self.assertEqual(actual, expected)

    def test_get_todays_games_returns_message_from_static_method(self):
        expected = 'Todays Games \nBoston Celtics: 101 vs. Phoenix Suns: 100 \n'
        self.apiService.data_conversion_service.convert_todays_games_to_string = MagicMock(return_value=expected)
        actual = self.apiService.get_todays_games()
        self.assertEqual(actual, expected)

    def tearDown(self):
        self.apiService.close()


if __name__ == '__main__':
    unittest.main()
