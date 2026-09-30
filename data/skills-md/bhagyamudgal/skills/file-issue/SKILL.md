---
name: file-issue
description: File one GitHub issue an assignee can act on unaided. Use when reporting a bug, requesting work, or capturing a finding as a ticket.
---

# File an issue

An issue is read by someone who was not there when the problem was found, often months later. Every bar below exists so that reader can act on it without coming back to ask what it meant.

## 1. Confirm this is one issue

One issue carries one observable problem and one acceptance condition.

Work that splits into several tickets with blocking edges between them belongs to `to-tickets`. A spec synthesised from the current conversation belongs to `to-spec`. Hand off rather than filing a container ticket that hides its real scope.

The gate is simple. The scope is one problem with one acceptance condition, or the work is handed off by name.

## 2. Search before filing

```bash
gh issue list --repo "$repository" --search "<the symptom in your words>" --state all --limit 20
gh issue list --repo "$repository" --search "<the symptom in the reporter's words>" --state all --limit 20
```

Search twice with different vocabulary, because the existing ticket was filed by someone who described it differently. `--state all` matters. A closed near-match is either the thing to reopen or the context the new issue needs.

Resolve every near match before filing. Each one ends duplicate, related, or genuinely new. Link a related one with `Refs #N` and one line saying what is different about this one.

The gate is that both searches ran and every near match has a resolution.

## 3. Compose the title

Prefix the title under the issue-title rule in `CLAUDE.md`: conventional-commit type plus the module the work actually lives in, named the way the board reads it rather than the way the directory spells it.

The description clears the same bar as the title step in `file-pr`. Name what you observe, never the mechanism you suspect, and never a generic verb standing alone as the description.

A good bug title names the wrong behaviour, not the suspected cause. `fix(auth): session drops on tab switch` survives being wrong about the cause. `fix(auth): cookie expiry miscalculated` becomes a lie the moment the cause turns out to be something else.

The gate is that the title names an observation that stays true independent of the diagnosis.

## 4. Compose the body

Four parts, in this order, each one prose rather than a fragment:

- **What happens.** The observed behaviour, opening the body with no heading above it.
- **How to see it.** Exact steps, command, URL, or `file:line` evidence. Someone with repo access and nothing else reaches the same observation from this alone.
- **What should happen instead.** Stated separately from the observation, because the gap between them is the actual request.
- **Done looks like.** One condition a reviewer can check. "Works properly" is not one.

Then add only what carries content. That means `Refs #N` links and the environment when it matters. Take the environment from evidence. The URL bar in a screenshot tells you whether this was production or dev. Never assume it.

Attach screenshots rather than describing them. A described screenshot loses everything the describer did not notice, and the person fixing this needs the image itself.

The gate is that the four parts are present and the reproduction stands on its own without the session that produced it.

## 5. Cold-read the result

Run the cold-read bars from `file-pr` against the composed title and body, then two more that only an issue has:

- **Reproduction.** Someone with repo access and no other context reaches the observation.
- **Acceptance.** The done condition is checkable by someone who did not write it.

A bar you did not name is a bar you did not check.

The gate is that every bar has a named result and none is failing.

## 6. File it

Render the final body to a file and record its SHA-256 digest. Resolve the repository's stable identity and current duplicate-search results, then invoke `preflight-mutations` with the exact repository, title, body path and digest, create options including `--label ai-created`, ownership boundary, and authoritative read-back query. A changed title, option, label, body path, digest, repository, or duplicate result invalidates the card.

Ensure the `ai-created` provenance label exists before creating. It marks every issue filed through this skill so agent-filed issues stay distinguishable from human-filed ones. When it is absent, raise a separate label-creation card through `preflight-mutations` naming the repository, then look the label up by exact name rather than a capped listing, tolerate only the already-exists race on create, and prove the label reads back:

```bash
if ! gh api "repos/$repository/labels/ai-created" >/dev/null 2>&1; then
  create_out=$(gh label create ai-created --repo "$repository" --color "A2EEEF" --description "Created by an AI agent" 2>&1) || printf '%s\n' "$create_out" | grep -qiE "already.?exists"
fi
gh api "repos/$repository/labels/ai-created" --jq .name | grep -Fqx "ai-created"
```

Creating an issue writes to shared state, so continue only on a current `ready` result. Pass the title as one argument and the frozen body by file, always with the provenance label:

```bash
gh issue create --repo "$repository" --title "$title" --body-file "$body_path" --label "ai-created"
gh issue view <issue-url> --repo "$repository" --json number,title,body,state,author,assignees,labels,url
```

Set assignee, estimate, or priority only within the project-board ownership boundary in `CLAUDE.md`. Filing an issue does not make those fields yours to set. Never drop the `ai-created` label to set another label. Triage labels go on alongside it.

Require one created URL, then compare the fetched repository, title, body, labels, metadata, and URL with the approved payload. Require `ai-created` present in the fetched labels. When the command result is missing or ambiguous, search the target repository for exact-title candidates and compare their bodies and metadata. Mark the attempt `reconcile-required` and do not retry until that authoritative search proves whether the issue exists.

Print the URL only after the read-back identifies one matching issue.

The run is done when the scope is one issue, both duplicate searches ran and resolved, the title names an observation that survives a wrong diagnosis, the body carries all four parts, every cold-read bar is named and clean, and authoritative read-back identifies the printed issue URL carrying the `ai-created` label or the attempt remains `reconcile-required` without retry.
