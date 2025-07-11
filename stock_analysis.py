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
    try:
        print(f"Fetching data for {ticker}")
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

        competitive_advantage = None
        market_share = None
        brand_recognition = None
        corporate_governance = None

        return [
            ticker, company_name, current_price, book_value, earnings_per_share,
            price_to_earnings, debt_to_equity, return_on_equity, dividend_yield,
            current_ratio, quick_ratio, operating_cashflow, revenue_growth, pb_ratio,
            intrinsic_value, competitive_advantage, market_share, brand_recognition,
            corporate_governance
        ]
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_data():
    all_data = []
    for ticker in tickers:
        data = fetch_ticker_data(ticker)
        if data:
            all_data.append(data)
        else:
            all_data.append([ticker] + [None]*18)
        time.sleep(1)  # Avoid hitting API rate limits

    columns = [
        'Ticker', 'Company Name', 'Current Price', 'Book Value', 'Earnings Per Share',
        'Price-to-Earnings Ratio', 'Debt-to-Equity Ratio', 'Return on Equity', 'Dividend Yield',
        'Current Ratio', 'Quick Ratio', 'Operating Cashflow', 'Revenue Growth', 'P/B Ratio',
        'Intrinsic Value', 'Competitive Advantage', 'Market Share', 'Brand Recognition',
        'Corporate Governance'
    ]

    df = pd.DataFrame(all_data, columns=columns)
    df.set_index('Ticker', inplace=True)

    # Retry tickers with missing critical data
    tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    while tickers_to_retry:
        print(f"Retrying tickers with missing data: {tickers_to_retry}")
        time.sleep(5)
        for ticker in tickers_to_retry:
            data = fetch_ticker_data(ticker)
            if data:
                df.loc[ticker] = data[1:]
            else:
                print(f"Retry failed for {ticker}")
            time.sleep(1)
        tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    df['Date'] = date.today()
    df.sort_index(inplace=True)
    return df
