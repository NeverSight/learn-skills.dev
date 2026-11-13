---
name: kode-thai
description: Run an iterative audit-and-fix loop on Thai prose using the kien-thai skill — repeats audit/fix passes until a full pass produces zero new edits. TRIGGER when user invokes `/kode-thai`, asks for "audit loop" / "วน audit" / "ตรวจวนๆ" / "ขัดภาษาไทยให้สุด" on Thai writing, says variants of "แก้ไปเรื่อยๆ จนกว่าจะไม่เจอที่ผิด", or explicitly requests repeated review passes on Thai prose. DO NOT TRIGGER for single-pass rewrites or one-off Thai edits (use kien-thai directly), or for non-Thai content.
---

# kode-thai

โคตรไทย — invoke kien-thai in a loop until the prose stops changing.

## Why this exists

Single-pass review misses issues that only surface after earlier fixes shift
sentence shape. A connective collapses, the next sentence's framing changes, a
new awkward seam appears. Loop until clean.

## Protocol

1. Load `kien-thai` in full — `SKILL.md` plus all eight references
   (`ai-tells.md`, `craft.md`, `grammar.md`, `style-rules.md`, `register.md`,
   `examples.md`, `exemplars.md`, `forbidden-phrases.md`). Don't skip
   references. Both audit and fix passes need depth — this is a deep
   language-analysis job, not mechanical scanning. (The pytest harness injects
   a leaner audit-mode bundle instead — register-scoped, draft-workflow
   sections stripped; see the project CLAUDE.md "Two-tier injection". "In
   full" governs interactive runs.)

2. Read the target file end-to-end before editing anything. Skim-and-fix
   produces shallow passes.

3. Audit pass. Deep-read end-to-end first, then list every issue. Cite each
   issue with the rule's slug (e.g. `f4/targhak-closure`, `wrong-classifier`,
   `f6/ko-resumptive`) and quote the offending text inline. As a pre-check,
   scan `forbidden-phrases.md` against the prose — un-backticked occurrences
   only (use/mention exemption). If everything passes, output a single line
   `CLEAN` — no prose, no commentary.

4. Fix pass. Apply the listed edits.

5. Re-read the edited file end-to-end. Diff-level review misses paragraph-flow
   problems that only show on full re-read.

6. Repeat steps 3–5 until one audit pass produces zero new issues.

7. Stop only on a clean pass — not on "good enough", not on "running out of
   obvious things". If you think it's done, run one more audit pass to confirm.

## Stop condition

The loop ends when an audit pass surfaces zero edits. A pass that finds one
issue and fixes it doesn't end the loop — the next pass might surface a new
issue caused by that fix. Only a fully clean pass terminates.

## Token cost

Each pass reloads kien-thai (~tens of thousands of tokens of skill +
references) plus the full target file. For long prose this compounds fast.
Warn the user before starting on files over ~1000 words so they can decide
whether to scope the loop to a section.

## Best input: a Thai-native model draft

This loop audits any Thai prose, but its highest-value use is over a draft from
a Thai-native model (Typhoon and peers), not Claude/Codex output. See
kien-thai's "Best output" section and `skills/kien-thai/scripts/`: run
`thai-route.sh` to produce the draft, then run this loop on it. The route
script handles drafting and fallback; this loop is the audit half — the part
that is language judgment, not a scriptable transform.

## Relationship to kien-thai

`kien-thai` is the rule set. `kode-thai` is the loop. `kode-thai` doesn't add
new rules — it enforces that kien-thai's rules get applied to convergence. If
the audit surfaces a pattern no kien-thai rule covers, follow the iteration
discipline in the project `CLAUDE.md` ("Iteration discipline — READ FIRST"):
trace the gap before adding a rule, don't synthesize on vibes.
