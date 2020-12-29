#!/usr/bin/env python3

from typing import Text
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import sys
from selenium import webdriver
from time import sleep
import time
import notify2
# print(sys.argv)


# default league
import os
league = "epl"
if(len(sys.argv) > 1):
    league = sys.argv[1]


# Notification Initialiser

ICON_PATH = '/home/codexharsh/Desktop/live_football/logo.png'
# initialise the d-bus connection
notify2.init("News Notifier")

# create Notification object
n = notify2.Notification(None, icon=ICON_PATH)

# set urgency level
n.set_urgency(notify2.URGENCY_NORMAL)

# set timeout for a notification
n.set_timeout(10000)

# URL for different leagues
URL = {"epl": "https://www.espn.in/football/scoreboard/_/league/eng.1",
       "laliga": "https://www.espn.in/football/scoreboard/_/league/esp.1",
       "ger": "https://www.espn.in/football/scoreboard/_/league/ger.1",
       "ita": "https://www.espn.in/football/scoreboard/_/league/ita.1",
       "fra": "https://www.espn.in/football/scoreboard/_/league/fra.1"}


# League Name
lgname = {"epl": "English Premier League",
          "laliga": "LaLiga Santander",
          "ger": "German Bundesliga",
          "ita": "Italian Serie A",
          "fra": "French Ligue 1"}

# Scraping the data from the URLs

# Initialising Selenium webdriver and opening URL in headless mode
opts = webdriver.FirefoxOptions()
opts.headless = True
driver = webdriver.Firefox(options=opts)
driver.get(URL[league])
iteration = 0
prevscores = []
prevnames = []

# Infinite Loop for Continuous Scores
while True:
    starttime = time.time()
    # sleep(2)
    html = driver.execute_script(
        "return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, 'html5lib')
    teams = soup.findAll('span', attrs={'class': 'abbrev'})

    names = []
    for team in teams:
        tname = team.text
        names.append(tname)
    # print(names)
    scores_html = soup.findAll('span', attrs={'class': 'score'})
    scores = []
    for score_html in scores_html:
        score = score_html.text
        score = score.strip()
        if score == '':
            score = '0'
        scores.append(score)

    game_times_html = soup.findAll('span', attrs={'class': 'game-time'})
    game_times = []
    for game_html in game_times_html:
        game_times.append(game_html.text.strip())
    # print(game_times)
    checkcnt=0
    for gtime in game_times:
        if gtime=='FT' or gtime=='HT' or gtime[-1]=='M':
            checkcnt+=1

    # print(scores)
    scores = [scores[i * 2:(i + 1) * 2]
              for i in range((len(scores) + 2 - 1) // 2)]
    names = [names[i * 2:(i + 1) * 2]
             for i in range((len(names) + 2 - 1) // 2)]
    # print(names,scores)

    print(colored(
        f"----------------------------{lgname[league]} Scores----------------------------", "red"))

    for i in range(len(names)):
        print(colored(f'{names[i][0]}\t{scores[i][0]}', 'yellow'), " - ",
              colored(f'{scores[i][1]}    {names[i][1]}', 'magenta'),f'{game_times[i]}')

    # Notifications for Goals
    if iteration > 0:
        for i in range(len(names)):
            teamA = names[i][0]
            teamB = names[i][1]
            scoreA = scores[i][0]
            scoreB = scores[i][1]
            prevscoreA = prevscores[i][0]
            prevscoreB = prevscores[i][1]
            if prevscoreA != scoreA:
                n.update(f'Goal by {teamA}!', f'{teamA}\t{scoreA}' + " - " +
                         f'{scoreB}\t{teamB}')
                n.show()
                sleep(7)
            if prevscoreB != scoreB:
                n.update(f'Goal by {teamB}!', f'{teamA}\t{scoreA}' + " - " +
                         f'{scoreB}\t{teamB}')
                n.show()
                sleep(7)
    prevscores = scores
    prevnames = names
    endtime = time.time()
    print("Results rendered in", endtime-starttime,
          "seconds!\nUpdating after 10 seconds")
    print(colored(".......", "green"))
    if checkcnt==len(game_times):
        n.update("Live Football","All Matches are currently either HT or FT or yet to begin")
        n.show()
        break
    sleep(10)
    os.system('clear')
    iteration += 1

driver.quit()
