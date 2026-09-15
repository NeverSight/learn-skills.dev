---
name: audit-code-complexity
description: Find needless code complexity and suggest simpler designs that preserve behavior.
---

# Audit code complexity

Find what is materially harder to understand, change, or verify than the problem requires.

## Scope

Choose from the user's wording:

- **Current-state.** Audit the target as it exists, regardless of when complexity was introduced.
- **Change-scoped.** Report only complexity introduced or materially worsened by the named changes. Inspect surrounding code only for context.

Do not infer change scope merely because a repository has changes. If both modes are requested, report them separately. Ask only when genuine ambiguity would materially change the audit.

## Method

Inspect the target, repository instructions, callers, tests, configuration, and only the requirements or docs needed to understand behavior and constraints.

Look for:

- unjustified indirection, wrappers, genericity, extension points, dependencies, or infrastructure
- tangled control flow, flag combinations, implicit state, invalid states, or multiple sources of truth
- repeated transformations, leaky types, wide APIs, hidden side effects, or unclear ownership
- duplicated policy, scattered edits for one change, or modules with unrelated responsibilities
- misleading names, distant cause and effect, broad mutation, dense expressions, or clever code
- speculative guards, fallbacks, compatibility paths, or dead machinery
- test harnesses, fixtures, mocks, or setup that make production behavior harder to understand or change

Smell names are optional vocabulary for explaining a concrete mechanism, not a checklist to exhaust or evidence of a violation. Use labels such as Feature Envy, Data Clumps, Shotgun Surgery, or Speculative Generality only when they make a finding clearer.

Include a finding only when:

1. The code creates a concrete maintenance, comprehension, correctness, or operational cost.
2. The claim is supported by code, usage, tests, or requirements.
3. A simpler alternative is concrete and preserves required behavior and contracts.
4. The benefit outweighs migration and regression risk.

Line count, nesting, complexity metrics, and unfamiliarity are clues, not findings.

Before recommending removal of a wrapper, read its callers, including tests. Check what it handles that callers would otherwise need to handle themselves. Keep it when it owns useful behavior or protects a required contract. If it only forwards a call, consider putting that call in the appropriate existing module. File size and caller count alone do not decide this.

When you find a problem, check whether the same problem occurs elsewhere in the code you were asked to audit. Report affected locations together when the same fix applies; keep cases separate when they must preserve different behavior. If you checked only part of the target, say so instead of presenting examples as a complete list.

## Test boundary

Inspect tests when they establish a contract, explain intended behavior, or provide evidence for a complexity finding.

Report test-related complexity only when the test architecture creates or conceals a concrete cost. Examples include shared setup with hidden state, helper layers that obscure behavior, duplicated fixtures that encode policy in several places, test-only seams that force production indirection, or mocks that hide unclear ownership.

Do not turn this into a general review of test value, coverage, snapshots, assertions, or missing cases. When tests are the main subject, use `test-quality-audit` instead.

## Output

Lead with a verdict, then prioritized findings. For each finding include:

- impact and confidence
- exact location and evidence
- concrete cost
- simpler alternative
- behavior or contracts that must remain unchanged

Add justified complexity, simplification order, and validation only when useful. If no material findings exist, say so directly.

## Rules

- Audit only; do not edit unless explicitly asked.
- Prefer local simplification over rewrites.
- Do not create an abstraction solely to remove similar-looking code; require a shared concept.
- Preserve domain distinctions, data semantics, source of truth, identity, routing, validation, security, accessibility, and compatibility.
- Skip formatter, linter, naming, and style nits unless they materially obscure behavior.
- Do not present an ordinary correctness bug as a complexity or simplification finding. Report bugs, security, or performance issues only when caused or concealed by the complexity under review, and label them separately from simplification findings.
