import asyncio
import aiohttp
import sqlite3
from aiohttp import ClientTimeout

# Функция для проверки доступности домена
async def check_domain(domain_name):
    url = f"https://{domain_name}"
    try:
        # Устанавливаем таймаут для HTTP-запроса
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=10)) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
    except Exception as e:
        print(f"Error checking domain {domain_name}: {str(e)}")
    return False

# Функция для обработки доменов
async def process_domains(domains, cursor):
    tasks = []
    for domain in domains:
        task = asyncio.create_task(check_domain(domain[1]))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)

    # Удаляем неактуальные домены и остаемся с доступными
    inaccessible_domains = [domain for domain, is_accessible in zip(domains, results) if not is_accessible]
    
    for domain in inaccessible_domains:
        print(f"Domain {domain[1]} is not accessible and will be deleted.")
        cursor.execute("DELETE FROM domains WHERE id = ?", (domain[0],))

async def periodic_commit(conn, interval):
    """Функция, которая периодически сохраняет изменения в базе данных."""
    try:
        while True:
            await asyncio.sleep(interval)
            conn.commit()
            print("Database changes committed.")
    except asyncio.CancelledError:
        # Если таск будет отменен, следует сделать финальный commit
        conn.commit()
        print("Final database changes committed upon cancellation.")

# Основная функция
async def main():
    # Подключаемся к базе данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Извлекаем все домены
    cursor.execute("SELECT * FROM domains")
    all_domains = cursor.fetchall()

    # Запуск периодического сохранения изменений
    commit_task = asyncio.create_task(periodic_commit(conn, 10))

    try:
        for i in range(0, len(all_domains), 10):
            batch = all_domains[i:i+10]
            await process_domains(batch, cursor)

    finally:
        # Корректно завершаем таск сохранения, обработка при завершении
        commit_task.cancel()
        await commit_task

        # Обязательно сохраняем все изменения перед закрытием соединения
        conn.close()

if __name__ == "__main__":
    asyncio.run(main())