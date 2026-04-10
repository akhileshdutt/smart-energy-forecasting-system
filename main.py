import subprocess
import time

def run_pipeline():
    """
    Orchestrates and executes the complete energy prediction pipeline.
    """
    steps = [
        ("Step 1: Generating Synthetic Data", "datagen.py"),
        ("Step 2: Performing Feature Engineering", "features.py"),
        ("Step 3: Training Machine Learning Model", "train.py"),
        ("Step 4: Forecasting Next Month's Energy", "forecast.py"),
        ("Step 5: Estimating Electricity Costs", "cost.py"),
        ("Step 6: Detecting Peak Usage Hours", "peak.py"),
        ("Step 7: Generating Energy-Saving Recommendations", "recommend.py"),
        ("Step 8: Generating Final Dashboard Summary", "dashboard_summary.py")
    ]
    
    print("=" * 60)
    print("STARTING ENERGY PROJECT PIPELINE")
    print("=" * 60)
    
    total_start_time = time.time()
    
    for desc, script_name in steps:
        print(f"\n--> {desc} ({script_name})...")
        step_start_time = time.time()
        try:
            # Run the script in a subprocess
            subprocess.run(["python", script_name], check=True)
            
            step_time = time.time() - step_start_time
            print(f"SUCCESS: Completed {script_name} in {step_time:.2f}s.")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Occurred while running {script_name}.")
            print("Aborting pipeline execution.")
            return

    total_time = time.time() - total_start_time
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {total_time:.2f} SECONDS!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
