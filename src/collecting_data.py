"""
===============================================================================
 Script Name: collecting_data.py
 Author: Igor Latii
 Description:
     This script automates the data acquisition process from Eurostat for a
     predefined list of indicators specified in the file `/reports/indicators.csv`.

     It connects to the Eurostat API via the `eurostat` Python package, downloads
     each dataset, filters it for the selected country (default: Latvia, LV), and
     saves the cleaned raw data in CSV format to the `/data/raw/` directory.

 Workflow:
     1. Load the list of indicators and metadata from `/reports/indicators.csv`.
     2. For each indicator:
         - Fetch the corresponding dataset from the Eurostat API.
         - Filter data for the selected country (geo = LV).
         - Save the dataset as a raw CSV file in `/data/raw/`.
     3. Log progress and handle missing or malformed datasets gracefully.

 Output:
     Raw CSV files in `../data/raw/`, one per indicator.

 Dependencies:
     - eurostat
     - pandas
     - os
===============================================================================
"""

import eurostat
import pandas as pd
import os

# === File paths ===
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, '../data/raw')
indicators_path = os.path.join(base_dir, '../reports/indicators.csv')
# === Create data folder if it doesn't exist ===
os.makedirs(data_dir, exist_ok=True)

# === Load indicators ===
indicators = pd.read_csv(indicators_path)
print(f"Found {len(indicators)} indicators to load...")

# === Iterate through all selected codes and download data ===
for _, ind in indicators.iterrows():
    code = ind['code']
    name = ind.get('name', code)
    geo = ind.get('geo', 'LV')  # from indicators.csv

    print(f"INFO: Loading {name} ({code}) for {geo} ...")
    try:
        # Loading the entire dataset
        df = eurostat.get_data_df(code)

        # Filter by GEO (if applicable)
#        print("  Columns:", list(df.columns))
        if 'geo\\TIME_PERIOD' in df.columns:
            df = df[df['geo\\TIME_PERIOD'] == geo]
            print(f"  INFO: Filtered by geo={geo}, remaining {len(df)} rows.")
        else:
            print(f"  WARNING: 'geo' column not found in dataset {code}.")

        # Checking the structure
        print(f"  SUCCESS: Successfully loaded: {df.shape[0]} rows, {df.shape[1]} columns")

        # Save filtered by geo dataset
        output_path = os.path.join(data_dir, f"{code}_raw.csv")
        df.to_csv(output_path, index=False)
        print(f"  SUCCESS: Saved in: {output_path}")

    except Exception as e:
        print(f"  ERROR: Error loading {code}: {e}")

print("\n=== Completed. All available indicators for selected geo are saved in ../data/raw/ ===")