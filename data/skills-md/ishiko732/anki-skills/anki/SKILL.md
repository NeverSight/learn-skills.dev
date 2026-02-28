---
name: anki
description: "Use this skill when users want to work with Anki flashcards. This includes: creating/managing decks, adding flashcards (from text, PDF, CSV, Excel), creating note templates/models, checking Anki connection status, viewing study statistics and review history, or generating flashcards from any source material using spaced repetition best practices."
---

# Anki Skill

Manage Anki flashcards via [AnkiConnect](https://github.com/FooSoft/anki-connect) HTTP API.

---

## ⛔ MANDATORY: Pre-Add Checklist (READ THIS FIRST)

**You MUST NOT call `addNote` or `addNotes` until ALL steps below are completed. No exceptions. No defaults. No shortcuts.**

### Agent Mode Exception

When called by the `anki-flashcard-generator` agent (or any automated agent), skip the interactive checklist below. Instead:
1. Read deck and model from `.claude/anki.json` config (create with defaults `{"deck": "program::claude", "model": "Basic"}` if missing)
2. Call `modelFieldNames` to verify the configured model's fields
3. Proceed directly with `addNotes` — no user confirmation needed

### Interactive Mode (User-Initiated)

**Step 1 — Fetch available models:**
Call `modelNames` to get the full list of note types from the user's Anki.

**Step 2 — Ask the user to choose a model:**
Present the available models to the user via `AskUserQuestion` and let them pick one. NEVER default to "Basic" or any other model without explicit user selection.

**Step 3 — Verify field mapping:**
After the user selects a model, call `modelFieldNames` with that model to inspect its fields. Map the card content to the correct fields and show the mapping to the user for confirmation.

**Step 4 — Confirm deck, model, and tags:**
Present a final summary of deck name, chosen model, field mapping, and tags. Wait for user approval before proceeding.

**Only after the user explicitly confirms ALL of the above may you call `addNote` or `addNotes`.**

Skipping any step (e.g., adding cards without asking for model selection) is a rule violation.

---

## Prerequisites

1. **Anki** desktop must be running
2. **AnkiConnect** plugin installed (code: `2055492159`)
   - In Anki: `Tools → Add-ons → Get Add-ons…` → enter `2055492159`

## Helper Script

### macOS / Linux (Bash)

`scripts/anki-connect.sh` wraps `curl` for convenience:

```bash
# Basic usage
bash scripts/anki-connect.sh <action> [params_json]

# Examples
bash scripts/anki-connect.sh version
bash scripts/anki-connect.sh deckNames
bash scripts/anki-connect.sh createDeck '{"deck":"MyDeck"}'
```

### Windows (PowerShell)

`scripts/anki-connect.ps1` wraps `Invoke-RestMethod` for convenience:

```powershell
# Basic usage
pwsh scripts/anki-connect.ps1 <action> [params_json]

# Examples
pwsh scripts/anki-connect.ps1 version
pwsh scripts/anki-connect.ps1 deckNames
pwsh scripts/anki-connect.ps1 createDeck '{"deck":"MyDeck"}'
```

### Platform Detection

Choose the correct script based on the current OS:
- **Windows** (`$env:OS -eq 'Windows_NT'` or `os.platform() === 'win32'`): use `anki-connect.ps1`
- **macOS / Linux**: use `anki-connect.sh`

Override the endpoint with `ANKI_CONNECT_URL` env var (default: `http://127.0.0.1:8765`).

You can also call AnkiConnect directly with `curl`:

```bash
curl -s http://127.0.0.1:8765 -X POST -d '{"action":"version","version":6}'
```

## API Reference

All requests use POST to `http://127.0.0.1:8765` with JSON body:
```json
{"action": "<action>", "version": 6, "params": { ... }}
```

Response format:
```json
{"result": <value>, "error": <null or string>}
```

### Connection Check

```bash
bash scripts/anki-connect.sh version
# → {"result": 6, "error": null}
```

### Deck Operations

**List all decks:**
```bash
bash scripts/anki-connect.sh deckNames
# → {"result": ["Default", "Japanese::JLPT N5"], "error": null}
```

**List decks with IDs:**
```bash
bash scripts/anki-connect.sh deckNamesAndIds
# → {"result": {"Default": 1}, "error": null}
```

**Create a deck:**
```bash
bash scripts/anki-connect.sh createDeck '{"deck":"Spanish::Vocabulary"}'
```

**Get deck statistics:**
```bash
bash scripts/anki-connect.sh getDeckStats '{"decks":["Default"]}'
# Returns: new_count, learn_count, review_count, total_in_deck
```

### Model (Note Type) Operations

**List all models:**
```bash
bash scripts/anki-connect.sh modelNames
# → {"result": ["Basic", "Basic (and reversed card)", "Cloze"], "error": null}
```

**Create a custom model:**
```bash
bash scripts/anki-connect.sh createModel '{
  "modelName": "MyModel",
  "inOrderFields": ["Front", "Back", "Extra"],
  "css": ".card { font-family: Arial; font-size: 20px; text-align: center; }",
  "isCloze": false,
  "cardTemplates": [
    {
      "Name": "Card 1",
      "Front": "{{Front}}",
      "Back": "{{FrontSide}}<hr id=answer>{{Back}}<br><small>{{Extra}}</small>"
    }
  ]
}'
```

### Note Operations

> **⛔ STOP: Before using `addNote` or `addNotes`, you MUST complete the Pre-Add Checklist above. Do NOT call these APIs until the user has confirmed model, field mapping, deck, and tags.**

**Add a single note:**
```bash
bash scripts/anki-connect.sh addNote '{
  "note": {
    "deckName": "Default",
    "modelName": "Basic",
    "fields": {"Front": "What is photosynthesis?", "Back": "The process by which plants convert light energy into chemical energy"},
    "tags": ["biology", "ai-generated"],
    "options": {"allowDuplicate": false, "duplicateScope": "deck"}
  }
}'
```

**Add multiple notes (batch):**
```bash
bash scripts/anki-connect.sh addNotes '{
  "notes": [
    {
      "deckName": "Default",
      "modelName": "Basic",
      "fields": {"Front": "Q1", "Back": "A1"},
      "tags": ["batch"]
    },
    {
      "deckName": "Default",
      "modelName": "Basic",
      "fields": {"Front": "Q2", "Back": "A2"},
      "tags": ["batch"]
    }
  ]
}'
```

**Find notes:**
```bash
bash scripts/anki-connect.sh findNotes '{"query":"deck:Default"}'
bash scripts/anki-connect.sh findNotes '{"query":"tag:biology"}'
# Query syntax: https://docs.ankiweb.net/searching.html
```

**Update note fields:**
```bash
bash scripts/anki-connect.sh updateNoteFields '{
  "note": {
    "id": 1514547547030,
    "fields": {"Front": "updated front", "Back": "updated back"}
  }
}'
```

### Card Operations

**Find cards:**
```bash
bash scripts/anki-connect.sh findCards '{"query":"deck:Default"}'
# → {"result": [1494723142483, 1494703460437], "error": null}
```

**Get card details:**
```bash
bash scripts/anki-connect.sh cardsInfo '{"cards":[1498938915662]}'
# Returns: question, answer, deckName, modelName, fields, interval, reps, lapses, etc.
```

### Statistics

**Cards reviewed today:**
```bash
bash scripts/anki-connect.sh getNumCardsReviewedToday
# → {"result": 42, "error": null}
```

**Cards reviewed by day:**
```bash
bash scripts/anki-connect.sh getNumCardsReviewedByDay
# → {"result": [["2025-01-15", 124], ["2025-01-14", 261]], "error": null}
```

**Review history for a deck:**
```bash
bash scripts/anki-connect.sh cardReviews '{"deck":"Default","startID":0}'
# Returns: [reviewTime, cardID, usn, buttonPressed, newInterval, previousInterval, newFactor, reviewDuration, reviewType]
```

**Review history for specific cards:**
```bash
bash scripts/anki-connect.sh getReviewsOfCards '{"cards":["1653613948202"]}'
```

### Batch Operations

Use `multi` to combine multiple actions in one request:
```bash
bash scripts/anki-connect.sh multi '{
  "actions": [
    {"action": "deckNames"},
    {"action": "modelNames"},
    {"action": "getNumCardsReviewedToday"}
  ]
}'
```

## Flashcard Generation Guide

When generating flashcards from source material, follow this process:

### Step-by-Step Process

1. **Rewrite** the content using clear and concise language while retaining its original meaning
2. **Split** the rewritten content into sections, each focusing on one main point
3. **Generate** multiple flashcards from each section; for sections with more than 10 words, split and summarize before creating cards

### Quality Rules

- Keep flashcards **simple, clear, and focused** on the most important information
- Questions must be **specific and unambiguous**
- Use **simple and direct language** for readability
- Each answer should contain only a **single key fact/name/concept/term**
- Avoid yes/no questions — ask "what", "where", "why", "how" instead
- Do not repeat the question stem in the answer

### Example: Dead Sea

**Source text:**
> The characteristics of the Dead Sea: Salt lake located on the border between Israel and Jordan. Its shoreline is the lowest point on the Earth's surface, averaging 396 m below sea level. It is 74 km long. It is seven times as salty (30% by volume) as the ocean. Its density keeps swimmers afloat. Only simple organisms can live in its saline waters.

**Generated flashcards:**

| Question | Answer |
|---|---|
| Where is the Dead Sea located? | on the border between Israel and Jordan |
| What is the lowest point on the Earth's surface? | The Dead Sea shoreline |
| What is the average level on which the Dead Sea is located? | 396 meters (below sea level) |
| How long is the Dead Sea? | 74 km |
| How much saltier is the Dead Sea as compared with the oceans? | 7 times |
| What is the volume content of salt in the Dead Sea? | 30% |
| Why can the Dead Sea keep swimmers afloat? | due to high salt content |
| Why is the Dead Sea called Dead? | because only simple organisms can live in it |
| Why only simple organisms can live in the Dead Sea? | because of high salt content |

### Example: ECG (Electrocardiography)

**Source text:**
> The contraction of any muscle is associated with electrical changes called 'depolarization', and these changes can be detected by electrodes attached to the surface of the body. Since all muscular contraction will be detected, the electrical changes associated with contraction of the heart muscle will only be clear if the patient is fully relaxed and no skeletal muscles are contracting. Although the heart has four chambers, from the electrical point of view it can be thought of as having only two, because the two atria contract together ('depolarization'), and then the two ventricles contract together.

**Generated flashcards:**

| Question | Answer |
|---|---|
| What electrical changes are associated with muscle contraction? | depolarization |
| How can depolarization be detected? | by electrodes attached to the surface of the body |
| Why must the patient be fully relaxed during an ECG? | because skeletal muscle contractions would also be detected |
| How many chambers does the heart have from an electrical point of view? | two (atria contract together, then ventricles contract together) |
| What is the term for the two atria contracting together? | depolarization |

### Output Format

Always present generated flashcards in a table for user review before adding to Anki:

```
| Question | Answer |
|---|---|
| ... | ... |
```

After user confirms, use `addNotes` to batch-add all cards at once.

## File Integration

### PDF → Flashcards

1. Use the `pdf` skill to extract text from the PDF
2. Apply the flashcard generation guide above to create Q&A pairs
3. Present the table to the user for review
4. Confirm: target deck, note type (model), and tags
5. Use `addNotes` to batch-add

### CSV / Excel → Flashcards

1. Use the `xlsx` skill to read and parse the file
2. Inspect the columns — if data is already in Q/A format, map directly to Front/Back fields
3. If not Q/A format, apply the flashcard generation guide to the content
4. Present the mapping/cards to the user for review
5. Confirm: target deck, note type (model), and tags
6. Use `addNotes` to batch-add

**⛔ IMPORTANT: You MUST follow the Pre-Add Checklist (at the top of this document) before adding any cards. This means: fetch models → ask user to choose → verify fields → confirm deck/model/tags. No exceptions.**

## Workflow Examples

### 1. Check Connection and List Decks

```bash
bash scripts/anki-connect.sh version
bash scripts/anki-connect.sh deckNames
bash scripts/anki-connect.sh getDeckStats '{"decks":["Default"]}'
```

### 2. Generate and Add Flashcards from Text

1. User provides text content
2. Apply flashcard generation guide — rewrite, split, generate Q&A pairs
3. Present table for review
4. **Follow Pre-Add Checklist:**
   a. Fetch models: `bash scripts/anki-connect.sh modelNames`
   b. Ask user to choose model via `AskUserQuestion`
   c. Verify fields: `bash scripts/anki-connect.sh modelFieldNames '{"modelName":"<user-chosen-model>"}'`
   d. Show field mapping to user and confirm
   e. Confirm deck, model, and tags — present final summary
5. Only after user confirms all of the above:
```bash
bash scripts/anki-connect.sh addNotes '{
  "notes": [
    {"deckName":"<deck>","modelName":"<user-chosen-model>","fields":{"<field1>":"Q1","<field2>":"A1"},"tags":["ai-generated"]},
    {"deckName":"<deck>","modelName":"<user-chosen-model>","fields":{"<field1>":"Q2","<field2>":"A2"},"tags":["ai-generated"]}
  ]
}'
```

### 3. Generate Flashcards from PDF

1. Use `pdf` skill to extract text
2. Follow "Flashcard Generation Guide" on extracted text
3. Present cards for review
4. **Follow Pre-Add Checklist** (fetch models → user picks → verify fields → confirm all)
5. Batch-add with `addNotes`

### 4. Import Flashcards from CSV/Excel

1. Use `xlsx` skill to parse the file
2. Map columns to Front/Back or generate cards
3. Present mapping for review
4. **Follow Pre-Add Checklist** (fetch models → user picks → verify fields → confirm all)
5. Batch-add with `addNotes`

### 5. View Study Statistics

```bash
# Today's review count
bash scripts/anki-connect.sh getNumCardsReviewedToday

# Review history by day
bash scripts/anki-connect.sh getNumCardsReviewedByDay

# Detailed review history for a deck
bash scripts/anki-connect.sh cardReviews '{"deck":"Default","startID":0}'

# Deck stats (new/learn/review counts)
bash scripts/anki-connect.sh getDeckStats '{"decks":["Default"]}'
```
