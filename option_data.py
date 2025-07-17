import pickle
import time
import threading
from smartapi import SmartConnect, WebSocket
import firebase_admin
from firebase_admin import credentials, storage
import json

# Angel One API Setup
api_key = "4TsVPFmc"
client_id = "C38390"
client_secret = "a1fe0499-1017-42c0-9d11-1668312fa61a"
pin = "9024"

obj = SmartConnect(api_key)
data = obj.generateSession(client_id, client_secret, pin)
feedToken = obj.getfeedToken()
refreshToken = data['data']['refreshToken']

# Load tokens.json
with open("tokens.json") as f:
    token_data = json.load(f)

live_data = {}

for symbol, token in token_data.items():
    live_data[symbol] = {
        "bid": [],
        "ask": [],
        "ltp": 0
    }

# Firebase Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'YOUR_BUCKET_NAME.appspot.com'  # Replace with your actual Firebase bucket name
})

bucket = storage.bucket()

def upload_to_firebase():
    blob = bucket.blob("live_data.pkl")
    blob.upload_from_filename("live_data.pkl")
    blob.make_public()
    print(f"Uploaded to Firebase: {blob.public_url}")
    return blob.public_url

def save_data():
    while True:
        with open("live_data.pkl", "wb") as f:
            pickle.dump(live_data, f)
        upload_to_firebase()
        time.sleep(1)

threading.Thread(target=save_data, daemon=True).start()

def on_message(wsapp, message):
    global live_data
    res = json.loads(message)
    if res['t'] == 'tk':
        token = str(res['tk'])
        for symbol, tkn in token_data.items():
            if tkn == token:
                # Update LTP, Bid, Ask
                live_data[symbol]['ltp'] = res['lp']

                live_data[symbol]['bid'].append({
                    "qty": res['bq'],
                    "price": res['bp'],
                    "time": time.strftime("%H:%M:%S")
                })
                live_data[symbol]['ask'].append({
                    "qty": res['sq'],
                    "price": res['sp'],
                    "time": time.strftime("%H:%M:%S")
                })

                # Keep only top 20 by qty
                live_data[symbol]['bid'] = sorted(live_data[symbol]['bid'], key=lambda x: -x['qty'])[:20]
                live_data[symbol]['ask'] = sorted(live_data[symbol]['ask'], key=lambda x: -x['qty'])[:20]

# WebSocket Setup
ws = WebSocket(obj, feedToken, client_id)

ws.on_ticks = on_message
ws.subscribe(list(token_data.values()), mode='full')
ws.run_forever()