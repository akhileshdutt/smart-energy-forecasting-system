import pandas as pd
import numpy as np

def generate_energy_data(filename='synthetic_energy_data.csv'):
    """
    Generates synthetic household energy consumption data.
    """
    # 1. Setup time range: 365 days of hourly data (8760 periods)
    start_date = '2023-01-01'
    periods = 365 * 24
    timestamps = pd.date_range(start=start_date, periods=periods, freq='h')
    
    df = pd.DataFrame({'timestamp': timestamps})
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    df['dayofyear'] = df['timestamp'].dt.dayofyear
    
    # 2. Simulate realistically fluctuating temperatures
    # Yearly seasonal sine wave (colder in winter, warmer in summer)
    yearly_temp = 15 - 12 * np.cos(2 * np.pi * df['dayofyear'] / 365)
    # Daily sine wave (peak temperature usually around 2 PM / hour 14)
    daily_temp = 6 * np.cos(2 * np.pi * (df['hour'] - 14) / 24)
    # Random temperature noise
    temp_noise = np.random.normal(0, 1.5, periods)
    
    df['temperature'] = yearly_temp + daily_temp + temp_noise

    # 3. Simulate energy consumption
    base_load = 0.5  # Base kW of 'always-on' appliances (fridge, standby devices, etc.)
    
    time_factor = np.zeros(periods)
    
    # Define masks for time of day
    morning_peak = (df['hour'] >= 6) & (df['hour'] <= 9)
    evening_peak = (df['hour'] >= 18) & (df['hour'] <= 22)
    off_peak = ~(morning_peak | evening_peak)
    
    # Assign base profile variations
    time_factor[off_peak] = 0.4
    time_factor[morning_peak] = 1.2
    time_factor[evening_peak] = 1.8
    
    # 4. Weekday vs Weekend variation
    weekend_mask = df['dayofweek'] >= 5 # 5 is Saturday, 6 is Sunday
    
    # On weekends, daytime base load is a bit higher and peaks distribute longer or differently
    weekend_multiplier = np.ones(periods)
    weekend_multiplier[weekend_mask] = 1.2 # General 20% increase for weekend overall
    
    # Flatten the distinct peaks a bit for weekends (people wake up later, more steady usage)
    time_factor[weekend_mask & morning_peak] = 0.9
    time_factor[weekend_mask & evening_peak] = 1.5
    time_factor[weekend_mask & off_peak] = 0.7  # Daytime weekend use is higher
    
    # 5. Temperature impact on load (Heating/Cooling)
    # Require heating when temperature is below 15C, cooling if above 23C
    heating_factor = np.where(df['temperature'] < 15, (15 - df['temperature']) * 0.06, 0)
    cooling_factor = np.where(df['temperature'] > 23, (df['temperature'] - 23) * 0.08, 0)
    
    # 6. Add Randomness using Numpy
    energy_noise = np.random.normal(0, 0.25, periods)
    
    # Combine the factors
    df['energy_consumption'] = ((base_load + time_factor) * weekend_multiplier 
                                + heating_factor 
                                + cooling_factor 
                                + energy_noise)
    
    # Apply a floor so we don't have negative consumption due to noise
    df['energy_consumption'] = np.clip(df['energy_consumption'], base_load * 0.5, None)
    
    # Formulate final dataset
    final_df = df[['timestamp', 'energy_consumption', 'temperature']]
    
    # Save the output to a CSV file
    final_df.to_csv(filename, index=False)
    print(f"Data shape: {final_df.shape}")
    print(f"Successfully generated 1 year of hourly data and saved to '{filename}'.")

if __name__ == "__main__":
    generate_energy_data()
