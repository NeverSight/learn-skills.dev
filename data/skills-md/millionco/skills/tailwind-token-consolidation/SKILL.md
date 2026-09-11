---
name: tailwind-token-consolidation
description: Use when consolidating, deduping, or reducing the number of CSS custom properties / Tailwind v4 design tokens in a globals.css file. Triggers on requests like "reduce tokens", "standardize design tokens", "too many tokens", "dedupe globals.css", "shrink @theme inline", "collapse similar colors", or any task whose goal is fewer tokens while keeping the same visual result. Covers @theme inline, --color-* aliases, :root/.dark/.dashboard-page blocks, dead-token analysis, value-similar collapse, single-use inlining, and the Tailwind v4 arbitrary-value escape syntax.
---

# Tailwind Token Consolidation

You are reducing the count of design tokens in a Tailwind v4 `globals.css` while preserving visual fidelity.

REQUIRED, in order, for every consolidation task:

1. **Audit first, edit never-first.** Parse `globals.css` into structured blocks (`@theme inline`, `:root`, `.dark`, every other scoped block). Count tokens. Build a usage map by scanning ALL `.ts/.tsx/.css/.mdx` files (excluding `globals.css`) for class names AND `var(--...)` refs.
2. **Compute the LIVE set transitively.** A token is live if (a) its suffix appears as a Tailwind class anywhere, OR (b) it is referenced as `var(--name)` anywhere, OR (c) it is referenced inside another live token's value. Iterate to a fixed point.
3. **Scan `globals.css`'s own utility classes too.** Any `var(--...)` inside `.X { ... }` blocks (outside `:root`/`.dark`/`@theme inline`) is a hard dependency. Tokens demanded by those classes MUST stay.
4. **Build a deterministic rename map** as data (`old_suffix -> new_suffix` or `DELETE`). Apply it to globals.css AND code in a single script. Never hand-edit class names across the codebase.
5. **Verify after every pass:** run `pnpm typecheck`, `pnpm lint`, `pnpm format`, `pnpm build`. All must pass before declaring done.

Do not skip any step. A skipped step is a failed task.

## The Two Reduction Levers (apply in this order)

| Lever | What it removes | Risk |
|---|---|---|
| 1. **Dead deletion** | Tokens with zero usage in code + zero intra-globals demand | None — safe |
| 2. **Value-similar collapse** | Rename `--button` → `--card` when values are within ~5% in both light + dark | Small — pick truly-similar values only |

DO NOT inline tokens into Tailwind arbitrary values (`px-[17px]`, `text-[16px]/[1.6875rem]`, `shadow-[#000_0px_1px]`). Inlining trades named-token clutter for arbitrary-value clutter — same noise, different file. Named tokens carry intent; arbitrary values destroy it. Realistic reduction with these two levers alone is 50–60%, not 70%. If the user asks for a higher number, push back: the right answer is fewer tokens, not the same noise in className strings.

## The Eight Bugs You Will Hit (anticipate them)

1. **Value precedence bug.** When N tokens collapse to one canonical name, first-write-wins from parse order is unpredictable. The result is often the WRONG color (e.g., `--danger` ends up holding `--diagnostics-table-error-border` value, which is the pale border tint, not the bright red). **Fix:** add an explicit `CANONICAL_SOURCE` override dict mapping new tokens to a specific source token whose value should win.

2. **Scoped override bug.** `.dashboard-page { --text-inline: 14px; }` only works because `--text-inline` is a `var()`-referenced custom property. Tokens overridden in any scoped block (`.dashboard-page`, `.dark .dashboard-page`, etc.) MUST stay as tokens; deleting them silently breaks the scoped override.

3. **Intra-globals consumer bug.** Utility classes inside `globals.css` (e.g., `.dropdown-menu-highlight { padding: var(--spacing-dropdown-menu-padding); }`) read tokens that don't appear in any `.tsx` file. Deleting these from `@theme` produces a runtime-undefined CSS var. **Fix:** strip `@theme inline`/`:root`/`.dark`/etc. blocks from the CSS text before scanning, then collect every `var(--X)` ref in the remainder. Those tokens MUST stay.

4. **Category cross-pollination bug.** A suffix can appear in multiple categories. For example, `organization-section-surface` is a COLOR (`white`) AND a SHADOW alias prefix (`--shadow-organization-section-surface`). If your map has both `'organization-section-surface': 'card'` (color) and `'organization-section-surface': 'surface-soft'` (shadow), the second one will overwrite the bare-token rename in your global map. **Fix:** only the COLOR category renames the bare `--X` token. For SHADOW/SPACING/TEXT/RADIUS/FONT/TRACKING, rename ONLY the `--<theme-prefix>-X` alias, never the bare name.

5. **Aggressive icon-color collapse bug.** Collapsing every "grey icon" (#696969, #898989, #b3b3b3, #c1c1c1, #dddddd) to a single `--icon` token makes the originally-light icons look noticeably darker — and on dark surfaces (e.g., dropdown menus that stay dark in both modes), it inverts the intended contrast. **Fix:** keep TWO icon tones: `--icon` (~#696969 mid-grey) and `--icon-soft` (~#b3b3b3 light-grey). Map originally-light icons to `--icon-soft`.

6. **Surface-with-conditional-transparency bug.** Some tokens are `transparent` in one mode and a concrete color in the other (e.g., `--repository-card-panel: #ffffff` in light, `transparent` in dark — the dark version is intentionally see-through). Collapsing into `--card` makes the panel opaque in dark mode, visibly changing the layered look. **Fix:** if a token's value is `transparent` in one mode and concrete in the other, do NOT collapse it with an always-opaque token. Either keep it separate or inline the conditional logic in the consuming className.

7. **`bg-X` color/image collision bug.** Tailwind v4 resolves `bg-X` against BOTH `--color-X` (background-color) and `--background-image-X` (background-image). If only `--background-image-X` exists, `bg-X` paints the gradient correctly. But if you rename some OTHER token (e.g., `--install-button-text`) to `--install-button`, you create a `--color-install-button` alias — and now `bg-install-button` may set `background-color: white` on top of the gradient, making the button look empty/invisible. **Fix:** before collapsing a color suffix to name `X`, grep for `--background-image-X` and any `bg-X` class usage. If either exists, pick a different target name (e.g., keep `--install-button-text` instead of renaming to `--install-button`).

8. **Always-dark surface bug.** Tokens for dropdown menus, tooltips, popovers-that-stay-dark, etc., have text/icon colors that are LIGHT in BOTH light and dark modes (because the surface stays dark regardless of theme). Collapsing `--dropdown-menu-text` into `--foreground` makes the dropdown text dark in light mode (dark text on dark surface = invisible). **Fix:** before collapsing a token, diff its light-mode and dark-mode values. If both values are on the same side of the L=0.5 line (both light or both dark), it lives on an always-light or always-dark surface and CANNOT be collapsed with a flipping token like `--foreground` or `--icon`. Keep it as its own token.

## The Three-Pass Block Transformation

When emitting a `:root` or `.dark` block, write entries in THIS order:

```python
# Pass 1: canonical (non-renamed) entries — these set the source of truth.
for name, value in original_decls.items():
    target = TOKEN_RENAME.get(name)
    if target is None or target == name:
        out[name] = fix_var_refs(value)

# Pass 2: CANONICAL_SOURCE overrides — explicit pick for collapsed groups.
for new_token, source_token in CANONICAL_SOURCE.items():
    if source_token in original_decls:
        out[new_token] = fix_var_refs(original_decls[source_token])

# Pass 3: other renamed entries — only if the target isn't already set.
for name, value in original_decls.items():
    target = TOKEN_RENAME.get(name)
    if target and target != name and target not in out:
        out[target] = fix_var_refs(value)
```

This guarantees: (a) the canonical token's original value always wins over a rename, (b) you explicitly control which source provides the value for NEW tokens like `--danger`, and (c) duplicate entries never appear in the output.

## Apply-And-Verify Loop

Run this loop after EVERY rename-map change:

```bash
git checkout -- apps/web   # always start from a clean tree
python3 /tmp/transform.py  # apply the rename + inline map
pnpm typecheck && pnpm lint && pnpm format && pnpm --filter web build
```

If any check fails, fix the map (not the generated output), then re-run. Hand-editing the generated `globals.css` is a footgun: the next transformation run will overwrite your fix.

## Rationalization Table

| You will think | Don't |
|---|---|
| "I'll just delete this token, no one uses it" — without searching globals.css's own classes | Strip the @theme/:root/.dark blocks and search the remainder for `var(--X)` first |
| "These two greys are basically the same" — without checking BOTH light and dark mode values | Diff both modes. A value that's close in light can diverge in dark |
| "I'll inline single-use tokens into arbitrary values for extra reduction" | That's just relocating the noise. Keep named tokens; inlining is anti-consolidation |
| "User asked for 70% — I should hit it even if I have to inline" | Push back. 50–60% with named tokens beats 70% with arbitrary values. Report the honest number |
| "I'll fix the broken class manually after the script runs" | The next script run will revert your edit. Fix the script, not the artifact |
| "First-write-wins is fine, parse order is deterministic" | Until someone reorders `:root`. Use explicit `CANONICAL_SOURCE` overrides |
| "This rename target name is fine, no collisions" — but there's already a `--background-image-<name>` | Grep for `--background-image-<target>` and `bg-<target>` usage before picking the target name |

## Before Declaring Done

You MUST have:

1. Run `pnpm typecheck` — exit 0.
2. Run `pnpm lint` — 0 errors, 0 warnings.
3. Run `pnpm format` — completed.
4. Run `pnpm --filter web build` — exit 0.
5. Counted final tokens with `rg "^\s*--[a-z][a-zA-Z0-9-]*\s*:" apps/web/app/globals.css -o | sort -u | wc -l`. Report before/after counts and the percentage reduction.
6. Confirmed at least the top 3 visible surfaces (cards, page background, dropdowns) render with the intended colors by reading the resulting `:root` block end-to-end and verifying canonical values match what you expected.

A green build with broken visual output is a failed task. A counted reduction without verification is a failed task.
