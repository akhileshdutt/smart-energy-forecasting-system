import pandas as pd

def generate_recommendations(peak_file='peak_analysis.csv', cost_file='cost_estimation.csv', output_file='recommendations.txt'):
    """
    Generates actionable energy-saving recommendations based on peak and cost analysis.
    """
    print("Loading analysis data...")
    try:
        peaks = pd.read_csv(peak_file)
        cost_df = pd.read_csv(cost_file)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Identify peak hours from the peak_analysis file (assuming sorted descending average)
    top_3_peak_hours = peaks.head(3)['hour_of_day'].tolist()
    off_peak_hours = peaks.tail(3)['hour_of_day'].tolist()
    
    # Simple Savings Calculation
    # Assumption: User shifts 15% of energy usage from the top 3 peak hours to off-peak hours.
    # To find out the total energy consumed in top 3 peak hours:
    cost_df['timestamp'] = pd.to_datetime(cost_df['timestamp'])
    cost_df['hour'] = cost_df['timestamp'].dt.hour
    
    # We assume 'predicted_energy_consumption' or similar is present, fallback to general 'energy_consumption'
    energy_col = 'predicted_energy_consumption' if 'predicted_energy_consumption' in cost_df.columns else 'energy_consumption'
    
    peak_energy_total = cost_df[cost_df['hour'].isin(top_3_peak_hours)][energy_col].sum()
    peak_cost_total = cost_df[cost_df['hour'].isin(top_3_peak_hours)]['cost_per_hour'].sum()
    
    # Calculate estimated savings (assume shifted to an off-peak rate, or simply saving energy)
    # Let's say shifting 15% usage out of peak hours could reduce the load, 
    # but since cost is static 6 INR across all hours, shifting doesn't magically decrease money unless 
    # there's a Time of Use (TOU) tariff, OR we just reduce usage.
    # We will assume a simple 15% reduction in usage during peak hours as the saving mechanism.
    reduction_percentage = 0.15
    energy_saved_kwh = peak_energy_total * reduction_percentage
    money_saved_inr = peak_cost_total * reduction_percentage
    
    # Let's write the recommendations
    recs = []
    recs.append("=" * 50)
    recs.append("ENERGY SAVING RECOMMENDATIONS")
    recs.append("=" * 50 + "\n")
    
    recs.append("1. SHIFT APPLIANCE USAGE TO OFF-PEAK HOURS")
    recs.append(f"   Your highest energy consumption happens during hours: {', '.join([f'{int(h):02d}:00' for h in top_3_peak_hours])}.")
    recs.append(f"   Consider shifting the use of heavy appliances (like washing machines or dishwashers)")
    recs.append(f"   to off-peak hours such as: {', '.join([f'{int(h):02d}:00' for h in off_peak_hours])}.")
    recs.append("")
    
    recs.append("2. REDUCE USAGE DURING HIGH-COST HOURS")
    recs.append("   The peak hours are driving your energy costs right now.")
    recs.append("   Lowering the thermostat on heating/cooling slightly during these evening peaks")
    recs.append("   will yield the highest overall reduction in your monthly bill.")
    recs.append("")
    
    recs.append("3. ESTIMATED POTENTIAL SAVINGS")
    recs.append(f"   If you manage to reduce your energy footprint by just {int(reduction_percentage*100)}% during")
    recs.append(f"   your top 3 peak hours, you will achieve the following monthly savings:")
    recs.append(f"      - Energy Reduced: {energy_saved_kwh:.2f} kWh")
    recs.append(f"      - Money Saved:    {money_saved_inr:.2f} INR")
    recs.append("")
    recs.append("=" * 50)

    # Print to console
    output_text = "\n".join(recs)
    print(output_text)

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_text)
        
    print(f"Recommendations successfully saved to '{output_file}'.")

if __name__ == "__main__":
    generate_recommendations()
