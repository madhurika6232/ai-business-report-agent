# Changelog

All notable changes to RetailOps AI are documented here.

The project uses Semantic Versioning.

## [1.0.0] - 2026-09-22

### Added

- Multi-agent retail intelligence architecture
- Business, operations, customer, and risk specialist agents
- Groq-backed natural-language business intelligence
- Retail analytics and machine-learning capabilities
- Delivery-risk modeling and forecasting
- Customer review intelligence
- Guardrails for injection, PII, authorization, grounding, and output validation
- Multi-turn conversation memory
- Agent-to-agent coordination
- MCP resources and tooling
- 19-skill analytical capability registry
- Seven-evaluator AI quality framework
- Persisted RetailOps V1 evaluation baseline
- FastAPI production API
- API authentication, rate limiting, structured logging, request IDs, health, and readiness endpoints
- React and TypeScript production frontend
- Business intelligence dashboard
- Ask RetailOps workspace
- Conversation interface
- Skills Explorer
- Evaluation Dashboard
- Responsive and accessible user interface
- Nginx production gateway
- Server-side API-key injection
- Multi-stage backend and frontend Docker deployment
- Docker Compose production architecture
- Automated backend, frontend, security, Docker, and integration CI workflows

### Security

- Backend credentials are excluded from browser bundles
- Runtime secrets are excluded from Git
- Production frontend uses a trusted Nginx gateway
- Repository CI checks for accidental secret exposure
- Raw datasets and generated model artifacts are excluded from version control

### Quality

- 95 API tests passing
- 323 full Python tests passing
- 41 frontend tests passing
- Frontend ESLint validation passing
- Frontend production build passing
- Production Docker health and readiness checks passing