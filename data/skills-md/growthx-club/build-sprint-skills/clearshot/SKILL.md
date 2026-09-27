---
name: clearshot
description: "Structured screenshot analysis for UI implementation and critique. Analyzes every UI screenshot with a 5×5 spatial grid, full element inventory, and design system extraction — facts and taste together, every time. Escalates to full implementation blueprint when building. Trigger on any digital interface image file (png, jpg, gif, webp — websites, apps, dashboards, mockups, wireframes) or commands like 'analyse this screenshot,' 'rebuild this,' 'match this design,' 'clone this.' Skip for non-UI images (photos, memes, charts) unless the user explicitly wants to build a UI from them. Does NOT trigger on HTML source code, CSS, SVGs, or any code pasted as text."
---

## Preamble

Run this bash block first, before any analysis:

```bash
# ─── Find skill directory (works from any install path) ───────
_CS_DIR=""
for _d in ".claude/skills/clearshot" ".agents/skills/clearshot" "$HOME/.claude/skills/clearshot" "$HOME/.agents/skills/clearshot"; do
  [ -f "$_d/SKILL.md" ] && _CS_DIR="$(cd "$_d" && pwd)" && break
done
# fallback: search
[ -z "$_CS_DIR" ] && _CS_DIR="$(cd "$(dirname "$(find "$HOME/.claude" "$HOME/.agents" -name SKILL.md -path '*/clearshot/*' -print -quit 2>/dev/null)")" 2>/dev/null && pwd || echo "")"
_CS_VER=""
[ -n "$_CS_DIR" ] && [ -f "$_CS_DIR/VERSION" ] && _CS_VER="$(cat "$_CS_DIR/VERSION" | tr -d '[:space:]')"
_CS_STATE="$HOME/.clearshot"
mkdir -p "$_CS_STATE/analytics" "$_CS_STATE/feedback"

# ─── First-run detection ─────────────────────────────────────
_CS_FIRST_RUN="no"
[ ! -f "$_CS_STATE/config.yaml" ] && _CS_FIRST_RUN="yes"

# ─── Read config (only if it exists) ─────────────────────────
_CS_UPDATE_MODE="ask"
_CS_TEL="off"
_CS_TEL_PROMPTED="no"
if [ -f "$_CS_STATE/config.yaml" ]; then
  _CS_UPDATE_MODE=$(grep -E '^update_mode:' "$_CS_STATE/config.yaml" 2>/dev/null | awk '{print $2}' | tr -d '[:space:]' || echo "ask")
  _CS_TEL=$(grep -E '^telemetry:' "$_CS_STATE/config.yaml" 2>/dev/null | awk '{print $2}' | tr -d '[:space:]' || echo "off")
fi
[ -f "$_CS_STATE/.telemetry-prompted" ] && _CS_TEL_PROMPTED="yes"

# ─── Version check (only if user opted into updates) ─────────
# No network calls until config exists and user has chosen
if [ -n "$_CS_VER" ] && [ "$_CS_FIRST_RUN" = "no" ] && [ -d "$_CS_DIR/.git" ]; then
  _CS_CACHE="$_CS_STATE/last-update-check"
  _STALE=""
  [ -f "$_CS_CACHE" ] && _STALE=$(find "$_CS_CACHE" -mmin +60 2>/dev/null || true)
  if [ ! -f "$_CS_CACHE" ] || [ -n "$_STALE" ]; then
    _CS_REMOTE=$(curl -sf --max-time 5 "https://raw.githubusercontent.com/udayanwalvekar/clearshot/main/VERSION" 2>/dev/null | tr -d '[:space:]' || true)
    if echo "$_CS_REMOTE" | grep -qE '^[0-9]+\.[0-9.]+$' 2>/dev/null; then
      if [ "$_CS_VER" != "$_CS_REMOTE" ]; then
        if [ "$_CS_UPDATE_MODE" = "always" ]; then
          cd "$_CS_DIR" && git pull origin main --quiet 2>/dev/null
          _CS_VER="$(cat "$_CS_DIR/VERSION" 2>/dev/null | tr -d '[:space:]')"
          echo "CS_AUTO_UPDATED: $_CS_VER"
          echo "UP_TO_DATE $_CS_VER" > "$_CS_CACHE"
        else
          echo "UPGRADE_AVAILABLE $_CS_VER $_CS_REMOTE" > "$_CS_CACHE"
          echo "CS_UPGRADE: UPGRADE_AVAILABLE $_CS_VER $_CS_REMOTE"
        fi
      else
        echo "UP_TO_DATE $_CS_VER" > "$_CS_CACHE"
      fi
    fi
  else
    _CACHED="$(cat "$_CS_CACHE" 2>/dev/null || true)"
    case "$_CACHED" in UPGRADE_AVAILABLE*)
      if [ "$_CS_UPDATE_MODE" = "always" ]; then
        cd "$_CS_DIR" && git pull origin main --quiet 2>/dev/null
        _CS_VER="$(cat "$_CS_DIR/VERSION" 2>/dev/null | tr -d '[:space:]')"
        echo "CS_AUTO_UPDATED: $_CS_VER"
        echo "UP_TO_DATE $_CS_VER" > "$_CS_CACHE"
      else
        echo "CS_UPGRADE: $_CACHED"
      fi
      ;;
    esac
  fi
fi

# ─── Session tracking ────────────────────────────────────────
_CS_SESSION_ID="$$-$(date +%s)"
_CS_TEL_START=$(date +%s)

echo "CS_FIRST_RUN: $_CS_FIRST_RUN"
echo "CS_SKILL_DIR: $_CS_DIR"
echo "CS_UPDATE_MODE: $_CS_UPDATE_MODE"
echo "CS_TEL_PROMPTED: $_CS_TEL_PROMPTED"
echo "CS_TELEMETRY: ${_CS_TEL:-off}"
echo "CS_SESSION_ID: $_CS_SESSION_ID"
echo "CS_TEL_START: $_CS_TEL_START"
echo "CS_VERSION: ${_CS_VER:-unknown}"
```

### Interpreting preamble output

**If `CS_FIRST_RUN` is `yes`:**
This is the first time clearshot is running — no config exists yet. Before doing any analysis, tell the user to run the onboarding setup. Say something brief like:

"clearshot needs a quick first-run setup (two questions, arrow keys + enter):"

Then instruct them to type: `! {CS_SKILL_DIR}/bin/onboarding.sh`

Use the actual `CS_SKILL_DIR` value from the preamble output (e.g. `~/.claude/skills/clearshot` or `~/.agents/skills/clearshot`). The script asks about update preference and telemetry, writes the config, and completes in seconds.

After the user runs it, proceed with the analysis. If the user declines, proceed anyway — no network calls will happen without config.

**If `CS_AUTO_UPDATED` appears:**
The skill auto-updated itself. Mention it briefly: "clearshot updated to v{version}" and continue with the analysis. No action needed.

**If `CS_UPGRADE` shows `UPGRADE_AVAILABLE <old> <new>`:**
The user has `update_mode: ask`. Tell them a new version is available and instruct them to run the interactive update picker:

"clearshot v{new} is available (you're on v{old}):"

Then instruct them to type: `! {CS_SKILL_DIR}/bin/update-prompt.sh {old} {new}`

The script lets them choose "Update now" or "Always update" (which also switches to auto-update mode for the future). If the user skips it, continue with the analysis on the current version.

**If `CS_TEL_PROMPTED` is `no` (but `CS_FIRST_RUN` is also `no`):**
The user has a config but somehow skipped the telemetry question. Tell them to run:

`! {CS_SKILL_DIR}/bin/telemetry-setup.sh`

After the user runs it, proceed with the analysis. If the user declines, proceed anyway with telemetry off.

# Screenshot analysis

When an LLM looks at a screenshot and tries to go directly from pixels to code (or feedback or a description), it loses spatial relationships, misreads component hierarchy, and hallucinates design details. The fix: build a structured intermediate representation between "seeing the image" and "responding about it." That intermediate layer is what this skill provides.

## Gate check

Not every image needs this skill.

**Ask two questions before doing anything:**

1. Is this image a digital interface? (websites, apps, dashboards, mockups, wireframes, Figma exports, CLI with UI context, browser DevTools with a visible page all count. Photos, memes, standalone charts, presentation slides, documents, handwritten notes do not.)

2. Is the conversation about building, debugging, designing, or evaluating UI?

**Three outcomes:**

- Neither is true: exit the skill entirely. Respond normally. Don't mention this framework.
- Image is not a UI, but the conversation IS about building UI (e.g. "build me a page that feels like this photo"): the image is inspiration, not a spec. Describe what it communicates — mood, texture, weight — and move on. No structured analysis.
- Image IS a UI and the conversation is about building/evaluating: proceed with the analysis levels below.

## Analysis levels

Every analysis combines facts and taste. There is no separate "analytical mode" or "qualitative mode" — every observation is grounded in specifics (hex values, pixel measurements) AND includes how it feels (hierarchy, weight, cohesion). This mirrors how a senior designer thinks: feel first, then investigate why, always both.

### Level 1: Map (always runs)

Divide the screenshot into a **5×5 grid**. For each occupied region: what section lives there (nav, hero, sidebar, content, footer, modal, drawer, empty space), its approximate size relative to viewport, and how it relates to neighbors.

For every visible element, capture: type (button, input, card, image, icon, text, link, toggle, dropdown, tab, badge, avatar, table, chart, etc.), label/content (exact visible text), position (grid region + relative placement), state (default, hover, active, disabled, selected, error, loading, focused), size (pixel estimate), background color (hex), text color (hex), border (visible/none + radius in px), shadow (none/sm/md/lg), icon if present. Group by section.

Also note: where the eye goes first. Whether the layout breathes or feels cramped. Whether the hierarchy is clear or competing. What feels intentional vs accidental.

### Level 2: System (always runs)

Extract the design system behind what's visible:

**Colors:** page bg, card/surface bg, primary action, secondary, text primary, text secondary/muted, border/divider, accent, destructive, success. All hex values. Note whether the palette feels cohesive or patchwork — is there a clear system or are colors ad hoc?

**Typography:** heading style (size in px, weight, case), body text (size, weight, line-height), caption/small text, font family if identifiable. Note whether the type scale feels intentional — do sizes step consistently or jump randomly?

**Spacing and shape:** spacing pattern (tight 4-8px / comfortable 12-16px / spacious 24-32px+), border radius pattern (sharp 0-2px / subtle 4-6px / rounded 8-12px / pill), overall density (compact / comfortable / spacious). Note whether spacing is consistent or inconsistent across sections.

### Level 3: Blueprint (escalates when building)

This level runs when the user needs to implement, rebuild, or clone the UI from the screenshot. The LLM should escalate to Level 3 when the conversation involves writing code from this screenshot.

**Layout architecture:** page layout pattern (single column, sidebar+content, dashboard grid, centered container, full-bleed), content layout per section (flex row, flex column, CSS grid with column count, stack), container width (max-width constrained vs full-width), responsive context (mobile <640px / tablet 640-1024px / desktop >1024px), scroll clues (content cut off, sticky header, fixed bottom bar), z-index layers (overlays, modals, dropdowns, toasts).

**Interaction map:** primary CTA (the single most important action), secondary actions, navigation pattern (top nav, side nav, tabs, breadcrumbs, bottom bar), form elements and grouping, data display patterns (tables, card grids, lists), visible states (loading, empty, error, success). Note where a user would hesitate or feel friction, and what feels polished.

## Output

Match the output to the context. Don't force headers and sections when a paragraph will do.

**Critique/feedback:** lead with what's wrong or what needs attention. Ground each observation in specifics (the exact hex, spacing, or element causing the problem) and how it affects the experience. Don't catalog everything — focus on what matters.

**Implementation spec (Level 3):** structured output with section headers — layout map, elements by section, design tokens, layout architecture, interaction map. This is the build document.

**Comparison (two screenshots):** what changed, what improved, what regressed, what still needs work.

## Core principles

**Be specific.** "A dashboard with some cards" is never acceptable. "3-column grid, ~280px cards, #F9FAFB bg, 8px radius, subtle shadow — the cards feel weightless, almost floating" is. Every observation needs both the measurement and the judgment.

**Hex over color names, pixels over vague sizes.** Say #3B82F6 not "blue." Say ~16px not "some." If uncertain, give your best estimate and note it.

**Group by section, not by element type.** The nav's elements belong together. Don't lump all buttons across the page into one list.

**Call out the non-obvious.** Custom illustrations, unusual component patterns, implied animations, dynamic vs static data. These are the things that break implementations.

**Match the user's pace.** Rapid iteration = concise output. Detailed clone request = exhaustive. But the analysis depth (Levels 1+2) is always the same — what changes is how much you output, not how much you see.

## Self-rating

### Internal, silent, every time

After completing any analysis, rate your own output 0-10 across these criteria: spatial accuracy (did the grid correctly map the layout?), specificity (are colors hex, sizes pixel-estimated, components precisely named?), level selection (did the right levels run?), taste (did you catch what feels off, not just what's measurably wrong?), actionability (could someone act on this analysis?). Average the scores.

This rating is strictly internal. It flows into telemetry as the `RATING` field in the epilogue, but it is never shown to the user. Displaying a score after every analysis is noisy and self-congratulatory.

### When to surface feedback

There are exactly three situations where the skill should involve the user in quality feedback. Outside of these, stay quiet.

**Trigger 1: User correction.** If the user corrects the analysis — "no, that's wrong," "you missed the nav," "the padding is off" — fix the issue, then note briefly: "logged that miss so clearshot gets better at catching [the specific thing]." Automatically write a field report (see below).

**Trigger 2: After a rebuild completes.** If Level 3 ran and the implementation is done, ask one casual question: "clearshot nailed it or missed something? just curious." One shot. Not a form.

**Trigger 3: Session wind-down.** If 3 or more analyses happened in a single session and the conversation is winding down, append: "ran clearshot X times this session. anything it kept getting wrong?" Only if 3+ analyses occurred. Never mid-flow.

**Never trigger feedback:** during rapid iteration, after every single analysis, or when the user is clearly in flow.

### Field reports

Write to `~/.clearshot/feedback/YYYY-MM-DD-{slug}.md`, only when:

- **User correction**: automatic. Format:

```
# {Title describing the miss}
**What was analyzed:** {screenshot description}
**Levels run:** {1,2 or 1,2,3}
**What was missed:** {specific element or detail the user corrected}
**Correction:** {what the user said}
**Internal rating:** {X}/10
**Date:** {YYYY-MM-DD} | **Version:** {version from preamble}
```

- **User explicitly says something was wrong** (via trigger 2 or 3 response): write a field report with the user's feedback included.

- **Internal rating below 5**: write a field report silently.

Field reports are never written for routine analyses that went fine.

## Epilogue

After analysis is complete, log the event. Substitute actual values for the placeholder variables.

```bash
_CS_TEL_END=$(date +%s)
_CS_DUR=$(( _CS_TEL_END - _CS_TEL_START ))
_CS_TEL_MODE=$(grep -E '^telemetry:' "$HOME/.clearshot/config.yaml" 2>/dev/null | awk '{print $2}' | tr -d '[:space:]' || echo "off")
if [ "$_CS_TEL_MODE" != "off" ]; then
  _CS_OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
  _CS_ARCH="$(uname -m)"
  _CS_INSTALL_ID="$(printf '%s-%s' "$(hostname)" "$(whoami)" | shasum -a 256 | awk '{print $1}')"
  _CS_ID_JSON="\"$_CS_INSTALL_ID\""
  printf '{"v":1,"ts":"%s","version":"%s","os":"%s","arch":"%s","duration_s":%s,"outcome":"%s","levels_run":"%s","self_rating":%s,"installation_id":%s}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "CS_VERSION" "$_CS_OS" "$_CS_ARCH" \
    "$_CS_DUR" "OUTCOME" "LEVELS_RUN" "RATING" "$_CS_ID_JSON" \
    >> "$HOME/.clearshot/analytics/usage.jsonl" 2>/dev/null || true

  # Sync to Convex (rate-limited, background)
  _CS_CONVEX_URL=""
  for _csd in "$HOME/.claude/skills/clearshot" "$HOME/.agents/skills/clearshot"; do
    [ -f "$_csd/config.sh" ] && _CS_CONVEX_URL="$(grep -E '^CS_CONVEX_URL=' "$_csd/config.sh" 2>/dev/null | cut -d'"' -f2 || true)" && break
  done
  if [ -n "$_CS_CONVEX_URL" ] && [ "$_CS_CONVEX_URL" != "https://placeholder.convex.site" ]; then
    _CS_RATE="$HOME/.clearshot/analytics/.last-sync-time"
    _CS_SYNC_STALE=$(find "$_CS_RATE" -mmin +5 2>/dev/null || echo "sync")
    if [ ! -f "$_CS_RATE" ] || [ -n "$_CS_SYNC_STALE" ]; then
      _CS_CURSOR_FILE="$HOME/.clearshot/analytics/.last-sync-line"
      _CS_CURSOR=$(cat "$_CS_CURSOR_FILE" 2>/dev/null | tr -d '[:space:]' || echo "0")
      _CS_TOTAL=$(wc -l < "$HOME/.clearshot/analytics/usage.jsonl" 2>/dev/null | tr -d ' ' || echo "0")
      if [ "$_CS_CURSOR" -lt "$_CS_TOTAL" ] 2>/dev/null; then
        _CS_SKIP=$(( _CS_CURSOR + 1 ))
        _CS_BATCH=$(tail -n "+$_CS_SKIP" "$HOME/.clearshot/analytics/usage.jsonl" | head -100)
        _CS_JSON_BATCH="[$(echo "$_CS_BATCH" | paste -sd ',' -)]"
        _CS_HTTP=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
          -X POST "$_CS_CONVEX_URL/telemetry" \
          -H "Content-Type: application/json" \
          -d "$_CS_JSON_BATCH" 2>/dev/null || echo "000")
        case "$_CS_HTTP" in 2*) echo $(( _CS_CURSOR + $(echo "$_CS_BATCH" | wc -l | tr -d ' ') )) > "$_CS_CURSOR_FILE" ;; esac
        touch "$_CS_RATE" 2>/dev/null || true
      fi
    fi
  fi
fi
```

Replace these placeholders with actual values from the analysis:
- `_CS_TEL_START` — the value from preamble output
- `CS_VERSION` — the version from preamble output
- `OUTCOME` — "success", "error", or "abort"
- `LEVELS_RUN` — "1,2" or "1,2,3"
- `RATING` — the self-rating number (0-10)
