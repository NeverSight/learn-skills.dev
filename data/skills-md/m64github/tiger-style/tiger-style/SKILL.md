---
name: tiger-style
description: TigerBeetle coding style for safety-critical Zig code. Use for writing new code aligned with TigerStyle, or analyzing existing code to produce structured reports showing aligned patterns, violations, and gray areas.
argument-hint: "[analyze <file> | check]"
---

# TigerStyle Skill

Coding style from TigerBeetle optimized for **Safety > Performance > DX**.

## Usage Modes

| Invocation | Mode | Output |
|------------|------|--------|
| `/tiger-style` | Writing | Guidance for writing new code |
| `/tiger-style analyze <file>` | Analysis | Complete report: Aligned + Violations + Gray Areas |
| `/tiger-style check` | Quick check | Violations only (brief) |

## Mode Instructions

### Writing Mode (`/tiger-style`)

When invoked without arguments, activate TigerStyle for all code you write or modify in this session:

1. Read [SAFETY.md](SAFETY.md), [PERFORMANCE.md](PERFORMANCE.md), and [DX.md](DX.md) to load the full rule set.
2. Apply all rules as you write Zig code. Every function you produce must have 2+ assertions (preconditions, postconditions, or invariants).
3. Before presenting code to the user, validate it against [CHECKLIST.md](CHECKLIST.md).
4. If a rule would be violated, fix it before showing the code. If a gray area arises, flag it to the user.

### Analyze Mode (`/tiger-style analyze <file>`)

When invoked with `analyze` and a file path:

1. Read the file specified in `$ARGUMENTS` (the path after `analyze`).
2. Read [SAFETY.md](SAFETY.md), [PERFORMANCE.md](PERFORMANCE.md), and [DX.md](DX.md) for the complete rule set.
3. Produce a structured report following the template in [REPORT_FORMAT.md](REPORT_FORMAT.md).
4. Check every rule against the file. Be thorough - scan for all violation types, not just obvious ones.
5. Group aligned patterns by category. Group violations by severity. Note gray areas with reasoning.

### Check Mode (`/tiger-style check`)

When invoked with `check`:

1. Scan the current file, staged changes, or recently modified Zig files.
2. Report only violations, grouped by severity (CRITICAL first, then MAJOR, then MINOR).
3. Skip aligned patterns and gray areas - keep output brief.
4. Use the format: `SEVERITY | location | rule | issue` (one line per violation).

## Workflow

After analysis or check, guide the user through fixing:

1. Fix CRITICAL violations first - these are safety risks.
2. Fix MAJOR violations - these affect maintainability.
3. MINOR violations are worth fixing but should not block progress.
4. Run `/tiger-style check` to verify fixes.
5. Repeat until clean.

## Quick Lookup

| Topic | See | Key Rules |
|-------|-----|-----------|
| Assertions | [SAFETY.md](SAFETY.md) | Min 2 per function, pair assertions, split compound |
| Control flow | [SAFETY.md](SAFETY.md) | No recursion, split compound conditions, every if has else |
| Memory | [SAFETY.md](SAFETY.md) | Static only, no dynamic after init |
| Function size | [SAFETY.md](SAFETY.md) | Max 70 lines |
| Types | [SAFETY.md](SAFETY.md) | Explicit sizes (u32 not usize) |
| Performance | [PERFORMANCE.md](PERFORMANCE.md) | Design-time thinking, batching, buffer bleeds |
| Resources | [PERFORMANCE.md](PERFORMANCE.md) | Network > disk > memory > CPU |
| Naming | [DX.md](DX.md) | snake_case, units last, semantic richness |
| Formatting | [DX.md](DX.md) | 80 cols, 4-space indent, braces on ifs |
| Bug prevention | [DX.md](DX.md) | Off-by-one, explicit division, options structs |
| Pre-submit | [CHECKLIST.md](CHECKLIST.md) | Quick validation checklist |
| Report format | [REPORT_FORMAT.md](REPORT_FORMAT.md) | Analysis output template |

## Our Customizations (vs pure TigerStyle)

| Rule | TigerStyle | Our Standard |
|------|------------|--------------|
| Line length | 100 columns | **80 columns** |
| Assertions | 2+ per function | Same |
| Memory in structs | Never store allocator | Same + never store Io |

## Severity Definitions

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Safety risk: missing assertions, unbounded loops, dynamic memory, ignored errors, missing else branches |
| **MAJOR** | Maintainability: function too long, complex control flow, usize instead of explicit type |
| **MINOR** | Style: naming, formatting, comments |
