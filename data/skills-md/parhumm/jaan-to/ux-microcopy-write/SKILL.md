---
name: ux-microcopy-write
description: Generate multi-language microcopy packs for UI components with cultural adaptation. Use when writing UI text and translations.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/ux/**), Write($JAAN_CONTEXT_DIR/localization.md), Write($JAAN_CONTEXT_DIR/tone-of-voice.md), WebSearch, Task, AskUserQuestion, Bash(source:*), Bash(mkdir:*), Edit(jaan-to/config/settings.yaml)
argument-hint: [initiative-or-feature-description]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# ux-microcopy-write

> Generate multi-language microcopy packs for UI components.

## Context Files

- `$JAAN_CONTEXT_DIR/config.md` - Configuration
- `$JAAN_CONTEXT_DIR/localization.md` - Language preferences (auto-created if missing)
- `$JAAN_CONTEXT_DIR/tone-of-voice.md` - Tone guidelines (auto-created if missing)
- `$JAAN_TEMPLATES_DIR/jaan-to-ux-microcopy-write.template.md` - Output template
- `$JAAN_LEARN_DIR/jaan-to-ux-microcopy-write.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` - Per-language rules, export templates, JSON schema, output format, definition of done

## Input

**Initiative**: $ARGUMENTS

IMPORTANT: The initiative/feature description above is your input. Use it directly. Do NOT ask for the initiative again.

**Optional**: Screenshot paths can be provided to show UI elements where copy appears. Images will be embedded in the output as `![UI Context - {category}](resolved-path)`.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `ux-microcopy-write`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_ux-microcopy-write`

> **Language exception**: This setting controls only plugin conversation language. The multi-language microcopy output is independently controlled by `$JAAN_CONTEXT_DIR/localization.md` and this skill's own Language Selection step.

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Language Selection

Check if language preferences already exist:

Use Read tool on: `$JAAN_CONTEXT_DIR/localization.md`

**If file exists**:
- Show current enabled languages
- Use AskUserQuestion:
  - Question: "Use saved language preferences or modify?"
  - Header: "Languages"
  - Options:
    - "Use saved" — Use languages from localization.md
    - "Modify" — Let me change the language selection

**If file does NOT exist OR user selected "Modify"**:

Show available languages:
- **EN** (English) - LTR, Latin
- **FA** (فارسی / Persian) - RTL, Perso-Arabic
- **TR** (Türkçe / Turkish) - LTR, Latin
- **DE** (Deutsch / German) - LTR, Latin (+30-35% text expansion)
- **FR** (Français / French) - LTR, Latin (+15-25% text expansion)
- **RU** (Русский / Russian) - LTR, Cyrillic (3-form pluralization)
- **TG** (Тоҷикӣ / Tajik) - LTR, Cyrillic

Use AskUserQuestion:
- Question: "Which languages do you need microcopy for?"
- Header: "Language Selection"
- Options:
  - "All 7" — Generate for all languages
  - "Common Set (EN, FA, TR)" — Most requested trio
  - "Custom" — Let me select specific languages

If "Custom" selected:
- Ask: "Enter comma-separated language codes (e.g., en,fa,de,ru)"
- Parse and validate codes
- Show selected languages for confirmation

**Write language preferences to**: `$JAAN_CONTEXT_DIR/localization.md`
- Use template structure from seed file
- Mark enabled languages
- Include RTL handling notes for Persian

## Step 2: Tone-of-Voice Discovery

Check if tone preferences already exist:

Use Read tool on: `$JAAN_CONTEXT_DIR/tone-of-voice.md`

**If file exists**:
- Show current tone profile
- Use AskUserQuestion:
  - Question: "Use saved tone-of-voice or modify?"
  - Header: "Tone"
  - Options:
    - "Use saved" — Use tone from tone-of-voice.md
    - "Modify" — Let me change the tone profile

**If file does NOT exist OR user selected "Modify"**:

Use AskUserQuestion:
- Question: "What tone should the microcopy have?"
- Header: "Tone Profile"
- Options:
  - "Professional & Formal" — Banking, B2B, enterprise (Sie, Вы, شما formal pronouns)
  - "Friendly & Conversational" — Consumer apps, social (du, ты, تو informal pronouns)
  - "Sample-based" — I'll provide example text to match

If "Sample-based" selected:
- Ask: "Provide 2-3 example sentences from your current UI"
- Analyze tone characteristics:
  - Formality level (formal/semi-formal/informal)
  - Warmth (warm/neutral/direct)
  - Directness (specific/general)
  - Emotion (empathetic/neutral/celebratory)
- Show extracted tone profile:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Tone Profile Detection Template" for the display template with formality, warmth, directness, emotion levels and language-specific pronouns.
- Ask: "Use this tone profile? [y/n]"
- If no, ask again for refinement

**Write tone profile to**: `$JAAN_CONTEXT_DIR/tone-of-voice.md`
- Use template structure from seed file
- Include language-specific formality rules
- Add example microcopy for reference

## Step 3: Category Detection & Selection

Analyze initiative/feature description for microcopy needs using keyword detection:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Category Detection Rules" for keyword-to-category mapping rules.

Show detected categories + additional common ones:
```
SMART CATEGORY DETECTION
────────────────────────
Based on your initiative, I detected these categories:
✓ {detected category 1}
✓ {detected category 2}
✓ {detected category 3}

Additional common categories:
○ {suggested category 1}
○ {suggested category 2}
```

**Available microcopy categories** (11 total):

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Microcopy Categories Catalog" for the full list of 11 categories with descriptions.

Use AskUserQuestion:
- Question: "Which categories do you need?"
- Header: "Categories"
- Options:
  - "Detected set" — Use auto-detected categories
  - "Core set" — Labels, Errors, CTAs, Success (4 categories)
  - "Full set" — All 11 categories
  - "Custom" — Let me select specific categories

If "Custom" selected:
- Show checklist of all 11 categories
- Ask for comma-separated list or numbered selection
- Confirm selected categories

## Step 4: Item Inventory

For each selected category, build inventory of items needed:

**For each category**, show common examples and ask:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Category Item Examples" for common examples per category (Labels & Buttons, Error Messages, etc.) to show users when building inventory.

If screenshot paths were provided, read images to identify visible UI elements needing copy and inform category/item selection.

After gathering counts, build complete inventory list:
```
ITEM INVENTORY
──────────────
Labels & Buttons: 8 items
Error Messages: 5 items
Success Messages: 3 items
CTAs: 6 items

Total: 22 items across 4 categories
```

---

# HARD STOP - Human Review Check

Show complete plan before proceeding:

```
MICROCOPY GENERATION PLAN
──────────────────────────
Languages: {list with native names} ({n} languages)
Tone Profile: {tone summary}
Categories: {selected categories} ({n} categories)
Total Items: {count} items

Process:
1. Generate 3 English options per item
2. Iterate up to 5 rounds if needed
3. Support custom user input
4. Translate to all {n} languages
5. Cultural adaptation per language
6. RTL handling for Persian
7. Quality validation checklist

Output Files:
- $JAAN_OUTPUTS_DIR/ux/content/{id}-{slug}/{id}-microcopy-{slug}.md
- $JAAN_OUTPUTS_DIR/ux/content/{id}-{slug}/{id}-microcopy-{slug}.json
```

Use AskUserQuestion:
- Question: "Proceed with microcopy generation?"
- Header: "Proceed"
- Options:
  - "Yes" — Start generating microcopy
  - "Edit" — Let me modify the plan
  - "No" — Cancel

If "Edit": Return to appropriate step based on user feedback

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 5: Generate Microcopy (Per Item, Per Category)

For each item in inventory:

### 5.1: Show Context

```
GENERATING ITEM {current}/{total}
──────────────────────────────────
Category: {category_name}
Item Type: {item_description}
Tone: {tone_profile}
```

### 5.2: Initial English Generation

Generate 3 options in English following best practices:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Generation Best Practices" for per-category guidelines (Error Messages, CTAs/Labels, Empty States, Success Messages) with structure patterns and examples.

Show 3 options to user:
```
Option 1: {text1}
Option 2: {text2}
Option 3: {text3}
```

### 5.3: Options Iteration Loop

Use AskUserQuestion:
- Question: "Which option do you prefer?"
- Header: "Select Option"
- Options:
  - "Option 1" — Use first option
  - "Option 2" — Use second option
  - "Option 3" — Use third option
  - "My own" — I'll write my own version
  - "More" — Show 3 more options

**If "My own" selected**:
1. Ask: "Enter your custom text:"
2. Show: "Your text: {user_text}"
3. Generate 3 more options in same style/tone
4. Show: "Here are 3 variations in the same style:"
   - Option A: {variation1}
   - Option B: {variation2}
   - Option C: {variation3}
5. Use AskUserQuestion with 5 options:
   - "Use my text" — Use exact user text
   - "Option A/B/C" — Use variation
   - "More" — Generate 3 more variations
6. Loop back to selection

**If "More" selected**:
1. Increment round counter
2. If round <= 5:
   - Generate 3 NEW options (different from previous)
   - Show options
   - Loop back to selection
3. If round > 5:
   - Show: "⚠️ Last round of suggestions"
   - Generate 3 final options
   - Add emphasis: "Or select 'My own' to write your own text"
   - Loop back to selection

**If "Option 1/2/3" selected**:
- Save as approved English version
- Proceed to Step 5.4

### 5.4: Multi-Language Translation

For each selected language, translate approved English text with cultural adaptation:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Per-Language Translation Rules" for full per-language rules (pronouns, punctuation, text expansion, script/direction).

Apply the language-specific rules from the reference to each translation. Store translations in memory for output generation.

### 5.5: Track Progress

After each item completed, show:
```
✓ Item {current}/{total} completed
  Category: {category}
  EN: {english_text}
  Translated to {n} languages
```

Continue loop until all items completed.

## Step 6: Quality Validation Checklist

Before writing output, validate all generated microcopy:

**Universal Checks**:
- [ ] All {n} items have all {n} languages
- [ ] Tone consistency across all items (formal/informal pronouns consistent)
- [ ] Grammar check for each language (use WebSearch if uncertain)
- [ ] Reading level 7-8th grade (English baseline)
- [ ] No ambiguous language
- [ ] Error messages include recovery instructions
- [ ] If screenshots provided: UI context images embedded with `![alt](...)` syntax and URL-encoded paths

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Quality Validation: Language-Specific Checks" for per-language and cultural adaptation checklists.

If any check fails:
- Fix issues
- Re-validate
- Continue when all checks pass

## Step 7: Preview Output

Source ID generator and generate next ID:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/ux/content"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
```

Generate slug from feature name:
- Lowercase
- Replace spaces/special chars with hyphens
- Max 50 characters
- Example: "User Authentication" → "user-authentication"

Generate executive summary:
```
Multi-language microcopy pack for {feature_name} covering {n} categories ({category_list}) in {n} languages ({language_list}). Includes culturally-adapted copy with RTL support for Persian/Farsi and tone-of-voice consistency across all languages.
```

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Output Preview Format" for the complete preview template with metadata, category items, character counts, and native speaker warning.

Use AskUserQuestion:
- Question: "Write these output files?"
- Header: "Write"
- Options:
  - "Approve" — Write output files
  - "Revise" — Let me modify specific items
  - "Cancel" — Don't write

If "Revise": Loop back to Step 5 for specific items

## Step 7.7: Resolve & Copy Assets

If screenshot paths were provided:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/asset-embedding-reference.md` for the asset resolution protocol (path detection, copy rules, markdown embedding).

Source `${CLAUDE_PLUGIN_ROOT}/scripts/lib/asset-handler.sh`. For each screenshot: check `is_jaan_path` — if inside `$JAAN_*`, reference in-place; if external, ask user before copying. Use `resolve_asset_path` for markdown-relative paths.

## Step 8: Write Output Files

If approved:

### 8.1: Create Folder Structure

```bash
OUTPUT_FOLDER="$JAAN_OUTPUTS_DIR/ux/content/${NEXT_ID}-${slug}"
mkdir -p "$OUTPUT_FOLDER"
```

### 8.2: Write Main File

Write to: `$OUTPUT_FOLDER/${NEXT_ID}-microcopy-${slug}.md`

Use template from: `$JAAN_TEMPLATES_DIR/jaan-to-ux-microcopy-write.template.md`

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Main File Sections" for the complete list of sections to fill (title, summary, metadata, warnings, localization, tone, items, exports, validation).

### 8.3: Write JSON File

Write to: `$OUTPUT_FOLDER/${NEXT_ID}-microcopy-${slug}.json`

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "JSON Output Structure" for the complete JSON schema with metadata, translations, direction, and script fields.

### 8.4: Update Subdomain Index

Source index updater:
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
```

Add to index:
```bash
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Feature Name}" \
  "{Executive Summary from Step 7}"
```

### 8.5: Confirm Write

Show confirmation:
```
✅ MICROCOPY PACK CREATED
─────────────────────────
ID: {NEXT_ID}
Folder: $JAAN_OUTPUTS_DIR/ux/content/{NEXT_ID}-{slug}/
Main: {NEXT_ID}-microcopy-{slug}.md
JSON: {NEXT_ID}-microcopy-{slug}.json
Index: Updated $JAAN_OUTPUTS_DIR/ux/content/README.md

Total Items: {n} items across {n} categories in {n} languages
```

## Step 9: Export Formats (Optional)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Export Format Templates" for React i18next, Vue i18n, and ICU MessageFormat examples with installation and usage code.

Show export format examples from the reference to the user, tailored to their generated microcopy data.

## Step 10: Feedback Capture

Use AskUserQuestion:
- Question: "Any feedback on the microcopy pack?"
- Header: "Feedback"
- Options:
  - "No" — All good, done
  - "Fix now" — Update specific items
  - "Learn" — Save lesson for future runs
  - "Both" — Fix now AND save lesson

**If "Fix now" or "Both"**:
1. Ask: "Which items need changes? (Specify by category + item name)"
2. For each item:
   - Show current text in all languages
   - Loop back to Step 5 for that item
   - Regenerate translations
   - Update output files
3. Show updated output
4. Re-ask for feedback

**If "Learn" or "Both"**:
1. Ask: "What lesson should I remember for future microcopy generations?"
2. Run: `/jaan-to:learn-add ux-microcopy-write "{feedback}"`
3. Confirm: "Lesson saved to LEARN.md"

**If "No"**:
- Confirm completion

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Template-driven output structure
- Generic across platforms and design systems
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/ux-microcopy-write-reference.md` section "Definition of Done" for the complete 14-item checklist (language prefs, tone, categories, languages, validation, ID, files, index, review warning, exports, approval).
