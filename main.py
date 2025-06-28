import requests
import time
from datetime import datetime
import requests
import time
from datetime import datetime

BOT_TOKEN = '7561132734:AAGy6qJnISJEb2daEsxKBMVcRDluITIpO0I'
CHAT_ID = '1554765982'
API_KEY = 'bf830b9cce66f5476f9e1bfb1e78881a'
REGION = 'eu'
SPORT = 'soccer'
MARKET = 'totals'
INTERVAL = 300
CHANGE_THRESHOLD = 10
TRACKED_TOTALS = ['0.5', '1.5', '2.5', '3.5']

previous_odds = {}

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    try:
        resp = requests.post(url, data=data)
        if resp.status_code != 200:
            print(f"[TG Error] {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[TG Exception] {e}")

def log_to_file(text):
    with open("signals_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} — {text}\n\n")

while True:
    print("=== Check The Odds API ===")
    try:
        resp = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?regions={REGION}&markets={MARKET}&apiKey={API_KEY}')
        print(f"[API] Status: {resp.status_code}")
        if resp.status_code != 200:
            print("[API Error]", resp.text)
            time.sleep(INTERVAL)
            continue

        data = resp.json()
        signals = False

        for m in data:
            mid = m.get('id', m['home_team'] + "_" + m['away_team'])
            for bm in m.get('bookmakers', []):
                for mk in bm.get('markets', []):
                    if mk['key'] != 'totals': continue
                    for out in mk.get('outcomes', []):
                        tot = str(out.get('point'))
                        name = out.get('name')
                        cur = out.get('price')
                        if name != "Over" or tot not in TRACKED_TOTALS: continue
                        if not cur: continue

                        key = f"{mid}_{tot}_{name}"
                        old = previous_odds.get(key)
                        if old:
                            pct = ((old - cur) / old) * 100
                            if pct >= CHANGE_THRESHOLD:
                                signals = True
                                msg = (
                                    f"📉 <b>Прогруз на тотал!</b>\n"
                                    f"Матч: {m['home_team']} vs {m['away_team']}\n"
                                    f"Тотал: Over {tot}\n"
                                    f"Было: {old} → Стало: {cur}\n"
                                    f"Снижение: {pct:.1f}%\n"
                                    f"Источник: {bm['title']}"
                                )
                                print(msg)
                                send_telegram_message(msg)
                                log_to_file(msg)
                        previous_odds[key] = cur

        if not signals:
            print("[No signals]")
        time.sleep(INTERVAL)
    except Exception as e:
        print("[Loop Exception]", e)
        time.sleep(INTERVAL)
BOT_TOKEN = '7561132734:AAGy6qJnISJEb2daEsxKBMVcRDluITIpO0I'
CHAT_ID = '1554765982'
API_KEY = 'bf830b9cce66f5476f9e1bfb1e78881a'
REGION = 'eu'
SPORT = 'soccer'
MARKET = 'totals'
INTERVAL = 300
CHANGE_THRESHOLD = 10
TRACKED_TOTALS = ['0.5', '1.5', '2.5', '3.5']

previous_odds = {}

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    try:
        resp = requests.post(url, data=data)
        if resp.status_code != 200:
            print(f"[TG Error] {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[TG Exception] {e}")

def log_to_file(text):
    with open("signals_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} — {text}\n\n")

while True:
    print("=== Check The Odds API ===")
    try:
        resp = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?regions={REGION}&markets={MARKET}&apiKey={API_KEY}')
        print(f"[API] Status: {resp.status_code}")
        if resp.status_code != 200:
            print("[API Error]", resp.text)
            time.sleep(INTERVAL)
            continue

        data = resp.json()
        signals = False

        for m in data:
            mid = m.get('id', m['home_team'] + "_" + m['away_team'])
            for bm in m.get('bookmakers', []):
                for mk in bm.get('markets', []):
                    if mk['key'] != 'totals': continue
                    for out in mk.get('outcomes', []):
                        tot = str(out.get('point'))
                        name = out.get('name')
                        cur = out.get('price')
                        if name != "Over" or tot not in TRACKED_TOTALS: continue
                        if not cur: continue

                        key = f"{mid}_{tot}_{name}"
                        old = previous_odds.get(key)
                        if old:
                            pct = ((old - cur) / old) * 100
                            if pct >= CHANGE_THRESHOLD:
                                signals = True
                                msg = (
                                    f"📉 <b>Прогруз на тотал!</b>\n"
                                    f"Матч: {m['home_team']} vs {m['away_team']}\n"
                                    f"Тотал: Over {tot}\n"
                                    f"Было: {old} → Стало: {cur}\n"
                                    f"Снижение: {pct:.1f}%\n"
                                    f"Источник: {bm['title']}"
                                )
                                print(msg)
                                send_telegram_message(msg)
                                log_to_file(msg)
                        previous_odds[key] = cur

        if not signals:
            print("[No signals]")
        time.sleep(INTERVAL)
    except Exception as e:
        print("[Loop Exception]", e)
        time.sleep(INTERVAL)
