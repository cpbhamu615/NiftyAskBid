import streamlit as st
from supabase import create_client
import pickle
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
bucket = "niftyaskbid-data"

supabase = create_client(url, key)

try:
    res = supabase.storage.from_(bucket).download("live_data.pkl")
    data = pickle.loads(res.read())
except Exception as e:
    st.error("Data load failed: "+str(e))
    st.stop()

st.title("📊 NiftyAskBid - Live Bid/Ask Tracker")

for symbol in data.keys():
    st.header(f"🔹 {symbol}")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Bids")
        st.table(data[symbol]['bid'])

    with col2:
        st.subheader("Top 5 Asks")
        st.table(data[symbol]['ask'])

    st.markdown(f"LTP: {data[symbol]['ltp']}")