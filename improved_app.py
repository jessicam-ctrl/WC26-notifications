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
# STEP 1: DATA EXTRACTION LAYER (The "SQL Query" equivalent)
# =====================================================================
def get_todays_wc_matches(all_matches):
    """
    Acts like a SQL WHERE clause. Takes 128 raw matches, 
    applies the 6-hour timezone shift, filters by league,
    and returns a clean list of ONLY today's World Cup dictionaries.
    """
    TARGET_LEAGUE_ID = 914609
    curated_games = []
    
    for match in all_matches:
        if match["leagueId"] == TARGET_LEAGUE_ID:
            # 1. Do your 6-hour datetime subtraction right here
            uhc_clock = datetime.strptime(match["time"], "%d.%m.%Y %H:%M")
            arg_clock = uhc_clock - timedelta(hours=6)
            # 2. Create new dictiodnary with only information we want
            slim_match = {
                "match_id":match["id"],
                "league_id":match["leagueId"],
                "kickoff_time":arg_clock,
                "home_team":match["home"]["name"],
                "away_team":match["away"]["name"],
            }
            curated_games.append(slim_match)
        else:
            pass    
    return curated_games # Returns a pristine list of dicts


# =====================================================================
# STEP 2: PRESENTATION LAYER (The "Reporting Engine")
# =====================================================================
def send_daily_digest(curated_games):
    """
    Takes the already curated list, runs your string-building logic,
    and sends the morning message. It doesn't care about league IDs anymore!
    """
    match_message = ""
    # 1. Take the curated_games list
    for game in curated_games:
        time = game['kickoff_time']
        match_info = f"{game['home_team']} vs {game['away_team']} as {time.strftime('%H:%M')} hs\n"
        match_message += match_info
    
    daily_greeting = "*Los juegos del Mundial 26 de hoy*\n\n"
    final_message = daily_greeting + match_message
    # 3. Call send_telegram_message(text_message)
    send_telegram_message(final_message)


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
    todays_games = get_todays_wc_matches(raw_matches)

    # 3. Sends the daily matches message to Telegram
    send_daily_digest(todays_games)
    
    # 4. Grab the exact current time right now
    current_time = datetime.now()
    print(f"\n⏰ System check: Current local time is {current_time.strftime('%d.%m.%Y %H:%M')}")
    print(f"📋 Analyzing {len(todays_games)} World Cup matches for live tracking...")
    # 5. Determine whether there is an active game at the moment
    for game in todays_games:
    # 5.1. Grab your pre-calculated datetime object out of the game dictionary
        game_start = game["kickoff_time"]
    
    # 5.3 Time comparison math logic:
        game_time_window = game_start + timedelta(minutes=90)
        if game_start <= current_time and game_time_window > current_time:
        # Trigger your live worker engine!
            monitor_live_game(game["match_id"], game["home_team"], game["away_team"])
        elif game_start > current_time:
            print(f"⏳ {game['home_team']} hasn't kicked off yet.")
        else:
            print(f"⏳ {game['home_team']} vs {game['away_team']} has ended.")