# Simulated raw data from a sports database for today's games
import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime

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

    # C) Send data over the internet to Telegram.
    response = requests.post(url, json=payload)

    # D) Return the response so you can see if Telegram accepted it
    return response.json()


# =====================================================================
# PILLAR 1: THE DAILY DIGEST
# =====================================================================

def send_daily_digest(all_matches):
    """
    Filters today's matches for the World Cup, builds a summary message,
    and sends a single morning notification to Telegram.
    """
    #1.1 Extracts the daily WC games and prepares the info
    TARGET_LEAGUE_ID = 914609
    world_cup_matches = ""
    
    for match in all_matches:
        if match["leagueId"] == TARGET_LEAGUE_ID:
            home_name = match["home"]["name"]
            away_name = match["away"]["name"]
            time = match["time"]
            formatted_time = datetime.strptime(time, "%d.%m.%Y %H:%M")
            match_info = f"{home_name} vs {away_name} at {formatted_time.hour}:{formatted_time.minute}\n"
            world_cup_matches += match_info
        else:
            pass
            
    #1.2 Sends the info to telegram        
    send_telegram_message(world_cup_matches)
        
    #1.3 Return the filtered games so our master script knows what games exist today!
    return world_cup_matches

# =====================================================================
# PILLAR 2: THE LIVE TRACKER
# =====================================================================
def monitor_live_game(match_id, home_team, away_team):
    """
    This function will be triggered when a game starts.
    It loops, polls the live stats API, and alerts us of goals.
    """
    print(f"🚨 Waking up tracker! Monitoring: {home_team} vs {away_team} (ID: {match_id})")
    
    # We will build this loop next! For now, a placeholder print is perfect.
    pass


# =====================================================================
# THE MASTER CONTROLLER (The Execution Zone)
# =====================================================================
if __name__ == "__main__":
    # Load your snapshot file
    with open("sample_response.json", "r") as file:
        data = json.load(file)
    raw_matches = data["response"]["matches"]
    
    # 1. Run the Daily Digest pipeline
    todays_games = send_daily_digest(raw_matches)
    
    # 2. Look ahead at the schedule to plan the live tracking
    print(f"\n📋 Master controller analyzing {len(todays_games)} scheduled games...")
