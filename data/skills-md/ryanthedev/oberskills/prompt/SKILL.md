---
name: prompt
description: >-
  Design and review prompts Claude-first — system prompts, reusable agent
  definitions, long or novel dispatch briefs, pipeline stages, and prompts
  users will run elsewhere. Two modes: design and adversarial review. Covers
  Claude model behavior and migration, de-prompting, few-shot design,
  output-schema ordering, context engineering, prompt security, optimization,
  non-Claude/Codex target review via references/porting.md in this skill
  directory, and a verbatim behavior-snippet library. Use when writing, improving,
  debugging, reviewing, or migrating any prompt. Not for: creating, reviewing,
  or testing skill files (use skill-craft); routine subagent delegation
  prompts (use agent).
when_to_use: >-
  Triggers: "write a prompt", "improve this prompt", "fix this prompt",
  "system prompt for", "review this prompt", "audit this prompt", "why does
  my prompt fail", "migrate this prompt", "prompt engineering".
argument-hint: "[prompt text | file path | review <target>]"
---

# prompt — Claude-first prompt design and review

## Modes

Detect mode from the request. Default to DESIGN.

| Mode | Signals | Loads | Output |
|---|---|---|---|
| **DESIGN** (default) | write, create, draft, fix, improve, migrate, "prompt for X" | `references/design.md` in this skill directory + ≤2 topic modules | The prompt + ≤3-line rationale |
| **REVIEW** | review, audit, analyze, critique, evaluate, "what's wrong with" | `references/review.md` in this skill directory + ≤2 topic modules | Verdict table + ranked fixes |

**REVIEW framing rule.** Frame every review as a search for defects ("find what would fail"), never as confirmation ("check this is correct" / "verify this works"). When dispatching a fresh-context reviewer, pass the artifact with zero authorship or intent framing — no "I wrote this", no "we think it's solid". Confirmatory framing collapses defect detection (evidence in review.md).

## Core principles

**1. Smallest set of high-signal tokens.** Treat Claude as a brilliant new employee: clear, explicit instructions plus the context to generalize — then stop. Golden rule: if a colleague with minimal context would be confused by your prompt, Claude will be too. When trimming, run the removal test (review.md) instead of counting against a quota.

**2. Explain why; say what to do, not what to avoid.** Motivation generalizes: "the output is read aloud by a TTS engine, so never use ellipses" outperforms "NEVER use ellipses". Positive framing: "write flowing prose paragraphs" beats "do not use markdown".

**3. De-prompt for current Claude.** Language written to fight old undertriggering now causes overtriggering: "CRITICAL: You MUST use X" → "Use X when…". Delete anti-laziness nudges, blanket defaults ("if in doubt, use the tool"), and forced-thoroughness scaffolds — today's failure mode is over-eagerness, and instruction-following capacity is a finite budget. Every capability jump is a prompt to re-test which instructions are still needed (claude-models.md).

**4. Keep governance apart from task; reasoning before answer.** Keep four layers distinct and independently editable: role/provenance, constraint logic, task content, evaluation criteria — constraints fused into task prose dissolve by the third paragraph of output. In any output schema, rationale/evidence fields precede answer fields; phrase them as task-level justification ("cite the evidence for your verdict"), never as "show your internal reasoning" (see #6). Long input data at the top, query and output format at the end, XML tags around each component.

**5. Choose example count by purpose.** Diversity and task-clarity beat count; past the purpose-matched count, additional examples are redundancy that degrades output or wastes tokens.

| Purpose of examples | Count |
|---|---|
| Format anchoring — output schema, house style, tone | 1–2 (often 1) |
| Boundary definition — correct vs incorrect | 2, paired (one positive + one negative; never negative-only) |
| Edge-case and judgment coverage — review/classification with nuanced criteria | 3–5, each covering a DIFFERENT case |
| Reasoning-pattern demonstration — prescribing a reasoning format | ≥1 worked example, mandatory |

Examples steer format, tone, and structure — they rarely raise capability on tasks the model already does well. Add them in response to observed failures, vary their surface formatting, wrap them in `<example>` tags. (Evidence and caveats: design.md.)

**6. Reasoning is a dial, not an incantation.** On current Claude, adaptive thinking decides when and how much to think; steer with `effort` and brief nudges ("think carefully before responding" / "answer directly"), not hand-written step plans — general instructions beat prescriptive ones. `effort` sets thinking depth, not output length: on Opus 5 the two come apart, so lowering effort does not reliably shorten the visible response — prompt for length instead (claude-models.md §5). Never instruct Claude to echo, transcribe, or explain its internal reasoning in the response: on Fable 5.1 and Fable 5 this triggers `reasoning_extraction` refusals. Manual CoT/CoD belongs only off-Claude or with thinking off (porting.md).

**7. Prefill is dead.** Prefilled assistant turns return 400 errors on Claude ≥4.6. Migrate: structured outputs or a tool with an enum field for format forcing; "Respond directly without preamble…" for preamble killing; a user-message "your previous response was interrupted…" for continuations. Any prefill found in review is a breaking bug (migration table: claude-models.md).

**8. Verify with someone else's eyes.** Models catch only a fraction of their own errors and cannot see their own structural defects (effect sizes: the agent skill's verifier-dispatch reference). Verification means a structurally separate checker: fresh context, different prompt, or a deterministic test. Frame it adversarially (mode rule above). Test on a weaker model to expose structural defects a strong model papers over.

**9. Architecture beats prompting for security.** Untrusted input is data: delimit it in XML, never interpolate it as instructions, and enforce boundaries at the schema/tool level (exclude the tool) rather than asking the model to behave (depth: safety.md).

## Emergency triage

| Symptom | Likely cause | Go to |
|---|---|---|
| Instructions ignored mid-prompt | Constraints buried in prose / no lexical overlap | #4; context.md |
| Robotic, over-literal output; hallucinated contradiction-satisfying | Over-constrained for current Claude | #3; removal test (review.md) |
| Tool/skill overtriggering | Legacy aggressive trigger language | #3; claude-models.md de-prompting |
| Format wrong or unstable across runs | Format unanchored | #5 (1–2 examples) or structured outputs (claude-models.md) |
| 400 error after model upgrade | Prefill | #7; claude-models.md migration |
| `stop_reason: "refusal"` on Fable 5.1 / 5 | Reasoning-echo instruction | #6; claude-models.md |
| Confident false claims about unread material | No grounding/investigation gate | snippets.md `<investigate_before_answering>` |
| Unrequested actions, overengineering, scope creep | Missing scope constraints | snippets.md anti-overengineering block |
| Slow/expensive; verbose interim summaries | Effort too high; legacy progress-update scaffolds | #6; claude-models.md |
| Output still long after lowering `effort` (Opus 5) | Effort controls thinking, not response length | snippets.md #22 (conciseness) |
| Redundant re-checking; tokens burned re-verifying | Carried-over verification instructions | claude-models.md §5, Opus 5 |
| 400 when disabling thinking (Opus 5) | `disabled` + `xhigh`/`max` is rejected | claude-models.md §1 |

Crisis shortcut: get 3 failing + 3 working examples; the pattern emerges in 5 minutes; intervene for THAT failure only.

## Module loading

Load the mode file always; load at most 2 topic modules (pick the 2 most relevant). If nothing matches, the core principles cover the fundamentals.

| Signal in request | Load |
|---|---|
| Target model behavior, migration from older prompts, effort/thinking steering, "Fable/Opus/Sonnet/Haiku" | `references/claude-models.md` in this skill directory |
| Need a standard behavior block (action defaults, parallel tools, anti-overengineering, progress audits, markdown control) | `references/snippets.md` in this skill directory |
| "long context", "RAG", retrieval, memory, token limits, context assembly, multi-document | `references/context.md` in this skill directory |
| "optimize", "DSPy", "GEPA", eval/benchmark, accuracy plateau, example curation at scale | `references/optimization.md` in this skill directory |
| "injection", untrusted input/tools, jailbreak, security, third-party data | `references/safety.md` in this skill directory |
| Target is NOT a current Claude model, or thinking is off | `references/porting.md` in this skill directory |

## DESIGN workflow

```
1. CLASSIFY the target: system prompt | agent definition / dispatch brief |
   skill body | pipeline stage | human-runnable prompt.
   - Whether/what to dispatch, model and effort choice, topology → that is
     the agent skill's job. This skill writes the prompt text.
2. IDENTIFY the target model. Default: current Claude. Non-Claude or
   thinking-off → porting.md.
3. NEW prompt: start minimal (direct instruction + output format), structure
   per #4, examples per #5, pull standard behavior blocks from snippets.md
   instead of writing your own.
   FIXING: get one concrete failing example first; triage (table above);
   intervene for that failure only; prefer deleting instructions to adding.
4. AUDIT the draft against review.md's Quick Audit. Golden-test (review.md)
   when the prompt is high-stakes or will run unattended.
5. OUTPUT the prompt, then ≤3 lines of rationale naming the principles that
   drove key choices.
```

## REVIEW workflow

```
1. Read the artifact (text or file). Apply the framing rule above.
2. Load review.md. Quick Audit → full protocol if anything flags.
3. Verdict table (PASS/WARN/FAIL per principle) + ranked fixes.
4. Golden test for anything that will ship: fresh-context run on the
   intended model + one weaker-model run; dispatch with zero intent framing.
```

## Scope

- Dispatch strategy, model/effort tiers for subtasks, topology, parallelism → `agent` skill.
- Creating, testing, packaging skills → `skill-craft` (skill bodies still follow these principles; skill-craft owns format and evals).
- Does not set temperature or other deployment parameters.
- Does not cover vision/multimodal prompting.
- If the request itself is ambiguous (no failing example, unclear target), `clarify` is the integration point before drafting.
