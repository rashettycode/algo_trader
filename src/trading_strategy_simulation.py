import pandas as pd
import joblib
import numpy as np

def trading_strategy(predicted_return, threshold=0):
    if predicted_return > threshold:
        return 1  # Buy
    elif predicted_return < -threshold:
        return -1  # Sell
    else:
        return 0  # Hold

def simulate_trading(data_path, model_path, initial_capital=100000, max_iterations=10, commission=0):
    # Load data
    try:
        df = pd.read_parquet(data_path)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Display the columns in the DataFrame
    print(f"Columns in DataFrame: {df.columns.tolist()}")

    # Load model
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Ensure necessary columns are present
    required_columns = ['Ticker', 'Return']
    if not all(col in df.columns for col in required_columns):
        print(f"Missing required columns in the data. Required columns: {required_columns}")
        print(f"Available columns: {df.columns.tolist()}")
        return
    
    # Drop unnecessary columns and handle potential NaNs
    X = df.drop(columns=required_columns, errors='ignore').fillna(0)
    
    try:
        df['Predicted_Return'] = model.predict(X)
        print("Prediction successful.")
    except Exception as e:
        print(f"Error during prediction: {e}")
        return
    
    df['Action'] = df['Predicted_Return'].apply(trading_strategy)
    
    df['Portfolio_Value'] = initial_capital
    df['Position'] = 0

    # Create a list to store portfolio values
    portfolio_values = [initial_capital]

    for i in range(1, min(max_iterations, len(df))):
        action = df['Action'].iloc[i]
        prev_position = df['Position'].iloc[i - 1]

        if action == 1:
            df.at[i, 'Position'] = min(prev_position + 1, 10)
            transaction_cost = commission
            print(f"Buy: Iteration {i}, Position {df.at[i, 'Position']}, Transaction Cost {transaction_cost}")
        elif action == -1:
            df.at[i, 'Position'] = max(prev_position - 1, -10)
            transaction_cost = commission
            print(f"Sell: Iteration {i}, Position {df.at[i, 'Position']}, Transaction Cost {transaction_cost}")
        else:
            df.at[i, 'Position'] = prev_position
            transaction_cost = 0
            print(f"Hold: Iteration {i}, Position {df.at[i, 'Position']}")

        # Update the portfolio value based on the position and return
        new_portfolio_value = portfolio_values[-1] * (1 + df['Return'].iloc[i] * df.at[i, 'Position']) - transaction_cost
        portfolio_values.append(new_portfolio_value)
        df.at[i, 'Portfolio_Value'] = new_portfolio_value
        print(f"Iteration {i}: Return = {df['Return'].iloc[i]}, Position = {df.at[i, 'Position']}, Portfolio Value = {df.at[i, 'Portfolio_Value']}")

    final_portfolio_value = portfolio_values[-1]
    total_return = (final_portfolio_value - initial_capital) / initial_capital
    sharpe_ratio = ((df['Return'].mean() * 252) - 0.05) / (df['Return'].std() * np.sqrt(252))
    max_drawdown = ((df['Portfolio_Value'].max() - df['Portfolio_Value'].min()) / df['Portfolio_Value'].max()) * 100

    print(f"Portfolio Values: {portfolio_values}")  # Debugging: print all portfolio values
    print(f"Initial Capital: {initial_capital}")
    print(f"Final Portfolio Value: {final_portfolio_value}")
    print(f"Total Return: {total_return * 100:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2f}%")

if __name__ == "__main__":
    data_path = "C:/Users/rahul/Desktop/Project_Algo/data/processed/feature_engineered_dataset.parquet"
    model_path = "C:/Users/rahul/Desktop/Project_Algo/data/processed/best_ensemble_model.pkl"
    simulate_trading(data_path, model_path, commission=0)  # Adjust commission as needed











