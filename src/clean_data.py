import pandas as pd
import json
import os
import sys

def process_and_engineer_data():
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'raw_data.json')
    OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'processed_data.csv')

    print(f"Starting Tasks 2 & 3: Processing data from {INPUT_FILE}...")
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)
    
    df = pd.json_normalize(raw_data, record_path=['records'])
    
    if df.empty:
        print("No records found in the raw data. Exiting.")
        return

    print(f"Loaded {len(df)} records.")
    
    # --- CHANGE HERE ---
    # Add 'ProductionType' to the list of required columns
    required_columns = [
        'HourUTC', 'HourDK', 'PriceArea',
        'ProductionType',  # <-- ADD THIS
        'CO2PerkWh', 'CH4PerkWh', 'N2OPerkWh'
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"ERROR: Required columns missing: {missing_cols}", file=sys.stderr)
        sys.exit(1)
        
    df = df[required_columns]
    
    df['HourUTC'] = pd.to_datetime(df['HourUTC'])
    df['HourDK'] = pd.to_datetime(df['HourDK'])
    
    emission_cols = ['CO2PerkWh', 'CH4PerkWh', 'N2OPerkWh']
    for col in emission_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df[emission_cols] = df[emission_cols].fillna(0)
    print("Cleaned and converted data types.")
    
    GWP_CH4 = 28
    GWP_N2O = 265
    
    df['gCO2e_per_kWh'] = (
        df['CO2PerkWh'] +
        (df['CH4PerkWh'] * GWP_CH4) +
        (df['N2OPerkWh'] * GWP_N2O)
    )
    print("Engineered 'gCO2e_per_kWh' (Eco-Score) feature.")
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # --- CHANGE HERE ---
    # Add 'ProductionType' to the final list of columns
    final_columns = ['HourDK', 'PriceArea', 'ProductionType', 'gCO2e_per_kWh']
    
    df_final = df[final_columns]
    
    # Filter out the extreme outliers (like 120,000) for a cleaner default plot
    # This is a temporary fix; a better fix is a filter in the app
    df_final = df_final[df_final['gCO2e_per_kWh'] < 20000]
    
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    print("\n--- Tasks 2 & 3 Complete ---")
    print(f"Final processed data saved to {OUTPUT_FILE}")
    print("\nFinal DataFrame Head:")
    print(df_final.head())

if __name__ == "__main__":
    process_and_engineer_data()