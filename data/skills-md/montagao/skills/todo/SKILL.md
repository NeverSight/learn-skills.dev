---
name: todo
description: Create a Plane task in Plane. By default, use the interview skill first to flesh out the issue before creating it; only skip the interview when the user clearly wants a minimal quick capture.
user-invocable: true
---

# /todo

Turn the user's message into a Plane work item.

Default to a short `interview` before creating the Plane item so the issue is specific, scoped, and actionable. Only skip the interview when the user clearly wants a fast inbox capture or provides a fully formed issue already.

## Behavior
- Default label: `claw_inbox`
- Extract (best effort):
  - due date (convert to YYYY-MM-DD)
  - priority (urgent/high/medium/low/none)
- By default, use the `interview` skill before creating anything.
- Skip the interview only if:
  - the user explicitly wants a quick capture with minimal ceremony, or
  - the request already includes a solid title, scope, outcome, and next step
- If you skip the interview and critical info is still missing, ask at most one clarifying question. If you still do not have enough detail, create it with `Needs details` in the description.

## When to use `interview`
Use `interview` as the default path. It is especially important when:
- the input sounds like a problem to explore rather than a task to track
- there is no clear outcome or deliverable
- scope, owner, or next step is unclear
- the user is asking to "flesh out", "think through", or define the issue
- the title would otherwise be generic and the description would be mostly placeholders

When you use `interview`:
- keep it lightweight and focused on making one good Plane issue
- ask enough questions to capture:
  - the problem or opportunity
  - the desired outcome
  - the scope and notable constraints
  - the next step or acceptance signal
- then turn the resulting brief/spec into the Plane issue description
- do not create the Plane item until the issue is concrete enough to be useful

## Tool use
- By default, use the `interview` skill first to produce a concise issue brief.
- If you skip the interview, do so intentionally and only for fast capture or already-complete issues.
- Use the `plane-api` skill:
  - action: "create"
  - title: from the user, or from the refined issue brief if `interview` was used
  - description: include the refined brief when available
  - due/priority if detected
  - labels: ["claw_inbox"]
  - use the `url` returned by `plane-api` as the canonical issue link; never hand-build Plane links

## Output
- ✅ Created: <title>
- ID: <id>
- Link: <url> (if available, and it should be the canonical `browse/<ISSUE_KEY>` link)
- Briefly mention whether the issue was fleshed out via `interview` or captured directly.
- If failure: short error summary + what to fix (auth/base url/workspace/project).
