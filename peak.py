import pandas as pd

def analyze_peaks(input_file='cost_estimation.csv', output_file='peak_analysis.csv'):
    """
    Analyzes energy consumption to find peak usage periods.
    """
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Set proper column names dynamically based on earlier outputs
    energy_col = 'predicted_energy_consumption' if 'predicted_energy_consumption' in df.columns else 'energy_consumption'
    cost_col = 'cost_per_hour' if 'cost_per_hour' in df.columns else df.columns[-1]

    # 1. Identify top 10 highest individual energy consumption hours
    top_10_energy = df.nlargest(10, energy_col)
    
    # 2. Identify top 10 highest cost hours
    top_10_cost = df.nlargest(10, cost_col)
    
    # 3. Extract hour from timestamp
    df['hour'] = df['timestamp'].dt.hour
    
    # 4. Group by hour and calculate average consumption
    hourly_avg = df.groupby('hour')[energy_col].mean().reset_index()
    hourly_avg.rename(columns={energy_col: 'avg_energy_consumption'}, inplace=True)
    
    # Sort the averages to easily see the peak hours of the day
    hourly_avg_sorted = hourly_avg.sort_values(by='avg_energy_consumption', ascending=False)

    # Print results clearly
    print("\n" + "="*50)
    print("PEAK ANALYSIS RESULTS")
    print("="*50)
    
    print("\n1. Top 5 Peak Hours of the Day (Average over forecast):")
    print("-" * 50)
    for index, row in hourly_avg_sorted.head(5).iterrows():
        print(f"Hour {int(row['hour']):02d}:00  -->  {row['avg_energy_consumption']:>5.2f} kWh")

    print("\n2. Top 10 Highest Individual Consumption Sequences:")
    print("-" * 50)
    for index, row in top_10_energy.iterrows():
        print(f"{row['timestamp']}  |  {row[energy_col]:>5.2f} kWh  |  Cost: {row[cost_col]:.2f} INR")
        
    print("\n3. Top 10 Highest Individual Cost Sequences:")
    print("-" * 50)
    for index, row in top_10_cost.iterrows():
        # Because we assumed a static cost (6 INR), this is effectively identical, 
        # but satisfies the requirement exactly.
        print(f"{row['timestamp']}  |  Cost: {row[cost_col]:>6.2f} INR  |  {row[energy_col]:.2f} kWh")
        
    print("="*50)

    # 5. Save results to peak_analysis.csv
    # Saving the hourly averages as the structured peak analysis file
    hourly_avg_sorted.columns = ['hour_of_day', 'avg_consumption_kwh']
    hourly_avg_sorted.to_csv(output_file, index=False)
    print(f"\nSaved average hourly consumption summary to '{output_file}'.")

if __name__ == "__main__":
    analyze_peaks()
