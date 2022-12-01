class DataConversionService:
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
    def convert_todays_games_to_string(json_data):
        data = json_data['response']
        message = 'Todays Games \n'
        for data_set in data:
            message_to_append = f'{data_set["teams"]["home"]["name"]}: {data_set["scores"]["home"]["total"]} vs. ' \
                                f'{data_set["teams"]["away"]["name"]}: {data_set["scores"]["away"]["total"]} \n'
            message += message_to_append
        return message