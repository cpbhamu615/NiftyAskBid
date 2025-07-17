from smartapi import SmartConnect
from smartapi import WebSocket
import pandas as pd
import json
import time
from datetime import datetime
import threading
import pickle

# 🔑 Angel One API Details
api_key = "4TsVPFmC"
client_id = "C38390"
pin = "9024"
totp = "YOUR_TOTP"

obj = SmartConnect(api_key=api_key)

# 🛡️ Generate Session
data = obj.generateSession(client_id, pin, totp)
refresh_token = data['data']['refreshToken']
feed_token = obj.getfeedToken()

# 🎯 Load Strike Tokens from JSON
with open('tokens.json', 'r') as f:
    tokens = json.load(f)

live_data = {}

# Initialize structure
for token, symbol in tokens.items():
    live_data[symbol] = {
        "bid": [],
        "ask": [],
        "ltp": 0
    }

def on_tick(ws, tick_data):
    for tick in tick_data:
        token = tick['token']
        symbol = tokens[str(token)]
        time_now = datetime.now().strftime("%H:%M:%S")

        ltp = tick.get('last_traded_price', 0) / 100
        bid_price = tick.get('best_bid_price', 0) / 100
        bid_qty = tick.get('best_bid_quantity', 0)
        ask_price = tick.get('best_ask_price', 0) / 100
        ask_qty = tick.get('best_ask_quantity', 0)

        # Update LTP
        live_data[symbol]['ltp'] = ltp

        # Track Top 20 Bid Qty
        live_data[symbol]['bid'].append({"qty": bid_qty, "price": bid_price, "time": time_now})
        live_data[symbol]['bid'] = sorted(live_data[symbol]['bid'], key=lambda x: x['qty'], reverse=True)[:20]

        # Track Top 20 Ask Qty
        live_data[symbol]['ask'].append({"qty": ask_qty, "price": ask_price, "time": time_now})
        live_data[symbol]['ask'] = sorted(live_data[symbol]['ask'], key=lambda x: x['qty'], reverse=True)[:20]

# 🗃️ Save live_data to file continuously
def save_data():
    while True:
        with open("live_data.pkl", "wb") as f:
            pickle.dump(live_data, f)
        time.sleep(1)

threading.Thread(target=save_data, daemon=True).start()

# 🔌 WebSocket Setup
ws = WebSocket(api_key, client_id, feed_token, obj.refreshToken)

ws.on_ticks = on_tick

token_list = list(tokens.keys())
ws.subscribe(token_list, mode="full")

ws.connect()