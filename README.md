# Auth System - Система аутентификации и авторизации

Django + DRF приложение с JWT аутентификацией и системой разграничения прав доступа.

---

## Быстрый старт

```bash
# Установка зависимостей
uv sync

# Миграции
uv run python manage.py migrate

# Запуск сервера
uv run python manage.py runserver
```

---

## API Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/register/` | POST | Регистрация |
| `/api/login/` | POST | Логин (JWT) |
| `/api/logout/` | POST | Логаут |
| `/api/profile/` | GET/PUT | Профиль |
| `/api/profile/delete/` | POST | Удаление аккаунта |

**Swagger:** http://localhost:8000/swagger/

---

## Тесты

```bash
uv run pytest auth_system/tests/ -v
```

15 тестов: регистрация, логин, профиль, логаут, удаление, права доступа.

---

## Схема БД

- **User** — пользователи (email, password, is_active)
- **Role** — роли (admin, manager, user, guest)
- **UserRole** — связь пользователь-роль
- **BusinessObject** — объекты доступа (users, orders, products...)
- **AccessRoleRule** — правила доступа (роль + объект + права)
- **Session** — сессии/токены

---

## Технологии

- Django 5.2 + DRF
- PostgreSQL
- JWT (djangorestframework-simplejwt)
- Swagger (drf-yasg)
- pytest
