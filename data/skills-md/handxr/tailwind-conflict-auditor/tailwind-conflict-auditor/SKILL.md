---
name: tailwind-conflict-auditor
description: Audit Tailwind CSS classes for conflicts, redundancies, duplicate utilities, obsolete v3 patterns, and class ordering issues. Use when reviewing Tailwind code quality, debugging unexpected styles, auditing components, or when a user asks to check their Tailwind classes, find class conflicts, clean up duplicates, or migrate from v3 to v4. Triggers on tasks involving HTML/JSX/TSX/Vue/Svelte files with Tailwind CSS utility classes.
---

# Tailwind Class Conflict & Redundancy Auditor

Scan project files for Tailwind CSS class issues. Conservative approach: report and suggest, never auto-apply changes.

## Workflow

1. Locate files using Glob (`**/*.{html,jsx,tsx,vue,svelte,astro,erb,php,hbs,ejs,njk,twig,js,ts}`)
2. Run the auditor script from the skill directory:
   ```bash
   python3 <skill-path>/scripts/tailwind_class_auditor.py <file_or_dir> --json
   ```
3. Parse the JSON output
4. Present findings grouped by severity (errors first, then warnings, then info)
5. For each issue, show the file, line, conflicting classes, and a concrete suggestion
6. Wait for user approval before applying any changes

## Running the Auditor

**Single file:**
```bash
python3 <skill-path>/scripts/tailwind_class_auditor.py src/components/Button.tsx --json
```

**Entire directory:**
```bash
python3 <skill-path>/scripts/tailwind_class_auditor.py src/ --json
```

**Include ordering suggestions** (default: only conflicts/duplicates/obsolete):
```bash
python3 <skill-path>/scripts/tailwind_class_auditor.py src/ --json --strict
```

**Human-readable output** (omit `--json`):
```bash
python3 <skill-path>/scripts/tailwind_class_auditor.py src/
```

## What It Detects

### Conflicts (severity: error)
Two classes setting the same CSS property in the same variant context:
- `p-4 p-6` — both set `padding`
- `text-red-500 text-blue-500` — both set `color`
- `flex block` — both set `display`
- `md:hidden md:block` — both set `display` at `md:`

### Duplicates (severity: warning)
Same class appearing twice in the same attribute:
- `mt-4 ... mt-4`

### Obsolete v3 patterns (severity: warning)
Classes renamed or removed in Tailwind v3/v4:
- `transform`, `filter`, `backdrop-filter` — no longer needed
- `flex-grow` → `grow`, `flex-shrink` → `shrink`
- `bg-opacity-50` → `bg-red-500/50` (slash notation)

### Ordering (severity: info, only with `--strict`)
Classes not following recommended order: layout > position > flex/grid > spacing > sizing > typography > backgrounds > borders > effects > transitions > transforms

## Interpreting Results

The JSON report per file contains:

- **summary**: Counts for class_attributes, conflicts, duplicates, obsolete, ordering
- **issues**: Array of issue objects, each with:
  - `type`: "conflict" | "duplicate" | "obsolete" | "ordering"
  - `severity`: "error" | "warning" | "info"
  - `line`: Line number in the file
  - `message`: Human-readable description
  - `suggestion`: Concrete fix

## Presenting Suggestions

When reporting to the user:
1. Start with summary stats per file
2. Group issues by severity (errors first)
3. For conflicts: show both classes and the CSS property they fight over
4. For obsolete: show the old class and its modern replacement
5. For duplicates: show the duplicated class
6. Propose specific fixes (e.g., "Remove `p-4`, keep `p-6`")

For detailed rules on conflict types and valid patterns, read [references/tailwind-conflict-rules.md](references/tailwind-conflict-rules.md).

## Known Limitations

- `cn()`/`clsx()`/`classnames()` calls: the auditor extracts all string literals and merges them. Conditional classes like `cn("p-4", condition && "p-6")` may produce false-positive conflicts. Review these before suggesting fixes.

## Applying Corrections

Only apply corrections after user approval. When the user approves:
1. Apply one change at a time
2. Re-run the auditor after each batch to verify improvement
3. Never introduce new conflicts while fixing existing ones
