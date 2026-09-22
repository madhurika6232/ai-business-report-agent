# RetailOps AI — Agent Architecture

## Overview

RetailOps AI uses a multi-agent architecture orchestrated with LangGraph.

The system routes business questions to specialized agents, executes trusted
analytics and ML tools, collects structured evidence, and uses Groq to
synthesize a grounded user-facing response.

## Architecture

User Question
→ Router
→ Specialist Agent(s)
→ Deterministic Tools / ML / Review Intelligence
→ Evidence Collection
→ Grounded Synthesis
→ Final Answer

## Specialist Agents

### Business Agent

Handles:

- revenue
- orders
- average order value
- monthly performance
- product categories
- geographic performance

### Operations Agent

Handles:

- delivery performance
- late deliveries
- seller performance
- cancellations
- freight

### Customer Experience Agent

Handles:

- review scores
- satisfaction trends
- complaint themes
- delivery impact on satisfaction
- review intelligence
- operational complaint evidence

### Risk Agent

Handles:

- anomaly detection
- forecasting
- delivery-risk screening

## Router

Groq determines which specialist agents are required.

The router supports both single-agent and multi-agent questions.

Example:

"Which sellers have the worst delivery performance?"
→ Operations

"Why did customer satisfaction decline when delivery performance got worse?"
→ Customer + Operations

"Did unusual delivery patterns coincide with lower customer satisfaction?"
→ Risk + Operations + Customer

## LangGraph Workflow

The orchestration graph follows:

START
→ Router
→ Specialist Execution
→ Conditional Error Check
→ Synthesis OR Error Response
→ END

Specialist failures are captured rather than crashing the workflow.

## Grounding

Specialist agents do not independently invent business conclusions.

They retrieve structured evidence from trusted tools.

Groq receives this evidence during final synthesis and is instructed to:

- use only supplied facts
- preserve quantitative values
- avoid unsupported causal claims
- acknowledge uncertainty
- avoid invented root causes
- provide evidence-supported recommendations

Numeric evidence is rounded by deterministic Python before synthesis.

## Agent Evaluations

### Router Evaluation

Final routing golden set:

- 20 scenarios
- Exact route accuracy: 100%
- Macro precision: 100%
- Macro recall: 100%
- Macro F1: 100%
- Failure rate: 0%

These results apply to the current small development evaluation set and are
not production guarantees.

### Tool Selection

12 specialist tool-selection scenarios:

- Exact tool-selection accuracy: 100%
- Failure rate: 0%

### Multi-Agent Evaluation

5 multi-agent scenarios:

- Routing accuracy: 100%
- Execution accuracy: 100%
- Answer generation rate: 100%
- Error-free rate: 100%

### Numeric Faithfulness

5 end-to-end grounding scenarios were evaluated.

All quantitative values appearing in the evaluated final answers were
traceable to specialist evidence:

- Numeric faithfulness: 100%

The evaluator explicitly ignores formatting artifacts such as:

- numbered lists
- dates
- delay-range labels
- anonymized identifiers

## Guardrails

The agent system includes safeguards for:

- unsupported agent names
- empty queries
- specialist failures
- partial multi-agent failures
- safe error responses
- prompt injection in retrieved/customer content
- unsupported numerical claims
- unsupported causal claims

## Limitations

Evaluation sets are intentionally small development benchmarks.

A 100% score on these sets does not imply perfect generalization to arbitrary
user questions.

Routing, grounding, tool selection, and answer quality should continue to be
evaluated as new scenarios are introduced.

## Human Oversight

RetailOps AI is a decision-support system.

The intended workflow is:

User Question
→ AI Routing
→ Trusted Analytics / ML
→ Evidence-Grounded AI Interpretation
→ Human Review
→ Business Action