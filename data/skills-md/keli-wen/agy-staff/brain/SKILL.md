---
name: brain
description: Ask an external AGY reasoning lead to originate the proposal while the host challenges it and owns delivery. Use when the user explicitly invokes /agy:brain or requests this division of responsibilities.
argument-hint: '[--model carbon|argon|hydrogen|flash|<id>] [--effort low|medium|high|xhigh] [task]'
---

# agy brain

Use the supplied task or the current request. In /agy:lead the host sets direction; here the external brain frames the problem and owns the first proposal and major revisions. You still own the workspace, verification and delivery. Match the user's stage: a design discussion authorizes discussion, not implementation.

## Get the first proposal

Give the brain the original goal, verbatim constraints, already-settled decisions, known facts with sources, uncertainty, and available resources. Do not draft a solution, shortlist approaches or conduct an exhaustive investigation before handing off. Keep instructions about invoking this skill out of the brief. Include any budget and deadline; leave time for acceptance. The brain can reuse evidence, request targeted facts or use native Hydrogen / Flash for read-only reconnaissance.

Read `../jobs/SKILL.md` for execution boundaries, waiting and recovery. Resolve `<skill-dir>` to the absolute directory containing **this installed SKILL.md**. It is a placeholder you replace before invoking the shell. From that directory, go up two levels to the plugin root and use its `companion/agy-companion.mjs`. Keep the command's working directory in the user's target workspace so the job belongs to that project. Substitute the actual brief file path as well:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" staffer --brain --prompt-file "<brief-path>"
```

Pass `--model <carbon|argon|hydrogen|flash|id>` (and optional `--effort low|medium|high|xhigh` when paired with `--model`) when a specific model is requested; otherwise this background job defaults to Gemini 4 Carbon (`gemini-4-carbon-medium`). Honor explicit `--model`, `--effort`, `--timeout` and permission choices: if an explicitly requested model is unavailable, surface the diagnostic rather than silently switching models or widening permissions. Keep the ID with the assignment and wait using jobs.

## Challenge and deliver

Before substantive execution, independently check the proposal's consequential assumptions and trade-offs against the user's goal and concrete evidence. Small read-only probes need no gate. If it holds, state briefly what you checked and proceed within authorization. If a premise fails, pause that part and send the counterexample, its source and the decision it affects back to the brain:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" continue --job <brain-job-id> --prompt-file "<followup-path>"
```

When sending a counterexample, name the decision it challenges and ask what changes or still holds. Check any new consequential claim in the revision before accepting it; a proposed default can be useful without being an existing requirement.

The host's intervening discussion is not visible to AGY. Include changed constraints and evidence in the follow-up and retain the newly returned job ID for the next turn. If a conversation must start fresh, supply the original goal, current proposal and reasons earlier routes were dropped. Keep references inline or in an existing project artifact when useful; no required decision log.

Decompose and dispatch accepted work through available workers, integrate their changes and verify the result. Handle local execution choices yourself. Bring back evidence that changes the technical direction; a successful check needs no ceremonial round trip. Ask the user only when a decision changes their goal, budget or authorization. Report the outcome with its evidence and any remaining uncertainty.

**Example — a migration plan.** The team believes every historical job records a conversation ID. Pass that belief to the brain as an unverified premise. If its proposal relies on that ID, check an older record. An ID-less record is a reason to continue the brain job with the evidence and ask for a revised fallback. If the proposal already covers that case, verify the fallback and deliver the plan. A design-only request ends there.
