# Dockerfile
# Базовый образ с Python 3.10
FROM python:3.10-slim

# Настраиваем рабочую директорию
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Указываем переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Открываем порт
EXPOSE 5000

# По умолчанию запускаем gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
