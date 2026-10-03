---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, compare them in a visual HTML report, then explore a chosen candidate with the user. Use when asked to review or improve architecture, module boundaries, or codebase navigability.
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Improve codebase architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

Before the review, load the `codebase-design` skill. It is the single source of truth for **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**, the deletion test, and dependency categories. Use those terms when describing architectural roles and outcomes; preserve repository domain names, file names, protocol names, and quoted code terminology as evidence.

## Process

### 1. Explore

**Scope before you scan — YAGNI.** Deepening pays off where future changes concentrate, so establish the target before examining its internals.

1. Establish the repository root and the available evidence: version-control history, relevant code, callers, tests, and dependency declarations.
2. Establish the domain-document layout through the `domain-modeling` skill's **Establish the document layout** step. Read the selected domain context and ADRs affecting the target area before interpreting its seams. Record an unavailable history, context document, or ADR directory as absent evidence rather than inferring its contents.
3. Determine scope:
   - When the user names a module, subsystem, or pain point, use that direction.
   - Otherwise, inspect a useful stretch of recent history for paths that recur. Let a concentrated hot spot set the initial scope; when the changes are dispersed, compare the most recurrent areas.
4. Spawn a sub-agent with the selected scope and evidence requirements. Have it inspect the involved modules, their callers, tests, and dependencies, then return observed friction with file-level evidence.
5. Assess observed friction through these lenses:
   - Understanding one concept requires moving across several modules.
   - A module is **shallow**: its interface approaches the complexity of its implementation.
   - Logic extracted for testability leaves its call-site behavior untested, reducing **locality**.
   - Coupled modules leak across a **seam**.
   - An interface makes behavior difficult to test.
6. Apply the **deletion test** to each plausible candidate. Identify whether deletion would concentrate complexity in callers or merely remove a pass-through. Classify its dependencies using the dependency categories the `codebase-design` skill defines in its deepening reference, so its future test surface is credible.
7. Calibrate each candidate from the evidence:
   - **Strong** — repeatable friction in the selected scope, a deletion test that supports deepening, and a credible dependency/test shape.
   - **Worth exploring** — observed friction and a plausible deepening, with a material dependency or ownership question still open.
   - **Speculative** — a concrete hypothesis whose next observation can confirm or reject it.

**Complete when:** every reported candidate has file-level evidence, a stated source of friction, a deletion-test result, a dependency category, and a calibrated strength; unavailable repository or domain evidence is explicit.

### 2. Present candidates as an HTML report

Load [HTML-REPORT.md](references/HTML-REPORT.md) before composing the report. It is the single source of truth for the report scaffold, card structure, diagrams, and visual style.

Write one HTML file to the OS temp directory, keeping the repository unchanged. Resolve the temp directory from `$TMPDIR`, falling back to `/tmp` on Linux/macOS or `%TEMP%` on Windows. Write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. The report loads Tailwind and Mermaid from their CDNs; open it with the platform command and return its absolute path.

Keep each candidate at decision level: show the friction, the responsibility that could become local, the affected seam, and the test/dependency shape. Reserve alternative interface design for the selected-candidate discussion.

Surface an ADR conflict only when observed friction warrants reconsidering it. Mark the relevant card with the ADR and the code evidence that justifies reopening the decision.

When one or more candidates are evidence-backed, end by asking: **“Which of these would you like to explore?”** When none are evidence-backed, state that outcome, list the examined scope and unavailable evidence, and ask whether the user wants a broader or differently focused scan.

**Complete when:** the HTML file exists at a unique temporary path, contains every evidence-backed candidate, and has been opened for the user with its absolute path returned. When candidates exist, it includes one evidence-backed top recommendation in the prescribed format; otherwise it records the examined scope and evidence gaps without a recommendation card.

### 3. Explore the selected candidate

Once the user chooses a candidate, run the `grilling` skill to work its **design tree** with them: constraints, dependencies, the deepened module's responsibility, its seam, what remains behind it, and the tests that survive. The `grilling` skill owns the questioning loop and its completion criterion.

As decisions settle, apply the `domain-modeling` skill to keep the selected domain context and ADR directory current:

- A settled deepened-module name introduces a domain concept: capture the term in the selected context document.
- A settled decision sharpens an existing fuzzy term: update its definition in the selected context document.
- A user rejects the candidate for a durable, non-obvious reason: offer to record that decision as an ADR when future architecture reviews need it to avoid reopening the same proposal.
- The user asks to compare alternative interfaces: run the design-it-twice pattern from the `codebase-design` skill.

**Complete when:** the `grilling` skill has exhausted the selected candidate's decision frontier, the `domain-modeling` skill reflects every settled term and qualifying decision, and the user has confirmed shared understanding before implementation or publication begins.
