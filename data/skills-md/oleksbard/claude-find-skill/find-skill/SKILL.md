---
name: find-skill
description: Use when the user wants to find or discover a Claude Code skill that is NOT already installed — e.g. "is there a skill for X", "find me a skill that…", "what skills exist for…", or "/find-skill <topic>". Searches the official plugin marketplace, GitHub, and curated awesome-lists for community skills matching a need, removes anything already installed, and recommends the top 5 with links. Do NOT use this to create or edit skills (that is skill authoring), or to pick among skills you already have.
---

# Find a Skill

Discover Claude Code skills that are **not yet installed** and recommend the best matches for a stated need. This is **discover-and-recommend only** — never install, download, clone, or modify the user's system. End by showing a ranked shortlist with links; the user installs manually.

## Procedure

### 1. Turn the request into keywords

Extract 2–4 search keywords from the user's need (the topic, the verb, key nouns). If the request is too vague to search (e.g. "find me a useful skill"), ask one clarifying question first.

### 2. List what's already installed (for dedup)

The whole point is to surface skills the user does **not** have. Build a set of installed skill names/topics:

```sh
ls -d ~/.claude/skills/*/ 2>/dev/null                       # personal skills
find ~/.claude/plugins -maxdepth 8 -name SKILL.md 2>/dev/null  # plugin skills
```

Also account for the available-skills list already present in your context. Any candidate that matches something installed must be **excluded** — or mentioned as "you already have this" — never recommended as new.

### 3. Search the sources

Run all three. They are independent; if one fails, continue with the others.

**A. Official marketplace — local cache, offline, fast. Always do this first.**

```sh
jq -r --arg kw "<keyword>" '
  .catalog.plugins | to_entries[]
  | .key as $id | .value as $p
  | ($p.marketplace_entry.name // $id) as $name
  | ($p.marketplace_entry.description // "") as $desc
  | ([$p.components.skills[]?.name] | join(", ")) as $skills
  | select((($name+" "+$desc+" "+$skills)|ascii_downcase) | test($kw|ascii_downcase))
  | "\($p.unique_installs // 0)\t\($name)\t\($id)\t\($p.marketplace_entry.homepage // "")\t\($desc)"
' ~/.claude/plugins/plugin-catalog-cache.json | sort -rn | head -10
```

Columns: `unique_installs` (popularity) · name · install id (`name@marketplace`) · homepage · description. Install hint for these: `/plugin install <id>`.

**B. GitHub — degradation chain. Use the first rung that works.**

1. **Authed `gh`** (best precision). Check `gh auth status`; if logged in:
   ```sh
   gh search repos "<kw> claude skill" --limit 20 --stars ">=10" \
     --json fullName,description,stargazersCount,pushedAt,url
   gh search code "filename:SKILL.md <kw>" --limit 20 \
     --json repository,path,url        # code search REQUIRES auth
   ```
2. **No auth → public REST API** (repos only, rate-limited ~10/min). The `stars:>=10` qualifier applies the popularity floor server-side:
   ```sh
   curl -sG "https://api.github.com/search/repositories" \
     --data-urlencode "q=<kw> claude skill stars:>=10" --data "sort=stars" --data "per_page=20" \
     | jq -r 'if .message then "ERR: \(.message) — fall through to WebSearch" else (.items[]? | "\(.stargazers_count)\t\(.full_name)\t\(.pushed_at[0:7])\t\(.html_url)\t\(.description // "")") end'
   ```
3. **API unavailable/rate-limited → WebSearch tool.** Query `claude skill <topic> SKILL.md site:github.com`, then WebFetch the most promising repos to read their `SKILL.md` / README and confirm they really are skills. There's no star filter here, so apply the popularity floor yourself when ranking (step 4).

Columns from rungs 1–2: stars · repo · last-push month (`pushedAt`/`pushed_at`, the true freshness signal — **not** `updatedAt`, which bumps on a mere star or description edit) · url · description.

Install hint for GitHub finds: symlink or copy the skill dir, e.g. `git clone <url>` then point Claude at its `SKILL.md`.

**C. Curated awesome-lists — human-vetted, good signal.**

WebSearch `awesome claude code skills`, then WebFetch the top index (start with `github.com/hesreallyhim/awesome-claude-code`) and pull entries matching the keywords. Verify a link before recommending it.

### 4. Merge, dedup, rank

- **Dedup** across sources by repo URL / skill name. Drop anything already installed (per step 2) — or note "you already have `<name>`" instead of listing it as new.
- **Popularity floor (GitHub raw search only).** Drop GitHub repos under **10 stars** — single-author throwaways and 1–3 ★ repos are unvetted noise, not recommendations. Marketplace plugins (`unique_installs` is their signal) and curated-list entries (human-vetted) are **exempt** from this floor. Also downrank repos with no code push in ~6 months (use `pushedAt`, not `updatedAt`).
- **Verify GitHub candidates are real skills.** Repo search (rungs 1–2) matches on text — a repo can name-drop "claude skill" without containing one. Before a GitHub repo enters the top 5, confirm it actually has a `SKILL.md`: `gh search code "filename:SKILL.md repo:<owner/name>"` when authed, else WebFetch the repo to check for a `SKILL.md` (as rung 3 already does). Drop what you can't confirm, or label it `unverified`. Marketplace and curated-list entries are already known skills — skip this.
- **Rank** by relevance to the stated need first; break ties by popularity (`stargazersCount` / `unique_installs`) and recency (`pushedAt`).
- Keep the **top 5** — fewer is fine. A short list of vetted picks beats five padded with low-star repos.

### 5. Present

One block per candidate:

```
**<name>** — <one-line description>
  Source: GitHub | Marketplace | List   ·   <★ stars (GitHub) | N installs (Marketplace)> · pushed <YYYY-MM>
  Link: <repo url / marketplace id>
  Why: <one line: how it fits the stated need>
  Get it: <copy-paste hint — `/plugin install …` or `git clone …`>  (not run for you)
```

If a source was skipped or degraded, add a one-line footer, e.g.
`> GitHub searched via WebSearch — run \`gh auth login\` for sharper, code-level results.`

## Edge cases

- **No matches** → say so plainly; suggest broader keywords, or `/plugin` to browse the marketplace UI.
- **Everything is below the popularity floor** → don't pad the list with 2-star repos. Say the topic has no well-established skill yet. Only mention a sub-floor GitHub repo if it's an unusually strong topical fit, and label it explicitly, e.g. `early-stage (3★)`, so it never reads as a vetted pick.
- **Everything matches something installed** → tell the user they're already covered, naming the installed skill(s); don't pad with weak picks.
- **A source errors** (network, rate limit, missing `jq`/`gh`) → note which one, continue with the rest. Never hard-fail the whole search.

## Out of scope

No installing, cloning, downloading, or any system modification. No general/open web search (GitHub + marketplace + curated lists only). No result caching, no scoring engine — judge relevance yourself.
