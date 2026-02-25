---
name: neuro-symbolic-reasoning
description: Neuro-symbolic AI combining LLMs with symbolic solvers. Use when exploring neuro-symbolic approaches (ideation, no code) or implementing solver integrations (code).
---

# Neuro-Symbolic Reasoning

## Mode Detection

Detect user intent and route accordingly:

**→ Ideation**: "How should I...", "What are the tradeoffs...", "Design an experiment..."
- NO code, NO file creation
- See [references/ideation.md](references/ideation.md)

**→ Implementation**: "Implement...", "Build...", "Write code...", "Debug..."
- See [references/solvers.md](references/solvers.md) for code
- See [references/logic-llm.md](references/logic-llm.md) for format
- See [references/packages.md](references/packages.md) for setup

## File Creation Policy

**Small files, few files:**
- Create files (not inline code) but keep them small and focused
- Avoid scaffolding project structures unless asked
- Follow good coding practices: clear names, comments where needed

## Core Pipeline

```
NL Problem → LLM Formulator → Logic Program → Symbolic Solver → Answer
                    ↑                              |
                    └──── Self-Refinement ←────────┘
```

## Solver Selection

| Logic Type | Solver | Use When |
|------------|--------|----------|
| First-order logic | Prover9 | Expressive reasoning, theorem proving |
| Constraints/SAT | Z3 | Scheduling, planning, satisfiability |
| Rule-based | Pyke | Simple propositional rules |
