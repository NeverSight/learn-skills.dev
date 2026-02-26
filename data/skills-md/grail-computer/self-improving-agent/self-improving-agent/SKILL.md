---
name: self-improving-agent
description: >
  Meta-skill for making the agent self-improving. Covers updating AGENTS.md,
  creating new skills from repeated workflows, and deciding what to systematize.
  Invoke after completing tasks, when noticing repeated friction, or at session end.
---

# Self-Improving Agent

> **When to use this skill:**
>
> - After completing a significant task (post-task reflection)
> - When you notice yourself repeating a multi-step workflow
> - When a human corrects your behavior and you need to persist the correction
> - When the codebase map in AGENTS.md is stale
> - At the end of a working session

---

## Step 1: Diagnose What Needs Improving

Ask yourself these questions after completing work:

1. **Did I wander?** Did I spend time searching for files that should have been in the codebase map?
   - → Update the **Codebase Map** in `AGENTS.md`

2. **Did I get corrected?** Did the human tell me to do something differently?
   - → Add the correction to **Local Norms**, **Guardrails**, or **Patterns & Gotchas** in `AGENTS.md`

3. **Did I repeat a workflow?** Did I follow a multi-step procedure that I've done before (or will likely do again)?
   - → Create a new **skill** (see Step 3 below)

4. **Did something surprise me?** Did I discover a gotcha, a deprecated API, or a non-obvious coupling?
   - → Add it to **Patterns & Gotchas** in `AGENTS.md`

5. **Is the AGENTS.md stale?** Do the norms, entry points, or conventions no longer match the actual codebase?
   - → Update the outdated sections now

If none of these apply, no action is needed. Don't create artifacts for the sake of it.

---

## Step 2: Update AGENTS.md

When updating `AGENTS.md`, follow these rules:

### Codebase Map Updates

1. Read the current map in `AGENTS.md`.
2. Use `find` or `ls` (not recursive full-tree) to see the actual top-level structure.
3. Update only the parts that have changed. Don't rewrite the whole map.
4. Focus on: entry points, directory roles, config files, test locations.

### Adding Norms or Guardrails

1. Write the rule as a **short, imperative statement** — one line if possible.
2. Place it in the correct section:
   - **Local Norms** → How to build, test, run, or style code in this repo
   - **Guardrails** → What the agent must NEVER do
   - **Patterns & Gotchas** → Non-obvious discoveries about the codebase
3. If a correction contradicts an existing entry, update the existing entry rather than adding a duplicate.

### Quality Checks

- Keep entries concise. Agents read this every session — brevity compounds.
- Remove placeholder/example entries (italicized) once real entries exist.
- Don't add generic advice. Every entry should be **specific to this repo**.

---

## Step 3: Create a New Skill

Use this procedure when you've identified a repeatable workflow worth capturing.

### Decision: Is This a Skill or an AGENTS.md Entry?

```
Is it a multi-step procedure with a clear output?
  → YES → Skill
  → NO  → AGENTS.md entry

Is it specific to HOW this repo works (norms, navigation)?
  → YES → AGENTS.md entry
  → NO  → Skill

Am I unsure?
  → Start as an AGENTS.md entry. Promote to skill if it grows.
```

### Creating the Skill

1. **Choose a name.** Use a verb-noun pattern reflecting the job: `debug-ci`, `draft-release-notes`, `run-migration`, etc.

2. **Create the folder and file:**

   ```
   skills/<skill-name>/SKILL.md
   ```

3. **Write the SKILL.md** with this structure:

   ```markdown
   ---
   name: <skill-name>
   description: <one-line description of what job this skill does>
   ---

   # <Skill Name>

   > **When to use:** <clear trigger condition>

   ## Steps

   1. <Step 1 — be specific and imperative>
   2. <Step 2>
   3. ...

   ## Output Contract

   <What "done" looks like. Be specific about format, location, and quality.>
   ```

4. **Key principles for good skills:**
   - Frame around a **job to be done**, not a tool ("debug CI failure", not "use grep")
   - Make the **trigger** clear — when should an agent reach for this?
   - Define the **output contract** — what does "done" look like?
   - Include **examples of good output** as assets if helpful (put in `skills/<name>/examples/`)
   - Keep steps **imperative and specific** — avoid vague instructions

5. **Add the new skill to the skills table** in `AGENTS.md`:
   ```markdown
   | [<skill-name>](skills/<skill-name>/SKILL.md) | <purpose> | <trigger> |
   ```

### Adding Scripts or Assets to a Skill

If a skill needs deterministic execution (not just LLM judgment), add scripts:

```
skills/<skill-name>/
├── SKILL.md          # The playbook (always required)
├── scripts/          # Helper scripts for deterministic steps
│   └── validate.sh
└── examples/         # Reference outputs showing "good" quality
    └── example-output.md
```

Reference these from SKILL.md: "Run `scripts/validate.sh` to verify the output."

---

## Step 4: Decide Scope — Repo-Local vs Global vs Shared

```
Does this skill only matter for THIS repo?
  → Keep it in skills/ within this repo (repo-local)

Have I felt this pain in another repo too?
  → Promote to ~/.agent/skills/<name>/ (machine-global)
  → Copy the skill folder there

Does my team keep repeating this workflow?
  → Promote to a shared repo or registry (shared)
  → Move the skill folder into the team's shared skills repo
```

### Promotion Checklist

When promoting a skill from repo-local to global:

1. Remove any repo-specific paths or references from the SKILL.md.
2. Make the instructions generic enough for any project.
3. Test it works without the original repo's context.
4. Keep the repo-local version if it has repo-specific customizations.

---

## Step 5: Validate the Improvement

After making any changes (AGENTS.md update or new skill):

1. **Re-read the updated file.** Does it read clearly? Would a fresh agent session benefit from it?
2. **Check for contradictions.** Does the new entry conflict with anything existing?
3. **Check for bloat.** Is this file getting too long? If AGENTS.md exceeds ~200 lines, consider:
   - Archiving old gotchas that are no longer relevant
   - Moving detailed procedures into skills
   - Summarizing verbose entries
4. **Commit the changes** with a clear message:
   ```
   docs: update AGENTS.md with <what you learned>
   ```
   or
   ```
   feat: add <skill-name> skill for <job description>
   ```

---

## Anti-Patterns to Avoid

| ❌ Don't                                            | ✅ Do Instead                                                             |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| Add generic advice ("write clean code")             | Add repo-specific rules ("use `pnpm`, not `npm`")                         |
| Create skills for one-off tasks                     | Create skills for tasks you'll do again                                   |
| Let AGENTS.md grow unbounded                        | Prune stale entries, move procedures to skills                            |
| Write vague skill steps ("figure out what's wrong") | Write specific steps ("run `npm test`, read the first failing assertion") |
| Create a skill around a tool                        | Create a skill around a job to be done                                    |
| Start with shared/global skills                     | Start repo-local, promote when pain repeats                               |

---

## Quick Reference: The Compounding Loop

```
Work on task
    ↓
Complete task
    ↓
Reflect: Did I wander? Get corrected? Repeat a workflow? Discover a gotcha?
    ↓
    ├── Navigation miss     → Update Codebase Map
    ├── Behavior correction → Add to Local Norms / Guardrails
    ├── Repeated workflow   → Create a Skill
    ├── Surprise discovery  → Add to Patterns & Gotchas
    └── Nothing notable     → Move on
    ↓
Next task starts from a better baseline
```

> _"The most valuable skill is the habit of watching yourself work."_
> Each improvement makes future improvements easier. That's how agents compound.
