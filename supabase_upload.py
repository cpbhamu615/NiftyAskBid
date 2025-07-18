from SmartApi import SmartWebSocket, SmartConnect
import pickle
import time

# Angel One Credentials (replace with your keys)
api_key = "4TsVPFmc"
client_id = "C38390"
pwd = "9024"
totp = "123456"   # (Use Google Authenticator OTP)

# Create SmartConnect object
obj = SmartConnect(api_key=api_key)
data = obj.generateSession(client_id, pwd, totp)

feedToken = data['feedToken']
client_code = data['data']['clientcode']

# Define token mapping (replace these tokens with actual Angel One tokens of Nifty options)
token_mapping = {
    "NIFTY25200CE": "260123",  # Example token
    "NIFTY25150PE": "260124",
    "NIFTY25300CE": "260125",
    "NIFTY25000PE": "260126"
}

# Data structure to store bids/asks
live_data = {}
for symbol in token_mapping:
    live_data[symbol] = {
        "bid": [],
        "ask": [],
        "ltp": 0
    }

def on_data(wsapp, message):
    global live_data
    for symbol, token in token_mapping.items():
        if message['token'] == token:
            ltp = message['ltp']
            bids = message['bestFive']['buy']
            asks = message['bestFive']['sell']

            live_data[symbol]['ltp'] = ltp
            live_data[symbol]['bid'] = [[b['price'], b['quantity']] for b in bids]
            live_data[symbol]['ask'] = [[s['price'], s['quantity']] for s in asks]

    # Save to pickle
    with open("live_data.pkl", "wb") as f:
        pickle.dump(live_data, f)

def on_error(wsapp, message):
    print("Error:", message)

def on_close(wsapp):
    print("Closed")

def on_open(wsapp):
    print("Connection opened")
    wsobj.subscribe(token_mapping.values(), feedToken, client_code, "mw")

wsobj = SmartWebSocket(feedToken, client_code)

wsobj.on_data = on_data
wsobj.on_error = on_error
wsobj.on_close = on_close
wsobj.on_open = on_open

wsobj.connect()