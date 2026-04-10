import streamlit as st
import pandas as pd
import subprocess

# Set page configuration for a wider, cleaner layout
st.set_page_config(page_title="Smart Energy Consumption Dashboard", layout="wide", page_icon="⚡")

def load_data(filename):
    """Utility to load CSV safely."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return None

def main():
    # ---- PIPELINE SIDEBAR ----
    st.sidebar.title("⚡ Control Panel")
    st.sidebar.write("Generate new synthetic data and run the backend forecasting models.")
    if st.sidebar.button("🚀 Run Data Pipeline", use_container_width=True):
        with st.sidebar.status("Pipeline Running...", expanded=True) as status:
            try:
                result = subprocess.run(["python", "main.py"], capture_output=True, text=True, check=True)
                status.update(label="Complete!", state="complete", expanded=False)
                st.sidebar.success("Pipeline executed successfully!")
            except subprocess.CalledProcessError as e:
                status.update(label="Failed", state="error", expanded=False)
                st.sidebar.error("Execution failed.")
                
    st.sidebar.markdown("---")
    st.sidebar.caption("Dashboard auto-updates when data changes.")

    # ---- MAIN DASHBOARD TITLE ----
    st.title("Smart Energy Consumption Dashboard")
    st.markdown("Monitor forecasted loads, estimate upcoming costs, and discover saving opportunities.")
    st.markdown("---")
    
    # Pre-load core metrics
    forecast_df = load_data("next_month_forecast.csv")
    cost_df = load_data("cost_estimation.csv")
    peak_df = load_data("peak_analysis.csv")

    if forecast_df is None or cost_df is None or peak_df is None:
        st.warning("Data is missing. Please click 'Run Data Pipeline' in the sidebar.")
        return

    # Extract High-Level Variables
    total_energy = forecast_df['predicted_energy_consumption'].sum()
    total_cost = cost_df['cost_per_hour'].sum() if 'cost_per_hour' in cost_df.columns else cost_df.iloc[:, -1].sum()
    top_peak_hour = int(peak_df.iloc[0]['hour_of_day'])
    top_peak_load = peak_df.iloc[0]['avg_consumption_kwh']

    # ---- SECTION 1: TOP METRICS ----
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Energy Consumption", value=f"{total_energy:,.0f} kWh")
    with col2:
        st.metric(label="Total Estimated Cost", value=f"{total_cost:,.0f} INR")
    with col3:
        st.metric(label="Peak Usage Hour", value=f"{top_peak_hour:02d}:00", delta=f"{top_peak_load:.2f} kWh avg", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- SECTION 2: CHARTS ----
    st.markdown("### 📈 Consumption & Cost Trends")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.caption("Forecasted Energy Output (Next 30 Days)")
        forecast_df['timestamp'] = pd.to_datetime(forecast_df['timestamp'])
        st.line_chart(data=forecast_df.set_index('timestamp')['predicted_energy_consumption'], color="#ffaa00", height=300)

    with chart_col2:
        st.caption("Hourly Cost Distribution")
        cost_df['timestamp'] = pd.to_datetime(cost_df['timestamp'])
        # Depending on data size, we might want to plot the daily cost or hourly cost.
        # The prompt requested "Bar chart for hourly cost", so we group by hour of day for costs.
        cost_df['hour'] = cost_df['timestamp'].dt.hour
        hourly_cost = cost_df.groupby('hour')['cost_per_hour'].mean().reset_index()
        st.bar_chart(data=hourly_cost.set_index('hour')['cost_per_hour'], color="#00ff00", height=300)
        
    st.markdown("<br>", unsafe_allow_html=True)

    # ---- SECTION 3: PEAK USAGE & RECOMMENDATIONS ----
    st.markdown("### 🔍 Analytics & Insights")
    insight_col1, insight_col2 = st.columns([1, 2])

    with insight_col1:
        st.markdown("#### 🔥 Top Peak Hours")
        peak_df_sorted = peak_df.sort_values(by="avg_consumption_kwh", ascending=False).head(5)
        # Display peak hours gracefully
        for idx, row in peak_df_sorted.iterrows():
            hour = int(row['hour_of_day'])
            avg_load = row['avg_consumption_kwh']
            st.markdown(f"**{hour:02d}:00** &mdash; `{avg_load:.2f} kWh`")

    with insight_col2:
        st.markdown("#### 💡 Recommendations")
        try:
            with open("recommendations.txt", "r", encoding="utf-8") as f:
                recs_lines = f.readlines()
                
            # Formatting the raw txt into clean markdown layout
            clean_recs = ""
            for line in recs_lines:
                if line.startswith("==") or "ENERGY SAVING RECOMMENDATIONS" in line:
                    continue  # Strip out the CLI borders formatting from txt
                clean_recs += line
                
            st.info(clean_recs.strip())
        except FileNotFoundError:
            st.warning("Recommendations are not available yet.")

if __name__ == "__main__":
    main()
