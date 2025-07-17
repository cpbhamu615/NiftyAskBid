from smartapi import SmartConnect
import json

# Angel One API Setup
api_key = "4TsVPFmc"
client_id = "C38390"
client_secret = "a1fe0499-1017-42c0-9d11-1668312fa61a"
pin = "9024"

obj = SmartConnect(api_key)
data = obj.generateSession(client_id, client_secret, pin)

# Fetch Option Symbols
def get_option_tokens(symbol, expiry, strike_list, option_type):
    search_result = obj.searchscrip(exchange="NFO", symbolName=symbol)
    output = {}

    for scrip in search_result['data']:
        if scrip['symbol'].startswith(symbol) and scrip['expiry'] == expiry:
            strike = float(scrip['strikePrice'])
            if strike in strike_list and scrip['optionType'] == option_type:
                key = f"{symbol} {int(strike)} {option_type}"
                output[key] = scrip['token']

    return output

# Example input
symbol = "NIFTY"
expiry = "2025-07-24"   # <-- Update with correct expiry
strikes = [25000, 25050, 25100, 25150, 25200, 25250, 25300, 25350]

# CE and PE tokens
call_tokens = get_option_tokens(symbol, expiry, strikes, "CE")
put_tokens = get_option_tokens(symbol, expiry, strikes, "PE")

# Merge both
final_tokens = {call_tokens, put_tokens}

# Save to tokens.json
with open("tokens.json", "w") as f:
    json.dump(final_tokens, f, indent=4)

print("✅ tokens.json generated successfully!")