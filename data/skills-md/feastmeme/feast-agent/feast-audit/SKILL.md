---
name: feast-audit
description: Audit a Feast strategy script before it may run with real money — the runtime's static rules first, then a model read against a fixed checklist — and record the verdict, bound to the file's exact bytes. Use when the user has a strategy script for their Feast agent, asks you to write one, or asks whether a script is safe to run.
---

# Feast script audit

A strategy script runs with the user's money, so it passes two stages first. Both are bound to the file's sha256: any edit is a new file and needs a new audit.

`FL` is the runtime's command, as in the feast-league skill:

```bash
node "${FEAST_LEAGUE_RUNTIME:-$HOME/.feast-league/runtime}/src/league/bin.mjs"
```

## Stage 1: the static rules (deterministic)

```bash
FL audit <file.mjs>
```

The runtime parses the file; it never runs it.

| Rule | Refuses |
| --- | --- |
| A1 | any direct wallet or process access: `baw`, child processes, `process`, workers |
| A2 | imports of any kind: `import`, `import()`, `require`, `import.meta` |
| A3 | network: `fetch`, sockets, URLs to any host but feast.meme |
| A4 | secrets: key-shaped hex, seed-phrase-shaped words, API keys, key files |
| A5 | dynamic code and reaching for globals: `eval`, `Function`, `globalThis`, `constructor`, `__proto__`, keys it cannot read |
| A6 | unbounded loops (`while`, unbounded `for`, recursion) and timers |
| A7 | the wrong shape: other exports, a tick outside 15–3600 s, code at the top level, over 64 KB |
| A8 | any `api` member but `buy`, `sell`, `launch`, `read.*`, `state`, `params`, `log` |
| A9 | (a warning) literal sizes over the per-trade limit |

**If it refuses:**
1. Show every hit with its rule and line.
2. Stop.
3. If you wrote the script, offer to fix it and audit again. Do not argue a rule away.

## Stage 2: your model read

**Before you start:**
- Read the whole file yourself, against [references/checklist.md](references/checklist.md).
- Answer every question in writing, in a few lines each.
- Be the user's advocate. You are looking for a script that would surprise them with their own money.
- Code you wrote yourself gets no exemption.

**Record the verdict:**

```bash
FL audit <file.mjs> --model-verdict pass --notes "M1: … M2: … M3: … M4: … M5: … M6: … M7: … M8: …"
FL audit <file.mjs> --model-verdict refuse --notes "M2: buys on every tick with no condition …"
```

**Refuse when** any answer is a real concern:
- it trades more than the user asked
- it has no exit
- it is obfuscated
- it does something the user did not ask for

**Then tell the user** in two sentences what the script does, and whether it passed.

## Then

A script with both stages passed can be planned and started (see the feast-league skill). It runs in the **warm-up tier**:
- its first 5 trades are at 0.001 BNB
- two failures in a row, or any hard-limit hit, stop it and notify the user

The runtime refuses to start a script whose current bytes lack either pass.
