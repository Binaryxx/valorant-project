import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pickle as pkl


comp_list = []
outcome_list = []
map_list = []


# Getting the soup for the URL with the list of tournaments
url = "https://www.vlr.gg/events"
response = requests.get(url).text
soup_main = BeautifulSoup(response, features="lxml")

# Getting the list of tournament links
print("\nCollecting tournaments")
tournament_list = []
for events_list in soup_main.find_all(name = "div", class_ = "events-container-col"):
    if events_list.find(name = "div", class_ = "wf-label mod-large mod-completed"): # Collect only finished tournaments
        for tournaments in events_list.find_all(name = "a", class_ = "wf-card mod-flex event-item"):
            for words in tournaments.find(name = "div", class_ = "event-item-desc-item mod-dates").get_text(strip = True).split("—"):
                if (words[:3] == "Jan"): # Collect only tournaments that have started or finished on January; Can possibly miss tournaments that is longer than 1 month
                    tournament_list.append("https://www.vlr.gg"+tournaments.attrs["href"])
print(len(tournament_list),"tournaments collected")


# Collect all the links to the games in each tournament
for tournament_link in tournament_list:

    url_tournament = tournament_link
    response_tournament = requests.get(url_tournament).text
    soup_tournament = BeautifulSoup(response_tournament, features="lxml")

    print("\nCollecting games in a tournament")
    link_list = []
    for anchor in soup_tournament.find_all(name = "a", class_ = "wf-module-item"):
        link_list.append("https://www.vlr.gg"+anchor.attrs["href"])
    print(len(soup_tournament.find_all(name = "a", class_ = "wf-module-item")),"games collected from a tournament")
    
    # For each game; collect the game data
    print("Collecting match data from games")
    for link in link_list:
        url_game = link
        response_game = requests.get(url_game).text
        soup_game = BeautifulSoup(response_game, features="lxml")

        matches = soup_game.find_all(name = "div", class_ ="vm-stats-game")

        adj_matches = []
        # Filter out the tab that aggregates the result for all games given the game (team A vs team B summary of 3 maps played for qualifiers)
        for match in matches:
            if ((match.attrs)["data-game-id"] != "all"):
                # Filter out the tab that is empty if only 2 maps were played instead of 3
                if (match.find(name = "div", class_ = "score mod-win").string.strip() != "0"):
                    adj_matches.append(match)

        # For each match played for the game; collect info
        for match in adj_matches:
            # Collect map played
            for i in range(2):
                map_list.append(match.find(name = "div", class_ = "map").find("span").get_text(strip = True))
            # Collect match outcome
            for team in match.find_all(name = "div", class_ = "score"):
                if "mod-win" in team.attrs["class"]:
                    outcome_list.append("win")
                else:
                    outcome_list.append("lose")
            # Collect team comp
            for team in match.find_all("tbody"):
                team_comp = []

                for player in team.find_all("tr"):
                    if player.find("img"): # To cover for instances where a match was played(?) [there's a score] but no agent comp was recorded
                        team_comp.append(player.find("img").attrs["title"]) 
                    else:
                        comp_list.append(np.nan)
                        break
                if team_comp:
                    comp_list.append(team_comp)
    print("Match data collected")

print("\nPickling")
if outcome_list:
    with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\pro_outcome.pkl", "wb") as pro_outcome_file:
        pkl.dump(outcome_list, pro_outcome_file)

if comp_list:
    with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\pro_comp.pkl", "wb") as pro_comp_file:
        pkl.dump(comp_list, pro_comp_file)

if map_list:
    with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\pro_map.pkl", "wb") as pro_map_file:
        pkl.dump(map_list, pro_map_file)
print("Pickled")

print("\nScript has finished running")