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

# Авторизация и роли пользователей

## Администратор:

управляет всеми пользователями и паролями,
доступ к админ-панели (/admin/),
может редактировать логины и пароли сотрудников.

## Персонал:

доступ к интерфейсу поиска и редактирования,
может управлять сотрудниками.

## Обычный пользователь:

доступен только просмотр.

# Экспорт сотрудников

В разделе поиска доступна кнопка Экспорт Excel.
Файл будет скачан с именем employees.xlsx.

# REST API через POSTMAN
### (в данный момент в процессе разработки...)

## Авторизация через JWT
### Получение токена:

POST /api/token/
{
  "username": "admin",
  "password": "admin123"
}

### Обновление токена:

POST /api/token/refresh/
{
  "refresh": "..."
}

### Проверка токена:

POST /api/token/verify/
{
  "token": "..."
}

## Эндпоинты API

Метод       URL     Описание
GET	/api/employees/	список сотрудников
POST	/api/employees/	создание сотрудника
GET	/api/employees/{id}/	просмотр сотрудника
PUT	/api/employees/{id}/	обновление сотрудника
DELETE	/api/employees/{id}/	удаление сотрудника
GET	/api/regions/	список регионов
GET	/api/regions/{id}/	просмотр региона

## Технологии

Python 3.10+
Django 5
Django REST Framework
SimpleJWT
Bootstrap 5 (шаблоны)
openpyxl (экспорт Excel)

## Логгирование

Все действия сотрудников фиксируются в таблице ActionLog.
История входов хранится в LoginHistory.
Просмотр доступен в админ-панели.


# Примеры запросов для REST API
### (в данный момент в процессе разработки...)

### Получение токена

curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

Пример ответа:

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}

### Обновление токена

curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'

### Проверка токена

curl -X POST http://127.0.0.1:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token": "your_access_token"}'

## Работа с сотрудниками

### Получение списка сотрудников

curl -X GET http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer your_access_token"

### Создание сотрудника

curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Иванов",
    "first_name": "Иван",
    "patronymic": "Иванович",
    "region_name": 23,
    "region_code": 23,
    "note_date": "2025-09-21",
    "note_number": "123",
    "action": "create"
  }'

### Обновление сотрудника

curl -X PUT http://127.0.0.1:8000/api/employees/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"last_name": "Петров"}'

### Удаление сотрудника

curl -X DELETE http://127.0.0.1:8000/api/employees/1/ \
  -H "Authorization: Bearer your_access_token"

## Работа с регионами

### Получить список регионов

curl -X GET http://127.0.0.1:8000/api/regions/ \
  -H "Authorization: Bearer your_access_token"

### Просмотр конкретного региона

curl -X GET http://127.0.0.1:8000/api/regions/23/ \
  -H "Authorization: Bearer your_access_token"
 
# Postman коллекция

Для удобства можно использовать Postman.
Создан файл postman_collection.json, импортируй его в Postman.

# Контакты:

Автор: Мощук Андрей, Москва, 2025
Эл. почта: dr.sam159ru@yandex.ru
GitHub: https://github.com/DrSam159ru