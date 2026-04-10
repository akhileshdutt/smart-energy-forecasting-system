import pandas as pd
import numpy as np
import joblib
from datetime import timedelta

def generate_forecast(model_file='energy_model.pkl', data_file='energy_features.csv', output_file='next_month_forecast.csv', steps=720):
    """
    Uses the trained model to recursively forecast future energy consumption hour-by-hour.
    """
    print(f"Loading model from {model_file}...")
    model = joblib.load(model_file)
    
    print(f"Loading historical data from {data_file}...")
    df = pd.read_csv(data_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # We need the last 24 hours of data to seed the initial lag features (t-1 and t-24)
    last_24 = df.tail(24).copy()
    
    # Keep track of true and predicted energy sequentially
    # This list will hold past values and new predictions appended one by one
    historical_energies = last_24['energy_consumption'].values.tolist()
    
    # We will start predicting from the hour directly following the last known timestamp
    last_timestamp = last_24['timestamp'].iloc[-1]
    
    forecast_records = []
    
    print(f"Generating recursive forecast for the next {steps} hours...")
    for i in range(steps):
        # Determine the datetime for the current step
        current_time = last_timestamp + timedelta(hours=i+1)
        
        # Extract direct temporal features
        hour = current_time.hour
        day_of_week = current_time.dayofweek
        day_of_year = current_time.dayofyear
        
        # Approximate future temperature using the same deterministic wave formula as our generator
        yearly_temp = 15 - 12 * np.cos(2 * np.pi * day_of_year / 365)
        daily_temp = 6 * np.cos(2 * np.pi * (hour - 14) / 24)
        assumed_temp = yearly_temp + daily_temp
        
        # Extract lag features dynamically from our historical/predicted list
        lag_1h = historical_energies[-1]
        lag_24h = historical_energies[-24]
        
        # Construct feature vector exactly as the model was trained
        # (Order: temperature, hour, day_of_week, energy_lag_1h, energy_lag_24h)
        X_pred = pd.DataFrame({
            'temperature': [assumed_temp],
            'hour': [hour],
            'day_of_week': [day_of_week],
            'energy_lag_1h': [lag_1h],
            'energy_lag_24h': [lag_24h]
        })
        
        # Make single-step prediction
        pred_energy = model.predict(X_pred)[0]
        
        # Add to sequence so it can be used for future lags
        historical_energies.append(pred_energy)
        
        # Record result
        forecast_records.append({
            'timestamp': current_time,
            'predicted_energy_consumption': pred_energy,
            'assumed_temperature': assumed_temp,
            'energy_lag_1h': lag_1h,
            'energy_lag_24h': lag_24h
        })

    # Save outputs
    forecast_df = pd.DataFrame(forecast_records)
    
    # We only output the required basic metrics and our forecast
    final_output = forecast_df[['timestamp', 'predicted_energy_consumption']]
    final_output.to_csv(output_file, index=False)
    
    print(f"Forecast complete! Generated {steps} hourly predictions.")
    print(f"Results saved to '{output_file}'.")

if __name__ == "__main__":
    generate_forecast()
