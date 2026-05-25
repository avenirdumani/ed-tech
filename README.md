# Ed-Tech Demo

**[Watch Demo Video](https://www.loom.com/share/77655a7214ea4ceeaed5b309c9c27a8c)**

A full-stack ed-tech application with a Python backend and a Nuxt frontend.

> **Disclaimer:** This project was built within a 3-hour time limit. As a result, there are known rough edges — frontend pagination is functional but could be smoother, and parts of the backend could be refactored for better readability and maintainability. These are conscious trade-offs made under time constraints, not oversights.

---

## Prerequisites

- Python 3.13+
- Node.js 20+
- PostgreSQL

---

## Docker Compose

The fastest way to run the full stack using Docker.

```bash
docker compose up --build
```

| Service  | URL                        |
| -------- | -------------------------- |
| Frontend | http://localhost:3000      |
| API      | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

The database is seeded automatically on first startup.

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
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make run-seed
make run-server
```

The API will be available at `http://localhost:8000` & the docs of the API at `http://localhost:8000/docs`.

---

## Frontend

```bash
cd frontend
```

Create a `.env` file:

```env
BASE_API_URL=http://localhost:8000
```

Install dependencies and run:

```bash
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

---

## Tests

### Running tests

**Backend**

```bash
cd backend
make run-tests
```

**Frontend**

```bash
cd frontend
npm test
```

## Features

### Current

- Applicant profile management (personal info, documents, status tracking)
- JWT-based authentication with protected routes
- Application and program browsing
- Role-based access control foundation

### Roadmap

#### User Roles & Organizations

- Multiple user types: applicants, counselors, admins, and super-admins, each with scoped permissions
- Organization accounts for schools and other educational institutions — a dedicated backoffice to manage admissions pipelines, onboarding workflows, document review, and applicant communications

#### Authentication

- OAuth 2.0 sign-in with third-party providers (Google, Microsoft, etc.) alongside existing email/password
- Account linking so users can connect multiple providers to a single profile

#### Search, Filtering & Pagination

- Cursor- and offset-based pagination to support large result sets
- Composable filter system with multi-field, range, and full-text search options
- Saved filters and sortable table views

#### Notifications

- In-app notification center organized by type: rejected documents, approaching deadlines, note reminders, and status updates
- Email and SMS delivery channels powered by a transactional provider (e.g. SendGrid, Twilio)
- Per-user notification preferences — choose which events trigger which channels

#### Interview Scheduling

- In-app interview scheduling with time-slot management and calendar availability
- Integrations with video platforms (Zoom, Google Meet, Microsoft Teams) to auto-generate meeting links
- Automated confirmation and reminder notifications for participants

#### Dashboard Widgets

- Modular, configurable dashboard with drag-and-drop layout
- Calendar widget showing deadlines, interview dates, and document due dates
- Application pipeline summary, recent activity feed, and quick-action shortcuts

#### Backend Observability

- Structured JSON logging with request tracing and correlation IDs
- Sentry integration for error tracking and performance monitoring
- Datadog integration for metrics, APM traces, and alerting

#### Deployment & CI/CD

- Target cloud platform: AWS (ECS Fargate or App Runner for containers, RDS for PostgreSQL, S3/CloudFront for the frontend)
- GitHub Actions pipeline with environment promotion: `feature/*` branches deploy to dev, `main` deploys to staging, tags (`v*`) deploy to production
- Docker image versioning tied to branch name and commit SHA
- Infrastructure as Code via Terraform or AWS CDK (to be decided)

---

## Tech Stack

**Backend** — Python 3.13, FastAPI, SQLAlchemy, PostgreSQL, JWT auth (PyJWT + argon2), Uvicorn

**Frontend** — Nuxt 4, Vue 3, TypeScript, Tailwind CSS, Zod

**Testing** — Pytest + pytest-cov (backend), Vitest (frontend)
