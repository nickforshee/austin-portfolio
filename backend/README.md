# Backend (Flask API)

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Environment Variables

- `DATABASE_URL`: Optional SQLAlchemy database URL (Postgres recommended for production)
- `JWT_SECRET_KEY`: Long random secret for JWT signing
- `ADMIN_USERNAME`: Seeded admin username
- `ADMIN_PASSWORD`: Seeded admin password
- `PORT`: Flask bind port (default `5050`)
- `CORS_ORIGINS`: Comma-separated frontend origins allowed to call `/api/*`
- `AUTO_INIT_DB`: If `true`, runs table creation and seed on startup/import

Example:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
JWT_SECRET_KEY=replace-with-a-long-random-secret
ADMIN_USERNAME=austin
ADMIN_PASSWORD=change-me
PORT=5050
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
AUTO_INIT_DB=true
```

API base URL (default): `http://localhost:5050/api`

## One-time manual DB init (optional)

```bash
cd backend
source .venv/bin/activate
python -c "from app import init_db; init_db()"
```
