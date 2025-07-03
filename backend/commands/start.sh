#!/bin/bash
echo "🔄 Створюємо міграції..."
python manage.py makemigrations --noinput
echo "🔄 Застосовуємо міграції..."
python manage.py migrate --noinput

echo "🧹 Очищуємо та збираємо статичні файли..."
rm -rf /app/staticfiles/*
python manage.py collectstatic --noinput

echo "📁 Перевіряємо створені статичні файли..."
ls -la /app/staticfiles/
echo "📁 Перевіряємо admin файли..."
find /app/staticfiles -name "*admin*" -type d
echo "📁 Загальна кількість файлів:"
find /app/staticfiles -type f | wc -l
echo "📁 Структура статичних файлів:"
tree /app/staticfiles/ -L 2 2>/dev/null || find /app/staticfiles -type d | head -10

echo "🚀 Запускаємо Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
