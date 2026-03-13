---
name: sky
description: Answer a question about Sky governance using the local knowledge base
argument-hint: <question> | sync | add repo <url> | remove repo <name>
allowed-tools: Grep(*), Read(*), Edit(*), Write(*), Bash(git *), Bash(python3 *), Bash(test *), Bash(rm -rf *), Bash(mkdir *), Bash(ls *)
---

# Sky Knowledge Base

## Registry

<!-- Updated by /sky setup — do not edit manually -->
(Not configured yet. Ask a question or run `/sky sync` to set up.)

## Routing

Parse the user's input to determine the subcommand:

- `sync` → **Sync** flow
- `add repo <url>` → **Add Repo** flow
- `remove repo <name>` → **Remove Repo** flow
- Anything else → **Search** flow (default)

**Do not announce which flow you are running. Just execute it.**

---

## Setup flow

Triggered automatically when the Registry section above says "Not configured yet" and the user runs any command.

1. **Ask where to store the KB** using AskUserQuestion — suggest `~/sky-kb` as the default (with the user's actual home directory expanded). Let the user pick or type a custom path.

2. **Clone the repo** if the path doesn't exist:
   ```bash
   git clone https://github.com/arcniko/sky-kb.git <path>
   ```

3. **Ask which bundle** to install using AskUserQuestion with these options:
   - **All (Recommended)** — all categories + Atlas (~41 repos). "Full picture: governance, technical, everything."
   - **Core** — Atlas + protocol docs + core contracts (~18 repos). "Essential protocol documentation."
   - **Technical** — Core + Spark, Grove, keepers, migration, endgame (~29 repos). "Developer-focused: all code repos, skip governance/community."

4. **Map the bundle to category IDs**:
   - All → `["laniakea", "core-protocol", "spark", "grove", "migration", "endgame", "keepers", "governance"]`
   - Core → `["laniakea", "core-protocol"]`
   - Technical → `["laniakea", "core-protocol", "spark", "grove", "migration", "endgame", "keepers"]`

5. **Write `<path>/.kb_config.json`**:
   ```json
   {"preset": "sky", "categories": [...selected IDs...], "custom_repos": [], "atlas": true}
   ```

6. **Update the Registry section** in this SKILL.md — replace the placeholder text with `<path>` using the Edit tool.

7. **Run sync**:
   ```bash
   python3 <path>/scripts/sync.py --kb-path <path>
   ```

8. If the user had a question, continue to the **Search** flow to answer it.

---

## Search flow

1. **Resolve KB path** from the Registry section above. If it says "Not configured yet" → trigger **Setup** flow automatically.

2. **Read `<kb-path>/DIRECTORY.md`** to understand what content exists and where.

3. **Target your search** — based on DIRECTORY.md, identify the most relevant subdirectories for the question. Grep within those specific directories rather than all of `content/`.

4. **Read matching files** to find the answer.

5. For Atlas results: also read the parent scope file for broader context.

6. For protocol questions: prioritize `laniakea-docs` (current), then `mcd-docs-content` (legacy).

7. For smart contract address lookups: read `<kb-path>/content/chainlog-ui/api/mainnet/active.json` — this is the live chainlog with all current contract addresses.

### How to answer

- Be specific and cite your sources (Atlas formal ID like `A.1.2.3`, or file path for repo docs)
- Quote relevant passages when helpful
- If the content doesn't contain an answer, say so clearly

---

## Sync flow

1. **Resolve KB path** from the Registry section above. If it says "Not configured yet" → trigger **Setup** flow.
2. Run:
   ```bash
   python3 <kb-path>/scripts/sync.py --kb-path <kb-path>
   ```
3. Summarize concisely — only mention what changed:
   - Atlas: "updated" or "already up to date"
   - Repos: if ≤5 updated, list their names; if >5, just show the count (e.g. "12 repos updated")
   - If nothing changed: "Everything up to date."
4. If errors occurred, show them and suggest fixes.

---

## Add Repo flow

1. **Parse arguments** — extract repo URL (required), name (optional, derive from URL), description (optional, ask user).
2. **Resolve KB path** from the Registry section above. If it says "Not configured yet" → trigger **Setup** flow first.
3. **Validate** — run `git ls-remote <url> HEAD` to confirm accessibility.
4. **Read `<kb-path>/.kb_config.json`** — check `custom_repos` for duplicates.
5. **Add to config** — append to the `custom_repos` array in `.kb_config.json`.
6. **Run sync** to clone the new repo.
7. **Report** what was added.

---

## Remove Repo flow

1. **Parse the repo name** from arguments.
2. **Resolve KB path** from the Registry section above.
3. **Read `<kb-path>/.kb_config.json`** — find the repo in `custom_repos`.
   - If not found there, check if it's a preset repo. If so, tell the user to remove the category instead.
4. **Remove from config** — edit `.kb_config.json` to remove the entry.
5. **Delete content**: `rm -rf <kb-path>/content/<name>`
6. **Run sync** to regenerate DIRECTORY.md.
7. **Report** what was removed.
