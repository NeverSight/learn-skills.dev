---
name: network-change-cab
description: Plan and run network change control — RFC, CAB pack, freeze, rollback, standard vs normal vs emergency, clinical windows. Use for production mutations, freeze calendars, or "can we ship this Friday". Pairs with atlassian-ops tickets and netops-mcp for the actual commit.
origin: snm-pack
---

# Network change & CAB

If it mutates production, it is a change. If it can delay care, it is a
**clinical** change. Consent-gated on the device (`netops-mcp`) is not a
substitute for CAB — it is the last mile.

## When to use

- Building a change plan or CAB agenda
- Emergency vs normal vs standard classification
- Freeze (EHR go-live, financial close, Joint Commission survey)
- Rollback design, T-minus checklist

## Classification

| Type | When | Path |
|------|------|------|
| Standard | catalogued, low risk, reversible, done before | pre-approved, still ticketed |
| Normal | everything else | peer review + CAB |
| Emergency | active Sev1 / safety | SNM + InfoSec, post-CAB within 2 business days |

If the engineer is unsure, it is **normal**.

## T-minus checklist (normal/major)

| When | Gate |
|------|------|
| T-7d | RFC approved, Lucid to-be, monitoring probes named |
| T-3d | CAB decision, comms to site/clinical, spare/optics on site |
| T-24h | config staged, diff reviewed, rollback timed |
| T-0 | freeze check, window start, commander named |
| T+verify | probes green, app owner yes, ticket evidence |
| T+24h | no silent error counters, close or back out |

Full: [reference/tminus.md](reference/tminus.md).

## Rollback is a plan, not a slogan

- Trigger: named probe or app-owner "no" within N minutes
- Time to restore < remaining window / 2
- Who types the commands; who says go
- Healthcare: clinical engineering on the bridge for biomedical/EHR paths

Refuse to file a change with rollback = "restore last backup" and no
timing.

## Freeze

Maintain a freeze calendar: EHR upgrades, imaging go-lives, Joint
Commission, year-end, mass-casualty drills. Standard changes may pass;
normal changes need SNM exception in writing.

## CAB pack (one page per change)

Title, risk, services, window, what can go wrong, rollback minutes,
verifier, related incidents, Lucid, RFC. SNM reads this, not the 40-page
SOW.

## Output

```text
CLASS
- standard | normal | emergency
- why

WINDOW
- start/end · freeze conflict · clinical calendar

PLAN
- steps · commander · verifier

ROLLBACK
- trigger · minutes · commands owner

CAB
- ask (approve/defer) · conditions
```

## Reference Files
- [reference/tminus.md](reference/tminus.md)
