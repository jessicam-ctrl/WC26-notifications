# ⚽ World Cup 2026 Live Match Notifier

A lightweight Python backend service that fetches live soccer match data 
from a third-party REST API, filters out irrelevant fixtures, and pushes 
formatted, real-time match reports directly to a personal Telegram channel.


## 🚀 Features
- **Live Data Ingestion:** Integrated with the RapidAPI Football service to pull real-time match data.
- **Custom Data Filtering:** Built a robust business-logic filter to isolate specific tournament `leagueId` fields from hundreds of global club fixtures.
- **Asynchronous Notifications:** Wired directly into the Telegram Bot API using structured JSON payloads to deliver instant match schedules.
- **Environment Security:** Leveraged `python-dotenv` to isolate API keys and chat tokens from public version control.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** `requests`, `python-dotenv`
- **External APIs:** Telegram Bot API, RapidAPI (Free API Live Football Data)
- **Environment:** Linux (Fedora) / virtualenv

## 💻 Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/WC26-notifications.git](https://github.com/your-username/WC26-notifications.git)
cd WC26-notifications

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

