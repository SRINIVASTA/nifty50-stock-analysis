import json
import os
import yfinance as yf
import pandas as pd
import time
from datetime import date
import streamlit as st  # needed for session_state in auth functions only

USERS_FILE = "users.json"

# --- User Auth Code ---

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

if "users" not in st.session_state:
    st.session_state.users = load_users()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

def sign_up():
    st.subheader("Sign Up")
    new_user = st.text_input("New username", key="new_user")
    new_password = st.text_input("New password", type="password", key="new_pass")
    if st.button("Create account"):
        if not new_user or not new_password:
            st.error("Please enter both username and password.")
        elif new_user in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_user] = new_password
            save_users(st.session_state.users)
            st.success("Account created! Please sign in.")
            st.experimental_rerun()

def sign_in():
    st.subheader("Sign In")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Sign In"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")

            # Add this debugging line:
            st.write("Available attributes in st:", dir(st))

            # Then try rerun
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

def access_denied():
    st.error("You do not have access to this app or it does not exist.")
    st.info("Please sign in to continue.")
    st.write("If you believe this is a bug, contact support.")

# --- Stock Data Functions ---

tickers = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BHARTIARTL.NS",
    "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "ETERNAL.NS",
    "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS",
    "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS",
    "ITC.NS", "JIOFIN.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SHRIRAMFIN.NS",
    "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "TECHM.NS", "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

def fetch_ticker_data(ticker):
    try:
        stock_data = yf.Ticker(ticker)
        info = stock_data.info

        company_name = info.get("longName")
        current_price = info.get("currentPrice")
        book_value = info.get("bookValue")
        earnings_per_share = info.get("trailingEps")
        price_to_earnings = info.get("trailingPE")
        debt_to_equity = info.get("debtToEquity")
        return_on_equity = info.get("returnOnEquity")
        dividend_yield = info.get("dividendYield")
        current_ratio = info.get("currentRatio")
        quick_ratio = info.get("quickRatio")
        operating_cashflow = info.get("operatingCashflow")
        revenue_growth = info.get("revenueGrowth")

        pb_ratio = (current_price / book_value) if (current_price is not None and book_value not in [None, 0]) else None
        growth_rate = revenue_growth * 100 if revenue_growth is not None else 0
        intrinsic_value = (earnings_per_share * (8.5 + 2 * growth_rate)) if earnings_per_share is not None else None

        return [
            ticker, company_name, current_price, book_value, earnings_per_share,
            price_to_earnings, debt_to_equity, return_on_equity, dividend_yield,
            current_ratio, quick_ratio, operating_cashflow, revenue_growth, pb_ratio,
            intrinsic_value, None, None, None, None
        ]
    except Exception:
        return None

def get_data():
    all_data = []
    for tic in tickers:
        data = fetch_ticker_data(tic)
        all_data.append(data if data else [tic] + [None]*18)
        time.sleep(1)

    columns = [
        'Ticker', 'Company Name', 'Current Price', 'Book Value', 'Earnings Per Share',
        'Price-to-Earnings Ratio', 'Debt-to-Equity Ratio', 'Return on Equity', 'Dividend Yield',
        'Current Ratio', 'Quick Ratio', 'Operating Cashflow', 'Revenue Growth', 'P/B Ratio',
        'Intrinsic Value', 'Competitive Advantage', 'Market Share', 'Brand Recognition',
        'Corporate Governance'
    ]

    df = pd.DataFrame(all_data, columns=columns)
    df.set_index('Ticker', inplace=True)

    tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    while tickers_to_retry:
        time.sleep(5)
        for tic in tickers_to_retry:
            data = fetch_ticker_data(tic)
            if data:
                for i, col in enumerate(df.columns):
                    if pd.isna(df.at[tic, col]) and data[i + 1] is not None:
                        df.at[tic, col] = data[i + 1]
            time.sleep(1)
        tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    df['Date'] = date.today()
    df.sort_index(inplace=True)
    return df
