---
name: ada-knowledge
description: Manage an Ada agent's knowledge base at scale with adacli — audit, create, update, delete articles, manage availability rules, list, create and update sources, and scrape URLs. Use when the user wants to bulk-edit knowledge, import content, audit the KB, or fix what the agent knows.
require-tools:
  - Bash
  - Read
  - Write
---

# Knowledge base management

The knowledge base is the agent's source of truth. Better knowledge = higher automated
resolution. Commands target `adacli <instance> knowledge ...` (alias `kb`).

## Audit / read

```bash
adacli <instance> knowledge list --json --limit 100        # all articles (paginate with --page)
adacli <instance> knowledge get <id> --json                # one article
adacli <instance> knowledge sources --json                 # sources, their status and availability rules
```

To find candidates for cleanup, list and inspect with jq, e.g. titles only:
`adacli <instance> knowledge list --json | jq -r '.articles[].title'`.

## Create / update

```bash
# From a file (preferred for real content)
adacli <instance> knowledge create --title "Refund Policy" --file refund.md

# Inline
adacli <instance> knowledge create --title "Shipping FAQ" --body "We ship in 3-5 days..."

# Update content or title
adacli <instance> knowledge update <id> --file updated.md
adacli <instance> knowledge update <id> --title "New Title"
```

## Bulk import from a folder

For many files, loop and create one article per file, deriving the title from the filename:

```bash
for f in ./kb/*.md; do
  title="$(basename "$f" .md)"
  adacli <instance> knowledge create --title "$title" --file "$f" --json
done
```

## Availability rules & scraping

```bash
adacli <instance> knowledge set-rules ...                  # gate which articles are searchable
adacli <instance> knowledge scrape --rules ...             # import content from URLs, with a rule for every page
adacli <instance> knowledge sources create --name ... --rules ...   # Knowledge API source with a rule
adacli <instance> knowledge sources update <id> --rules ... | --clear-rules
adacli <instance> knowledge sources sync <id>              # re-crawl a website import now
```

A rule on a source applies to the articles the source adds after the change; existing articles keep their own rules.
Run `adacli <instance> knowledge set-rules --help` / `scrape --help` / `sources update --help` for the exact options.

## Rules

- **Read before write**: `get` an article and show the user the change before `update`.
- **Confirm deletes**: `knowledge delete <id>` is destructive — confirm with the user.
- After bulk changes, verify with `knowledge list --json` and (optionally) the
  **ada-config-snapshot** skill to commit the new state.
- To verify a change is live for end users, see the **ada-insights** skill or test a
  question through the agent.
