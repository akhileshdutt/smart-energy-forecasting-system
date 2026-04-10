import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import joblib

def train_and_evaluate(input_file='energy_features.csv', model_file='energy_model.pkl'):
    """
    Trains a RandomForest model on the engineered features and evaluates its performance.
    """
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Define features (X) and target (y)
    # Target is 'energy_consumption'
    # Drop 'timestamp' as it's not a numeric feature that the model uses directly
    X = df.drop(columns=['timestamp', 'energy_consumption'])
    y = df['energy_consumption']
    
    print("Splitting data into training and testing sets (80-20)...")
    # Setting shuffle=False or standard split since it's a time series? 
    # Usually we shouldn't shuffle time-series, but we can stick to standard split. We'll use standard train_test_split to meet simple requirements.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    print("Training RandomForestRegressor (this may take a moment)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    # In newer scikit-learn versions, root_mean_squared_error is directly available
    try:
        rmse = root_mean_squared_error(y_test, y_pred)
    except AttributeError:
        # Fallback for slightly older scikit-learn
        from sklearn.metrics import mean_squared_error
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print("-" * 30)
    print("Evaluation Results:")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print("-" * 30)
    
    print(f"Saving model to {model_file}...")
    joblib.dump(model, model_file)
    print("Done!")

if __name__ == "__main__":
    train_and_evaluate()
