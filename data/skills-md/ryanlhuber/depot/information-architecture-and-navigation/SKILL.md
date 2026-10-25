---
name: information-architecture-and-navigation
description: "Defines how content and functions are grouped, labeled, and reached, and verifies that key destinations are findable. Use when designing or restructuring a product's organization, or when users struggle to find things."
---

# Information Architecture and Navigation

## Purpose
Define how content and functions are grouped, labeled, and reached, and verify that key destinations are findable.

## When to use
- Use when: designing or restructuring the organization of a product, site, or large screen set.
- Use when: users report difficulty finding things, or the structure has grown without a model.
- Do not use when: the question concerns a single screen's layout.

## Inputs
- Required: the inventory of content and functions, and the primary user tasks.
- Optional: user vocabulary, usage data, platform conventions, constraints on depth or screen size, existing structure.
- Assumptions: unconfirmed priorities or vocabulary are marked as assumed.

## Process
1. Inventory items and classify each as content, function, or both; remove duplicates and note ownership.
2. Rank tasks by importance and frequency from the inputs, noting what is assumed.
3. Group items by user mental model and task relationship, not by internal org structure. Name each group using terms users use where known.
4. Define the hierarchy: top-level destinations, nesting depth, and which items appear in more than one place.
5. Choose navigation mechanisms (persistent, contextual, search, shortcuts) based on the number of destinations, task frequency, platform convention, and available space.
6. Write the labels and check each for clarity, distinctiveness, and consistency.
7. Verify findability: for each key task, trace the path from each entry point and count steps and decisions.
8. Identify orphaned items, ambiguous labels, overlapping groups, and excessive depth.

## Rules and heuristics
- Required: every item is reachable by a defined path; none is orphaned.
- Required: labels are distinct enough that a user can predict what each contains.
- Recommended: keep persistent top-level destinations few and stable; justify exceptions.
- Recommended: validate groupings and labels with representative users (sorting or findability tasks) when stakes are high.
- Treat any structure choice as a recommendation tied to context, not a universal rule.

## Checks
- All inventory items are placed.
- Each key task has a traced path with its step count.
- No two labels are interchangeable.
- Platform conventions in scope are respected or deviations are justified.

## Output
Return the hierarchy, navigation mechanisms per level, label list with rationale, task-path traces, identified problems, and recommended validation.

## Completion criteria
- Every item is placed and reachable.
- Key task paths are traced and justified.
- Unvalidated assumptions are listed.
