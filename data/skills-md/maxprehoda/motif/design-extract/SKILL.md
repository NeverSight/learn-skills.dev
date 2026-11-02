---
name: design-extract
description: "Lists every spacing, type, color, radius, shadow and motion value a codebase uses and how often, finds near-duplicates and one-off values, and counts how many existing values each candidate scale would fit. Produces .design/drift.json. Use as phase 1 of design-system, or when the user asks how inconsistent their UI is."
---

# Design Extract

Count the values the code uses today. Do not recommend anything.

The next phase, `design-grill`, uses these counts to back up its recommendations. "This scale fits 24 of your 31 spacing values" is a reason the user can check.

## Step 1: Detect the stack

```bash
cat package.json 2>/dev/null | grep -E '"(tailwindcss|svelte|react|vue|next)"'
ls tailwind.config.* app/globals.css src/app.css src/**/*.css 2>/dev/null | head
```

Record the framework, the Tailwind major version (v3 uses `tailwind.config.js`, v4 uses `@theme` in a CSS file), whether a `components.json` file exists (it means the project uses shadcn/ui), and the file extension components use.

The commands below assume a `src` folder and Svelte or React files. Adjust the folder and `--include` patterns to match the project.

## Step 2: Count the values

Run each search and keep the counts.

One-off values. In Tailwind these are values written in square brackets, like `p-[13px]`, instead of a step from the scale:

```bash
grep -rhoE '\b(p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|gap|w|h|top|left|right|bottom|text|rounded|z)-\[[^]]+\]' \
  src --include="*.svelte" --include="*.tsx" --include="*.jsx" --include="*.vue" | sort | uniq -c | sort -rn
```

Spacing:

```bash
grep -rhoE '\b(p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|gap|space-[xy])-[0-9.]+\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
```

Font sizes, weights and line heights:

```bash
grep -rhoE '\btext-(xs|sm|base|lg|xl|[2-9]xl)\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
grep -rhoE '\bfont-(thin|light|normal|medium|semibold|bold|extrabold|black)\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
grep -rhoE '\bleading-[a-z0-9.]+\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
```

Color, in three groups: Tailwind palette colors used directly (like `text-neutral-700`), hex codes, and named color roles (like `text-primary`):

```bash
grep -rhoE '\b(bg|text|border|ring|from|to|via)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-[0-9]{2,3}\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
grep -rhoE '#[0-9a-fA-F]{3,8}\b' src --include="*.svelte" --include="*.tsx" --include="*.css" | sort | uniq -c | sort -rn
grep -rhoE '\b(bg|text|border)-(background|foreground|primary|secondary|muted|accent|card|popover|destructive)\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
```

Corner radius, shadows and motion:

```bash
grep -rhoE '\brounded(-[a-z0-9]+)?\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
grep -rhoE '\bshadow(-[a-z0-9]+)?\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
grep -rhoE '\b(transition|duration|ease|animate)-[a-z0-9-]+\b' src --include="*.svelte" --include="*.tsx" | sort | uniq -c | sort -rn
```

## Step 3: Sort the values

For each category (spacing, type, color and so on), sort the values into four groups:

- **Near-duplicates**: values within 15% of each other doing the same job, like `px-3` and `px-3.5` on two buttons side by side.
- **Long tail**: values used only once or twice.
- **Working set**: the few values that make up most of the usage.
- **Orphans**: one-off bracket values that aren't close to any step on any scale.

Then, for each scale the project might adopt, count how many of the current values would **fit** it: move onto one of its steps with a visible difference under 2px. `design-grill` quotes this number when it recommends a scale.

## Step 4: Write the output

`.design/drift.json`:

```json
{
  "stack": { "framework": "svelte", "tailwind": 3, "shadcn": true, "ext": "svelte" },
  "axes": {
    "spacing": {
      "distinct": 31, "arbitrary": ["pb-[15px]"], "workingSet": ["2","3","4","6","8"],
      "nearDuplicates": [["3","3.5"]], "longTail": ["1.5","7","9","11"]
    }
  },
  "hotspots": [{ "file": "src/routes/about/+page.svelte", "issues": 14 }]
}
```

Then print a summary of 25 lines or fewer. For each category, give the number of distinct values, the number of one-off bracket values, and how many values make up 80% of usage. Name the three files with the most findings.

Do not recommend a scale. That is `design-grill`'s job.
