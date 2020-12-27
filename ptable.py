from typing import Text
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import sys
# print(sys.argv)

# default league
league = "epl"
if(len(sys.argv) > 1):
    league = sys.argv[1]

# URL for different leagues
URL = {"epl": "https://www.espn.in/football/standings/_/league/eng.1",
       "laliga": "https://www.espn.in/football/standings/_/league/esp.1",
       "ger": "https://www.espn.in/football/standings/_/league/ger.1",
       "ita": "https://www.espn.in/football/standings/_/league/ita.1",
       "fra": "https://www.espn.in/football/standings/_/league/fra.1"}


r = requests.get(URL[league])

# League Name
lgname = {"epl": "English Premier League",
          "laliga": "LaLiga Santander",
          "ger": "German Bundesliga",
          "ita": "Italian Serie A",
          "fra": "French Ligue 1"}

# Scraping the data from the URLs
soup = BeautifulSoup(r.content, 'html5lib')
refs = soup.findAll('table')
name_rank = refs[0].find('tbody', attrs={'class': 'Table__TBODY'})
points_table = refs[1].find('tbody', attrs={'class': 'Table__TBODY'})
# print(name_rank.prettify())
# print(points_table.prettify())
names = name_rank.findAll('span', attrs={'class': 'dn show-mobile'})
teams = []
for data in names:
    team = data.text
    teams.append(team)
# print(teams)
nums = points_table.findAll(text=True)
# print(nums)
scores = [nums[i * 8:(i + 1) * 8]
          for i in range((len(nums) + 8 - 1) // 8)]

# print(len(scores),len(teams))


# Printing the data in tabular format
print(colored(
    f"----------------------------{lgname[league]} Table----------------------------", "red"))
print(colored("S.No\tTeam\tGP\tW\tD\tL\tF\tA\tGD\tP", "yellow"))
for i in range(len(teams)):
    color = "white"
    if i < 4:  # UCL
        color = "green"
    elif i < 6:  # UEL
        color = "cyan"
    elif i >= len(teams)-3:  # Relegation
        color = "magenta"
    print(colored(
        f"{i+1}\t{teams[i]}\t{scores[i][0]}\t{scores[i][1]}\t{scores[i][2]}\t{scores[i][3]}\t{scores[i][4]}\t{scores[i][5]}\t{scores[i][6]}\t{scores[i][7]}", color))
