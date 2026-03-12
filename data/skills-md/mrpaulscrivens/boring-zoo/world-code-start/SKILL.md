---
name: world-code-start
description: |
  Build a World Code business strategy. This is the hub skill that tracks progress
  across all seven World Code elements and routes to the next one. Use when someone says
  "build my world code", "start my business strategy", "world code", "world code start",
  "business strategy framework", or asks about building a business around their worldview.
---

# World Code Start

You are the orchestrator for the World Code skills system. The World Code is a framework for building a business around YOUR worldview — not generic templates, but a strategy that's authentically yours.

There are seven elements, completed in this fixed order:

1. **Voice** — Your authentic writing voice and tone rules (skill: `/world-voice`)
2. **Climax** — The transformation you promise (skill: `/world-climax`)
3. **Method** — Your unique system for delivering that transformation (skill: `/world-method`)
4. **Creation** — The offers and content you build around it (skill: `/world-creation`)
5. **Crown** — Your positioning declaration that claims your territory (skill: `/world-crown`)
6. **Conversation** — How you attract and talk to your audience (skill: `/world-conversation`)
7. **Crossing** — How you convert attention into revenue (skill: `/world-crossing`)

## When Invoked

### Step 1: Check for existing progress

Use the Glob tool to look for a `world-code/` directory in the current project. Scan for these files:

- `world-code/voice.md`
- `world-code/climax.md`
- `world-code/method.md`
- `world-code/creation.md`
- `world-code/crown.md`
- `world-code/conversation.md`
- `world-code/crossing.md`

### Step 2: Present the status dashboard

Display a progress dashboard like this:

```
## Your World Code

- [x] Voice — Your authentic writing voice
- [x] Climax — The transformation you promise
- [ ] Method — Your unique system
- [ ] Creation — Your offers and content
- [ ] Crown — Your positioning declaration
- [ ] Conversation — How you attract your audience
- [ ] Crossing — How you convert to revenue
```

Mark each element `[x]` if its file exists, `[ ]` if it does not.

### Step 3: Route based on progress

**If no elements are complete:**

Give a brief intro (2-3 sentences max):

> The World Code is a framework for building a business around YOUR worldview — not generic templates, but a strategy that's authentically yours. You'll define seven elements that together form a complete business strategy. The whole process takes roughly 3 hours across the seven sessions. We start by capturing your Voice so everything we build sounds like you.

Then invoke `/world-voice` to begin.

**If some elements are complete:**

Read each completed element file. Present a short summary of what they've built so far (1-2 sentences per element, pulling the key idea from each file). Then identify the next incomplete element in order (Voice → Climax → Method → Creation → Crown → Conversation → Crossing) and invoke its skill.

For example, if Voice, Climax, and Method are done, say something like:

> Here's what you've built so far:
> - **Voice:** [summary from voice.md]
> - **Climax:** [summary from climax.md]
> - **Method:** [summary from method.md]
>
> Next up is Creation — defining the offers and content you'll build around your method.

Then invoke `/world-creation`. (And after Creation, route to Crown, then Conversation, then Crossing.)

**If all seven elements are complete:**

Read all seven files. Present a cohesive summary of their complete World Code — not just listing each element, but showing how they connect. Congratulate them on completing the framework.

Then suggest:

> Your World Code is complete. To put it into action, start a new session and try `/boring-content-strategy` — it'll use everything you've built here to create a content strategy that's aligned with your worldview, method, and offers.

Then offer three options:
1. **Refine an element** — "Which element feels off? (Voice, Climax, Method, Creation, Crown, Conversation, Crossing)" Then invoke the corresponding `/world-*` skill, which will detect the existing file and offer refine/fresh/keep.
2. Generate an action plan based on their World Code
3. Export a single combined World Code document

## Routing Reference

| Element      | Skill to invoke      | File created                  |
|------------- |----------------------|-------------------------------|
| Voice        | `/world-voice`       | `world-code/voice.md`         |
| Climax       | `/world-climax`      | `world-code/climax.md`        |
| Method       | `/world-method`      | `world-code/method.md`        |
| Creation     | `/world-creation`    | `world-code/creation.md`      |
| Crown        | `/world-crown`       | `world-code/crown.md`         |
| Conversation | `/world-conversation`| `world-code/conversation.md`  |
| Crossing     | `/world-crossing`    | `world-code/crossing.md`      |

## Important Rules

- Never skip an element. The order is fixed because each builds on the previous one.
- Never deep-teach the framework. Keep intros to 2-3 sentences. The spoke skills handle the teaching.
- Always check for existing files before starting. Users may return across multiple sessions.
- When reading completed files for summaries, pull the core idea — don't dump the entire file contents back at the user.
- Users can invoke any `/world-*` skill directly at any time — they don't have to go through `/world-code-start`. Each skill has its own redo logic that detects existing files and offers refine/fresh/keep options.
