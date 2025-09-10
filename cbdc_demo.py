import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# --- Header with logo ---
logo = Image.open("edirham_logo.jpg")

col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo, width=80)
with col2:
    st.title("e-Dirham: Issuance & Distribution Demo")

st.markdown("---")

# --- Initialize Wallets Safely ---
default_wallets = {
    "CBUAE_Reserve": 10_000_000,     # Central Bank pool
    "ADCB_Fiat": 10_000_000,         # ADCB fiat reserve with CBUAE
    "ADCB_CBDC": 0,                  # ADCB CBDC pool
    "Aamir_Fiat": 100_000,           # Aamir's fiat account at ADCB
    "UAE-CBDC-AAMIR-001": 0          # Aamir's retail CBDC wallet
}

if "wallets" not in st.session_state:
    st.session_state.wallets = default_wallets.copy()
else:
    # Ensure missing keys are restored if session is refreshed
    for k, v in default_wallets.items():
        if k not in st.session_state.wallets:
            st.session_state.wallets[k] = v

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
            "Purpose": "Issuance: Fiat → CBDC conversion at ADCB"
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
        st.session_state.wallets["UAE-CBDC-AAMIR-001"] += dist_amount
        st.session_state.wallets["ADCB_CBDC"] -= dist_amount

        st.session_state.tx_log.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "From": "ADCB_CBDC",
            "To": "UAE-CBDC-AAMIR-001",
            "Amount": dist_amount,
            "Purpose": "Distribution: Aamir converts fiat to CBDC"
        })
        st.success(f"✅ Aamir received {dist_amount:,} AED as e-Dirham. Equivalent debited from his fiat account.")
    else:
        st.error("❌ Not enough balance (either Aamir’s fiat or ADCB’s CBDC pool).")

# --- Transaction Log ---
if st.session_state.tx_log:
    st.subheader("📜 Transaction History")
    st.dataframe(pd.DataFrame(st.session_state.tx_log))
