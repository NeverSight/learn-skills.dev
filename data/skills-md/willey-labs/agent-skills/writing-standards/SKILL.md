---
name: writing-standards
description: >
  Standards for writing, editing, and reviewing DOCUMENTS — READMEs, specs, rules, skills,
  design docs, guides, and any prose deliverable produced from a source (existing code, or a
  prior discussion). Two rule sets apply on every document task: (1) source-to-deliverable —
  code→doc describes what the system DOES with no code or code-identifiers; discussion→rule
  states the general principle, not the specific example just discussed; (2) anti-slop —
  cut hedging, hype words, throat-clearing, cheerleading, reflexive formatting, and padding.
  Use when the user says "write a document", "document this code", "write up what this does",
  "turn this into a rule/skill", "make a doc from our discussion", "review this doc", or
  "is this slop?". Consult before authoring or reviewing ANY document, even when the user does
  not say "standards" — every document write/edit/review must comply. The companion to
  coding-standards: that one governs code, this one governs documents.
license: MIT
metadata:
  author: willey-labs
  version: "0.1.0"
---

# Writing Standards

Every document you write, edit, or review must comply with these rules. A *document* is any
prose deliverable: a README, a spec, a rule, a skill, a design doc, a guide, a review, release
notes. This skill does **not** govern normal conversation — only the deliverable.

The rules come in two sets, both applied on every document task:

- **`references/common/source-to-deliverable.md`** — how to turn a *source* (code you read, or a
  discussion you had) into a deliverable without dragging the source into the output.
- **`references/common/anti-slop.md`** — the patterns that make a document read as machine-padded
  filler, each with a rule code and a fix.

All paths in this document are relative to this SKILL.md file, so they resolve wherever the skill
is installed.

---

## Step 0 — Bootstrap the reminder hooks (once per session, only if needed)

The hooks inject a short reminder of these rules at session start and on every prompt, so the
rules don't get buried as a conversation grows. Run the fast read-only check first (single
absolute-path command, no `cd`/`&&`):

```bash
python3 <skill-dir>/bootstrap.py --verify
```

Exit 0 → hooks are wired; go to Step 1. Non-zero → wire them:

```bash
python3 <skill-dir>/bootstrap.py
```

It auto-detects scope (this project's `.claude/settings.json` vs global `~/.claude/settings.json`)
from where the skill is installed, and merges two entries — `SessionStart` and `UserPromptSubmit` —
without disturbing hooks you already have. Tell the user to **restart the session** so the hooks
activate; until then the reminder isn't injected, but this SKILL.md is still in force for any
document you write this session.

---

## Step 1 — Pick the document type (optional refinement)

`references/common/` applies to every document. If a per-type guide exists under
`references/<doc-type>/` (README, spec, review, …), read it too — it specializes the common rules
for that kind of document. If none matches, the common rules are the whole standard.

---

## Step 2 — Write, edit, or review against the rules

Read both common references, then produce the document. The two failures this skill exists to stop:

1. **Echoing the source.** You read code (or had a discussion) to understand something, then paste
   that source — the code, the function names, the one example you just discussed — into the
   deliverable. The source is what you learned from; it does not appear in the output. See
   `source-to-deliverable.md`.
2. **Slop.** Hedging, hype, throat-clearing, cheerleading, reflexive headers/bold/lists, and
   sentences that sound like content but carry none. See `anti-slop.md`.

When **reviewing** a document, report violations by rule code with the offending line and the fix —
the same way coding-standards reports a code review.
