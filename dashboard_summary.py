import pandas as pd

def generate_dashboard_summary(cost_file='cost_estimation.csv', peak_file='peak_analysis.csv', output_file='dashboard_summary.txt'):
    """
    Generates a high-level summary report for dashboard consumption.
    """
    print("Loading data for dashboard summary...")
    try:
        cost_df = pd.read_csv(cost_file)
        peak_df = pd.read_csv(peak_file)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # 1. Total monthly consumption
    # Use predicted_energy_consumption if available, else energy_consumption
    energy_col = 'predicted_energy_consumption' if 'predicted_energy_consumption' in cost_df.columns else 'energy_consumption'
    total_consumption = cost_df[energy_col].sum()

    # 2. Total cost
    # Use cost_per_hour if available
    cost_col = 'cost_per_hour' if 'cost_per_hour' in cost_df.columns else cost_df.columns[-1]
    total_cost = cost_df[cost_col].sum()

    # 3. Peak usage hour
    # Peak dataframe is sorted by average consumption, so the first row is the peak hour
    peak_hour = peak_df.iloc[0]['hour_of_day']
    peak_avg_consumption = peak_df.iloc[0]['avg_consumption_kwh']

    # 4. Format a clean summary
    summary_lines = []
    summary_lines.append("*" * 40)
    summary_lines.append("        DASHBOARD OVERVIEW        ")
    summary_lines.append("*" * 40)
    summary_lines.append(f"Total Monthly Consumption: {total_consumption:,.2f} kWh")
    summary_lines.append(f"Total Estimated Cost:      {total_cost:,.2f} INR")
    summary_lines.append(f"Absolute Peak Usage Hour:  {int(peak_hour):02d}:00 ({peak_avg_consumption:.2f} kWh avg load)")
    summary_lines.append("*" * 40)

    # 5. Print to console
    output_text = "\n".join(summary_lines)
    print("\n" + output_text + "\n")

    # 6. Save to txt
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_text)
        
    print(f"Dashboard summary successfully exported to '{output_file}'.")

if __name__ == "__main__":
    generate_dashboard_summary()
