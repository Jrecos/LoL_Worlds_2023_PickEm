#%%
import csv
from mwrogue.esports_client import EsportsClient

# Initialize the client
site = EsportsClient("lol")

# 1. Extract the teams that will participate in Worlds 2023
response = site.cargo_client.query(
    tables="Tournaments",
    fields="Participants",
    where="OverviewPage='Worlds 2023'"
)
teams = response[0]['Participants'].split(',')

# Prepare the CSV data
csv_data = []

#%%
# 2. Extract the roster of each team and 3. Extract the match history
for team in teams:
    # Roster
    roster_response = site.cargo_client.query(
        tables="TournamentRosters",
        fields="Player",
        where=f"Team='{team}' AND OverviewPage='Worlds 2023'"
    )
    roster = [player['Player'] for player in roster_response]

    # Match history
    match_response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields="DateTime_UTC,Team1,Team2,Winner",
        where=f"(Team1='{team}' OR Team2='{team}') AND OverviewPage='Worlds 2023'"
    )
    matches = [(match['DateTime_UTC'], match['Team1'], match['Team2'], match['Winner']) for match in match_response]

    # Append to CSV data
    csv_data.append({
        'Team': team,
        'Roster': ', '.join(roster),
        'Matches': ', '.join([f"{match[0]}: {match[1]} vs {match[2]} (Winner: {match[3]})" for match in matches])
    })

# 4. Save the result in a CSV file
with open('worlds_2023_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Team', 'Roster', 'Matches']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv_data:
        writer.writerow(row)


