# СанычЪ Frontend

Простой Vue 3 + Vite фронтенд для текущего API.

## Запуск

1. Запусти PostgreSQL:

```bash
docker compose up -d
```

2. Запусти backend из корня проекта:

```bash
uvicorn app.main:app --reload --app-dir backend
```

3. В отдельном терминале:

```bash
cd frontend
npm install
npm run dev
```

Открой адрес, который покажет Vite (обычно `http://localhost:5173`).

Vite проксирует `/api/*` на `http://127.0.0.1:8000`, поэтому отдельно настраивать CORS для локальной разработки не нужно.

## Что уже работает

- регистрация: `POST /auth/register`;
- вход: `POST /auth/login`;
- текущий пользователь: `GET /auth/me`;
- список открытых миссий: `GET /missions`;
- свои миссии заказчика: `GET /missions/my`;
- создание миссии: `POST /missions`;
- отклик на миссию: `POST /missions/{mission_id}/apply`;
- JWT хранится в `localStorage`.

Project API в текущем backend пока отсутствует, поэтому при создании миссии `project_id` вводится вручную.
