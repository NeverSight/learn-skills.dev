---
name: research
description: Research evidence-backed questions from authoritative sources. Use when a decision, documentation, API, or examined-system source-code fact needs a cited finding.
license: MIT
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Research

A **finding** is one Markdown artifact that answers a bounded question with claim-level evidence. The source that owns a claim is authoritative: official vendor documentation, specifications, source code, and the API or reference material of the system being examined. Use secondary material to discover sources, then cite the authoritative source in the finding.

## Pick a role

- **Research lead** — a direct request, unless its dispatch explicitly says `Role: research worker`. Establish the brief and dispatch one background research worker. Keep ownership of any user-facing or tracker action.
- **Research worker** — a dispatch marked `Role: research worker`. Investigate and write the finding directly. Return the artifact and evidence-backed summary to the lead; do not dispatch another researcher or update a Wayfinder ticket.

## Research lead

1. **Bound the brief.** State the question, scope, source constraints, repository root, and any existing output location. For a Wayfinder ticket, include the map and ticket links; the session that claimed the ticket remains its lifecycle owner.

   **Complete when:** the worker can answer one checkable question without choosing its own scope or tracker actions.

2. **Choose the artifact location.** Inspect the repository for an existing research-note convention and use it. If none exists, use `docs/research/<topic-slug>.md`, avoiding a collision with an existing note.

   **Complete when:** the worker receives one exact, writable artifact path.

3. **Dispatch the worker.** Send the brief, exact path, and `Role: research worker`. Ask it to return the path, a concise answer, sources for every material claim, and any uncertainty or evidence conflict.

   **Complete when:** one background worker owns the investigation and has the complete brief.

## Research worker

1. **Trace the evidence.** Investigate the brief. Follow every material factual claim through to the authoritative source that owns it; read enough surrounding context to preserve qualifications, versions, and limits.

   **Complete when:** every material conclusion is supported by an authoritative, directly linked source or is marked as an inference or unresolved question.

2. **Write the finding.** Create the assigned Markdown file with these sections:

   ```markdown
   # <Question>

   ## Answer
   <Concise, evidence-backed answer.>

   ## Evidence
   - <Claim> — [Source title](URL) (<relevant version, section, or location>)

   ## Caveats and open questions
   <Uncertainty, source conflicts, assumptions, or an explicit “None found”.>
   ```

   **Complete when:** the file exists at the assigned path, every material claim in **Answer** has an adjacent or clearly corresponding entry in **Evidence**, and caveats distinguish source-backed facts from inference.

3. **Return the result.** Return the exact artifact path, the concise answer, source links, and caveats to the lead. For Wayfinder, the lead records the resolution comment, closes the ticket, and indexes the map.

   **Complete when:** the lead has the durable finding and all information needed for its own lifecycle action.
