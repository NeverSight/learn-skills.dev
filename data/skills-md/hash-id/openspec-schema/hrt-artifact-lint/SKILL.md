---
name: hrt-artifact-lint
description: "Runs the deterministic structural lint over a tempa-spec change's artifacts (hashtag counts, checkbox format, delta headers, capability<->spec-file correspondence, Covers: target existence, design.md section presence, unverified External Dependencies rows) so a language model does not do this by hand. Called from hrt-adversarial-authoring and hrt-align-consistency-review. Judgement checks stay with the reviewers."
---

# hrt-artifact-lint

Run the bundled `lint.cjs` (sits next to this file, installed at `.agents/skills/hrt-artifact-lint/lint.cjs`, no dependencies) against the change directory - the folder with `proposal.md`, `specs/`, `design.md`, `tasks.md`:

```
node .agents/skills/hrt-artifact-lint/lint.cjs <change-dir>
```

Output is `LEVEL path:line  message`, one per line. Exit 1 if any `ERROR`, else 0.

- **ERROR**: a deterministic structural defect with exactly one correct fix. Fix it directly, no user prompt, record what changed.
- **WARN**: non-blocking. Fix if quick.

The caller does not re-run these checks by hand after the lint passes. The caller's judgement checks (is a scenario genuinely behaviour, is a requirement genuinely testable, is an N/A section genuinely non-applicable) are not covered here and still run.

If Node is missing or `lint.cjs` cannot be found, say so and fall back to checking these by hand. Do not skip them silently.
