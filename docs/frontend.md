# RetailOps AI Frontend Guide

## Overview

RetailOps AI includes a production React frontend for interacting with
the FastAPI-based retail intelligence platform.

The frontend provides:

- business intelligence dashboard
- AI business query workspace
- multi-turn conversations
- conversation memory
- skills explorer
- evaluation dashboard
- structured answer rendering
- safety and trust indicators
- responsive layouts
- accessibility support
- loading, error, empty, and 404 states
- production Docker deployment

---

## Technology Stack

The frontend uses:

```text
React
TypeScript
Vite
React Router
TanStack Query
Recharts
Lucide React
React Markdown
Remark GFM
Vitest
React Testing Library
Nginx
Docker
```

---

## Architecture

Development architecture:

```text
Browser
   ↓
React / Vite
   ↓
FastAPI
   ↓
RetailOps guardrails
   ↓
LangGraph / agents
   ↓
Groq / analytical tools
```

Production architecture:

```text
Browser
   ↓
Nginx :8080
   ├── React SPA
   │
   └── /api/*
          ↓
     server-side X-API-Key
          ↓
       FastAPI
          ↓
       Guardrails
          ↓
     RetailOps agents
          ↓
       Groq / tools
```

Backend credentials are never compiled into the browser application.

---

## Frontend Directory

```text
frontend/
├── src/
│   ├── app/
│   ├── components/
│   │   ├── common/
│   │   ├── conversation/
│   │   ├── dashboard/
│   │   ├── evaluation/
│   │   ├── layout/
│   │   ├── query/
│   │   └── skills/
│   ├── hooks/
│   ├── layouts/
│   ├── pages/
│   ├── services/
│   ├── test/
│   ├── types/
│   └── utils/
├── Dockerfile
├── nginx.conf.template
├── docker-entrypoint.sh
├── .dockerignore
├── .env.example
├── .env.production.example
├── package.json
└── vite.config.ts
```

---

## Application Routes

### Overview

```text
/
```

Provides:

- platform status
- official quality baseline
- evaluator coverage
- skill count
- release status
- quick actions
- platform health

---

## Ask RetailOps

```text
/query
```

Provides:

- business-question composer
- suggested questions
- loading state
- guarded AI response
- Markdown rendering
- agent indicators
- trust indicators
- authentication/rate-limit error handling

Example question:

```text
How is the business performing?
```

---

## Conversations

```text
/conversations
```

Provides:

- multi-turn analysis
- browser session IDs
- conversation memory
- follow-up resolution
- Markdown assistant responses
- specialist-agent indicators
- new-session controls
- session deletion

Example:

```text
How was revenue in March 2018?
```

Follow-up:

```text
What about the previous month?
```

RetailOps can resolve the follow-up using conversation context.

---

## Skills Explorer

```text
/skills
```

Displays the live RetailOps skill catalog.

Capabilities are grouped into:

```text
Business
Operations
Customer
Risk
```

The interface supports:

- domain filtering
- text search
- responsive skill cards
- live skill count

The current catalog contains 19 analytical skills.

---

## Evaluation Dashboard

```text
/evaluation
```

Displays the persisted RetailOps evaluation configuration and baseline.

Current official V1 baseline:

```text
Name: retailops_baseline_v1
Overall score: 92.82
Release decision: PASS
Evaluators: 7
```

Viewing the evaluation dashboard does not execute the expensive
Groq-backed evaluation suite.

---

## Frontend Environment Configuration

Development:

```text
frontend/.env
```

Example:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Production:

```text
frontend/.env.production.example
```

Production normally uses:

```dotenv
VITE_API_BASE_URL=
```

An empty API base URL causes browser requests to use the same origin
as the production Nginx gateway.

---

## Secret Safety

Never place these values in frontend environment variables:

```text
GROQ_API_KEY
RETAILOPS_API_KEY
```

Never create:

```text
VITE_GROQ_API_KEY
VITE_RETAILOPS_API_KEY
```

for production.

Vite variables are browser-accessible and must not contain backend
credentials.

The production bundle is validated to ensure backend secret names and
values are not included.

---

## Development

From the project root, start FastAPI:

```powershell
.\venv\Scripts\Activate.ps1

uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

From another terminal:

```powershell
cd frontend

npm run dev
```

The development frontend is normally available at:

```text
http://localhost:5173
```

---

## Frontend Build

From:

```text
frontend/
```

run:

```powershell
npm run build
```

The production bundle is written to:

```text
frontend/dist/
```

---

## Linting

Run:

```powershell
npm run lint
```

Production changes should leave ESLint clean.

---

## Frontend Tests

Run:

```powershell
npm test
```

The suite covers:

- query composer
- Markdown answer rendering
- blocked responses
- conversation messages
- conversation context
- session utilities
- API client
- shared application states
- 404 behavior
- Skills filtering/search
- Evaluation rendering
- routing
- sidebar navigation
- frontend secret safety
- production configuration

---

## Accessibility

The application includes:

- semantic navigation
- accessible form labels
- visible keyboard focus
- skip-to-main-content navigation
- keyboard-operable controls
- responsive layouts
- reduced-motion support

---

## Responsive Design

The interface is designed for:

```text
Desktop
Laptop
Tablet
Mobile
```

Primary layouts adapt at approximately:

```text
1050px
900px
800px
760px
700px
```

---

## Production Docker Build

The frontend uses a multi-stage Docker build.

Build stage:

```text
node:24-alpine
```

Runtime stage:

```text
nginx:1.29-alpine
```

The Node stage compiles React.

Only the generated `dist/` application is copied into the runtime
Nginx image.

---

## Production Nginx Gateway

Nginx performs two responsibilities:

```text
Serve React static assets
Proxy RetailOps API requests
```

Protected requests under:

```text
/api/
```

are forwarded to:

```text
http://backend:8000
```

The Nginx runtime injects:

```text
X-API-Key
```

using the server-side:

```text
RETAILOPS_API_KEY
```

The credential is never exposed to browser JavaScript.

---

## Runtime Secret Injection

The frontend container receives the backend API key through Docker
runtime environment configuration.

The startup script validates that the key exists before Nginx starts.

The key is inserted into the runtime Nginx configuration.

It is not part of:

```text
React source
Vite environment
React production bundle
Docker build arguments
browser requests
browser storage
```

---

## Docker Compose

From the project root:

```powershell
docker compose build
```

Start:

```powershell
docker compose up -d
```

Check:

```powershell
docker compose ps
```

Expected:

```text
retailops-backend     healthy
retailops-frontend    healthy
```

Production frontend:

```text
http://localhost:8080
```

---

## Production Health

Through the Nginx gateway:

```text
GET /health
GET /ready
```

Expected:

```text
/health → 200
/ready  → 200
```

---

## SPA Routing

Nginx uses an SPA fallback so direct navigation works for:

```text
/query
/conversations
/skills
/evaluation
/settings
```

Refreshing a frontend route should return the React application rather
than an Nginx 404.

---

## Production Authentication Validation

A protected missing-session request through Nginx should return:

```text
404
```

rather than an authentication error.

This demonstrates:

```text
request
   ↓
Nginx
   ↓
server-side X-API-Key
   ↓
FastAPI authentication
   ↓
session lookup
   ↓
404 missing session
```

---

## Production AI Smoke Test

A successful production query follows:

```text
Browser
   ↓
Nginx
   ↓
FastAPI authentication
   ↓
Guardrails
   ↓
Router
   ↓
Specialist agent
   ↓
Groq / tools
   ↓
Output validation
   ↓
Nginx
   ↓
React
```

A validated production smoke request returned:

```text
POST /api/v1/query → 200
```

with structured request logging and no sensitive query content in the
API logs.

---

## Logging Privacy

Production backend logs include:

```text
timestamp
request ID
method
path
status code
latency
```

They do not intentionally include:

```text
business question text
conversation content
GROQ_API_KEY
RETAILOPS_API_KEY
model prompts
model responses
```

---

## Production Bundle Security Check

After building:

```powershell
Get-ChildItem -Path frontend\dist -Recurse -File |
    Select-String -Pattern "GROQ_API_KEY|RETAILOPS_API_KEY|VITE_RETAILOPS_API_KEY"
```

Expected:

```text
no output
```

---

## Troubleshooting

### Frontend development site unavailable

Run:

```powershell
cd frontend
npm run dev
```

Use the exact URL printed by Vite.

---

### Backend unavailable

From the project root:

```powershell
uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Check:

```text
http://127.0.0.1:8000/health
```

---

### Production frontend unavailable

Check:

```powershell
docker compose ps
```

Then:

```powershell
docker compose logs frontend --tail 100
```

---

### Frontend container restarting

Verify the root backend `.env` contains:

```text
RETAILOPS_API_KEY
```

and that the frontend Compose service receives the root `.env` through
`env_file`.

Never solve this by putting the API key into a `VITE_*` variable.

---

### CORS errors during Vite development

Development CORS should permit:

```text
http://localhost:5173
http://127.0.0.1:5173
```

Production same-origin requests through Nginx do not require the
browser to know the backend container address.

---

## Phase 13 Production Checklist

Before releasing the frontend:

```text
[ ] npm tests pass
[ ] TypeScript production build passes
[ ] ESLint passes
[ ] No backend secrets in frontend bundle
[ ] Dashboard loads live API data
[ ] Ask RetailOps works
[ ] Conversation memory works
[ ] Skills Explorer works
[ ] Evaluation Dashboard works
[ ] Unknown routes show 404 UI
[ ] Keyboard navigation works
[ ] Responsive layouts work
[ ] Backend Docker container healthy
[ ] Frontend Docker container healthy
[ ] /health returns 200 through Nginx
[ ] /ready returns 200 through Nginx
[ ] SPA route refresh works
[ ] Protected proxy authentication works
[ ] Production AI smoke request returns 200
[ ] Sensitive request content is absent from logs
```

---

## Production Architecture Summary

RetailOps AI now provides:

```text
React + TypeScript frontend
Professional analytics workspace
AI query experience
Conversation memory
Skills Explorer
Evaluation Dashboard
Responsive design
Accessibility support
Typed FastAPI client
Automated frontend tests
Secret-safe browser bundle
Nginx production gateway
Server-side API authentication
Frontend Docker image
Backend Docker image
Docker Compose deployment
Container health checks
Production smoke validation
```