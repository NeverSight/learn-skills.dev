---
name: data-gtm-datalayer
description: Generate production-ready GTM tracking code with dataLayer pushes and HTML attributes. Use when adding analytics tracking.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Edit(jaan-to/config/settings.yaml)
argument-hint: [prd-path | tracking-description | (interactive)]
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# data-gtm-datalayer

> Generate production-ready GTM tracking code with enforced naming conventions.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-data-gtm-datalayer.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_TEMPLATES_DIR/jaan-to-data-gtm-datalayer.template.md` - Output template
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Tracking Request**: $ARGUMENTS

- If PRD path provided → Read and suggest tracking points
- If text description provided → Design tracking based on input
- If empty → Start interactive wizard

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `data-gtm-datalayer`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_data-gtm-datalayer`

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Determine Input Mode

Check $ARGUMENTS:

**Mode A - PRD Input:**
If path to `$JAAN_OUTPUTS_DIR/` or PRD text provided:
1. Read/parse the PRD
2. Identify trackable interactions (buttons, forms, modals, etc.)
3. Suggest tracking points with types:
   - Impressions: modal displays, section visibility
   - Clicks: buttons, links, interactive elements
   - Include non-happy paths (close, dismiss, cancel)
4. Ask user to confirm/modify suggestions

**Mode B - Description Input:**
If text description of what to track:
1. Parse the description
2. Ask clarifying questions if needed
3. Suggest tracking structure

**Mode C - Interactive Wizard:**
If no arguments, ask questions in order:

### Question 1: Tracking Type
> "What type of tracking do you need?"
> 1. **click-html** - HTML attributes (data-al-*) for simple clicks
> 2. **click-datalayer** - dataLayer.push for flow-based clicks
> 3. **impression** - dataLayer.push for visibility/exposure events

### Question 2: Feature Name
> "What is the feature name? (e.g., player, checkout, onboarding)"

Apply naming rules:
- Convert to lowercase-kebab-case: "Play Button" → "play-button"
- If unclear (e.g., "btn1", "x"), ask: "What does '{input}' represent?"
- Suggest better name if abbreviated: "nav" → suggest "navigation" or "navbar"
- Confirm conversion: "Feature 'Play Button' → 'play-button' - OK? [y/edit]"

### Question 3: Item Name
> "What is the item name? (e.g., play, pause, submit, modal-purchase)"

Apply same naming rules as feature.

### Question 4: Action (click-datalayer only)
> "What is the action? (default: Click)"

If user provides custom action, apply naming rules.
If empty/skipped, use "Click".

### Question 5: Additional Params (optional)
> "Any additional params? Enter as key=value, one per line. (or 'skip')"

Example:
```
source=modal
count=3
active=true
```

Parse into object with **ES5 type detection**:
- `true` / `false` → bool (no quotes): `true`
- Numeric values (e.g., `3`, `42`) → int (no quotes): `3`
- Everything else → string (with quotes): `"modal"`

If none provided, omit params entirely from output.

## Step 2: Confirm Values

Show full dataLayer preview before generating:

**For click-html:**
```
TRACKING SUMMARY
────────────────────────────────────────

<button data-al-feature="{feature}" data-al-item="{item}">...</button>

────────────────────────────────────────
```

**For click-datalayer (without params):**
```
TRACKING SUMMARY
────────────────────────────────────────

dataLayer.push({
  event: "al_tracker_custom",
  al: {
    feature: "{feature}",
    item: "{item}",
    action: "{action}"
  },
  _clear: true
});

────────────────────────────────────────
```

**For click-datalayer (with params):**
```
TRACKING SUMMARY
────────────────────────────────────────

dataLayer.push({
  event: "al_tracker_custom",
  al: {
    feature: "{feature}",
    item: "{item}",
    action: "{action}",
    params: {
      source: "modal",
      count: 3,
      active: true,
    }
  },
  _clear: true
});

────────────────────────────────────────
```
Values are typed: strings in `"quotes"`, ints/bools without quotes.

**For impression (without params):**
```
TRACKING SUMMARY
────────────────────────────────────────

dataLayer.push({
  event: "al_tracker_impression",
  al: {
    feature: "{feature}",
    item: "{item}"
  },
  _clear: true
});

────────────────────────────────────────
```

**For impression (with params):**
```
TRACKING SUMMARY
────────────────────────────────────────

dataLayer.push({
  event: "al_tracker_impression",
  al: {
    feature: "{feature}",
    item: "{item}",
    params: {
      variant: "A",
      position: 1,
      visible: true,
    }
  },
  _clear: true
});

────────────────────────────────────────
```

> "Generate tracking code with these values? [y/edit]"

---

# HARD STOP - Human Review Check

Show the full dataLayer preview above (not just field summary).

> "Proceed with code generation? [y/n/edit]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 3: Generate Code

Based on tracking type, generate the appropriate code:

### Type: click-html

```html
<element data-al-feature="{feature}" data-al-item="{item}">{element content}</element>
```

Example output:
```html
<button data-al-feature="player" data-al-item="pause">Pause</button>
```

### Type: click-datalayer

Without params:
```javascript
dataLayer.push({
  event: "al_tracker_custom",
  al: {
    feature: "{feature}",
    item: "{item}",
    action: "{action}"
  },
  _clear: true
});
```

With params (ES5 typed values):
```javascript
dataLayer.push({
  event: "al_tracker_custom",
  al: {
    feature: "{feature}",
    item: "{item}",
    action: "{action}",
    params: {
      {key1}: {value1},  // string: "value", int: 3, bool: true
      {key2}: {value2},
    }
  },
  _clear: true
});
```

### Type: impression

Without params:
```javascript
dataLayer.push({
  event: "al_tracker_impression",
  al: {
    feature: "{feature}",
    item: "{item}"
  },
  _clear: true
});
```

With params (ES5 typed values):
```javascript
dataLayer.push({
  event: "al_tracker_impression",
  al: {
    feature: "{feature}",
    item: "{item}",
    params: {
      {key1}: {value1},  // string: "value", int: 3, bool: true
      {key2}: {value2},
    }
  },
  _clear: true
});
```

## Step 4: Quality Check

Before preview, verify:
- [ ] `event` key present in all dataLayer pushes
- [ ] Feature and item are non-empty strings
- [ ] Feature/item/action are lowercase-kebab-case
- [ ] No abbreviations without user clarification
- [ ] Names are descriptive and understandable
- [ ] User-provided strings preserved (after kebab conversion)
- [ ] `_clear: true` included in all dataLayer pushes
- [ ] No empty `params: {}` (omit entirely if no params)
- [ ] Param values use correct ES5 types (string in `"quotes"`, int/bool without)
- [ ] Output is deterministic (same input → same code)

If any check fails, fix before preview.

## Step 5: Preview & Approval

Display the generated code in conversation:

```
GENERATED TRACKING CODE
───────────────────────

{code block}

EXAMPLE WITH VALUES
───────────────────
{example showing real values based on user input}
```

> "Save tracking code to output? [y/n]"

## Step 5.5: Generate ID and Folder Structure

If approved, set up the output structure:

1. Source ID generator utility:
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
```

2. Generate sequential ID and output paths:
```bash
# Define subdomain directory
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/data/gtm"
mkdir -p "$SUBDOMAIN_DIR"

# Generate next ID
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")

# Create folder and file paths (slug from feature-item, e.g., "player-pause")
slug="{lowercase-hyphenated-feature-item}"
OUTPUT_FOLDER="${SUBDOMAIN_DIR}/${NEXT_ID}-${slug}"
MAIN_FILE="${OUTPUT_FOLDER}/${NEXT_ID}-gtm-${slug}.md"
```

3. Preview output configuration:
> **Output Configuration**
> - ID: {NEXT_ID}
> - Folder: $JAAN_OUTPUTS_DIR/data/gtm/{NEXT_ID}-{slug}/
> - Main file: {NEXT_ID}-gtm-{slug}.md

## Step 6: Write Output

1. Create output folder:
```bash
mkdir -p "$OUTPUT_FOLDER"
```

2. Write tracking code to main file using template:
```bash
# Use template from $JAAN_TEMPLATES_DIR/jaan-to-data-gtm-datalayer.template.md
cat > "$MAIN_FILE" <<'EOF'
{generated tracking documentation with Executive Summary}
EOF
```

3. Update subdomain index:
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Tracking Title}" \
  "{1-2 sentence summary: feature-item tracking with event type}"
```

4. Confirm completion:
> ✓ Tracking code written to: $JAAN_OUTPUTS_DIR/data/gtm/{NEXT_ID}-{slug}/{NEXT_ID}-gtm-{slug}.md
> ✓ Index updated: $JAAN_OUTPUTS_DIR/data/gtm/README.md

## Step 7: Capture Feedback

> "Any feedback? [y/n]"

If yes:
> "[1] Fix now  [2] Learn for future  [3] Both"

- **Option 1**: Update output, re-preview, re-write
- **Option 2**: Run `/jaan-to:learn-add data-gtm-datalayer "{feedback}"`
- **Option 3**: Do both

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Template-driven output structure
- Generic and tech-stack agnostic
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] User confirmed tracking values
- [ ] Code generated and displayed in conversation
- [ ] Markdown file written to `$JAAN_OUTPUTS_DIR/data/gtm/{slug}/`
- [ ] User can copy-paste and use immediately
