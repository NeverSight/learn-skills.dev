---
name: learning-save
description: Saves durable knowledge from a Codex chat, conversation, source, rough note, synthesis session, or long-running thread into the user's established knowledge base or an explicitly named destination. Use when the user wants to roll up, archive, unpin, distill, preserve, route, or make context retrievable. Do not use for ordinary code or workflow handoff.
---

# Learning Save

Long chats are caches. Durable artifacts are memory.

Use this skill to compress what should survive, route it to its owning surface, and reduce dependence on conversation history.

## Place in the learning workflow

Use `/learning-save` to preserve useful research or conversation knowledge while it is fresh. The user's global research-capture rule may invoke it automatically; the destination's standing permission determines which writes are allowed. Its output is a sourced, retrievable KB artifact or a justified skip when there is nothing new worth keeping.

Saving a finding does not make it govern future work. When an accepted lesson needs to change a project's decisions or checks, use `/learning-loop`. When evidence supports reuse beyond that project, use `/learning-playbook` to assess the candidate before promotion. Keep substantive project decisions at their owners and point to them from the KB.

## Owner And Oracle

Before writing, name:

- owner surface
- allowed writes
- forbidden writes
- source material being compressed
- done gate
- first real check

Ask only when the owner surface or write authorization cannot be inferred safely. Otherwise state one concrete routing assumption and proceed.

## Destination

Default to the user's established local knowledge base, even when the chat starts in a code repository. Resolve its path from a user-supplied location, personal instructions, or workspace routing; do not assume a universal filesystem path. When that KB is available, hand off directly without asking the user to choose the destination again.

If no KB is established or it is unavailable, ask the user to select a local folder before writing. Do not silently substitute a project repository or temporary directory.

## Route

For an Obsidian KB, resolve the live content root from its owner instructions before choosing note paths. A tooling repository may contain the vault in a nested folder; the checkout root is not necessarily the vault root. Follow the owner's retrieval and internal-link conventions.

Read the owner's local instructions, applicable `AGENTS.md`, schema, and completion checks before writing. Prefer an existing artifact that already owns the idea. Otherwise create the smallest durable artifact the owner accepts.

Use another destination when the user explicitly names it. Preserve existing project contracts at their owners and link them from the KB rather than copying their authority. Do not make a temporary file the final capture.

## Preserve

Keep:

- the durable claim
- source pressure: what makes the claim sharp, resistant, or non-obvious
- provenance: chat/source/file/link/date/path
- live distinction: what this is not and what it must not collapse into
- open questions
- retrieval hook: exact title, link, index entry, or search phrase

Drop:

- generic chat summary
- assistant self-narration
- details that only help another agent resume workflow
- duplicate copies of PRDs, plans, notes, issues, commits, or diffs
- secrets, credentials, and unnecessary personal data

## Output Shapes

Pick one shape.

### Source Capture

Use when the source itself must survive before interpretation.

Preserve the required source body and provenance under the owner's schema.

### Claim Or Insight

Use when one strong idea should survive.

Include:

- claim
- why it matters
- provenance
- evidence
- counterpressure or caveat
- open questions

### Synthesis Note

Use when several sources or threads need integration.

Include:

- synthesis thesis
- source cluster
- important distinctions
- tensions
- implications

### Existing Artifact Update

Use when an existing artifact already owns the idea.

Update it instead of creating a duplicate.

## Long Codex Chat Compression

When the user wants to archive, unpin, or stop relying on a long chat, capture durable knowledge only. Do not turn the artifact into a next-session briefing.

## Completion

Before calling done, run the owner's required checks and inspect the written artifact.

Report:

- artifact path
- owner surface
- what survived
- what was intentionally not copied
- registry or index update, if required
- retrieval hook
- whether the original chat can now be archived safely

## Anti-Patterns

Do not:

- dump a whole chat transcript into a synthesis artifact
- create temp files as the final artifact
- smooth away the user's sharp language or source pressure
- create a new artifact when an existing one owns the idea
- treat workflow handoff and knowledge capture as the same operation
- duplicate material already captured elsewhere
- claim done without checking the owner's conventions
