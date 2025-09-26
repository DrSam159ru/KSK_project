# Проект КСК

Django-система для управления сотрудниками с поддержкой авторизации, ролей пользователей, логгирования, поиска и REST API (DRF + JWT).

## Функционал

Авторизация пользователей (логин/логаут).

## Главная страница с меню:

создание сотрудника,
поиск сотрудников,
помощь,
выход.

## Сотрудники:

фамилия, имя, отчество (ФИО),
регион (название и код),
дата и номер служебной записки,
логин (автогенерация),
пароль (автогенерация по правилам, можно редактировать админом),
действия: создать, редактировать, удалить, заблокировать.

## Автоматическая генерация пароля по правилам (количество букв, цифр, символов настраивается в админке).

## Логгирование:

все действия (создание, редактирование, удаление),
история входов.

## Экспорт сотрудников в Excel.

## REST API с DRF:

управление сотрудниками и регионами,
аутентификация через JWT.

# Установка и запуск
1. Клонирование репозитория
git clone https://github.com/username/ksk_project.git
cd ksk_project

2. Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate   # для Linux/Mac
.venv\Scripts\activate      # для Windows

3. Установка зависимостей
pip install -r requirements.txt

4. Применение миграций
python manage.py makemigrations
python manage.py migrate

5. Загрузка регионов из JSON
python manage.py loaddata employees/fixtures/regions.json

6. Создание суперпользователя
python manage.py createsuperuser

7. Запуск сервера
python manage.py runserver

Сайт откроется по адресу: http://127.0.0.1:8000

# Роли пользователей

## Admin
Имеет полный доступ ко всем разделам и API.

## Manager
Может управлять сотрудниками (создавать, редактировать, блокировать).

## Viewer
Может только просматривать данные.

# Аутентификация

Используется JWT через djangorestframework-simplejwt.

## Получение токена:

POST /api/token/
{
  "username": "user",
  "password": "password"
}

## Обновление токена:

POST /api/token/refresh/

## Проверка токена:

POST /api/token/verify/

# API эндпоинты

## Сотрудники

GET /api/v1/employees/ — список сотрудников

POST /api/v1/employees/ — создать сотрудника

GET /api/v1/employees/{id}/ — детали сотрудника

PUT/PATCH /api/v1/employees/{id}/ — обновить сотрудника

DELETE /api/v1/employees/{id}/ — удалить сотрудника

Фильтры: status, region_name, region_code
Поиск: last_name, first_name, patronymic
Сортировка: last_name, first_name, created_at

## Регионы

GET /api/v1/regions/ — список регионов

POST /api/v1/regions/ — создать регион

GET /api/v1/regions/{id}/ — детали региона

PUT/PATCH /api/v1/regions/{id}/ — обновить регион

DELETE /api/v1/regions/{id}/ — удалить регион

## Политика паролей

GET /api/v1/password-policies/ — список правил

POST /api/v1/password-policies/ — создать правило

GET /api/v1/password-policies/{id}/ — детали правила

PUT/PATCH /api/v1/password-policies/{id}/ — обновить правило

DELETE /api/v1/password-policies/{id}/ — удалить правило


# Примеры запросов и ответов API

## Аутентификация (JWT)

### Запрос
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "adminpassword"
}

### Ответ
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...long_token...",
  "access": "eyJ0eXAiOiJKV1QiLCJh...short_token..."
}

## Сотрудники

### Получить список сотрудников
GET /api/v1/employees/?status=active&ordering=last_name
Authorization: Bearer <access_token>

### Ответ
[
  {
    "id": 1,
    "last_name": "Иванов",
    "first_name": "Иван",
    "patronymic": "Иванович",
    "region_name": {
      "id": 1,
      "code": "77",
      "name": "Москва"
    },
    "region_code": {
      "id": 1,
      "code": "77",
      "name": "Москва"
    },
    "status": "active",
    "created_at": "2025-09-26T12:45:30Z",
    "updated_at": "2025-09-26T12:45:30Z"
  }
]

### Создать сотрудника
POST /api/v1/employees/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "last_name": "Петров",
  "first_name": "Петр",
  "patronymic": "Петрович",
  "region_name": 1,
  "region_code": 1,
  "status": "active"
}

### Ответ
{
  "id": 2,
  "last_name": "Петров",
  "first_name": "Петр",
  "patronymic": "Петрович",
  "region_name": 1,
  "region_code": 1,
  "status": "active"
}

## Регионы
### Получить список регионов
GET /api/v1/regions/?ordering=code
Authorization: Bearer <access_token>

### Ответ
[
  {
    "id": 1,
    "code": "77",
    "name": "Москва"
  },
  {
    "id": 2,
    "code": "78",
    "name": "Санкт-Петербург"
  }
]

## Политика паролей
### Создать правило
POST /api/v1/password-policies/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "uppercase": 1,
  "lowercase": 1,
  "digits": 1,
  "symbols": 1,
  "allowed_symbols": "!@#$%^&*"
}

### Ответ
{
  "id": 1,
  "uppercase": 1,
  "lowercase": 1,
  "digits": 1,
  "symbols": 1,
  "allowed_symbols": "!@#$%^&*"
}

# Postman-коллекция для тестирования API:
## В коллекции у каждого ресурса (employees, regions, password-policies) есть полный набор:

GET (list),
POST (create),
PATCH (update),
DELETE (delete).

В Authorization используется Bearer 
{{access_token}}, переменная задаётся один раз.

### Можно:

Импортировать коллекцию в Postman → File → Import → выбрать postman_collection.json.

Сначала выполнить запрос Auth → Получение токена, скопировать access.

В переменной {{access_token}} прописать этот токен (можно в разделе Collection Variables).

Тестировать все эндпоинты:
- employees (CRUD),
- regions (CRUD),
- password-policies (CRUD).

# Технологии:

Python 3.10+
Django 5
Django REST Framework
SimpleJWT
Bootstrap 5 (шаблоны)
openpyxl (экспорт Excel)

# Логгирование:

Все действия сотрудников фиксируются в таблице ActionLog.
История входов хранится в LoginHistory.
Просмотр доступен в админ-панели.

# Контакты:

Автор: Мощук Андрей, Москва, 2025
Эл. почта: dr.sam159ru@yandex.ru
GitHub: https://github.com/DrSam159ru