---
name: truth
description: >
  Maximum epistemological rigor for any input — questions, claims, draft text, arguments,
  decisions, tweets, anything. Always runs the full truth-seeking pipeline: strips prestige,
  malformed framing, false confidence, and heuristic overreach. This skill exists to push
  reasoning deeper than the agent would go by default. Use for anything where you want
  honesty over agreeableness.
  Triggers on /truth, "find the truth", "what's really true", "epistemological analysis",
  "truth-seek this", "check this", "is this true", "sanity check".
argument-hint: <question, claim, draft text, or anything to truth-check>
license: MIT
disable-model-invocation: false
---

# TRUTH-SEEKING PROTOCOL

The user invoked /truth. This activates the full epistemological reasoning pipeline on whatever
they provided — a question, a claim, a draft tweet, an argument, a decision, anything. Run
every phase. Skip nothing. If your analysis feels easy, you haven't gone deep enough.

**HARD RULE 1: YOU DON'T KNOW.** Your default state is not-knowing — not at the start, but
throughout. Every claim, every phase, every iteration: recalibrate yourself to not-knowing.
You are not retrieving an answer — you are building one from observations, questions, and
evidence. Your observations and exploration ARE the path to the answer. There is no shortcut.
The moment you feel confident, recalibrate yourself to not-knowing: "Do I actually know this,
or did I just stop questioning it?" The skill works when you stay in not-knowing long enough
for the evidence to speak. It fails when you exit too early into false certainty.
**This applies to severity and impact too.** Not-knowing means you don't pre-decide whether
a finding is serious or minor. You don't soften findings to be agreeable. If your evidence
says something is a real problem, call it a real problem — don't wrap it in "no showstopper"
or "will functionally work" to cushion the blow. Minimizing your own findings is just false
certainty in the other direction. Let the evidence set the severity, not your comfort level.

**HARD RULE 2: YOUR FIRST OUTPUT IS QUESTIONS, NOT ANALYSIS.** Before any analysis, generate
at least 10 clarification questions and present them to the user. Stop. Wait for answers.
Then analyze. Every minute spent analyzing under wrong assumptions is wasted. See Phase 0.3.

**HARD RULE 3: FOLLOW THE OUTPUT FORMAT EXACTLY.** The structured output in Phase 6.3 is not
a suggestion — it is mandatory. Every section must appear: Claim Inventory (10+), Observations,
Gotchas (5+), Cross-References, Question Assessment, Key Finding, Evidence, Confidence, What I
Don't Know, New Questions. These sections exist because they force thoroughness — skipping any
one of them is how findings get missed or minimized. A narrative essay is not a substitute.
See Phase 6.3.

**HARD RULE 4: YOUR OBSERVATIONS AND CLAIMS ARE HIGH VALUE — RE-READ THEM.** After writing
your Observations and Claim Inventory sections, stop and re-read them as a whole before
continuing. These lists contain your raw signal. Patterns, contradictions, and insights emerge
from reading them together that you will not see while writing them one by one. The answer is
often already in your observations — you just haven't looked at them yet. Do not rush past
your own work.

---

## PHASE -1: ACTIVATE DEEP REASONING ENGINE

**You MUST follow ALL of these rules. They are the engine that makes the rest of this skill
work rather than decoration.**

### -1.1 Extended Thinking is Mandatory

Use your extended thinking to its absolute maximum. Think for as long as the problem demands
before outputting a single word. A truth-seeking checklist run quickly is worse than no
checklist — it gives false confidence that scrutiny happened when it didn't.

### -1.2 Decompose Before Concluding

Break the problem into atomic sub-questions. Generate at least 3 distinct framings of the
question before settling on one. The framing that survives the harshest criticism of its
assumptions is the right one.

### -1.3 Adversarial Self-Challenge

Before presenting any conclusion, spend significant effort trying to prove yourself wrong.
Steelman the opposing position, then try to destroy your own. For every answer you're about
to give, ask: "Did I actually think about this, or did I retrieve it?" If you retrieved it,
verify the retrieval applies HERE. Audit your exemptions — when your analysis produces a
reason why something doesn't apply here, that exemption needs the hardest scrutiny.
Exemptions are where motivated reasoning hides.

### -1.4 Surface Every Detail

Write down every observation, however small. Variable names, word choices, structural
patterns, numbers, things that seem "off." Don't filter for relevance prematurely — details
that seem trivial alone often combine into insights when read together. The observation you
almost didn't write down is often the one that matters.

### -1.5 Verification Over Theorizing

- If something can be checked, check it. Don't theorize about what's probably true.
- **Your training data is not a measurement instrument.** Verify claims rather than trusting
  memory. Recalling from training data feels like knowing. It isn't.
- **Hedging triggers verification.** Saying "I believe X but haven't verified" is the move
  that triggers checking. The confident wrong answer kills the verification impulse.
- **Verify by dependency, not by doubt.** Check the claim your conclusion most depends on
  first — not the one you're least sure about.

### -1.6 Single-Pass Incompleteness

You will not follow all of these instructions correctly in one pass. After drafting your
analysis, audit and verify it in 2-3 passes:

1. **Audit** — re-read every claim. Did you verify it or recall it? If recalled, hedge it.
2. **Verify** — for load-bearing claims, attempt real verification. Search for counterexamples,
   gotchas, documented behavior changes.
3. **Check phases** — did you actually run each phase or skip to answering?

Stop when corrections between passes get small.

---

## PHASE 0: UNDERSTAND WHAT YOU'RE BEING ASKED

### 0.1 Literal Reading

Read the question three times. What is literally being asked? What is implied but unstated?
What assumptions are embedded?

### 0.2 Question Well-Formedness Check (MANDATORY)

Most wrong answers are correct answers to malformed questions. Run EVERY check. If ANY fires,
reformulate before proceeding.

| Check | Test | If fired |
|---|---|---|
| **A: False Dichotomy** | Can you construct a coherent position between the options? | Identify the continuum, restate as "where on this spectrum, under what conditions?" |
| **B: Context-Dependent** | Can you name two contexts with different correct answers? | Identify contextual variables, state conditional answers |
| **C: Value vs Empirical** | Would two people with ALL the same facts still disagree? | Separate the IS from the SHOULD BE. Name the values in conflict |
| **D: Verbal Dispute** | Taboo the key term — do they still disagree? | State each side's implicit definition, show disagreement is linguistic |
| **E: Loaded Framing** | Restate with neutral language — does it change reasonable answers? | Strip loaded terms, note how framing was biasing |
| **F: Presupposition Failure** | Does the question assume something unverified? | Flag and verify the presupposition before proceeding |

### 0.3 Clarification Questions (MANDATORY FIRST OUTPUT)

**Your first response must be questions, not analysis.** Generate at least 10 questions you'd
need answered to be confident. Output them. Stop. Wait for answers. Then analyze.

Star (*) the 1-3 most critical ones — those where a different answer would flip your analysis.
Tell the user they can answer as many or as few as they want.

```
Before I analyze, a few questions that would change my answer:

1. *[blocking question]
2. *[blocking question]
3. [question]
...
10. [question]

Answer what you can — I'll state assumptions for the rest and proceed.
```

Do NOT generate the full analysis alongside the questions.

### 0.4 Claim Inventory

List **at least 10 factual claims** — stated, embedded, and implied by multiple lines together.
Include claims that feel like background facts. The act of enumerating forces you to surface
assumptions you'd otherwise skip. If you struggle to reach 10, you haven't looked hard enough.
Star (*) the load-bearing ones. Verify those before proceeding.

---

## PHASE 1: INTELLECTUAL PRESTIGE AUDIT

The branding of an idea is not evidence for its correctness. The smarter something sounds,
the harder you check it. The more profound it feels, the more likely the feeling is doing the
persuasion, not the logic. "Everyone knows X" gets high scrutiny — consensus isn't proof.

For every framework, principle, or methodology you're about to apply:
- Would I find this convincing without the prestige? Strip the name, the citations.
- Who benefits from me accepting this? (Cui bono applied to ideas)
- Is this being used as a credential or as a tool?

**Named framework traps** (verify each applies HERE, not in general):

| Framework | The trap |
|---|---|
| Logical fallacy labels | Naming a fallacy is not a refutation. Appeal to authority is sometimes rational. |
| "First principles" | Often invoked to sound rigorous while ignoring that cached knowledge is legitimate. |
| "Scientific consensus" | Current best model, not final truth. Consensus has been wrong. Weight it, don't worship it. |
| "Data-driven" | Data requires interpretation. Same dataset supports different conclusions. |
| "Best practice" | Best for whom? In what context? Usually means "what most people do." |
| "Peer-reviewed" | Filters out the worst work. Doesn't guarantee correctness (replication crisis). |

---

## PHASE 2: EVIDENCE EVALUATION

### 2.1 Source Incentive Analysis (MANDATORY for every claim)

| Question | What it reveals |
|---|---|
| Who made this claim? | Source identity |
| What do they gain if I believe it? | Incentive alignment |
| Would they tell me if they were wrong? | Self-correction capacity |

**Incentive tiers:** Aligned (profits from accuracy) → weight high. Neutral (no stake) →
medium. Misaligned (profits from your belief) → low for evaluative claims. Adversarial
(optimizing for your belief) → near zero.

### 2.2 Source Independence

Five sources saying the same thing is NOT five data points if they're all downstream of one
original. Trace claims to their origin. If you remove the original, does the "consensus"
collapse?

### 2.3 Evidence Quality

When claims conflict, higher-tier evidence wins: Direct measurement > Reproducible experiments
> Expert testimony with skin in the game > Observational data > Expert opinion > Anecdote >
Hearsay.

### 2.4 Absence of Evidence

What evidence SHOULD exist if true? Does it? What evidence SHOULD exist if false? Does it?
"No studies show X is harmful" can mean "X is safe" OR "nobody studied X." Radically different.

### 2.5 Symmetric Investigation (MANDATORY for comparisons)

When claiming A > B, verify you investigated both to the same depth. List the checks you ran
for each side. Asymmetric investigation masquerades as evidence.

---

## PHASE 3: REASONING HYGIENE

### 3.1 Heuristic Awareness

Every reasoning tool is a heuristic with false positive cases. For every tool you apply:
name it, state its assumption, identify when it fails, check if you're in the failure zone.

| Tool | When it fails |
|---|---|
| Analogy | Surface similarity hides structural difference |
| Induction | Small/biased sample, or fat-tailed domain |
| Deduction | Hidden premises, unstated assumptions |
| Occam's razor | Simpler explanation has less predictive power |
| Pattern matching | Novel situation, domain shift |

### 3.2 Effort Calibration

Match effort to stakes. High stakes/irreversible → full protocol. Low stakes/correctable →
cached knowledge + flagged uncertainty. Pattern-matching is legitimate when the domain is
stable and stakes are low. The failure is pattern-matching without realizing it in novel
or high-stakes situations.

Stop meta-reasoning (reasoning about reasoning) when the next level costs more than the
expected value of catching an error. Level 0: answer. Level 1: check your answer. Level 2:
check your checking. Level 3+: almost never worth it.

### 3.3 Motivated Exemption Detection

When your reasoning produces a convenient exemption — a reason why something doesn't apply
here — that's the highest-risk conclusion. Three tests:

1. **Directional motivation:** If following the rule were FREE, would you still claim the
   exemption? If compliance cost is the only reason, it's rationalization.
2. **Reversal:** If someone else presented this exemption, would you accept it?
3. **Escalation:** Is this your second or third justification after earlier ones failed?
   Increasing sophistication in justification is a red flag — motivated reasoning upgrades
   its armor rather than conceding.

### 3.4 Composite Implication Check

True facts arranged together can imply something false. After verifying individual claims,
state the conclusion a reader will draw from the text as a whole. Verify THAT independently.
If the composite implication is false but every individual claim is true, the problem is
arrangement.

### 3.5 Embedded Premise Extraction

"X because Y" has two claims. You scrutinize X (the conclusion). Y (the premise) rides
through unchecked. Extract every embedded premise and verify it. The premise that feels most
obviously true is the highest-risk.

---

## PHASE 4: DISAGREEMENT ANALYSIS

When encountering competing claims, classify the disagreement using Phase 0.2's checks:

| Type | Response |
|---|---|
| False dichotomy / Malformed | DISSOLVE — identify the continuum, refuse the binary |
| Context-dependent | MAP — state "X when A, Y when B" |
| Values conflict | SEPARATE — name the values, note empirical evidence can't resolve it |
| Verbal dispute | CLARIFY — define terms, show disagreement is linguistic |
| Genuinely contested | ACKNOWLEDGE — state known/unknown, current best estimate with confidence |

**Check the floor:** Before evaluating which side is stronger, ask: are the categories
themselves real? Do they carve reality at its joints? If the categories are wrong, both
positions fall — not because the arguments are weak, but because the framing is.

For any claim: find the most knowledgeable person who disagrees. State their argument at full
strength. If you can't find an expert skeptic, either the claim is solid or you haven't looked.

---

## PHASE 5: CONFIDENCE CALIBRATION

### 5.1 Confidence Ladder

| Level | Meaning | Language |
|---|---|---|
| **Certain** | Direct verification, multiple independent sources | State as fact |
| **High** | Strong evidence, no strong counter-evidence | "Evidence strongly supports X" |
| **Medium** | Evidence leans one way but has gaps | "X seems likely, but Y remains possible because..." |
| **Low** | Limited evidence, significant uncertainty | "My best guess is X, but low confidence because..." |
| **Unknown** | Evidence absent or contradictory | "I don't know. Here's what I'd need to find out." |

**Confidence is earned, not assumed.** Every unverified claim starts at UNKNOWN. Recalling
from training data earns at most LOW. For anything that changes between versions, contexts,
or implementations: UNKNOWN until checked. NEVER present Low/Medium conclusions with High
language. If you catch yourself saying "clearly" or "obviously" — check the ladder.

### 5.2 What Would Change My Mind?

For every conclusion: what evidence would make me revise this? Have I looked for it?
If you cannot name such evidence, you're rationalizing, not reasoning.

### 5.3 Claims Taken on Trust

List every claim you couldn't verify, accepted on source credibility, or "know" from memory.
These are your vulnerability points. Flag them.

---

## PHASE 6: SYNTHESIS AND OUTPUT

### 6.1 The Uncomfortable Truth Test

Before presenting your final answer: Is this what I genuinely believe, or what feels
agreeable? Am I softening a hard truth when one side is clearly stronger?

### 6.2 The Dissolution Report

If Phase 0 found the question was malformed: state what was asked, why it's malformed,
the reformulated question, and the answer to the reformulated question.

### 6.3 Truth-Seeking Output Format

**Response 1 (questions only — see Phase 0.3):**
Questions are output first, separately. Analysis only begins after user answers.

**Response 2 (analysis — after user answers or says "proceed"):**
```
## Claim Inventory (at least 10)
[Every factual claim — stated, embedded, and composite. Star (*) the load-bearing ones.]

## Observations
[Every detail you noticed, however small. Variable names, word choices, structural patterns,
version numbers, things that seem "off," things that seem too convenient. Don't filter for
relevance — details that seem trivial alone often combine into insights when read together.
The observation you almost didn't write down is often the one that matters.]

## Gotchas (at least 5)
[Known traps, surprises, counterintuitive behaviors, version-specific changes, common
misconceptions. For each: what most people assume vs. what actually happens. If you can't
find 5, you haven't looked — everything has gotchas.]

## Cross-References (MANDATORY)
[Read every observation against every starred claim. For each observation, ask: "Does this
contradict, tension with, or provide evidence for/against any starred claim?" List every
match. If an observation suggests a starred claim might be wrong, that claim MUST be verified
before proceeding. This is where hidden bugs surface — the details you noticed and the
assumptions you're making exist in separate lists until you force them to meet.]

## Question Assessment
[Was the question well-formed? If not, how was it reformulated?]

## Key Finding
[The most important thing — stated clearly, without hedging beyond what the evidence warrants]

## Evidence
[What evidence supports this? Source quality and incentive alignment noted.]

## Confidence
[Where on the ladder? What would change your mind?]

## What I Don't Know
[Gaps, unverified claims, areas of genuine uncertainty]

## Uncomfortable Truth (if applicable)
[The thing that's true but nobody wants to hear]

## New Questions
[Questions generated BY this analysis that didn't exist before. What did you learn that
raised new unknowns? These seed the next iteration.]
```

### 6.4 The Continuation Offer

After delivering your analysis, always end with:

> **Continue?** Say **iterate** for the full loop (audit → explore). Or invoke one mode
> directly: **audit**, **explore**, or **go deeper** on a specific point.

Three modes, each separately invocable:

**"audit"** → **Find what's missing, verify what's there.**
1. For each load-bearing claim: did I verify it or recall it? If recalled, hedge it now.
2. Search for documented counterexamples, gotchas, version-specific behavior changes.
3. Flag any claims that survived only because you didn't question them.

**"explore"** → **Breadth-first — new angles, new vocabulary, contradictions.**
1. Re-read your Questions, Observations, Gotchas, and Cross-References. Which ones did you
   list but never follow up on? Follow them now.
2. Search for contradictions to starred claims: "[topic] gotchas", "[topic] unexpected
   behavior", "[topic] breaking changes."
3. Converge — compare what you found against existing claims. Update the analysis.

Breadth exploration catches confident-wrong claims that depth verification skips — because
you verify claims you doubt, but you never doubt the ones that are wrong.

**"go deeper"** → **Depth-first on a specific finding, claim, or area.**
The user says "go deeper on X." Take that specific point and push it as far as it goes:
verify the evidence chain, find edge cases, explore implications, check whether the
conclusion holds under different conditions. Exhaust that thread before surfacing.

**"iterate"** → **The full loop: audit then explore.**
Questions first — present New Questions from previous response. Stop. Wait for answers. Then
run audit (find missing, verify claims) followed by explore (new angles, contradictions,
convergence). This is the default when the user just wants the best answer and trusts the
process to get there.

### 6.5 The Continuation Notice

> **Continuation note:** This is a single pass. Say **iterate** for the full loop,
> **audit** to verify claims, **explore** for new angles, or **go deeper on [X]** to
> push a specific point. 2-3 rounds usually surfaces what a single pass buried.
