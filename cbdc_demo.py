import streamlit as st
import pandas as pd
from datetime import datetime

st.title("💴 UAE CBDC Demo: Issuance & Distribution")

# --- Initialize Wallets ---
if "wallets" not in st.session_state:
    st.session_state.wallets = {
        "CBUAE": 0,              # Central Bank of the UAE
        "ADCB_LFI": 0,           # ADCB as Licensed Financial Institution
        "UAE-CBDC-ALICE-001": 0  # Alice's retail wallet
    }

# --- Initialize Transaction Log ---
if "tx_log" not in st.session_state:
    st.session_state.tx_log = []

# --- Display Wallet Balances ---
st.subheader("💼 Current Wallet Balances")
st.write(pd.DataFrame.from_dict(st.session_state.wallets, orient="index", columns=["Balance (AED-CBDC)"]))

# --- Step 1: Issuance ---
st.subheader("Step 1 — Issuance")
if st.button("CBUAE issues 10,000 AED-CBDC to ADCB (LFI)"):
    st.session_state.wallets["CBUAE"] -= 10000
    st.session_state.wallets["ADCB_LFI"] += 10000
    st.session_state.tx_log.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "From": "CBUAE",
        "To": "ADCB_LFI",
        "Amount": 10000,
        "Purpose": "CBDC Issuance to LFI"
    })
    st.success("✅ CBUAE issued 10,000 AED-CBDC to ADCB (LFI)")

# --- Step 2: Distribution ---
st.subheader("Step 2 — Distribution")
if st.button("ADCB distributes 1,000 AED-CBDC to Alice’s wallet"):
    if st.session_state.wallets["ADCB_LFI"] >= 1000:
        st.session_state.wallets["ADCB_LFI"] -= 1000
        st.session_state.wallets["UAE-CBDC-ALICE-001"] += 1000
        st.session_state.tx_log.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "From": "ADCB_LFI",
            "To": "UAE-CBDC-ALICE-001",
            "Amount": 1000,
            "Purpose": "Distribution to retail wallet"
        })
        st.success("✅ ADCB distributed 1,000 AED-CBDC to Alice’s retail wallet")
    else:
        st.error("❌ Not enough balance in ADCB wallet for distribution")

# --- Transaction Log ---
if st.session_state.tx_log:
    st.subheader("📜 Transaction History")
    st.dataframe(pd.DataFrame(st.session_state.tx_log))
