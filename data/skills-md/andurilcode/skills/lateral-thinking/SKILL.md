---
name: lateral-thinking
description: Apply lateral thinking whenever the user is stuck on a problem, has tried the obvious solutions without success, needs to generate new ideas or alternatives, or wants to break out of conventional thinking patterns. Triggers on phrases like "we're out of ideas", "nothing seems to work", "what else could we try?", "how do we innovate here?", "we keep thinking about it the same way", "what if we approached this differently?", "brainstorm alternatives", "we need a creative solution", or any situation where analytical thinking has hit a ceiling. Also trigger when a proposed solution is merely an incremental improvement on the existing approach — lateral thinking looks sideways, not just forward. Don't keep digging in the same direction when the hole isn't working.
---

# Lateral Thinking

**Core principle**: Most thinking is vertical — digging deeper in the same direction, refining what already exists. Lateral thinking moves *sideways* — deliberately escaping the dominant pattern to find a different place to dig. The goal is not a better version of the current solution. It's a different solution entirely.

> *"You cannot dig a hole in a different place by digging the same hole deeper."* — Edward de Bono

---

## When Vertical Thinking Fails

Vertical thinking is efficient when the problem is well-defined and the solution space is known. It fails when:
- The problem keeps recurring despite fixes (the frame is wrong)
- All solutions feel like variations of the same idea
- The best available option is "least bad"
- Everyone in the room agrees on the approach (groupthink + vertical thinking)
- The problem is genuinely novel

When any of these are true, stop digging. Move laterally.

---

## Core Techniques

### 1. Random Entry
Introduce a completely unrelated stimulus — a random word, image, or object — and force a connection to the problem.

**Process:**
1. Pick a random word (or use one: *bridge / fog / anchor / seed / mirror / friction*)
2. List properties or associations of that word
3. Force-connect each property to the problem
4. Don't filter — connections that seem absurd often lead somewhere real

**Why it works**: The random stimulus activates parts of the solution space the brain wouldn't reach through logical progression.

**Example**: Problem: *how do we reduce agent pipeline errors?*
Random word: *filter*
Associations: removes impurities, selective, layered, passive
→ Idea: add a passive validation layer between agents that only flags, never blocks — removes errors without slowing the flow

---

### 2. Provocation (Po)
Make a deliberately absurd, impossible, or reversed statement about the problem — then extract useful ideas from it.

**Provocations use the operator "Po"** (signals it's a provocation, not a claim):
- *Po: the agent has no memory at all*
- *Po: users pay us to make mistakes*
- *Po: the bottleneck is the solution*
- *Po: we do the opposite of what we're doing now*

**Process:**
1. State the provocation (make it extreme — mild provocations produce mild ideas)
2. Ask: *"What would have to be true for this to work?"*
3. Ask: *"What intermediate ideas does this generate?"*
4. Extract the usable concepts, even if the provocation itself is impossible

**Example**: Problem: *onboarding takes too long*
Po: *users onboard themselves before they meet us*
→ Idea: pre-onboarding flow that users complete asynchronously, so the first live interaction starts mid-process, not at the beginning

---

### 3. Challenge
Question every assumption about *why* things are done the way they are — not to criticize, but to open alternatives.

**Challenge questions:**
- *"Why is it done this way?"*
- *"Does it have to be done at all?"*
- *"Does it have to be done in this order?"*
- *"Does it have to be done by this person/system?"*
- *"Does it have to be done at this point in the process?"*

Every "because that's how it's done" is a candidate for lateral escape.

**Distinguish:**
- **Necessary constraints**: Remove them and the goal disappears (challenge won't help here)
- **Arbitrary constraints**: Historical, habitual, or inherited — fertile ground for lateral thinking

---

### 4. Alternatives (Fixed Point)
Fix the goal but change everything else. List as many alternative ways to achieve the same outcome as possible — without evaluating any of them until the list is complete.

**Process:**
1. State the fixed point: *"The goal is [outcome]"*
2. Generate 10+ routes to that outcome — including the obvious, the strange, and the impractical
3. Only evaluate after the full list exists (evaluation during generation kills lateral thinking)
4. Look for hybrids between non-obvious options

**Quota thinking**: Set a number before you start ("we need 15 alternatives") — it forces you past the first 3–4 obvious answers into genuinely new territory.

---

### 5. Concept Extraction
Abstract the current solution to its core concept, then find other ways to deliver the same concept.

**Process:**
1. Describe the current solution in one sentence
2. Extract the underlying concept: *"The concept here is [X]"*
3. List other implementations of that same concept
4. Pick the most promising and develop it

**Example**: Current solution: *weekly sync meeting to align the team*
Core concept: *shared awareness of state*
Alternative implementations: async status page, ambient dashboard, daily digest message, visual kanban, automated diff reports
→ Some of these are faster, quieter, and more persistent than a meeting

---

### 6. Reversal
Reverse the problem statement entirely. Then ask what that reversed world looks like, and work backwards to generate ideas.

**Process:**
1. State the problem: *"How do we get more users to complete onboarding?"*
2. Reverse it: *"How do we get users to abandon onboarding?"*
3. List everything that would cause the reversed outcome
4. Invert those back into ideas for the original problem

**Why it works**: The reversed problem is often easier to answer — and inverting the answers surfaces ideas that pure forward thinking wouldn't reach.

---

## Output Format

### 🔀 Dominant Pattern Identification
Before generating alternatives, name the dominant pattern being broken:
- *"The current thinking is: [frame/assumption/direction]"*
- *"The rut is: [what keeps pulling solutions back to the same place]"*

### 💡 Generated Alternatives
Present ideas grouped by technique used. For each:
- **Idea**: One-sentence description
- **Origin**: Which technique generated it (signals it's deliberate, not random)
- **Kernel**: The useful concept inside, even if the idea as stated is impractical

Don't filter during generation. Quantity first, quality second.

### 🌱 Most Promising Concepts
After generation, select the 2–4 ideas with the most potential:
- What makes this worth developing?
- What would need to be true for it to work?
- What's the next concrete step to test it?

### ⚠️ Dominant Pattern Traps to Watch
Note any ideas that are actually vertical (refined versions of the existing approach disguised as new ideas). Flag and set aside — they belong in a different conversation.

---

## Rules for Lateral Thinking Sessions

1. **Suspend judgment** during generation — evaluation kills divergence
2. **Welcome the absurd** — impractical ideas often contain useful kernels
3. **Quantity before quality** — the goal is to move past the first 3 obvious answers
4. **Build, don't reject** — "yes, and..." before "yes, but..."
5. **Name the dominant pattern first** — you can't escape a rut you haven't identified

---

## Thinking Triggers

- *"What would this look like if we had no history with the problem?"*
- *"Who solves a completely different problem in a way that could apply here?"*
- *"What's the most counterintuitive thing we could do?"*
- *"If we couldn't use the current approach at all, what would we do?"*
- *"What would a 10-year-old suggest? What about someone from a completely different industry?"*
- *"What are we not allowed to question — and why?"*

---

## Example Applications
- **"We've tried everything to reduce churn"** → Challenge every assumption about what "reducing churn" means, then use Reversal to find what causes people to *want* to leave — inverted back into retention ideas
- **"Our pipeline is slow and we don't know how to speed it up"** → Random Entry + Provocation to break out of "optimize each step" thinking
- **"We need a new feature but everything feels incremental"** → Concept Extraction to abstract what users are really hiring current features to do, then explore radically different implementations
- **"The team keeps proposing the same solutions in retros"** → Fixed Point alternatives with a quota of 15 — forces past the obvious into genuinely new territory
