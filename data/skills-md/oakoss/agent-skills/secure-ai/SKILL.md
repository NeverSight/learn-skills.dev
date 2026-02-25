---
name: secure-ai
description: 'Secures AI integrations against prompt injection, privilege escalation, and data leakage. Use when implementing defense-in-depth for LLM pipelines, applying zero-trust controls to autonomous agents, hardening server actions that interact with AI services, validating model outputs, securing MCP tool integrations, or auditing AI system access patterns and identity management. Use for OWASP LLM Top 10, prompt injection defense, agentic security, AI supply chain.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Secure AI

## Overview

Secures AI integration layers through multi-layered defense, structural isolation, and zero-trust orchestration. Covers prompt injection defense, model output validation, agentic security, secure server actions, supply chain integrity, MCP tool security, and audit protocols for applications that interact with LLMs.

Aligned with the OWASP Top 10 for LLM Applications 2025 and the NIST AI Risk Management Framework (AI RMF 1.0). Provides coverage for all ten OWASP LLM risks with concrete defense patterns.

**When to use:** Securing LLM-powered features against prompt injection, validating and sanitizing model outputs before downstream use, implementing zero-trust for autonomous agents, hardening server actions for AI endpoints, securing MCP tool integrations, managing AI supply chain risks, auditing AI access patterns.

**When NOT to use:** General web application security without AI components, frontend-only security concerns, non-AI API hardening, basic authentication or authorization without AI involvement.

## Quick Reference

| Pattern                | Approach                                        | Key Points                                                 |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------- |
| Structural isolation   | Separate system/user message roles              | Never mix instructions and user data in one string         |
| Input boundaries       | Delimit user data with markers                  | Helps models identify where untrusted data begins/ends     |
| Guardian model         | Pre-scan input with a fast classifier           | Detect injection patterns before main reasoning model      |
| Output validation      | Treat LLM output as untrusted input             | Context-aware encoding, parameterized queries, CSP headers |
| Least privilege        | Capability-based scopes per sub-task            | Agents get only the tools needed for current work          |
| Human-in-the-loop      | Require human sign-off for destructive actions  | Financial or data-altering events need approval            |
| Non-human identity     | OIDC-based agent authentication                 | Verifiable identity for every agent, rotate keys regularly |
| Server-only AI logic   | `server-only` imports for all AI code           | Keys and reasoning never leak to client bundle             |
| Input validation       | Zod schemas on all AI-facing server actions     | Never pass raw user input to AI services                   |
| Rate limiting          | Per-user/IP token budget via Redis              | Prevent denial-of-wallet attacks on AI endpoints           |
| Stream scrubbing       | Filter sensitive strings from AI output streams | Remove internal IDs, secrets before reaching client        |
| MCP tool security      | Allowlist tools, validate inputs/outputs        | Treat MCP servers as untrusted, enforce least privilege    |
| Supply chain integrity | Verify model provenance, maintain AI-BOM        | Track models, datasets, and dependencies with checksums    |
| Secret management      | Environment variables with CI leak scanning     | Use gitleaks in CI to prevent committed secrets            |

## Core Security Principles

1. **Isolation is absolute** -- user data must never be treated as system instruction
2. **LLM output is untrusted** -- treat all model responses as potentially malicious input before downstream use
3. **Least privilege for agents** -- grant only the tools needed for the current sub-task, revoke after completion
4. **Human verification of destruction** -- destructive or irreversible actions require a human signature
5. **No secrets in client** -- all AI logic and keys reside in server-only environments
6. **Adversarial mindset** -- assume both users and agents will attempt to bypass rules
7. **Defense in depth** -- layer defenses so that bypassing one layer does not compromise the system
8. **Supply chain verification** -- verify provenance and integrity of all models, datasets, and AI tools

## OWASP LLM Top 10 (2025) Coverage

| OWASP Risk                             | Reference                                                  |
| -------------------------------------- | ---------------------------------------------------------- |
| LLM01 Prompt Injection                 | Prompt Injection Defense                                   |
| LLM02 Sensitive Information Disclosure | Secure Server Actions (stream scrubbing, output filtering) |
| LLM03 Supply Chain                     | Supply Chain and MCP Security                              |
| LLM04 Data and Model Poisoning         | Supply Chain and MCP Security                              |
| LLM05 Improper Output Handling         | Output Validation and Encoding                             |
| LLM06 Excessive Agency                 | Agentic Zero-Trust Security (least privilege, HITL)        |
| LLM07 System Prompt Leakage            | Prompt Injection Defense (non-extractable prompts)         |
| LLM08 Vector and Embedding Weaknesses  | Output Validation and Encoding (RAG sanitization)          |
| LLM09 Misinformation                   | Output Validation and Encoding (semantic filtering)        |
| LLM10 Unbounded Consumption            | Secure Server Actions (rate limiting, token budgets)       |

## Common Mistakes

| Mistake                                                            | Correct Pattern                                                                                |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Mixing user input and system instructions in the same prompt field | Use structural isolation with separate system and user message roles                           |
| Trusting LLM output and passing it directly to exec, eval, or SQL  | Treat all model output as untrusted; use parameterized queries and context-aware encoding      |
| Giving agents unlimited tool access for all tasks                  | Apply capability-based scopes granting only tools needed per sub-task                          |
| Using static API keys for AI service authentication                | Use OIDC with dynamic key rotation and short-lived tokens                                      |
| Loading third-party models without provenance checks               | Verify model checksums, use signed artifacts, maintain AI-BOM                                  |
| Granting MCP servers broad permissions without validation          | Allowlist MCP tools, validate all inputs/outputs, enforce human approval for sensitive actions |
| Passing raw user input directly to AI services                     | Validate all input with Zod schemas before AI processing                                       |
| Streaming AI responses without output filtering                    | Scrub sensitive strings from streams before they reach the client                              |

## Key Frameworks

- **OWASP Top 10 for LLM Applications 2025** -- industry standard for LLM vulnerability classification
- **NIST AI Risk Management Framework (AI RMF 1.0)** -- four-function framework (Govern, Map, Measure, Manage) for AI risk
- **NIST Cybersecurity Framework Profile for AI (NISTIR 8596)** -- guidelines for secure AI adoption
- **OWASP MCP Security Cheat Sheet** -- practical guide for securing third-party MCP server integrations
- **CycloneDX 1.6 / SPDX 3.0** -- standards supporting AI Bill of Materials (ML-BOM)

## Delegation

- **Scan codebase for prompt injection vulnerabilities**: Use `Explore` agent to search for user data flowing into system prompts and unvalidated inputs
- **Implement zero-trust agent orchestration**: Use `Task` agent to add identity verification, sandboxing, and human approval gates
- **Audit model output handling**: Use `Explore` agent to find LLM outputs passed to exec, eval, SQL, or rendered as HTML without sanitization
- **Review MCP tool configurations**: Use `Explore` agent to check MCP server permissions, tool allowlists, and authentication setup
- **Design secure AI integration architecture**: Use `Plan` agent to map trust boundaries, agent scopes, and audit requirements
- **Assess supply chain risks**: Use `Explore` agent to inventory third-party models, datasets, and MCP servers with provenance records
- **Set up security monitoring**: Use `Task` agent to configure audit logging, anomaly detection, and incident response alerts

> For general application security (OWASP Top 10, auth patterns, security headers, input validation), use the `application-security` skill. For database-layer security (RLS policies, audit trails, Postgres hardening), use the `database-security` skill.

## References

- [Prompt Injection Defense](references/prompt-injection-defense.md) -- multi-layered isolation, guardian models, input boundaries, indirect injection
- [Output Validation and Encoding](references/output-validation.md) -- zero-trust output handling, context-aware encoding, RAG sanitization
- [Agentic Zero-Trust Security](references/agentic-security-zero-trust.md) -- non-human identity, resource isolation, anomaly detection
- [Secure Server Actions](references/secure-server-actions.md) -- server-only patterns, input validation, rate limiting, stream security
- [Supply Chain and MCP Security](references/supply-chain-mcp.md) -- model provenance, AI-BOM, MCP tool hardening, data poisoning defense
- [Security Audit Protocols](references/security-audit-protocols.md) -- monitoring agent behavior, compliance checklists, incident response
