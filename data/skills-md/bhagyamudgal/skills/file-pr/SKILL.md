---
name: file-pr
description: Open a GitHub pull request whose title and body a reviewer understands in one read. Use when opening a PR or publishing ready-to-publish work for review. Never open one by hand.
---

# File a pull request

A PR is read by someone who has not seen the session, the diff, or the ticket. Every bar below exists so that reader understands the change in one pass.

## 1. Check preconditions

Read the branch and the current `done` readiness card.

- **Branch.** `git rev-parse --abbrev-ref HEAD` exactly equals **Branch** in the card and satisfies the branch-naming rule in `CLAUDE.md`. A rename or switch makes the card stale and returns to `done`.
- **Readiness card.** Require the current Git card defined by `done`, including its request, currency, coverage, lane, evidence, verdict, and next-action fields. Its verdict must be `ready-to-publish`, with this skill as the exact next action. A missing field or another verdict returns to `done`. Do not reconstruct it here.
- **Publication mode.** Bind the expected PR state and draft mode to the user's publication request. When the request does not name draft publication, use `OPEN` and `isDraft: false`.

The gate is that branch, card presence, expected state, and draft mode each have a recorded result, and a failed one stops the PR.

## 2. Validate the base and resolve the issue link

Use the PR base ref and exact base remote already resolved by `done`. Refresh that recorded `<base-remote>` ref with the card's exact commands, then require its remote name, ref name, remote base-tip SHA, and merge-base SHA to match. A hard-coded or substituted remote makes the card stale. Another base state or choice returns to `done` because it changes the verified diff.

Choose exactly one issue link:

- The diff fully resolves the issue: `Closes #N`
- It resolves part of one, a sub-task of an umbrella ticket or one slice of an epic: `Refs #N`, plus one line naming which part it covers and what stays open
- It was found while investigating an issue but does not fix it: `Refs #N`, and say that in the body

Never `Closes` an issue this diff does not finish.

The gate is that the base ref, remote base tip, and merge base match the refreshed remote state, and the issue link comes from issue output rather than assumption.

### Revalidate card currency and handoff eligibility

Recompute the card instead of trusting its label:

- the active request scope matches **Originating request**;
- the active branch exactly matches **Branch**;
- the refreshed base ref, tip, and merge base match **PR base ref**, **Remote base-tip commit**, and **Merge-base commit**;
- fresh authoritative read-back of every mixed external target matches its recorded target, version, and fields; and
- the card satisfies `done`'s `ready-to-publish` rule.

Immediately before scope validation, run `done`'s alternate-index construction through `git write-tree`. Before its cleanup, run the candidate diff:

```bash
GIT_INDEX_FILE="$snapshot_index" git diff --cached --no-ext-diff <merge-base> --
```

Require the snapshot to match **Verified content snapshot**. Account every changed hunk or logical change to one verified request row. Anything outside those rows is the stop-and-ask case in `CLAUDE.md`. Then run `done`'s index cleanup.

For an initial publication card whose **Existing PR URL** is `not-applicable`, require `HEAD` to equal **Pre-verification head** and **Expected append-only commits** to be `none`. For a superseding existing-PR card, require the recorded append-only transition and post-commit content seal from `done` to match current `HEAD` and **Verified content snapshot**. Another commit is forbidden. A changed request, base, unexpected head, or content snapshot makes the card stale. Return to `done` on any mismatch.

The gate is that the recomputed request, branch, base ref and SHAs, head, snapshot, external currency, candidate diff, and `ready-to-publish` verdict all match the card.

## 3. Compose the title

Form: `<type>(<module>): <description>`. Name the module the way it reads on the board, not the way the directory spells it.

The description names what someone observes: what broke, or what is now possible. Not what you edited.

Banned as the whole description: `improve`, `update`, `handle`, `refactor`, `fix logic`, `clean up`, `various fixes`.

| Mechanism: rewrite | Outcome: ship |
|---|---|
| `fix(portions): correct filter logic` | `fix(portions): portion totals skipped orders placed after cutoff` |
| `feat(auth): update session handling` | `feat(auth): stay signed in across browser restarts` |

Name who observes the thing in the title. When the only honest answer is "someone reading the diff", the title names a mechanism, so rewrite it.

The gate is that the observer is named and no banned word stands as the description.

## 4. Compose the body

Open with two to four sentences of plain prose answering what was wrong, then what changed. Write it to make sense to someone who never opens the diff. No heading above it, never a bullet list, never optional.

Then include only the sections that carry real content:

- **What changed.** Derive one outcome-focused bullet from each verified request row. Do not infer additions from the diff.
- **How to verify.** Derive only from the evidence index's exact observations. Include applicable `not-applicable` reasons and do not invent evidence.
- **QA recording.** When the change is UI-visible and a `browser-qa` recording path is known, attach the recording at creation with `--attach <path>` only when the recording holds synthetic or redacted data, or the user explicitly approved publishing it. Backend-only changes attach nothing. Attaching requires gh v2.99.0 or later; confirm the floor with `gh --version` before any push or create side effect. When the install is older, stop back to `done` for a gh upgrade instead of publishing a UI-visible PR without its recording; publish bare only on explicit user decision, keeping the late-attach duty after upgrading.
- **Risk or scope notes.** Only when something is genuinely uncertain, migrated, or deliberately deferred.
- The issue link from section 2.

A heading with nothing under it comes out. A small PR is the lead paragraph, how to verify, and the link. Do not paste the internal readiness tables into the PR body.

The human-authored rule in `CLAUDE.md` governs the body's voice and its ban on agent, pipeline, and session references.

The gate is that the lead paragraph stands alone without the diff and every heading present carries content.

## 5. Cold-read the result

Read the composed title and body once as someone with no session context. Name a result for each bar:

- **Title.** Who observes it.
- **Lead.** States what was wrong and what changed, without the diff.
- **Terms.** Every file, flag, or term is introduced where it first appears.
- **Back-references.** No "as mentioned", "the above", "the earlier issue".
- **Verification.** Describes what ran, not what should work.
- **Voice.** No stock phrases, no em or en dashes, no agent or session references.

A bar you did not name is a bar you did not check. Rewrite a failed bar and re-read it. Never ship one as a noted exception.

The gate is that all six bars have a named result and none is failing.

## 6. Commit and open it

Resolve `$repository` through authenticated `gh repo view ... --json id,nameWithOwner` and record it as the base repository. A valid remote has ordered complete fetch and push sets from `git remote get-url --all <remote>` and `git remote get-url --push --all <remote>` whose credential-free normalized endpoints all resolve through authenticated `gh repo view ... --json id,nameWithOwner` to one common repository ID and `nameWithOwner`. An endpoint whose scheme is not HTTPS or SSH is invalid even when it resolves, since credentials would cross the wire in cleartext. When resolution follows a redirect, the final host, owner, and repository must equal the intended target or the remote is invalid. When push output mentions a redirect, resolve that final URL the same way and require HTTPS with the intended host, owner, and repository before recording the push as landed. Retain only ordered normalized sets or their digests and resolved IDs, never credentials.

When **Existing PR URL** is present, skip commit, push, and create, and load `${CLAUDE_SKILL_DIR}/references/existing-pr-reuse.md` before enumerating remotes. It holds that branch's `gh pr view` read of the existing URL, the head-identity remote match with its multiple- and zero-match dispositions, the freeze, revalidation and reconciliation requirements, what supplies the remote-head evidence without another push, and how the paginated candidate search below and any title or body edit behave on a superseding card.

Without **Existing PR URL**, inspect the current branch's configured upstream before selecting a remote. A fully configured, resolvable upstream whose branch ref matches the publication branch selects its named remote only when that remote is valid. A malformed, partial, or unresolvable configured upstream is `reconcile-required`. When upstream is authoritatively absent, enumerate valid remotes: auto-select one, use AskUserQuestion with concrete `<remote>: <nameWithOwner> (<id>)` options and pagination when multiple remain, paginating disjoint option sets when needed, and stop with `Configure one valid publication remote or bind the branch upstream, then rerun file-pr.` when none remain. The selected valid remote establishes the head repository identity and `<head-owner>`. It may equal or differ from the base repository.

Record the selected remote's ordered complete endpoint sets plus separate base and head identities as guards and invalidators. Re-enumerate immediately before each push and authoritative read-back. Any addition, removal, reorder, resolution failure, or head-repository mismatch is `reconcile-required`. The named-remote push may target its configured complete push set only while that frozen set still matches.

For an initial publication, immediately before `git-commit`, or before push when no commit is needed, repeat the branch, head, refreshed base ref and SHAs, mixed external read-back, and alternate-index snapshot checks from sections 1-2. Reuse the completed hunk accounting only when the snapshot is unchanged. A changed snapshot returns to `done`. When the verified snapshot differs from `HEAD^{tree}`, invoke `git-commit` for the verified request rows in sealed-index mode: pass **Verified content snapshot**, require the staged tree to equal it, and forbid another staging pass before commit. Record every SHA it creates. Run the append-only transition commands defined by `done`. Their ancestry, merge, and exact ordered-list criteria must all pass. A rebase, merge, or unrecorded commit returns to `done`. Add the exact ordered list to **Expected append-only commits** in the publication evidence returned with the card.

For an initial publication, before pushing, require the active branch to still equal **Branch**, freshly re-fetch every mixed external target, and require its currency to still match. Then run `done`'s post-commit content seal. Record the exact outputs of `git status --porcelain=v1 --untracked-files=all` and `git rev-parse HEAD^{tree}`. The status output must be empty and the tree SHA must exactly equal **Verified content snapshot**. Otherwise return to `done`.

For an initial publication, freeze **push-attempt SHA** only after `git symbolic-ref --quiet HEAD` equals `refs/heads/<card-branch>` and that branch ref and `HEAD` resolve to the same SHA. Query the exact remote ref and require one SHA or authoritative absence. When present, require that SHA to be an ancestor of **push-attempt SHA**. Immediately before pushing, invoke `preflight-mutations` with one inline, single-item card. Its action pushes **push-attempt SHA** to the exact ref. Its guards and invalidators include the active symbolic ref, branch-ref SHA, `HEAD` SHA, selected-remote name, ordered complete fetch and push endpoint sets and repository IDs, separate base and head repository IDs, exact remote SHA or absence, and mixed external currency. Its read-back is the exact `git ls-remote` query below. The authorized `file-pr` invocation under the global rule is the authorization source. Apply the result independently: continue only on `ready` while every invalidator matches, present `confirmation-required`, and stop on `blocked`. Re-read the active symbolic ref, branch ref, `HEAD`, and selected-remote identity immediately before the command. Any movement invalidates the attempt.

```bash
git push --force-with-lease="refs/heads/<card-branch>:<expected-remote-sha-or-empty>" "<push-remote>" "<push-attempt-sha>:refs/heads/<card-branch>"
git ls-remote --heads "<push-remote>" "refs/heads/<card-branch>"
```

After every push attempt, including a nonzero or ambiguous command result, recheck the selected-remote identity and run the exact `git ls-remote` read-back once. Record **landed-push SHA** only when that authoritative SHA equals **push-attempt SHA**. An old or unexpected SHA, unavailable read-back, or changed remote identity is `reconcile-required`: stop publication and never retry from the push command result alone.

On an initial publication, recheck the active symbolic ref, branch-ref SHA, and `HEAD` against the frozen attempt. Local movement invalidates the remaining publication even when the remote read-back succeeded. Then load `${CLAUDE_SKILL_DIR}/references/upstream-binding.md`. Reached only on this initial-publication branch, it holds the two `git config` probes that resolve the branch's upstream state, the `ABSENT`, `reconcile-required`, and authoritative-no-op classification, the guarded binding command with its read-back, and the `remote landed / upstream not bound` disposition when binding fails after the push landed.

Write the final body to a file and record its SHA-256 digest. Before deciding whether an earlier attempt exists, fetch every PR in the base repository through an authoritative paginated REST query:

```bash
gh api --paginate --slurp "repos/$repository/pulls?state=all&per_page=100"
```

Require every page to return successfully and parse completely. Any page error, unavailable continuation, or partial pagination is `reconcile-required`. Filter the complete result locally by exact `head.repo.id == <selected-head-repository-id>` and `head.ref == <head-branch>`, then map the retained records to the existing candidate fields, deriving `MERGED` from non-null `merged_at` and otherwise preserving `OPEN` or `CLOSED`.

Without **Existing PR URL**, recheck the active symbolic ref, branch-ref SHA, and `HEAD` against **landed-push SHA**, then reconcile every retained candidate across all states. Any `OPEN` candidate with a wrong head SHA or multiple open candidates is `reconcile-required`, and creation stops. One valid open candidate either matches the requested base, state, and draft mode or enters the explicit base-rebind or publication-decision path. Record its URL and return to `done` to bind it before any edit. A `CLOSED` or `MERGED` candidate at a different head SHA is historical and does not block branch reuse. A closed or merged candidate at **landed-push SHA** requires an explicit reopen, new-branch, or no-publication decision. Create only when the complete all-state result contains no open candidate and no closed or merged candidate for the current attempt. Use the same full paginated query and exact local filter when a create attempt returns no usable URL.

Require authoritative repository metadata to show that the selected head is the base repository or belongs to its fork network. An unrelated head blocks creation. Freeze one creation lane before preflight: same-repository heads use `gh pr create --head <branch>`. When the selected head repository is not the base repository, load `${CLAUDE_SKILL_DIR}/references/fork-creation-lanes.md` before freezing the lane. It holds the authenticated-user-owned and organization-owned fork lanes, the stable-ID owner-type and ownership determination that blocks any other relation, and the REST `head_repo` create form. Immediately before creating the PR, invoke `preflight-mutations` with a new inline, single-item card. Its target is the exact base repository and selected head repository. Its action records the frozen creation lane, base, head repository and branch, **landed-push SHA**, title, body path and digest, recording attach path plus its data approval, SHA-256 digest, and byte size when one is frozen, expected `OPEN` state, and expected draft mode. Its guards include both complete endpoint sets and their repository IDs, separate base and head repository IDs, the active symbolic ref, branch-ref SHA and `HEAD` still at **landed-push SHA**, the verified remote branch, recorded base tip, the complete paginated candidate result and exact filter, and confirmed absence of an open candidate or same-head-SHA current attempt. Its read-back is the exact `gh pr view` query below. Apply this result independently under the same result contract. A changed local ref, `HEAD`, endpoint set, base or head identity, creation lane, title, body path, digest, recording attach path, approval, digest, size, state, or draft mode invalidates the card. A non-ready PR card does not erase the landed push evidence.

Append `--draft` to the create command exactly when the bound draft mode is `isDraft: true`.

Same repository:

```bash
gh pr create --repo "$repository" --base "$base" --head "$head_branch" --title "$title" --body-file "$body_path" [--attach "$recording_path"] [--draft]

`--attach` needs gh v2.99.0 or later and uploads the file to GitHub, WebM included, so the body carries no local path. Video cap is 10 MB on Free plans, 100 MB on paid. Immediately before creating with `--attach`, recompute the recording SHA-256 and byte size and require both to match the frozen card values.
```

Read back every lane identically with the ten-field query below. This list is the single home; `references/existing-pr-reuse.md` and `references/fork-creation-lanes.md` cite it, never restate it:

```bash
gh pr view <pr-url> --repo "$repository" --json url,title,body,baseRefName,baseRefOid,headRefName,headRefOid,headRepository,state,isDraft
```

Execute only the frozen lane. The other examples are not fallbacks after an ambiguous result.

Require the PR `title` to equal the frozen value. When no recording was attached, require `body` to equal the frozen body exactly. When a recording was attached, require the frozen body text intact plus the uploaded recording reference, and preserve that reference through any reconciliation instead of editing the body back to the frozen bytes. Require `headRepository.id` to equal the selected head repository ID, `headRefName` to equal **Branch**, `headRefOid` to equal **landed-push SHA**, and `baseRefOid` to equal **Remote base-tip commit**. Require its URL, base name, `state`, and `isDraft` to match the publication request. Recheck the active symbolic ref, branch-ref SHA, and `HEAD` against **landed-push SHA** before accepting the publication. Record the created URL as `landed` as soon as one PR is authoritatively identified. When only title or body differs while repository, base, head, state, and draft mode still match, preflight an exact edit of that existing PR and read it back. A base mismatch enters `done`'s existing-PR rebind path with that URL and its observed values. Never issue another create. A state or draft mismatch stops for an explicit publication decision. Never silently reopen, close, convert, or create another PR. Record both single-step cards, the landed push, the PR observations, the ordered commit list, and the exact commands as publication evidence for the next `done` run. When authoritative search cannot identify whether a PR was created, mark the create `reconcile-required` and do not retry.

Print the URL and return to `done` for CI, review, publication-lane, and final row evaluation. Never merge. Opening the PR is a publication transition, not overall task completion.

The handoff holds when the preconditions held, base currency and issue link came from real output, the title and body passed the cold read, the remote branch and PR matched the local publication, and the evidence went back to `done` without claiming overall completion.
