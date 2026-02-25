---
name: generate-flashcards
description: >-
  Generate learning-science-backed flashcard YAML files from lesson content.
  Use when: (1) a lesson .md file needs flashcards generated, (2) a chapter
  directory needs flashcards for all lessons, (3) user says "generate flashcards",
  "create flashcards", "make cards for", or references /generate-flashcards.
  Produces .flashcards.yaml files adjacent to lesson .md files, consumed by
  the remark-flashcards plugin and rendered by Flashcards components.
---

# Generate Flashcards

Generate two kinds of cards from lesson content — **recall cards** that lock in critical facts, and **thinking cards** that force genuine understanding. Half and half. That's it. Always plan first, use your tasks tool to organize the plan and track your progress.

## Quick Reference

| Constraint   | Recall                                          | Thinking                                       |
| ------------ | ----------------------------------------------- | ---------------------------------------------- |
| Front length | <40 words                                       | <25 words                                      |
| Back length  | <15 words (enum exception: list items ≤5w each) | 20-40 words                                    |
| Front format | Direct question ending in `?`                   | Why/How question ending in `?`                 |
| Back content | Just the fact — no "because"                    | Reasoning chain (BECAUSE/THEREFORE)            |
| `why` field  | Never                                           | Always (<20 words, different angle than front) |
| Difficulty   | basic or intermediate                           | intermediate or advanced                       |

## What Makes a Good Card

Read this section first. Everything else is mechanics.

### Recall Cards (half the deck)

Follow the **minimum information principle** (one question, one answer). Keep questions concise but explicit (**under 40 words**). Ensure each card is self-contained and atomic (tests only one concept). Focus on **key terms, formulas, and relationships**. A student should be able to answer in under 5 seconds.

**No filler phrases**: Don't pad fronts with "According to the lesson," "In the lesson's framework," or "The lesson says." Just ask the question directly. Filler wastes words and weakens the retrieval cue.

**The test**: Cover the back — can a student who read the lesson produce the answer from memory? If yes, the card works. If the card requires context not on the front, it fails.

**Back length**: Recall backs must be **under 15 words**. Just the fact — no explanation, no elaboration. If you need more words, you're explaining (that's a thinking card) or testing two things (split).

**Enumeration exception**: When a recall card tests a numbered list (3+ items), the back may exceed 15 words if each item is ≤5 words. Use `\n`-separated format (see example below).

**Structured mapping backs**: When the answer is a set of paired items, use multiline format with `\n`. Word count applies to total words across all lines. Example:

```yaml
back: "Specs: WHAT to do.\nSkills: HOW to do it.\nFeedback loops: IMPROVE over time."
```

**One question per card**: If the front contains "and" joining two distinct questions, split it into two cards. "What is X and why does it matter?" = two cards.

**Good recall card**:

```yaml
- id: "preface-agent-native-001"
  front: "In the Agent Factory model, what are the three pillars?"
  back: "1. AI Agents\n2. Cloud Infrastructure\n3. Business Model"
  tags: ["agent-factory", "pillars"]
  difficulty: "basic"
```

**Bad recall card** (and why):

```yaml
# BAD: Too vague — what kind of "pillars"? Not self-contained.
- front: "What are the three pillars?"
  back: "Agents, Infrastructure, Business Model"

# BAD: Tests recognition, not recall — the answer is in the question.
- front: "Is SDD the methodology where specs are the source of truth?"
  back: "Yes"

# BAD: Tests two things at once — split into two cards.
- front: "What is SDD and what is MCP?"
  back: "SDD is spec-driven development. MCP is model context protocol."

# BAD: Back is a paragraph — just give the fact, not the explanation.
- front: "In the Agent Factory era, what do companies manufacture?"
  back: "AI employees — role-based systems that compose tools, spawn
    specialist agents, and deliver outcomes at scale."
# FIXED: back: "AI employees (Digital FTEs)"
```

### Discrimination Cards (recall subtype)

When the source has a comparison table or contrasting pairs, generate either/or discrimination cards that force the student to classify:

```yaml
- front: "SaaS era product: software tools. Agent Factory era product?"
  back: "AI employees."
```

Trigger: comparison tables, before/after lists, era transitions. These count as recall cards (no `why` field, basic/intermediate difficulty). See `references/CARD-TYPES.md` for more examples.

### Thinking Cards (half the deck)

Focus on **understanding, not just rote memorization**. The question itself must be a **Why** or **How** question to encourage deeper thinking and force the student to reason, not just retrieve. These cards take 10-30 seconds to answer.

**Front length**: Keep thinking fronts **under 25 words**. A scenario setup should be one short sentence, not a paragraph. If the front is longer than two lines, the student is reading, not retrieving. Cut the setup to its essential detail.

**The test**: Does answering this card require the student to _think_, not just _remember_? If a parrot could answer it, it's not a thinking card.

**The reasoning-chain test**: Read just the back. Does it contain a **BECAUSE** or **THEREFORE** — an actual causal chain? Or is it a fact someone could memorize from a bullet point? If there's no reasoning in the back, it's a disguised recall card. Reclassify or rewrite.

**Back length**: Thinking backs should be **20-40 words**. Lead with the key insight, follow with one reasoning step. Over 40 words = you're testing multiple things or writing an essay.

**Back tone**: Write the claim, not the argument. The back is a crisp factual chain (X because Y), not persuasive prose. If the student will "remember the vibe but not the exact claim," the back is too rhetorical. Strip adjectives, strip rhetoric, keep the causal link.

**Front variety**: Vary thinking card formats across the deck. Use scenarios, comparisons, counterfactuals, and causal questions — not just "Why does the [source] argue that...". **No more than 2 cards per deck** may use the "Why does the [text/lesson/preface] argue/say/recommend..." template.

**Good thinking card**:

```yaml
# Scenario — student must reason about what's missing
- id: "preface-agent-native-002"
  front: "A startup builds great AI agents with solid cloud infrastructure, but revenue stalls. Why?"
  back: "Technology without a business model doesn't generate revenue. The Agent Factory requires all three pillars — agents, infrastructure, AND a model for selling verified outcomes."
  tags: ["agent-factory", "business-model"]
  difficulty: "intermediate"
  why: "What's the difference between selling outcomes and selling software subscriptions?"

# Counterfactual — what breaks if you remove X?
- id: "ch01-example-002"
  front: "What would happen if a company deployed Custom Agents without any Incubation phase first?"
  back: "They'd over-engineer solutions to the wrong problem. Without exploration, requirements are guesses — the resulting agent is brittle and must be rebuilt."
  tags: ["agent-maturity-model", "anti-patterns"]
  difficulty: "advanced"
  why: "How would you recognize premature specialization in a real project?"
```

**Bad thinking card** (and why):

```yaml
# BAD: This is just a recall card with "Why" stapled on.
- front: "Why is SDD important?"
  back: "Because specs are the source of truth."

# BAD: Disguised recall — the back is a memorizable before/after comparison, not reasoning.
- front: "How does the human role change from the SaaS era to the Agent Factory era?"
  back: "From operator to supervisor and verifier."
# FIXED: Make it a recall card, or rewrite to require actual reasoning:
#   front: "Why does shifting from operator to supervisor require new skills, not just less work?"

# BAD: Answer is too short — no reasoning shown.
- front: "A company's AI agents keep failing in production. What's the likely cause?"
  back: "No evaluation."

# BAD: Front is so long it becomes a reading exercise, not a thinking exercise.
- front:
    "Given that a company has deployed agents using Claude Code with MCP integration
    and their specs follow the SDD methodology but they haven't implemented golden
    dataset evaluation and their shadow mode period was only 2 weeks..."
  back: "..."

# BAD: Formulaic — 6 cards in one deck all start with "Why does the lesson argue..."
- front: "Why does the lesson argue that open-source AI models are critical?"
# FIXED: "Open-source AI models are available but governments still build proprietary systems. Why?"
```

### The `why` Field

Only on thinking cards. A single question, under 20 words, that pushes one level deeper — implications, mechanisms, or connections to other concepts. It must NOT repeat the front.

**Good**: Front asks "Why did X happen?" → `why` asks "How would you prevent X?"
**Bad**: Front asks "Why did X happen?" → `why` asks "Can you explain why X happened?"

### Self-Contained Rule

Every card must make sense in isolation. A student reviewing cards 3 weeks later has forgotten the lesson structure. If your card front says "What is the third element?" — third element of what? Always anchor terms in their context.

## Card Generation Process

### 1. Find the Lesson

```bash
# "ch N" or "chapter N" — substitute the chapter number:
ls -d apps/learn-app/docs/*/NN-*/

# Bare lesson name:
find apps/learn-app/docs -name "*lesson-slug*" -name "*.md"
```

### 2. Check for Existing Flashcards

```bash
# Use absolute path — CWD may vary
ls "$(dirname /absolute/path/to/lesson.md)/$(basename /absolute/path/to/lesson.md .md).flashcards.yaml" 2>/dev/null
```

- Exists + no regeneration requested → skip with notice
- Exists + regeneration requested → bump `deck.version`, regenerate
- Doesn't exist → generate fresh (version: 1)

### 3. Read the Lesson

Read the full `.md` file. Identify what's worth **memorizing** (terms, frameworks, lists) vs. **understanding** (causal mechanisms, tradeoffs, "why X not Y").

**Prioritization** (highest → lowest card-worthiness):

1. Definitions and named concepts (a student who can't define the terms can't think with them)
2. Frameworks and models (pillars, phases, layers — the structural scaffolding)
3. Numbered lists and enumerations (easy to half-remember, cards prevent that)
4. Causal claims and tradeoffs (why X beats Y, what breaks when Z fails)
5. Named citations and attributed claims (when the lesson cites a specific person, organization, or study to anchor an argument, that attribution is card-worthy — it's a concrete proof point students should recall)
6. Examples that embody a principle (concrete anchors for abstract ideas)

Skip: anecdotes, historical color, motivational asides, repeated explanations of the same point.

**Card density**: Starting estimate: ~1 card per 150-200 words of prose (exclude code blocks). Dense concept sources (thesis statements, summary tables, framework introductions) will produce more cards — let concept count from step 3.5 drive the final card count, not word count. Floor: 8. Ceiling: `min(30, prose_words / 150)` — book-level pages with dense prose may reach 30; short lessons stay lower. Never pad a deck with filler.

**Enumeration rule**: When a lesson is structured around a numbered list (e.g., "8 objections", "5 deployment stages", "4 monetization models"), each item deserves at least one card — either recall (name/define it) or thinking (test understanding of it). Don't summarize N items into 2 cards. A student who "sort of remembers 3 of the 8" has failed to learn the framework.

**List card weight**: Never create a single card that asks a student to recall a long list (6+ items). Long lists are heavy recall and produce vague "I sort of know this" responses. Instead: use "Name any K of the N" (e.g., "Name any 4 of the 8 objections") — this tests retrieval without requiring perfect enumeration. Then card each individual item separately through recall or thinking cards.

### 3.5 Extract Concept List

**Before writing any cards**, produce a numbered list of every card-worthy concept from the lesson. Tag each as a recall or thinking candidate:

- **R** = recall candidate (definition, named framework, enumeration, key term)
- **T** = thinking candidate (causal mechanism, tradeoff, decision, "why X and not Y")

Example:

```
1. [R] SaaSpocalypse — definition and trigger event
2. [R] Agent Triangle — three deployment paths
3. [T] Why legal tech got hit hardest
4. [R] Digital FTE hours vs Human FTE hours
5. [T] Why skipping Incubator stage fails
6. [R] Golden Dataset — definition and threshold
7. [T] Why open-source plugins were more threatening than proprietary ones
```

**Validation checks on the concept list:**

- Does every H2/H3 heading in the lesson have at least one concept?
- Are any key terms defined in the lesson but missing from the list?
- If the lesson introduces a numbered framework (e.g., "8 objections"), is each item represented?
- Are named citations or attributed claims (specific people, organizations, studies cited to anchor arguments) captured?
- **Balance gate**: If R/T split exceeds 60/40 in either direction, STOP. Reframe concepts until within 55/45. Recall concepts that involve tradeoffs or causal mechanisms → convert to T. Thinking concepts that are really just definitions → convert to R.

**Depth check on R-tagged concepts**: For each concept tagged R, ask: "Is there a deeper angle here that would make a stronger thinking card?" A concept like "three nation categories" is recall on the surface, but the deeper insight (why Global South nations face existential stakes) makes a better thinking card. When a recall concept has a richer thinking angle, tag it T and create a separate simpler recall card for the bare fact.

**Only then proceed to card generation, working from this list.** Every card you write must trace back to a concept on this list. If you generate a card that doesn't map to a listed concept, either add the concept to the list (it was genuinely missing) or cut the card (it's filler).

### 4. Generate Cards

Work through your concept list from step 3.5. For each concept, **commit to the card type BEFORE writing**:

1. Read the concept and its R/T tag
2. **Declare**: "This is a RECALL card" or "This is a THINKING card"
3. Apply the rules from "What Makes a Good Card" above — no mixing types
4. If you find yourself writing a recall front with a thinking-length back, **STOP**. Either trim the back to a fact (recall) or rewrite the front as a Why/How question (thinking). Never let type emerge implicitly from what you happened to write.

Apply the three learning science principles from `references/LEARNING-SCIENCE.md`: **Minimum Information** (one concept per card), **Retrieval Practice** (force recall, never hint at the answer), and **Elaborative Interrogation** (thinking cards push deeper with `why`).

**Variety target**: In decks with 8+ thinking cards, use at least 3 distinct formats from: Scenario, Counterfactual, Comparison, Causal. No single format >40%.

**Mix them** — alternate recall and thinking cards throughout the deck. Don't cluster all recall cards at the top.

**Per-card check** (before moving to the next card): (1) Type declared (R or T)? (2) Constraints from Quick Reference met? (3) Card self-contained?

### 5. Self-Check Before Writing

Run this unified checklist. It covers quality, coverage, type purity, and overlap — the Quality Gate (§6.5) handles mechanical constraints.

**Quality**:

- [ ] Does every front make sense without seeing the lesson? (self-contained)
- [ ] Could a parrot answer this? If yes, it's recall — make sure it's marked that way
- [ ] Read each thinking card back: does it contain a BECAUSE/THEREFORE reasoning chain, or just a memorizable fact? If no reasoning → reclassify as recall (trim back, remove `why`)
- [ ] Read each recall card back: does it contain "because" or an explanation? If yes → reclassify as thinking (add `why`, rewrite front as Why/How)
- [ ] Are thinking backs factual chains, not persuasive prose? Strip rhetoric.
- [ ] Every number, percentage, and proper noun on a card appears **verbatim in the source lesson**. If you inferred or calculated a figure, either verify it against the text or remove it.
- [ ] Could any two cards in this deck be answered with the same back? If yes, differentiate the fronts clearly or merge into one card.

**Coverage**:

- [ ] Every H2/H3 heading has at least one card
- [ ] Every numbered list (e.g., "eight objections", "three pillars") has: one recall card that names/enumerates the items + at least one thinking card testing understanding of an individual item
- [ ] Cross-reference against your concept list from step 3.5 — any uncarded concepts?
- [ ] Did I skip any concept that a student would be embarrassed not to know?

**Type purity** (if any card changes type, update its difficulty accordingly):

- [ ] No thinking card has a back that could be memorized as a bullet point
- [ ] No recall card has a back over 15 words or containing "because"

If a section is deliberately skipped (anecdote, motivational aside), note it in the report. Otherwise, add cards.

### 6. Write the YAML

Write `<lesson-basename>.flashcards.yaml` adjacent to the `.md` file. Follow the schema in `references/YAML-SCHEMA.md`.

### 6.5 Mandatory Quality Gate (Do Not Skip)

Before you finalize, enforce these constraints:

1. Card IDs must match `^{deck.id}-\d{3}$` exactly. Never shorten the prefix (for example `preface-001` is invalid if `deck.id` is `preface-agent-native`).
2. Every card `front` ends with `?`.
3. Every thinking card has a non-empty `why` field.
4. No recall card includes a `why` field.
5. Thinking card fronts explicitly include `Why` or `How`.
6. Recall/thinking balance is within 45%-55% each.
7. Recall fronts remain under 40 words.
8. No card back starts with `Yes` or `No`.
9. **Recall backs under 15 words.** Count them. If over, trim to just the fact.
10. **Thinking backs 20-40 words.** Lead with the insight, add one reasoning step.
11. **No compound questions.** If a front has "and" joining two questions, split into two cards.
12. **Thinking front variety.** No more than 2 cards per deck use "Why does the [source] argue/say/recommend..." — use scenarios, counterfactuals, and comparisons instead.
13. **Difficulty distribution.** Target: ~30% basic, ~50% intermediate, ~20% advanced. Acceptable range: basic 20-40%, intermediate 40-60%, advanced 10-30%. Only adjust if outside the acceptable range.
14. **Thinking fronts under 25 words.** Count them. Scenario setups must be one sentence — read the cue in 3 seconds, think for 20.
15. **No filler phrases.** No "According to the lesson," "In the lesson's framework," or "The lesson says." Just ask the question.
16. **No list cards with 6+ items.** Use "Name any K of the N" instead. Card each item individually.
17. **Named citations covered.** If the lesson cites a specific person or organization to anchor an argument, at least one card references it.
18. **Thinking backs are factual chains, not rhetoric.** Each back should state a claim with a reason ("X because Y"), not make a persuasive argument.

If any gate fails, revise cards and re-check before returning the final output.

### 6.7 Run Validator (MANDATORY)

```bash
cd apps/learn-app && pnpm exec tsx scripts/validate-flashcards.ts
```

This validates all decks across the book (duplicate IDs, schema violations, missing fields). **Do NOT swallow errors** — if the validator fails, fix the issues before returning.

### 7. Heading Convention

When adding flashcards to a lesson `.md` file, add this heading and component:

```markdown
## Flashcards Study Aid

<Flashcards />
```

**IMPORTANT**: Do NOT add an `import` statement for the Flashcards component. The `remark-flashcards` plugin automatically injects the component at build time. Adding `import Flashcards from '@site/src/components/Flashcards';` will cause a build error because the component is virtual (provided by the plugin, not a real file).

## Card ID Strategy (Prevents Collisions)

Card IDs must be globally unique across all decks in the book. Use the **full `deck.id`** as the card prefix:

```yaml
deck:
  id: "ch05-reusable-skills" # Globally unique deck ID

cards:
  - id: "ch05-reusable-skills-001" # Full deck ID + sequence
  - id: "ch05-reusable-skills-002"
```

This prevents collisions when multiple lessons in the same chapter generate cards. The validator at `apps/learn-app/scripts/validate-flashcards.ts` checks global uniqueness across all decks.

**Deck ID convention**: `<section>-<lesson-slug>` in kebab-case.

- `preface-agent-native`, `ch01-factory-paradigm`, `ch05-reusable-skills`
- For lessons with numeric prefixes: `ch05-03-skills` (chapter 5, lesson 03)

## Difficulty

- `basic` — Can you recall this fact? (definitions, identifications, lists)
- `intermediate` — Can you apply this? (scenarios, comparisons, causal reasoning)
- `advanced` — Can you evaluate or create? (critique, predict consequences, synthesize)

**Target**: ~30% basic, ~50% intermediate, ~20% advanced. **Acceptable range**: basic 20-40%, intermediate 40-60%, advanced 10-30%. Only adjust if outside the acceptable range. If basic >40%, promote complex recall cards to intermediate. If advanced = 0%, promote the deepest thinking cards to advanced. Every deck should have at least 1-2 advanced cards.

## Chapter Mode

When generating for an entire chapter:

1. `ls <chapter-dir>/*.md` — discover lessons
2. Skip README.md, index.md, _category_.json
3. Generate for each lesson sequentially
4. Each lesson gets its own deck with its own `deck.id` — no shared IDs

## Cross-Deck Awareness

When generating for related lessons (same chapter, same part, or book-level pages like thesis/preface):

1. Check for existing `.flashcards.yaml` files in sibling directories
2. If a concept already has a card in a sibling deck, either **skip it** or **card it from a distinctly different angle**
3. Never duplicate the same concept with the same framing across decks
4. If you card a concept from a different angle than a sibling deck, note it in the report

## Common Mistakes

| What goes wrong                                      | How to fix it                                                                                 |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| All cards feel the same                              | Check: is each card clearly recall OR thinking? Not a muddy mix.                              |
| Cards aren't self-contained                          | Add context to the front: "In the Agent Factory model, ..."                                   |
| Thinking cards are just recall with "Why"            | Read the back: does it have BECAUSE/THEREFORE reasoning? If not, it's recall.                 |
| `why` repeats the front                              | Push to a different dimension: implications, prevention, adjacent concepts                    |
| Too many cards about minor details                   | Would a student be embarrassed not to know this? If not, cut it.                              |
| YAML special chars break parsing                     | Quote strings with `: # " '`                                                                  |
| Same concept in two sibling decks                    | Skip or card from a different angle. Never duplicate.                                         |
| No concept list before generation                    | Always extract concepts first (step 3.5). Cards without a concept map drift.                  |
| Unverified numbers on cards                          | Every stat must appear verbatim in the source. Don't infer or calculate figures.              |
| Shallow recall where thinking card would be stronger | Run the depth check: does this R-concept have a richer T-angle? Split into recall + thinking. |

## Report

After generation, output:

```
Generated: <path>
Cards: <count> total (recall: N, thinking: N)
Why fields: N
Ratios: recall=<0.00>, thinking=<0.00>, thinking-fronts-with-why/how=<0.00>
ID format: PASS/FAIL (`deck.id-NNN`)
Fronts end with '?': PASS/FAIL
Recall backs ≤15 words: PASS/FAIL (longest: N words, card: <id>)
Thinking backs 20-40 words: PASS/FAIL (shortest: N, longest: N, violators: <ids>)
Compound questions: PASS/FAIL (N found)
"Why does the [source]..." fronts: N (max 2)
Difficulty: basic: N (NN%), intermediate: N (NN%), advanced: N (NN%)
Factual verification: PASS/FAIL (unverified figures: <ids>)
Type purity: PASS/FAIL (hybrids reclassified: N)
Coverage: N concepts extracted, N carded, N skipped (list skipped sections if any)
```

## Revision Protocol

When updating an existing deck (not generating fresh):

1. Bump `deck.version` (e.g., 1 → 2)
2. **Preserve IDs** for cards whose concept is unchanged (even if wording is tweaked)
3. Append new cards with the next sequential ID after the highest existing one
4. Re-run the Quality Gate (§6.5) on the full revised deck
5. Add a `## Changes` section to the report: cards added, removed, reworded, with IDs

## References

- **`references/LEARNING-SCIENCE.md`** — Cognitive science foundations (retrieval practice, minimum information, elaborative interrogation)
- **`references/CARD-TYPES.md`** — Card type examples and anti-patterns
- **`references/YAML-SCHEMA.md`** — Exact YAML schema, field constraints, escaping rules
