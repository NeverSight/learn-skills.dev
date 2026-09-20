---
name: read-lore
description: >-
  Load and present an existing Lore Work from refs/lore/<work-id> with
  structured document order and a handoff summary. Use when the user asks to
  read lore, load lore, show lore, summarize lore, onboard to a work, or
  wants lore context or a handoff.
---

# read-lore

Load and present an existing Lore Work for onboarding. read-lore resolves
which Work to read, shows documents in a structured order, previews recent
lore history, and synthesizes a handoff summary.

Lore is read via `git show` on the lore ref — nothing is written to the
working tree.

Protocol reference: [references/protocol.md](references/protocol.md) and Lore Work
`refs/lore/git-lore` (`git show refs/lore/git-lore:spec.md`) for full
specification. This skill's Lore Work: `refs/lore/read-lore`.

## When to use

- Onboarding to a piece of work (fresh agent or human)
- User asks to "read lore", "load lore", "show lore", or "summarize lore"
- User wants lore context, a handoff, or to understand what has been decided
- create-lore suggests read-lore after creating a Work

Do **not** use when:

- No Lore Work exists yet → create-lore
- User wants to **change** Lore → edit-lore
- Work may exist only on remote → sync-lore first, then read-lore

## Read modes

Determine mode from the user's request:

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| Full | Default | Structured read + handoff summary |
| Document | User names a file | That file only via `git show` |
| Summary | "summarize lore", "handoff" | Handoff summary without full document dump |
| History | "lore history", "lore log" | `git log` only |

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Resolve work-id
- [ ] Step 2: Verify Work exists
- [ ] Step 3: Show metadata and document list
- [ ] Step 4: Show recent lore history
- [ ] Step 5: Read documents (mode-dependent)
- [ ] Step 6: Synthesize handoff summary
- [ ] Step 7: Suggest next skill if appropriate
```

### Step 1: Resolve work-id

Resolve in order:

1. **Explicit argument** — user provides `work-id` (e.g. "read lore for git-lore")
2. **Branch config**:

```bash
BRANCH=$(git branch --show-current)
git config --get "branch.${BRANCH}.lore"
```

3. **Disambiguation** — list Works and ask:

```bash
git for-each-ref refs/lore --format='%(refname:short)'
```

If branch config points to a Work that does not exist locally, report the
stale config and fall through to disambiguation.

If zero Works exist, suggest create-lore.

### Step 2: Verify Work exists

```bash
WORK_ID=<work-id>
git rev-parse "refs/lore/${WORK_ID}"
```

If this fails:

- Remote may have the Work → suggest sync-lore
- Work may not exist → suggest create-lore

### Step 3: Show metadata and document list

```bash
REF="refs/lore/${WORK_ID}"
COMMIT=$(git rev-parse "$REF")
git ls-tree -r --name-only "$REF"
```

Report to the user:

- Work id: `<work-id>`
- Ref: `refs/lore/<work-id>`
- Latest commit: hash and `git log -1 --format='%s' "$REF"`

### Step 4: Show recent lore history

```bash
git log --oneline -10 "refs/lore/${WORK_ID}"
```

Default depth: 10 commits. Increase only when the user asks for full lore
history.

Do not dump full commit diffs by default. If the user wants last-change
detail:

```bash
git diff "refs/lore/${WORK_ID}~1" "refs/lore/${WORK_ID}"
```

Skip this step in **History** mode when document content is not needed, or
when the user only wants a **Summary**.

### Step 5: Read documents

Skip in **History** mode. In **Summary** mode, read enough to synthesize the
handoff (at minimum `plan.md`, `decisions.md`, `questions.md` if present).

#### Structured read order

When reading all documents, follow this priority. **Skip missing files
silently** — there is no fixed taxonomy.

| Priority | File | Role |
|----------|------|------|
| 1 | `plan.md` | Current direction and next steps |
| 2 | `decisions.md` | Settled choices |
| 3 | `questions.md` | Unresolved items |
| 4 | `spec.md` | Technical specification |
| 5 | `investigation.md` | Research and alternatives |
| 6 | `architecture.md` | System design |
| 7 | `handoff.md` | Curated handoff (if present) |
| 8 | Other | Remaining files, alphabetical |

Read each present file:

```bash
git show "refs/lore/${WORK_ID}:plan.md"
```

Present each document under a clear heading — do **not** concatenate all
files into one unstructured block.

#### Read specific document

In **Document** mode, or when the user names a file:

```bash
git show "refs/lore/${WORK_ID}:<path>"
```

Verify the path exists in the lore tree before reading.

### Step 6: Synthesize handoff summary

Skip in **Document** and **History** modes unless the user also asked for a
summary.

After reading structured content, produce a concise handoff:

```markdown
## Lore handoff: <work-id>

**What:** [What this work / project is — 1–2 sentences]
**Why:** [Why it exists / problem being solved]
**Decided:** [Key settled choices — bullet list]
**Rejected:** [Approaches ruled out and why — bullet list, if any]
**Next:** [Immediate next steps from plan.md or obvious gaps]
**Open:** [Unresolved questions from questions.md — bullet list, if any]
```

Rules:

- Base the summary on **lore content only**, not conversation history
- If a section has no content in Lore, say "Not recorded in Lore"
- Do not invent detail not present in the lore documents
- Keep it concise — this is a handoff, not a transcript

The handoff summary is generated at read time. It is not stored in Lore
unless the user later curates `handoff.md` via edit-lore.

### Step 7: Suggest next skill if appropriate

| Situation | Suggest |
|-----------|---------|
| Lore stale or missing context | edit-lore |
| Work not found locally, remote may have it | sync-lore |
| User wants to change Lore | edit-lore |
| No Works exist | create-lore |

read-lore does not call other skills — it only suggests them.

## Examples

### Default read on current branch

Branch `skills/read-lore` with `branch.skills/read-lore.lore = read-lore`:

1. Resolve work-id → `read-lore`
2. List documents: `plan.md`, `spec.md`, `questions.md`
3. Show lore history (2 commits)
4. Read documents in structured order
5. Synthesize handoff summary

### Read protocol Lore

User: "read lore for git-lore"

```bash
WORK_ID=git-lore
git show refs/lore/git-lore:plan.md
git show refs/lore/git-lore:decisions.md
# ... structured order for remaining files
```

Handoff covers what git-lore is, why it exists, key decisions, and next steps.

### Summary only

User: "summarize the lore"

Read `plan.md`, `decisions.md`, `questions.md` (minimum), produce handoff
summary without dumping full `spec.md` or `investigation.md` unless needed
for accuracy.

### Specific document

User: "show me the lore spec"

```bash
git show refs/lore/read-lore:spec.md
```

### Stale branch config

```bash
$ git config --get branch.feature-x.lore
old-work
$ git rev-parse refs/lore/old-work
fatal: Needed a single revision...
```

Report stale config. List available Works and ask which to read.

### No lore exists

```bash
$ git for-each-ref refs/lore --format='%(refname:short)'
```

Empty output → suggest create-lore.

## Verification

After reading, confirm:

```bash
git status
```

Working tree must remain clean — read-lore does not checkout lore files.

## Non-goals

- No working-tree checkout of lore files
- No lore modification (edit-lore)
- No fetch from remote (sync-lore)
- No multi-work reads in a single invocation
- No automatic AI summarisation beyond structured presentation
- No executable or helper scripts
