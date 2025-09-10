import streamlit as st
import pandas as pd
from datetime import datetime

st.title("💴 e-Dirham: Issuance & Distribution (WalkThrough)")

# --- Initialize Wallets ---
if "wallets" not in st.session_state:
    st.session_state.wallets = {
        "CBUAE_Reserve": 10_000_000,     # Central Bank holding
        "ADCB_Fiat": 10_000_000,         # ADCB’s fiat reserve with CBUAE
        "ADCB_CBDC": 0,                  # ADCB CBDC wallet
        "Aamir_Fiat": 100_000,           # Aamir's fiat account at ADCB
        "UAE-CBDC-Aamir-001": 0          # Aamir's retail CBDC wallet
    }

if "tx_log" not in st.session_state:
    st.session_state.tx_log = []

# --- Display Wallet Balances ---
st.subheader("💼 Current Balances")
st.write(pd.DataFrame.from_dict(st.session_state.wallets, orient="index", columns=["Balance (AED)"]))

# --- Step 1: Issuance (CBUAE -> ADCB) ---
st.subheader("Step 1 — Issuance (CBUAE → ADCB)")
issue_amount = st.number_input("Enter amount of AED-CBDC to issue to ADCB", min_value=1000, step=1000)

if st.button("Submit Issuance"):
    if issue_amount <= st.session_state.wallets["ADCB_Fiat"]:
        st.session_state.wallets["ADCB_Fiat"] -= issue_amount
        st.session_state.wallets["ADCB_CBDC"] += issue_amount
        st.session_state.tx_log.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "From": "ADCB_Fiat",
            "To": "ADCB_CBDC",
            "Amount": issue_amount,
            "Purpose": "Issuance: Fiat to CBDC conversion at ADCB"
        })
        st.success(f"✅ Issued {issue_amount:,} AED-CBDC to ADCB. Equivalent fiat debited from ADCB reserve.")
    else:
        st.error("❌ Not enough fiat balance at ADCB for issuance.")

# --- Step 2: Distribution (ADCB -> Aamir) ---
st.subheader("Step 2 — Distribution (ADCB → Aamir)")
dist_amount = st.number_input("Enter amount Aamir requests as e-Dirham (CBDC)", min_value=100, step=100)

if st.button("Submit Distribution"):
    if dist_amount <= st.session_state.wallets["Aamir_Fiat"] and dist_amount <= st.session_state.wallets["ADCB_CBDC"]:
        st.session_state.wallets["Aamir_Fiat"] -= dist_amount
        st.session_state.wallets["UAE-CBDC-Aamir-001"] += dist_amount
        st.session_state.wallets["ADCB_CBDC"] -= dist_amount

        st.session_state.tx_log.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "From": "ADCB_CBDC",
            "To": "UAE-CBDC-Aamir-001",
            "Amount": dist_amount,
            "Purpose": "Distribution: Aamir converts fiat to CBDC"
        })
        st.success(f"✅ Aamir received {dist_amount:,} AED as e-Dirham. Equivalent debited from her fiat account.")
    else:
        st.error("❌ Not enough balance (either Aamir’s fiat or ADCB’s CBDC pool).")

# --- Transaction Log ---
if st.session_state.tx_log:
    st.subheader("📜 Transaction History")
    st.dataframe(pd.DataFrame(st.session_state.tx_log))
