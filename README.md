# Agro Subsidy — Django + Angular

Система управления заявками на агросубсидии.

## Состав проекта

```
backend/    — Django + DRF (API, JWT аутентификация)
frontend/   — Angular 21 (SPA)
```

## Быстрый старт

### 1. Поднять PostgreSQL + ML сервис (старый проект)
```bash
cd ~/agro_subsidy-modified
docker compose up -d
```

### 2. Запустить Django backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python manage.py runserver 8001
```

### 3. Запустить Angular frontend
```bash
cd frontend
npm install
ng serve
```

Открыть **http://localhost:4200**

## Порты

| Сервис | Порт |
|---|---|
| Angular | 4200 |
| Django API | 8001 |
| PostgreSQL | 5433 |
| ML сервис | 8000 |

## Демо-аккаунты

| Роль | Логин | Пароль |
|---|---|---|
| Администратор | `admin` | `admin` |
| Пользователь | `user` | `user` |

## API эндпоинты (Django)

| Метод | Путь | Описание |
|---|---|---|
| POST | `/api/login/` | Вход, возвращает JWT |
| POST | `/api/submit/` | Подать заявку |
| GET | `/api/applications/` | Список заявок |
| PATCH | `/api/applications/{id}/` | Одобрить / отклонить |
| DELETE | `/api/applications/{id}/` | Удалить заявку |
| GET | `/api/subsidies/` | Справочник субсидий |
| GET | `/api/budget/` | Бюджеты по регионам |
| PATCH | `/api/budget/{id}/` | Обновить бюджет |

## Участники группы

- Алихан
- Бека
- Асланбек
- Иска
