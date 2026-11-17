---
name: reset-context-contamination
description: Discards this thread's accumulated drafts and framings and re-derives the task from a clean problem statement. Use when the user says the thread is contaminated, the conversation is going in circles, or that they want a fresh take.
metadata:
  version: "0.1.5"
  categories: "agents"
  topics: "context, reset, reframing, thread-hygiene"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/reset-context-contamination
    emoji: "🧹"
---

This thread's history has become the problem - prior drafts and framings are anchoring every new attempt. Reset.

First, extract what's worth keeping, in plain factual terms: who is involved, the outcome I want, the hard constraints, the known facts, and - critically - what's already been tried and ruled out, so a fresh derivation doesn't walk back into a dead end.

Then pick the path by severity:

- Deep contamination, or anything high-stakes: do not try to reset yourself - the contaminated model cannot be trusted to author its own reset. Hand the extracted brief to a fresh subagent, or recommend I start a new session. A genuinely clean context window is the only reliable reset.
- Mild drift only: re-derive in-thread from the extracted brief, as if seeing the task for the first time. Void the earlier drafts entirely - no referencing, quoting, or patching them. If you are unsure the brief itself is right, show it to me before drafting; otherwise just proceed.
