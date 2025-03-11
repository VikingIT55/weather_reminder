

FROM python:3.13

# Робоча директорія
WORKDIR /DjangoWeatherReminder
COPY . .

# Оновлення pip та встановлення залежностей
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "weather_reminder.wsgi:application", "--bind", "0.0.0.0:8000"]

