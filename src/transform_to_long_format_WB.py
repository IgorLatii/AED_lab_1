import os
import pandas as pd

# === Paths ===
base_dir = os.path.dirname(__file__)
raw_dir = os.path.join(base_dir, '../data/raw')
processed_dir = os.path.join(base_dir, '../data/processed/transformed_to_long_format')
os.makedirs(processed_dir, exist_ok=True)

for file in os.listdir(raw_dir):
    if not file.lower().endswith("126864.csv"):
        continue

    print(f"Обрабатываем {file} ...")
    file_path = os.path.join(raw_dir, file)

    # Пропускаем первые 4 строки метаданных (источник, дата, пустая, заголовки)
    df = pd.read_csv(file_path, skiprows=4, sep=",", quotechar='"')

    # Убираем пробелы из названий колонок
    df.columns = [c.strip() for c in df.columns]

    # Определяем метаданные и годы
    meta_cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    period_cols = [c for c in df.columns if c not in meta_cols]

    # Преобразуем в long формат
    df_long = df.melt(
        id_vars=meta_cols,
        value_vars=period_cols,
        var_name="TIME_PERIOD",
        value_name="VALUE"
    )

    # Чистим значения
    df_long["TIME_PERIOD"] = df_long["TIME_PERIOD"].astype(str).str.strip()
    df_long["VALUE"] = pd.to_numeric(df_long["VALUE"], errors='coerce')

    # Убираем пустые строки
    df_long = df_long.dropna(subset=["VALUE"])

    # --- Фильтруем только Latvia ---
    df_long = df_long[df_long["Country Name"] == "Latvia"]

    # Сохраняем результат
    output_file = os.path.join(processed_dir, file.replace(".csv", "_long.csv"))
    df_long.to_csv(output_file, index=False)
    print(f"Готово: {len(df_long)} строк → {output_file}")
