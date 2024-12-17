# Используем официальный Python образ с нужной версией
FROM python:3.12-slim

# Устанавливаем зависимости для PostgreSQL (при необходимости)
# Если используете другую базу данных или вообще не используете БД, удалите или измените следующий шаг
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY . /app/

# Собираем статические файлы (при необходимости)
RUN python manage.py collectstatic --noinput

# Устанавливаем переменную окружения для Django
ENV DJANGO_SETTINGS_MODULE=randomsite.settings.production

# Открываем порт 8000 на контейнере
EXPOSE 8000

# Команда запуска Django приложения
# Команда, которая подходит для запуска проекта, следует использовать:
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# Замените `your_project_name` на фактическое имя вашего Django проекта