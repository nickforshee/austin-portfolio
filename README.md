# Austin Kimbell Portfolio

A full-stack theatre educator portfolio built for graduate program applications.

## Features

- Public site with sections for:
  - Professional profile and statement
  - Past shows
  - Accomplishments
  - Teaching work samples
  - Blog posts
  - Photo gallery
- Admin login with content management at /admin
- CRUD for all section entries
- Profile editing from admin

## Stack

- Frontend: Vue 3 + Vite + TypeScript
- Backend: Flask + SQLite + JWT auth

## Local Setup

### 1) Backend

`ash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
`

Backend runs at http://localhost:5050.

### 2) Frontend

`ash
cd frontend
npm install
cp .env.example .env
npm run dev
`

Frontend runs at http://localhost:5173.

## Admin Credentials

Credentials are seeded from backend .env:

- ADMIN_USERNAME
- ADMIN_PASSWORD

The app seeds starter demo data on first run.

## Deployment Notes (Vercel + Domain)

Recommended setup:

1. Deploy rontend/ to Vercel.
2. Deploy ackend/ as a separate API service (Render/Fly.io/Railway, or Vercel Python project).
3. Set VITE_API_URL in Vercel frontend environment variables to your deployed API URL.
4. Attach your custom domain in Vercel and point DNS there.

If you want everything on Vercel only, create two Vercel projects from this repo:

- Frontend project root: rontend
- Backend project root: ackend

Then connect frontend VITE_API_URL to backend URL.
