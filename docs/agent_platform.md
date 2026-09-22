# RetailOps AI — Agent Platform

## Overview

RetailOps AI extends its LangGraph multi-agent system with reusable Skills,
Model Context Protocol (MCP) integration, structured agent-to-agent
coordination, and conversational memory.

## Skills

RetailOps capabilities are exposed through a centralized Skill Registry.

The registry currently contains 19 skills across four domains:

- Business: 4
- Operations: 5
- Customer: 6
- Risk: 4

Each skill contains:

- name
- description
- domain
- executable handler

This allows capabilities to be discovered and executed without duplicating
the underlying analytics or ML implementations.

## MCP

RetailOps AI exposes selected capabilities through Model Context Protocol.

Implementation:

- MCP Python SDK 2.0
- local stdio transport
- MCPServer
- in-process MCP client integration testing

### Exposed MCP Tools

- business_summary
- delivery_summary
- cancellation_metrics
- complaint_themes
- delivery_anomalies
- delivery_risk
- forecast_method

### MCP Resources

- retailops://platform
- retailops://skills
- retailops://domains

The MCP integration was validated through a real MCP client rather than
direct Python function calls.

## Agent-to-Agent Coordination

Specialist communication uses structured Pydantic message contracts.

Supported message concepts include:

- sender
- recipient
- message type
- task
- context
- payload
- evidence
- success/failure state

The A2A coordination layer supports both single-agent and multi-agent
delegation.

Example:

Supervisor
→ Customer Agent
→ Operations Agent
→ Structured Agent Responses
→ Supervisor

Specialist failures are isolated and represented through structured error
responses.

## Conversational Memory

RetailOps AI maintains session-level conversation memory.

Each session can store:

- user turns
- assistant turns
- metadata
- previous query
- previously selected agents
- resolved conversational context

Contextual follow-up questions can be rewritten into standalone business
questions before routing.

Example:

User:
"How was revenue in March 2018?"

Follow-up:
"What about the previous month?"

Resolved query:
"What was revenue in February 2018?"

The resolved query is then passed through the normal LangGraph workflow.

## Memory Boundaries

Current memory is application-session memory stored in process.

It is not yet a durable long-term user profile or cross-device memory system.

Persistent storage can be introduced later without changing the
conversation-memory interface.

## Architecture

User
→ Conversation Memory
→ Context Resolution
→ LangGraph Router
→ Specialist Agents
→ Skills / MCP / Analytics / ML
→ A2A Coordination
→ Evidence
→ Grounded Synthesis
→ Response
→ Conversation Memory

## Testing

Phase 8 automated tests:

- Skills: 9
- MCP: 5
- A2A: 8
- Memory: 10

Full project regression suite:

- 127 tests passed
- 0 failures

## Limitations

The current MCP server is configured primarily for local development.

The A2A layer provides structured internal coordination and should not be
interpreted as a complete implementation of every external agent
interoperability protocol.

Conversation memory currently exists only for the lifetime of the running
application unless a persistent backing store is added.

## Human Oversight

Skills, MCP tools, agent delegation, and memory extend the system's ability
to retrieve and coordinate evidence.

They do not change the core principle that consequential business actions
remain subject to human review.