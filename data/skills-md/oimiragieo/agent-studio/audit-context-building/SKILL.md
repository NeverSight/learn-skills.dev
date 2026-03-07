---
name: audit-context-building
description: Ultra-granular code analysis for deep architectural context building. Line-by-line and block-by-block analysis using First Principles, 5 Whys, 5 Hows methodology at micro scale. Builds mental models, tracks invariants and assumptions, and maps cross-function call flows for security audit preparation.
version: 1.2.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Glob, Grep, Bash, Write]
args: '<target-path> [--depth deep|standard] [--focus security|architecture|correctness]'
best_practices:
  - Always read code line-by-line before forming any conclusions
  - Track every assumption and invariant explicitly in notes
  - Build mental models incrementally from concrete code, never from abstractions
  - Map cross-function call flows completely before analyzing individual functions
  - Document what the code ACTUALLY does, not what comments say it does
error_handling: graceful
streaming: supported
agents: [security-architect, code-reviewer, developer]
verified: true
lastVerifiedAt: 2026-03-01T00:00:00.000Z
---

# Audit Context Building Skill

<!-- Agent: evolution-orchestrator | Task: #2 | Session: 2026-02-21 -->
<!-- License: CC-BY-SA-4.0 | Source: Trail of Bits (github.com/trailofbits/skills) -->
<!-- Attribution: Adapted from Trail of Bits audit-context-building skill -->

<identity>
Ultra-granular code analysis skill adapted from Trail of Bits audit methodology. Builds deep architectural context through systematic line-by-line analysis using First Principles, 5 Whys, and 5 Hows at micro scale. Designed for security audit preparation, architectural understanding, and correctness verification.
</identity>

<capabilities>
- Line-by-line and block-by-block code analysis
- First Principles reasoning at code-level granularity
- 5 Whys root cause analysis at micro scale
- 5 Hows implementation verification at micro scale
- Mental model building from concrete code paths
- Invariant and assumption tracking across functions
- Cross-function call flow mapping and analysis
- State transition identification and verification
- Trust boundary identification and classification
- Data flow tracking through function boundaries
- Anti-hallucination enforcement: conclusions from code only
</capabilities>

## Overview

This skill implements Trail of Bits' audit context building methodology for the agent-studio framework. The core principle is: **never form conclusions about code without reading it line by line first**. This skill systematically builds understanding from the ground up, tracking every assumption, invariant, and data flow explicitly.

**Source repository**: `https://github.com/trailofbits/skills`
**License**: CC-BY-SA-4.0
**Methodology**: First Principles + 5 Whys + 5 Hows at micro scale

## When to Use

- Before security audits to build deep codebase understanding
- When analyzing unfamiliar codebases for architectural review
- When debugging complex cross-function interactions
- When verifying correctness of critical code paths (auth, crypto, state machines)
- When preparing for threat modeling with concrete code evidence
- When onboarding to a new codebase section that handles sensitive operations

## Iron Laws

1. **NEVER form conclusions without line-by-line evidence** — every claim about code behavior MUST be backed by specific line references; if you have not read the code, you do not know what it does.
2. **NEVER trust comments over actual code** — comments describe intent, code describes behavior; when they conflict, the code is authoritative; always verify what comments claim.
3. **NEVER skip error handling paths** — error paths frequently contain security-relevant behavior (fallback auth, leaked stack traces, privilege bypass) that is invisible to happy-path analysis.
4. **ALWAYS map cross-function call flows before analyzing individual functions** — isolated function analysis misses inter-function trust assumptions; understand the full call chain first.
5. **ALWAYS record unverified assumptions explicitly** — an unverified assumption is an unexamined risk; mark every assumption with `[UNVERIFIED]` and track it until confirmed or disproven.

## Anti-Hallucination Rules

1. **Never assume** what a function does based on its name alone
2. **Never trust** comments over actual code behavior
3. **Never skip** error handling paths -- they often contain security-relevant behavior
4. **Never extrapolate** behavior from one code path to another without verification
5. **Always note** when you have NOT read a dependency and mark assumptions as unverified

## Phase 1: Initial Reconnaissance

**Goal**: Map the surface area before diving deep.

### Steps

1. **Enumerate entry points**: Find all public APIs, CLI commands, HTTP handlers, event listeners
2. **Map the module graph**: Identify imports, exports, and dependency relationships
3. **Identify trust boundaries**: Where does external input enter? Where do privilege changes occur?
4. **Catalog data stores**: Databases, files, caches, environment variables, secrets

### Output Format

```markdown
## Reconnaissance Report

### Entry Points

- [ ] `path/to/file.ts:42` - HTTP handler `POST /api/login`
- [ ] `path/to/file.ts:89` - HTTP handler `GET /api/users/:id`

### Trust Boundaries

- [ ] External input at: [list locations]
- [ ] Privilege escalation at: [list locations]
- [ ] Serialization/deserialization at: [list locations]

### Data Stores

- [ ] Database: [type, access patterns]
- [ ] File system: [paths, permissions]
- [ ] Environment: [variables accessed]
```

## Phase 2: Deep Analysis (Line-by-Line)

**Goal**: Build precise mental model of each critical code path.

### The Analysis Loop

For each function/method under analysis:

1. **Read every line**. No skipping.
2. **For each line, ask**:
   - What state does this line depend on?
   - What state does this line modify?
   - What can go wrong here? (error paths)
   - What assumptions does this line make about its inputs?
   - Is the assumption validated upstream?
3. **Track in a structured note**:

```markdown
### Function: `authenticateUser(req, res)` at `src/auth.ts:45-92`

#### Line-by-Line Notes

- L45-48: Extracts `email` and `password` from `req.body`. **Assumption**: body is parsed JSON. **Verified**: Yes, middleware at `app.ts:12`.
- L50: Queries DB for user by email. **Assumption**: email is sanitized. **Verified**: No -- raw string interpolation. **FINDING: SQL injection risk**.
- L55-60: Compares password hash. Uses `bcrypt.compare()`. **OK**: timing-safe comparison.
- L62: Creates JWT token. **Assumption**: secret is strong. **Unverified**: need to check env config.

#### Invariants

- User must exist in DB before authentication succeeds
- Password comparison is timing-safe (bcrypt)
- JWT secret strength is unverified

#### Assumptions (Unverified)

- [ ] Email input is sanitized before DB query
- [ ] JWT secret is cryptographically random
- [ ] Session duration is bounded

#### Call Flow

authenticateUser() → findUserByEmail() → bcrypt.compare() → jwt.sign()
```

## Phase 3: Cross-Function Flow Analysis

**Goal**: Trace data and control flow across function boundaries.

### Steps

1. **Select a critical data flow** (e.g., user input to database query)
2. **Trace forward**: Follow the data from entry point through every transformation
3. **At each boundary**, document:
   - What validation occurs?
   - What transformation occurs?
   - Is the data type preserved or changed?
   - Are there implicit type coercions?
4. **Build the flow diagram**:

```markdown
### Flow: User Login Input to Database

1. `req.body` (raw JSON) → Express body parser
2. `{ email, password }` (destructured) → `authenticateUser()`
3. `email` (string, UNVALIDATED) → `findUserByEmail(email)` ← RISK
4. `email` → SQL query template literal ← FINDING: injection
5. Result → `user` object (or null)
6. `password` + `user.passwordHash` → `bcrypt.compare()` ← OK
```

## Phase 4: 5 Whys at Micro Scale

Apply 5 Whys to each finding or anomaly discovered:

```markdown
### Finding: SQL injection in findUserByEmail

1. **Why** is there SQL injection? → Email is concatenated into query string
2. **Why** is it concatenated? → Developer used template literals instead of parameterized queries
3. **Why** no parameterized query? → The ORM wrapper doesn't enforce parameterization
4. **Why** no input validation? → No validation middleware for this route
5. **Why** no middleware? → Route was added without security review
```

## Phase 5: 5 Hows at Micro Scale

Apply 5 Hows to verify implementation correctness:

```markdown
### Verification: JWT Token Generation

1. **How** is the token created? → `jwt.sign(payload, secret, options)`
2. **How** is the secret managed? → `process.env.JWT_SECRET`
3. **How** is the secret rotated? → No rotation mechanism found
4. **How** is token expiry enforced? → `expiresIn: '24h'` in options
5. **How** is token revocation handled? → No revocation mechanism found
```

## Output: Context Report

The final output is a structured context report:

```markdown
# Audit Context Report: [Component Name]

## Summary

- Files analyzed: N
- Functions analyzed: N
- Findings: N (Critical: X, High: Y, Medium: Z)
- Unverified assumptions: N

## Mental Model

[High-level description of how the component works, backed by line references]

## Findings

[Each finding with line references, 5 Whys analysis, severity]

## Invariants

[All tracked invariants with verification status]

## Unverified Assumptions

[All assumptions that require further investigation]

## Call Flow Maps

[All traced data/control flows]

## Recommendations

[Prioritized list of actions based on findings]
```

## Integration with Agent-Studio

### Recommended Workflow

1. Invoke `audit-context-building` skill first for deep analysis
2. Feed findings into `security-architect` for threat modeling
3. Use `variant-analysis` skill to find similar patterns
4. Use `static-analysis` skill for automated confirmation

### Complementary Skills

| Skill                 | Relationship                                   |
| --------------------- | ---------------------------------------------- |
| `security-architect`  | Consumes context reports for threat modeling   |
| `variant-analysis`    | Finds pattern variants across codebase         |
| `static-analysis`     | Automated confirmation of manual findings      |
| `differential-review` | Reviews fixes for completeness                 |
| `code-analyzer`       | Provides complexity metrics for prioritization |

## Anti-Patterns

| Anti-Pattern                                  | Why It Fails                                                 | Correct Approach                                           |
| --------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| Skipping to conclusions from function names   | Names describe intent, not behavior; leads to false findings | Read the code line-by-line before forming conclusions      |
| Trusting comments without reading code        | Comments are often wrong, stale, or misleading               | Treat comments as hypotheses to verify against actual code |
| Skipping error paths in analysis              | Security bugs often live in error handlers, not happy paths  | Explicitly trace all error branches with equal rigor       |
| Analyzing functions before mapping call flows | Misses cross-function trust assumptions and data flow        | Map module/call graph in Phase 1 before deep analysis      |
| Leaving assumptions untracked                 | Unverified assumptions silently become false findings        | Mark every assumption [UNVERIFIED] until confirmed         |

## Memory Protocol

**Before starting**: Read existing audit context from `.claude/context/reports/backend/` for prior analysis of the same codebase area.

**During analysis**: Write incremental findings to context report file as you discover them. Do not wait until the end.

**After completion**: Record key findings and methodology notes to `.claude/context/memory/learnings.md` for future audit sessions.
