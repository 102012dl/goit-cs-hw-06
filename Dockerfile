# syntax=docker/dockerfile:1

# Базовий образ
FROM python:3.9-slim

# Встановлення залежностей
RUN pip install pymongo pillow

# Копіювання коду
COPY . /app
WORKDIR /app

# Запуск серверів
CMD ["python", "main.py"]
