#!/usr/bin/env python3

from typing import Text
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import sys
from selenium import webdriver
from time import sleep
# print(sys.argv)
# default league
league = "epl"
if(len(sys.argv) > 1):
    league = sys.argv[1]

# URL for different leagues
URL = {"epl": "https://www.espn.in/football/scoreboard/_/league/eng.1",
       "laliga": "https://www.espn.in/football/scoreboard/_/league/esp.1",
       "ger": "https://www.espn.in/football/scoreboard/_/league/ger.1",
       "ita": "https://www.espn.in/football/scoreboard/_/league/ita.1",
       "fra": "https://www.espn.in/football/scoreboard/_/league/fra.1"}


# r = requests.get(URL[league])

# League Name
lgname = {"epl": "English Premier League",
          "laliga": "LaLiga Santander",
          "ger": "German Bundesliga",
          "ita": "Italian Serie A",
          "fra": "French Ligue 1"}

# Scraping the data from the URLs

opts = webdriver.FirefoxOptions()
opts.headless = True
driver = webdriver.Firefox(options=opts)
driver.get(URL[league])
# sleep(2)
html = driver.execute_script(
    "return document.getElementsByTagName('html')[0].innerHTML")
driver.quit()
soup = BeautifulSoup(html, 'html5lib')
teams = soup.findAll('span',attrs={'class':'abbrev'})

names=[]
for team in teams:
    tname = team.text
    names.append(tname)
# print(names)
scores_html = soup.findAll('span',attrs={'class':'score'})
scores = []
for score_html in scores_html:
    score = score_html.text
    score = score.strip()
    if score=='':
        score='0'
    scores.append(score)
# print(scores)
scores = [scores[i * 2:(i + 1) * 2]
          for i in range((len(scores) + 2 - 1) // 2)]
names = [names[i * 2:(i + 1) * 2]
         for i in range((len(names) + 2 - 1) // 2)]
# print(names,scores)

print(colored(
    f"----------------------------{lgname[league]} Scores----------------------------", "red"))

for i in range(len(names)):
    print(colored(f'{names[i][0]}    {scores[i][0]}', 'yellow')," - ",
          colored(f'{scores[i][1]}    {names[i][1]}', 'magenta'))
