"""
===============================================================================
 Script Name: aggregate_annual_indicators.py
 Author: Igor Latii
 Description:
     This script performs annual aggregation and interpolation on the merged
     dataset (`merged_df_readable.csv`) created in the previous phase.

     The purpose is to harmonize indicators with different temporal frequencies
     (monthly, quarterly, annual) into a single annual dataset suitable for
     exploratory data analysis (EDA).

     Specifically, the script:
        1. Loads the merged multi-indicator dataset.
        2. Groups observations by year.
        3. Sums continuous (economic and transport) indicators to represent
           total annual activity.
        4. Averages discrete (event-based or demographic) indicators to obtain
           representative annual levels.
        5. Applies linear interpolation to continuous indicators with small gaps.
        6. Saves the resulting annual dataset for use in subsequent analysis.

 Output:
     /data/processed/merged/merged_df_annual.csv

 Dependencies:
     - pandas
     - os
===============================================================================
"""

import pandas as pd
import os

# === PATH CONFIGURATION ===
input_file = "../data/processed/merged/merged_df_readable.csv"
output_dir = "../data/processed/merged"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "merged_df_annual.csv")

# === LOAD MERGED DATA ===
# Load the previously merged dataset and ensure TIME_PERIOD is parsed as datetime.
df = pd.read_csv(input_file, parse_dates=['TIME_PERIOD'])

# Extract the year component for aggregation.
df['Year'] = df['TIME_PERIOD'].dt.year

# === DEFINE INDICATOR CATEGORIES ===
# Continuous indicators (summed annually and interpolated)
continuous_cols = [
    'GDP (Quarterly)',
    'Population',
    'Exports (National Accounts)',
    'Air Passenger Transport',
    'Freight Transport',
    'Inflation (HICP Manufacturing)',
    'Road Passenger Transport',
    'Industrial Production Index',
    'Retail Trade Turnover',
    'Energy Prices'
]

# Discrete / event-based indicators (averaged annually; not interpolated)
discrete_cols = [
    'Net Migration (World Bank)',
    'Unemployment Rate',
    'Emigration of Citizens'
]

# === DEFINE AGGREGATION STRATEGY ===
# Continuous indicators → annual totals
# Discrete indicators → annual averages
agg_dict = {col: 'sum' for col in continuous_cols}  # sum for transport, economy
agg_dict.update({col: 'mean' for col in discrete_cols})  # to have one meaning per year

# Perform the aggregation by year.
annual_df = df.groupby('Year').agg(agg_dict).reset_index()

# === INTERPOLATE CONTINUOUS INDICATORS ===
# Fill small gaps in continuous indicators using linear interpolation.
annual_df[continuous_cols] = annual_df[continuous_cols].interpolate(method='linear')

# === SAVE OUTPUT FILE ===
annual_df.to_csv(output_file, index=False)
print(f"🎯 Успешно создан merged_df_annual.csv ({annual_df.shape[0]} строк, {annual_df.shape[1]} колонок)")
