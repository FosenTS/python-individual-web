import csv
import sqlite3

# Имя CSV-файла
csv_file = 'domains.csv'

# Подключение к базе данных SQLite3 (если базы нет, будет создана)
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# Создание таблицы (если уже не создана)
cur.execute('''
    CREATE TABLE IF NOT EXISTS domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain_name TEXT,
        registrar_name TEXT,
        expiry_date TEXT
    )
''')

# Функция для чтения CSV и вставки данных в базу данных
def import_csv_to_db(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain_name = row['domain_name']
            registrar_name = row['registrar_name']
            expiry_date = row['expiry_date']
            
            # Вставка данных в таблицу
            cur.execute('''
                INSERT INTO domains (domain_name, registrar_name, expiry_date)
                VALUES (?, ?, ?)
            ''', (domain_name, registrar_name, expiry_date))
            print(f'Добавлен домен: {domain_name}, Регистратор: {registrar_name}, Срок истечения: {expiry_date}')

    # Сохранение изменений в базе данных
    conn.commit()

# Вызов функции импорта данных из CSV
import_csv_to_db(csv_file)

# Закрытие подключения к базе данных
conn.close()