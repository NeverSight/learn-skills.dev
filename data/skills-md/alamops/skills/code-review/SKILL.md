---
name: code-review
description: (alamops) Performs a thorough, read-only code review on any source of changes — a pull request, a git diff, uncommitted edits in the working tree, recent commits on the current branch, or code that was just produced or discussed in the conversation. Flags bugs, security issues (tenant isolation, authz gaps, atomicity, retry safety, multi-step flow completeness, RLS / row-policy self-recursion), performance issues (in-memory aggregation, sequential fan-out, partial-period comparisons), consistency issues (including schema ↔ code column-reference drift), and blast-radius gaps. Returns structured findings (category, severity, file, line, suggestion) without modifying any code. Use whenever the user asks for a code review, PR review, diff review, feedback on pending or recent changes, or a critique of code just written in this session.
---

# Code review

A read-only review skill: produce structured findings, never edit code. Tone: friendly coding teammate, concise.

## Pick the review target

Before reviewing, identify *what* you are reviewing. The skill applies the same rigor regardless of source — only the discovery step changes:

| Trigger | How to gather the diff |
| --- | --- |
| User names a PR (URL or number) | Fetch PR metadata + diff (e.g., `gh pr view <n>`, `gh pr diff <n>`). |
| User asks to review "this branch" / "my changes" / "what I'm about to push" | `git status`, `git diff <base>...HEAD`, `git log <base>..HEAD --stat`. Default `<base>` to `origin/main` (or `origin/master`); fall back to `main`. |
| User asks to review uncommitted / pending / staged work | `git status`, `git diff` (unstaged) and `git diff --cached` (staged). |
| User asks to review "recent commits" / "the last commit" | `git log -n <N> --stat`, `git show <sha>` for each. |
| User asks to review code we just wrote / discussed in this conversation | Use the in-conversation edits and tool results. Re-read the modified files from disk if it has been a while or if context may have been compacted. |
| Ambiguous ("review my code") | Ask once: "Review the open PR, the uncommitted changes in your working tree, the diff against `main`, recent commits, or the code we just wrote together?" Then proceed. |

## Rules

1. **Read-only.** Even if an editing tool is available, do not modify code. Surface fixes, refactors, and tests as findings, not commits.
2. **Promise discipline.** Do not defer work you can do now. If you spot something, write it as a finding immediately rather than "I'll come back to this."
3. **Complete the entire review.** Walk every changed file. Don't stop after the first few hits.
4. **Question, don't assume.** If you're unsure whether something is a bug, frame it as a question. Don't fabricate certainty.
5. **Explain the why.** Every finding states what the issue is and why it matters. No bare assertions.
6. **No positive findings.** Findings are for problems. Do *not* emit `[info] Positive: …` items, do *not* dress up "this is fine" or "nice touch" observations as findings, and do *not* add `info` entries that boil down to "this code is good / consistent / well-scoped / harmless." If something is clean, it goes in the overall summary as a one-line acknowledgement — not as its own finding block. When in doubt, ask: "Is there an action the author should take?" If no, it is not a finding.

## Review efficiency

- **Shallow-first.** Start with the cheapest signal: PR title/description/linked issues, commit messages, `git status`, or the user's stated intent in the conversation. Look at full diffs and file contents *after* you know what changed and why.
- **Use the right scope.** Don't review files that weren't touched. For working-tree reviews, the scope is `git diff` + `git diff --cached`; for branch reviews, `git diff <base>...HEAD`; for in-conversation reviews, the files actually edited this session.
- **Skip artifacts.** If a changed file looks generated, bundled, or minified, review the source-of-truth file instead.
- **Verify before recommending.** If web search is available, confirm current stable versions, API shapes, and best practices before suggesting a library, flag, or pattern.

## Review checklist

Copy this into your response and check items off as you progress:

```
Review progress:
- [ ] Review target identified (PR / branch diff / working tree / recent commits / in-conversation edits)
- [ ] Intent gathered (PR description, commit messages, conversation context, or stated goal)
- [ ] All changed files reviewed
- [ ] Security swept (tenant isolation, authz, atomicity, retry, flow completeness, orphaned state, RLS self-recursion)
- [ ] Performance swept (in-memory aggregation, fan-out, duplicate scans, period comparisons)
- [ ] Consistency swept (enums, validation, business-rule duplication, contract alignment, schema↔code column-reference drift)
- [ ] Blast radius traced for every modification (callers, sibling paths, downstream flows)
- [ ] Findings logged with category, severity, file, line, suggestion
- [ ] Overall summary written (counts, top issues, verdict)
```

## What to look for

### Code quality
Clean, readable, maintainable code. Names that describe intent.

### Security

- **Injection / XSS / CSRF.**
- **Tenant isolation.** Do operations on tenant-scoped resources include the org/company/team filter? Are privileged or unscoped code paths properly bounded? Can a user from one tenant read or affect another tenant's resources?
- **Authorization gaps.** Are destructive operations (delete, revoke, disconnect, status change) guarded by ownership checks before executing?
- **Information disclosure.** Do error responses leak stack traces, internal errors, or internal URLs? Is raw error detail returned to clients? Are dynamic values escaped before being rendered as markup?
- **Atomicity.** Are security-critical state transitions (OAuth state consumption, lock claims) atomic? Or do they read-then-write with a TOCTOU window?
- **Timeouts.** Do all external HTTP calls have explicit timeouts?
- **Retry safety.** Are non-idempotent operations (writes, creates, side-effecting tool calls) retried only on connection-level errors — never on server errors?
- **Stateless runtime assumptions.** Does the code rely on module-level state, in-memory queues, or background timers for durable state in a serverless/edge environment? These are lost between invocations. Does service-worker code make authenticated requests without explicit token management?
- **Multi-step flow completeness.** Do flows spanning multiple requests / redirects / pages (auth, payment, invitation) have a handler at every redirect destination? Does every temp token / authorization code have a consuming endpoint? Do callbacks check authorization, membership, *and* invitation — not just the happy-path exchange?
- **Orphaned state cleanup.** When an early step creates durable state (auth sessions, tokens, records) and a later step fails, is the early state rolled back? On password change, are other sessions invalidated? On feature disablement, are dependent records cleaned up?
- **Source-of-truth verification.** Is auth checked against the actual provider (a real session/token validation call) — not proxies like cookie-name existence, header presence, or cached state? Does route protection verify assurance levels (post-MFA) and app-layer authorization (org membership, role)?
- **RLS / policy self-recursion.** For any row-level-security or row-policy definition, does the `USING` / `WITH CHECK` clause query the *same table the policy protects* (directly, or transitively via a view)? Postgres throws `42P17 infinite recursion detected in policy for relation "<T>"` at query time, often only on the read path that triggers it — easy to ship undetected. The fix is to wrap the membership check in a `SECURITY DEFINER` helper function so the inner lookup bypasses RLS. **Also**: when adding a new query, RPC, or join that touches table T, scan T's *existing* policies for self-referencing `EXISTS (SELECT … FROM T …)` patterns even if T is not in this diff — the recursion only manifests when something queries T, so a clean new RPC can still detonate an old policy.

### Performance

- **In-memory aggregation.** Are analytics / reporting / dashboard endpoints loading large raw datasets into memory just to compute totals, counts, or groupings? Push aggregation to the data layer (using its native aggregation primitives) instead of materializing thousands of records. Fetching huge result sets to derive a summary is a critical perf bug.
- **Duplicate scans.** Do multiple functions fetch the same data slice (same org, same date window) independently? Share one fetch or pre-aggregate.
- **Partial vs. full period comparisons.** Are trend calculations comparing a partial (in-progress) period against a full (completed) prior period? Misleading metrics.
- **Sequential fan-out.** Does one event trigger N sequential async operations in a loop? Use bounded concurrency / parallelism primitives instead of awaiting each call. Hoist invariants out of loops.

### Testing
Are tests adequate? Do they cover edge cases, error paths, and the new behavior introduced in this change?

### Documentation
Are non-obvious decisions, invariants, or workarounds documented where a future reader will need them?

### Error handling
Is failure handled, or punted upward without context?

### Consistency

- **Enum / constant alignment.** Do UI filter values, dropdown options, and status enums match what the backend actually writes? If a new status, type, or category was added in backend code, are all corresponding frontend lists updated?
- **Data-source consistency.** Do different pages showing the same concept (e.g., "active users", "pending invitations") use the same filters and conditions, or do some include/exclude states differently?
- **Backend → frontend contract.** When the backend returns pagination, sorting, or filtering metadata, does the frontend consume it? Are backend capabilities wired through to the UI, or do they get dropped at the boundary?
- **Redundant event paths.** In real-time flows, does one logical event cause the same mutation twice? (e.g., server broadcasts a counter update *and* the client increments optimistically — double-counting.) Each metric needs exactly one source of truth.
- **Validation consistency.** Do sibling endpoints (GET/POST/PATCH/DELETE on the same resource) use the same validation approach, or does one fall back to raw type assertions? Are validations semantically correct (e.g., hour values 0–23, not just two digits)?
- **Single source of truth for business rules.** Is the same rule (password requirements, access criteria) implemented in multiple places (client indicator + server schema, frontend form + API validation)? Do they enforce identical constraints? Can the UI show "valid" while the API rejects?
- **Mutual-exclusion / co-dependency.** Do schemas marking fields optional enforce that at least one of a mutually-exclusive group is present? (e.g., password OR an OAuth provider required — not both optional with no refinement.) Look for cross-field validation / refinement.
- **Column-reference drift (schema ↔ code).** When client / server code names a column — `.select('a, b, last_message_at')`, `.eq('status', …)`, `.order('created_at')`, raw SQL strings, ORM field refs — does the column actually exist in the migration history? Grep the migrations for each referenced column name. A missing column produces a runtime `42703 column "X" does not exist` that unit tests typically miss (they mock the DB). Conversely: when a diff *adds* a column, is something on the other side reading it, or is it stranded? This catches the "client merged before the migration" and "migration merged but feature shipped without the column wired up" failure modes.

### Blast radius (CRITICAL)

The highest-impact bugs are not in the code that was changed — they are in the code that **should have been changed but wasn't**. For every modification:

- What else calls or consumes the changed function, interface, or type? Are all callers updated?
- What flows (user flows, background jobs, event handlers, scheduled tasks) does this code participate in? Does the change break any of them?
- What other steps in the same flow assume the old behavior? Walk the pipeline forward and backward.
- What error handlers, retry paths, and fallback logic carry assumptions from the old happy path that are now wrong?
- What state, references, caches, or IDs become stale after this change?
- Are there sibling code paths (tools, handlers, services) handling the same concern? Do they all implement the change consistently? (e.g., if one tool refreshes expired tokens, do *all* similar tools?)
- **Flag any change where blast radius wasn't fully traced.**

## Workflow

1. **Identify the target** using the table above. If unclear, ask once.
2. **Gather intent.** PR description + linked issues, commit messages, the user's stated goal, or the conversation thread that produced the code. Note what the change is *trying* to do — half of code review is checking whether the change actually accomplishes its goal.
3. **Skim the changed-file list and line counts.** Identify the most-impacted files.
4. **For each changed file, walk the diff** and apply the categories above. When reviewing in-conversation edits, re-read the file from disk — don't trust your memory of the patch.
5. **Trace blast radius** for every meaningful change.
6. **Log each issue** as a finding (format below).
7. **End with an overall summary.**

## Finding format

Each finding:

```markdown
### [<severity>] <short title>

- **Category:** Bug | Security | Performance | Style | Suggestion | Improvement
- **File:** `path/to/file.ts:LINE`

<description: what is wrong and why it matters>

**Suggestion:**

<actionable fix, with snippet if useful>

\`\`\`ts
// optional snippet
\`\`\`
```

Fields:

- `category`: `Bug` | `Security` | `Performance` | `Style` | `Suggestion` | `Improvement`
- `severity`: `critical` | `high` | `medium` | `low` | `info`
- `description`: self-contained Markdown prose
- `suggestion`: actionable; optional but strongly preferred
- `file_path`: relative to repo root
- `line_number`: specific line if applicable
- `code_snippet`: relevant snippet, if applicable

### Examples

```markdown
### [critical] Missing tenant scope on resource listing

- **Category:** Security
- **File:** `path/to/listing-handler:LINE`

The listing operation returns records for all tenants — it neither accepts nor applies a tenant identifier. Any authenticated user can read records belonging to any other tenant, a tenant-isolation breach.

**Suggestion:**

Require the caller to pass the tenant scope, resolved from the authenticated session at the request boundary — not deep inside callers, where it is easy to forget.
```

```markdown
### [high] Sequential fan-out in notification broadcast

- **Category:** Performance
- **File:** `path/to/broadcast-handler:LINE`

The handler iterates over recipients and awaits each external call serially. For a list of N recipients, this is ~N× slower than necessary and risks exceeding the function's wall-clock timeout.

**Suggestion:**

Use bounded parallelism — fire requests concurrently with a concurrency limit. Hoist invariants (template / payload construction) outside the loop so they aren't recomputed per recipient.
```

## Overall summary

End every review with:

- **Counts by severity** — `critical` / `high` / `medium` / `low` / `info`.
- **Top must-fix items** — highest-severity findings, named explicitly. Include as many as truly warrant attention (could be one, could be several); don't pad to hit a count, don't truncate to fit one. Omit this line if there are no findings worth surfacing here.
- **What's good (1–3 lines max).** A short, consolidated acknowledgement of what was done well — e.g. "Test scope is tight, the action-union pattern is consistent with the file, and the rename handler is symmetric with the existing upsert." One sentence is ideal; never a list of separate "positive findings."
- **Verdict** — `approve` / `request changes` / `comment`.

If the review surfaced **zero findings**, skip the counts table and the must-fix line. Lead directly with a 2–4 sentence summary of what the change does and what was done well, then state the verdict. Do not pad the response with empty sections or fabricated nits.
