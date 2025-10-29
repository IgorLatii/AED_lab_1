import pandas as pd
import os

base_dir = os.path.dirname(__file__)
initial_dir = os.path.join(base_dir, '../data/processed/transformed_to_long_format')
processed_dir = os.path.join(base_dir, '../data/processed/formatted_time_periods')

for file in os.listdir(initial_dir):
    if not file.endswith('_long.csv'):
        continue

    print(f"Formatting {file} ...")
    path = os.path.join(initial_dir, file)
    df = pd.read_csv(path)

    # Преобразуем TIME_PERIOD в datetime (векторно)
    tp = df['TIME_PERIOD'].astype(str)
    df['TIME_PERIOD'] = df['TIME_PERIOD'].astype(object)

    mask_year = tp.str.match(r'^\d{4}$')
    mask_month = tp.str.match(r'^\d{4}-\d{2}$')
    mask_quarter = tp.str.match(r'^\d{4}-Q[1-4]$')

    df.loc[mask_year, 'TIME_PERIOD'] = pd.to_datetime(tp[mask_year] + '-01-01', format='%Y-%m-%d', errors='coerce')
    df.loc[mask_month, 'TIME_PERIOD'] = pd.to_datetime(tp[mask_month] + '-01', format='%Y-%m-%d', errors='coerce')

    years = tp[mask_quarter].str[:4].astype(int)
    quarters = tp[mask_quarter].str[-1].astype(int)
    months = (quarters - 1) * 3 + 1
    df.loc[mask_quarter, 'TIME_PERIOD'] = pd.to_datetime(
        years.astype(str) + '-' + months.astype(str).str.zfill(2) + '-01',
        format='%Y-%m-%d',
        errors='coerce'
    )

    #df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], errors='coerce')

    # Можно отсортировать, если нужно
    df = df.sort_values('TIME_PERIOD')

    # Сохраняем результат
    output = os.path.join(processed_dir, file.replace('_long.csv', '_formatted.csv'))
    df.to_csv(output, index=False)
    print(f"✓ Saved: {output}")