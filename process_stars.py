import pandas as pd
import numpy as np
import json

# 1. Загрузка файла
# Пропускаем строки с комментариями (#)
print("Загружаю файл... это может занять время, если файл большой.")
file_path = 'data.csv'
df = pd.read_csv(file_path, comment='#', low_memory=False)

# 2. Очистка: оставляем только звезды с известным расстоянием (parallax)
# Паллакс должен быть положительным, чтобы мы могли вычислить дистанцию
df = df.dropna(subset=['ra', 'dec', 'parallax', 'phot_g_mean_mag'])
df = df[df['parallax'] > 0]

# 3. Ограничение: выберем 10 000 самых ярких звезд, чтобы браузер не тормозил
# phot_g_mean_mag — чем меньше значение, тем ярче звезда
df = df.sort_values('phot_g_mean_mag').head(10000)

print(f"Обрабатываю {len(df)} звезд...")

# 4. Конвертация в 3D координаты (X, Y, Z)
stars = []
for _, row in df.iterrows():
    # Расстояние в парсеках
    r = 1000 / row['parallax']
    
    # Переводим градусы в радианы
    ra_rad = np.radians(row['ra'])
    dec_rad = np.radians(row['dec'])
    
    # Сферические координаты -> Декартовы
    x = r * np.cos(dec_rad) * np.cos(ra_rad)
    y = r * np.cos(dec_rad) * np.sin(ra_rad)
    z = r * np.sin(dec_rad)
    
    stars.append({
        "x": round(float(x), 2),
        "y": round(float(y), 2),
        "z": round(float(z), 2),
        "mag": round(float(row['phot_g_mean_mag']), 2)
    })

# 5. Сохраняем результат
output_file = 'stars_data.json'
with open(output_file, 'w') as f:
    json.dump(stars, f)

print(f"Готово! Файл {output_file} создан. Можешь использовать его в Three.js.")