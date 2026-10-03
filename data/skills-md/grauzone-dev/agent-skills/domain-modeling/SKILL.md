---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
license: MIT
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Domain modeling

Actively build and sharpen the project's domain model as you design. This is the active discipline: challenge terms, test them against concrete scenarios and code, then record settled language and durable decisions.

## 1. Establish the document layout

When `docs/agents/domain.md` exists, load it before reading or changing domain documentation. It is the repository-specific layout contract.

Otherwise, load [CONTEXT-FORMAT.md](references/CONTEXT-FORMAT.md) to select the default context layout and the relevant `CONTEXT.md`. Load [ADR-FORMAT.md](references/ADR-FORMAT.md) when an architectural choice may need recording.

**Complete when:** the relevant context, domain-document layout, and ADR directory are identified.

## 2. Read the current model and evidence

Read the selected `CONTEXT.md`, ADRs that affect the topic, and the relevant code before proposing terminology or a decision. Treat the current glossary as the starting language, not a constraint that prevents correcting it.

**Complete when:** existing terminology, prior decisions, and code behavior relevant to the discussion are known or explicitly absent.

## 3. Sharpen the model

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, surface the conflict and ask which meaning is intended.

### Sharpen fuzzy language

When a term is vague or overloaded, propose a precise canonical term. Test domain relationships with concrete scenarios that force their boundaries to become explicit.

### Cross-reference with code

When the user states how something works, check whether the code agrees. Surface contradictions for resolution rather than silently preferring either source.

**Complete when:** every term or relationship settled in the discussion has one unambiguous meaning and any code contradiction is resolved or explicit.

## 4. Capture settled knowledge

When a term is resolved, update the selected `CONTEXT.md` immediately. Follow the repository-specific layout contract when `docs/agents/domain.md` exists; otherwise use [CONTEXT-FORMAT.md](references/CONTEXT-FORMAT.md) for the glossary format. Keep the glossary focused on context-specific language and its definitions.

When an architectural choice may be durable and non-obvious, load [ADR-FORMAT.md](references/ADR-FORMAT.md). It defines whether the choice qualifies, where it belongs, and how to record it.

**Complete when:** the selected context reflects every settled term, each qualifying architectural decision is recorded in its correct ADR directory, and unresolved terms remain explicit.

## Delivery evidence

Report the context and ADR directories used, terms added or changed, decisions captured, code evidence checked, and unresolved terminology or contradictions.
