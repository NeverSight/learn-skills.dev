---
name: crash-out
description: Anti-hallucination mode where Claude drafts an answer and then becomes obsessed with proving itself wrong, attacking every claim with tools and counter-evidence and shipping only what survives; invoke via /crash-out on factual questions, debugging, research, or any answer where confident-and-wrong is expensive.
---

# Crash Out

Hallucinations survive because the model defends its first draft. This flips the incentive: after drafting, the only goal is to destroy the draft. Every claim gets attacked. Whatever is still standing is the answer.

## When to use
- Factual questions, research, technical claims, debugging conclusions.
- Anywhere a confident wrong answer costs more than a slow right one.

## Behavior
1. Draft the answer privately. Do not show it yet.
2. Extract every load-bearing claim from the draft into a list: facts, numbers, names, API behaviors, causal statements. If the answer depends on it, it goes on the list.
3. Attack each claim in turn. Attacking means evidence, not re-reading your own reasoning:
   - Run the code, command, or query when one exists.
   - Read the actual source, docs, or file.
   - Search for disconfirming evidence, not confirming.
   - Attack load-bearing claims from at least two angles.
4. Verdict per claim:
   - SURVIVED: attacked and held, evidence cited.
   - SHAKY: could not verify either way. Must be labeled as unverified in the final answer, never asserted as fact.
   - BUSTED: disproven. Correct it or delete it.
5. Rewrite the answer from survivors only. Shaky items appear with an explicit flag and what would confirm them.
6. If a busted claim was central, say the original answer was wrong and what changed. Never smooth it over.

## Output
The verified answer with unverified statements flagged inline, followed by a short kill list: claims that got busted during the crash-out and what replaced them.
