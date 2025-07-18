import streamlit as st
import pickle
import requests

st.set_page_config(layout="wide")
st.title("📊 NiftyAskBid - Live Bid/Ask Tracker")

url = "https://firebasestorage.googleapis.com/v0/b/niftyaskbid-XXXX.appspot.com/o/live_data.pkl?alt=media"

response = requests.get(url)
data = pickle.loads(response.content)

for symbol in data.keys():
    st.header(f"🔹 {symbol}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 20 Bid Qty")
        st.table(data[symbol]['bid'])

    with col2:
        st.subheader("Top 20 Ask Qty")
        st.table(data[symbol]['ask'])

    st.markdown(f"LTP: {data[symbol]['ltp']}")