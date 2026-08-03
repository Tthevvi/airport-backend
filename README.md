# Шаг 1. Окружение и структура проекта

## 1.1. Необходимые
- Python 3.11+ (проверить: `python3 --version`)
- Docker Desktop (для локальной PostgreSQL)
- Git

## 1.2. Разворачиваем окружение

```bash
# создаём виртуальное окружение
python3 -m venv venv

# активируем venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# ставим зависимости (файл requirements.txt приложен)
pip install -r requirements.txt
```

## 1.3. Поднимаем PostgreSQL в Docker
Запустите:

```bash
docker compose up -d
docker compose ps        # убедиться, что airport_db запущен
```
## 1.4. Создаём Django-проект

```bash
django-admin startproject config .
```

## 1.5. Создаём приложения (по одному на каждый сервис из компонентной диаграммы)

```bash
python manage.py startapp accounts     # Cashier, роли, аутентификация
python manage.py startapp references   # Airport, Direction, AircraftType, Tariff (справочники)
python manage.py startapp flights      # Flight, Seat
python manage.py startapp passengers   # Passenger
python manage.py startapp bookings     # Booking
python manage.py startapp payments     # Payment
python manage.py startapp shifts       # Shift
python manage.py startapp refunds      # Refund
python manage.py startapp audit        # AuditLog
```
## 1.6. Проверяем, что всё работает

```bash
python manage.py migrate      # применит только встроенные миграции Django, пока без наших моделей
python manage.py runserver
```
## 1.7. Git

```bash
git init
git add .
git commit -m "комментарий"
```

