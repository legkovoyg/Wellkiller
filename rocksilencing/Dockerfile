# rocksilencing/Dockerfile

# Используем официальный Python образ как базовый
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . /app/

# Удаляем команду collectstatic, чтобы избежать перезаписи томов
# RUN python manage.py collectstatic --noinput

# Запускаем Gunicorn
CMD ["gunicorn", "rocksilencing.wsgi:application", "--bind", "0.0.0.0:8000"]
