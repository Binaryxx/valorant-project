# valorant_project

WORK IN PROGRESS: Although the code is functional, I would like to clean up readability, make code shorter, and update the presentation slides.


First personal data science project; the goal was to make a stat tracker for Valorant, specifically the win rate and pick rate of each agent; also used machine learning to prove the irrelevance of stats to skill by creating a classifier to predict what rank a player is based on stats such as headshot percentage and kast


INTRO:

As mentioned above, this is my first personal data science project, other than the IBM Capstone project that was included in the IBM Data Science Certificate. The purpose of this project was to simply redo the process done with the IBM Capstone project but apply it to a topic I was interested in. Most of the steps done in the IBM Capstone Project (with the geo visualizer through Folium as a notable exception) was done in this project. New skills and processes were also learned as I encountered new issues and problems with the project. 

Code and presentation of the files in this repository needs to be cleaned up by a lot. As of February 15, 2023, the files are just made for myself and is able to achieve what I needed them to do; however, they may not be the most efficient (lots of nested for loops that could be reduced and some redundant code that may be able to achieve with less lines) and easily understandable (no comments in some parts explaining what I am doing and why I did what I did). The data collected is also not sufficient. The data is mainly skewed towards the Gold rank which is roughly where the average is but does not collect enough data for lower and higher ranks. The sheer number of the matches are also not enough to reliably make any conclusions; However the project is working under the assumption that it is enough, assuming that I will get access to the Riot API for the full user database for a more complete picture.

The project is still technically a work in progress given the problems mentioned above; but as is, it is able to meet the goals set for the project. The files will be improved over time, but I wanted to post this first version of the project as a way to showcase using the skills learned during the IBM Data Science Certificate Course, as well as showcase the independent learning I had done to solve problems encountered which was not covered in the curriculum.


CONTEXT:
Valorant is a 5v5 tactical first person shooter game that involves 2 teams playing in a rotation of maps. The goal of the game is to either plant the spike, essentially a bomb, at designated locations in the maps or to prevent the opposing team from doing so. The game has class specializations (aka Agents) which encourages team work and proper team composition to be able to play the game effectively. Although not a make or break situation for winning, different team composition would dictate how a team could effectively play to their strengths and mititgate weaknesses of pool of agents they're playing as. 


ROADMAP:

As a road map for the chronological order of how to view these files (based on when I worked on them); begin with the Notebook folder. The order is as follows: 
  * val_prep1 (goes over the API options and exploring the API and the information provided)
  * val_prep2 (goes over what to do with the info provided by the API and what I had in mind prior to exploring the API)
      - the pkl files were created as a result of the data_collector.py file in the main branch; those contain the data contained from multiple runs since the API only provided the most recent 5 matches; to work around the 5 matches limitation, I have collected and saved matches over a span of 2 weeks so I can work more closely to what a full database would be like. 
  * val_data (goes over the data collected through the API; performing data cleaning and EDA with them to further understand what I am working with)\
  * val_independence (goes over the independence of features to one another [when I was still planning on making a team reccomender] as well as any dependencies of the features to the target label)
  * val_correlation (goes over correlation to understand the extent of the relationship between the features with one another, including the target label)
  * val_dash_outline (a notebook I used to piece together the components needed to make a working interactive dashboard to display the agent stats in Valorant, similar to how DotaBuff does it; refer to the Dashboard folder for the actual python script and a prettier version of the dashboard with the use of a stylesheet)
  * val_webscrape (went back in the process to make sure I cover the webscraping aspect done in the IBM capstone; refer to the Pro folder for the notebooks where I conducted some EDA with pro data; the data was scraped from VLR, a valorant tournaments wiki, capturing data such as agents used and match outcome)
      - val_pro_correlation (goes over the correlation of controller pick rate and win rate in the pro scene and understanding when each agent is used based on the map; this notebook specifically goes over Astra)
      - val_brim, val_omen, and val_val_viper (uses the same process with astra with the other Controller agents; CONCLUSION: Astra is the more generalized pick while others are mostly map dependent. TODO: a function should have been made for undergoing the same process for the different agents, understanding when each agent is selected per map)
  * val_ml (uses machine learning to prove whether or not one stat [or in this a collection of stats] is enough to determine how "good" a player is. There have been times where players uses a stat tracking site and uses noticeably lower stats as a way to convince them to play differently; I was able to prove that none of the stats collected was enough to determine a player's rank accurately/reliably, meaning that these stats are not an indicator whether or not a player is good and that they should enjoy the game and not fall prey to such tactics)
