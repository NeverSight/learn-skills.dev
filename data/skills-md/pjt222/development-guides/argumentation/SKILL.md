---
name: argumentation
description: >
  Construct well-structured arguments using the hypothesis-argument-example
  triad. Covers formulating falsifiable hypotheses, building logical arguments
  (deductive, inductive, analogical, evidential), providing concrete examples,
  and steelmanning counterarguments. Use when writing or reviewing PR descriptions
  that propose technical changes, justifying design decisions in ADRs, constructing
  substantive code review feedback, or building a research argument or technical
  proposal.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: general
  complexity: intermediate
  language: multi
  tags: argumentation, reasoning, hypothesis, logic, rhetoric, critical-thinking
---

# Construct Arguments

Build rigorous arguments from hypothesis through reasoning to concrete evidence. Every persuasive technical claim follows the same triad: a clear hypothesis states *what* you believe, an argument explains *why* it holds, and examples prove *that* it holds. This skill teaches you to apply that structure to code reviews, design decisions, research writing, and any context where claims need justification.

## When to Use

- Writing or reviewing a PR description that proposes a technical change
- Justifying a design decision in an ADR (Architecture Decision Record)
- Constructing feedback in a code review that goes beyond "I don't like this"
- Writing a research argument or technical proposal
- Challenging or defending an approach in a technical discussion

## Inputs

- **Required**: A claim or position that needs justification
- **Required**: Context (code review, design decision, research, documentation)
- **Optional**: Audience (peer developers, reviewers, stakeholders, researchers)
- **Optional**: Counterarguments or alternative positions to address
- **Optional**: Evidence or data available to support the claim

## Procedure

### Step 1: Formulate the Hypothesis

State your claim as a clear, falsifiable hypothesis. A hypothesis is not an opinion or a preference -- it is a specific assertion that can be tested against evidence.

1. Write the claim in one sentence
2. Apply the falsifiability test: can someone prove this wrong with evidence?
3. Scope it narrowly: constrain to a specific context, codebase, or domain
4. Distinguish from opinions by checking for testable criteria

**Falsifiable vs. unfalsifiable:**

| Unfalsifiable (opinion)              | Falsifiable (hypothesis)                                       |
|--------------------------------------|----------------------------------------------------------------|
| "This code is bad"                   | "This function has O(n^2) complexity where O(n) is achievable" |
| "We should use TypeScript"           | "TypeScript's type system will catch the class of null-reference bugs that caused 4 of our last 6 production incidents" |
| "The API design is cleaner"          | "Replacing the 5 endpoint variants with a single parameterized endpoint reduces the public API surface by 60%" |
| "This research approach is better"   | "Method A achieves higher precision than Method B on dataset X at the 95% confidence level" |

**Expected:** A one-sentence hypothesis that is specific, scoped, and falsifiable. Someone reading it can immediately imagine what evidence would confirm or refute it.

**On failure:** If the hypothesis feels vague, apply the "how would I disprove this?" test. If you cannot imagine counter-evidence, the claim is an opinion, not a hypothesis. Narrow the scope or add measurable criteria until it becomes testable.

### Step 2: Identify the Argument Type

Select the logical structure that best supports your hypothesis. Different claims call for different reasoning strategies.

1. Review the four argument types:

| Type        | Structure                                  | Best for                          |
|-------------|--------------------------------------------|-----------------------------------|
| Deductive   | If A then B; A is true; therefore B        | Formal proofs, type safety claims |
| Inductive   | Observed pattern across N cases; therefore likely in general | Performance data, test results    |
| Analogical  | X is similar to Y in relevant ways; Y has property P; therefore X likely has P | Design decisions, technology choices |
| Evidential  | Evidence E is more likely under hypothesis H1 than H2; therefore H1 is supported | Research findings, A/B test results |

2. Match your hypothesis to the strongest argument type:
   - Claiming something *must* be true? Use **deductive**
   - Claiming something *tends* to be true based on observations? Use **inductive**
   - Claiming something *will likely work* based on similar prior cases? Use **analogical**
   - Claiming one explanation *fits the data better* than alternatives? Use **evidential**

3. Consider combining types for stronger arguments (e.g., analogical reasoning backed by inductive evidence)

**Expected:** A chosen argument type (or combination) with a clear rationale for why it fits the hypothesis.

**On failure:** If no single type fits cleanly, the hypothesis may need splitting into sub-claims. Break it into parts that each have a natural argument structure.

### Step 3: Construct the Argument

Build the logical chain that connects your hypothesis to its justification.

1. State the premises (the facts or assumptions you start from)
2. Show the logical connection (how the premises lead to the conclusion)
3. Steelman the strongest counterargument: state the best opposing case *before* refuting it
4. Address the counterargument directly with evidence or reasoning

**Worked example -- Code Review (deductive + inductive):**

> **Hypothesis**: "Extracting the validation logic into a shared module will reduce bug duplication across the three API handlers."
>
> **Premises**:
> - The three handlers (`createUser`, `updateUser`, `deleteUser`) each implement the same input validation with slight variations (observed in `src/handlers/`)
> - In the last 6 months, 3 of 5 validation bugs were fixed in one handler but not propagated to the others (see issues #42, #57, #61)
> - Shared modules enforce a single source of truth for logic (deductive: if one implementation, then one place to fix)
>
> **Logical chain**: Because the three handlers duplicate the same validation (premise 1), bugs fixed in one are missed in others (premise 2, inductive from 3/5 cases). A shared module means fixes apply once to all callers (deductive from shared-module semantics). Therefore, extraction will reduce bug duplication.
>
> **Counterargument (steelmanned)**: "Shared modules introduce coupling -- a change to validation for one handler could break the others."
>
> **Rebuttal**: The handlers already share identical validation *intent*; the coupling is implicit and harder to maintain. Making it explicit via a shared module with parameterized options (e.g., `validate(input, { requireEmail: true })`) makes the coupling visible and testable. The current implicit duplication is riskier because it hides the dependency.

**Worked example -- Research (evidential):**

> **Hypothesis**: "Pre-training on domain-specific corpora improves downstream task performance more than increasing general corpus size for biomedical NER."
>
> **Premises**:
> - BioBERT pre-trained on PubMed (4.5B words) outperforms BERT-Large pre-trained on general English (16B words) on 6/6 biomedical NER benchmarks (Lee et al., 2020)
> - SciBERT pre-trained on Semantic Scholar (3.1B words) outperforms BERT-Base on SciERC and JNLPBA despite a smaller pre-training corpus
> - General-domain scaling (BERT-Base to BERT-Large, 3x parameters) yields smaller gains on biomedical NER than domain adaptation (BERT-Base to BioBERT, same parameters)
>
> **Logical chain**: The evidence consistently shows that domain corpus selection outweighs corpus scale for biomedical NER (evidential: these results are more likely if domain specificity matters more than scale). Three independent comparisons point the same direction, strengthening the inductive case.
>
> **Counterargument (steelmanned)**: "These results may not generalize beyond biomedical NER -- biomedicine has unusually specialized vocabulary that inflates the domain-adaptation advantage."
>
> **Rebuttal**: Valid limitation. The hypothesis is scoped to biomedical NER specifically. However, similar domain-adaptation gains appear in legal NLP (Legal-BERT) and financial NLP (FinBERT), suggesting the pattern may generalize to other specialized domains, though that is a separate claim requiring its own evidence.

**Expected:** A complete argument chain with premises, logical connection, a steelmanned counterargument, and a rebuttal. The reader can follow the reasoning step by step.

**On failure:** If the argument feels weak, check the premises. Weak arguments usually stem from unsupported premises, not faulty logic. Find evidence for each premise or acknowledge it as an assumption. If the counterargument is stronger than the rebuttal, the hypothesis may need revision.

### Step 4: Provide Concrete Examples

Support the argument with independently verifiable evidence. Examples are not illustrations -- they are the empirical foundation that makes the argument testable.

1. Provide at least one **positive example** that confirms the hypothesis
2. Provide at least one **edge case or boundary example** that tests limits
3. Ensure each example is **independently verifiable**: another person can reproduce or check it without relying on your interpretation
4. For code claims, reference specific files, line numbers, or commits
5. For research claims, cite specific papers, datasets, or experimental results

**Example selection criteria:**

| Criterion              | Good example                                        | Bad example                              |
|------------------------|-----------------------------------------------------|------------------------------------------|
| Independently verifiable | "Issue #42 shows the bug was fixed in handler A but not B" | "We've seen this kind of bug before"     |
| Specific               | "`createUser` at line 47 re-implements the same regex as `updateUser` at line 23" | "There's duplication in the codebase"    |
| Representative         | "3 of 5 validation bugs in the last 6 months followed this pattern" | "I once saw a bug like this"             |
| Includes edge cases    | "This pattern holds for string inputs but not for file upload validation, which has handler-specific constraints" | (no limitations mentioned)               |

**Expected:** Concrete examples that a reader can verify independently. At least one positive and one edge case. Each references a specific artifact (file, line, issue, paper, dataset).

**On failure:** If examples are hard to find, the hypothesis may be too broad or not grounded in observable reality. Narrow the scope to what you can actually point to. Absence of examples is a signal, not a gap to paper over with vague references.

### Step 5: Assemble the Complete Argument

Combine hypothesis, argument, and examples into the appropriate format for the context.

1. **For code reviews** -- structure the comment as:
   ```
   [S] <one-line summary of the suggestion>

   **Hypothesis**: <what you believe should change and why>

   **Argument**: <the logical case, with premises>

   **Evidence**: <specific files, lines, issues, or metrics>

   **Suggestion**: <concrete code change or approach>
   ```

2. **For PR descriptions** -- structure the body as:
   ```markdown
   ## Why

   <Hypothesis: what problem this solves and the specific improvement claim>

   ## Approach

   <Argument: why this approach was chosen over alternatives>

   ## Evidence

   <Examples: benchmarks, bug references, before/after comparisons>
   ```

3. **For ADRs (Architecture Decision Records)** -- use the standard ADR format with the triad mapped to Context (hypothesis), Decision (argument), and Consequences (examples/evidence of expected outcomes)

4. **For research writing** -- map to the standard structure: Introduction states the hypothesis, Methods/Results provide argument and examples, Discussion addresses counterarguments

5. Review the assembled argument for:
   - Logical gaps (does the conclusion actually follow from the premises?)
   - Missing evidence (are there unsupported premises?)
   - Unaddressed counterarguments (is the strongest objection answered?)
   - Scope creep (does the argument stay within the hypothesis bounds?)

**Expected:** A complete, formatted argument appropriate for its context. The reader can evaluate the hypothesis, follow the reasoning, check the evidence, and consider counterarguments -- all in one coherent structure.

**On failure:** If the assembled argument feels disjointed, the hypothesis may be too broad. Split it into focused sub-arguments, each with its own hypothesis-argument-example triad. Two tight arguments are stronger than one sprawling one.

## Validation

- [ ] Hypothesis is falsifiable (someone could disprove it with evidence)
- [ ] Hypothesis is scoped to a specific context, not a universal claim
- [ ] Argument type is identified and appropriate for the claim
- [ ] Premises are stated explicitly, not assumed as shared knowledge
- [ ] Logical chain connects premises to conclusion without gaps
- [ ] Strongest counterargument is steelmanned and addressed
- [ ] At least one positive example supports the hypothesis
- [ ] At least one edge case or limitation is acknowledged
- [ ] All examples are independently verifiable (references provided)
- [ ] Output format matches the context (code review, PR, ADR, research)
- [ ] No logical fallacies (appeal to authority, false dichotomy, strawman)

## Common Pitfalls

- **Stating opinions as hypotheses**: "This code is messy" is a preference, not a hypothesis. Rewrite as a testable claim: "This module has 4 responsibilities that should be separated per the single-responsibility principle, as evidenced by its 6 public methods spanning 3 unrelated domains."
- **Skipping the counterargument**: Unaddressed objections weaken the argument even if the reader never voices them. Always steelman -- state the strongest opposing case in its best form before rebutting it.
- **Vague examples**: "We've seen this pattern before" is not evidence. Point to specific issues, commits, lines, papers, or datasets. If you cannot find a concrete example, your hypothesis may not be well-grounded.
- **Argument from authority**: "The senior engineer said so" or "Google does it this way" is not a logical argument. Authority can *motivate* investigation, but the argument must stand on its own evidence and reasoning.
- **Scope creep in conclusions**: Drawing conclusions broader than what the evidence supports. If your examples cover 3 API handlers, don't conclude about the entire codebase. Match conclusion scope to evidence scope.
- **Conflating argument types**: Using inductive language ("tends to") for deductive claims ("must be") or vice versa. Be precise about the strength of your conclusion -- deductive arguments give certainty, inductive arguments give probability.

## Related Skills

- `review-pull-request` -- applying argumentation to structured code review feedback
- `review-research` -- constructing evidence-based arguments in research contexts
- `review-software-architecture` -- justifying architectural decisions with the hypothesis-argument-example triad
- `create-skill` -- skills themselves are structured arguments for how to accomplish a task
- `write-claude-md` -- documenting conventions and decisions that benefit from clear justification
