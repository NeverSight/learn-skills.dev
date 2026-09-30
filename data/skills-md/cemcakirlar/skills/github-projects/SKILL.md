---
name: github-projects
description: Work with GitHub Projects v2 from the command line using gh project and GraphQL via gh api. Use for boards, custom fields, iterations, adding issues or pull requests as items, editing status and priority, listing and querying items. Triggers on GitHub project, project board, gh project, add to project, sprint field, project item, roadmap board, and similar Projects v2 requests.
metadata:
  type: workflow
  version: "1.2"
  stack: gh-project
---

# GitHub Projects

Operate on **Projects v2** through **`gh project`**. If that is not enough, prefer **REST `.../projectsV2/...`** when you have owner + number + numeric IDs. Use **GraphQL** when you only have `PVT_` node IDs or REST cannot do the mutation.

Repo-centric git work (clone, branch, PR, commit) is not this skill. Use `github-cli` first, then attach the issue or PR here.

Recipes live in `references/recipes.md`. REST escape hatch: `references/rest.md`. GraphQL escape hatch: `references/graphql.md`.

---

## Tool Choice

| Job                                                          | Tool                                     |
| ------------------------------------------------------------ | ---------------------------------------- |
| List/create/view/edit/close/copy project                     | `gh project`                             |
| Fields, items, link/unlink to a repo                         | `gh project field-*` / `item-*` / `link` |
| Multi-field write, list items with field values, numeric IDs | `gh api` REST `.../projectsV2/...`       |
| Node IDs only, views, mutations REST does not expose         | `gh api graphql`                         |
| Create the issue or PR itself                                | `github-cli` (`gh issue` / `gh pr`)      |

Do not use classic Projects (`/projects/{id}` columns API). This skill is Projects v2 only.

REST uses integer field/item IDs, not `PVT_` / `PVTI_`. User-owned REST routes often reject fine-grained PATs and GitHub App tokens; `gh auth` classic/OAuth is the usual fit. Org routes are more App-friendly. Details in `references/rest.md`.

---

## Preflight

Projects need the `project` token scope. `repo` is not enough.

```bash
gh auth status
# if project is missing
gh auth refresh -s project
```

Identify owner and number before mutating:

```bash
gh project list --owner "@me"
gh project list --owner ORG
gh project view NUMBER --owner OWNER --format json
```

`--owner "@me"` is the authenticated user. Org projects need the org login and org project permission, not only repo write.

---

## Safety Policy

1. Inspect with `list` / `view` / `item-list` / `field-list` before edit, archive, or delete.
2. **Do not `gh project delete`** unless the user named that exact owner and number and said delete.
3. **Do not `field-delete`** unless the user named the field. Deleting a field drops its values on every item.
4. Prefer `item-archive` over `item-delete` when the user said "remove from the board" but the issue should stay open.
5. Draft items (`item-create`) are not issues. Do not treat them as `OWNER/REPO#N`.
6. Never print tokens. Quote titles and field values.
7. Board layout, color, and most view cosmetics are UI-only. Say so instead of inventing GraphQL.
8. Treat GraphQL quota as a budget. `gh project` and `gh api graphql` share the GraphQL point bucket with every other client on this user token. Do not probe `rate_limit` before a single list or add. Do probe before a bulk field update, and after a 403/429.

---

## Default Workflow

Attach an existing issue or PR, then set Status if the field exists:

```bash
gh project item-add NUMBER --owner OWNER --url https://github.com/OWNER/REPO/issues/N
gh project field-list NUMBER --owner OWNER
gh project item-list NUMBER --owner OWNER --limit 50
```

Setting Status usually needs IDs from JSON. One field: `gh project item-edit` or GraphQL. Several fields on one item: REST PATCH in `references/rest.md`.

One item-add plus one field edit does not need a quota probe. Updating many items does:

```bash
gh api rate_limit --jq '.resources.graphql | {remaining,limit,reset}'
```

If GraphQL `remaining` is low and `core` is healthy, switch the writes to REST `projectsV2` (`references/rest.md`). If both are low, stop and give the `reset` time. Prefer one list-as-JSON over repeated `view` calls.

Create a board only when asked:

```bash
gh project create --owner OWNER --title "Title"
```

---

## IDs

| Kind                                  | Looks like           | Where you get it                      |
| ------------------------------------- | -------------------- | ------------------------------------- |
| Project number                        | `1`, `12`            | `gh project list` (human)             |
| Project / item / field **numeric** id | `13`, `123`          | same JSON `id` — use in REST paths    |
| Project node ID                       | `PVT_…`              | `gh project view --format json`       |
| Item node ID                          | `PVTI_…`             | `gh project item-list --format json`  |
| Field / option node IDs               | `PVTF_…` / `PVTSO_…` | `gh project field-list --format json` |

Numbers are per owner, not global. Always pass `--owner` with the number. REST wants the numeric `id`; GraphQL wants the node id.

---

## Out of Scope

- Classic Projects (repository Projects v1)
- Drawing board columns in the terminal
- Org-wide project policy or billing
- Creating the linked git commit / PR (use `github-cli`)
