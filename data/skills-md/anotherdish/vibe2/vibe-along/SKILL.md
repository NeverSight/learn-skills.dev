---
name: vibe-along
description: Guide a planning/design discussion that progressively lowers decisions into vibe pseudocode written directly into files. Use when the user invokes /vibe-along and wants to think through how to implement something while capturing decisions as vibe stubs in real files.
---

vibe-along is the complement to the vibe skill. Where vibe converts existing vibe pseudocode into working implementations, vibe-along captures a live planning conversation *as* vibe pseudocode — writing the thinnest possible structural stubs into files as decisions are made, from the highest level of abstraction down.

## Activation

Activate on `/vibe-along`. Stay active for the rest of the conversation — there is no formal exit.

If the user provides a task description in the invocation message, use it. If not, ask: "what are we building?"

**When composed with another skill** (e.g. grill-me driving the interview): vibe-along still owns the file-writing responsibility. Write a vibe stub immediately after each answer is confirmed — do not wait for the other skill to finish or hand back control.

## Before the discussion starts

Read files directly relevant to the described scope. Do not load the whole codebase — only what is adjacent to where the new work will land. Use this context to ground decisions in what already exists.

## Discussion levels

Work through decisions top-down. Do not invent content for a lower level while still settling a higher one.

1. **Files/modules** — what files exist, what each one owns
2. **Interfaces/contracts** — what each file exports, function signatures, data shapes
3. **Internal structure** — what major blocks or sections exist inside each unit
4. **Logic placeholders** — what the algorithmic steps are (still vibe, not implementation)

## Writing vibe code

Write to files immediately when a decision lands. Do not batch.

Match vibe code depth to the current discussion level:

- **Level 1** — a single top-level vibe comment describing the file's responsibility:
  ```python
  # vibe: auth module — login, logout, session management
  ```
- **Level 2** — function/type stubs with vibe comment bodies:
  ```python
  def login(user, password):
      # vibe: validate credentials against store
      # vibe: return session token
  ```
- **Level 3** — internal sections marked with vibe comments:
  ```python
  def login(user, password):
      # vibe: validate credentials
      # vibe: check rate limits
      # vibe: return session token
  ```
- **Level 4** — specific algorithmic steps:
  ```python
  def login(user, password):
      # vibe: hash password with stored salt
      # vibe: compare against db record
      # vibe: if match, create session and return token
      # vibe: if no match, increment failure count and raise
  ```

Keep vibe code structurally as simple as possible. Describe placeholders for units of functionality and abstractions — not implementation detail.

### New files

Create the file immediately when the decision is made, even if it only contains a single top-level vibe comment.

### Existing files

Add `vibe:` inline comments or `startvibe`/`endvibe` blocks to mark where new logic needs to land. Do not rewrite existing code.

### Multi-file decisions

When a decision spans multiple files (e.g. a caller and a callee), write stubs in all affected files simultaneously.

## Driving the conversation

Follow the user's lead. When a level appears settled — the key decisions have landed and been written — silently descend to the next level without announcing it. If the user seems uncertain or is circling back, stay at the current level.

Prompt the user when decisions are needed to unblock the next level. Ask one question at a time.
