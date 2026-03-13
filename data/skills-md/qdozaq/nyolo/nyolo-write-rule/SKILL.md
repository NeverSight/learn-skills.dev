---
name: nyolo-write-rule
description: |
  Write new nyolo permission rules for Claude Code safety guardrails.
  Use when the user wants to create, add, or write a nyolo rule to allow, deny, or ask
  confirmation for specific commands, file paths, URLs, or tool operations.
---

# Write nyolo Permission Rule

You are helping the user create a new nyolo permission rule. nyolo is a PreToolUse hook for Claude Code that blocks or gates dangerous operations.

## Step 1: Gather intent

Ask the user what they want the rule to do. You need:

1. **What to match** — a command, file path, URL, or search query pattern
2. **Which tool** — `Bash`, `Edit`, `Write`, `WebFetch`, `WebSearch`, or a combination (pipe-delimited, e.g. `Write|Edit`). Omit to match any tool.
3. **What action** — `deny` (block outright), `ask` (require confirmation), or `allow` (permit without prompt)
4. **Why** — a short reason shown to Claude when the rule triggers

## Step 2: Ask where to put the rule

Use AskUserQuestion to ask the user:

**Where should this rule be saved?**

| Option | Description |
|--------|-------------|
| **Project** (`./nyolo.config.js`) | Applies only to the current project. Defaults are auto-appended. |
| **Global** (`~/.claude/nyolo.config.js`) | Applies to all projects. You compose the full rule set via imports. |

## Step 3: Write the rule

### Rule format (declarative)

```js
{
  name: "kebab-case-unique-name",       // required: unique identifier
  description: "Human-readable summary", // optional
  category: "custom",                    // optional: grouping label
  tool: "Bash",                          // optional: pipe-delimited tool filter
  match: {
    // field → pattern (AND logic across fields)
    command: "*pattern*",               // glob (default) — micromatch with extglob
    // file_path: "**/.env",            // glob with path semantics
    // url: "*example.com*",            // for WebFetch
    // query: "*secret*",              // for WebSearch
    // For complex matching, use regex instead of glob:
    // command: { pattern: "sudo\\s", parser: "regex", flags: "i" },
  },
  action: "deny",                        // "deny" | "ask" | "allow"
  reason: "Explanation shown to Claude",
}
```

### Match field reference

| Tool | Field | Notes |
|------|-------|-------|
| `Bash` | `command` | Glob: `*` matches `/`. Also tested against sub-commands (`;`, `&&`, `\|\|`, `$()`) |
| `Write` / `Edit` | `file_path` | Standard glob path semantics (use `**/` for deep match) |
| `WebFetch` | `url` | Glob pattern against the URL |
| `WebSearch` | `query` | Glob pattern against the search query |

### Pattern tips

- **Glob (preferred)**: `"*dangerous*"` — uses micromatch with extglob (`@()`, `!()`, `*()`, `+()`, `?()`)
- **Regex**: `{ pattern: "sudo\\s", parser: "regex" }` — only when glob can't express the match
- **Regex flags**: `{ pattern: "DROP TABLE", parser: "regex", flags: "i" }` — case-insensitive
- For `command` fields, `*` matches `/` (relaxed path semantics)
- For `file_path` fields, standard path glob semantics apply (`*` does NOT match `/`)
- An empty `match: {}` matches everything (useful as a catch-all)
- Multiple fields in `match` use AND logic — all must match

### Callback rules (advanced)

For complex logic that can't be expressed declaratively:

```js
(toolName, toolInput, { cwd }) => {
  if (toolName === "Bash" && /pattern/.test(toolInput.command)) {
    return { action: "deny", reason: "Explanation" };
  }
  return null; // null = skip, continue to next rule
}
```

- Return `{ action, reason }` to decide, or `null`/`undefined` to skip
- Thrown errors → `deny` (fail-closed)
- Async callbacks are NOT supported (denied immediately)

## Step 4: Write the config file

### Project config (`./nyolo.config.js`)

If the file doesn't exist, create it. The 35 recommended defaults are auto-appended after your rules (first-match-wins), so your rules take priority.

```js
// nyolo.config.js
export default [
  // new rule goes here
];
```

To suppress defaults, add: `export const noDefaults = true;`

### Global config (`~/.claude/nyolo.config.js`)

The global config IS the base rule set. Import categories from nyolo:

```js
// ~/.claude/nyolo.config.js
import { recommended } from "nyolo";

export default [
  // new rule goes here — evaluated before recommended
  ...recommended,
];
```

Or pick specific categories:

```js
import { filesystem, git, network } from "nyolo";
export default [
  // new rule
  ...filesystem,
  ...git,
  ...network,
];
```

Available category imports: `recommended`, `filesystem`, `cloud`, `network`, `git`, `database`, `system`, `container`, `protection`, `sensitive`, `warnings`, `defineConfig`.

## Step 5: Verify

After writing the rule, tell the user to run `npx nyolo test` to verify their rules load and work correctly, or `npx nyolo rules` to list all active rules.

## Important notes

- **First-match-wins**: rule order matters. Project rules are evaluated before global rules.
- **Keep rules minimal**: prefer a precise pattern over a broad one.
- Rules should have unique `name` values.
- Prefer `ask` over `deny` when the operation might be legitimately needed — `ask` lets Claude request approval rather than being blocked entirely.
