---
name: china-maxing
description: Session mode that translates every sub-agent prompt into Mandarin before dispatch (more meaning per character, fewer tokens) while keeping code, identifiers, and all user-facing output in English; invoke via /china-maxing at the start of any session that will fan out sub-agents and the token bill matters.
---

# China Maxing

Mandarin packs more meaning per character than English, so the same brief costs fewer tokens on most tokenizers. Flip this on and every prompt you send to a sub-agent ships in compressed Mandarin while your source-of-truth and all results stay in English. Same instructions, smaller bill.

## When to use
- At the start of a session that will spawn sub-agents (Agent/Task tools) more than once or twice.
- Long, instruction-heavy briefs going to multiple agents. The longer the prose, the bigger the cut.

## Behavior
1. On activation, confirm the mode in one line and keep it on for the rest of the session.
2. Before every sub-agent dispatch, translate the instruction prose into clear, dense Simplified Chinese. Keep every constraint, acceptance criterion, and edge case intact.
3. Never translate: code, file paths, identifiers, URLs, CLI commands, API and product names, or anything the agent must echo verbatim. Those stay exactly as written.
4. Back-check before sending: reread the Mandarin against the English intent. If any clause turns ambiguous in Mandarin, keep that clause in English rather than risk drift.
5. Tell every sub-agent to reason in whatever language it likes and RETURN results in English.
6. Skip translation when a prompt is mostly code or under about 50 words. Translating those saves nothing.
7. Everything the user sees stays in the user's language. Mandarin lives only on the wire between agents.

## Output
Dispatches go out in Mandarin; results and all user-facing output come back in English. On the first dispatch, note the rough token savings in one line (typical prose briefs compress 30 to 50 percent).
