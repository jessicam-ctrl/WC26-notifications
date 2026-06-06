# Simulated raw data from a sports database for today's games
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN") 
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message_text):
    ## Define the Telegram URL for sending messages
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
   
    ## Define dictionary with CHAT_ID and TOKEN
    payload = {
        "chat_id":CHAT_ID,
        "text":message_text,
        "parse_mode": "Markdown"
    }

    # C) Send the letter over the internet.
    # Use requests.post(). You need to pass it two things: 
    # 1. The url
    # 2. The payload. (Crucial hpipint: Use the `json=` parameter, NOT `data=`, 
    #    so requests automatically formats your dictionary into JSON).
    print(f"DEBUG: My script is trying to hit: {url}")
    response = requests.post(url, json=payload)

    # D) Return the response so you can see if Telegram accepted it
    return response.json()


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

# Test your logic locally in the console first

print(world_cup_matches)


print(send_telegram_message(world_cup_matches))