---
name: value-proposition-builder
description: "Use this skill when you need a sharp B2B value proposition: \"write our value prop\", \"our messaging is generic\", \"how do we describe what we do\", \"homepage headline\", \"one-liner for outbound\". Builds the value proposition from the customer's problem, the alternatives they use today and the outcome only you deliver, tests it against competitors and real buyer language, and outputs a one-liner, a short paragraph, three supporting pillars with proof, and versions for the homepage, cold email and sales calls."
license: MIT
metadata:
  title: Value proposition builder
  category: positioning
  tags: "Founders, Marketing, Sales Leaders"
  author: prosyo
  version: "1.0.0"
  keywords: "value proposition template b2b, write a value proposition, positioning statement, claude value proposition skill, saas messaging"
  inputs: "Product and customers, Customer quotes and win reasons, Competitors and alternatives"
  outputs: "One-liner, Value paragraph, Three pillars with proof, Channel versions"
---

Use this when the company cannot say what it does in a sentence that makes a buyer lean in. It produces one value proposition and the versions each channel needs.

## Inputs

- The product and who uses it.
- Evidence: customer quotes, win reasons, reviews, the words buyers use on calls.
- Alternatives: competitors, spreadsheets, agencies, hiring, doing nothing.

## The play

### 1. Start with the alternative, not the product
What does the buyer do today without you? The value proposition is the difference between that and life with you. Read [references/value-prop-canvas.md](references/value-prop-canvas.md) for the canvas and a worked example.

### 2. Find the outcome only you deliver
List the outcomes customers mention. Strike every outcome a competitor could claim with a straight face. What is left is your positioning; if nothing is left, the differentiation is in the how (speed, simplicity, a segment you serve better), so say that.

### 3. Write the one-liner
Formula options:
- "<Outcome> for <who>, without <the pain of the alternative>."
- "<Product> helps <who> <do the job> so they can <outcome>."
- "The <category> for <specific who>."

Test: a buyer should be able to repeat it to a colleague after hearing it once.

### 4. Back it with three pillars
Each pillar: a benefit headline, how it works in one line, and proof (a number, a customer, a demo moment).

### 5. Write channel versions
- Homepage: headline (under 10 words), subheadline (one sentence), three pillars.
- Cold email: one sentence, in the reader's problem language.
- Sales call: a 30-second spoken version.
- LinkedIn headline or bio.

## Output format

```
One-liner: <...>
Paragraph (40-60 words): <...>
Pillars: <benefit - how - proof> x3
Homepage: H1 / subhead
Cold email line: <...>
30-second spoken version: <...>
What we deliberately do not claim: <...>
```

## What good looks like

- Uses customer words, not internal jargon.
- Specific enough that a competitor could not use it unchanged.
- The proof is real and checkable.
- The common mistake is a feature list dressed as a benefit ("AI-powered, all-in-one platform"), which describes the product and says nothing about the buyer.

## Rules

- MUST ground every claim in customer evidence or verifiable product facts.
- MUST name the alternative the buyer uses today.
- NEVER use superlatives you cannot prove ("best", "leading", "#1").

## Example prompts

- "Write our value proposition. We sell scheduling software to multi-location dental groups."
- "Our homepage headline is 'The all-in-one AI platform'. Fix it using these customer quotes."
- "Give me a one-liner for cold emails to CFOs."
