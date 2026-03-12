---
name: red-team-review
aliases: ["Review and Critique Pattern"]
description: "(Industry standard: Review and Critique Pattern) Primary Use Case: Iterative generation paired with adversarial review, continuing until an 'Approved' verdict is reached. Orchestrated adversarial review loop. Use when: research, designs, architectures, or decisions need to be reviewed by red team agents (human, browser, or CLI). Iterates in rounds of research → bundle → review → feedback until approved."
allowed-tools: Bash, Read, Write
---
# Red Team Review Loop

An iterative review loop where research is bundled via `context-bundler` and dispatched to one or more adversarial reviewers. The loop continues until the red team approves.

## When to Use

- Architecture or design decisions that need adversarial scrutiny
- Research findings that need epistemic validation
- Security analysis that needs independent verification
- Any work product where "more eyes" reduce risk

## Process Flow

1. **Research & Analyze** — Deep-dive into the problem domain. Create analysis docs, capture sources.
2. **Review Packet Generation** — Prepare the context for the reviewer:
   - **Create Prompt**: Write or update a `red-team-prompt.md` explaining exactly what is being reviewed and what the reviewer should focus on.
   - **Define Manifest**: Update a `manifest.json` or equivalent list dictating which source files and research artifacts to include.
   - **Bundle Context**: Execute the `context-bundler` plugin, feeding it the manifest and prompt, to compile a single cohesive review packet.
   - **Iteration Directory Isolation**: Bundle the context and save the output to explicitly isolated directories (e.g., `.history/review-iteration-1/`) so that when the Red Team forces a rewrite, the baseline artifact is never destructively overwritten.
3. **Dispatch to Reviewers** — Send the bundle to:
   - Human reviewers (paste-to-chat or browser)
   - CLI agents with adversarial personas (security auditor, devil's advocate)
   - Browser-based agents for interactive review
4. **Receive Feedback** — Capture the red team's verdict:
   - **"More Research Needed"** → Loop back to step 1 with targeted questions
   - **Asynchronous Benchmark Metric Capture**: Explicitly log the `total_tokens` and `duration_ms` used by the adversarial agent during this specific iteration into an `evals/timing.json` file to calculate the true cost of approval.
5. **Completion & Handoff** — Once the Red Team verdicts "Approved":
   - Terminate the review loop.
   - Pass the final, approved research and feedback documents back to the Orchestrator.
   - **DO NOT** attempt to seal the session or run a retrospective. The Orchestrator handles that.

## Dependencies

- **`context-bundler`** — Required for creating review packets
- **Personas** — Adversarial personas in `personas/` directory (e.g., `security-audit.md`, `architect-review.md`)

## Diagram

See: [red_team_review_loop.mmd](../../resources/diagrams/red_team_review_loop.mmd)
