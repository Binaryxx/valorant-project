import pickle as pkl
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Retrieves the match histories collected
runs = []
with open("C:\\Users\\Binaryxx Sune\\Documents\\Programming\\personal_projects\\data\\competitive_data.pkl", "rb") as comp_data_file: # Change path to competitive data pickle file if needed
    try:
        while True:
                runs.append(pkl.load(comp_data_file))
    except:
        pass
matches = sum(runs, []) # Flattens the list of lists of match histories to one list of match histories

agent = []
val_map = []
rank = []
outcome = []


# Iterate through match histories to retrieve needed info
for match in matches:
        # Get map played by each player
        for i in range(10):
            val_map.append(match["metadata"]["map"])

        
        for player in match["players"]["all_players"]:
            # Get agent played by each player and their rank
            agent.append(player["character"])
            rank.append(player["currenttier"])
            # Get match outcome of each player (Did they win?)
            player_team = player["team"].lower()
            outcome.append(match["teams"][player_team]["has_won"])


# Assign collected info into a dataframe
data_dict = {"agent": agent, "val_map" : val_map, "rank": rank, "win": outcome}
val_data = pd.DataFrame(data_dict)

# Filter out maps that are out of competitive queue rotation
val_data = val_data[~val_data["val_map"].isin(["Breeze", "Bind"])]


# -------------------------------------------------------------------------------------------------------------------------------

# Create app object
app = dash.Dash(__name__)

# Set app elements and configurations
app.layout = html.Div(children=[html.H1("Valorant Trends Dashboard"), # Header/Title 
                                html.Br(),
                                
                                html.Div( # Rank Range Slider Div
                                    [html.H3("Rank Range Filter"),
                                    html.P("Please adjust the slider to set the minimum and maximum rank ranges; a reccomended range is one rank tier above and below (Gold 1s should select a range from Silver 1 to Platinum 1)"),
                                    dcc.RangeSlider(id="rank-slider",
                                                    min = 0,
                                                    max = 25,
                                                    step = 1,
                                                        marks={ # TODO: Use the more compact way of listing values from the df rather than manually inputting values; not sure if it'll make it more compact since I'll have to define the function that sets rank labels
                                                            0: 'Uncalibrated',
                                                            1: 'Iron 1',
                                                            2: 'Iron 2',
                                                            3: 'Iron 3',
                                                            4: 'Bronze 1',
                                                            5: 'Bronze 2',
                                                            6: 'Bronze 3',
                                                            7: 'Silver 1',
                                                            8: 'Silver 2',
                                                            9: 'Silver 3',
                                                            10: 'Gold 1',
                                                            11: 'Gold 2',
                                                            12: 'Gold 3',
                                                            13: 'Platinum 1',
                                                            14: 'Platinum 2',
                                                            15: 'Platinum 3',
                                                            16: 'Diamond 1',
                                                            17: 'Diamond 2',
                                                            18: 'Diamond 3',
                                                            19: 'Ascendant 1',
                                                            20: 'Ascendant 2',
                                                            21: 'Ascendant 3',
                                                            22: 'Immortal 1',
                                                            23: 'Immortal 2',
                                                            24: 'Immortal 3',
                                                            25: 'Radiant'
                                                            },
                                                    value = [1, 24] # Default value set to not include Radiants and Uncalibrated Players
                                                    )]),
                                html.Br(),

                                html.Div([ # Map Dropdown Div
                                    html.H3("Map Selection"),
                                    html.P("Please select a map"),
                                    dcc.Dropdown(
                                                id="map-dropdown",
                                                options = 
                                                    [
                                                        {"label": "All Maps", "value": "all"}, 
                                                        {"label": "Ascent", "value": "Ascent"}, 
                                                        {"label": "Haven", "value": "Haven"},
                                                        {"label": "Icebox", "value": "Icebox"},
                                                        {"label": "Lotus", "value": "Lotus"},
                                                        {"label": "Pearl", "value": "Pearl"},
                                                        {"label": "Fracture", "value": "Fracture"},
                                                        {"label": "Split", "value": "Split"}
                                                    ],
                                                value = "all", 
                                                placeholder = "Select a Map", 
                                                searchable = True,
                                                )]),
                                html.Br(),

                                html.Div([ # Playable Agent Checklist
                                    html.H3("Playable Agents"),
                                    html.P("Please select the agent(s) that you are able to comfortably play"),
                                    dcc.Checklist(
                                                id="agent-checklist",
                                                options = # TODO: Use the more compact way of listing values from the df rather than manually inputting values
                                                        [
                                                        {"label": "Astra", "value": "Astra"}, 
                                                        {"label": "Breach", "value": "Breach"}, 
                                                        {"label": "Brimstone", "value": "Brimstone"}, 
                                                        {"label": "Chamber", "value": "Chamber"}, 
                                                        {"label": "Cypher", "value": "Cypher"}, 
                                                        {"label": "Fade", "value": "Fade"},
                                                        {"label": "Harbor", "value": "Harbor"},
                                                        {"label": "Jett", "value": "Jett"},
                                                        {"label": "Kay/O", "value": "KAY/O"},
                                                        {"label": "Killjoy", "value": "Killjoy"},
                                                        {"label": "Neon", "value": "Neon"},
                                                        {"label": "Omen", "value": "Omen"},
                                                        {"label": "Phoenix", "value": "Phoenix"},
                                                        {"label": "Raze", "value": "Raze"},
                                                        {"label": "Reyna", "value": "Reyna"},
                                                        {"label": "Sage", "value": "Sage"},
                                                        {"label": "Skye", "value": "Skye"},
                                                        {"label": "Sova", "value": "Sova"},
                                                        {"label": "Viper", "value": "Viper"},
                                                        {"label": "Yoru", "value": "Yoru"}, 
                                                        ]
                                                )]),
                                html.Br(),
                                html.Hr(),
                                html.Br(),

                                html.Div(
                                    dcc.Graph(id="agent-success")), # Output Graph of Statistics
                                
                                html.Br(),

                                html.Div([
                                    html.P("Ideally, a minimum match count of 35 is needed to be able to somewhat rely on the statistics"),
                                    dcc.Graph(id="agent-reliability")] # Output Match Counts
                                )])


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Set Input and Output components and the function used to process the Input to the appropriate Output
@app.callback(Output(component_id='agent-success', component_property='figure'),
              Output(component_id='agent-reliability', component_property='figure'),
              Input(component_id='rank-slider', component_property='value'), 
              Input(component_id='map-dropdown', component_property='value'), 
              Input(component_id='agent-checklist', component_property='value'))


def get_agent_fig(rank_range, input_map, agent_list):
    dash_data = val_data
    low, high = rank_range

    # Filter the df by the range of ranks selected from the slider
    dash_data = dash_data[dash_data["rank"].isin(range(low, high+1))]

    # Filter the df by the input map selected with the dropdown
    if input_map != "all":
        dash_data = dash_data[dash_data["val_map"] == input_map]

    # Create the necessary features to output the win rate and pick rate
    agent_data = dash_data.groupby(["agent"], as_index = False)["win"].sum() # Create a new df grouped by agents

    # Necessary variables to calculate wanted features
    win_count = agent_data["win"].to_numpy()
    match_count = dash_data.groupby(["agent"], as_index = False)["win"].count()["win"].to_numpy()
    total_matches = match_count.sum()

    # Add the Match Count to a separate df
    reliability_data = agent_data
    reliability_data["match_count"] = match_count

    # Add the Win Rate and Pick Rate columns
    agent_data["win_rate"] = np.around((win_count / match_count) * 100, decimals = 2)
    agent_data["pick_rate"] = np.around((match_count / total_matches) * 100, decimals = 2)

    agent_data = agent_data.drop(["win"], axis = 1) # Remove win count as it is not needed
    agent_data = agent_data.drop(["match_count"], axis = 1) # Remove match count; not sure why it's included in this df

    # Filter the df based on the selected agents that the user can play in the checklist
    if agent_list:
        agent_data = agent_data[agent_data["agent"].isin(agent_list)]
    if agent_list:
        reliability_data = reliability_data[reliability_data["agent"].isin(agent_list)]

    # Transform df so that win rate and pick rate can be represented as different colored bars for each agent selected
    agent_data = pd.melt(agent_data, id_vars = "agent", var_name = "win/pick", value_name = "rates")


    # Create the visualization of the win and pick rate given the set conditions
    success_viz = px.bar(agent_data, x = "rates", y = "agent", color = "win/pick", # Select columns to set for the axis and colored bars
        orientation = "h", # Make the bars horizontal
        barmode = "group", # Have the different colored bars side to side rather than on top of each other (stacked)
        labels = { # X and Y Labels
            "rates": "Percentage (%)",
            "agent": "Agent(s)"
        },
        color_discrete_sequence = ["rgb(201, 44, 44)", "rgb(44, 201, 175)"], # Set the 2 colors used for the win rate and pick rate bar colors
        title = "Agent(s) Pick Rate and Win Rate",
        text_auto = True # Display the values of the bars next to the bars
        )
    
    # Change the labels that appear when a bar is hovered over
    success_viz.update_traces(hovertemplate = "<br>".join([ 
        "Agent: %{y}",
        "Rate: %{x}%"
    ]))

    # Replace the labels to display the set dictionary values rather than the column names in the df for the legend title and on hover
    newnames = {'win_rate':'Win Rate', 'pick_rate': 'Pick Rate'} 
    success_viz.for_each_trace(lambda t: t.update(name = newnames[t.name], # reassigns name value with what is in the dictionary
                                      legendgroup = newnames[t.name], # replaces the label on the legend
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name]) # replaces the text on hover
                                     )
                  )

    # Change the color of the background
    success_viz.update_layout({
        'plot_bgcolor': 'rgb(36, 36, 36)',
        'paper_bgcolor': 'rgb(36, 36, 36)'
    },)
    # Change the color and sizing of the labels and title
    success_viz.update_layout(
        font_color = "rgb(170, 170, 170)",
        title_font_color = "#dc3d4b",
        title_font_size = 24,
        legend_title_font_color = "#dc3d4b"
    )


    # Create a figure that shows match count to determine whether the statistic provided is reliable
    reliability_viz = px.bar(reliability_data, x = "match_count", y = "agent", # Select columns to set for the axis and colored bars
        orientation = "h", # Make the bars horizontal
        labels = { # X and Y Labels
            "match_count": "Match Count",
            "agent": "Agent(s)"
        },
        title = "Agent(s) Match Count",
        text_auto = True, # Display the values of the bars next to the bars
        color_discrete_sequence = ["rgb(201, 44, 44)"]
        )

    # Change the color of the background
    reliability_viz.update_layout({
        'plot_bgcolor': 'rgb(36, 36, 36)',
        'paper_bgcolor': 'rgb(36, 36, 36)'
    },)

    # Change the color and sizing of the labels and title
    reliability_viz.update_layout(
        font_color = "rgb(170, 170, 170)",
        title_font_color = "#dc3d4b",
        title_font_size = 24,
        legend_title_font_color = "#dc3d4b"
    )

    # Change the labels that appear when a bar is hovered over
    reliability_viz.update_traces(hovertemplate = "<br>".join([ 
        "Agent: %{y}",
        "Match Count: %{x}"
    ]))


    return success_viz, reliability_viz


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Run the app
if __name__ == '__main__':
    app.run_server()