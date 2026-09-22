# RetailOps AI Production Guide

## 1. Overview

RetailOps AI is a guarded multi-agent retail analytics platform served through FastAPI.

The production application provides:

- guarded business queries
- multi-agent routing and orchestration
- conversation memory
- session management
- skills discovery
- evaluation status
- prompt-injection protection
- PII protection
- numeric grounding validation
- request IDs
- structured JSON logging
- request latency tracking
- API-key authentication
- rate limiting
- CORS controls
- health and readiness checks
- Docker deployment support
- Docker Compose support
- production configuration validation

The current official evaluation baseline is:

```text
Baseline: retailops_baseline_v1
Overall score: 92.82
Release decision: PASS
```

---

## 2. Requirements

The application currently uses:

```text
Python 3.12
FastAPI
Uvicorn
LangGraph
Groq
Pydantic
Pandas
scikit-learn
Docker
Docker Compose
```

Install Python dependencies with:

```powershell
pip install -r requirements.txt
```

Verify dependency consistency with:

```powershell
pip check
```

Expected:

```text
No broken requirements found.
```

---

## 3. Environment Configuration

RetailOps AI uses environment variables for runtime configuration and secrets.

Never hardcode production credentials in application source code.

### Development template

Use:

```text
.env.example
```

as the development configuration template.

### Production template

Use:

```text
.env.production.example
```

as the production configuration template.

Never place real credentials in either example file.

---

## 4. Required Production Environment Variables

A production deployment requires:

```text
RETAILOPS_ENV=production
GROQ_API_KEY
RETAILOPS_API_KEY
RETAILOPS_API_DEBUG=false
RETAILOPS_API_DOCS_ENABLED=false
RETAILOPS_CORS_ORIGINS
```

Example:

```dotenv
RETAILOPS_ENV=production

GROQ_API_KEY=replace-with-production-groq-key
RETAILOPS_API_KEY=replace-with-strong-production-api-key

RETAILOPS_API_TITLE=RetailOps AI API
RETAILOPS_API_VERSION=1.0.0

RETAILOPS_API_DEBUG=false
RETAILOPS_API_DOCS_ENABLED=false

RETAILOPS_CORS_ORIGINS=https://app.example.com
```

Multiple CORS origins may be supplied as a comma-separated list.

Example:

```dotenv
RETAILOPS_CORS_ORIGINS=https://app.example.com,https://admin.example.com
```

---

## 5. Secret Management

Real secrets should be stored only in local or deployment environment files or the deployment platform's secret-management system.

The project ignores environment files such as:

```text
.env
.env.local
.env.production
```

Safe templates remain available:

```text
.env.example
.env.production.example
```

Never commit:

```text
GROQ_API_KEY
RETAILOPS_API_KEY
```

with real credential values.

Never place `.env` files inside a Docker image.

---

## 6. Local Development

Navigate to the project:

```powershell
cd C:\Users\madhu\Documents\ai-business-report-agent
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal should show:

```text
(venv) PS C:\Users\madhu\Documents\ai-business-report-agent>
```

Start the API:

```powershell
uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Expected startup output includes:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

Stop the server with:

```text
Ctrl+C
```

---

## 7. Development API Documentation

When API documentation is enabled, FastAPI exposes:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

Production configuration must use:

```dotenv
RETAILOPS_API_DOCS_ENABLED=false
```

In production, these endpoints should return:

```text
404 Not Found
```

---

## 8. Health Checks

RetailOps AI separates process liveness from application readiness.

### Liveness

Endpoint:

```text
GET /health
```

Example:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok",
  "service": "RetailOps AI"
}
```

`/health` answers:

> Is the API process alive?

---

## 9. Readiness

Endpoint:

```text
GET /ready
```

Example:

```text
http://127.0.0.1:8000/ready
```

Expected:

```json
{
  "status": "ready",
  "service": "RetailOps AI"
}
```

`/ready` validates the application's configuration for the active environment.

Production readiness requires valid production configuration.

---

## 10. API Endpoints

### Health

```text
GET /health
```

### Readiness

```text
GET /ready
```

### Guarded business query

```text
POST /api/v1/query
```

### Memory-aware conversation

```text
POST /api/v1/conversation
```

### Get conversation session

```text
GET /api/v1/sessions/{session_id}
```

### Delete conversation session

```text
DELETE /api/v1/sessions/{session_id}
```

### Skills catalog

```text
GET /api/v1/skills
```

### Evaluation status

```text
GET /api/v1/evaluation
```

The evaluation-status endpoint reports configuration and the persisted baseline. It does not launch the expensive evaluation suite.

---

## 11. API Authentication

Protected API endpoints use:

```text
X-API-Key
```

The configured server-side value comes from:

```text
RETAILOPS_API_KEY
```

Example request header:

```text
X-API-Key: <configured-api-key>
```

The API compares credentials safely and rejects missing or invalid credentials.

Protected endpoints include the expensive query/conversation workflows and session-management endpoints.

Health and public metadata endpoints remain accessible according to application configuration.

---

## 12. Guardrails

Production queries pass through the RetailOps guardrail layer.

The system includes:

- prompt-injection detection
- PII detection/redaction
- numeric grounding validation
- safe output validation
- protection against exposing internal prompts and implementation details

Retrieved text and customer content are treated as untrusted data rather than instructions.

Unsupported or unsafe output can be contained before reaching the final user response.

---

## 13. Rate Limiting

Expensive AI-backed endpoints use an in-memory rate limiter.

Current defaults:

```text
Maximum requests: 10
Window: 60 seconds
```

The limiter protects Groq-backed endpoints from accidental request bursts and unnecessary quota consumption.

The current implementation is appropriate for a single-process deployment.

For a multi-instance production deployment, replace the in-memory limiter with a shared mechanism such as:

```text
Redis
API Gateway
Load-balancer rate limiting
Managed platform rate limiting
```

---

## 14. Request IDs

Every API request receives a correlation ID.

Header:

```text
X-Request-ID
```

If the client supplies an existing request ID, the API preserves it.

Otherwise, the API generates a new UUID.

The response includes the same request ID.

Request IDs allow operational events to be correlated without logging sensitive request content.

---

## 15. Structured Logging

RetailOps API logs are emitted as structured JSON.

Example:

```json
{
  "timestamp": "2026-08-26T17:52:22.711085+00:00",
  "level": "INFO",
  "logger": "retailops.api",
  "message": "request_completed",
  "request_id": "example-request-id",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "latency_ms": 3.42
}
```

Operational logs may contain:

```text
timestamp
log level
request ID
HTTP method
route/path
status code
latency
error type
```

The application intentionally does not log:

```text
request bodies
business query text
conversation content
API keys
Groq keys
authorization headers
PII
model prompts
model responses
```

---

## 16. Error Handling

Unexpected internal exceptions pass through the centralized API error handler.

The API returns sanitized errors rather than raw Python exceptions.

Internal responses do not expose:

```text
stack traces
local filesystem paths
API keys
internal prompts
implementation details
raw exception messages containing secrets
```

Known HTTP errors such as missing sessions preserve their appropriate status codes.

---

## 17. CORS

Development defaults allow:

```text
http://localhost:3000
http://127.0.0.1:3000
```

Production should explicitly configure:

```text
RETAILOPS_CORS_ORIGINS
```

Example:

```dotenv
RETAILOPS_CORS_ORIGINS=https://app.example.com
```

Avoid unrestricted production configuration such as:

```text
*
```

unless there is a specific architectural reason for it.

---

## 18. Application Lifecycle

RetailOps AI uses a FastAPI application lifespan.

At startup:

- production configuration is validated
- application startup is logged

At shutdown:

- in-memory conversation sessions are cleared
- application shutdown is logged

This provides deterministic process startup and shutdown behavior.

---

## 19. Docker

The project includes:

```text
Dockerfile
.dockerignore
docker-compose.yml
```

The production image uses:

```text
python:3.12-slim
```

and serves the application using:

```text
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

---

## 20. Build the Docker Image

From the project root:

```powershell
docker build -t retailops-ai:phase12 .
```

Verify:

```powershell
docker images retailops-ai
```

Expected repository/tag:

```text
retailops-ai    phase12
```

---

## 21. Docker Secret Safety

`.dockerignore` excludes sensitive/runtime files including:

```text
.env
.env.*
venv/
.venv/
__pycache__/
.pytest_cache/
outputs/
reports/
data/evaluation/checkpoints/
```

Safe environment templates may remain available.

Never use:

```dockerfile
COPY .env .
```

Never bake production secrets into an image.

Secrets should be supplied at runtime.

---

## 22. Run Docker Locally

Development-style runtime:

```powershell
docker run -d `
  --name retailops-api `
  -p 8000:8000 `
  --env-file .env `
  retailops-ai:phase12
```

Check:

```powershell
docker ps
```

View logs:

```powershell
docker logs retailops-api
```

Stop:

```powershell
docker stop retailops-api
```

Remove:

```powershell
docker rm retailops-api
```

---

## 23. Production Docker Runtime

Create a local:

```text
.env.production
```

based on:

```text
.env.production.example
```

Never commit the real production file.

Start:

```powershell
docker run -d `
  --name retailops-production-test `
  -p 8000:8000 `
  --env-file .env.production `
  retailops-ai:phase12
```

Check logs:

```powershell
docker logs retailops-production-test
```

Expected startup includes:

```text
application_started
Application startup complete.
```

---

## 24. Docker Health Check

The image contains a Docker health check against:

```text
http://127.0.0.1:8000/health
```

Inspect health:

```powershell
docker inspect --format="{{.State.Health.Status}}" retailops-production-test
```

Expected:

```text
healthy
```

---

## 25. Docker Compose

Start the application:

```powershell
docker compose up -d
```

Check:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs
```

Check container health:

```powershell
docker inspect --format="{{.State.Health.Status}}" retailops-api
```

Expected:

```text
healthy
```

Stop and remove Compose resources:

```powershell
docker compose down
```

---

## 26. Production Smoke Test

A successful production deployment should satisfy:

```text
GET /health         -> 200
GET /ready          -> 200
GET /docs           -> 404
GET /redoc          -> 404
GET /openapi.json   -> 404
Docker health       -> healthy
```

No Groq request is required to perform this infrastructure smoke test.

---

## 27. Production Configuration Validation

Production startup rejects invalid configuration.

Examples of invalid production states include:

```text
missing GROQ_API_KEY
missing RETAILOPS_API_KEY
placeholder credentials
debug enabled
API documentation enabled
invalid RETAILOPS_ENV
missing/invalid production CORS configuration
```

The goal is to fail during startup/configuration validation rather than during the first user request.

---

## 28. Evaluation Framework

RetailOps AI contains seven standardized evaluators:

```text
router
tool_selection
review_classifier
numeric_grounding
guardrails
multi_agent
answer_quality
```

Evaluation execution supports:

```text
PASS
WARNING
FAIL
INCOMPLETE
```

`INCOMPLETE` distinguishes infrastructure/API execution failures from genuine model-quality failures.

---

## 29. Official Phase 10 Baseline

Official baseline:

```text
retailops_baseline_v1
```

Overall score:

```text
92.82 / 100
```

Release decision:

```text
PASS
```

Evaluator scores:

```text
Router                100.00
Tool selection        100.00
Review classifier      97.00
Numeric grounding      66.35
Guardrails             100.00
Multi-agent            100.00
Answer quality         100.00
```

The numeric-grounding normalized score includes diagnostic warnings.

The release-critical grounding containment metric passed at:

```text
100%
```

The persisted baseline is:

```text
data/evaluation/baselines/retailops_baseline_v1.json
```

The evaluation report is:

```text
reports/retailops_evaluation_v1.md
```

---

## 30. Evaluation Checkpoints

Large Groq-backed evaluations can be persisted individually.

Checkpoint directory:

```text
data/evaluation/checkpoints/
```

This prevents successful evaluator results from being lost when Groq quota is exhausted or a process is restarted.

A completed evaluator can be checkpointed and later combined with the remaining evaluator results.

Incomplete evaluator results must not be saved as official checkpoints/baselines.

---

## 31. Groq Rate Limits

Large evaluation workloads can consume significant Groq token capacity.

Avoid repeatedly rerunning complete evaluation suites when only one evaluator remains incomplete.

Prefer:

```text
run evaluator
    ↓
checkpoint successful result
    ↓
run next evaluator
```

This prevents unnecessary token consumption.

The production application and offline evaluation workloads should eventually use separate capacity strategies where appropriate.

---

## 32. Testing

Run API tests:

```powershell
pytest tests/api -q
```

Run the complete project:

```powershell
pytest -q
```

Check dependencies:

```powershell
pip check
```

The project should remain fully green before deployment.

---

## 33. Container Configuration Tests

The automated test suite validates:

- Dockerfile existence
- Python 3.12 base image
- production Uvicorn command
- Docker healthcheck
- `.dockerignore` secret protection
- virtual-environment exclusion
- Compose configuration
- Compose healthcheck configuration

These tests validate deployment configuration without requiring Docker Desktop during every pytest run.

---

## 34. Security Validation

Production validation covers:

- API-key authentication
- prompt-injection guardrails
- PII guardrails
- sanitized internal errors
- restricted CORS
- rate limiting
- production debug disabled
- production API docs disabled
- environment secrets excluded from Docker images
- request-body privacy in logs
- authorization/header privacy in logs

---

## 35. Troubleshooting

### Docker command not found

Verify Docker Desktop is installed and running.

Run:

```powershell
docker --version
```

If Docker was installed after VS Code was opened, restart the terminal or VS Code so it receives the updated PATH.

For a per-user Docker Desktop installation, the executable may be located under:

```text
%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin
```

---

### Docker engine unavailable

Run:

```powershell
docker info
```

Make sure Docker Desktop reports:

```text
Engine running
```

---

### Verify Docker installation

Run:

```powershell
docker run --rm hello-world
```

Expected:

```text
Hello from Docker!
```

---

### API will not start

Check:

```text
RETAILOPS_ENV
GROQ_API_KEY
RETAILOPS_API_KEY
RETAILOPS_API_DEBUG
RETAILOPS_API_DOCS_ENABLED
RETAILOPS_CORS_ORIGINS
```

For development, ensure the virtual environment is active.

---

### Readiness fails

Check production configuration.

Production requires:

```text
GROQ_API_KEY
RETAILOPS_API_KEY
RETAILOPS_API_DEBUG=false
RETAILOPS_API_DOCS_ENABLED=false
RETAILOPS_CORS_ORIGINS
```

---

### Authentication fails

Verify:

```text
RETAILOPS_API_KEY
```

and send the matching header:

```text
X-API-Key
```

---

### Rate limited

The API may return:

```text
429 Too Many Requests
```

for application-level rate limiting.

Groq may independently return rate-limit errors for:

```text
TPM
TPD
```

Avoid repeated expensive evaluation runs when quota is constrained.

---

### Groq requests fail

Verify:

```text
GROQ_API_KEY
```

Then check Groq quota/rate-limit information.

Infrastructure health can still be tested through `/health` and `/ready` without making an expensive AI query.

---

## 36. Deployment Checklist

Before deployment verify:

```text
[ ] Production environment variables configured
[ ] Real secrets are not committed
[ ] Debug disabled
[ ] API docs disabled
[ ] Production CORS origin configured
[ ] API authentication enabled
[ ] pip check passes
[ ] API tests pass
[ ] Full project tests pass
[ ] Docker image builds
[ ] Docker container starts
[ ] /health returns 200
[ ] /ready returns 200
[ ] /docs returns 404 in production
[ ] /openapi.json returns 404 in production
[ ] Docker reports healthy
[ ] Structured logs contain request IDs
[ ] Sensitive request content is not logged
[ ] Official evaluation baseline remains available
```

---

## 37. Current Production Baseline

At the completion of the production-hardening work, RetailOps AI has:

```text
Guarded multi-agent platform
FastAPI production API
Conversation memory
Session management
19-skill catalog
Evaluation framework
Official V1 evaluation baseline
API-key authentication
Rate limiting
CORS controls
Structured JSON logging
Request IDs
Latency tracking
Production configuration validation
Docker image
Docker Compose configuration
Container health checks
Production documentation
```

Any production change should preserve the automated regression suite and should be evaluated against the existing RetailOps V1 quality baseline.