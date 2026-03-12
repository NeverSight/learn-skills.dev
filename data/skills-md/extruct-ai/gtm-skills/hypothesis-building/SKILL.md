---
name: hypothesis-building
description: >
  Generate testable pain hypotheses from the company context file (ICP, win
  cases, product knowledge) and user input. Fast, no API keys needed — pure
  reasoning. Outputs a hypothesis set with search angles that directly guide
  list-building queries. Sits between context-building and list-building.
  Triggers on: "build hypotheses", "hypothesis set", "pain hypotheses",
  "define hypotheses", "what pain points", "campaign angles", "search angles",
  "refine hypotheses".
---

# Hypothesis Building

Generate testable pain hypotheses from what you already know — ICP, win cases, product value prop, and user knowledge of the target vertical. No API keys, no external research. Pure reasoning from context + conversation.

## When to Use

- After `context-building`, before `list-building`
- When entering a new vertical and need to define what to search for
- When you know the vertical well enough to form hypotheses without deep research
- When you want a fast starting point before (optionally) validating with `market-research`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Context file | `claude-code-gtm/context/{company}_context.md` | yes |
| Target vertical | User input | yes |
| Additional knowledge | User input — industry experience, known pain points | recommended |
| Existing hypothesis set | `claude-code-gtm/context/{vertical-slug}/hypothesis_set.md` | no (for refine mode) |

## Output

```
claude-code-gtm/context/{vertical-slug}/hypothesis_set.md
```

Same path and format as `market-research` output — all downstream skills work unchanged.

## Workflow

### Step 1: Read context file

Read `claude-code-gtm/context/{company}_context.md` and extract:

- **ICP profiles** — who buys, company size, roles, geographies
- **Win cases** — why past customers bought, what pain triggered the purchase
- **Product value prop** — what the product does, key numbers
- **Active hypotheses** — any existing hypotheses already in the context file

### Step 2: Gather vertical context from user

Ask the user:

| Question | Why |
|----------|-----|
| What vertical are you targeting? | Defines the slug and scope |
| What geographies are you targeting? | Shapes search filters and regional pain points |
| What do you know about how these companies operate? | Seeds the hypothesis reasoning |
| What problems do you think your product solves for them? | Grounds hypotheses in real value |
| Any specific signals or patterns you've noticed? | Captures practitioner knowledge |

Keep it conversational — don't force all questions if the user gives rich context upfront.

### Step 3: Extract patterns from win cases

For each win case in the context file, identify:

1. **Trigger** — what event or pain made them look for a solution?
2. **Workflow gap** — what were they doing before? What broke?
3. **Value delivered** — what specific outcome did the product provide?
4. **Transferability** — does this pattern apply to the target vertical?

Map win case patterns to potential hypotheses for the new vertical.

### Step 4: Draft hypotheses

Generate 3-7 hypotheses. Each hypothesis must have:

- **Short name** — 3-5 word label
- **Description** — 2-3 sentences explaining the pain, why it exists, and why the product fits
- **Best fit** — what type of company within the vertical this applies to most
- **Search angle** — 1-2 specific search queries or Discovery criteria to find companies matching this pain

**Quality checks per hypothesis:**

- Is it specific to a workflow or decision, not a vague industry trend?
- Can the recipient confirm it from their own experience?
- Does it connect to a product capability (not just a random pain)?
- Is the search angle concrete enough to drive a list-building query?

### Step 5: Review with user

Present the full hypothesis set and ask:

- "Do these match your understanding of the vertical?"
- "Any hypotheses to add, merge, or remove?"
- "Are the search angles specific enough?"

Refine based on feedback. This is interactive — expect 1-2 rounds.

### Step 6: Save

Save to `claude-code-gtm/context/{vertical-slug}/hypothesis_set.md`. Create the directory if it doesn't exist.

## Output Format

```markdown
## Hypothesis Set: [Vertical]

### #1 [Short name]
[2-3 sentence description — the pain, why it exists, why the product fits]
Best fit: [company type within the vertical]
Search angle: [1-2 search queries or Discovery criteria to find these companies]

### #2 [Short name]
[2-3 sentence description]
Best fit: [company type]
Search angle: [search queries or criteria]

...
```

The `Search angle` field is what makes this skill useful before list-building — it directly tells list-building what to search for.

## Refine Mode

When a hypothesis set already exists at the output path, enter refine mode:

1. Read the existing hypothesis set
2. Ask what changed — new win cases, campaign results, vertical knowledge
3. Update, merge, or add hypotheses
4. Preserve hypothesis numbering where possible (downstream references use `#N`)

## Key Difference from market-research

| | hypothesis-building | market-research |
|---|---|---|
| **Speed** | Fast — minutes | Slow — external research queries |
| **Source** | Your own knowledge + context file | External research (e.g. Perplexity) |
| **API keys** | None | Requires API key for chosen provider |
| **Best for** | Verticals you know well, fast starts | Verticals you're entering blind |
| **Output** | hypothesis_set.md | hypothesis_set.md + sourcing_research.md |

They're complementary: hypothesis-building first (define what you think), market-research later (validate with external data). Or skip market-research entirely if you know the vertical well.

## Output Consumers

The hypothesis set is consumed by:
- `list-building` — search angles guide query design
- `enrichment-design` — hypotheses drive segmentation column design
- `list-segmentation` — matches companies to hypotheses for tiering
- `email-prompt-building` — hypotheses become P1 email angles
- `email-generation` — personalized openers per hypothesis
- `email-response-simulation` — evaluates copy alignment with hypotheses
