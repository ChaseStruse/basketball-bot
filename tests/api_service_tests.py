import json
import unittest
from unittest.mock import MagicMock

from src.api_service import ApiService


class ApiServiceTests(unittest.TestCase):
    def setUp(self):
        self.apiService = ApiService('TEST_KEY')

    def test_get_current_team_stats_returns_value_from_static_method(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'team': 'team'
        }
        mock_response.get.return_value = mock_response

        expected = {
            'test team': 'test name',
            'games': 10
        }
        self.apiService.convert_team_stats_json_to_dict = MagicMock(return_value=expected)
        actual = self.apiService.get_current_team_stats(1)
        self.assertEqual(actual, expected)

    def test_convert_team_stats_json_to_dict_returns_correct_dict_data(self):
        test_json = '{ "response": [ [ { "position": 1, "team": { "name": "Boston Celtics"}, "games": { "played": 11, ' \
                    '"win": { "total": 10 }, "lose": { "total": 1 } } } ] ] } '
        expected = {
            'standings_rank': 1,
            'team_name': 'Boston Celtics',
            'games_played': 11,
            'games_won': 10,
            'games_lost': 1
        }
        actual = self.apiService.convert_team_stats_json_to_dict(json.loads(test_json))
        self.assertEqual(actual, expected)

    def tearDown(self):
        self.apiService.close()


if __name__ == '__main__':
    unittest.main()
