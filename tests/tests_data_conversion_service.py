import json
import unittest
from src.services.data_conversion_service import DataConversionService


class ApiServiceTests(unittest.TestCase):
    def setUp(self):
        self._sut = DataConversionService()

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
        actual = self._sut.convert_team_stats_json_to_dict(json.loads(test_json))
        self.assertEqual(actual, expected)

    def test_given_valid_team_stats_convert_team_stats_to_message_returns_proper_str(self):
        team_stats = {
            'standings_rank': '1',
            'team_name': 'Boston Celtics',
            'games_played': '10',
            'games_won': '9',
            'games_lost': '1',
        }
        expected = ((f'{team_stats["team_name"]} \n'
                     f"Standings Rank: {team_stats['standings_rank']} \n"
                     f"Games Played: {team_stats['games_played']} \n"
                     f"Record (Wins/Losses): {team_stats['games_won']} - {team_stats['games_lost']} \n"))
        actual = self._sut.convert_team_stats_to_message(team_stats)
        self.assertEqual(actual, expected)

    def test_given_valid_json_convert_standings_json_to_lists_returns_proper_lists(self):
        east_conf_json = '{ "group": { "name": "Eastern Conference" }, "team":{ "name":"Boston Celtics" }}'
        west_conf_json = '{"group": {"name": "Western Conference"}, "team": {"name": "Golden State Warriors"}}'
        test_json = '{ "response": [ [ { "group": { "name": "Eastern Conference" }, "team":{ "name":"Boston Celtics" ' \
                    '}}, {"group": {"name": "Western Conference"}, "team": {"name": "Golden State Warriors"}} ] ] } '
        expected_east = [json.loads(east_conf_json)]
        expected_west = [json.loads(west_conf_json)]
        actual_east, actual_west = self._sut.convert_standings_json_to_lists(json.loads(test_json))
        self.assertEqual(actual_west, expected_west)
        self.assertEqual(actual_east, expected_east)

    def test_given_valid_lists_convert_standings_to_message_returns_valid_str(self):
        east_team_json = ('{ "position": 1, "team": { "name": "Boston Celtics"}, '
                          '"games": { "played": 11, "win": { "total": 10 }, "lose": { "total": 1 } } }')
        west_team_json = ('{ "position": 1, "team": { "name": "Golden State Warriors"}, '
                          '"games": { "played": 11, "win": { "total": 2 }, "lose": { "total": 9 } } }')
        east = [json.loads(east_team_json)]
        west = [json.loads(west_team_json)]
        expected = 'EASTERN CONFERENCE STANDINGS \n1. Boston Celtics 10 - 1 \n' \
                   '\nWESTERN CONFERENCE \n1. Golden State Warriors 2 - 9 \n'
        actual = self._sut.convert_standings_to_message(east, west)
        self.assertEqual(actual, expected)

    def test_given_valid_json_convert_games_to_string_returns_valid_str(self):
        test_json = '{ "response": [ { "teams": { "home": { "name": "Boston Celtics" }, ' \
                    '"away": { "name": "Golden State Warriors"} }, ' \
                    '"scores": { "home": { "total": "101" }, "away": { "total": "99"} } } ] }'
        expected = 'Todays Games \nBoston Celtics: 101 vs. Golden State Warriors: 99 \n'
        actual = self._sut.convert_todays_games_to_string(json.loads(test_json))
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
