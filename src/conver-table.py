import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta

# Зчитуємо дані з CSV-файлу (замініть 'your_dataset.csv' на назву свого файлу)
df = pd.read_csv('data/ev_charging_patterns.csv')

# Генеруємо випадковий timestamp для кожного рядка у 2025 році
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31, 23, 59, 59)
total_seconds = int((end_date - start_date).total_seconds())

def generate_random_timestamp():
    random_seconds = random.randint(0, total_seconds)
    return (start_date + timedelta(seconds=random_seconds)).strftime('%Y-%m-%d %H:%M:%S')

df['timestamp'] = [generate_random_timestamp() for _ in range(len(df))]

# Підключаємося до бази даних (файл 'mydatabase.db' буде створено)
conn = sqlite3.connect('main.db')

# Записуємо DataFrame у базу даних SQLite
# Якщо таблиця вже існує, вона буде замінена
df.to_sql('Start Table', conn, if_exists='replace', index=False)

# Закриваємо з'єднання
conn.close()

print("Дані успішно імпортовано до 'main.db'")