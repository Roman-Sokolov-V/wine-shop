#!/bin/sh


echo "🔄 Створюємо міграції..."
python manage.py makemigrations --noinput

echo "🔄 Застосовуємо міграції..."
python manage.py migrate --noinput

echo "🧹 Збираємо статичні файли..."
python manage.py collectstatic --noinput

echo "🚀 Запускаємо Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
