---
name: clean-code-design
description: Guide code design toward simple, maintainable structure before or during implementation. Use when Codex is designing a new module, adding APIs, refactoring complex code, splitting files, reducing global state, deciding whether to introduce abstractions, or evaluating whether a feature's complexity is justified.
---

# Clean Code Design

## Overview

Apply a small set of design rules that bias code toward clarity, reuse, and low
complexity. Prefer simple structures, explicit tradeoffs, and small units over
clever or deeply layered solutions.

## Design Workflow

Follow this order before writing substantial code:

1. Restate the problem in the smallest useful scope.
2. Check whether existing modules, algorithms, data structures, or libraries
   already solve most of it.
3. Choose the simplest design that satisfies the requirement.
4. Identify complexity that is optional rather than necessary.
5. Split responsibilities into small functions and small files before adding
   abstractions.
6. Explain tradeoffs when a requested feature materially increases complexity.

## Core Rules

## Prefer KISS

Keep the design easy to explain. Reject unnecessary indirection, excessive
configurability, and speculative abstractions. Treat "less is more" as the
default position.

## Compress Wide Parameter Lists

When a new interface needs many related parameters, group them into a struct,
object, or options type. Use this to improve readability, call-site stability,
and future extensibility. Avoid wrapping a tiny parameter list just for style.

## Convert Repeated Parameters Into State

When the same parameter set is threaded through many functions, consider
introducing an object that owns that state. Prefer passing shared state through
`this`, instance fields, or an explicit receiver rather than repeating long
parameter chains. Do this only when the grouped functions form a coherent unit.

## Replace Global State With Context

When global variables become numerous or leak across modules, consolidate them
into an explicit context object. Pass the context deliberately so dependencies
become visible and testable. Keep the context focused; do not turn it into an
unbounded dump of unrelated state.

## Extract Shared Logic

When multiple modules repeat nearly the same logic, extract the common part into
a public helper, shared module, or reusable type. Extract only the stable shared
behavior. Do not create a generic utility if the duplication is accidental or
still diverging.

## Keep Functions And Files Small

Keep functions focused, easy to name, and easy to scan. Prefer functions under
50 lines and files under 200 lines when practical. Split by responsibility, not
by arbitrary line count. Use shallow, obvious names instead of clever or
overloaded ones.

## Question Complexity Early

When a feature introduces significant branching, state management, parsing, or
abstraction overhead, stop and evaluate necessity. Explain the gains, costs, and
simpler alternatives to the user. If the feature is needed, isolate complexity
behind clear module boundaries or layered interfaces.

## Reuse Before Rebuilding

Before implementing a module, check whether the need is already covered by
existing code or a mature library. Search especially for common algorithms,
parsers, serialization helpers, and standard data structures. Prefer proven
libraries when they reduce complexity without introducing disproportionate
dependency cost.

## Choose Parsing By Complexity

Match the parsing approach to the input:

1. Parse simple strings manually.
2. Use regular expressions or glob-style matching for moderately structured
   text.
3. Use a parser generator only when the grammar is genuinely complex.

Avoid premature parser frameworks for trivial formats.

## Response Pattern

When using this skill during design or review, structure the guidance like this:

1. State the simplest viable design.
2. Call out any parameter-grouping, objectification, context extraction, or
   shared-logic extraction opportunities.
3. Highlight complexity risks and whether they are justified.
4. Suggest file and function boundaries if implementation is about to begin.

If the requested design remains complex, say so directly and explain why.
