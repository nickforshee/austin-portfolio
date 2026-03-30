# Backend (Flask API)

## Setup

`ash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
`

## Environment Variables

- JWT_SECRET_KEY: Long random secret for JWT signing
- ADMIN_USERNAME: Seeded admin username
- ADMIN_PASSWORD: Seeded admin password
- PORT: Flask bind port (default 5000)
- CORS_ORIGINS: Comma-separated frontend origins allowed to call /api/*

Example:

`env
JWT_SECRET_KEY=replace-with-a-long-random-secret
ADMIN_USERNAME=austin
ADMIN_PASSWORD=change-me
PORT=5000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
`

API base URL (default): http://localhost:5050/api
