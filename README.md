# Dating API

REST API для платформы знакомств на Django REST Framework.

## Стек

- Python 3.14
- Django 6.1
- Django REST Framework
- SimpleJWT (JWT-авторизация)
- drf-spectacular (Swagger)
- SQLite локально, PostgreSQL в Docker
- Docker + docker-compose

## Запуск локально

1. Клонировать репозиторий:
   git clone https://github.com/VerMishelle-26/dating_api/upload
   cd dating-api

2. Установить зависимости:
   pip install -r requirements.txt

3. Применить миграции:
   python manage.py migrate

4. Создать суперпользователя:
   python manage.py createsuperuser

5. Запустить сервер:
   python manage.py runserver

Сервер откроется на http://127.0.0.1:8000/

## Запуск через Docker

1. Собрать и запустить контейнеры:
   docker-compose up --build

2. Применить миграции:
   docker-compose exec web python manage.py migrate

3. Создать суперпользователя:
   docker-compose exec web python manage.py createsuperuser

Примечание: Docker-конфигурация приложена (Dockerfile, docker-compose.yml).
Локально Docker не запускался из-за отсутствия поддержки виртуализации
на учебном ноутбуке. На машине с работающим Docker проект запускается
командой docker-compose up --build.

## Документация API

Swagger: http://127.0.0.1:8000/swagger/
ReDoc:   http://127.0.0.1:8000/redoc/
Admin:   http://127.0.0.1:8000/admin/

## Как авторизоваться в Swagger

1. Получить токен через POST /api/token/ (email + password).
2. Нажать кнопку Authorize справа сверху.
3. Ввести только сам токен (без слова Bearer, Swagger добавит его сам).
4. Нажать Authorize, потом Close.

## Эндпоинты

Пользователи:
- POST /api/users/register/ — регистрация
- GET  /api/users/me/ — мой профиль
- GET  /api/users/ — список пользователей
- POST /api/users/{id}/add_photo/ — добавить фото

Авторизация:
- POST /api/token/ — получить JWT
- POST /api/token/refresh/ — обновить токен

Взаимодействия:
- POST /api/interactions/likes/ — лайк/дизлайк
- GET  /api/interactions/likes/liked/ — кого я лайкнул
- GET  /api/interactions/likes/disliked/ — кого я дизлайкнул
- GET  /api/interactions/random/ — случайный профиль с фильтрами
- GET  /api/interactions/views/ — история просмотров
- POST /api/interactions/invitations/ — приглашение на свидание

Пример лайка:

POST /api/interactions/likes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "to_user": 2,
  "type": "like"
}

Ответ 201 Created:

{
  "id": 1,
  "from_user": "admin@example.com",
  "to_user": 2,
  "type": "like",
  "created_at": "2026-09-25T19:18:09.491Z"
}

## Фильтры случайного профиля

GET /api/interactions/random/?gender=F&city=Москва&age_min=20&age_max=30

Параметры:
- gender — M / F / O
- city — город (частичное совпадение)
- status — searching / busy / friends / relationship
- age_min — минимальный возраст
- age_max — максимальный возраст

## Тесты

Запуск:
python manage.py test interactions

Ожидаемый результат:
Found 5 test(s).
Ran 5 tests in ...s
OK

## Структура проекта

config/ — настройки Django
users/ — пользователи, профиль, фото
interactions/ — лайки, просмотры, приглашения
media/ — загруженные файлы
manage.py — управляющий скрипт
requirements.txt — зависимости
Dockerfile, docker-compose.yml — конфигурация Docker
README.md — этот файл

## Модели

User — пользователь системы (email, ФИО, пол, возраст, город, увлечения, статус, приватность, главное фото).

Photo — фотогалерея пользователя. Одна фотография может быть заглавной.

Like — лайк или дизлайк пользователя. Уникальная пара (from_user, to_user).

ProfileView — история просмотренных профилей.

DateInvitation — приглашение на свидание при взаимном лайке.

## Переменные окружения (.env)

SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=*
USE_POSTGRES=False
POSTGRES_DB=dating
POSTGRES_USER=dating
POSTGRES_PASSWORD=dating
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_URL=redis://localhost:6379/0

## Автор

VerMishelle
GitHub: https://github.com/VerMishelle-26