import os
import pandas as pd

processed_dir = "../data/processed/formatted_time_periods"
output_dir = "../data/processed/merged"
os.makedirs(output_dir, exist_ok=True)

dfs = []

for file in os.listdir(processed_dir):
    if not file.endswith('.csv'):
        continue

    # Убираем суффиксы из названия колонки
    indicator_name = os.path.splitext(file)[0]
    indicator_name = indicator_name.replace('_raw_formatted', '').replace('_formatted', '')

    file_path = os.path.join(processed_dir, file)
    df = pd.read_csv(file_path)

    df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], errors='coerce')
    df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')

    # === Группировка по TIME_PERIOD ===
    # Если в файле есть категории, они будут просуммированы
    df = df.groupby('TIME_PERIOD', as_index=False)['VALUE'].sum()

    # Оставляем только TIME_PERIOD и VALUE
    df = df[['TIME_PERIOD', 'VALUE']].rename(columns={'VALUE': indicator_name})

    # Убираем дубликаты
    df = df.drop_duplicates(subset=['TIME_PERIOD'])

    dfs.append(df)
    print(f"✅ Загружен {indicator_name} ({len(df)} строк)")

# Объединяем всё по TIME_PERIOD
if dfs:
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='TIME_PERIOD', how='outer')

    merged_df = merged_df.sort_values('TIME_PERIOD')
    output_file = os.path.join(output_dir, 'merged_df_clean.csv')
    merged_df.to_csv(output_file, index=False)
    print(f"\n🎯 Успешно создан merged_df_clean.csv ({merged_df.shape[0]} строк, {merged_df.shape[1]} колонок)")
else:
    print("❌ Нет файлов для объединения.")
