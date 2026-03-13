---
name: mikado-method
description: >
  Enforce and guide the Mikado Method when a developer is refactoring, restructuring,
  or dealing with legacy code. Use this skill whenever the user mentions refactoring,
  technical debt, legacy code, code restructuring, dependency untangling, or "breaking
  everything" when making changes. Also trigger when the user wants to make a large
  change safely, asks how to split a big refactoring task, wants to work on main branch
  without a long-lived feature branch, or asks how to incrementally improve a codebase.
  The skill enforces the full Mikado loop: goal → naive attempt → map prerequisites →
  revert → implement leaves → commit → repeat.
---

# Mikado Method Skill

A skill for guiding developers through the Mikado Method: a disciplined, graph-driven
approach to safe, incremental refactoring that keeps the codebase in a working state
at all times.

---

## What is the Mikado Method?

Named after the **Pickup Sticks** game (Mikado), where you must remove the topmost
sticks without disturbing the pile before reaching the high-value stick at the bottom.
In software, your **goal** (the "Mikado") sits beneath a pile of dependencies. The
method surfaces those dependencies visually so you can remove them one by one, safely.

> Think of it as a "to-do list on steroids" — a living graph that is simultaneously
> your plan, your progress tracker, and your communication tool.

---

## Core Definitions

| Term | Meaning |
|---|---|
| **Goal** | The root node. What you ultimately want to achieve (e.g., "Encapsulate DB", "Extract Interface"). Circle it twice so it doesn't get lost. |
| **Prerequisite** | A dependency that must be resolved before its parent node can be done. Becomes a child bubble in the graph. |
| **Leaf node** | A node with no further prerequisites. Safe to implement immediately without breaking anything. |
| **Mikado Map / Graph** | The full tree of goal + prerequisites. Your "save game" for the refactoring. |
| **Revert** | Undoing all changes to return to a stable, compiling/passing state. The map survives; the broken code does not. |

---

## The Core Loop

Repeat this cycle until all leaves are resolved and the goal is reached:

```
1. SET GOAL        → Write the goal as the root node. Circle it twice.
2. BE NAIVE        → Attempt to implement the goal directly in the code.
3. OBSERVE BREAKS  → Compiler errors, failing tests, or broken behavior = prerequisites.
4. MAP             → Add each prerequisite as a child bubble connected to the current node.
5. REVERT          → Undo ALL changes immediately. Return to green/stable state.
6. PICK A LEAF     → Choose any leaf node (no children) and repeat the loop from step 2 on it.
7. COMMIT LEAF     → Once a leaf is implemented cleanly without breakage, commit it.
8. PRUNE THE GRAPH → Remove the committed leaf. Reveal new leaves. Continue upward.
```

⚠️ **The revert step is non-negotiable.** It feels counterintuitive to throw away
"hard work," but the thought process IS the work — it produced the map. Never build
on top of broken code.

---

## Building the Mikado Graph

### Starting a new graph

When the user presents a refactoring goal, help them:

1. **Name the goal precisely** — vague goals produce vague maps. Bad: "clean up the DB
   layer". Good: "Replace `FileDatabase` with a `DatabaseInterface`".
2. **Draw the root node** — on paper, whiteboard, or a tool like Mermaid or Excalidraw.
3. **Attempt the change naively** in a throwaway branch or with `git stash` ready.
4. **List every error/breakage** — each one becomes a child bubble.
5. **Revert immediately** — `git checkout .` or `git stash drop`.

### Populating prerequisites

For each prerequisite node, apply the same loop recursively. A prerequisite may itself
have prerequisites. The graph grows depth-first until you reach nodes that:
- Can be implemented without touching anything else (leaves), OR
- Map to a single atomic refactoring from Fowler's catalog.

### What makes a good leaf?

A leaf node is ready to implement when:
- It compiles/passes tests after the change with NO other modifications needed.
- It can be expressed as **one atomic commit** (a single refactoring gesture: rename,
  extract method, move class, add parameter, etc.).
- It does **not change observable behavior** (internal structure only).

---

## Execution Strategy

### Order of work

Always implement **leaves first**, work upward toward the goal. Never attempt a parent
node until all its children are committed and pruned from the graph.

```
Example graph execution order:

Goal: Replace FileDatabase with DatabaseInterface
  ├── Extract DatabaseInterface              ← implement 3rd
  │   ├── Move FileDatabase to impl/         ← implement 1st ✓
  │   └── Update all import paths            ← implement 2nd ✓
  └── Add constructor injection              ← implement 4th
      └── Rename constructor param           ← implement 1st ✓
```

### Committing

- One commit per leaf node.
- Commit message should name the atomic refactoring: `"Extract: DatabaseInterface from FileDatabase"`.
- Commits go directly to **main/trunk** — no refactoring branches needed.
- Never commit a node that leaves the build broken or tests failing.

---

## Practical Guidance by Situation

### Legacy code with no tests

Use the **Mikado + Test Data Builder** combination:
1. Make "add a test around this bug/feature" a node in the graph.
2. Each prerequisite for that test (instantiating a tangled class) becomes a
   **Test Data Builder** node — a reusable builder other developers can leverage.
3. Each completed builder increases system-wide testability virally.
4. Avoid mocks for data setup — they duplicate real behavior and create rigidity.

### Circular dependencies

A classic Mikado target. Typical leaf sequence:
1. Identify the cycle (compiler/linter output).
2. Leaves: move classes, add interfaces, update imports.
3. Work inward until the cycle is broken.

### Very large / multi-week refactorings

- Keep the graph on a **physical whiteboard** visible to the whole team.
- Long-running graphs (weeks or months) are normal — the map tracks progress.
- Team members can pick up any current leaf node independently.
- The graph is also a **negotiation tool**: show stakeholders the dependency tree to
  make scope/cost trade-offs visible (e.g., "removing this node saves 3 months").

### Solo / informal use

For small tasks, the method can be done mentally. For anything touching more than
~3 files or taking more than a day, always externalize the map (paper is fine).

---

## Enforcing Good Refactoring Hygiene

When reviewing or generating refactoring code, enforce these rules:

1. **No behavior changes in a refactoring commit.** Renaming a variable ✓. Renaming
   a public API endpoint ✗ (that is a breaking change).
2. **One type of change per commit.** Mixed commits (rename + extract + move) make
   the graph untrustworthy and rollback dangerous.
3. **Always return to green before picking the next leaf.** If the build is red,
   revert — do not patch forward.
4. **No "just one more thing" creep.** If a new prerequisite is discovered mid-leaf
   implementation, stop, add it to the map, and revert. Do not chain fixes.
5. **Prefer TDD.** Fast test feedback makes error discovery immediate, shrinking
   the identify-prerequisites step dramatically.

---

## Output Format

When helping a user apply the Mikado Method, always produce:

### 1. The Mikado Map (Mermaid diagram)
```mermaid
graph TD
    G(["🎯 GOAL: <goal name>"]) --> P1["Prerequisite A"]
    G --> P2["Prerequisite B"]
    P1 --> L1["🟢 Leaf: step 1"]
    P1 --> L2["🟢 Leaf: step 2"]
    P2 --> L3["🟢 Leaf: step 3"]
```
Use 🟢 for current leaf nodes (safe to implement), ⬜ for prerequisites not yet
reachable, ✅ for completed nodes.

### 2. Ordered implementation plan
A numbered list of leaf-first steps, each with:
- The atomic refactoring gesture (from Fowler's catalog if applicable)
- A one-line test to verify it didn't break behavior
- The suggested commit message

### 3. Revert reminder
After any naive attempt, explicitly remind the user: **"Revert now — `git checkout .`
— your map is saved, the broken code is not needed."**

---

## Common Mistakes to Correct

| Mistake | Correction |
|---|---|
| Fixing errors in place instead of reverting | "Revert now. Add these errors as prerequisite nodes instead." |
| Building on top of broken code | "This violates the core rule. Revert to green before continuing." |
| One giant commit with multiple changes | "Split into one commit per leaf node." |
| Skipping the graph for "small" refactors | "Start with even a 3-node graph. It prevents scope creep." |
| Using mocks to avoid test data setup pain | "This creates Mock Hell. Use Test Data Builders as Mikado leaf nodes instead." |
| Long-lived refactoring branches | "Work on main. Only commit leaves that don't break anything." |

---

## Quick Reference Card

```
MIKADO LOOP
───────────
① Write goal (root) → circle it twice
② Attempt naively in code
③ Every error = a prerequisite bubble
④ REVERT (always, immediately)
⑤ Pick a leaf → repeat from ②
⑥ Leaf passes cleanly → commit → prune
⑦ Repeat until goal is reached

RULES
─────
• Never build on broken code
• One atomic change per commit
• No behavior changes in refactoring commits
• Leaves only touch one concern
• The map is the work — protect it
```
