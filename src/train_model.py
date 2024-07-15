import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.impute import SimpleImputer

def train_model(data_path, model_path):
    # Load the data
    print("Loading data...")
    df = pd.read_parquet(data_path)
    
    print(f"Columns in the dataset: {df.columns}")
    
    # Ensure there are no NaN values in 'Return'
    if df['Return'].isnull().any():
        print(f"Found {df['Return'].isnull().sum()} NaN values in the target variable. Removing these rows.")
        df = df.dropna(subset=['Return'])
    
    # Separate features and target
    print("Preparing features and target variable...")
    X_train = df.drop(columns=['Return', 'Ticker'])
    y_train = df['Return']
    
    # Handle missing values in features
    print("Handling missing values...")
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)
    
    # Define models
    print("Defining models...")
    rf = RandomForestRegressor(random_state=42)
    gbr = GradientBoostingRegressor(random_state=42)
    xgbr = XGBRegressor(random_state=42)
    
    # Ensemble model using Voting Regressor
    print("Creating ensemble model...")
    ensemble_model = VotingRegressor(estimators=[
        ('rf', rf),
        ('gbr', gbr),
        ('xgbr', xgbr)
    ])
    
    # Train the ensemble model
    print("Training the ensemble model...")
    ensemble_model.fit(X_train_imputed, y_train)
    print("Training complete.")
    
    # Save the ensemble model
    print(f"Saving the model to {model_path}...")
    joblib.dump(ensemble_model, model_path)
    print(f"Trained model saved to {model_path}")
    
    # Evaluate the model
    print("Evaluating the model...")
    y_train_pred = ensemble_model.predict(X_train_imputed)
    mse = mean_squared_error(y_train, y_train_pred)
    r2 = r2_score(y_train, y_train_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")

if __name__ == "__main__":
    data_path = 'C:/Users/rahul/Desktop/Project_Algo/data/processed/feature_engineered_dataset.parquet'
    model_path = 'C:/Users/rahul/Desktop/Project_Algo/data/processed/best_ensemble_model.pkl'
    train_model(data_path, model_path)
