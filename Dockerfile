FROM python:3.11

# Установить gcc и другие нужные пакеты
RUN apt-get update && apt-get install -y gcc python3-dev libffi-dev && rm -rf /var/lib/apt/lists/*

# Установить зависимости Python
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
