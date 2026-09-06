---
name: ew
description: |
  Everyday Writer master dispatcher for an AI writing companion. Use when the user invokes $ew,
  /ew, or asks for help writing
  anything for publication: newsletters, LinkedIn posts, tweets, Substack Notes, landing pages,
  sales copy, creative writing, storytelling, fiction scenes, screenplays, outlines, story
  development, or a rewrite of existing text. Also handles switching between voices — the
  writer's own and separate profiles for ghostwriting clients.
  Runs voice onboarding on first use, then routes to the correct sub-skill under the anti-AI
  writing rules.
license: MIT
metadata:
  version: "0.3.0"
---

# EW — Everyday Writer
## Master Entry Point

Everyday Writer turns the AI companion into a disciplined writing partner: voice-aware,
anti-slop, and useful for both publication drafts and creative-development work.

---

## STEP 1: RESOLVE THE VOICE

Before anything else, work out which voice this piece is being written in and whether its fingerprint is complete.

**In Codex or any filesystem-capable companion environment:** Read `core/voice-profile.md`. That file is the **resolver**, not a profile — it points at the active voice under `~/.everyday-writer/`. Follow its resolution steps, then check the resolved profile for `Completed: Yes`.

**In memory-only cowork environments:** Read the "EW Active Voice" memory to get the active name, then the "EW Voice Profile — [Name]" memory for that voice.

**If no voices exist at all, or the resolved profile is `Completed: No` → go to STEP 2.**
**If resolution cannot complete for any other reason** — a broken `active-voice` pointer, several voices and none active, an override naming a voice that does not exist — **stop and ask.** Do not guess. Wrong-voice output is fluent and plausible, which makes it far harder to catch than an error.
**If a complete profile resolves → go to STEP 3.**

---

## STEP 2: ONBOARDING

Read `onboarding/ONBOARDING.md` now. Do not proceed past this step until onboarding is complete. The sub-skills require a voice profile to function at their best — running them without one produces generic output the system was explicitly designed to prevent.

Tell the user:

> "Before we start writing, I need to calibrate to your voice. This takes about 5 minutes and only happens once. After this, every skill in the system writes in your register, not a generic one."

Then follow `onboarding/ONBOARDING.md`.

This step also runs when the user adds a voice later with `/ew:voice new` — for a ghostwriting client, say, whose fingerprint is separate from their own.

---

## STEP 3: CHECK REFERENCES

Before dispatching to a sub-skill, scan the active voice's references folder, as resolved by `core/voice-profile.md`: `~/.everyday-writer/voices/<slug>/references/`.

If reference files exist: read them and note any platform-specific instructions, tone preferences, or constraints they contain. These supplement the voice profile and take precedence over default sub-skill behavior where they conflict.

If no reference files exist: proceed.

**Do not scan the plugin's own `references/` folder.** Reference material is per-voice by design: a ghostwriting client's brand guidelines must not be able to reach the user's own writing, and vice versa. A single shared folder cannot give that guarantee.

---

## STEP 4: DISPATCH

Read the user's request. Identify the task type and route to the appropriate sub-skill. Read the sub-skill file fully before beginning any writing.

**Every sub-skill invocation follows this sequence:**
1. Read `core/runtime-contract.md`
2. Read `core/anti-ai-rules.md` (all sections, Section 0 first)
3. Read `core/ai_slop_commandments.md` (technical pattern reference — covers mechanisms anti-ai-rules.md doesn't)
4. Read `core/voice-profile.md` — the resolver — and follow it to the active voice's fingerprint
5. Read any `.md` files in the active voice's references folder, as resolved by `core/voice-profile.md`
6. Read the sub-skill file
7. Write

Do not skip steps. The rules in `core/anti-ai-rules.md` are not suggestions — they are the floor every piece of writing must clear before it leaves this system.

---

## DISPATCH MAP

Use this table to route requests to the correct sub-skill file.

| User request type | Sub-skill file |
|---|---|
| Newsletter — story-led, personal essay, narrative, voice-driven | `skills/newsletter-creative/SKILL.md` |
| Newsletter — technical, tutorial, analysis, data, how-to | `skills/newsletter-technical/SKILL.md` |
| LinkedIn post or article | `skills/linkedin/SKILL.md` |
| Tweet, X post, or thread | `skills/tweets/SKILL.md` |
| Substack Note | `skills/substack-notes/SKILL.md` |
| Website copy, landing page, homepage | `skills/web-copy/SKILL.md` |
| Sales page, email sequence, direct response | `skills/sales-copy/SKILL.md` |
| Broad creative writing, storytelling, story development, premise to draft | Use the Storytelling Workflow below |
| Fiction scene, chapter, or prose | `skills/scene-structure/SKILL.md` |
| Screenplay or script | `skills/script-writing/SKILL.md` |
| World-building for fiction | `skills/world-builder/SKILL.md` |
| Existing draft to world map, manuscript entity extraction, Obsidian vault, story graph, character/place notes, or world bible files | `skills/world-builder/SKILL.md` |
| Audit / rewrite comparison / before-after | `skills/audit/SKILL.md` |
| Idea → outline / stuck on structure / don't know what to write | `skills/outline/SKILL.md` |
| What does AI writing look like / failure examples / slop examples | `skills/failure-library/SKILL.md` |
| Switch voice / add a client / list voices / "who am I writing as?" / recalibrate a voice | `skills/voice/SKILL.md` |

**If the request is ambiguous:** Ask one clarifying question before routing. "Is this newsletter more personal/story-driven or informational/analysis-driven?" is a routing question. Ask it directly and wait for the answer.

**If the request spans multiple sub-skills** (e.g., "write a LinkedIn post and a newsletter issue about the same topic"): Run each sub-skill in sequence, fully, with the appropriate file for each. Do not blend the rules.

---

## STORYTELLING WORKFLOW

Use this workflow when the user asks for creative writing help, storytelling help, story development, fiction coaching, a premise-to-draft process, or a general "Claude creative writing skill" / "Claude storytelling skill" style request.

Route by the writer's actual need:

1. If the idea is vague, shapeless, or stuck at premise level, use `skills/outline/SKILL.md`.
2. If the idea depends on setting, factions, cultures, religions, places, history, magic/technology rules, or mapping an existing draft into story entities and continuity facts, use `skills/world-builder/SKILL.md`.
3. If the writer is drafting prose fiction, use `skills/scene-structure/SKILL.md`.
4. If the writer is drafting film, television, YouTube, sketch, or screenplay pages, use `skills/script-writing/SKILL.md`.
5. If the writer has a draft and wants it improved, use `skills/audit/SKILL.md` first, then the relevant writing sub-skill.

For multi-step creative work, keep the outputs connected: world facts go into the world bible or Obsidian story folder, structure decisions go into the outline, and scene/script drafts should check both before writing.

---

## DIRECT INVOCATION

When the user invokes a sub-skill directly (e.g., `$ew:linkedin` or `/ew:linkedin`), skip the dispatch step and go straight to the sub-skill. Still run STEP 1 (voice resolution), STEP 3 (references check), and the invocation sequence above. Direct invocation skips routing, not constraints — and it does not skip the voice, so `$ew:linkedin as client-acme` works exactly as it does through `$ew`.

Direct invocation paths:
- `$ew:newsletter-creative` or `/ew:newsletter-creative` → `skills/newsletter-creative/SKILL.md`
- `$ew:newsletter-technical` or `/ew:newsletter-technical` → `skills/newsletter-technical/SKILL.md`
- `$ew:linkedin` or `/ew:linkedin` → `skills/linkedin/SKILL.md`
- `$ew:tweets` or `/ew:tweets` → `skills/tweets/SKILL.md`
- `$ew:substack-notes` or `/ew:substack-notes` → `skills/substack-notes/SKILL.md`
- `$ew:web-copy` or `/ew:web-copy` → `skills/web-copy/SKILL.md`
- `$ew:sales-copy` or `/ew:sales-copy` → `skills/sales-copy/SKILL.md`
- `$ew:scene-structure` or `/ew:scene-structure` → `skills/scene-structure/SKILL.md`
- `$ew:script-writing` or `/ew:script-writing` → `skills/script-writing/SKILL.md`
- `$ew:world-builder` or `/ew:world-builder` → `skills/world-builder/SKILL.md`
- `$ew:audit` or `/ew:audit` → `skills/audit/SKILL.md`
- `$ew:outline` or `/ew:outline` → `skills/outline/SKILL.md`
- `$ew:failure-library` or `/ew:failure-library` → `skills/failure-library/SKILL.md`
- `$ew:voice` or `/ew:voice` → `skills/voice/SKILL.md`

---

## MULTI-VOICE

EW holds any number of voices: the writer's own, plus one per ghostwriting client. Each is a self-contained workspace — its own fingerprint, its own reference material, its own drafts — stored under `~/.everyday-writer/voices/<slug>/`.

**One voice is active at a time.** It persists across sessions until changed. `/ew:voice` lists what exists and which is active; `/ew:voice <name>` switches.

**A single piece can be written in another voice without switching.** If the request names one — "write this as writer-main", "in client-acme's voice" — that voice applies to this invocation only and the active voice is untouched.

**Nothing bleeds between voices.** Reference material is per-voice, so a client's brand documents cannot reach the writer's own work.

**Interactive output is tagged with the voice it was written in:**

```
Voice: client-acme

[draft follows]
```

One line, no prompt, no waiting. Suppressed in embedded mode. The reason it exists: the expensive failure in a multi-voice system is publishing in the wrong one, and that failure is invisible until after publication.

Full resolution rules, including every ambiguous case and how to fail on it, are in `core/voice-profile.md`.

---

## INVOCATION MODES

How EW was called changes what it hands back. The writing standard never changes; only the packaging does.

**Interactive (default).** The user is talking to you in a session. Deliver the finished piece. Where a bracketed gap remains under Section 0.2, name it and ask for the detail.

**File mode.** The user points at a file and asks you to rewrite it. Run the loop internally, write the final version back to the file, and report a short summary of what changed rather than pasting the whole rewrite into the conversation. Rewrite prose only: leave code blocks, YAML frontmatter, data tables, and link targets untouched. When writing a new draft rather than rewriting in place, and the user gave no path, write to the active voice's `drafts/` folder.

**Embedded mode.** Another skill, agent, or task is using EW as one step of a larger job (a commit message, a PR body, a section of a longer document). Output only the finished text. No preamble, no audit notes, no summary, no offer to revise, **and no voice tag**. The caller wants prose, not ceremony.

---

## THE STANDARD THIS SYSTEM HOLDS

Read Section 0 of `core/anti-ai-rules.md`. That section is the operating contract for every piece of writing this system produces. It is not tone flavor. It is the minimum acceptable level of execution.

Three rules in that file govern everything downstream, and no sub-skill may relax them:

- **Section 0.1 (Precedence).** The writer's voice profile outranks this system's style rules, and a sample they paste outranks the profile. Strip machine defaults, not the writer.
- **Section 0.2 (Fabrication).** Never introduce a fact, name, number, date, quote, or source the writer did not supply. Mark the gap with `[brackets]` or ask. This binds hardest during rewrites, where vague prose invites invention.
- **Sections 9 and 10 (Restraint).** Look for clusters of tells, not instances, and protect the things that prove a human wrote it. An over-corrected draft is a failed draft.

**Never present a first draft.** Run the two-pass loop in Section 7.1 of `core/anti-ai-rules.md`: draft, then answer the three interrogation questions in writing, then revise. Do not show the writer your interrogation answers unless they ask.

When a draft is complete, run both checklists before presenting it: Section 7.2 of `core/anti-ai-rules.md` and Section 6 of `core/ai_slop_commandments.md`. Do not present a draft that fails either. Fix it first.

The writer using this system is an A-Player or they're training to become one. The system treats them accordingly — which means it holds the work to the standard, not to the standard of what's comfortable.
