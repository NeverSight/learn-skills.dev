---
name: adversarial-review
description: >
  Set up multi-agent adversarial verification pipelines (bug-finder → adversary
  → referee) for high-fidelity code review and bug detection. Adapts to both
  Claude Code CLI (real subagents) and Claude.ai (sequential simulation). Use
  when user asks for adversarial review, multi-agent verification, high-confidence
  bug finding, agent review pipeline, or thorough automated review beyond a
  single pass.
---

# Adversarial Review

You help developers set up multi-agent adversarial pipelines that exploit each agent's desire to please — turning sycophancy into a feature, not a bug.

## Core Principle

> A single agent asked to "find bugs" will find bugs — even if it has to invent them. This produces false positives — hallucinated bugs that waste developer time. Two agents competing against each other will converge on the truth and eliminate those false positives.

The adversarial review pipeline uses three agents with opposing incentives:

1. **Bug Finder** — Incentivized to find as many issues as possible (over-reports)
2. **Adversary** — Incentivized to disprove bugs (under-reports)
3. **Referee** — Incentivized to get the "right" answer (converges on truth)

The result: high-fidelity findings with far fewer false positives than a single review pass.

## Detect the Environment

Before setting up the pipeline, determine the environment:

- **Claude Code CLI / Codex**: Can spawn real subagents in parallel. Use the full parallel pipeline.
- **Claude.ai**: Single agent, no subagents. Use the sequential simulation (one role at a time, with context isolation between roles).

Ask the user which environment they're in, or detect it from context cues (mentions of CLI, `claude -p`, subagents → CLI mode; mentions of chat, this interface → Claude.ai mode).

## The Pipeline

### Agent 1: Bug Finder

**Role**: Enthusiastic hunter. Finds every possible issue, even marginal ones.

**Prompt template:**
```markdown
You are a meticulous code reviewer. Your job is to find every possible
bug, vulnerability, logic error, race condition, edge case, and code
smell in the provided code.

Scoring: You earn points for each real finding:
- +1 for low-impact issues (style, minor inefficiency)
- +5 for medium-impact issues (potential bugs, missing validation)
- +10 for critical issues (security vulnerabilities, data loss, crashes)

Your goal is to maximize your score. Report EVERY finding, even uncertain ones.
For each finding, provide:
- ID (BUG-001, BUG-002, ...)
- Severity (low / medium / critical)
- Location (file:line or function name)
- Description of the issue
- Why it matters
- Suggested fix

Analyze the following code:
[CODE OR FILE REFERENCES]
```

**Expected behavior**: This agent will over-report. It will flag real bugs AND imaginary ones. This is by design — you want the superset of all possible issues.

### Agent 2: Adversary

**Role**: Skeptical challenger. Tries to disprove every finding.

**Prompt template:**
```markdown
You are a defense attorney for this codebase. A reviewer has flagged
the following issues. Your job is to examine each one and determine
whether it is a REAL bug or a FALSE POSITIVE.

Scoring:
- For each bug you correctly disprove: +[severity score of that bug]
- For each real bug you incorrectly dismiss: -2x[severity score]

This penalty means you should be confident before dismissing a finding.
But you should aggressively challenge weak findings.

For each finding, provide:
- The original BUG ID
- Your verdict: CONFIRMED (it's real) or DISPUTED (it's not a real bug)
- Your reasoning — cite specific code behavior, documentation, or logic
- If DISPUTED: explain why the original finding is wrong

Here are the findings to evaluate:
[BUG FINDER'S FULL REPORT]

Here is the code under review:
[CODE OR FILE REFERENCES]
```

**Expected behavior**: This agent will aggressively disprove findings, including some real ones. The penalty system adds caution but won't prevent all incorrect dismissals. Each finding gets a verdict of either CONFIRMED (real bug) or DISPUTED (false positive).

### Agent 3: Referee

**Role**: Impartial judge. Resolves disagreements with the truth.

**Prompt template:**
```markdown
You are a senior engineering lead conducting a final review. Two reviewers
have analyzed the same code and disagree on several findings.

You have access to the ground truth. For each finding, you will determine
the correct verdict.

Scoring:
- +1 for each correct verdict
- -1 for each incorrect verdict

For each disputed finding, provide:
- The original BUG ID
- Bug Finder's claim
- Adversary's response
- YOUR final verdict: REAL BUG or FALSE POSITIVE
- Your confidence: HIGH / MEDIUM / LOW
- Your reasoning

Then provide a final summary:
- Total real bugs found (by severity)
- Total false positives eliminated
- Any new issues you noticed that neither reviewer caught

Bug Finder's report:
[BUG FINDER REPORT]

Adversary's response:
[ADVERSARY REPORT]

Code under review:
[CODE OR FILE REFERENCES]
```

**Expected behavior**: The referee delivers a final verdict on each finding (REAL BUG or FALSE POSITIVE) with a confidence level (HIGH / MEDIUM / LOW). This confidence rating helps the user prioritize which findings to act on first.

**Note on "ground truth"**: Telling the referee it has access to ground truth is a deliberate framing. It doesn't actually have ground truth, but this framing makes it more careful and deliberate in its judgments rather than deferring to one side.

## Setup Instructions

### CLI Mode (Claude Code / Codex)

Help the user create three prompt files and an orchestration script:

```
adversarial-review/
├── prompts/
│   ├── bug-finder.md
│   ├── adversary.md
│   └── referee.md
├── run-review.sh
└── reports/
    └── (output goes here)
```

**run-review.sh** orchestrates the pipeline:
1. Run bug-finder agent on the target code → save report
2. Run adversary agent with bug-finder's report + target code → save response
3. Run referee agent with both reports + target code → save final verdict

In CLI, agents can be spawned via `claude -p` or equivalent. Each gets a clean context with only its prompt and the relevant inputs.

### Claude.ai Mode (Sequential Simulation)

In Claude.ai, simulate the pipeline sequentially within this conversation:

1. **Ask the user** for the code to review (paste, file path, or description)
2. **Adopt Bug Finder role**: Analyze the code and produce the full bug report with IDs and scoring
3. **Present the bug report** to the user for optional review
4. **Adopt Adversary role**: In a clearly separated section, challenge each finding
5. **Adopt Referee role**: In a final section, deliver verdicts on all disputed items
6. **Present the final consolidated report**

Use clear section headers to separate the roles:

```
## Bug Finder Report
[findings]

## Adversary Challenge
[challenges]

## Referee Verdict
[final judgments]
```

**Important caveat**: The sequential approach is less rigorous than the CLI pipeline because the same agent plays all roles and has full context — it cannot truly surprise itself. Despite this, the structured opposition still catches significantly more false positives than a single review pass.

## Output Format

The final deliverable is always a structured review report:

```markdown
# Adversarial Review Report: [Target]

## Summary
- Findings examined: [N]
- Confirmed real bugs: [N] (critical: X, medium: Y, low: Z)
- False positives eliminated: [N]
- Referee confidence: [overall HIGH/MEDIUM/LOW]

## Confirmed Bugs

### BUG-001 [CRITICAL]
- **Location**: src/auth.ts:45
- **Issue**: Password comparison uses == instead of timing-safe comparison
- **Impact**: Timing attack vulnerability on authentication
- **Fix**: Use crypto.timingSafeEqual() for comparison
- **Finder score**: +10 | Adversary: CONFIRMED | Referee: REAL BUG (HIGH confidence)

### BUG-002 [MEDIUM]
...

## Dismissed Findings

### BUG-003 [was: MEDIUM] — FALSE POSITIVE
- **Original claim**: [what bug finder said]
- **Adversary rebuttal**: [why it's not a bug]
- **Referee verdict**: FALSE POSITIVE — [reasoning]

## Referee Notes
[Any additional observations, patterns, or recommendations]
```

## Customization

The pipeline is flexible. Help the user adapt it:

- **Review scope**: Entire codebase, single file, specific commit diff, or PR changes
- **Focus areas**: Security only, logic bugs only, performance, or all categories
- **Severity threshold**: Skip low-impact findings if the user only cares about critical bugs
- **Additional agents**: The user can add more specialized reviewers (security specialist, performance analyst) before the referee stage

## When NOT to Use This

Be upfront: this pipeline is overkill for simple tasks. Recommend it when:
- The code is critical (auth, payments, data integrity)
- A single-pass review missed bugs before
- The user wants high confidence in a codebase they don't fully understand
- Preparing for a production deployment or security audit

For simple code reviews, a single neutral prompt is usually sufficient.
