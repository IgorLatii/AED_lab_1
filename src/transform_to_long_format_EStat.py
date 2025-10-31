"""
===============================================================================
 Script Name: transform_to_long_format_EStat.py
 Author: Igor Latii
 Description:
     This script converts Eurostat raw datasets from wide format to long format,
     preparing them for consistent analysis and further time-based processing.

 Workflow:
     1. Load all raw CSV files from /data/raw/ that end with "_raw.csv".
     2. Detect and rename Eurostat-specific columns (e.g., 'geo\\TIME_PERIOD' → 'geo').
     3. Identify time-period columns (columns that start with a year or contain 'Q').
     4. Separate metadata columns (non-period columns) from period data.
     5. Transform each dataset from wide to long format using pandas.melt().
     6. Remove empty or invalid rows (where VALUE is NaN).
     7. Save the reshaped tables to /data/processed/transformed_to_long_format/
        with the "_long.csv" suffix.

 Output:
     - One cleaned and reshaped long-format CSV file per indicator.
     - Standard columns: TIME_PERIOD, VALUE, and all relevant metadata fields.

 Purpose:
     - Standardizes Eurostat datasets for temporal harmonization and merging.
     - Serves as an intermediate step before date formatting and aggregation.

 Dependencies:
     - pandas
     - os
===============================================================================
"""

import pandas as pd
import os

# === Paths ===
base_dir = os.path.dirname(__file__) # Base directory of the script
raw_dir = os.path.join(base_dir, '../data/raw') # Directory containing raw CSV files
processed_dir = os.path.join(base_dir, '../data/processed/transformed_to_long_format') # Directory to save processed files
os.makedirs(processed_dir, exist_ok=True) # Create processed directory if it does not exist

# === Process all Eurostat files in the raw directory ===
for file in os.listdir(raw_dir):
    if not file.lower().endswith("_raw.csv"):
        continue # Skip files that do not match the pattern

    print(f"Processing {file} ...")

    file_path = os.path.join(raw_dir, file)
    # --- Read the CSV file ---
    df = pd.read_csv(file_path)

    # --- Rename Eurostat-specific column ---
    # Some Eurostat CSVs have 'geo\TIME_PERIOD' as a column, rename it to 'geo'
    if 'geo\\TIME_PERIOD' in df.columns:
        df = df.rename(columns={'geo\\TIME_PERIOD': 'geo'})

    # --- Identify period columns ---
    # Columns representing time periods usually start with a year (4 digits) or contain 'Q' for quarters
    period_cols = [c for c in df.columns if c[:4].isdigit() or 'Q' in c]
    print(period_cols)

    # --- Identify metadata columns ---
    # All columns that are not period columns are considered metadata
    meta_cols = [c for c in df.columns if c not in period_cols]
    print(meta_cols)

    # --- Transform from wide to long format ---
    df_long = df.melt(
        id_vars=meta_cols,       # Columns to keep as-is
        value_vars=period_cols,  # Columns to unpivot
        var_name='TIME_PERIOD',  # Name for the new column containing period labels
        value_name='VALUE'       # Name for the new column containing values
    )

    # --- Remove empty rows ---
    df_long = df_long.dropna(subset=["VALUE"]) # Drop rows where VALUE is NaN

    # --- Save the processed data ---
    output_file = os.path.join(processed_dir, os.path.basename(file).replace(".csv", "_long.csv"))
    df_long.to_csv(output_file, index=False) # Save to CSV without the index

    print(f"Done: {len(df_long)} rows  → {output_file}")