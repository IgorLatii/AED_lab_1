import pandas as pd
import os

# === Пути ===
input_file = "../data/processed/merged/merged_df_readable.csv"
output_dir = "../data/processed/merged"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "merged_df_annual.csv")

# === Загрузка merged_df ===
df = pd.read_csv(input_file, parse_dates=['TIME_PERIOD'])

# === Годовая агрегация ===
df['Year'] = df['TIME_PERIOD'].dt.year

# Список непрерывных индикаторов для интерполяции
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

# Список дискретных/событийных индикаторов (оставляем пропуски)
discrete_cols = [
    'Net Migration (World Bank)',
    'Unemployment Rate',
    'Emigration of Citizens'
]

# Агрегация по году
agg_dict = {col: 'sum' for col in continuous_cols}  # суммируем транспорт, экономику
agg_dict.update({col: 'mean' for col in discrete_cols})  # среднее для дискретных, чтобы иметь одно значение за год

annual_df = df.groupby('Year').agg(agg_dict).reset_index()

# Интерполяция непрерывных индикаторов (линейная)
annual_df[continuous_cols] = annual_df[continuous_cols].interpolate(method='linear')

# Сохраняем результат
annual_df.to_csv(output_file, index=False)
print(f"🎯 Успешно создан merged_df_annual.csv ({annual_df.shape[0]} строк, {annual_df.shape[1]} колонок)")
