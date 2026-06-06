import os
import requests
from dotenv import load_dotenv

# 1. Wake up dotenv
load_dotenv()

# 2. Extract your hidden API key from your computer environment
API_KEY = os.getenv("SPORTS_API_KEY")

def fetch_live_matches():
    # Swap this URL out with the MATCHES endpoint URL you find on the sidebar!
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-matches-by-date"
    
    # Check the dashboard for what parameters the match endpoint needs 
    # (Usually a date like '2026-06-06' or a league ID)
    querystring = {"date":"20260606"}
    
    # Set up headers securely using your API_KEY variable
    headers = {
        "x-rapidapi-key": API_KEY,  # 👈 Look! No hardcoded string secrets here anymore.
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    # YOUR CODE HERE:
    # Trigger requests.get() passing the url, headers, and params=querystring.
    response = requests.get(url, headers=headers, params=querystring)
    
    # Parse the response to JSON data
    data = response.json()
    return data

# Test block to verify it runs smoothly
if __name__ == "__main__":
    import json # Built-in Python library for working with JSON files
    
    # 1. Grab the real live data once
  ##  live_data = fetch_live_matches()
    
    # 2. Save it to a file named 'sample_response.json'
    # 'indent=4' makes it automatically readable instead of a single giant line!
  ##  with open("sample_response.json", "w") as file:
 ##       json.dump(live_data, file, indent=4)
        
  ##  print("🎯 Snapshot saved safely to sample_response.json! No more API calls needed.")


# 1. Open and load the entire file into a variable named 'data'
with open("sample_response.json", "r") as file:
    data = json.load(file)

# 1. Drill down through 'response' then 'matches' to get your list
matches = data["response"]["matches"]

# Create an empty basket to hold ONLY the matches you want
world_cup_matches = ""

# Your target ID that you discovered from Step 1
TARGET_LEAGUE_ID = 914609  # Swap this with the actual number you find!

for match in matches:
    league_id = match["leagueId"]
    if TARGET_LEAGUE_ID == league_id:
        home_name = match["home"]["name"]
        away_name = match["away"]["name"]
        time = match["time"]
        match_info = f"Teams: {home_name} vs {away_name} at {time}\n"
        world_cup_matches += match_info
    else:
        pass

print(world_cup_matches)

