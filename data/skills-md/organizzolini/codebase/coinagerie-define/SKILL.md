---
name: coinagerie-define
description: Use when writing or improving a definition in a coinagerie glossary, filling a bare `- **word**:` bullet or an empty JSON value, reviewing a definition that restates its word or reads like a dictionary entry, or explaining a word whose meaning in this codebase differs from its everyday English meaning.
license: MIT
---

# Defining a word

A definition tells a reader who has never seen this code what the word means
**here**. The glossary exists because every reader would otherwise infer a
different meaning from usage, so a definition is the one reading the codebase
stands behind.

## What a definition holds

Up to three parts, in order, a sentence or two each:

1. **The meaning here.** What the thing is, does, holds, or decides in this
   codebase, concretely enough that a reader could point at it.
2. **Against everyday English.** Only when this codebase's use differs from the
   ordinary sense: say what the ordinary word suggests, then how this use
   departs. A word used in its ordinary sense gets part 1 alone, kept short; a
   contrast invented for the sake of the template misleads.
3. **Where it lives.** The code that defines it, by symbol and file
   (`HoldService` in `hold.service.ts`) or by folder. A name outlasts an edit;
   a line number does not. Name the definition's home, not every use.

**Never restate the word.** Remove the headword from the sentence: what remains
must still say something. "A hold is something that holds" fails; so does
defining by a synonym that is itself undefined.

```markdown
- **hold**: A reservation that keeps one copy aside for one patron until
  pickup. Everyday "hold" suggests a grip or a delay; here it is a record with
  an expiry, never an action. Created by `HoldService` in `hold.service.ts`;
  its lifetime is `HOLD_WINDOW` in `hold.constants.ts`.
```

## Procedure

1. **Pick the gaps.** Bare `- **word**:` bullets in markdown and `""` values in
   JSON are undefined (the `coinagerie-collect` skill lists them). Start with
   the words that carry domain meaning. Plain programming words (`index`,
   `value`) get one short sentence, or belong in `exclude.words` if they never
   mean anything specific here.
2. **Find the word's home.** Search for the headword **and its forms**.
   Headwords are folded: `settings` is listed as `set`, a plural as its
   singular, `configured` as `configure`. Search inside identifiers too:
   `CallGateService` contributes `gate`. Look for a type, class, constant, folder,
   or file named after it, then the docs beside that code and the tests that
   show it used.
3. **Write only what the code shows.** A wrong definition does more harm than a
   bare bullet, which is at least findable. When the code does not make the
   meaning clear, leave the bullet bare and say so in your report.
4. **Several meanings.** Define the dominant one and name the other in the same
   definition. A word that only completes a larger name (`service` in
   `HoldService`) is defined by how this codebase uses the suffix.
5. **Check the file still parses.** Run `coinagerie --check`. Definitions never
   change a check's verdict, but a parse failure shows up there.

## Formats

- **Markdown**: `- **word**: Definition.` Continue on following lines, each
  indented by at least one space. A line at the left margin inside the block is
  refused. Indented lines may hold sub-bullets, and a blank line may separate
  indented paragraphs. A definition may start on the line after the bare
  bullet.
- **JSON**: the value is the definition string, with `\n` for a line break.
- **Leave the bold headword exactly as written**, except to follow a rename in
  the code. Editing it otherwise creates a new word, and the next `--write`
  deletes the old bullet with its definition.
- A word that appears in two glossaries is defined where it is listed. Nothing
  copies a definition between destinations, and a word the parent glossary
  already holds is usually excluded from the child.

## Common mistakes

| Mistake                                        | Repair                                                     |
| ---------------------------------------------- | ---------------------------------------------------------- |
| restating the word                             | say what it is, does, or decides                           |
| the dictionary meaning of the English word     | give the meaning here, and the contrast only if it differs |
| explaining the implementation line by line     | state what it is for; point at the code for how            |
| a line number as the location                  | the symbol and file name                                   |
| a guess presented as fact                      | leave it bare until the code or its author says            |
| a line at the left margin in a long definition | indent every continuation line                             |
