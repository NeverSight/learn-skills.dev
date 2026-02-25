---
name: eve-skill-distillation
description: Distill repeated work into Eve skillpacks by creating or updating skills with concise instructions and references. Use when a workflow repeats or knowledge should be shared across agents.
---

# Eve Skill Distillation

Use this workflow to turn repeated patterns into reusable skills.

## When to distill

- A workflow has repeated across two or more jobs.
- Knowledge would benefit other agents working on the same project.
- A failure mode keeps recurring and the fix should be encoded.

## Workflow: Orchestrate, Don't Serialize

When distilling involves multiple skills (creating several, updating a batch, or a mix), use an orchestrator pattern rather than doing everything sequentially. This protects your context budget and parallelizes independent work.

### Step 1: Capture patterns (orchestrator)

Identify all the patterns worth distilling from recent work. For each one:

- Name the repeated steps, commands, or failure modes.
- Decide: update an existing skill, or create a new one?
- Choose the target repo/pack first - is this likely to be
  - `./private-skills/` or similar for repo-specific development workflows that are not going to be imported into other projects (private)
  - `./private-eve-dev-skills/` when working in the eve-horizon repo and the skills relate to internal development of the platform itself (private)
  - `../eve-skillpacks/eve-se/`  for Eve platform work (deploy, auth, manifests, pipelines)
  - `../eve-skillpacks/eve-work/` for general knowledge work (docs, orchestration, distillation)
  - `../eve-skillpacks/eve-design/` for architecture and design thinking

### Step 2: Plan work items (orchestrator)

Create a tracked work item for each skill to create or update. Each work item description must be self-contained — a worker with no prior context should be able to execute it.

Include in each work item:
- The target file path (e.g., `eve-se/eve-auth-and-secrets/SKILL.md`)
- Whether this is a **create** or **update**
- The pattern being captured: what the skill should teach
- Any source material the worker should read (existing skills, reference docs, conversation history)
- The authoring rules (see "Skill Authoring Rules" below)

If there are housekeeping updates (README, ARCHITECTURE.md), add those as a final work item blocked until all skill work items complete.

### Step 3: Dispatch workers (parallel)

Spawn one worker per skill work item. Launch them all at once.

Each worker prompt must be self-contained. The worker has no access to the orchestrator's conversation. Include:
- The target file path to create or edit
- The pattern to capture, described in enough detail to write from
- The authoring rules below
- Existing file content to preserve (for updates)

### Step 4: Collect and finalize (orchestrator)

Wait for all workers to complete. Then:
- Update pack README and `ARCHITECTURE.md` listings if skills were added or removed.
- Verify each new/updated skill follows the authoring rules.

### Single-skill shortcut

If there's only one skill to distill, skip the orchestrator pattern and do it directly. The overhead of dispatching a single worker isn't worth it.

## Skill Authoring Rules

Every worker (or direct author) must follow these:

- **Frontmatter**: YAML with `name` and `description` only.
- **Voice**: Imperative form throughout. ("Run the command", not "You should run the command".)
- **Conciseness**: Keep SKILL.md under 5,000 words. Move long details into `references/`.
- **Teach thinking, not just steps**: Skills should help agents understand *why*, not just *what*. Include the reasoning behind workflows so agents can adapt when conditions change.
- **Structure for skimming**: Use headers, short paragraphs, and code blocks. Agents scan before they read.
- **Agent-agnostic language**: Describe *what* to do, not *which tool to call*. Say "edit the file" not "use the Edit tool". Say "spawn a background worker" not "launch a Task sub-agent".

## Recursive distillation

- Repeat this loop after each significant job.
- Merge overlapping skills instead of duplicating them.
- Keep skills current as platform behavior evolves.
- When a skill's instructions no longer match reality, update or retire it.
