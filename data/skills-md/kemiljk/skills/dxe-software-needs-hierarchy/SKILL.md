---
name: dxe-software-needs-hierarchy
description: "Evaluate software through a Maslow-inspired hierarchy of user needs and prioritise improvements from basic function and trust through belonging, competence, and growth. Use when a product needs a needs-based quality review or competing improvements need ordering."
license: MIT
---

# Software Needs Hierarchy

Help people do the essential task, trust the result, feel accommodated, develop confidence, and achieve more of what matters to them. Use these needs to decide which software improvements earn attention.

This is an editorial translation of Maslow's human motivation framework into software decisions, not a validated theory of software quality. The needs belong to people using software, not to the software itself. Read [source and translation notes](references/source-and-translation.md) when explaining the origin or limits. The working method below is self-contained.

## Establish the person and task

Infer the intended consumer, desired outcome, context, and constraints from the request and available evidence. For an API or developer tool, consider the developer's task and the consequences for their users. Define a representative journey and what successful completion means. Ask only when missing information would materially change the decision.

Inspect the named flow, code, design, or proposal at the requested depth. A review produces recommendations; an improvement request authorises scoped changes. A narrow request should stay narrow. Use the hierarchy to explain the relevant dependency, not to mandate a whole-product audit.

## Translate the five needs

| Human need | Software translation | User's question | Evidence to seek |
| --- | --- | --- | --- |
| Physiological | Basic function and access | Can I do the essential thing? | A realistic task completes with the necessary inputs, usable output, and relevant access methods. |
| Safety | Safety and trust | Can I depend on this without losing control or work? | State is accurate, work survives relevant failures, and consequential actions respect permissions and support recovery. |
| Love and belonging | Fit and belonging | Does this accommodate me and the way I work? | Language, defaults, conventions, and interoperability fit the audience and context without forced social participation. |
| Esteem | Competence and confidence | Can I understand, act, and become capable? | People can predict consequences, recognise progress, correct mistakes, and use efficient paths as experience grows. |
| Self-actualisation | Growth and expression | Can I achieve something meaningful on my own terms? | The product supports the user's creative, learning, or professional goals through useful freedom and control. |

### 1. Basic function and access

Start with the outcome the product promises. Loading a screen or returning a successful status code is insufficient if the person cannot finish the task or use the result. Examine correctness, availability, essential content, discoverable actions, and responsiveness in the actual context. Accessibility is part of completing the task from the outset; it is not an optional upper tier.

**Decision:** fix a blocked essential path before adding an enhancement that depends on it. Use an appropriate task or runtime check; a polished screenshot does not demonstrate function.

### 2. Safety and trust

Look for risks to work, privacy, control, and confidence in the result. Connect feedback to actual state. Consider persistence, permissions, understandable costs, destructive actions, interruptions, retries, and recovery where they matter to this task. Familiar appearance cannot establish security or reliability.

**Decision:** prioritise a credible risk of serious harm even if another need appears lower in the table. Verification should exercise the relevant boundary or failure, not merely inspect reassuring copy.

### 3. Fit and belonging

Make the intended audience feel accommodated through relevant terminology, respectful copy, useful defaults, platform conventions, and compatibility with their existing work. Consider locale, abilities, expertise, and constraints rather than assuming a single average user. Collaboration and community belong here only when they support a real task. A private tool can fulfil this need without profiles, feeds, or social features.

**Decision:** remove a mismatch that excludes or burdens the intended audience. If exclusion blocks access, treat its impact as foundational too. Preserve useful density and product identity instead of imposing a universal visual style.

### 4. Competence and confidence

Support understanding and agency: clear action labels, visible system status, useful explanations, recoverable mistakes, and discoverable expert paths. Judge efficiency over repeated use as well as first use. Help people learn the task instead of making them dependent on opaque automation.

**Decision:** favour a change that gives the person useful control or reduces recurring effort. Streaks, badges, and praise are not substitutes for capability; confidence must correspond to actual behaviour.

### 5. Growth and expression

Ask what the user can now create, understand, decide, or accomplish. Where appropriate, support exploration, flexible workflows, adaptation, interoperability, and ownership of output. For a utility, success may mean finishing quickly and returning to life outside the product. Extra engagement is not the goal.

**Decision:** invest in possibilities tied to the user's purpose. A creative tool's expressive capability may be its core function, so do not postpone it as an optional luxury. Delight and visual craft can support any layer; neither automatically represents this one.

## Prioritise without turning the hierarchy into a gate

Use the lowest consequential unmet need as a starting point, then account for impact, frequency, affected people, confidence in the evidence, dependencies, and effort. Needs overlap, and their importance varies by person and task. Do not require complete perfection in one layer before improving another, average away a blocked group, or assign a single maturity level to a whole product.

Compare competing changes through their specific effects. A save failure usually outweighs celebratory animation; an inaccessible control blocks function even in an otherwise reliable product; clear labels may improve both completion and confidence. These are hypothetical illustrations, not findings about the current product.

When the evidence is incomplete, recommend the smallest check that could change the priority. Mark each relevant need as **supported, impaired, or unknown**, tied to the examined journey. Unknown does not mean failed. Do not manufacture a finding for each layer or use numerical scores without an agreed rubric.

## Produce an actionable result

For material findings, connect **person and task → evidence → unmet need → consequence → smallest effective change → acceptance check**. Keep facts, hypotheses, and proposed design decisions distinct. Every reported bug needs a credible consumer use case, prerequisites and reproduction steps, expected and actual behaviour, and impact. Claim reproduction only after performing it; omit theoretical concerns without a supported use case.

Match checks to claims: runtime or input sequences for operation, failure simulation for recovery, rendered inspection for hierarchy, and user evidence for perceived belonging or confidence. A screenshot cannot prove persistence, security, accessibility, or emotional response.

Deliver the requested proposal, review, or implementation with the priority and its reason, relevant strengths, checks performed, and consequential unknowns. For implementation, revisit the affected journey and any lower-layer promise the change could compromise. Stop when the scoped outcome is supported; this lens does not authorise unrelated features, publication, or deployment.
