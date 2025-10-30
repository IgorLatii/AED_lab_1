import os
import pandas as pd

# === Paths ===
base_dir = os.path.dirname(__file__) # Base directory of the script
raw_dir = os.path.join(base_dir, '../data/raw') # Directory with raw CSV files
processed_dir = os.path.join(base_dir, '../data/processed/transformed_to_long_format') # Directory to save processed files
os.makedirs(processed_dir, exist_ok=True) # Create processed directory if it doesn't exist

# === Process all WorldBank files in the raw directory ===
for file in os.listdir(raw_dir):
    if not file.lower().endswith("126864.csv"):
        continue # Skip files that do not match the pattern

    print(f"Processing  {file} ...")
    file_path = os.path.join(raw_dir, file)

    # --- Read the CSV file ---
    # Skip first 4 rows which usually contain metadata (source, date, empty row, header row)
    df = pd.read_csv(file_path, skiprows=4, sep=",", quotechar='"')

    # --- Clean column names ---
    # Remove leading/trailing whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # --- Identify metadata and period columns ---
    meta_cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] # Columns describing metadata
    period_cols = [c for c in df.columns if c not in meta_cols] # Remaining columns are time periods (years)

    # --- Transform from wide to long format ---
    df_long = df.melt(
        id_vars=meta_cols,       # Columns to keep as-is
        value_vars=period_cols,  # Columns to unpivot
        var_name="TIME_PERIOD",  # Name for the new column containing period labels
        value_name="VALUE"       # Name for the new column containing values
    )

    # --- Clean data ---
    df_long["TIME_PERIOD"] = df_long["TIME_PERIOD"].astype(str).str.strip() # Strip whitespace from period labels
    df_long["VALUE"] = pd.to_numeric(df_long["VALUE"], errors='coerce') # Convert values to numeric, invalid parsing becomes NaN

    # --- Remove empty rows ---
    df_long = df_long.dropna(subset=["VALUE"]) # Drop rows where VALUE is NaN

    # --- Filter by specific country ---
    df_long = df_long[df_long["Country Name"] == "Latvia"] # Keep only rows for Latvia

    # --- Save the processed data ---
    output_file = os.path.join(processed_dir, file.replace(".csv", "_long.csv"))
    df_long.to_csv(output_file, index=False) # Save to CSV without the index
    print(f"Done: {len(df_long)} rows  → {output_file}")
