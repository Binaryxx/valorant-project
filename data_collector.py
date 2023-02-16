import pandas as pd
import requests
import pickle as pkl

# check API status; runs into 502 errors mostly, not sure why or how to resolve besides waiting and retrying
url = "https://api.henrikdev.xyz/valorant/v3/matches/na/Binaryxx/BINX"
status = requests.get(url)

if status.status_code != 200:
    print("API Status:",status.status_code,". Consult documentation and respond accordingly.")

else:
    print("API Status:",status.status_code)
    account_access = [["Binaryxx", "BINX"], ["Bayes", "BINX"], ["kobayashi", "5473"], ["nicotineistired", "8118"], ["Benfucius", "NA1"], ["Lawtm","1228"], ["Clerbert", "NA1"], 
    ["Endovascular", "5117"], ["moongirl", "sweet"], ["moon bun", "blue"], ["SeaTeaWall", "9256"], ["4balls", "42042"], ["ShaRaJa", "NA1"], ["Lezduit", "9829"], ["Pepsini","9318"], 
    ["Hashbrown", "Succ"], ["SaveMyElo","5047"], ["navisaturn", "NA1"], ["LAMA","4936"], ["Kev0ut", "NA1"]]


    # Get stored match id list to prevent appending duplicate matches; requires the file to be already made
    past_runs = []
    with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\past_matches.pkl", "rb") as match_id_file:
            try:
                while True:
                    past_runs.append(pkl.load(match_id_file))
            except:
                pass
    past_matches = sum(past_runs, []) #flatten lists of list of matches into just one list of matches

    # Initialize empty lists to store the match info in
    new_matches = [] # Empty list to store match ids captured during current file execution
    comp_data = [] # Empty list to store competitive match information
    unrated_data = [] # Empty list for unrated matches; kept just in case unrated matches will be utilized for other projects


    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # TODO: Get rid of the nested loops if possible; 
    # the entire process of collecting data then iterating through each match info to collect what is necessary requires 3 nested loops
    # Iterate through each account that we have consent for use of their match history
    print("\n Iterating through user lists")
    for username, tag in account_access:
        print("\nChecking user", username, tag)
        url = "https://api.henrikdev.xyz/valorant/v3/matches/na/"+username+"/"+tag
        response = requests.get(url)
        
        try: 
            json_response = pd.json_normalize(response.json()) # Flatten JSON structures to flat tables in order to store as a dataframe; not sure why some can't be normalized (might be because it's empty); Have not checked an individual instance to see why this happens
        except:
            print("Unable to normalize JSON file for user", username, tag)
        else:
            if "data" in json_response.columns: # Checks if there is any match history returned by the API for the user iterated through; not sure why another check is needed since I thought the normalize would catch players who does not have match histories; occurs with 502 errors
                matches = json_response["data"][0] # Select the list of match history for the user

                # Iterate through the list of matches
                for match in matches:
                    # Avoid reading matches that have been already collected; Happens due to party queueing
                    if not any(match["metadata"]["matchid"] in sublist for sublist in [past_matches, new_matches]): # Checks if the match id has been captured during this run or past runs
                        if (match["metadata"]["mode"] == "Competitive") or (match["metadata"]["mode"] == "Unrated"): # Process only competitive and unrated matches
                            # Add match id list to the list of match id list for this run to compare to in addition to the match id lists iterated in past runs
                            new_matches.append(match["metadata"]["matchid"]) 
                            if (match["metadata"]["mode"] == "Competitive"): # Append to competitive match id list if the match is competitive
                                comp_data.append(match)
                            elif (match["metadata"]["mode"] == "Unrated"): # Append to unrated match id list if the match is unrated
                                unrated_data.append(match)
                            print("New match collected for user", username, tag)
                        else: # Do not add non competitive or unrated matches to the list of matches to check; memory vs processing (a string vs a conditional check)
                            print("New match not competitive or unrated")

                    else: 
                        print("No more new matches to collect for user", username, tag) # If the first match has already been collected, the other 4 will also have been (the first match is the most recent)
                        break

            else:
                print("No 'data' column returned by API for user", username," ", tag)


    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Append new data to preexisting data files
    if new_matches:
        with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\past_matches.pkl", "ab") as match_id_file:
            pkl.dump(new_matches, match_id_file)

    if comp_data:
        with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\competitive_data.pkl", "ab") as comp_data_file:
            pkl.dump(comp_data, comp_data_file)

    if unrated_data:
        with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\unrated_data.pkl", "ab") as unrated_data_file:
            pkl.dump(unrated_data, unrated_data_file)
            
    print("\nScript has finished running")