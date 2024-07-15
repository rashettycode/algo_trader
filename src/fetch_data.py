import yfinance as yf
import pandas as pd

def fetch_data(tickers, start_date, end_date):
    # Download stock data
    df = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    
    # Flatten the MultiIndex columns
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    # Save DataFrame to a Parquet file
    df.to_parquet('data/processed/stock_data.parquet')
    print("Data fetched and saved successfully.")

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'NVDA', 'AMZN', 'META', 'TSLA', 
               'BRK-B', 'V', 'JNJ', 'PG', 'AVGO', 'AMD', 'ANET', 'ODFL', 'MNST', 
               'DECK', 'TSCO', 'FICO']  # List of tickers
    start_date = '2014-06-30'  # Ten years from June 30, 2024
    end_date = '2024-06-30'
    fetch_data(tickers, start_date, end_date)

