import pandas as pd

def estimate_cost(input_file='next_month_forecast.csv', output_file='cost_estimation.csv'):
    """
    Estimates electricity costs based on forecasted energy data.
    Assumes a fixed rate of 6 INR per kWh.
    """
    print(f"Loading forecast data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Check if 'predicted_energy_consumption' exists (this is what our forecast script outputted)
    if 'predicted_energy_consumption' in df.columns:
        energy_col = 'predicted_energy_consumption'
    elif 'energy_consumption' in df.columns:
        energy_col = 'energy_consumption'
    else:
        raise ValueError("Could not find the expected energy consumption column in the CSV.")
    
    # 1. Assume cost per unit = 6 INR per kWh
    # 2. Create the new column: cost_per_hour
    rate_per_kwh = 6.0
    df['cost_per_hour'] = df[energy_col] * rate_per_kwh
    
    # 3. Calculate total monthly cost
    total_monthly_cost = df['cost_per_hour'].sum()
    
    # 4. Print total cost clearly
    print("-" * 40)
    print("Cost Estimation Summary")
    print("-" * 40)
    print(f"Total Forecasted Energy: {df[energy_col].sum():.2f} kWh")
    print(f"Assumed Rate:             {rate_per_kwh} INR / kWh")
    print(f"Estimated Total Cost:     {total_monthly_cost:,.2f} INR")
    print("-" * 40)
    
    # 5. Save updated dataset
    df.to_csv(output_file, index=False)
    print(f"Updated dataset saved to '{output_file}'.")

if __name__ == "__main__":
    estimate_cost()
