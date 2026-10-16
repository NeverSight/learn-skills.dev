---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every spawn is a read-only `general-purpose` subagent. Explorers use the `how explorer` line in the pstack models config (default `sonnet`), and every explainer uses the `how explainer` line (default `opus`). Use the **pstack-harness** skill to resolve each spawn's model, effort, and agent type. Its **Spawn a role** section also covers a missing config, `inherit-parent`, and a rejected value.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` with the Direct exploration instructions. Omit Explorer Findings and Synthesis. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

If the repo has a GitNexus index (`.gitnexus/` exists) and `gitnexus` is on `PATH`, refresh it first — run `gitnexus analyze --index-only` once yourself before spawning anything (it is incremental and a no-op when up to date; never run it from parallel arms). Then seed exploration: `gitnexus query "<concept>"` for execution flows, `gitnexus context <symbol>` for callers/callees, `gitnexus trace <from> <to>` for the path between two symbols. Graph results choose where to read; the code itself remains the source of truth — the index reflects the last analyzed commit and never sees uncommitted edits. Without the index or the CLI, explore normally. When the repo has no index but `gitnexus` is on `PATH`, after answering a complex question, you may suggest `gitnexus analyze` to the user once for repos worth exploring again.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers in a single message, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md`, every explorer's findings, and the Synthesis instructions filled in. Omit Direct exploration.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
