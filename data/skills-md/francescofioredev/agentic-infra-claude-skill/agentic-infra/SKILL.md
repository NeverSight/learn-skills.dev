---
name: agentic-infra
description: >
  Knowledge base for designing, reviewing, and linting agentic AI infrastructure.
  Use when: (1) designing a new agentic system and need to choose patterns,
  (2) reviewing an existing agentic architecture ADR or design doc for gaps/risks,
  (3) applying the lint script to an ADR markdown file to get structured findings,
  (4) looking up a specific agentic pattern (prompt chaining, routing, parallelization,
  reflection, tool use, planning, multi-agent collaboration, memory management,
  learning/adaptation, MCP, goal setting, exception handling, HITL, RAG, A2A,
  resource optimization, reasoning techniques, guardrails, evaluation, prioritization,
  exploration/discovery, context compaction, plan-then-execute, sub-agent spawning,
  dual LLM, spectrum of control, agentic search, RLAIF, sandboxed authorization,
  LLM observability, reflection feedback loop).
  PDF-grounded patterns (21) cite page numbers; community patterns (10 individual + 139 via summaries)
  cite awesome-agentic-patterns sources.
---

# Agentic Infra Skill

## Quick Start

**Design use case**: "Help me design a customer support agent"
→ Consult `taxonomy.yaml` to identify relevant concerns → load the relevant `patterns/*.md` cards → use `templates/adr.md`

**Review use case**: "Review this agentic architecture ADR"
→ Run `scripts/lint_agentic_arch.py <adr.md>` → cross-reference findings against `checklists/review.md` → produce `templates/review-report.md`

## Taxonomy

See `taxonomy.yaml` for the full concern → patterns mapping across 11 concern areas:
`reliability`, `safety`, `memory`, `tool-use`, `orchestration`, `observability`, `eval`, `cost`, `ux-collaboration`, `feedback`, `context-management`

## Pattern Library — Level 1: PDF-Grounded (21 patterns)

All 21 patterns have full pattern cards in `patterns/`. Each card specifies:
- Intent, context, forces/tradeoffs
- Solution with code evidence
- Failure modes and instrumentation
- Related patterns and PDF page citations `(p. N)`

| # | Pattern | File |
|---|---------|------|
| 1 | Prompt Chaining | patterns/01-prompt-chaining.md |
| 2 | Routing | patterns/02-routing.md |
| 3 | Parallelization | patterns/03-parallelization.md |
| 4 | Reflection | patterns/04-reflection.md |
| 5 | Tool Use / Function Calling | patterns/05-tool-use.md |
| 6 | Planning | patterns/06-planning.md |
| 7 | Multi-Agent Collaboration | patterns/07-multi-agent-collaboration.md |
| 8 | Memory Management | patterns/08-memory-management.md |
| 9 | Learning & Adaptation | patterns/09-learning-adaptation.md |
| 10 | Model Context Protocol (MCP) | patterns/10-mcp.md |
| 11 | Goal Setting & Monitoring | patterns/11-goal-setting-monitoring.md |
| 12 | Exception Handling & Recovery | patterns/12-exception-handling-recovery.md |
| 13 | Human-in-the-Loop (HITL) | patterns/13-hitl.md |
| 14 | RAG | patterns/14-rag.md |
| 15 | A2A Inter-Agent Communication | patterns/15-a2a-communication.md |
| 16 | Resource-Aware Optimization | patterns/16-resource-aware-optimization.md |
| 17 | Reasoning Techniques | patterns/17-reasoning-techniques.md |
| 18 | Guardrails / Safety | patterns/18-guardrails-safety.md |
| 19 | Evaluation & Monitoring | patterns/19-evaluation-monitoring.md |
| 20 | Prioritization | patterns/20-prioritization.md |
| 21 | Exploration & Discovery | patterns/21-exploration-discovery.md |

## Pattern Library — Level 2: Community Pattern Cards (10 patterns)

Individual deep-dive cards for the most unique community patterns not covered by Level 1.
Each card follows the same structure as Level 1 cards; citations use `Source: awesome-agentic-patterns`.

| # | Pattern | Category | File |
|---|---------|----------|------|
| 22 | Context Window Auto-Compaction | Context & Memory | patterns/22-context-compaction.md |
| 23 | Plan-Then-Execute (Security Variant) | Orchestration & Control | patterns/23-plan-then-execute-secure.md |
| 24 | Sub-Agent Spawning | Orchestration & Control | patterns/24-sub-agent-spawning.md |
| 25 | Dual LLM Pattern | Orchestration & Control | patterns/25-dual-llm.md |
| 26 | Spectrum of Control / Blended Initiative | UX & Collaboration | patterns/26-spectrum-of-control.md |
| 27 | Agentic Search Over Tools | Tool Use & Environment | patterns/27-agentic-search.md |
| 28 | RLAIF (RL from AI Feedback) | Learning & Adaptation | patterns/28-rlaif.md |
| 29 | Sandboxed Tool Authorization | Security & Safety | patterns/29-sandboxed-authorization.md |
| 30 | LLM Observability | Reliability & Eval | patterns/30-llm-observability.md |
| 31 | Reflection Loop / Self-Critique | Feedback Loops | patterns/31-reflection-feedback-loop.md |

## Community Category Summaries (139 patterns across 8 categories)

Comprehensive summaries of the full awesome-agentic-patterns community library, organized by category.
Each summary file covers all patterns in its category with problem/solution descriptions.

| Category | Patterns | File |
|----------|----------|------|
| Context & Memory | 17 | patterns/community/context-memory.md |
| Feedback Loops | 13 | patterns/community/feedback-loops.md |
| Learning & Adaptation | 7 | patterns/community/learning-adaptation.md |
| Orchestration & Control | ~40 | patterns/community/orchestration-control.md |
| Reliability & Eval | 16 | patterns/community/reliability-eval.md |
| Security & Safety | 5 | patterns/community/security-safety.md |
| Tool Use & Environment | 24 | patterns/community/tool-use-environment.md |
| UX & Collaboration | 15 | patterns/community/ux-collaboration.md |

## Pattern Selection

When choosing patterns, load `references/pattern-selection-guide.md` for:
- **Symptom → pattern** lookup (e.g., "agent loops forever" → Pattern 11 + 31)
- **Use-case bundles** (customer support, coding agent, research, long-horizon, etc.)
- **Quick-reference table** of all 31 patterns with when-to-use and key constraints

## Review Workflow

1. Run lint script: `python3 scripts/lint_agentic_arch.py <path/to/adr.md>`
2. Inspect JSON findings (each finding includes: `severity`, `rule`, `pattern_ref`, `evidence_page`)
3. Walk `checklists/review.md` for any gaps not caught by lint — now covers 76 items across 10 areas including context management, sandboxed execution, and UX/autonomy
4. Fill in `templates/review-report.md` with findings

## Design Workflow

1. Identify system concerns from `taxonomy.yaml`
2. Load `references/pattern-selection-guide.md` to select patterns by symptom or use case
3. Load the specific pattern cards for those concerns
4. Choose patterns considering forces/tradeoffs in each card
5. Record decisions in `templates/adr.md`
6. Self-check against `checklists/review.md` before finalizing

## Examples

- Design (PDF patterns): `examples/design-example.md` — customer support agent using patterns 1–21
- Design (community patterns): `examples/community-design-example.md` — autonomous coding agent using patterns 22–31
- Review: `examples/review-example.md` — research pipeline with architectural gaps identified and remediated

## Evidence Policy

**PDF-grounded patterns (1–21):** Every rule cites a PDF page. Format: `(p. N)`. Never state a rule without citation.

**Community patterns (22–31 and community/ summaries):** Citations use `Source: awesome-agentic-patterns` with the category name. These patterns are grounded in community case studies, blog posts, and engineering references rather than the PDF.
