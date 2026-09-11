---
name: to-questionnaire
description: Turn a decision you cannot fully answer into a questionnaire for someone else.
disable-model-invocation: true
---

Create a Markdown discovery questionnaire for a recipient with missing knowledge. Grill the send, not the subject: ask only who receives it and what must come back.

1. Ask recipient role, expertise, relationship in one exchange; stop when audience and unique knowledge are clear.
2. Ask which facts/decisions the user cannot resolve; stop when answers enable a concrete next decision/action.
3. Write `to-questionnaire-<topic-slug>.md`; cover each outcome once and report path.

## Structure

Order questions most-important-first; use theme headings after a handful.

```markdown
# <Questionnaire title>
**Purpose:** <decision riding on it>
**From:** <user> -- **To:** <recipient> -- **How answers will be used:** <destination>
## Context
<One orienting paragraph.>
## How to answer
<Deadline/effort; partial and "I don't know" are useful.>
## <Theme>
### <One focused question>
_Why this matters: <only to prevent misreading>_
>
## Anything else?
What did we not ask that we should know?
```

One idea and answer stub per question; rationale only when misreading is likely.
