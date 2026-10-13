---
name: generative-thinking
description: Break out of a locked problem frame by picking one disciplined move — reframe, provocation (Po), random stimulus, SCAMPER, inversion, structured analogy, constraint play, or family traversal — and committing to it before evaluating. Use when stuck, when options feel narrow or obvious, when iterations produce variations of the same idea, or when the user says "widen this", "break out of", "think differently", "I'm stuck", "feels too obvious", "stress-test the framing", "what am I missing", or holds two related examples and asks what lies between or beyond them. Complements challenging (which evaluates) and convening-experts (which synthesizes viewpoints); this skill generates distance, not judgment.
metadata:
  version: 0.3.0
---

# Generative Thinking — One Move, Committed

Fixation is the default state. When a generator (human or LLM) has been working on a problem, attention concentrates on the current framing and subsequent ideas tend to be local variations on it. This skill is the interrupt: spend one move stepping sideways, then resume.

The discipline matters more than the move. Pick ONE technique per invocation, run it without second-guessing, and produce explicit reframings or candidate entry points — not a brainstorm list in the same frame.

## When to reach for this

Claude activates this skill when:
- The last 2+ iterations are variations of one idea (fixation signal)
- The user says "widen this", "think bigger", "I'm stuck", "what am I missing", "too narrow", "break out of"
- A problem is framed as a binary ("X or Y") and neither option is good
- An agent loop is producing convergent variations — suspect the frame, not the search depth
- The user explicitly wants a pre-mortem on the *framing* (not the plan) before committing

Do NOT activate this skill as a default before every consequential task — fixation is the trigger, not stakes. If the current frame is working, let it work.

## Core discipline

Three rules that apply across every move below. Violations make the output ideation-flavored but structurally identical to what came before.

1. **Generation before evaluation.** De Bono's core distinction: lateral thinking cares about *movement value*, not truth value. A provocation is not a proposal. Evaluate only after the move has produced 3+ candidate framings.
2. **One move, committed.** Do not rotate through five techniques as a menu. Pick the move that matches the diagnosis, execute it fully, surface what shook loose, then stop. Menus produce noise; commitment produces distance.
3. **Output framings, not ideas.** The deliverable of a generative move is usually *a new statement of the problem* or *a new entry angle*, not another solution candidate inside the old frame. If the output could have been produced without the move, the move didn't fire.

**Stop condition.** Stop when the move has produced 3+ non-trivial framings, or a single framing that reorganizes the problem (one sharp surprise beats five adjacent). Do not keep generating because the list looks short — volume is not the product.

**The fire test.** After every move, ask: *could this output have been produced without the move?* If yes, the move did not fire. Either commit harder (push the provocation further, make the reframe more aggressive, re-roll the random word, invert on a different axis) or the move was mismatched to the stuck-pattern — re-diagnose and pick the better-matched move. Re-diagnosis after a miss is not menu-rotation; menu-rotation is cycling through techniques without commitment. One move at a time, each one fully, and if it misses, diagnose why before the next.

**Tail sift.** The fire test with a number attached. Post-trained models carry a typicality bias: asked for one candidate they return the modal one, and asked for a list they return the top-k modes — a bestseller list, not a sample (Zhang et al. 2025). The 3 framings a move produces are subject to this too. So before evaluating, over-generate — 5 to 8 candidates rather than 3 — and write next to each one the probability, 0 to 1, that a generator still inside the old frame would have produced it. Drop everything above the threshold; the remainder is the move's actual output. Start the threshold at 0.3 and lower it if the survivors still read as adjacent. Writing the number is the mechanism, not decoration: prompts that request a distribution with verbalized probabilities recover diversity that prompts for instances or lists do not, quality holds when the candidates are reasoned rather than listed, and lowering the stated threshold moves output further into the tail. The gain scales with model capability; on a small model the sift adds burden without adding distance.

## Diagnostic → Move

Match the stuck-pattern to the move. When unsure, default to **Reframe**.

| If the stuck-pattern is… | Reach for… |
|---|---|
| Framing feels forced ("must be X or Y") | **Reframe** — change the verb, subject, scope, or level |
| Generator keeps returning near-duplicates | **Random stimulus** — force an unrelated concept into the frame |
| Obvious answer is wrong but you can't see past it | **Provocation (Po)** — state something impossible, extract movement |
| Iterating on an existing artifact | **SCAMPER** — seven structured transforms |
| Stuck on "how do we make X succeed?" | **Inversion** — ask "how do we guarantee X fails?" then negate |
| Problem is defined entirely in one domain's vocabulary | **Structured analogy** — map objects and relations by function into a distant domain, search there |
| Every solution is blocked by a constraint | **Constraint play** — remove it ("assume magic"), or add an absurd one ("must fit in a tweet") |
| Two known examples, no theory of the space between/beyond them | **Family traversal** — name the shared family, walk it to its limits |

### Reframe
The problem-as-stated is rarely the problem-to-solve. Mutate the sentence:
- Change the **verb**: "reduce X" → "redistribute X", "time-shift X", "prevent X from mattering"
- Change the **subject**: "our team can't ship faster" → "reviewers are the bottleneck" → "the artifact is too reviewable"
- Change the **scope**: zoom out (whose problem is this upstream?) or zoom in (which one user, which one minute?)
- Change the **frame**: from "problem to fix" to "signal to interpret"

Produce 3 reframings. **Fired if**: at least one makes the original statement sound naive, or shifts who owns the problem.

### Provocation (Po)
Edward de Bono's method. Prefix a deliberately wrong, impossible, or absurd statement with `Po:` to signal it is not a proposal — it is a stimulus. Then extract movement: what principle, consequence, or adjacent idea does this surface?

Four recipes (de Bono's formal provocations):
- **Escape**: remove an essential feature. *Po: the database has no writes.*
- **Reversal**: flip the causal direction. *Po: users pay us to NOT use the product.*
- **Exaggeration**: push a quantity to the absurd limit. *Po: onboarding takes six months.*
- **Wishful thinking**: assume impossible capability. *Po: we know what the user will click next week.*

The canonical example: a factory pollutes a river. *Po: the factory is downstream of itself.* Impossible, but it generates: move intake downstream of discharge. Internal incentive to not pollute. Closed-loop water. The provocation is discarded; the movement stays.

**Fired if**: the provocation is genuinely impossible or absurd (not merely edgy), AND extracting movement yields a principle that survives translation back to the real constraints. If the "provocation" is a thing you could actually do, it's a proposal, not a Po — push it further.

### Random stimulus
Pick a word, object, or domain with no connection to the problem. Force a connection. The forced-feel is the point — it routes around the habituated pathway.

Template: *"How is [problem] like [random]?"* then *"What does that suggest?"*

**Sourcing for humans**: a random Wikipedia article, a nearby physical object, an Oblique Strategies card, a concept from an unrelated field on the current desk. Commit to the first thing you land on; re-rolling defeats the method.

**Sourcing for an LLM agent**: an LLM asked directly for a random word does not produce one — the same attention that locked the frame picks a word adjacent to it, and post-training biases the pick toward whatever is typical. Two sources work:

- *External*: ask the user for a word, any word; fetch a random Wikipedia article; draw an Oblique Strategy by tool.
- *Internal, hashed* — String Seed of Thought (Misaki & Akiba 2025). Write out a long random string (40+ characters, mixed letters, digits and symbols, no visible pattern). Then write out the reduction — sum the character codes, or compute a rolling hash — modulo the size of a pre-listed vocabulary, and take the word at that index. [`references/stimulus-vocabulary.md`](references/stimulus-vocabulary.md) holds 128 nouns from distant domains for exactly this; the Oblique Strategies deck works the same way. Measured: the recipe reaches near-PRNG faithfulness on long-reasoning models, and on open-ended generation it beat both an injected PRNG seed and a random-number tool call, because the string can be re-hashed for several local choices and the derivation is on the page. Two failure modes, both measured: a lazy extraction that reads only the first character (LLM-generated strings have strong positional bias — 947 of 1000 QwQ-32B strings opened with "7"), and skipping the written arithmetic, after which reasoning models hallucinate the result. Use the whole string; write the sum. Models under ~8B cannot execute the reduction reliably — hand them an external source.

**Fired if**: the connection is genuinely forced (the first 10 seconds feel wrong), and working through the force produces an angle that was not in your prior search space. If the random word feels "relevant" immediately, you re-rolled, picked from attention, or read one character of the seed — get a new one.

### SCAMPER
For iterating on an existing artifact. Walk the seven prompts once; do not pick favorites in advance.

- **S**ubstitute — swap a component, material, person, step
- **C**ombine — merge with something else, including something it competes with
- **A**dapt — borrow a mechanism from elsewhere that solves a related problem
- **M**odify / magnify / minify — change a dimension, frequency, or weight drastically
- **P**ut to another use — who else could use this, for what?
- **E**liminate — what happens if this part simply is not there?
- **R**everse / rearrange — swap order, roles, or polarity

**Fired if**: at least one prompt produced a candidate you would not have reached by asking "what's a better version of this?". If all seven outputs are adjacent polish, the artifact is not the unit of analysis — zoom out and try Reframe.

### Inversion
Solve the inverse problem, then negate the solution. Works because failure modes are often more concrete than success paths.

- "How would I guarantee this fails?" → each failure mode is a protective requirement
- "What would the worst possible version look like?" → the inverse shape of the good version
- "If an adversary wanted us to choose X, why?" → surfaces the hidden trap in X

**Fired if**: inverting surfaced a concrete risk, mechanism, or incentive the forward framing was hiding. If negating the inverted answer gives you the same thing you already had, the inversion was too symmetric — invert on a different axis (goals → incentives, success → unobservable, user → operator).

### Structured analogy (perspective shift)
Move the problem into a distant domain by its relational structure, not by asking the distant domain a question. "How would biology solve this?" is the cross-domain baseline in Shen, Druckmann & Zou (2026), and it collapses almost as hard as no domain prompt at all: across 150 generations per problem, about 5% of proposed domains were unique, and solution diversity (Vendi score) was 8.3 against 5.8 for the unconstrained baseline. Explicit structure-mapping scored 90–173% higher on solution diversity, produced solutions judged novel 50–69% of the time against 1.6–38% for the baselines, and reached domains further from the problem. The written mapping is what changes the outcome.

Four steps, after Gentner's structure-mapping theory:
1. **Extract.** List the problem's objects with their functional roles, and the relations between them — predicates over two or more objects ("a stationary source releases a substance into a heterogeneous medium"). Attributes of single objects are not mapped.
2. **Map by function.** Pick a distant domain and write object ↔ object pairs with the reason each pair holds. "Delivers a payload" is a mapping basis; "is a liquid" is not. Partial coverage is allowed — the analogy needs a subset of the relations, not all of them.
3. **Search the target side.** Find an existing, named method in the distant domain that operates on the *mapped* objects and preserves the shared relations. Search there, not for solutions to the original problem. (Drug delivery ↔ groundwater contamination gave reactive-transport plume models; EEG source localization ↔ seismology gave the double-difference earthquake location algorithm.)
4. **Transfer back.** Re-substitute the source objects and state what the method becomes in the original domain.

Domain menu, when step 2 needs a starting point: **natural** (biology, ecology, geology), **trade** (kitchen, ER triage, shipping dock), **role** (CFO, child, historian, adversary), **scale** (100x, 1/100x).

**Fired if**: the mapped domain is one the problem's own literature would not cite, AND step 3 returned a named, existing method — not a metaphor. If the object pairs match by resemblance rather than role, or the "method" is the original problem restated in new nouns, the mapping was surface-level; redo step 2 with a further domain.

### Constraint play
Constraints define the solution space. Move them deliberately.

- **Remove**: "assume infinite budget / time / compute / permission" — what opens up?
- **Add absurd**: "must fit in a tweet", "under $5", "no code", "one meeting only", "physical-only"
- **Invert**: the constraint becomes the feature. Limited time → event-driven. Small budget → tiny team as the pitch.

**Fired if**: a relaxed-constraint solution reveals what you actually value (not just what you'll accept), or an added-constraint solution is sharper than the unconstrained one. If both feel like the same answer with a different budget, the binding constraint is elsewhere — find it.

### Family traversal
For when you hold two (or more) related instances and generation keeps orbiting them. The pair is not the object — the parametrized family containing both is. Sub-moves in descending observed yield:

1. **Name the face.** State the family or frontier both instances lie on, and its parameter. (*Two embedding quantizers → the rate–distortion frontier, parametrized by bits per dimension.*) If you cannot name the parameter, you have not found the family yet.
2. **Walk to the limits.** Continue past both anchors to the family's extreme points — limits are where members change character. (*The 0-bit limit of vector search is ranking by document prior; the zero-distortion limit is exact symbolic addressing — which revealed two "unrelated" projects as endpoints of one frontier.*)
3. **Swap the bound object.** Name the supporting constraint that walls the family — the bound that cannot be crossed. Since crossing is impossible within the model, change what the constraint binds. (*Cannot beat rate–distortion for embeddings → quantize the weights, or the knowledge, instead.*)
4. **Probe the chord.** Mixtures and blends of the anchors (dithering, ensembles, fusion weights). Lowest yield — blends average rather than extrapolate — but cheap. Run last, not first.

Then **sharpen and verify**: the traversal's real product is questions precise enough to have derivable answers; the discovery happens in the derivation and a cheap measurement, not in the geometry. (*A frontier framing of an addressing scheme implied a capacity law, j² ≤ 2^(significand bits); sixty seconds of numpy confirmed a cliff at exactly N = 4096, closing a four-month-old empirical mystery.*) Without this step the move outputs taxonomy, not generation.

**Fired if**: a limit point or constraint-swap landed outside the prior search space, AND at least one output is a checkable claim. If the output is only a tidy classification of the anchors, the move stalled — push further along the edge or swap the constraint.

*Caution*: do not equate the interior of the space with novelty. In high dimensions essentially all operation is already extrapolation outside the training hull (Balestriero & LeCun 2021), and mixtures of known points are averages. The generative directions are the limits and the constraint-swaps; the chord is a probe, not a doctrine.

## Applying the skill to an agent's own reasoning

LLM agents exhibit a context-bound analog of functional fixedness: attention concentrates on current framing and generates variations of it. A second mechanism compounds it and does not depend on context: preference data favors familiar text, so post-training sharpens the policy toward the modal continuation for any prompt (Zhang et al. 2025, Theorem D.1) — which is why "give me five alternatives" returns five near-neighbors even in a fresh context. Signals this is happening:
- The nth iteration has the same structure as the first
- The agent has rejected the same class of option three times with similar reasoning
- The plan has a step labeled "brainstorm" that is producing adjacent bullets

When detected, the fix is the same: pick one move from the diagnostic table, execute it on the agent's own current framing, and explicitly write out the new framing(s) before resuming work. The write-out is essential — a framing that stays implicit in attention gets re-absorbed into the previous frame.

## What this skill does NOT do

- **Does not evaluate.** Pair with **challenging** after generation if the artifact is high-stakes.
- **Does not do MECE coverage.** Use **tiling-tree** for exhaustive partitioning.
- **Does not synthesize multiple viewpoints.** Use **convening-experts** for collaborative multi-role panels.
- **Does not produce long idea lists.** A three-reframe output with one surprising move beats a fifty-item brainstorm in the original frame.

## Canonical references (progressive disclosure)

Load these only when the user wants depth on a specific technique.

- Lateral thinking, provocation, Po, random stimulus — Edward de Bono. Primary: [Wikipedia: Lateral thinking](https://en.wikipedia.org/wiki/Lateral_thinking), [Wikipedia: Po](https://en.wikipedia.org/wiki/Po_(lateral_thinking)). Essay: [de Bono, "Serious Creativity"](https://www.debono.com/serious-creativity-article). Books: *Lateral Thinking* (1970), *Serious Creativity* (1992).
- SCAMPER — Bob Eberle, *SCAMPER: Games for Imagination Development* (1971), built on Alex Osborn's *Applied Imagination* (1953) checklist. Summary: [Wikipedia: SCAMPER](https://en.wikipedia.org/wiki/SCAMPER).
- Oblique Strategies — Brian Eno & Peter Schmidt (1974–2001, five editions). Summary: [Wikipedia: Oblique Strategies](https://en.wikipedia.org/wiki/Oblique_Strategies). Full deck: [mattrickard.com/list-of-all-oblique-strategies](https://mattrickard.com/list-of-all-oblique-strategies). Draw one at random when reaching for random stimulus.
- Functional fixedness (the cognitive bias this skill counters) — Karl Duncker, originally *Zur Psychologie des produktiven Denkens* (1935); English translation *On Problem-Solving* (1945), [doi:10.1037/h0093599](https://doi.org/10.1037/h0093599). The candle problem is the canonical demonstration.
- Extrapolation vs interpolation in high dimensions (why "interior = novelty" is wrong) — Balestriero, Pesenti & LeCun, "Learning in High Dimension Always Amounts to Extrapolation," [arXiv:2110.09485](https://arxiv.org/abs/2110.09485).
- Typicality bias and mode collapse; verbalized-probability prompting (the tail sift) — Zhang, Yu, Chong, Sicilia, Tomz, Manning & Shi, "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity," [arXiv:2510.01171](https://arxiv.org/abs/2510.01171). Distribution-level prompts with probabilities raised creative-writing diversity 1.6–2.1× over direct prompting; a threshold in the prompt tunes how far into the tail; gains grow with model scale.
- String Seed of Thought (the hashed internal random stimulus) — Misaki & Akiba, Sakana AI, "String Seed of Thought: Prompting LLMs for Distribution-Faithful and Diverse Generation," [arXiv:2510.21150](https://arxiv.org/abs/2510.21150). Total-variation distance to the target distribution shrinks with string length even under autoregressive correlation (Thm 4.2); §D.5 for the first-character failure, §D.6 for the comparison against injected seeds and tool calls.
- Structure-mapping theory of analogy — Gentner, "Structure-Mapping: A Theoretical Framework for Analogy," *Cognitive Science* 7(2), 1983, [doi:10.1207/s15516709cog0702_3](https://doi.org/10.1207/s15516709cog0702_3). Relations map, attributes do not.
- Analogical reasoning as a diversity engine (the structured-analogy procedure) — Shen, Druckmann & Zou, Stanford, "Unlocking LLM Creativity in Science through Analogical Reasoning," [arXiv:2605.11258](https://arxiv.org/abs/2605.11258). Extraction and search prompts in §G.1; four AR-generated methods implemented and benchmarked in biomedicine.
- Design fixation and generative-AI specific failure modes — Wadinambiarachchi, Kelly, Pareek, Zhou & Velloso, "The Effects of Generative AI on Design Fixation and Divergent Thinking," CHI 2024, paper 380, [doi:10.1145/3613904.3642919](https://doi.org/10.1145/3613904.3642919) ([arXiv:2403.11164](https://arxiv.org/abs/2403.11164)). N=60 visual ideation experiment: participants with AI image-generator support showed *higher* fixation on the initial example, and lower fluency, variety, and originality than the no-support baseline. Directly relevant when the fixation is coming from an LLM's own prior outputs.

## Quick-reference card

```
DIAGNOSE: What kind of stuck?
  → framing forced        : REFRAME
  → near-duplicates       : RANDOM STIMULUS
  → can't see past obvious: PROVOCATION (Po)
  → iterating an artifact : SCAMPER
  → chasing success       : INVERSION
  → one domain vocabulary : STRUCTURED ANALOGY
  → blocked by constraint : CONSTRAINT PLAY
  → two examples, no theory: FAMILY TRAVERSAL

DISCIPLINE:
  1. Generation before evaluation
  2. One move, committed
  3. Output framings, not ideas
  TAIL SIFT: over-generate 5-8, tag P(old frame reaches it), drop > 0.3

STOP when: 3+ non-trivial framings produced, or one surprising framing that reorganizes the problem.
```
