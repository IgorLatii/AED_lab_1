import eurostat
import pandas as pd
import os

# === File paths ===
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, '../data/raw')
indicators_path = os.path.join(base_dir, '../reports/indicators.csv')

# === Load indicators ===
indicators = pd.read_csv(indicators_path)

print(f"Found {len(indicators)} indicators to load...")

# === Iterate through all selected codes and download data ===
for _, ind in indicators.iterrows():
    code = ind['code']
    name = ind.get('name', code)

    print(f"INFO: Loading {name} ({code}) ...")
    try:
        # Loading the entire dataset
        df = eurostat.get_data_df(code)

        # Checking the structure
        print(f"  SUCCESS: Successfully loaded: {df.shape[0]} rows, {df.shape[1]} columns")

        # Save as it is (raw)
        output_path = os.path.join(data_dir, f"{code}_raw.csv")
        df.to_csv(output_path, index=False)
        print(f"  SUCCESS: Saved in: {output_path}")

    except Exception as e:
        print(f"  ERROR: Error loading {code}: {e}")

print("\n=== Completed. All available indicators are saved in ../data/raw/ ===")