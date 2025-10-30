import pandas as pd
import os

# === Paths ===
base_dir = os.path.dirname(__file__) # Base directory of the script
initial_dir = os.path.join(base_dir, '../data/processed/transformed_to_long_format') # Directory with long-format CSVs
processed_dir = os.path.join(base_dir, '../data/processed/formatted_time_periods') # Directory to save formatted CSVs
os.makedirs(processed_dir, exist_ok=True) # Create processed directory if it does not exist

# === Process all Eurostat CSV files ===
for file in os.listdir(initial_dir):
    if not file.endswith('_long.csv'):
        continue

    print(f"Formatting {file} ...")
    path = os.path.join(initial_dir, file)
    df = pd.read_csv(path)

    # --- Remove zero values (considered as missing or invalid data) ---
    df = df[df["VALUE"] != 0]

    # --- Convert TIME_PERIOD to datetime ---
    tp = df['TIME_PERIOD'].astype(str) # Work with string representation of time
    df['TIME_PERIOD'] = df['TIME_PERIOD'].astype(object) # Prepare column for datetime assignment

    # --- Define masks for different time period formats ---
    mask_year = tp.str.match(r'^\d{4}$')            # e.g., '2023'
    mask_month = tp.str.match(r'^\d{4}-\d{2}$')     # e.g., '2023-05'
    mask_quarter = tp.str.match(r'^\d{4}-Q[1-4]$')  # e.g., '2023-Q2'
    mask_semester = tp.str.match(r'^\d{4}-S[1-2]$') # e.g., '2023-S1'

    # --- Year: convert to first day of the year ---
    df.loc[mask_year, 'TIME_PERIOD'] = pd.to_datetime(tp[mask_year] + '-01-01', format='%Y-%m-%d', errors='coerce')
    # --- Month: convert to first day of the month ---
    df.loc[mask_month, 'TIME_PERIOD'] = pd.to_datetime(tp[mask_month] + '-01', format='%Y-%m-%d', errors='coerce')
    # --- Quarter: convert to first month of the quarter ---
    years = tp[mask_quarter].str[:4].astype(int)
    quarters = tp[mask_quarter].str[-1].astype(int)
    months = (quarters - 1) * 3 + 1 # Q1 -> January, Q2 -> April, etc.
    df.loc[mask_quarter, 'TIME_PERIOD'] = pd.to_datetime(
        years.astype(str) + '-' + months.astype(str).str.zfill(2) + '-01',
        format='%Y-%m-%d',
        errors='coerce'
    )

    # --- Semester: convert to first month of the semester ---
    years_s = tp[mask_semester].str[:4].astype(int)
    semesters = tp[mask_semester].str[-1].astype(int)
    months_s = (semesters - 1) * 6 + 1  # S1 -> January, S2 -> July
    df.loc[mask_semester, 'TIME_PERIOD'] = pd.to_datetime(
        years_s.astype(str) + '-' + months_s.astype(str).str.zfill(2) + '-01',
        format='%Y-%m-%d',
        errors='coerce'
    )

    # --- Sort by TIME_PERIOD ---
    df = df.sort_values('TIME_PERIOD')

    # --- Save the formatted CSV ---
    output = os.path.join(processed_dir, file.replace('_long.csv', '_formatted.csv'))
    df.to_csv(output, index=False)
    print(f"Saved: {output}")