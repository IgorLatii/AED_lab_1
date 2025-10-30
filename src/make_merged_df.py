import os
import pandas as pd

processed_dir = "../data/processed/formatted_time_periods"
output_dir = "../data/processed/merged"
os.makedirs(output_dir, exist_ok=True)

# === Маппинг технических названий в понятные ===
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

dfs = []

for file in os.listdir(processed_dir):
    if not file.endswith('.csv'):
        continue

    indicator_name = os.path.splitext(file)[0]
    indicator_name = indicator_name.replace('_raw_formatted', '').replace('_formatted', '')

    file_path = os.path.join(processed_dir, file)
    df = pd.read_csv(file_path)

    df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], errors='coerce')
    df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')

    # === Группировка по TIME_PERIOD ===
    df = df.groupby('TIME_PERIOD', as_index=False)['VALUE'].sum()

    # === Применяем читаемое имя индикатора ===
    readable_name = indicator_mapping.get(indicator_name, indicator_name)
    df = df[['TIME_PERIOD', 'VALUE']].rename(columns={'VALUE': readable_name})

    df = df.drop_duplicates(subset=['TIME_PERIOD'])
    dfs.append(df)
    print(f"✅ Загружен {readable_name} ({len(df)} строк)")

# === Объединяем всё по TIME_PERIOD ===
if dfs:
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='TIME_PERIOD', how='outer')

    merged_df = merged_df.sort_values('TIME_PERIOD')
    output_file = os.path.join(output_dir, 'merged_df_readable.csv')
    merged_df.to_csv(output_file, index=False)

    print(f"\n🎯 Успешно создан merged_df_readable.csv ({merged_df.shape[0]} строк, {merged_df.shape[1]} колонок)")
else:
    print("❌ Нет файлов для объединения.")
