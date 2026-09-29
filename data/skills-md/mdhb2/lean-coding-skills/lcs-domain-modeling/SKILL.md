---
name: lcs-domain-modeling
description: "Use this skill to actively build and sharpen a project's domain model. Trigger on phrases like 'domain model', 'what do we call this', 'naming', 'glossary', 'ubiquitous language', 'CONTEXT.md', 'what does this term mean'. Challenges fuzzy language, invents edge-case scenarios, writes glossary/ADRs. Do NOT trigger for: code changes, bug fixes, task execution, or architecture review."
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Domain Modeling Skill

Shared Coding Contract: Refer to `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

**Purpose:** Actively build and sharpen a project's domain model. Challenge terms, invent edge-case scenarios, write glossary/ADRs the moment something crystallizes.

**Chain of Truth Level:** Standard

## OKF Frontmatter & Writing Safety

When creating artifacts, include YAML frontmatter following the schema in `../lcs-shared/contract.md`. Follow Artifact Writing Safety rules: generate content first, write one file, verify, stop on failure.

### Trigger

Activate when user wants to: define domain terms, clarify naming, build glossary, update CONTEXT.md, or resolve ambiguous language.

### Behavior Checklist

1. Read `.lcs/state.md` first. If continuing work, locate existing artifacts. Check project root for `CONTEXT.md` (if exists).

2. **Challenge against glossary:** When user uses a term that conflicts with `CONTEXT.md`, call it out immediately. Don't let terminology drift.

3. **Sharpen fuzzy language:** Propose precise canonical terms for overloaded words. "User" means different things in auth vs billing — nail it down.

4. **Cross-reference code:** Surface contradictions between user statements and actual codebase. "We use UUIDs" but the code uses auto-increment IDs → flag it.

5. **Update inline:** Update `CONTEXT.md` at project root immediately when a term is resolved. Don't batch updates.

6. **Offer ADRs sparingly:** Only create `docs/adr/XXXX-decision.md` if:
   - (1) Hard to reverse
   - (2) Surprising without context
   - (3) Results in a real trade-off

7. End with Handoff recommending `lcs-toprd` or returning to the previous skill.

### Output

- Updated `CONTEXT.md` at project root (if domain terms were resolved)
- Optional: `docs/adr/XXXX-decision.md` for significant decisions

> **Path Exception:** Domain artifacts live at the project root, shared across work items (documented exception in `../lcs-shared/contract.md`).

## Chain of Truth Report

### Level
Standard

### Sources Checked
- `.lcs/state.md`
- `CONTEXT.md` (if present)
- User statements / terminology in conversation

### Assumptions
- <label each [verified] or [unverified]>

### Actions Taken
- <Terms challenged, glossary entries added, ADRs created>

### Verification
- <CONTEXT.md exists / updated; manual review>

### Report
<1-3 sentence summary with confidence rating>

## Handoff

Next recommended skill: lcs-toprd
Next file to read: CONTEXT.md
Current phase: domain-modeling
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <summary>
Source of Truth Bundle: .lcs/state.md, CONTEXT.md
Must Preserve IDs: None
Unresolved IDs: None
Suggested next command: Buat PRD dari domain model

## Chain of Truth Level

Level: Standard

This skill follows the LCS Chain of Truth protocol at the declared level.
