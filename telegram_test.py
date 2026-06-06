import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN") 
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
 

def send_telegram_message(message_text):
    ## Define the Telegram URL for sending messages
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
   
    ## Define dictionary with CHAT_ID and TOKEN
    payload = {
        "chat_id":CHAT_ID,
        "text":message_text
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

# STEP 4: Test it!
# Call your function down here with a test string like "Hello from Python!"
# and print the result.

print(send_telegram_message('Hola amorcito corazon que yo amo un monton'))