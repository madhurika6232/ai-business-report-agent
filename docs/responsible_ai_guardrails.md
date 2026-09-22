# RetailOps AI — Responsible AI & Guardrails

## Overview

RetailOps AI uses a centralized guardrail layer to protect user input,
agent/tool execution, LLM-generated output, sensitive information, and
business evidence.

The guardrail architecture follows:

User Input
→ Input Validation
→ Injection Detection
→ PII Redaction
→ Agent Routing
→ Authorization
→ Trusted Tools
→ Evidence
→ LLM Synthesis
→ Output Validation
→ Grounding Validation
→ Audit
→ User

## Input Validation

User queries are normalized and validated before agent execution.

Protections include:

- empty-input rejection
- query-length limits
- whitespace normalization
- unsupported control-character detection

## Prompt Injection

RetailOps AI detects common prompt-injection patterns including:

- instruction override attempts
- system/developer prompt extraction
- role manipulation
- authorization bypass attempts
- guardrail bypass attempts

Benign language containing words such as "ignore" is not automatically
treated as malicious.

The current adversarial development set contains 15 labeled examples.

Measured performance:

- Detection accuracy: 100%
- False positives: 0
- False negatives: 0

These results apply only to the current development evaluation set and are
not guarantees against arbitrary attacks.

## Untrusted Data

Customer reviews, retrieved content, and external structured data are treated
as untrusted data.

External content is explicitly separated from system instructions before
being supplied to an LLM.

Instructions appearing inside customer or retrieved content must never
override application policy.

## PII Protection

The current PII layer detects and redacts:

- email addresses
- phone numbers
- payment-card-like numbers

Redaction occurs before sensitive text is passed deeper into the agent
workflow when detected.

The current 15-case development evaluation achieved:

- PII detection accuracy: 100%
- False positives: 0
- False negatives: 0

The regex-based detector is intentionally limited and does not claim to
identify every form of personal information.

## Agent Authorization

Each specialist agent has an explicit skill allowlist.

Business Agent:
- 4 authorized skills

Operations Agent:
- 5 authorized skills

Customer Agent:
- 6 authorized skills

Risk Agent:
- 4 authorized skills

Unauthorized skill execution raises a PermissionError before the capability
is executed.

## Evidence Grounding

Quantitative claims in generated answers are validated against trusted
specialist evidence.

The grounding layer:

- extracts business metrics from generated responses
- ignores dates, range labels, list numbering, and identifiers
- compares answer numbers against structured evidence
- rejects unsupported quantitative claims

Unsupported values raise a GroundingError before the response can be
delivered through the guarded workflow.

## Output Validation

Generated responses are checked for:

- empty output
- excessive output length
- system/developer prompt references
- hidden-instruction references
- internal implementation leakage
- LangGraph/internal routing disclosure

Responses that violate output policy are rejected.

## Safe Error Handling

Internal errors are converted into safe user-facing responses.

The system avoids exposing:

- local file paths
- stack traces
- API keys
- tokens
- passwords
- secrets
- internal exception details

## Guardrail Audit

Security and validation events can be recorded in a privacy-conscious audit
log.

Audit metadata may contain:

- event type
- action
- risk level
- detected PII types
- authorization result
- grounding result
- error type

Raw attack prompts, customer PII, credentials, and other sensitive content
are not intentionally stored in guardrail audit events.

## Guarded Agent Entry Point

The production-facing agent workflow can run through a centralized guarded
entry point:

Input Guardrails
→ LangGraph Agent Workflow
→ Evidence
→ Output Guardrails
→ Safe Response

Prompt-injection attempts are blocked before reaching the router or
specialist agents.

## Human Oversight

RetailOps AI remains a decision-support system.

Guardrails reduce risk but do not guarantee that every unsafe, inaccurate,
or adversarial input will be detected.

Consequential business actions remain subject to human review.

## Testing

Phase 9 added 71 automated guardrail and adversarial tests.

Full project regression suite:

- 198 tests passed
- 0 failures

Guardrail test coverage includes:

- input validation
- prompt injection
- PII
- authorization
- numeric grounding
- output validation
- centralized policy
- end-to-end adversarial behavior