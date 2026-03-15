---
name: frame
description: "Frame: create a Pitch from a problem statement or idea"
disable-model-invocation: true
---

# Frame: create a Pitch from a problem statement or idea

When the user types `/frame` and describes a problem, idea, or opportunity, do the following:

## 1) Understand the problem space (required)

- Ask clarifying questions to understand the core problem (max 3–5 questions).
- Identify who is affected and what they're trying to accomplish.
- Search the repo for existing related functionality, prior art, or adjacent features.
- Note any existing patterns, models, or abstractions that might be relevant.

## 2) Create skeleton Pitch file

- **Location**: `projects/<domain-name>/<project-name>/pitch.md`
- **Domain name**: the product area or team domain (e.g., `payments`, `family-messaging`, `attendance-plus`)
- **Project name**: derive a stable folder slug from the problem domain (e.g., `bank-deposit-reconciliation`, `attendance-notifications`).
- **First line**: `# Pitch: <Concise title>`
- Create the file with just the header and section structure (no content yet)

## 3) Iteratively build each section (one at a time)

**Important**: Work through sections one-by-one with the user. Keep content **succinct and high-level** — this is a starting point, not a complete definition.

For each section:
1. Generate a **brief, high-level** version (2–4 sentences max)
2. Show it to the user
3. Ask: "Does this capture the essence? What's missing or incorrect?"
4. Revise based on feedback
5. Move to the next section

### Problem (start here)

**Keep it high-level:**
- One sentence: what's broken or missing
- One sentence: who feels the pain
- One sentence: why it matters now

**Then ask**: "What specific use cases, edge cases, or nuances should we capture here?"

### Desired outcome

**Keep it high-level:**
- 2–3 bullet points: what users can do that they couldn't before
- One sentence: what "done" looks like

**Then ask**: "What concrete scenarios or success criteria should we add?"

### Appetite (recommendation)

**Keep it high-level:**
- **Recommended appetite**: Small Batch (1–2 weeks) or Big Batch (4–6 weeks)
- **One sentence rationale**: why this size fits

**Then ask**: "What constraints, dependencies, or business context should we note?"

### Solution idea (optional, rough)

**Keep it high-level:**
- One sentence: core approach
- One sentence: what it's NOT

**Then ask**: "What key capabilities or boundaries should we clarify?"

### Rabbit holes (known risks)

**Keep it high-level:**
- List 2–3 risks as one-line bullets
- Don't elaborate on solutions yet

**Then ask**: "What other risks or unknowns should we flag?"

### No-gos

**Keep it high-level:**
- List 3–4 items as one-line bullets

**Then ask**: "What else should be explicitly out of scope?"

## 4) Provide template for user to fill details

After reviewing all sections with the user, provide a **complete template structure** with:
- All sections expanded with detailed prompts/guidelines
- Placeholders showing what details to add
- Notes about what team discussions should cover

**Say**: "I've created a high-level skeleton. This is a starting point — please fill in the details based on your team discussions, user research, and domain knowledge. The AI output may miss important nuances, use cases, or edge cases that only your team can identify."

## 5) Next steps

Once the user has filled in the details:

- **If ready to shape**: run `/shape` with this Pitch to create a detailed Shaping doc
- **If needs approval**: share with stakeholders for betting table discussion
- **If needs research**: identify specific spikes to de-risk rabbit holes first
