---
name: anki
description: Create and manage Anki flashcards. Use when the user wants to create flashcards, add notes to Anki, manage decks, or work with spaced repetition learning. Also use when user mentions "anki", "make cards", "add to anki", "learn this", "memorize", "remember this", "SRS", or asks to turn content into flashcards.
---

# Anki Flashcard Management

Use the `anki.sh` script to create and manage flashcards via AnkiConnect.

```bash
ANKI="$(dirname "$SKILL_PATH")/scripts/anki.sh"
```

Preflight:
- Ensure Anki desktop is running with AnkiConnect enabled
- Ensure `curl` and `jq` are available in PATH

## CRITICAL: User Approval Required

**NEVER add cards to Anki without explicit user approval.**

Before adding any cards:
1. Display all proposed cards in full (front + back)
2. Ask user to confirm: "Ready to add these cards?"
3. Only proceed after explicit "yes" / approval

This is non-negotiable. Users must review card quality before adding.

For potentially destructive or irreversible actions:
- `delete`: ask explicit confirmation before deleting notes
- `update`: confirm exact fields/IDs before updating notes
- `rate`: show card + suggested rating, then wait for user confirmation before submitting

## Guidelines

- **MUST** use the `Anki Markdown` note type
- Use markdown for both front and back fields
- Test exactly one fact or idea per card
- Make questions atomic and simple
- Keep questions and answers short, clear, and unambiguous
- Ensure each card has one unique, specific answer
- Avoid long lists or multiple items in one card
- Add context or hints so your future self understands
- Personalize with examples or mnemonics if helpful
- Allow multiple simple cards for important concepts
- Create multiple variants of important questions from different angles
- Connect cards to personal goals and projects to avoid "orphan" facts
- Always use syntax highlighting for code (see Code Snippets section)
- When creating multiple related cards, use bulk operations for efficiency

## Front Field Format

Use markdown on the front to highlight key terms the question is about:
- Use **bold** or `==highlight==` for the main concept being tested
- Use inline code for technical terms, functions, or syntax

Example: `What does **vertex_index** return in WGSL?`

## Back Field Format

Use this format for the Back field:
1. **Bold one-liner** with the direct answer
2. Blank line
3. Additional context in normal text (optional)

### Formatting for Fast Skimming

- Use `==highlighted==` to make key terms stand out at a glance
- Use **bold** for critical concepts within explanations
- Use syntax highlighting for all code blocks including inline
- Optimize for quick visual scanning—readers should grasp the core idea instantly

### Keyboard Shortcuts

Use `<kbd>` tags for keyboard keys:

```markdown
Press <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> to open the command palette.
```

### Code Snippets

Always use syntax highlighting:

- Fenced blocks: Use triple backticks with language (```js, ```python, ```rust, etc.)
- Inline code: Use `` `code`{lang} `` syntax (e.g., `` `const x = 1`{js} ``)

Advanced features:
- Line highlighting: ```js {2} to highlight line 2
- Word highlighting: ```js /pattern/ to highlight specific words
- Focus mode: Add `// [!code focus]` comment to focus specific lines

### Callouts

Use GitHub-style alerts sparingly for important notes:

```markdown
> [!TIP]
> Brief helpful insight here.

> [!NOTE]
> Useful context the learner should know.

> [!WARNING]
> Common mistake or gotcha to avoid.
```

### Example

```
Front: What does `passEncoder.draw(3)`{js} do with **no vertex buffer**?
Back:

**Invokes the ==vertex shader== 3 times.**

The shader uses `@builtin(vertex_index)`{wgsl} to generate positions ==procedurally==.

> [!TIP]
> Useful for fullscreen quads without geometry data.
```

## Common Operations

Run via `$ANKI <action> [args...]`:

| Action | Description | Example |
|--------|-------------|---------|
| `sync` | Trigger AnkiWeb sync | `$ANKI sync` |
| `decks` | List decks | `$ANKI decks --stats` |
| `models` | List note types | `$ANKI models` |
| `fields` | Fields for a model | `$ANKI fields "Anki Markdown"` |
| `find` | Search notes | `$ANKI find "deck:Spanish tag:verb"` |
| `info` | Note details | `$ANKI info 1234 5678` |
| `add` | Add one note | `$ANKI add "My Deck" "Anki Markdown" '{"Front":"Q","Back":"A"}' --tags "t1 t2"` |
| `add-bulk` | Add many notes | `$ANKI add-bulk "My Deck" "Anki Markdown" '[{"Front":"Q1","Back":"A1"}]'` |
| `update` | Update fields | `$ANKI update 1234 '{"Front":"New Q"}'` |
| `delete` | Delete notes | `$ANKI delete 1234 5678` |
| `due` | Get due cards | `$ANKI due "My Deck" --limit 5` |
| `review` | Show card | `$ANKI review 1234` |
| `rate` | Rate card (1-4) | `$ANKI rate 1234 3` |
| `tags` | List tags | `$ANKI tags --pattern "verb"` |

### Typical workflow

```bash
$ANKI sync                          # sync first
$ANKI decks                         # check available decks
$ANKI models                        # verify required model exists
$ANKI fields "Anki Markdown"        # verify field names for selected model
$ANKI find "deck:MyDeck front:test" # check for duplicates
$ANKI add "MyDeck" "Anki Markdown" '{"Front":"...","Back":"..."}'
$ANKI sync                          # sync after changes
```
