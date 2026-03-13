---
name: embedded-review
description: "Expert code review for embedded/firmware projects with dual-model cross-review (Claude + Codex via ACP). Detects memory safety, interrupt hazards, RTOS pitfalls, hardware interface bugs, and C/C++ anti-patterns."
---

# Embedded Code Review Expert

## Overview

Perform structured code review of embedded/firmware projects using **dual-model cross-review**: Claude Code and Codex independently review the same diff, then findings are cross-compared to catch blind spots that single-model review misses.

Target environments: bare-metal MCU, RTOS (FreeRTOS/Zephyr/ThreadX), Linux embedded, mixed C/C++ firmware.

## Trigger

Activate when user asks to review embedded/firmware code changes. Examples:
- "review firmware-pro2 的改动"
- "review the NFC changes"
- `/embedded-review ~/Documents/dec/firmware-pro2`
- `/embedded-review ~/Documents/dec/firmware-pro2 HEAD~5..HEAD`
- `/embedded-review <github-pr-url>`

## Severity Levels

| Level | Name | Description | Action |
|-------|------|-------------|--------|
| **P0** | Critical | Memory corruption, interrupt safety violation, security vulnerability, brick risk | Must block merge |
| **P1** | High | Race condition, resource leak, undefined behavior, RTOS misuse | Should fix before merge |
| **P2** | Medium | Code smell, portability issue, missing error handling, suboptimal pattern | Fix or create follow-up |
| **P3** | Low | Style, naming, documentation, minor suggestion | Optional improvement |

---

## Workflow

### Mode Selection

**Single-model mode** (default for small diffs ≤100 lines):
- One review pass using the current session's model
- Faster, lower cost
- Suitable for trivial changes, config tweaks, documentation

**Dual-model cross-review** (default for diffs >100 lines, or when explicitly requested):
- Claude Code + Codex review independently via ACP
- Cross-compare findings
- Higher quality, catches heterogeneous blind spots
- Use for: new features, architecture changes, critical paths (ISR, crypto, NFC, DMA)

User can override: "用双模型 review" or "quick review 就行"

---

### Phase 0: Preflight — Scope & Context

1. Run `scripts/prepare-diff.sh <repo_path> [diff_range]` to extract:
   - Repository info (branch, last commit)
   - Target identification (MCU, RTOS, compiler)
   - Diff stat and full diff content

2. Assess scope:
   - **No changes**: Inform user; offer to review staged changes or a commit range.
   - **Small diff (≤100 lines)**: Default to single-model review.
   - **Large diff (>500 lines)**: Summarize by file/module first, then review in batches by subsystem.
   - **Critical path touched** (ISR, DMA, crypto, NFC, boot): Always recommend dual-model.

3. Build review context package:
   ```
   REVIEW_CONTEXT = {
     repo_info: (branch, MCU, RTOS, compiler),
     diff: (full git diff text),
     references: (relevant checklist sections from references/),
     focus_areas: (user-specified or auto-detected critical paths)
   }
   ```

---

### Phase 1: Single-Model Review

For small diffs or when dual-model is not requested:

#### 1) Memory safety scan
- Load `references/memory-safety.md` for detailed checklist.
- Stack overflow, buffer overrun, alignment, DMA cache coherence, heap fragmentation
- Flag `sprintf`, `strcpy`, `gets`, `strcat` — suggest bounded alternatives

#### 2) Interrupt & concurrency correctness
- Load `references/interrupt-safety.md` for detailed checklist.
- Shared variable access, critical sections, ISR best practices, RTOS pitfalls
- Priority inversion, reentrancy, nested interrupt handling

#### 3) Hardware interface review
- Load `references/hardware-interface.md` for detailed checklist.
- Peripheral init ordering, register access, timing violations, pin conflicts
- Communication protocols: I2C/SPI/UART/NFC buffer management, timeout handling

#### 4) C/C++ language pitfalls
- Load `references/c-pitfalls.md` for detailed checklist.
- Undefined behavior, integer issues, compiler assumptions, linker issues
- Preprocessor hazards, portability, type safety

#### 5) Architecture & maintainability
- HAL/BSP layering, abstraction, coupling, testability
- Dead code, magic numbers, configuration management

#### 6) Security scan (embedded-specific)
- Secret storage, debug interfaces, firmware update integrity
- Side channels, fault injection, input validation, stack canaries

→ Skip to **Phase 3: Output** for single-model results.

---

### Phase 2: Dual-Model Cross-Review (ACP)

When dual-model review is triggered:

#### Step 1: Prepare review payloads

Build two independent review tasks from the same REVIEW_CONTEXT:

**Claude Code task:**
```
You are a senior embedded systems engineer reviewing firmware code changes.

[REVIEW_CONTEXT: repo info, diff, focus areas]

Review checklist (apply all that are relevant):
- Memory safety (references/memory-safety.md)
- Interrupt & concurrency (references/interrupt-safety.md)
- Hardware interfaces (references/hardware-interface.md)
- C/C++ pitfalls (references/c-pitfalls.md)
- Architecture & security

Output format: For each finding, provide:
[P0/P1/P2/P3] [file:line] Title
- Description
- Risk
- Suggested fix

Be thorough. Flag everything you find, even if uncertain — mark uncertain items with [?].
```

**Codex task:**
```
You are an independent code reviewer for embedded/firmware projects.
Your job is to find bugs, security issues, and correctness problems.

[REVIEW_CONTEXT: repo info, diff, focus areas]

Focus on:
1. Memory corruption risks (buffer overflow, use-after-free, stack overflow)
2. Concurrency bugs (race conditions, missing volatile, ISR safety)
3. Hardware interface errors (timing, register access, peripheral init)
4. Logic errors and edge cases
5. Security vulnerabilities

Output: List every issue found as:
[SEVERITY: critical/high/medium/low] [file:line] Issue title
- What's wrong
- What could happen
- How to fix

Do NOT skip low-severity items. Report everything.
```

#### Step 2: Spawn parallel ACP sessions

```
sessions_spawn(runtime="acp", agentId="claude-code", task=claude_task)
sessions_spawn(runtime="acp", agentId="codex", task=codex_task)
```

Both run simultaneously. Wait for both to complete.

#### Step 3: Cross-compare findings

After both complete, analyze results:

1. **Consensus findings** (both flagged same issue): HIGH CONFIDENCE — these are real bugs
2. **Claude-only findings**: Review for validity — may be false positive or genuine catch
3. **Codex-only findings**: Review for validity — heterogeneous perspective may catch Claude's blind spots
4. **Contradictions**: Flag for human judgment — one says it's fine, other says it's a bug

Map to unified severity levels (P0-P3).

---

### Phase 3: Output Format

```markdown
## Embedded Code Review Summary

**Target**: [MCU/Board] | [RTOS/Bare-metal] | [Compiler]
**Branch**: [branch name]
**Files reviewed**: X files, Y lines changed
**Review mode**: [Single-model / Dual-model (Claude Code + Codex)]
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]

---

## Findings

### 🔴 P0 - Critical (must block)
(none or list)

### 🟠 P1 - High (fix before merge)
1. **[file:line]** Brief title [🤝 consensus / 🔵 Claude-only / 🟢 Codex-only]
   - Description of issue
   - Risk: what can go wrong
   - Suggested fix

### 🟡 P2 - Medium (fix or follow-up)
...

### ⚪ P3 - Low (optional)
...

---

## Cross-Review Analysis (dual-model only)

| Metric | Count |
|--------|-------|
| 🤝 Consensus (both found) | X |
| 🔵 Claude-only | Y |
| 🟢 Codex-only | Z |
| ⚠️ Contradictions | W |

### Notable disagreements
(list any contradictions with both perspectives)

---

## Hardware/Timing Concerns
(register access, peripheral init, timing-sensitive code)

## Architecture Notes
(layering, testability, portability observations)
```

### Phase 4: Next Steps

```markdown
---
## Next Steps

Found X issues (P0: _, P1: _, P2: _, P3: _).

**How would you like to proceed?**
1. **Fix all** — implement all suggested fixes
2. **Fix P0/P1 only** — address critical and high priority
3. **Fix specific items** — tell me which issues to fix
4. **Re-review with dual-model** — run cross-review (if single-model was used)
5. **No changes** — review complete
```

**Important**: Do NOT implement changes until user explicitly confirms.

---

## Resources

### references/

| File | Purpose |
|------|---------|
| `memory-safety.md` | Buffer, stack, heap, DMA, alignment checklist |
| `interrupt-safety.md` | ISR, concurrency, RTOS, atomic operations checklist |
| `hardware-interface.md` | Peripherals, registers, timing, protocol checklist |
| `c-pitfalls.md` | UB, integer, compiler, preprocessor, portability checklist |

### scripts/

| File | Purpose |
|------|---------|
| `prepare-diff.sh` | Extract git diff and build review context |
