from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

import numpy as np
import pandas as pd


class ShotChart:
    def __init__(self, name, season, mode):
        self.nba_players = players.get_players()
        self.name = name
        self.season_id = season
        self.mode = mode

        self.made_map = np.zeros((50, 42))
        self.total_map = np.zeros((50, 42))

        self.percentage_map = np.full((50, 42), -1.0)
        self.extract_data()
        self.create_map()

    def create_map(self):
        for i in range(len(self.total_map)):
            for j in range(len(self.total_map[0])):
                count = self.total_map[i][j]
                if count != 0:
                    self.percentage_map[i][j] = self.made_map[i][j] / count

    def extract_data(self):
        target_dict = []

        found = False
        for player in self.nba_players:
            if player['full_name'].lower() == self.name.lower():
                target_dict = player
                found = True

        if not found:
            print("Player not found.")
            return

        # career dataframe
        career = playercareerstats.PlayerCareerStats(player_id=target_dict['id'])
        career_df = career.get_data_frames()[0]

        # team id during the season
        team_id_series = career_df[career_df['SEASON_ID'] == self.season_id]['TEAM_ID']
        if not team_id_series.empty:
            team_id = int(team_id_series.iloc[0])
        else:
            print("Season data not found for player.")
            return

        shotchartlist = shotchartdetail.ShotChartDetail(
            team_id=team_id,
            player_id=int(target_dict['id']),
            season_type_all_star='Regular Season',
            season_nullable=self.season_id,
            context_measure_simple="FGA").get_data_frames()

        player_shotchart_df = shotchartlist[0]

        # Depending on mode, show specific heat map
        x_missed, y_missed, x_made, y_made = self.get_shots(player_shotchart_df)

        # Calculate the made shots and total shots map (used to create the percentage heat map)
        for i in range(0, len(x_made)):
            x_exact = x_made[i]
            y_exact = y_made[i]

            x = (250 + x_exact) // 10
            y = (52 + y_exact) // 10

            if 0 <= x < 50 and 0 <= y < 42:
                self.made_map[x][y] += 1
                self.total_map[x][y] += 1

        for j in range(0, len(x_missed)):
            x_exact = x_missed[j]
            y_exact = y_missed[j]

            x = (250 + x_exact) // 10
            y = (52 + y_exact) // 10

            if 0 <= x < 50 and 0 <= y < 42:
                self.total_map[x][y] += 1

    def get_shots(self, player_shotchart_df):
        if self.mode == 'paint':
            x_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('In The Paint (Non-RA)' or 'Restricted Area')]['LOC_X'].tolist()
            y_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('In The Paint (Non-RA)' or 'Restricted Area')]['LOC_Y'].tolist()

            x_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('In The Paint (Non-RA)' or 'Restricted Area')]['LOC_X'].tolist()
            y_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('In The Paint (Non-RA)' or 'Restricted Area')]['LOC_Y'].tolist()

        elif self.mode == 'midrange':
            x_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == 'Mid-Range']['LOC_X'].tolist()
            y_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == 'Mid-Range']['LOC_Y'].tolist()

            x_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == 'Mid-Range']['LOC_X'].tolist()
            y_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == 'Mid-Range']['LOC_Y'].tolist()

        elif self.mode == 'threes':
            x_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('Above the Break 3' or 'Left Corner 3' or 'Right Corner 3')]['LOC_X'].tolist()
            y_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('Above the Break 3' or 'Left Corner 3' or 'Right Corner 3')]['LOC_Y'].tolist()

            x_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('Above the Break 3' or 'Left Corner 3' or 'Right Corner 3')]['LOC_X'].tolist()
            y_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot'][player_shotchart_df['SHOT_ZONE_BASIC'] == ('Above the Break 3' or 'Left Corner 3' or 'Right Corner 3')]['LOC_Y'].tolist()

        else:
            x_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot']['LOC_X'].tolist()
            y_missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot']['LOC_Y'].tolist()

            x_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot']['LOC_X'].tolist()
            y_made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot']['LOC_Y'].tolist()

        return x_missed, y_missed, x_made, y_made
