---
name: write-prd
description: Turn a vague idea into a grounded PRD through user interview, codebase exploration, and Socratic drafting. Passes through the grill-me ambiguity gate before exit. Use when the user wants to write a PRD, spec out a feature, turn a meeting transcript into a plan, or says "write-prd", "write a PRD", "spec this out", "let's PRD this", "turn this into a spec". Also invoked by workflow orchestrators like bugbook:flow to produce the spec phase of a larger workflow.
---

# Write PRD

Turn vague ideas into grounded PRDs. Not aspirational prose — a spec that captures what exists, what should exist, and everything an agent with zero prior context would need to execute without asking questions.

Inspired by Matt Pocock's `write-a-prd` and Ouroboros's specification-first workflow. Synthesizes codebase exploration, Socratic interview, and the grill-me ambiguity gate into a single skill.

---

## Contract

**Input:** the conversation history, any context the caller has pre-loaded (e.g., bugbook:flow may pre-load project context pages before invoking), and whatever the user says.

**Output:** a markdown PRD with the structure below. Written to a destination the caller specifies, or default `docs/prds/<slug>.md` if invoked standalone. The PRD content also remains in the conversation so the caller can post-process it.

**What this skill does NOT do:** reach into Bugbook, Notion, Linear, or any external system directly. It only reads files on disk and context already in the conversation. Callers that want to persist the PRD to an external system (Bugbook page, GitHub issue, Linear ticket) do that themselves after this skill returns.

**Composition chain:** `caller` → `write-prd` → `grill-me` → ambiguity report → return PRD to caller.

---

## Phases

Skip any phase that's already been done by a caller. For example, if bugbook:flow has already pulled Bugbook project context into the conversation, you don't need to re-explore that context.

### Phase 1: Context load

Read what's already available before asking questions or exploring.

- Scan the conversation for existing context (prior discussion, meeting transcript, pasted error, caller-injected context)
- Read any files the user has already referenced
- Identify: what's the rough shape of the problem? What does the user already know? What's the caller's context?

If the conversation is rich with context (transcript, detailed description), skip to Phase 3 — you don't need to ask the user to restate.

If the conversation is thin ("I want to add X"), ask ONE broad question: "Tell me the problem you're solving and any ideas you already have about the solution." Then wait.

### Phase 2: Codebase exploration

Before writing a spec, understand what exists. This is what separates a grounded PRD from an aspirational one.

Ask the user: **"What area of the codebase does this touch?"** Accept a directory, a file list, or "not sure, help me find it".

Then read the relevant files. Look for:

- **Existing patterns** — how are similar features implemented? What conventions does the surrounding code follow?
- **Constraints** — what isn't obvious from the file list? (e.g., "the editor uses a LazyVStack so virtualized blocks don't support X", "the existing pattern uses `@Observable`, not `@ObservableObject`")
- **Related code** — are there sibling files, shared utilities, or existing abstractions this feature would build on?
- **Prior art** — has something similar been tried before? Check git log for the files involved.

This takes 5-10 minutes and prevents the #1 failure mode: specifying work that conflicts with how the codebase actually works.

**Time budget:** don't exhaustively map the codebase. Read 5-10 files max. If the scope is huge, ask the user which slice to explore first.

### Phase 3: Socratic interview

Now that you understand the problem and the existing code, interview the user to resolve what's unclear.

**One question at a time.** Provide your recommended answer alongside each question.

Walk down each branch of the design tree, resolving dependencies one-by-one. Target these categories:

- **Goals** — what's the specific outcome? How will we know it's done?
- **Scope** — what's explicitly NOT in scope? What's tempting to add that we shouldn't?
- **Approach** — which pattern should we follow? Why that over alternatives?
- **Constraints** — what did the codebase exploration reveal that shapes the approach?
- **Open questions** — what genuinely doesn't have an answer yet?

**Interview discipline:**

- If a question can be answered by reading more code, read instead of asking
- If the user gives a vague answer, push for specifics ("fast" → "under what latency?")
- If the user says "I don't know, what do you think?", give your recommendation and ask if it matches their intent
- Don't interview forever — once you have enough to draft, stop

### Phase 4: Draft the PRD

Write the PRD using this structure. This format is Max Forsey's proven spec format; it emphasizes executable clarity over narrative polish.

```markdown
# <Feature Name>

## Goals

<2-4 sentences. What we're trying to accomplish. Specific enough that "done" is distinguishable from "almost done".>

## Requirements

<Specific behaviors or capabilities that must exist when this is done. Be concrete —
"users can search transcripts with p95 latency under 100ms" not "improve search".>

- [ ] <requirement 1>
- [ ] <requirement 2>
- [ ] <requirement 3>

## Non-Goals

<What we're explicitly NOT doing. This prevents scope creep during execution. Be specific —
"not changing the data model", "not adding new navigation entries", "not handling offline mode".>

## Constraints

<Technical or design constraints discovered during codebase exploration. Things like:
"the editor uses a LazyVStack so virtualized blocks don't support X",
"the existing pattern uses @Observable, not @ObservableObject",
"all new .swift files must be added to Bugbook.xcodeproj/project.pbxproj".>

## Approach

<High-level implementation strategy. Which patterns to follow, which areas of the codebase
to modify, rough order of operations. Not pseudocode — just enough that an agent knows the direction.>

## Open Questions

<Anything unresolved. Tag each with who needs to answer:
- user decision — needs the user to pick
- needs exploration — needs more codebase investigation
- blocked on external — waiting on something outside our control.>

## Discoveries

<Initially empty. Populated by agents during execution as they find unexpected things.
This section is the knowledge loop — each entry includes date, ticket/context, what was found,
and implications for future work.>
```

**Draft discipline:**

- Present the PRD in chunks (2-3 sections at a time), not a wall of text
- After each chunk, ask: "Does this match what you want? Anything to adjust?"
- If the user pushes back, revise on the spot — don't defer to a later review
- Keep the language concrete. Avoid "robust", "scalable", "elegant", "clean" — those are decorations, not specs

#### Concrete example of what "good" looks like

A small feature PRD, for a hypothetical "add a Cmd+K shortcut to focus the search bar":

```markdown
# Cmd+K focuses search bar

## Goals

Give the user a one-key way to jump to the search bar from anywhere in the app.
The existing path (click the search field in the sidebar) works but breaks flow
when the user is in the middle of a note. This removes the context switch.

## Requirements

- [ ] Pressing Cmd+K anywhere in the app focuses the search bar
- [ ] If the search bar isn't visible (sidebar collapsed), show the sidebar first, then focus
- [ ] The caret lands at the end of any existing search text (not selected, not cleared)
- [ ] Escape from the focused search bar returns focus to whatever had it before
- [ ] The shortcut is shown in the Help menu alongside other navigation shortcuts

## Non-Goals

- Not changing the search bar's visual appearance
- Not adding a command palette (this is just a focus shortcut, not Cmd+K as in VS Code's command menu)
- Not adding Cmd+K shortcuts for any other UI element — this PRD is for the search bar only

## Constraints

- Cmd+K is currently unbound in Bugbook per a grep of `KeyboardShortcuts` usage — no conflict
- Focus management in SwiftUI requires @FocusState at the parent view level; the search bar is a child of ContentView, so the @FocusState will live there
- The sidebar-collapsed case means we need to listen for the shortcut at a higher level than the sidebar itself — probably at ContentView

## Approach

1. Add a `@FocusState` for the search field in ContentView
2. Add a `.keyboardShortcut("k", modifiers: .command)` to a hidden button or on ContentView itself
3. In the handler, first ensure the sidebar is visible (check `sidebarVisibility` state), then set the focus state to `.searchField`
4. For the Escape return-focus behavior, track the previous focus on entry and restore on `.onSubmit` or escape

Follows the existing pattern in `TicketListView` where keyboard shortcuts are attached at the container level, not the input level.

## Open Questions

- Should Cmd+K also clear the current search, or preserve it? (user decision — default: preserve)
- Does the shortcut need to work when a modal sheet is open? (needs exploration of modal focus behavior)

## Discoveries

<empty — will be populated during execution>
```

Notice what's concrete in this PRD:
- Requirements are observable behaviors, not aspirations
- Non-Goals explicitly rule out scope creep (the command-palette confusion)
- Constraints cite actual codebase facts (grep result, SwiftUI focus management pattern)
- Approach references an existing pattern by name (`TicketListView`)
- Open Questions tag who decides and what needs investigation

That's the target quality bar.

### Phase 5: Grill gate

Before finalizing, invoke the `grill-me` skill in spec mode against the drafted PRD.

grill-me will:
1. Walk the PRD section by section
2. Surface ambiguous scope, unverified assumptions, vague acceptance criteria, and missing Non-Goals
3. Produce an ambiguity report with per-dimension scores
4. Apply the spec-mode threshold (0.2)

If the ambiguity report is below threshold, proceed to Phase 6. If above, either iterate on the PRD until it passes or let the user override with "enough".

The ambiguity report gets appended to the PRD as a new section before output.

**If `max:grill-me` is not available** (e.g., invoked in an environment without the max plugin), fall back to a passive self-review: read the PRD aloud to yourself, flag anything vague, ask the user one clarifying round, and exit.

### Phase 6: Output

Write the PRD to the destination:

- **Standalone invocation:** write to `docs/prds/<slug>.md` where `<slug>` is a kebab-case version of the feature name. Create the directory if needed.
- **Caller-specified destination:** if the caller passed a destination (as conversation context or a parameter), write there instead.
- **No destination at all:** leave the PRD as conversation content only. The caller (or the user) decides where to persist it.

Print the final PRD path and the ambiguity report to the terminal:

```
✓ PRD written to docs/prds/sidebar-drag-fix.md
Ambiguity: 0.12 (below 0.2 spec threshold)
```

Return control to the caller.

---

## Composition notes

**When called by bugbook:flow:**

bugbook:flow pre-loads Bugbook project context into the conversation (via `bugbook search` + `bugbook context`), then invokes `max:write-prd`. write-prd skips Phase 1's conversation scan (already done) and proceeds directly to Phase 2 exploration. After Phase 6, bugbook:flow captures the PRD content and writes it to a Bugbook project context page using `bugbook page create`.

**When called standalone:**

User says "write-prd" or "spec this out". write-prd runs all phases from scratch. Output goes to `docs/prds/<slug>.md`.

**When called by another future orchestrator (e.g., Notion adapter):**

Same contract. The caller pre-loads Notion page context into the conversation, invokes write-prd, and post-processes the output to a Notion page. write-prd doesn't know or care about Notion.

---

## Anti-patterns

- **Skipping codebase exploration.** The whole point of this skill is grounding the PRD in reality. If you skip Phase 2, you produce specs that sound good but miss existing constraints. Don't.
- **Treating the interview as a questionnaire.** Grill-me is a stress-test, not a script. Ask follow-ups. Push on vague answers.
- **Writing the PRD before the interview is done.** You'll have to rewrite sections as new info comes in. Finish understanding first, then draft.
- **Asking the user to validate a wall of text.** Chunk the PRD into sections and get incremental approval. Review fatigue is real.
- **Reaching into external systems.** If you find yourself wanting to call `bugbook query` or `gh issue create`, stop — that's the caller's job, not yours. You output markdown; the caller persists.
