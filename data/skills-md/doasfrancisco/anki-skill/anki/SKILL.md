---
name: anki
description: Create and browse Anki flashcards during coding sessions. Use when the user invokes /anki, asks to create a flashcard, or when you notice the user learning something new and worth remembering (a concept, trick, gotcha, or mental model).
---

# Anki Card Creator

Create flashcards from Claude Code. Scripts are bundled in `./scripts/`.

## Available operations

### Create a card

```bash
python ./scripts/create_card.py \
  --deck "7. computer science" \
  --front "What does __slots__ do in Python?" \
  --back "Restricts instance attributes to a fixed set, saving memory by skipping the per-instance __dict__." \
  --tags "python,memory"
```

### List cards (check for duplicates before creating)

```bash
python ./scripts/list_cards.py --query "tag:python added:7"
python ./scripts/list_cards.py --deck "7. computer science" --added 30
```

### List decks (discover deck names)

```bash
python -c "import sys; sys.path.insert(0, './scripts'); from anki_connect import list_decks; print(list_decks())"
```

## Card quality rules

The user has 226 leeches. Quality over quantity.

1. **Atomic** — one fact per card. If the answer has "and", split it.
2. **Short, specific front** — few words, one unambiguous answer. Not open-ended.
3. **Minimal back** — no unnecessary text. If a structure speaks for itself, don't add explanation below it.
4. **Visual over prose** — prefer file trees, code blocks, or diagrams over sentences when the answer is structural.
5. **No trivia** — only things worth remembering long-term (concepts, gotchas, mental models).
6. **Tag consistently** — use lowercase, comma-separated (e.g. `python,decorators`).

### Good card

- Front: "What's the file structure of a Claude Code skill?"
- Back:
```
<skill>/
├── SKILL.md
└── scripts/
    ├── main.py
    └── helpers.py
```

### Bad card

- Front: "Explain Python's memory model, GIL, and garbage collection"
- Back: (three paragraphs) — too many facts, split into separate cards.

## Workflow

1. **Propose** the card: show front, back, deck, and tags in a formatted block.
2. **Wait** for user approval. Never create without explicit confirmation.
3. **Check duplicates** with `list_cards.py --query "<relevant keywords>"` before creating.
4. **Create** the card only after approval.
5. **Confirm** with the note ID from the output.

## Troubleshooting

If the connection fails, Anki desktop must be running with the AnkiConnect addon installed (addon code: 2055492159).
