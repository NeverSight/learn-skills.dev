---
name: memory-bank
description: "Use this skill to save, recall, or organize memories across conversations. Trigger on: 'remember this', 'save this', 'note this', 'what did we discuss about...', 'check your notes', 'do you remember', 'recall'. Also use proactively when the user seems to be resuming previous work, referencing past decisions, or when you discover something genuinely worth preserving for future sessions. This skill is NOT limited to code — use it for business decisions, personal notes, meeting recaps, research, project management, creative work, client history, anything."
---

# Agent Memory Bank

A persistent memory system for storing knowledge that survives across conversations — for any domain: code, business, personal, research, creative work, client management, and more.

**Default location:** `./memory/` (create if it doesn't exist)

**Default structure:**
- `./memory/episodic/`
- `./memory/semantic/`
- `./memory/procedural/`

---

## Core Philosophy

- **Three memory types, one system**: Store experiences as `episodic`, durable facts and evolving state as `semantic`, and repeatable workflows as `procedural`.
- **Use the shape that matches future retrieval**: Save things based on how you'll want to find them later — what happened, what is true, or how to do it.
- **Prefer history over rewrites**: When an event or decision matters in its own right, preserve it as a dated record rather than erasing what came before.
- **But don't spam**: Update living records when the goal is to maintain current state or current instructions.
- **Never delete memory files** — mark outdated ones with `status: superseded` instead.
- **Write for resumption**: Notes should be self-contained — a future session with zero context should still understand them.
- **Bias toward usefulness**: Save things that may matter later, especially details that are easy to forget but annoying to rediscover.
- **Tags are first-class**: Tag memories so they can be searched quickly across domains, projects, people, and topics with `rg`.

---

## Quick Routing Cheat Sheet

Use this fast decision tree when deciding what to save:

- Ask: **what will future-you want back?**
- If the answer is **what happened?** -> save `episodic`
- If the answer is **what is true now?** -> save or update `semantic`
- If the answer is **how do we do this?** -> save or update `procedural`
- If the answer is **more than one of those** -> save it in more than one form

Mini examples:
- "We had a nasty auth incident today" -> `episodic`
- "The client prefers weekly async updates" -> `semantic`
- "Here is the release checklist" -> `procedural`
- "A failed deploy taught us a safer rollout order" -> `episodic` + `procedural`
- "A conversation revealed a lasting user preference" -> `episodic` + `semantic`

---

## Memory Types

### Episodic

Use for events, moments, decisions-in-context, meetings, incidents, milestones, discoveries, failed attempts, and progress snapshots.

This answers: **what happened?**

Examples:
- A debugging session that revealed the root cause
- A client call and the decisions made during it
- A travel day where something went wrong
- A negotiation update or milestone reached

### Semantic

Use for durable knowledge, evolving facts, preferences, profiles, constraints, current project state, and anything that may be updated many times over.

This answers: **what is currently true?**

Examples:
- User communication preferences
- Current architecture constraints
- Client profile and standing preferences
- Active project status and known risks

### Procedural

Use for repeatable methods, checklists, workflows, instructions, playbooks, routines, and standard ways of doing things.

This answers: **how do we do this?**

Examples:
- How to deploy safely
- Weekly reporting workflow
- Travel packing checklist
- How to onboard a new client

One interaction may produce more than one memory type. That's good.

Example:
- An incident happens -> save an `episodic` note
- It reveals a durable constraint -> update a `semantic` note
- It teaches a better workflow -> update a `procedural` note

---

## Tags

Use tags generously but intentionally. Tags make cross-cutting retrieval easy without overcomplicating the folder structure.

Good tag categories:
- domain: `code`, `business`, `personal`, `research`, `creative`
- topic: `auth`, `deploy`, `health`, `finance`, `planning`
- entity: `client-acme`, `project-helios`, `user`, `team`
- type hints: `decision`, `preference`, `incident`, `checklist`, `workflow`

Prefer short, stable, lowercase tags with hyphens when needed.

Examples:
- `tags: [code, auth, incident, project-helios]`
- `tags: [business, client-acme, preference, communication]`
- `tags: [personal, travel, checklist]`

---

## How to Route New Information

Ask these questions:

1. Is this mainly an event or time-bound moment?
   - Save `episodic`
2. Is this a durable fact, preference, constraint, or current state?
   - Save or update `semantic`
3. Is this a repeatable method or instruction?
   - Save or update `procedural`
4. Does it fit more than one?
   - Save it in more than one form when future retrieval would differ

Examples:
- "We debugged auth and found the cookie domain was wrong"
  - `episodic`: the debugging session
  - `semantic`: auth depends on the correct parent-domain cookie setting
- "The client prefers weekly async updates"
  - `semantic`: client preference
- "Here is our monthly reporting process"
  - `procedural`: recurring workflow
- "Friday's failed deploy taught us to run migrations before workers"
  - `episodic`: failed deploy
  - `procedural`: safer release workflow

---

## Proactive Saving

Since this skill is loaded, memory is clearly valued here — lean into it. Save without being asked when you encounter:

- Something that took real effort to figure out (research, debugging, negotiation, comparison)
- A decision with non-obvious reasoning — why X over Y
- Information that would be painful to reconstruct if this conversation ended
- Dead ends and failed approaches — saves future sessions from repeating them
- In-progress work with clear next steps
- Anything the user seems to care about that isn't obvious from context alone

Applies to any domain — code, business, personal, creative, research, client work, anything.

---

## File Naming

```
episodic:   YYYY_MM_DD_meaningful_name.md
semantic:   stable_subject_name.md
procedural: how_to_meaningful_name.md
```

Examples — notice these span many domains:
- `2025_03_09_auth_bug_root_cause.md`
- `2025_03_10_q1_marketing_decisions.md`
- `user_preferences.md`
- `client_acme_profile.md`
- `project_helios_status.md`
- `how_to_rotate_api_keys.md`
- `weekly_client_reporting_workflow.md`

Multiple episodic files per day are normal and encouraged. Semantic and procedural files should usually keep stable names so they can be updated over time.

---

## Creating a Memory File

Use your native file tools to create and edit memory files.

**Shared frontmatter fields:**
```
---
summary: "One line — specific enough to know if you need to read this"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: episodic | semantic | procedural
tags: [optional, tags]
---

```

**Episodic template:**
```
---
summary: "Debugging session that found the auth cookie domain mismatch"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: episodic
tags: [code, auth, debugging, incident]
---

# Title

[Write the event clearly enough that a future session understands what happened and why it mattered]
```

**Semantic template:**
```
---
summary: "Current auth configuration constraints for production"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: semantic
tags: [code, auth, configuration, project-helios]
---

# Title

[Write the current known state, preferences, constraints, or facts that should remain current over time]
```

**Procedural template:**
```
---
summary: "Safe production deploy workflow"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: procedural
tags: [code, deploy, workflow, operations]
---

# Title

[Write the repeatable process clearly enough that someone can follow it later]
```

**Some section ideas** (use only what fits):
- **Context** — why this matters, background
- **Key Decisions** — what was decided and why
- **Details / Findings** — the actual content worth saving
- **Current State** — the up-to-date truth right now
- **Procedure / Checklist** — ordered steps or repeatable instructions
- **Lessons Learned** — what this teaches for future work, mistakes to avoid, or patterns worth reusing
- **People / Contacts** — who's involved
- **Next Steps** — what to do next
- **Didn't Work** — dead ends to avoid

There's no required structure. A memory for a client call looks different from a debugging session — that's fine.

---

## Editing an Existing Memory

Use your native file editing tools to update memory files.

### Update episodic when:
- You're still actively adding details to the same event or session
- You want to complete or correct the record of what happened

### Update semantic when:
- The current state, preference, fact, or constraint has changed
- You learned something that refines a long-lived record
- You want one stable file to represent the latest understanding

### Update procedural when:
- The workflow changed
- A checklist was improved
- You discovered a safer, faster, or clearer way to do the task

When a change deserves both history and current state, do both:
- create or update an `episodic` file for the event
- update the relevant `semantic` or `procedural` file for the lasting takeaway

---

## Searching Memories

### Quick orientation (run this first when memories feel relevant)
```bash
rg --files ./memory | sort
```
This shows the files that exist across all memory types — a fast orientation to what's here.

### Search by memory type
```bash
rg "^memory_type: episodic$" ./memory/ --no-ignore
rg "^memory_type: semantic$" ./memory/ --no-ignore
rg "^memory_type: procedural$" ./memory/ --no-ignore
```

### Read summaries across all files
```bash
rg "^summary:" ./memory/ --no-ignore
```

### Search by keyword (full text)
```bash
rg "keyword" ./memory/ --no-ignore -i
```

### Search summaries only
```bash
rg "^summary:.*keyword" ./memory/ --no-ignore -i
```

### Search by tag
```bash
rg "^tags:.*keyword" ./memory/ --no-ignore -i
```

### Search by tag combination
```bash
rg "^tags:.*auth.*project-helios|^tags:.*project-helios.*auth" ./memory/ --no-ignore -i
```

### Search semantic memories for current state
```bash
rg "keyword" ./memory/semantic/ --no-ignore -i
```

### Search procedural memories for how-to guidance
```bash
rg "keyword" ./memory/procedural/ --no-ignore -i
```

### Search episodic memories for what happened
```bash
rg "keyword" ./memory/episodic/ --no-ignore -i
```

After finding relevant files, **read them** using your native file tools. The summary tells you if it's worth reading; reading gives you the actual context.

---

## When to Check Memories

Default behavior: check memories when the task feels like it might connect to prior work — e.g. the user references a past decision, says "like we discussed", or you're about to re-research something familiar.

This default can be overridden by the environment. A system prompt may instruct you to always check memories, or only check when explicitly asked — follow those instructions. This skill describes the fallback when no such instruction exists.

When checking:
- orient quickly to what exists
- choose the memory type that matches the question
- search by tags, keywords, and summaries
- read the most relevant files for actual context

Use this retrieval pattern:
- `episodic` for "what happened?"
- `semantic` for "what do we know now?"
- `procedural` for "how do we do this?"

---

## When to Save

No strict rules — use judgment. Good candidates:
- Something that took real effort to figure out
- A decision with non-obvious reasoning behind it
- Information you'd lose if this conversation ended now
- Anything the user explicitly wants remembered
- A preference, profile, or constraint likely to matter again
- A workflow or checklist you'll likely reuse
- A bug, config detail, or environment-specific gotcha that could bite again later

Not worth saving:
- Easily googleable facts
- Transient scratchpad work
- Anything the user will obviously remember themselves

---

## Cleanup and Distillation

Do not aggressively reorganize or distill memories by default.

Only do memory cleanup when:
- The user asks to organize, clean up, archive, consolidate, or review memories
- You are already working inside the memory folder and obvious cleanup is part of the task

When cleaning up memories:
- Prefer marking outdated files with `status: superseded` or moving them into an `archive/` folder if such a structure already exists or the user asks for it
- Avoid deleting memory files unless the user explicitly requests deletion
- Preserve historical context; do not collapse distinct events into one vague note
- Merge or simplify only when duplicates are clearly redundant and the result is more useful than the originals
- Keep tags consistent so search stays clean

Distill carefully:
- Promote repeated or clearly durable facts into `semantic` memory when you have good evidence they should be long-lived
- Promote repeatable workflows into `procedural` memory when they are clearly meant to be reused
- If you are not confident, preserve the original memory and avoid over-distilling

If the user asks to "clean up my memories", a good default is:
- review for stale or superseded files
- archive or mark outdated material
- tighten titles and tags
- leave meaningful history intact

---

## When to Create vs Update a File

**Create a new file** when:
- You are recording a distinct event, session, decision point, incident, or milestone
- You are starting a new topic with no current memory for it
- You want to preserve a dated snapshot of what happened at a specific point in time

**Update an existing file** when:
- You are maintaining an ongoing semantic record of current state
- You are improving an existing procedure or checklist
- A stable file for this subject already exists and should remain the source of truth

The goal is to avoid both extremes: don't spam new files for every tiny change, but don't flatten meaningful history into one endlessly edited document either.

When in doubt:
- choose `episodic` if the value is historical context
- choose `semantic` if the value is current truth
- choose `procedural` if the value is repeatable guidance
- choose more than one if needed

When something evolves across clearly distinct phases, new files tell a useful story:

```
2025_03_09_supplier_negotiation_initial.md
2025_03_10_supplier_negotiation_counteroffer.md
2025_03_11_supplier_negotiation_final_terms.md
```

To mark a file as outdated, add `status: superseded` to its frontmatter — don't delete it.

---

## File Organization

By default, organize memory by type:
- `./memory/episodic/`
- `./memory/semantic/`
- `./memory/procedural/`

You may also encounter or be instructed to use a more structured layout such as `./memory/semantic/clients/` or `./memory/procedural/operations/`. Follow whatever structure exists; if none exists, use the default type-based layout.
