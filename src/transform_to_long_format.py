import re
import pandas as pd
import os

# === Paths ===
base_dir = os.path.dirname(__file__)
raw_dir = os.path.join(base_dir, '../data/raw')
processed_dir = os.path.join(base_dir, '../data/processed/transformed_to_long_format')
# === Create data folder if it doesn't exist ===
os.makedirs(processed_dir, exist_ok=True)

for file in os.listdir(raw_dir):
    if not file.lower().endswith("_raw.csv"):
        continue

    print(f"Обрабатываем {file} ...")

    file_path = os.path.join(raw_dir, file)
    df = pd.read_csv(file_path)

    # Переименовываем колонку Eurostat
    if 'geo\\TIME_PERIOD' in df.columns:
        df = df.rename(columns={'geo\\TIME_PERIOD': 'geo'})

    # Определяем колонки с периодами: содержат год, месяц или квартал
    period_cols = [c for c in df.columns if c[:4].isdigit() or 'Q' in c]
    #period_cols = [c.strip().strip('"') for c in df.columns if c.strip().strip('"').isdigit()]
    print(period_cols)

    # Все остальные колонки — метаданные
    meta_cols = [c for c in df.columns if c not in period_cols]
    print(meta_cols)

    # Melt в длинный формат
    df_long = df.melt(
        id_vars=meta_cols,
        value_vars=period_cols,
        var_name='TIME_PERIOD',
        value_name='VALUE'
    )

    # --- Убираем строки с пустыми значениями ---
    df_long = df_long.dropna(subset=["VALUE"])

    # Сохраняем результат
    output_file = os.path.join(processed_dir, os.path.basename(file).replace(".csv", "_long.csv"))
    df_long.to_csv(output_file, index=False)

    print(f"Готово: {len(df_long)} строк → {output_file}")