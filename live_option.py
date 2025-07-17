import streamlit as st
import pickle
import time

st.set_page_config(layout="wide")
st.title("📊 Nifty Option Live Bid-Ask Tracker (Top 20)")

while True:
    try:
        with open("live_data.pkl", "rb") as f:
            data = pickle.load(f)

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

        time.sleep(1)
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(2)