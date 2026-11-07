---
name: breakthrough-evaluator-agent
description: "Send an independent judge that is not the author: a fresh evaluator subagent that checks finished work against pass criteria written before it was built (evaluator mode), or audits a batch against its source of truth (audit mode), with evidence for every verdict and never a fix. Use when the owner asks for an evaluator, reviewer, auditor or judge, or says 'send a judge', 'evaluate this', 'check my work with a fresh agent', 'get a second agent to review this', 'audit this folder', 'audit my registry', 'verify this against the source of truth', or 'LLM-as-judge'. Runs only when asked; it does not fire on its own at the end of a task. Not for checks a machine can run (tests, schema validation, a search that must return zero), not for hundreds of identical units, and not for fixing anything."
---

# Evaluator agent

This skill is a pointer. ⛔ It holds no rules, no brief template and no output schema: all of that lives in the playbook, in one place, so there is nothing here to drift out of date. Do the three steps below.

## 1. Find the playbook, the owner's copy first

1. **A my-second-brain vault.** If the working directory (or a folder the owner names) has `99_Meta/structure-doctrine.md`, read that doctrine's section 1 for the real path of the methodology layer, then look for `<methodology>/Playbooks/evaluator-agent/`. If the folder is there, enter through its door: read `_Evaluator-Agent-Guide.md` and do its four beats, then read `evaluator-agent-playbook.md` in the same folder. The owner's copy always wins over the seed.
2. **A copy the owner keeps elsewhere.** Look for a standing pointer that names the folder of the owner's copy: in your memory, or in the `CLAUDE.md` of the folder you are working from (the installer writes one there when the owner saves a copy outside a my-second-brain vault). If you find one, or the owner tells you where the copy is, read the door and the playbook in that folder.
3. **Otherwise, the seed shipped with this skill**: `playbook/evaluator-agent/evaluator-agent-playbook.md`, relative to this file. Tell the owner in one line: "Using the seed playbook that came with the skill; nothing from this run will be kept unless you save a copy." The seed works without saving anything, but updating the skill replaces it, so the three jobs and the run log only last in a saved copy. When running from the seed, skip step 6 of the playbook's "The moves" (registering a row on the door) and ⛔ never edit any file inside this skill's folder, because an update replaces them.

If the playbook's "Your three real jobs" still shows placeholders, ask the owner for them once. ⛔ It does not block the run: if they skip it, carry on with the job in front of you.

## 2. Send the judge

Follow step 1 and step 2 of the playbook's "The moves": fill the six field brief, then send a new general-purpose subagent with the brief and nothing else. ⛔ Never a fork.

## 3. Receive the report

Follow the playbook's "The moves" from step 3 on. It starts with rerunning one piece of the judge's evidence yourself, before you trust anything else in the report.

Not installed properly, or want it inside a vault? The installer is `INSTALL.md` at https://github.com/breakthrough-edu/breakthrough-evaluator-agent.
