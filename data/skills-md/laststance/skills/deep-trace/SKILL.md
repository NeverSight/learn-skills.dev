---
name: deep-trace
description: Line-by-line diff trace
argument-hint: "[pr-number-or-file-path]"
---

# Deep Trace — Line-by-Line Execution Path Tracer

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


<essential_principles>

## Core Concept

Trace code like a debugger stepping through line-by-line, but enriched with:
- **Screen**: What the user sees when this code runs
- **URL**: The page/API route where this executes
- **Data flow**: What data enters, transforms, and exits
- **Trigger**: What event/action causes this line to execute

## Trace Table Format

Every trace outputs a structured table:

```
## Trace: [description]

| # | File:Line | Code | Screen/URL | Data Flow | Trigger |
|---|-----------|------|------------|-----------|---------|
| 1 | page.tsx:15 | `const router = useRouter()` | /drawings | — | Page mount |
| 2 | page.tsx:16 | `const { id } = router.query` | /drawings?id=123 | id: string | URL params |
| 3 | hook.ts:8 | `const { data } = useQuery(...)` | /drawings?id=123 | id → API call | React render |
| ... | ... | ... | ... | ... | ... |
```

## Principles

1. **Diff-first**: Start from changed lines, trace outward to entry point and downstream effects
2. **Line granularity**: Every meaningful line gets its own row (skip blank lines, imports, type-only lines)
3. **Screen mapping**: Always identify which screen/URL the user is on when this code runs
4. **Bidirectional**: Trace both UP (who calls this?) and DOWN (what does this call?)
5. **Application boundary**: Summarize library calls in 1 row, don't trace into node_modules
6. **No abbreviation in File:Line**: NEVER truncate or ellipsis file names. Always show the full file name (e.g., `useSetFormValuesFromQueryStrings.tsx:77`, NOT `useSetFormValues...:77`). Code column may be abbreviated if >80 chars, but file names must be exact.

</essential_principles>

## Workflow

### Step 1: Identify Target

Determine input source from user's argument:

| Input | Detection | Action |
|-------|-----------|--------|
| PR number | `#1234` or number | `gh pr diff <number>` |
| Branch diff | `--diff` or no arg | `git diff HEAD~1` or `git diff dev...HEAD` |
| File path | `.ts`, `.tsx`, etc. | Read file, trace from exports |
| Function name | text without path | Serena `find_symbol` |

### Step 2: Extract Changed Code

For PR/diff inputs:
1. Parse diff to get changed files and line ranges
2. Group changes by file
3. Prioritize: components > hooks > utils > types

For file/function inputs:
1. Read the target code
2. Identify exported functions/components

### Step 3: Find Entry Points

For each changed code section, trace UP to find the entry point:

```
Changed line → containing function → caller → ... → page component / API route / event handler
```

Use Serena tools:
- `find_symbol` — locate the function
- `find_referencing_symbols` — find callers
- Repeat until reaching a page/route/event boundary

**Entry point types:**
| Type | Example | Screen/URL |
|------|---------|------------|
| Page component | `pages/drawings/index.tsx` | `/drawings` |
| API route | `pages/api/drawings.ts` | `POST /api/drawings` |
| Event handler | `onClick`, `onSubmit` | Button click on current page |
| Effect | `useEffectOnMount` | Page load |
| Provider | `_app.tsx` wrapper | All pages |

### Step 4: Build Trace Table

Starting from entry point, step through line-by-line:

1. **Read the entry point file** (Serena `find_symbol` with `include_body=True`)
2. **For each meaningful line**, create a table row:
   - `#`: Sequential step number
   - `File:Line`: Full file name + line number. NEVER abbreviate or ellipsis file names
   - `Code`: The actual code (backtick-wrapped, may abbreviate if >80 chars)
   - `Screen/URL`: What screen/page/URL is active
   - `Data Flow`: What data is being read/written/transformed
   - `Trigger`: What causes this line to execute (mount, click, API response, etc.)

3. **When hitting a function call**:
   - If it's application code → trace INTO it (sub-steps like 3.1, 3.2, ...)
   - If it's a library call → summarize in 1 row with `[lib]` prefix

4. **When hitting a conditional**: note both paths, trace the primary path

### Step 5: Annotate with Context

Add these sections after the trace table:

```markdown
## Summary
- **When**: [user action / event that triggers this code]
- **Where**: [screen URL and component location]
- **What**: [1-2 sentence description of what the code accomplishes]
- **Data**: [key data entities involved, their sources and destinations]

## Key Observations
- [Notable patterns, potential issues, or design decisions]
```

### Step 6: Generate Extension-Compatible Output

After the Summary, generate a **separate copyable table** for the [deep-trace-extension](https://github.com/laststance/deep-trace-extension) VS Code extension.

**Extension format** (4 columns, specific header names required):

```markdown
## 📋 Deep Trace Extension

| file | line | col | reason |
| --- | --- | --- | --- |
| src/components/FreewordSearchFilter.tsx | 40 | 1 | useFreewordSearchFormContext — Component render |
| src/components/FreewordSearchFilter.tsx | 54 | 1 | useWatch target values — Form state change |
```

**Conversion rules from trace table → extension table:**

| Trace column | → Extension column | Rule |
|---|---|---|
| `File:Line` | `file` + `line` | Split on last `:` — file path before, line number after |
| — | `col` | Always `1` (column info not tracked in trace) |
| `Code` + `Trigger` | `reason` | Combine: short code description + ` — ` + trigger |

**Requirements:**
- Every row from the trace table gets a corresponding row
- `file` must be the **full relative path** (not just filename). Resolve from project root using Serena if the trace table only has the filename
- Output inside a fenced code block (` ```markdown ... ``` `) so users can copy the raw Markdown

### Step 6.5: Copy Extension Table to Clipboard (Optional, OS-aware)

Right after printing the fenced extension-table block from Step 6, **also pipe that same block into the bundled helper** so users can paste straight into the [deep-trace-extension](https://github.com/laststance/deep-trace-extension) without manual selection:

```bash
cat <<'EOF' | bash skills/deep-trace/scripts/copy-to-clipboard.sh
| file | line | col | reason |
| --- | --- | --- | --- |
| src/components/FreewordSearchFilter.tsx | 40 | 1 | useFreewordSearchFormContext — Component render |
| src/components/FreewordSearchFilter.tsx | 54 | 1 | useWatch target values — Form state change |
EOF
```

The helper auto-detects the host clipboard tool:

| OS / environment            | Tool tried                               |
|-----------------------------|------------------------------------------|
| macOS                       | `pbcopy`                                 |
| Linux (Wayland session)     | `wl-copy`                                |
| Linux (X11 session)         | `xclip -selection clipboard` → `xsel`    |
| WSL                         | `clip.exe`                               |
| Cygwin / MinGW / MSYS       | `clip`                                   |
| No tool / unknown OS        | Skipped with a one-line stderr notice    |

**Behavior contract (do not violate):**
- The fenced markdown block from Step 6 is **always** printed first — clipboard copy is purely additive, never a replacement.
- The script **always exits 0**, even when no clipboard tool exists. Skill workflow must not fail because clipboard is unavailable.
- The script reports the chosen tool (or skip reason) on **stderr**, e.g. `copy-to-clipboard: copied via pbcopy (macOS)`. Surface that line back to the user so they know whether to copy manually.

**When to skip this step entirely:**
- Headless CI / non-interactive runs (no human to paste)
- Sandboxed or remote environments where clipboard access is denied or meaningless
- User explicitly opts out (e.g. security-sensitive context)

### Step 7: Save to Memory (Optional)

If the user wants to remember this trace:
```
Serena write_memory("trace_<descriptive_name>", traceContent)
```

## Examples

### Example: Tracing a PR diff

```
/deep-trace #3548
```

Output:
```
## Trace: PR #3548 — フリーワード検索の種別フィルター追加

### Entry: FreewordSearchFilter.tsx (絞り込みPopover内)

| # | File:Line | Code | Screen/URL | Data Flow | Trigger |
|---|-----------|------|------------|-----------|---------|
| 1 | FreewordSearchFilter.tsx:40 | `const { control } = useFreewordSearchFormContext()` | /freeword_search?query=テスト | form context | Component render |
| 2 | FreewordSearchFilter.tsx:54 | `const targetValues = useWatch({ control, name: 'target' })` | same | target: SelectOption[] | Form state change |
| 3 | FreewordSearchFilter.tsx:65 | `useDocumentTypeSettingsQuery(...)` | same | API → document_type_settings | React Query cache/fetch |
| 4 | FreewordSearchFilter.tsx:70 | `const targetOptions = useMemo(...)` | same | settings → SelectOption[] | Deps change |
| 5 | FreewordSearchFilter.tsx:119 | `<MultiSelectRHF ... options={targetOptions}>` | same (Popover open) | targetOptions → UI | User opens filter |

### Summary
- **When**: User opens 絞り込み popover on freeword search page
- **Where**: /freeword_search (ファイルフリーワード検索モード)
- **What**: Shows multi-select filter for 種別 (drawing + document types)
- **Data**: document_type_settings API → SelectOption[] → form state → API search params

## 📋 Deep Trace Extension

```markdown
| file | line | col | reason |
| --- | --- | --- | --- |
| src/components/FreewordSearchFilter.tsx | 40 | 1 | useFreewordSearchFormContext — Component render |
| src/components/FreewordSearchFilter.tsx | 54 | 1 | useWatch target values — Form state change |
| src/components/FreewordSearchFilter.tsx | 65 | 1 | useDocumentTypeSettingsQuery — React Query cache/fetch |
| src/components/FreewordSearchFilter.tsx | 70 | 1 | useMemo targetOptions — Deps change |
| src/components/FreewordSearchFilter.tsx | 119 | 1 | MultiSelectRHF render — User opens filter |
```
```

## Tools Used

| Tool | Purpose |
|------|---------|
| `gh pr diff` | Get PR diff |
| `git diff` | Get branch diff |
| Serena `find_symbol` | Locate functions |
| Serena `find_referencing_symbols` | Find callers (trace UP) |
| Serena `get_symbols_overview` | Map file structure |
| Serena `write_memory` | Save trace for future reference |
| `scripts/copy-to-clipboard.sh` | OS-aware clipboard copy of the extension table (pbcopy / wl-copy / xclip / xsel / clip.exe / clip; graceful skip otherwise) |

## Success Criteria

- [ ] Entry point correctly identified (page/route/event)
- [ ] Every meaningful changed line has a trace row
- [ ] Screen/URL column populated for all rows
- [ ] Data flow shows inputs → transformations → outputs
- [ ] Trace is readable top-to-bottom as an execution story
- [ ] Summary captures when/where/what/data
- [ ] Extension-compatible table included with `file`, `line`, `col`, `reason` columns
- [ ] Extension table uses full relative paths (not just filenames)
- [ ] Extension table wrapped in fenced code block for easy copy
- [ ] Extension table also piped through `scripts/copy-to-clipboard.sh` (or step explicitly skipped with reason); helper's stderr status surfaced to the user
