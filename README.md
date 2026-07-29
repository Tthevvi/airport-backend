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

Это поднимет PostgreSQL на `localhost:5432` с базой `airport`
## 1.4. Создаём Django-проект

```bash
django-admin startproject config .
```
Это создаст:
```
airport-backend/
├── manage.py
└── config/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
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
Итоговая структура:
```
airport-backend/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── .env / .env.example
├── config/            
├── accounts/
├── references/
├── flights/
├── passengers/
├── bookings/
├── payments/
├── shifts/
├── refunds/
└── audit/
```

Каждое приложение — это модуль из нашей компонентной диаграммы: в нём будут `models.py` (шаг 2), `serializers.py` и `views.py` (шаг 4).

## 1.6. Настраиваем `config/settings.py`

Замените блок `INSTALLED_APPS` и `DATABASES` (полный файл — `settings_snippet.py` рядом, скопируйте нужные куски).

## 1.7. Проверяем, что всё работает

```bash
python manage.py migrate      # применит только встроенные миграции Django, пока без наших моделей
python manage.py runserver
```

Откройте http://127.0.0.1:8000 — должна открыться стартовая страница Django. Если открылась — окружение готово.

## 1.8. Git

```bash
git init
echo "venv/
__pycache__/
*.pyc
.env
db.sqlite3" > .gitignore
git add .
git commit -m "chore: инициализация проекта, окружение, приложения"
```

