# Simulated raw data from a sports database for today's games
import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

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
    daily_greeting = "*Los juegos del Mundial 26 de hoy*\n\n"
    #1.1 Extracts the daily WC games and prepares the info
    TARGET_LEAGUE_ID = 914609
    world_cup_matches = []
    
    for match in all_matches:
        if match["leagueId"] == TARGET_LEAGUE_ID:
            home_name = match["home"]["name"]
            away_name = match["away"]["name"]
            time = match["time"]
            utc_clock = datetime.strptime(time, "%d.%m.%Y %H:%M")
            arg_clock = utc_clock - timedelta(hours=6)
            clean_time = arg_clock.strftime("%H:%M")
            clean_date = arg_clock.strftime("%d.%M.%Y")
            match_info = f"{home_name} vs {away_name} as {clean_time} hs\n"
            world_cup_matches.append(match_info)
        else:
            pass
        
    #1.2 Sends the info to telegram        
    txt_wcm = "\n".join(world_cup_matches)
    final_message = daily_greeting + txt_wcm
    send_telegram_message(final_message)
        
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
    # 1. Load the data
    with open("sample_response.json", "r") as file:
        data = json.load(file)
    raw_matches = data["response"]["matches"]
    
    # 2. Run the digest (hands back our list of filtered, time-shifted WC dictionaries)
    todays_games = send_daily_digest(raw_matches)
    
    # 3. Grab the exact current time right now
    current_time = datetime.now()
    print(f"\n⏰ System check: Current local time is {current_time.strftime('%d.%m.%Y %H:%M')}")
    
    # ==========================================
    # YOUR MISSION STARTS HERE
    # ==========================================
    print(f"📋 Analyzing {len(todays_games)} World Cup matches for live tracking...")
    
    for game in todays_games:
        # A. Extract the raw time string from the game dictionary
        raw_time = data["response"]["matches"]["time"]
        # B. Parse it into a datetime object AND subtract your 6 hours!
        #    (Let's call this variable 'game_start_time')
        game_start_time = datetime.strptime(raw_time, "%d.%m.%Y %H:%M") - timedelta(hours=6)
        # C. Write an IF/ELSE statement to compare the times:
        # Hint: You can compare datetime objects directly using < or > symbols!
        if game_start_time <= current_time:
            # The game has already started or is happening right now!
            monitor_live_game(todays_games)
            
        else:
            # The game is scheduled for later
            print(f"⏳ {game['home']['name']} vs {game['away']['name']} is in the future. Waiting until kickoff.")