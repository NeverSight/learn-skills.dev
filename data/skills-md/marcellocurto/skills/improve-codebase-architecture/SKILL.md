---
name: improve-codebase-architecture
description: Find high-value ways to deepen a codebase's modules, present them visually, and explore the chosen change.
disable-model-invocation: true
---

# Improve Codebase Architecture

Find code that is hard to follow or change because callers must coordinate details that belong together. Propose modules that hide those details and make the behavior easier to test.

When the user has already selected a candidate or concrete target change, inspect that target and proceed directly to exploring it. Do not produce another candidate menu or ask them to select it again. A named subsystem may instead limit discovery when the user is still asking which change would help.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Consult the `codebase-design` skill when available for deep-module principles, caller contracts, and seam justification. Use its architectural distinctions alongside established product and repository vocabulary. Evaluate what an interface hides and what callers gain; adapter count alone does not justify or rule out a seam.
- The project's glossary gives names to good seams; its ADRs record decisions this command should not re-litigate. Follow the existing documentation locations rather than assuming `CONTEXT.md` and `docs/adr/`.

Locate companion skills by name in the available skill catalog, using its supplied locations or loading mechanism. If one is unavailable, continue with the procedure here; do not infer its installation path or fetch external guidance.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, use recent commit history (`git log --oneline`) to select an initial area where repeated change suggests maintenance cost. Broaden that area only when the evidence or requested coverage warrants it.

Read the project's existing domain glossary and any ADRs in the area you're touching first.

Explore the scoped area directly. Delegate a bounded, read-only slice when delegation is available and an independent investigation can improve evidence or save time alongside useful local work. Give the agent the question, target modules or paths, known requirements and constraints, and the expected result: concrete code locations or caller traces, the maintenance cost they demonstrate, a plausible improvement, and any uncertainty. If delegation is unavailable or adds little value, continue locally.

Look for friction supported by the code:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Before recommending removal of a module, check whether that removes unnecessary forwarding or makes callers handle its work themselves. Verify delegated findings against the code before presenting them. Stop when you can explain a concrete cost and a useful improvement in the requested area, or identify the facts still missing. No worthwhile candidate is a valid result.

### 2. Present the findings in a useful format

Follow the requested format and the environment's actual rendering capabilities. For a compact review, use concise prose with an inline diagram when the host can render it. For a portable report or a comparison that benefits from a separate artifact, use HTML. If visual rendering is unavailable, explain the relationships in text and state the limitation rather than blocking the analysis.

Use visuals where they clarify ownership, dependencies, caller effort, or the proposed change. A before/after diagram is useful when the structural difference matters; do not invent several candidates or diagram types merely to fill a report. Use the host's supported Mermaid rendering, inline SVG, or simple HTML/CSS as appropriate.

When writing an HTML report, use inline CSS and SVG so it opens without network dependencies. Save it to the requested location, otherwise to a fresh file in the OS temp directory. Use an available artifact preview to show it, or provide its absolute path and a link when opening is unavailable. Do not require a particular OS command or external browser.

For each candidate, provide the evidence needed to judge it:

- **Evidence**: relevant files, symbols, and caller traces
- **Problem**: the concrete friction and its consequence
- **Solution**: plain English description of what would change
- **Benefits**: concrete gains for callers and maintainers, including testability when affected
- **Structural comparison**: a diagram or concise explanation of what callers and maintainers would need to know afterward
- **Recommendation strength and uncertainty**: how strongly the evidence supports the change and what remains unverified

Recommend the strongest candidate when discovery was requested. For a selected target, explain whether the evidence supports that change and proceed with its design question. Use concise explanatory prose wherever a diagram alone cannot communicate the contract or tradeoff.

Use the project's glossary vocabulary for domain concepts and preserve established names such as "Order service." Explain how those names map to the architectural roles under discussion when the distinction matters.

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Explain the conflict and the evidence for reopening the decision in the report. Don't list every theoretical refactor an ADR forbids.

Read [HTML-REPORT.md](HTML-REPORT.md) only when producing an HTML artifact. Inspect the rendered report when the environment allows it and disclose any rendering gap; generating a file does not prove its diagrams are readable.

For discovery-only requests, deliver the findings and stop. If further exploration is requested but several materially different candidates remain, ask which to explore after presenting the evidence. When the target is already clear, continue without that selection pause.

### 3. Explore the selected change

Ground the selected candidate in its callers, constraints, dependencies, and existing tests. Reuse settled decisions and proceed directly to a concrete interface or migration recommendation when the evidence supports it. Use the `grilling` skill when available for material unresolved choices; otherwise ask focused questions about those choices directly. Do not require an interview when no human decision is missing.

Use the `domain-modeling` skill when available to keep meanings and records aligned. Follow existing documentation conventions and the authorized working mode: write only when documentation updates are authorized, and keep proposed text in the conversation for read-only or discussion work.

- **Naming a deepened module after a new domain concept?** Record its agreed definition in the existing glossary, or propose the entry in discussion mode.
- **Resolving a material ambiguity in a term?** Update or propose the definition once its meaning is settled; harmless wording variations do not need a new record.
- **User rejects the proposal for a reason future reviews would need?** Offer to record that reason in an ADR so later reviews do not repeat the proposal without its context. Skip temporary reasons such as “not worth it right now” and reasons already clear from the code or documentation.
- **Want to explore alternative interfaces for the deepened module?** Use the alternative-interface comparison guidance provided by the `codebase-design` skill when available. Otherwise compare concrete interface options against the same caller needs, protected contracts, and migration constraints. Use parallel agents when useful and available.

Finish with the requested findings or design recommendation, its evidence, preserved contracts, and the verification or decision still needed. Implementation, commits, or external publication require authorization for that work; selecting a candidate alone does not authorize them.
