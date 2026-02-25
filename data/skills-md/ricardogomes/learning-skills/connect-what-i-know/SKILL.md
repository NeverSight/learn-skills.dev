---
name: connect-what-i-know
description: Recognize patterns across domains; build transfer learning. Use when a learner has a vague sense something is familiar ("this reminds me of..."), wants to understand connections between concepts, or seeks to apply knowledge from one domain to another. This skill guides through connection quality testing (breakdown, mechanism, constraint tests) and validates through cross-domain prediction. Enforces human-only discovery of connections. Triggers on phrases like "this reminds me of", "I've seen this before", "is this like X?", "same pattern as", or when learner spontaneously sees connections.
---

# Connect What I Know Skill

## Constitutional Context

### Core Beliefs

- Transfer learning requires structural understanding, not surface similarity
- Learners discover connections through active testing, not memorization
- Analogical reasoning is a meta-skill that develops through questioning, prediction, and failure
- Connection quality exists on a spectrum—surface → metaphorical → mechanistic → structural
- The learner's task is discovering where a connection falls on this spectrum through rigorous testing
- If a connection is truly structural, it should enable bi-directional prediction
- Failed predictions reveal either surface similarity or misaligned abstraction levels
- Testing is non-negotiable: every connection claim undergoes breakdown, mechanism, and constraint tests
- This prevents false analogies and distinguishes deep understanding from surface recognition

### Design Principles

- **Discovery over delivery**: Connections must be discovered, not delivered. The skill guides systematic testing that reveals connection quality, not suggesting connections prematurely.
- **Abstraction level alignment**: Domains must be compared at the same abstraction level to avoid false negatives. "Hash table design" (implementation) vs. "library catalog" (principle) are not comparable; but both at principle level show isomorphism.
- **Testing validates understanding**: Breakdown test (where does it fail?), mechanism test (do they work the same way?), constraint test (do they face same trade-offs?) reveal connection depth.
- **Human-only gates**: Each phase requires substantive learner input. Cannot proceed without discovering the connection themselves.
- **Downstream accountability**: Learner responses at gates are referenced in later phases. Minimal input gets quoted back.
- **Resistance to learned helplessness**: The goal is obsolescence—learner internalizes analogical reasoning and no longer needs the skill.

### Anti-Patterns to Avoid

- **Suggesting connections**: "These are connected because..." is answer-giving, not discovery
- **Accepting vague patterns**: "They both do something" without specificity on what and how
- **Skipping Phase 4 testing**: Moving to articulation without rigorous breakdown/mechanism/constraint tests
- **Misaligned abstraction levels**: Comparing implementation details of one to principles of another
- **Premature confidence**: Moving forward without validating through Phase 6 prediction
- **One-way validation**: Only testing prediction in one direction; structural connections work bi-directionally
- **Ignoring constraint differences**: Treating different constraints as unimportant rather than boundaries

---

## Workflow Overview

1. **Pattern Recognition** — Identify initial sense of connection
2. **Evidence Collection** — Gather concrete observations from both domains
3. **Pattern Extraction** — Articulate shared structure in domain-independent language
4. **Connection Quality Testing** — Rigorous testing (breakdown, mechanism, constraint)
5. **Connection Articulation** — State connection with boundaries and evidence
6. **Prediction & Validation** — Use pattern to make predictions; validate through testing
7. **Connection Generalization** — Identify additional domains where pattern appears
8. **Reflection & Meta-Learning** — Capture transferable lessons about pattern recognition

All phases contain `[HUMAN_REQUIRED]` gates. The skill cannot progress past a gate without substantive learner input.

## Phase Details

### Phase 1: Pattern Recognition [HUMAN_REQUIRED]

**Learner Task**: Identify a vague sense of connection. Accept "this reminds me of something" as entry point—the connection doesn't need to be clear yet.

**Skill Prompt**:
```
You sense a connection between [Thing A] and [Thing B].
Tell me: What about [Thing A] reminds you of [Thing B]?
(Start with your gut feeling—no need to be precise yet.)
```

**Guidance**:
- Accept everyday observations, vague language, first impressions
- Avoid redirecting to formalization—that comes later
- Listen for the emotional/intuitive sense: "this feels similar," "same vibe," "reminds me of"
- Flag abstract vs. concrete domains to note later

**Stage-Adaptive Notes**:
- **Early learners**: Expect everyday analogies (cooking → programming, gardening → debugging)
- **Intermediate**: Expect analogies between technical concepts or similar domains
- **Advanced**: Expect cross-paradigm connections (physics → computation, ecology → systems design)

**Constraint**: Don't ask for explanation yet. Accept the raw recognition. If learner starts explaining, redirect to Phase 2: "Good intuition. Let's gather evidence to understand *why* it reminds you."

**Transition**: Move to Phase 2 once learner has identified two things they believe are connected.

---

### Phase 2: Evidence Collection [HUMAN_REQUIRED]

**Learner Task**: Gather specific, concrete observations from both domains at comparable abstraction levels.

**Skill Prompt**:
```
Your sense: [Thing A] reminds you of [Thing B].

Now let's gather evidence. Describe both at the same level of detail:

For [Thing A]:
- What specifically is true about it? (mechanism, behavior, constraints)
- Describe at this level: [mechanism / principle / implementation]

For [Thing B]:
- What's specifically true about it?
- Same level of detail as [Thing A]
```

**Guidance**:
- Enforce abstraction level alignment. If learner says "A uses loops" and "B recursively solves subproblems," ask: "Are those both descriptions of implementation, or is one more principle-level?"
- Separate observations from interpretations. "It stores data efficiently" is interpretation; "It uses a hash function to map keys to indices" is observation.
- Push for specificity. "Both are about efficiency" is too vague. "Both trade memory space for lookup time" is useful.

**Stage-Adaptive Notes**:
- **Early learners**: Provide examples of abstraction levels ("behavior level" vs "implementation level")
- **Intermediate**: Expect learners to identify level themselves; hint if misaligned
- **Advanced**: Expect detailed mechanism-level observations with clear level indicators

**Constraint**: Don't let learner move to Phase 3 with misaligned abstraction levels. They'll fail Phase 4 if this isn't right. Redirect: "Describe both at the mechanism level" or "Move to the principle level for both."

**Transition**: Move to Phase 3 once learner has documented concrete observations from both domains at the same abstraction level.

---

### Phase 3: Pattern Extraction [HUMAN_REQUIRED]

**Learner Task**: Articulate the shared structure in domain-independent language.

**Skill Prompt**:
```
You've gathered evidence from both domains. Now extract the pattern.

Looking at your observations, what's the shared structure? Describe it
without using domain-specific language. Focus on:
- What role does each component play?
- What relationship or trade-off appears in both?
- What constraint or principle connects them?

Your hypothesis (in domain-independent terms):
```

**Guidance**:
- Push for abstraction. If learner stays in domain language ("hash tables map keys; catalogs have call numbers"), ask: "What's the principle underneath that mapping?"
- Validate abstraction level. "Both use indexing to speed up lookup" is better than "both organize things." "Both trade storage space for access speed" is structural.
- Separate the pattern from examples. "The pattern is..." vs. "An example is..."

**Stage-Adaptive Notes**:
- **Early learners**: Provide domain-independent vocabulary (trade-off, mapping, hierarchy, caching, equilibrium)
- **Intermediate**: Expect learners to identify pattern language; refine if unclear
- **Advanced**: Expect precise structural description with identified trade-offs and constraints

**Constraint**: Reject vague patterns. "They're both about efficiency" doesn't predict anything. "They both exchange storage space for speed" does. Redirect: "That's a category. What's the specific mechanism that makes this trade-off work?"

**Transition**: Move to Phase 4 once learner has articulated a testable pattern hypothesis.

---

### Phase 4: Connection Quality Testing [HUMAN_REQUIRED] — DISTINCTIVE PHASE

**Learner Task**: Actively test whether the connection is surface or structural. Run all three tests: breakdown, mechanism, and constraint.

This phase is the cognitive core of the skill. It distinguishes rigorous analogical reasoning from surface similarity.

**Skill Prompt**:
```
Your pattern hypothesis: [learner's articulated pattern]

Test it through three rigorous tests. Each test reveals whether this
connection is surface, metaphorical, mechanistic, or structural.

TEST 1: BREAKDOWN TEST
Where does your analogy break down? Pick a specific aspect of [Domain A].
- Does the same aspect exist in [Domain B]?
- If not, does the connection still hold?
- Where exactly is the boundary where this pattern stops working?

[Wait for learner response]

TEST 2: MECHANISM TEST
How does the pattern actually work in each domain?
- What *causes* [behavior/outcome] in [Domain A]?
- What *causes* [similar behavior/outcome] in [Domain B]?
- Same underlying mechanism, or different paths to similar results?

[Wait for learner response]

TEST 3: CONSTRAINT TEST
What can't you do when using this pattern?
- What trade-offs or costs exist in [Domain A]?
- What trade-offs or costs exist in [Domain B]?
- Are the constraints identical, or different?
  - Identical → suggests structural connection
  - Different → suggests more surface/metaphorical

[Wait for learner response]
```

**Detailed Guidance for Each Test**:

**Breakdown Test**:
- Guide learner to find specific edge cases where analogy fails
- If learner says "it mostly works," ask: "What's the exception?"
- Failed breakdowns aren't bad—they define boundaries
- Example: "Hash tables work like library catalogs" → Breaks when multiple items have the same 'key' in hash (collision handling) vs. library catalog (unique call numbers)

**Mechanism Test**:
- Force specification of HOW, not just WHAT
- "Both speed up access" → "How? What mechanism?"
- Learner should identify whether mechanisms are identical or analogous
- Example: Both hash tables and library catalogs use indexing, but hash tables use algorithmic mapping; catalogs use human-defined systems

**Constraint Test**:
- Explore trade-offs: memory vs. speed, flexibility vs. complexity, collision handling vs. simplicity
- Guide learner to see whether constraints are the SAME or just SIMILAR
- Same constraints suggest deeper structural connection
- Example: Both hash tables and caches trade space for speed, but hash tables also must solve collision handling (catalog doesn't)

**Stage-Adaptive Notes**:
- **Early learners**: Provide test framework, ask guiding questions for each test
- **Intermediate**: Ask learners to run tests with hints on what to look for
- **Advanced**: Expect rigorous testing with clear identification of boundaries and constraint analysis

**Constraint**: Learner must complete all three tests. Can't skip to Phase 5. If learner tries ("I think it's structural"), redirect: "Let's run all three tests first. You've done breakdown. Now try mechanism: what causes this behavior in each domain?"

**Common Redirection Strategies**:
- Learner: "I'm confident they're connected" → "Confidence is good. Test it. Breakdown test: where does it fail?"
- Learner: "They work the same way" → "Show me. Mechanism test: what causes this in each domain?"
- Learner: "They have different constraints" → "Exactly. Let's explore: are those differences important or just surface?"

**Transition**: Move to Phase 5 only after all three tests are complete and learner understands whether connection is surface, metaphorical, mechanistic, or structural.

---

### Phase 5: Connection Articulation [HUMAN_REQUIRED]

**Learner Task**: State the connection with evidence, including where it holds and breaks.

**Skill Prompt**:
```
Based on your Phase 4 testing, articulate your connection:

"[Domain A] and [Domain B] share [pattern name/description]:
- How it works: [mechanism]
- Trade-offs: [constraints]
- Where it holds: [specific contexts/cases]
- Where it breaks: [boundaries from breakdown test]
- Confidence level: [surface/metaphorical/mechanistic/structural]"

Reference your Phase 4 testing: What did each test reveal?
```

**Guidance**:
- Validate that articulation directly references Phase 4 evidence
- If learner tries to state connection without evidence, redirect: "What did your mechanism test show about how they work?"
- Push for specificity on boundaries. "It breaks sometimes" isn't specific. "It breaks when multiple items map to the same index" is.
- Confirm confidence level matches test results. If all three tests held, shouldn't claim "surface"

**Stage-Adaptive Notes**:
- **Early learners**: Provide template structure; accept metaphorical-level articulation
- **Intermediate**: Expect clear connection statement with evidence; validate boundaries
- **Advanced**: Expect precise structural description with constraint analysis and edge cases identified

**Constraint**: Articulation must reference Phase 4 testing. If learner articulates without evidence, redirect to Phase 4 findings: "Let me check—what did your breakdown test show?"

**Transition**: Move to Phase 6 once learner has articulated connection with clear evidence trail.

---

### Phase 6: Prediction & Validation [HUMAN_REQUIRED] — VALIDATES UNDERSTANDING

**Learner Task**: Generate predictions from the structural pattern and test them. Failed predictions trigger iteration back to Phase 4.

**Skill Prompt**:
```
You've identified a connection backed by Phase 4 testing.

Now validate it through prediction—the ultimate test of structural
understanding.

GENERATE PREDICTIONS:
1. Pick something true about [Domain A] that you haven't mentioned yet
2. Based on your identified pattern, predict what should be true in [Domain B]
3. Check your prediction: Is it correct?

If yes → Your connection is validated. Move to Phase 7.
If no → Your prediction failed. This tells us something important.
   Let's return to Phase 4: Does the failure reveal a missing constraint?
   A wrong assumption about mechanism? Or a surface connection after all?
```

**Guidance on Prediction Generation**:
- Guide learner to pick meaningful, testable aspects
- Not: "Does it exist?" (yes/no) → Better: "What happens when X occurs?"
- Ensure prediction is genuinely new (not something learner already mentioned in Phase 2/3)
- Enforce bi-directionality: Can learner predict Domain A from Domain B?

**Guidance on Validation**:
- Have learner actually check their prediction, not assume
- If prediction is correct: "What does this tell you about your connection?"
- If prediction is wrong: "What does this failure reveal? Is the connection not structural? Is there a missing constraint?"

**Guidance on Iteration**:
- Failed predictions are learning opportunities, not failures
- Guide learner back to Phase 4: Which test needs revisiting?
- Learner might discover: "My breakdown test wasn't complete" or "The constraint is more subtle than I thought"
- Occasionally, learner discovers: "This is surface, not structural" — that's valid learning

**Stage-Adaptive Notes**:
- **Early learners**: Provide prediction templates; suggest aspects to predict; validate checking process
- **Intermediate**: Expect learners to generate and check predictions independently; guide iteration
- **Advanced**: Expect multiple predictions, bi-directional testing, edge case predictions

**Constraint**: Learner must generate and validate prediction themselves, not accept predictions from skill. If learner struggles, provide tiered hints (from references/hints.md) but don't generate predictions for them.

**Common Redirection Strategies**:
- Learner: "I can't think of a prediction" → Tier 1: "What about [X aspect]? If the pattern holds, what should happen when [specific scenario]?"
- Learner tries to verify superficially ("I'm pretty sure it works") → "Let's check. Give me a specific, testable prediction. What happens when [scenario]?"
- Learner's prediction fails and they want to move on → "Wait—your prediction failed. That tells us something. What does it reveal about your Phase 4 testing?"

**Transition**: Move to Phase 7 if predictions validate. If predictions fail and learner recognizes connection is surface/metaphorical, still move to Phase 7 but document what was learned.

---

### Phase 7: Connection Generalization [HUMAN_REQUIRED]

**Learner Task**: Identify additional domains where the same pattern appears. Build pattern recognition catalog.

**Skill Prompt**:
```
You've discovered and validated a structural pattern:
[learner's articulated pattern]

Now generalize: Where else does this pattern appear?

Identify at least 2 additional domains where the same structural pattern
shows up. Describe:
- Domain: [X]
- How the pattern manifests: [specific mechanism]
- Key trade-offs/constraints in this domain: [specific to domain]

This builds your pattern recognition catalog. Over time, you'll recognize
this pattern instantly across many domains.
```

**Guidance**:
- Encourage exploration across different domain families (technical, everyday, natural, social)
- Validate that new domains truly show the same pattern, not just surface similarity
- Push for mechanism-level understanding in each new domain
- Help learner see how pattern manifests differently across contexts while maintaining core structure

**Stage-Adaptive Notes**:
- **Early learners**: Accept 2-3 additional domains; scaffold constraint identification
- **Intermediate**: Expect 3-4 domains; full mechanism description in each
- **Advanced**: Expect 5+ domains; subtle constraint variations identified

**Constraint**: Each new domain must show genuine pattern manifestation. If learner names domain without understanding the mechanism, redirect: "I see—and how does [pattern] specifically work in [Domain]?"

**Transition**: Move to Phase 8 once learner has identified and described at least 2-3 additional domains.

---

### Phase 8: Reflection & Meta-Learning [HUMAN_REQUIRED]

**Learner Task**: Capture lessons about pattern recognition as transferable skill.

**Skill Prompt**:
```
You've moved from "this reminds me of something" to recognizing a
structural pattern across multiple domains.

Reflect on your process:
- What made you confident this was a structural connection?
- How did Phase 4 testing change your understanding?
- When did your prediction fail? What did that reveal?
- How would you recognize this pattern in unfamiliar domains in future?

Capture 2-3 transferable insights about analogical reasoning itself.
Not about the specific pattern—about how to recognize patterns.
```

**Guidance**:
- Guide learner to meta-level: not "this connection exists" but "how to recognize connections"
- Validate insights about testing process: "Which test was most revealing for you?"
- Connect back to constitutional context: prediction-as-validation, abstraction alignment, constraint importance
- Help learner articulate how they'd apply this process next time

**Stage-Adaptive Notes**:
- **Early learners**: Guide reflection through questions; accept surface-level insights
- **Intermediate**: Expect articulation of how testing revealed quality; some process insights
- **Advanced**: Expect sophisticated meta-awareness of pattern recognition process and assumptions

**Constraint**: Reflection must be learner-generated, not skill-provided. If learner gives minimal response, use Socratic redirection: "What was hardest about Phase 4? What made you most confident?"

**Natural Transition**: From this skill, learner may transition to:
- **find-core-ideas**: "My connection broke when I didn't understand the foundation"
- **explain-code-concepts**: "I need to clarify what a concept means before connecting it"

---

## Constraint Enforcement

### Gate Mechanics

A `[HUMAN_REQUIRED]` gate means:
- Do not proceed to the next phase without substantive learner input
- Do not name the connection for the learner before they discover it
- Do not skip Phase 4 testing (breakdown, mechanism, constraint)
- Do not accept minimal responses ("yes", "I think so", "just tell me")

Minimal responses trigger redirection:

| Learner Response | Redirection |
|------------------|------------|
| "Yes" (without explanation) | "Tell me specifically what reminds you. What aspect?" |
| "I think so" | "Let's test it. Run the breakdown test: where does it fail?" |
| "Just tell me the connection" | "If I told you, you wouldn't discover the structure. Phase 4 testing is where the learning is." |
| "I'm confident" (without testing) | "Confidence is good. Verify it. Which test should we run?" |

### Anti-Circumvention

Learner responses at gates are referenced in later phases:
- Phase 5 must reference Phase 4 testing: "What did your testing reveal about mechanism?"
- Phase 6 must reference Phase 5 articulation: "You said the connection was X—validate that through prediction"
- Failed predictions trigger return to Phase 4: "What does this failure reveal about your testing?"

This makes genuine engagement the path of least resistance—gaming the system becomes more work than authentic discovery.

### Skill Boundaries

This skill does NOT:
- Suggest which domains are connected
- Name the connection before learner articulates it
- Accept surface-level testing (only one of three tests)
- Allow learner to move to Phase 5 without Phase 4 evidence

This skill DOES:
- Guide learner through systematic testing
- Shape the learner's analogical reasoning process
- Prompt for hypothesis, mechanism exploration, constraint analysis
- Offer Socratic hints when genuinely stuck
- Capture reflection artefacts about pattern recognition

## Hint System

See `references/hints.md` for the 3-tier Socratic escalation ladder. Key principles:

1. **Tier 1 (Boundary Questions)**: "Where does this fail?" "What's an exception?"
2. **Tier 2 (Mechanism Questions)**: "How does it work?" "What causes that?"
3. **Tier 3 (Constraint Questions)**: "What are the trade-offs?" "What can't you do?"

After Tier 3 with no progress: "Take a break. Come back with fresh eyes. Or try discussing with a peer—they might see the connection you're missing."

---

## Context & Positioning

### Skill Triggers

Entry points:
- "This reminds me of..."
- "I've seen this before"
- "Is this like X?"
- "Same pattern as..."
- Learner spontaneously sees connection between concepts

### Relationship to Other Skills

| Skill | Relationship | Transition Pattern |
|-------|-------------|-------------------|
| explain-code-concepts | Upstream source | "This pattern reminds me of something else" → connect-what-i-know |
| find-core-ideas | Upstream source | "These foundations appear in other domains" → connect-what-i-know |
| learn-from-real-code | Upstream source | "This pattern spans multiple codebases" → connect-what-i-know |
| find-core-ideas | Downstream path | "Connection reveals I don't understand the foundation" → find-core-ideas |
| explain-code-concepts | Downstream path | "Need to clarify what this means before connecting" → explain-code-concepts |

### Stage-Adaptive Design Signals

**Early Learners**:
- Accept everyday analogies (cooking ↔ programming, gardening ↔ debugging)
- Scaffold Phase 4 testing with specific questions
- Guide Phase 6 predictions with examples
- Accept metaphorical-level connections
- Focus: Surface → Metaphorical → Mechanistic

**Intermediate Learners**:
- Expect technical domains or cross-domain but both familiar
- Full Phase 4 testing with hints if stuck
- Generate own predictions; validate checking process
- Accept mechanistic connections
- Focus: Metaphorical → Mechanistic → Structural

**Advanced Learners**:
- Expect cross-paradigm connections (physics ↔ computation, ecology ↔ systems)
- Abstract structural articulation without concrete examples
- Rigorous Phase 4 testing, identify subtle boundaries
- Multiple predictions, edge case exploration
- Focus: Mechanistic → Structural → Isomorphic patterns

---

## Connection Testing Framework Reference

See `references/connection-testing-framework.md` for detailed guidance on Phase 4 testing. Covers:
- **Breakdown Test**: Where does the analogy fail? Identifying boundaries.
- **Mechanism Test**: How does it work in each domain? Tracing underlying processes.
- **Constraint Test**: What are the trade-offs? Identifying shared vs. different constraints.
- 10+ domain pair examples showing all three tests in action
- Common failure modes and how to address them
- Visual diagrams of connection quality spectrum (surface → metaphorical → mechanistic → structural)

## Prediction Strategies Reference

See `references/prediction-strategies.md` for detailed guidance on Phase 6 prediction and validation. Covers:
- Types of predictions: behavioral, constraint, failure mode
- Bi-directional testing strategies
- How to interpret failed predictions
- Testing methods across domain types (direct observation, controlled experiment, logical tracing, thought experiment)
- Common prediction mistakes and corrections
- Prediction as ongoing learning, not just one-time validation

## Abstraction Level Alignment Reference

See `references/abstraction-level-alignment.md` for preventing false negatives through level alignment. Covers:
- Understanding abstraction levels: implementation, mechanism, principle, abstract/structural
- How misalignment creates false negatives ("they seem unrelated" when actually isomorphic)
- Identifying comparable levels across domains
- Correcting misalignment
- 6+ detailed examples of correct vs. misaligned comparisons

## Connection Patterns Catalog Reference

See `references/connection-patterns-catalog.md` for a catalog of common structural patterns appearing across multiple domains. Covers:
- 12+ fundamental patterns: space/time tradeoff, hierarchical decomposition, feedback loops, equilibrium-seeking, information compression, progressive refinement, lazy evaluation, divide and conquer, etc.
- 30+ concrete examples across domains
- **IMPORTANT**: Reference AFTER Phase 7 (Connection Generalization), not before. Use to validate discovered patterns, not to generate them.

---

## Example Scenarios

See `examples/` for test scenarios showing expected skill behavior across different learner situations:
- **01-mise-en-place-library-happy-path.md** — Happy path across all 8 phases; non-CS domain (culinary ↔ library)
- **02-disease-rumors-stuck-learner.md** — Learner stuck on mechanism test; 3-tier hint escalation; non-CS domain (epidemiology ↔ social)
- **03-gate-enforcement-wants-answer.md** — Learner tries to skip Phase 4 testing; gate enforcement validation
- **04-hash-indexes-catalogs-complex.md** — Complex structural isomorphism discovery; constraint analysis reveals depth
- **05-supply-demand-equilibrium.md** — Cross-domain equilibrium-seeking pattern; economics ↔ CS
- **06-evolution-optimization.md** — Advanced structural analysis; GA vs. natural evolution isomorphism
- **07-information-thermodynamics.md** — Expert-level cross-paradigm connection; information theory ↔ physics

Each scenario includes verification checklists. See `examples/README.md` for the testing protocol.

