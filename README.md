# Ed-Tech Demo

A full-stack ed-tech application with a Python backend and a Nuxt frontend.

## Tech Stack

**Backend** — Python 3.13, FastAPI, SQLAlchemy, PostgreSQL, JWT auth (PyJWT + argon2), Uvicorn

**Frontend** — Nuxt 4, Vue 3, TypeScript, Tailwind CSS, Zod

**Testing** — Pytest + pytest-cov (backend), Vitest (frontend)

---

## Prerequisites

- Python 3.13+
- Node.js 20+
- PostgreSQL

---

## Backend

```bash
cd backend
```

Create a `.env` file:

```env
DB_URL="postgresql://<user>:<password>@localhost:5432/ed-tech-db"
SECRET_KEY=<your-secret-key>
```

Install dependencies and run:

```bash
pip install -r requirements.txt
make run-seed
make run-server
```

The API will be available at `http://localhost:8000`.

---
