---
name: real-content-design
description: "Shape interface structure using representative content before layout decisions settle. Use when placeholders, uniform examples, incomplete records, or mixed content types may hide problems in hierarchy, comparison, navigation, or component design."
license: MIT
---

# Real Content Design

Let the material people actually need to read, compare, or act on shape the interface. This is a design method, not just a long-string stress test.

## Establish the content and task

Inspect the named surface, its content model, and available examples. Identify the audience's task: scan, compare, choose, understand, edit, or find something. Record which fields are essential to that task and which are optional, derived, unavailable, or conditional.

Use supplied or authorised project material first. When examples are insufficient, create clearly labelled synthetic fixtures that reproduce useful structural variation. Do not invent ownership, testimonials, results, or other factual claims for production copy. Keep fixtures separate from publishable content and avoid writing them into live records.

Ask for missing facts only when they prevent a meaningful decision. Otherwise work with explicit unknowns and propose the content requirement. A request to explore layouts authorises exploration; production content or code changes require the corresponding scope.

## Choose representative variation

Select examples that challenge a real decision rather than exhaustively combining every field:

| Variation | Design question |
| --- | --- |
| Uneven titles and summaries | Does hierarchy survive different amounts of explanation? |
| Missing images or optional fields | Is the remaining record understandable without fake filler? |
| Mixed status, type, or ownership | Can people distinguish what they are comparing? |
| Similar names or overlapping descriptions | Is enough distinguishing context visible? |
| Complex or consequential information | Does simplification remove something needed to decide? |
| Few, many, or no records | Does organisation still fit the task, and is the next action clear? |

Include long text, locale, units, or writing-direction variation when the intended audience and product support them. Avoid using arbitrary extremes as a reason to redesign an otherwise sound pattern. State which examples are real, synthetic, or still missing.

## Design from the material

Arrange the representative content in the existing system before inventing a new structure. Inspect what readers need together, which distinctions deserve emphasis, and what information is required at each decision.

Do not force equal copy lengths to rescue a rigid card grid. Try content-driven height, grouping, a list, or a different summary structure when the task supports it. Conversely, consistent comparison may need stable columns and explicit missing values. Choose based on use, not an automatic preference for fluid layouts.

Treat absence deliberately. Omit optional decoration, distinguish unavailable from not applicable where meaningful, and explain required next steps. Missing content, loading, and failure are different states; do not present all three as an empty placeholder.

Check truncation against the task. A detail view can justify a concise preview if the identifying information remains visible and access is clear. A tooltip does not adequately restore essential content for every input method. Keep headings, actions, and reading order coherent as the content changes.

## Turn discoveries into bounded changes

Distinguish three remedies: improve the content itself, change the content model, or change the presentation. A new layout cannot supply missing project ownership; a better summary cannot fix a component that clips supported text.

For example, a portfolio containing a shipped product, a team contribution, and an unfinished experiment needs honest status and contribution context. Unequal screenshots and summary lengths should inform the layout. Do not manufacture identical case studies or claim the experiment shipped. This is a hypothetical application.

For implementation work, place representative fixtures in the project's existing preview or development mechanism when useful. Avoid adding a new fixture framework for a small design decision. Check changed shared components in their relevant other uses.

## Verify and deliver

Revisit the task with the chosen content at relevant layout sizes and inputs. Inspect actual rendering for wrapping, reading order, image treatment, and discoverability. Exercise behaviour when the change affects it. A fixture demonstrates a scenario, not how common it is; a screenshot does not prove accessibility or task comprehension.

Report the sample, design decisions it changed, any factual content dependencies, and checks performed. Keep hypotheses separate from findings. For a bug, state the concrete consumer use case, prerequisites and reproduction steps, expected and actual behaviour, and impact; do not claim reproduction from imagined content alone.

Deliver the requested exploration, review, or scoped implementation. Preserve representative examples when they materially help future work, but do not replace real product content with demonstration data.
