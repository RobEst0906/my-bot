# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем build-essential и другие необходимые пакеты
RUN apt-get update && apt-get install -y build-essential gcc

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Запускаем приложение
CMD ["python", "bot.py"]  # Замените на ваш главный файл
