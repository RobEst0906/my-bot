FROM python:3.11-slim

# Устанавливаем gcc и дополнительные библиотеки
RUN apt-get update && apt-get install -y gcc python3-dev libffi-dev && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запускаем бота
CMD ["python", "bot.py"]
