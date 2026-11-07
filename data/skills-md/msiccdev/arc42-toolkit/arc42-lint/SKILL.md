---
name: arc42-lint
version: 1.0.1
description: Validates cross-section ID consistency in arc42 documentation that follows this toolkit's conventions. Checks toolkit IF-xx interface IDs (Section 3↔Section 5), building block deployment coverage (Section 5↔Section 7), Q42 quality tag traceability (Section 1↔Section 10), toolkit ADR risk references (Section 9↔Section 11), and aspirational scenario linkage (Section 10↔Section 11). Runs the automated linter script when available, or applies rules manually when not.
---

# arc42 Toolkit Convention Linter

You are an expert arc42 architect validating cross-section ID consistency in documentation that follows this toolkit's conventions.

This skill checks that identifiers defined in one section are correctly referenced in related sections when the documentation follows this toolkit's ID conventions. These checks are toolkit convention rules — not official arc42 requirements. It does not review content quality or completeness — use `arc42-review` for that.

**Five toolkit consistency rules:**

| Rule | Sections | What is checked |
|------|----------|-----------------|
| 1 | Section 3 ↔ Section 5 | Toolkit IF-xx interface IDs defined in Section 3 should appear in Section 5 Level-1, and vice versa |
| 2 | Section 5 ↔ Section 7 | Toolkit checks whether Section 5 building block names appear in the Section 7 deployment mapping |
| 3 | Section 1 ↔ Section 10 | Toolkit checks whether Q42 tags used in Section 10 quality scenarios appear in Section 1.2 quality goals |
| 4 | Section 9 ↔ Section 11 | Every toolkit RISK-xx in an ADR's "Risks created" field should have a Section 11 risk matrix entry |
| 5 | Section 10 ↔ Section 11 | Every toolkit aspirational scenario from Section 10.3 should be referenced in Section 11 |

---

## Step 1 — Locate the Documentation

**Do not start linting yet.** Ask the user:

1. **Where are the arc42 docs?** — What is the path to the documentation directory (e.g. `docs/`, `architecture/`, or a single monolithic file)?
2. **What language are the docs written in?** — Default is English (`en`). Built-in options: `de`, `fr`, `it`, `es`, `pt`. This affects how the linter recognises section headings and content patterns.
3. **Is `scripts/arc42-lint.py` present?** — Check whether the automated linter script exists in the project. If it does, prefer running it. If not, apply the rules manually.

If the user is unsure about the docs path, look for `.md` files in `docs/`, `architecture/`, `arc42/`, or the project root.

---

## Step 2 — Run or Simulate

Choose the path based on what is available:

### Path A — Automated script is present

Run the linter, passing the language the user confirmed in Step 1:

```bash
python scripts/arc42-lint.py <docs_path> --lang <lang> --format text
```

Capture the output. If the exit code is 0, all rules passed — proceed to Step 3 to present a clean report.

If there are errors or warnings, parse the output and continue to Step 3.

**Strict mode** (treat warnings as errors):
```bash
python scripts/arc42-lint.py <docs_path> --lang <lang> --format text --strict
```

---

### Path B — No script available (manual check)

Read the relevant documentation sections. Apply each rule in order. The phrases to look for in Rules 3, 4, and 5 depend on the documentation language — use the equivalents from `scripts/languages/<lang>.json` if the docs are not in English.

**Rule 1 — Section 3 ↔ Section 5 Interface IDs**
1. Read Section 3: collect every `IF-xx` from the interface table (first column)
2. Read Section 5 Level-1: collect every `IF-xx` from the Interfaces column of the building block table
3. Check both directions according to the toolkit convention: each IF-xx in Section 3 should appear in Section 5, and each IF-xx in Section 5 should appear in Section 3
4. Record any orphan IDs as toolkit convention deviations

**Rule 2 — Section 5 ↔ Section 7 Building Block Coverage**
1. Read Section 5: collect every component name (Name column of the building block table)
2. Read Section 7: search for each component name in the deployment view text and tables
3. Any component name absent from Section 7 is an error

**Rule 3 — Section 1 ↔ Section 10 Quality Tag Coverage**
1. Read Section 1.2: collect every Q42 tag (`#reliable`, `#efficient`, `#secure`, etc.) from the Quality Goal column
2. Read Section 10: collect the Q42 tag from every quality scenario's "Quality property" row
3. Any tag used in Section 10 that does not appear in Section 1.2 is an error

**Rule 4 — Section 9 ↔ Section 11 ADR Risk References**
1. Read Section 9: for each ADR, find the `Risks created (→ Section 11):` line in its Implications block; collect all `RISK-xx` IDs mentioned
2. Read Section 11: collect every `RISK-xx` from the risk matrix (ID column)
3. Any toolkit RISK-xx mentioned in Section 9 but absent from Section 11 is a toolkit convention deviation

**Rule 5 — Section 10.3 ↔ Section 11 Aspirational Scenarios** *(toolkit extension — Section 10.3 is not part of the official arc42 template)*
1. Read Section 10.3 (aspirational scenarios table): collect every `QS-xx` where Current State is "not measured"
2. Read Section 11: check that each aspirational QS-xx is referenced somewhere in the risks/debt section
3. Any aspirational QS-xx absent from Section 11 is a toolkit convention deviation

---

## Step 3 — Report Findings

Present results in this format:

```markdown
## arc42 Consistency Lint Report

**Docs path:** [path checked]
**Method:** Automated script / Manual check

---

### Rule Results

| Rule | Sections | Status | Details |
|------|----------|--------|---------|
| 1 | Section 3 ↔ Section 5  IF-xx | PASS / FAIL | [e.g. "IF-03 missing from Section 5"] |
| 2 | Section 5 ↔ Section 7  Building blocks | PASS / FAIL / SKIP | [detail or "Section 7 not found"] |
| 3 | Section 1 ↔ Section 10 Q42 tags | PASS / FAIL | [e.g. "#usable used in QS-04 but absent from Section 1.2"] |
| 4 | Section 9 ↔ Section 11 RISK-xx | PASS / FAIL | [e.g. "RISK-02 in ADR-003 missing from Section 11"] |
| 5 | Section 10 ↔ Section 11 Aspirational | PASS / FAIL / SKIP | [detail or "no aspirational scenarios found"] |

---

### Issues

**Errors (must fix — IDs are inconsistent):**
- [ ] [Rule N] [Section]: [Specific ID or name] — [what is missing and where]

**Warnings (advisory — a section was not found):**
- [ ] [Rule N]: [Which section is missing] — consistency cannot be fully verified

---

### Verdict

- [ ] **CLEAN** — All applicable rules pass
- [ ] **ISSUES FOUND** — N error(s), M warning(s) — see Issues above
```

---

## Step 4 — Offer to Fix

After presenting the report:

1. For each **error**: offer to fix it immediately — either by adding the missing ID to the correct section, or by running the relevant section skill (`/arc42-section-N`) to regenerate that section with the correct references.
2. For **warnings** about missing sections: offer to create the missing section using the relevant skill.
3. After fixes are applied, re-run the lint check (script or manual) and confirm the rule now passes.

Ask: **"Would you like me to fix these issues now?"**

---

*Based on [arc42.org](https://arc42.org), [docs.arc42.org](https://docs.arc42.org), [quality.arc42.org](https://quality.arc42.org)*
