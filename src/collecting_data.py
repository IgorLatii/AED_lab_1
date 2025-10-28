import eurostat
import pandas as pd
import os

# === Пути к файлам ===
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, '../data/raw')
indicators_path = os.path.join(base_dir, '../reports/indicators.csv')

# Создаём папку для данных, если её нет
os.makedirs(data_dir, exist_ok=True)

# === Загружаем список индикаторов ===
indicators = pd.read_csv(indicators_path, sep='\t')  # если CSV с табами
if 'code' not in indicators.columns:
    indicators = pd.read_csv(indicators_path, sep=',')  # fallback

print(f"Найдено {len(indicators)} индикаторов для загрузки...")

# === Основной цикл ===
for _, ind in indicators.iterrows():
    code = ind['code']
    name = ind.get('name', code)

    print(f"🔽 Загружаем {name} ({code}) ...")
    try:
        # Загружаем весь набор данных
        df = eurostat.get_data_df(code)

        # Проверим структуру
        print(f"  ✅ Успешно загружено: {df.shape[0]} строк, {df.shape[1]} колонок")

        # Сохраняем как есть (raw)
        output_path = os.path.join(data_dir, f"{code}_raw.csv")
        df.to_csv(output_path, index=False)
        print(f"  💾 Сохранено в: {output_path}")

    except Exception as e:
        print(f"  ❌ Ошибка при загрузке {code}: {e}")

print("\n=== Завершено. Все доступные индикаторы сохранены в ../data/raw/ ===")