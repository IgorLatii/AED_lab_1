"""
===============================================================================
 Script Name: make_merged_df.py
 Author: Igor Latii
 Description:
     This script merges all preprocessed and formatted Eurostat and World Bank
     indicator CSV files into a single unified dataset (`merged_df_readable.csv`).

     Each dataset in `/data/processed/formatted_time_periods/` contains two key
     columns: TIME_PERIOD (date) and VALUE (numeric indicator value). The script:
        1. Loads all formatted CSV files from the directory.
        2. Converts technical indicator codes to human-readable names.
        3. Aggregates data by TIME_PERIOD (summing multiple records if needed).
        4. Merges all indicators into one wide-format DataFrame.
        5. Saves the final merged dataset for later annual aggregation and EDA.

 Output:
     /data/processed/merged/merged_df_readable.csv

 Dependencies:
     - pandas
     - os

===============================================================================
"""

import os
import pandas as pd

# === Define input and output paths ===
processed_dir = "../data/processed/formatted_time_periods"
output_dir = "../data/processed/merged"
os.makedirs(output_dir, exist_ok=True)

# === Mapping of technical indicator codes to descriptive names ===
indicator_mapping = {
    "API_SM.POP.NETM_DS2_en_csv_v2_126864": "Net Migration (World Bank)",
    "avia_paocc": "Air Passenger Transport",
    "demo_pjan": "Population",
    "lfsi_emp_q": "Employment",
    "migr_emi1ctz": "Emigration of Citizens",
    "nama_10_exi": "Exports (National Accounts)",
    "namq_10_gdp": "GDP (Quarterly)",
    "nrg_pc_202": "Energy Prices",
    "prc_hicp_manr": "Inflation (HICP Manufacturing)",
    "road_pa_mov": "Road Passenger Transport",
    "sts_inpr_m": "Industrial Production Index",
    "sts_trtu_m": "Retail Trade Turnover",
    "tour_occ_nim": "Tourist Overnight Stays",
    "tran_hv_frtra": "Freight Transport",
    "une_rt_m": "Unemployment Rate"
}

dfs = [] # list to store each processed DataFrame

# === Iterate through all formatted indicator files ===
for file in os.listdir(processed_dir):
    if not file.endswith('.csv'):
        continue # skip non-CSV files

    # Extract clean indicator name from filename
    indicator_name = os.path.splitext(file)[0]
    indicator_name = indicator_name.replace('_raw_formatted', '').replace('_formatted', '')

    file_path = os.path.join(processed_dir, file)
    df = pd.read_csv(file_path)

    # Convert TIME_PERIOD to datetime and VALUE to numeric
    df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], errors='coerce')
    df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')

    # === Aggregate values by TIME_PERIOD ===
    # If multiple entries exist for the same period, sum them.
    df = df.groupby('TIME_PERIOD', as_index=False)['VALUE'].sum()

    # Apply readable indicator name (fallback to file name if not mapped)
    readable_name = indicator_mapping.get(indicator_name, indicator_name)

    # Rename columns and drop duplicates to keep clean structure
    df = df[['TIME_PERIOD', 'VALUE']].rename(columns={'VALUE': readable_name})
    df = df.drop_duplicates(subset=['TIME_PERIOD'])

    dfs.append(df)
    print(f"SUCCES: Loaded  {readable_name} ({len(df)} строк)")

# === Merge all datasets into one table by TIME_PERIOD ===
if dfs:
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='TIME_PERIOD', how='outer')

    merged_df = merged_df.sort_values('TIME_PERIOD')

    # Save merged dataset
    output_file = os.path.join(output_dir, 'merged_df_readable.csv')
    merged_df.to_csv(output_file, index=False)

    print(f"\nSUCCESS: Successfully created merged_df_readable.csv ({merged_df.shape[0]} rows, {merged_df.shape[1]} columns)")
else:
    print("ERROR: No CSV files found for merging.")
