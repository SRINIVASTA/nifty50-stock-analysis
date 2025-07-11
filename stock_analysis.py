# stock_analysis.py

import yfinance as yf
import pandas as pd
import time
from datetime import date

tickers = [
    'HEROMOTOCO.NS', 'BEL.NS', 'BPCL.NS', 'SHRIRAMFIN.NS', 'TATACONSUM.NS', 'TRENT.NS', 'ADANIENT.NS',
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS',
    'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'BAJAJFINSV.NS', 'AXISBANK.NS', 'MARUTI.NS', 'LT.NS',
    'ASIANPAINT.NS', 'M&M.NS', 'BAJFINANCE.NS', 'TITAN.NS', 'SUNPHARMA.NS', 'HCLTECH.NS', 'ULTRACEMCO.NS',
    'NESTLEIND.NS', 'TECHM.NS', 'POWERGRID.NS', 'GRASIM.NS', 'WIPRO.NS', 'INDUSINDBK.NS', 'NTPC.NS',
    'ONGC.NS', 'TATASTEEL.NS', 'CIPLA.NS', 'DRREDDY.NS', 'JSWSTEEL.NS', 'HDFCLIFE.NS', 'BRITANNIA.NS',
    'BAJAJ-AUTO.NS', 'EICHERMOT.NS', 'HINDALCO.NS', 'COALINDIA.NS', 'ADANIPORTS.NS', 'SBILIFE.NS',
    'TATAMOTORS.NS', 'APOLLOHOSP.NS'
]

def fetch_ticker_data(ticker):
    # ... (same fetch logic) ...
    return [
        ticker, company_name, current_price, book_value, earnings_per_share,
        price_to_earnings, debt_to_equity, return_on_equity, dividend_yield,
        current_ratio, quick_ratio, operating_cashflow, revenue_growth, pb_ratio,
        intrinsic_value, competitive_advantage, market_share, brand_recognition,
        corporate_governance
    ]

def get_data():
    all_data = []
    for ticker in tickers:
        data = fetch_ticker_data(ticker)
        if data:
            all_data.append(data)
        else:
            all_data.append([ticker] + [None]*18)
        time.sleep(1)

    columns = [ ... ]  # your columns list
    df = pd.DataFrame(all_data, columns=columns)
    df.set_index('Ticker', inplace=True)

    tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    while tickers_to_retry:
        print(f"Retrying: {tickers_to_retry}")
        time.sleep(5)
        for ticker in tickers_to_retry:
            data = fetch_ticker_data(ticker)
            if data:
                df.loc[ticker] = data[1:]
            time.sleep(1)
        tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    df['Date'] = date.today()
    df.sort_index(inplace=True)
    return df
