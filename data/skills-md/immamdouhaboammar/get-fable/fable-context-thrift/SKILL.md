---
name: fable-context-thrift
description: Use at the start of any multi-step task and during exploration — before reading files, searching, or re-checking completed work, especially when tempted to read whole files, re-verify known facts, or run independent lookups one at a time.
version: 1.0.0
pack: system
inputs:
  - exploration_intent
requires:
  - codebase_access
produces:
  - targeted_evidence
gates:
  - context_budget_conserved
fallback: fable-discover
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - get-fable
  continuations:
    - fable-discover
    - fable-execute
  lateral_peers:
    - fable-scope-discipline
  recovery: fable-recover
---

# Fable Context Thrift

Context is the budget everything else is paid from. Spend it on what changes your next action; nothing else.

## Purpose

Prevent context bloat, token exhaustion, unnecessary whole-file reads, redundant verifications, and sequential execution latency. `fable-context-thrift` treats context tokens and tool calls as a scarce, valuable engineering budget.

## When to Use

- At the start of any multi-step task and during exploratory codebase investigations.
- Before reading files, searching symbols, or checking repository structure.
- When tempted to read entire files rather than targeted slices, symbols, or functions.
- When executing multiple independent lookups or checks that can be batched in parallel.

## When NOT to Use

- Comprehensive codebase discovery requiring structural mapping of unknown subsystems (use `fable-discover`).
- External API documentation and primary-source research (use `fable-research`).
- Deep vulnerability tracing across distributed trust boundaries (use `fable-security`).

## Inputs

- `exploration_intent`: The specific load-bearing question or uncertainty to be resolved.
- `workspace_state`: Existing established facts, open files, and previous tool outputs.

## Expected Outputs

- `targeted_evidence`: Minimal, high-signal code excerpts, line references, and exact facts.
- `decision_readiness`: Confirmation that the "enough-to-act" bar is reached with zero extraneous tokens.

## Procedure

1. **Targeted Read Strategy**: Read only the symbol or section needed, not the file. Widen only when a specific question demands it.
2. **Parallel Block Batching**: Multiple greps, reads, or status checks must be dispatched in one parallel block. Sequencing independent reads adds latency, not care.
3. **Delegate Sweeps vs Keep Lookups**: Broad questions ("where is X handled", find-all-usages in unfamiliar territory) go to a search subagent if available — keep the conclusion, not the file dumps. Known single lookups stay direct. The subagent is for when you *don't* know where things live.
4. **Tool Confirmation Principle**: Never re-read a file to check an edit landed; the edit tool fails loudly. Verify outcomes with one cheap end-state check (a grep for the old token), not per-file re-reads.
5. **Preserve Established Facts**: What the conversation already verified, don't re-derive. What the user already decided, don't reopen.
6. **Eliminate Narrative Overhead**: Don't narrate options you won't pursue. Deliberation is for choices you might actually make.
7. **The Enough-to-Act Test**: If more exploration would not change your next action, exploration is over. Act.

## Decision Rules

| Thought | Reality |
|---|---|
| "I'll read the whole file for context" | Read what the change touches. The question you're answering defines the lines you need. |
| "Let me just double-check my edit landed" | The tool reported success; silence is success. One end-state grep beats N re-reads. |
| "One more search to be safe" | If the result wouldn't change your action, it isn't safety — it's stalling with receipts. |
| "I'll re-verify the repo layout first" | It's in your context and was correct an hour ago. Directory trees don't rot mid-session. |
| "Careful means one call at a time" | Careful means right calls. Independent lookups in sequence is the same work, slower. |
| "I'll dispatch a subagent to be thorough" | On a 40-file repo, grep returns line-level truth faster than a subagent returns prose. Match the tool to the territory. |

- If an additional search result would not change your next command or edit, do not make the search.
- When an edit succeeds cleanly, proceed directly to verification without viewing the modified file again.

## Tool Policy

- Batch all independent read and grep tool calls into a single message/turn.
- Use line offsets and targeted slices (`StartLine`, `EndLine`) when viewing files.
- Reject whole-file reads where ripgrep already provided exact line numbers.
- Prefer targeted ripgrep queries over file-tree traversal when locating symbols.

## Evidence Requirements

- Report line-level citations (`path/to/file#L10-L25`) rather than dumping full function bodies into conversation.
- Use single end-state checks (e.g. grep for deleted token or exit code) as proof of edit application.
- Preserve established facts without requiring repeat execution evidence in the same session.

## Failure Handling

Stop spending immediately when encountering any of these Red Flags:
- A Read call for a file you edited this turn.
- The same fact verified twice in one session.
- Sequential tool calls with no data dependency between them.
- An exploration step you can't name the decision for.
- Whole-file reads where a grep already gave you the line numbers.

## Completion Criteria

- The load-bearing question is answered with minimum tokens spent.
- The next engineering action is unblocked and clear.
- Context space is preserved for implementation, verification, and diff review.
