# Services

## Backend
- Start App: `uvicorn backend.src.main:fastapi --reload`
- Environment" `poetry init`
    1. `poetry shell`
    2. `poetry add uvicorn uvloop httptools fastapi pydantic pydantic_settings redis openai itsdangerous asyncpg sqlmodel`

## Frontend
- Start App (dev) - make sure you're in correct folder: `npm run dev`
- To Create: `npm create vite@latest`

## Database
- To inspect: `docker compose exec db psql --username=postgres --dbname=postgres`
- `\dt`