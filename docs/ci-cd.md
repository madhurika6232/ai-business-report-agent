# RetailOps AI CI/CD Guide

## Overview

RetailOps AI uses GitHub Actions to automate quality validation,
security checks, production image builds, integration testing, and
versioned releases.

The CI/CD system is designed so application changes can be validated
from a clean repository checkout without depending on developer
machine state.

---

## CI Architecture

The project contains the following workflows:

```text
.github/workflows/
├── backend-ci.yml
├── frontend-ci.yml
├── security-ci.yml
├── docker-ci.yml
├── integration-ci.yml
├── ci.yml
└── release.yml
```

The primary quality gates are:

```text
Push / Pull Request
        │
        ├── Backend CI
        ├── Frontend CI
        ├── Security CI
        ├── Docker CI
        └── Integration CI
```

The release workflow runs separately when a semantic-version Git tag
is pushed.

---

## Backend CI

Workflow:

```text
backend-ci.yml
```

Triggers:

```text
push → main
pull request → main
manual workflow dispatch
```

The backend workflow:

1. Checks out the repository.
2. Installs Python 3.12.
3. Installs `requirements-dev.txt`.
4. Runs `pip check`.
5. Runs the API regression suite.
6. Runs the complete Python regression suite.

Current validated baseline:

```text
API tests:        95 passed
Full Python:     323 passed
```

The test count may increase as new tests are added. CI success is based
on zero failures/errors rather than an exact permanent test count.

---

## Backend Dependencies

Production/runtime dependencies are defined in:

```text
requirements.txt
```

Development and test dependencies are defined in:

```text
requirements-dev.txt
```

The development manifest includes the runtime manifest:

```text
-r requirements.txt
```

This allows CI and local development environments to reproduce the
complete test environment without installing test packages into the
production Docker image.

---

## Frontend CI

Workflow:

```text
frontend-ci.yml
```

The frontend workflow uses Node.js 24 and performs:

```text
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
production bundle secret scan
```

Current validated baseline:

```text
Frontend tests:     41 passed
npm audit:          0 vulnerabilities
ESLint:             PASS
Production build:   PASS
Secret scan:        CLEAN
```

`package-lock.json` is version controlled so `npm ci` installs the
dependency tree deterministically.

---

## Security CI

Workflow:

```text
security-ci.yml
```

The security workflow checks the repository for accidental exposure of
credentials and inappropriate generated artifacts.

Checks include:

- Groq-style credential patterns
- forbidden tracked `.env` files
- browser-side secret assignments
- tracked files larger than 10 MB
- raw/processed datasets
- generated model binaries

The following files must never be committed:

```text
.env
.env.production
frontend/.env
frontend/.env.production
```

Safe templates are version controlled:

```text
.env.example
.env.production.example
frontend/.env.example
frontend/.env.production.example
```

---

## Secret Management

Runtime credentials must not be committed to Git.

Important backend secrets include:

```text
GROQ_API_KEY
RETAILOPS_API_KEY
```

Frontend code must never receive:

```text
VITE_GROQ_API_KEY
VITE_RETAILOPS_API_KEY
```

Vite environment variables are browser-accessible and therefore are
not appropriate for backend credentials.

Production authentication uses the Nginx server boundary to inject the
RetailOps API credential when proxying requests to FastAPI.

---

## Dataset Policy

Large raw and generated datasets are excluded from version control:

```text
data/raw/
data/processed/
```

Small evaluation assets are intentionally version controlled:

```text
data/evaluation/
```

Small demonstration data may also be committed:

```text
sample_data/
```

Generated model binaries are excluded:

```text
*.joblib
*.pkl
*.pickle
```

Models should be reproducible from source code and documented data
rather than relying on untracked binary state.

---

## Docker CI

Workflow:

```text
docker-ci.yml
```

Docker CI validates the production container build from a clean GitHub
runner.

It:

1. Validates Docker Compose configuration.
2. Builds the backend production image.
3. Builds the frontend production image.
4. Verifies both images exist.
5. Checks the frontend image for environment files.
6. Reports the generated image sizes.

Production components:

```text
retailops-ai
retailops-frontend
```

---

## Production Container Architecture

```text
Browser
   │
   ▼
Nginx / React
   │
   │ /api/*
   ▼
FastAPI
   │
   ├── Guardrails
   ├── Router
   ├── Specialist agents
   ├── Analytics / ML
   └── Groq
```

FastAPI is not directly exposed to the browser in the production
Compose topology.

---

## Integration CI

Workflow:

```text
integration-ci.yml
```

Integration CI launches the real production Docker Compose stack.

The workflow creates temporary CI-only runtime credentials and does not
use production secrets.

It validates:

```text
backend container health
frontend container health
GET /health
GET /ready
React SPA root
SPA route fallback
protected API proxy authentication
```

No real Groq query is executed in routine integration CI.

This keeps CI deterministic and avoids unnecessary external API usage,
network dependency, and model quota consumption.

---

## Protected Proxy Validation

Integration CI requests a deliberately nonexistent protected session.

Expected response:

```text
404
```

The request path is:

```text
CI
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

Receiving `404` instead of an authentication error demonstrates that
the trusted Nginx proxy successfully authenticated with FastAPI.

---

## CI Status Workflow

Workflow:

```text
ci.yml
```

This workflow reports the result of completed RetailOps CI workflows.

The individual workflows remain the primary required checks:

```text
Backend CI
Frontend CI
Security CI
Docker CI
Integration CI
```

For a protected `main` branch, these checks should be configured as
required status checks in GitHub repository settings.

---

## Versioning

RetailOps AI uses Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

The canonical project version is stored in:

```text
VERSION
```

Current V1 version:

```text
1.0.0
```

Git release tags include the `v` prefix:

```text
v1.0.0
```

The tag must match the contents of the `VERSION` file.

---

## Changelog

Release history is maintained in:

```text
CHANGELOG.md
```

Each release should document meaningful additions, security changes,
quality improvements, fixes, and operational changes.

---

## Release Automation

Workflow:

```text
release.yml
```

The release workflow triggers on semantic-version tags:

```text
v*.*.*
```

Example:

```text
v1.0.0
```

The workflow:

1. Reads the `VERSION` file.
2. Confirms the Git tag matches the project version.
3. Installs backend dependencies.
4. Runs the full Python regression.
5. Installs frontend dependencies.
6. Runs frontend tests.
7. Runs frontend lint.
8. Builds the production frontend.
9. Scans the frontend bundle for forbidden secret references.
10. Builds the backend release image.
11. Builds the frontend release image.
12. Creates the GitHub Release.

A release is not published if release validation fails.

---

## Creating a Release

Before creating a release:

```text
1. Update VERSION.
2. Update CHANGELOG.md.
3. Run the complete regression suite.
4. Commit the release changes.
5. Push the main branch.
6. Confirm all required CI workflows pass.
```

Then create the release tag:

```bash
git tag v1.0.0
```

Push it:

```bash
git push origin v1.0.0
```

The tag triggers the automated release workflow.

Do not create or push the release tag until the corresponding commit
has passed all required CI checks.

---

## Pull Request Quality Gates

Recommended required checks for `main`:

```text
Backend CI
Frontend CI
Security CI
Docker CI
Integration CI
```

A pull request should not merge if any required gate fails.

---

## Local Backend Validation

From the project root:

```powershell
pip check
python -m pytest tests/api -q
python -m pytest -q
```

If local Windows application-control policy prevents compiled Python
dependencies from loading, the same regression can be run in the
Linux Docker environment.

---

## Local Frontend Validation

From:

```text
frontend/
```

run:

```powershell
npm ci
npm audit
npm test
npm run lint
npm run build
```

Then scan the generated bundle:

```powershell
Get-ChildItem -Path dist -Recurse -File |
    Select-String -Pattern "GROQ_API_KEY|RETAILOPS_API_KEY|VITE_RETAILOPS_API_KEY"
```

Expected:

```text
no output
```

---

## Local Docker Validation

Build the backend:

```powershell
docker build -t retailops-ai:ci .
```

Build the frontend:

```powershell
docker build `
  --build-arg VITE_API_BASE_URL="" `
  -t retailops-frontend:ci `
  .\frontend
```

Validate Compose:

```powershell
docker compose config --quiet
```

---

## CI Troubleshooting

### Backend dependency failure

Run:

```text
pip check
```

and verify both dependency manifests.

---

### Frontend dependency failure

Use:

```text
npm ci
```

rather than `npm install` when reproducing CI.

Ensure `package-lock.json` matches `package.json`.

---

### Docker build failure

Reproduce locally with:

```text
docker build ...
```

Avoid relying on locally cached files that are excluded from Git.

---

### Integration container unhealthy

Inspect:

```text
docker compose ps
docker compose logs backend
docker compose logs frontend
```

---

### Secret scan failure

Never bypass the security workflow to ship a credential.

Determine whether the match is:

```text
real credential
placeholder
test fixture
documentation example
```

Real credentials must be revoked/rotated and removed from Git history
before release.

---

## Phase 14 Release Gate

Before Phase 14 is complete:

```text
[ ] backend dependency environment reproducible
[ ] frontend dependency environment reproducible
[ ] Backend CI defined
[ ] Frontend CI defined
[ ] Security CI defined
[ ] Docker CI defined
[ ] Integration CI defined
[ ] CI status workflow defined
[ ] release workflow defined
[ ] VERSION configured
[ ] CHANGELOG updated
[ ] CI/CD documentation complete
[ ] repository secret scan clean
[ ] staged secret scan clean
[ ] API regression passes
[ ] full Python regression passes
[ ] frontend tests pass
[ ] frontend lint passes
[ ] frontend production build passes
[ ] frontend bundle secret scan clean
[ ] backend Docker build passes
[ ] frontend Docker build passes
[ ] production Compose smoke test passes
[ ] GitHub Actions pass from clean checkout
```

---

## Current V1 Quality Baseline

```text
Backend API tests        95 passed
Full Python tests       323 passed
Frontend tests           41 passed
Frontend vulnerabilities  0
Frontend lint             PASS
Frontend build            PASS
Bundle secret scan        CLEAN
Backend container         HEALTHY
Frontend container        HEALTHY
Health endpoint           200
Readiness endpoint        200
```

---

## Summary

RetailOps AI CI/CD provides automated validation across:

```text
Source control
Dependencies
Backend tests
Frontend tests
Security
Docker images
Production topology
Release versioning
GitHub releases
```

The delivery pipeline is designed to ensure that RetailOps AI V1 can
be reproduced and validated from source without depending on local
developer machine state.