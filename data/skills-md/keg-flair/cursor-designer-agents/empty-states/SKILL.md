---
name: empty-states
description: Produces a state plan for empty/loading/error/success states for a screen, flow, or component, including copy patterns, recovery actions, accessibility, token hooks, and QA checklist. Use when the user asks for state design, edge cases, or “what happens when there’s no data / slow network / failure?”.
---

# Empty / Loading / Error States

See shared conventions in `docs/HOUSE_STYLE.md` (severity, fallbacks, token hooks protocol).

## Defaults

- **State coverage**: at minimum cover empty, loading, error, and success/confirmation (if applicable).
- **Recovery-first**: every error state should propose a user recovery path (retry, edit, contact support) where reasonable.
- **Copy is functional**: message explains what happened, what to do next, and what the system is doing.
- **Token-first**: describe styling hooks by intent (surface/text/border/icon/focus/motion), not hex values.

## Constraints

- **Do not invent** business rules, data models, or error taxonomies as fact; label assumptions.
- **Ask at most 3 clarifying questions** (only if it changes which states exist or the recovery policy).
- If inputs are thin, still output a usable baseline state matrix + “highest-value next inputs”.

## Clarifying questions (ask max 3)

1. What is the **surface** (component vs screen vs flow) and what’s the **primary user job**?
2. What are the **failure modes** we must handle (permissions, validation, network, server, partial failure)?
3. Any constraints: **a11y**, localization, compliance/trust, offline support, dark/high-contrast themes?

## Inputs to request (only if missing)

- Scope: component/screen/flow + where it lives in the journey
- Data shape (even high level): what “empty” means (no items vs filtered to none vs new user)
- Known constraints: permissions, rate limits, offline, compliance/trust, localization

## Output template

```markdown
## State plan: [Surface name]

### Assumptions / constraints
- …

### State taxonomy (what “empty” means here)
- **No data ever** (new user / zero items):
- **No results** (filters/search yield none):
- **No access** (permission/role):
- **Unavailable** (service down / maintenance):

### State matrix
| State | Trigger | User message (headline + body) | Primary action | Secondary action | System behavior | A11y notes |
| --- | --- | --- | --- | --- | --- | --- |
| Loading | … | … | n/a | n/a | skeleton/spinner + timeout policy | reduce motion, announce status (if needed) |
| Empty: first-time | … | … | Create/Add | Learn more | show education + examples | heading structure + focus |
| Empty: no results | … | … | Clear filters | Adjust search | preserve query/filter context | announce results count |
| Error: retryable | … | … | Retry | Contact support | preserve inputs; backoff | error association + focus |
| Error: validation | … | … | Fix inputs | n/a | inline errors + summary policy | labels/aria-describedby |
| Error: permission | … | … | Request access | Back | no dead ends | explain why + next steps |
| Success/confirmation | … | … | View item | Undo (if possible) | toast + audit trail link (if needed) | do not steal focus |

### Copy patterns (rules + examples)
- **Empty**: explain why it’s empty + what to do next + optional education.
- **Error**: what happened (safe) + what to do + what the system did/does.
- **Loading**: show progress/expectation; include timeout escalation if relevant.

### Recovery policy
- **Retry**: when offered, what resets vs what is preserved
- **Undo**: which actions qualify; time window; when audit log replaces undo

### Design system hooks (token-first)
- **Surface tokens**:
- **Text tokens**:
- **Icon/status tokens**:
- **Motion tokens** (reduced motion behavior):

### QA checklist
- [ ] All state triggers covered (including filtered empty vs true empty)
- [ ] Recovery actions are always available (no dead ends)
- [ ] Copy is localizable (no hardcoded lengths; truncation rules)
- [ ] Keyboard/focus behavior verified for error summaries and actions
- [ ] Reduced-motion path verified
```

