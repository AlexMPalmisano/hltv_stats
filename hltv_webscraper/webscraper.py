from bs4 import BeautifulSoup
from time import sleep
from maps import MAPS

import pandas as pd

with open("raw.html", "r") as html:
    html = str(html.readlines())

source = BeautifulSoup(html, 'lxml')

players = source.find_all('tr', class_=['group-2 first', 'group-2', 'group-1 first', 'group-1'])

dataframe = []
for player in players:
    date = player.find('div', class_='time').text

    span_elements = player.find_all('span')

    player_team = span_elements[0].text
    opponent = span_elements[2].text

    map = MAPS[player.find('td', class_='statsMapPlayed').text]
    kd = player.find('td', class_='statsCenterText').text.replace(' ', '')
    plus_minus = player.find('td', class_=['gtSmartphone-only centerStat lost', 'gtSmartphone-only centerStat won',
                                           'gtSmartphone-only centerStat']).text
    rating = player.find('td',
                         class_=['match-lost ratingNegative', 'match-lost ratingPositive', 'match-won ratingNegative',
                                 'match-won ratingPositive']).text

    player_team_score = span_elements[1].text
    opponent_score = span_elements[3].text

    dataframe.append([date, player_team, opponent, map, kd, plus_minus, rating])

    if False:
        print(f"""
            Date: {date}
            Player Team: {player_team}
            Opponent: {opponent}
            Map: {map}
            K-D: {kd}
            +/-: {plus_minus}
            Rating: {rating}
            Rounds Won: {player_team_score}
            Rounds Lost: {opponent_score}
            Player Team Score: {}
            Opponent Team Score: {}
            """)

df = pd.DataFrame(dataframe, columns=['Data', 'Player Team', 'Opponent', 'Map', 'K-D', '+/-', 'Rating', 'Rounds Won', 'Rounds Lost', 'Player Team Score', 'Opponent Team Score'])
df.to_excel("output.xlsx")
