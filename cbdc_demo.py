import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize balances
if "balances" not in st.session_state:
    st.session_state.balances = {"Alice": 1000, "Bob": 500}

st.title("💱 CBDC Wallet-to-Wallet Demo")

# Show balances
st.subheader("Current Balances")
st.write(pd.DataFrame.from_dict(st.session_state.balances, orient="index", columns=["Balance (CBDC)"]))

# Transfer form
st.subheader("Make a Transfer")
sender = st.selectbox("Sender", list(st.session_state.balances.keys()))
receiver = st.selectbox("Receiver", [u for u in st.session_state.balances if u != sender])
amount = st.number_input("Amount to Transfer", min_value=1, max_value=10000, step=1)
purpose = st.text_input("Purpose of Payment", "General transfer")

if st.button("Submit Transaction"):
    if amount <= st.session_state.balances[sender]:
        st.session_state.balances[sender] -= amount
        st.session_state.balances[receiver] += amount
        st.success(f"✅ {amount} CBDC transferred from {sender} to {receiver} for '{purpose}'")

        # Log transaction
        if "tx_log" not in st.session_state:
            st.session_state.tx_log = []
        st.session_state.tx_log.append(
            {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             "Sender": sender,
             "Receiver": receiver,
             "Amount": amount,
             "Purpose": purpose}
        )
    else:
        st.error("❌ Insufficient balance")

# Transaction history
if "tx_log" in st.session_state:
    st.subheader("Transaction History")
    st.dataframe(pd.DataFrame(st.session_state.tx_log))
