import pandas as pd
import os

def feature_engineering(raw_data_folder, save_path):
    # Read all the parquet files and concatenate them into a single DataFrame
    df_list = []
    for filename in os.listdir(raw_data_folder):
        if filename.endswith('.parquet'):
            file_path = os.path.join(raw_data_folder, filename)
            print(f"Reading file: {file_path}")
            df = pd.read_parquet(file_path)
            df['Ticker'] = filename.split('.')[0]
            df_list.append(df)
    
    df = pd.concat(df_list)
    print("Loaded and combined raw data successfully")

    # Ensure the data is sorted by date
    df = df.sort_values(by=['Ticker', 'Date'])

    # Feature Engineering
    df['Return'] = df.groupby('Ticker')['Adj Close'].pct_change()

    # Moving averages and volatility
    df['MA_5'] = df.groupby('Ticker')['Adj Close'].transform(lambda x: x.rolling(window=5).mean())
    df['MA_20'] = df.groupby('Ticker')['Adj Close'].transform(lambda x: x.rolling(window=20).mean())
    df['Volatility'] = df.groupby('Ticker')['Adj Close'].transform(lambda x: x.rolling(window=20).std())

    # Drop rows with NaN values
    df = df.dropna()

    # Save the processed DataFrame
    df.to_parquet(save_path)
    print(f"Feature engineering complete. Processed data saved to {save_path}")

if __name__ == "__main__":
    raw_data_folder = 'C:/Users/rahul/Desktop/Project_Algo/data/raw'
    save_path = 'C:/Users/rahul/Desktop/Project_Algo/data/processed/feature_engineered_dataset.parquet'
    feature_engineering(raw_data_folder, save_path)


