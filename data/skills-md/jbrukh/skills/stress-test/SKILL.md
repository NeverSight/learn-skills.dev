---
name: stress-test
description: Adversarially test a thesis or take for differentiation, robustness, and blind spots. Prevents publishing consensus as contrarian and surfaces what would change your mind.
---

# Stress Test

Take a thesis, take, or conviction and attack it. The goal is not to debunk — it's to find the load-bearing assumptions, test whether the take is genuinely differentiated, and surface the specific conditions under which it breaks. A take that survives stress-testing is worth publishing and acting on. One that doesn't was going to embarrass you eventually.

## When to Use

- User has a thesis, take, or prediction and wants to pressure-test it before publishing or acting
- User asks "is this take actually good?" or "what am I missing?" or "stress test this"
- User wants to know whether an insight is genuinely differentiated or just consensus
- User has conviction and wants to find the strongest counterargument before someone else does

Do NOT use for: generating insights from data (use surface-insight), evaluating prompts (use think-critically), or reframing problems (use mental-models).

## The Adversarial Rule

This skill's job is to find weaknesses. The single most important rule:

- Every attack must reference the specific thesis the user provided — no generic objections
- ENFORCEMENT: Every attack in the output must contain a verbatim quote from the user's thesis in the "The claim" field. If you cannot quote the thesis directly, the attack is not specific enough — discard it.
- If an attack would apply equally to any take on any topic, it's filler — discard it
- The test: "Would this specific objection surprise the person who holds this thesis?" If no, it's too obvious
- Prefer attacks where the user's own evidence or framing contains the seed of the problem

Honest stress-testing that finds nothing fatal is more valuable than performative skepticism that manufactures doubt. "This take is strong, here's the one thing to watch" is a valid output.

## Process

### Phase 1: Thesis Extraction (Silent)

Read the user's input. Silently identify:
- The core claim (what is actually being asserted?)
- The implicit claims (what must also be true for the thesis to hold?)
- The framing (how is the thesis positioned — as contrarian? obvious? urgent? inevitable?)
- The evidence offered (what supports it, and what's suspiciously absent?)
- The action it implies (what would someone do if they believed this?)

Restate the thesis internally in its strongest form before attacking it. Steel-man first, then stress-test. Attacking a weak version is dishonest and useless.

VAGUE THESIS GATE: If the thesis is too vague to attack substantively (e.g., "AI will be big," "crypto is the future"), do not proceed with attacks. Instead, output: "This thesis is too vague to stress-test. Here are 2-3 specific, attackable versions of what you might mean:" followed by 2-3 sharpened reformulations. Ask the user to pick one, then proceed. A stress test of a vague thesis produces only vague attacks — which violates the specificity rule.

FIRST-TOKEN RULE: Your output must begin with the literal characters "## Stress Test:" — no thinking, analysis, phase output, or preamble may precede this. Phase 1 and Phase 2 are internal reasoning only. If any text from Phase 1 or Phase 2 appears in your output, you have violated this constraint. Exception: if the VAGUE THESIS GATE triggers, your output begins with the vague-thesis response instead.

### Phase 2: Attack Discovery (Silent)

Run the thesis through each Attack Vector below. Not as a checklist — start from the thesis and find where it's genuinely vulnerable, then use the attack vectors to name and structure what you find.

For each vulnerability discovered, ask:
1. Is this a fatal flaw, a meaningful weakness, or a cosmetic issue?
2. Does it undermine the thesis itself, or just the way the thesis is framed?
3. Can the user fix it by adjusting the thesis, or does it require abandoning it?

Discard cosmetic issues. Keep fatal flaws and meaningful weaknesses.

EVIDENCE ASSESSMENT: Determine whether the thesis comes with supporting evidence or is a bare assertion. If evidence is provided, at least one attack must directly engage with that evidence — showing it's cherry-picked, misinterpreted, supports a different conclusion, or is insufficient for the claim's scope. If no evidence is provided, note "unsupported assertion" in at least one attack and explain what evidence would be needed to make the thesis credible.

FIRST-TOKEN RULE (repeated): Your output must begin with "## Stress Test:" — Phase 2 is internal reasoning only and must not appear in your output.

### Phase 3: Develop the Attacks

For each vulnerability, develop the attack:

1. **Name it** — What specific failure mode does this represent?
2. **Ground it** — Quote or reference the specific element of the thesis you're attacking
3. **Make the case** — Argue the counterposition as if you believe it. No hedging.
4. **Assess severity** — Fatal (thesis falls apart), Serious (thesis needs major revision), or Moderate (thesis survives but with caveats)

HARD RULE: Output exactly 3-5 attacks. If you find more than 5, keep the 5 most damaging. If you find fewer than 3 genuine vulnerabilities, say so — "This thesis is unusually robust; here are the 2 real risks" is honest. Never pad with weak attacks to hit a number.

STRONG THESIS PROTOCOL: If after genuine adversarial analysis you find fewer than 3 vulnerabilities above "cosmetic" level, output only the vulnerabilities you found — even if that's 1 or 0. In this case, add a "## Strengths" section before the Verdict listing 2-3 specific reasons the thesis is robust, referencing which attack vectors it survived and why. Do not manufacture attacks to fill a quota. A verdict of "Strong" with 1-2 moderate attacks is a legitimate and valuable output.

QUALITY GATE: After drafting all attacks, re-read each one and apply this test: "If the user shared their thesis publicly and a smart, informed critic responded, would this attack be the one that makes them wish they'd thought harder?" If no, delete the attack entirely — do not attempt to sharpen a fundamentally weak attack. It is better to output 2 genuine attacks than 4 where half are padding. The honest count matters more than hitting the range.

### Phase 4: Output

HARD CONSTRAINT: Your output must begin with the "## Stress Test:" header followed immediately by the first attack. No introductory paragraphs, context-setting, or thesis analysis may appear before the first attack. The one-line restatement in the header is the only permitted restatement of the thesis.

Present attacks ordered by severity (most damaging first).

**Output format:**

```
## Stress Test: [one-line restatement of thesis in its strongest form]

### [Attack Name]

**Severity:** [fatal | serious | moderate]

**The claim:** [verbatim quote from the user's thesis being attacked]

[2-4 sentences: the counterargument, stated with conviction. Every sentence must reference something concrete — a named entity, a market signal, a historical precedent, a logical contradiction, a specific mechanism. No sentence may consist entirely of abstract skepticism. Every attack must draw on your knowledge of the specific domain the thesis addresses — name real companies, real market dynamics, real historical precedents, or real technical constraints from that domain. Do not invent illustrative examples; use actual ones. If you lack domain knowledge to ground an attack concretely, state that limitation rather than fabricating specifics.]

**What it would take:** [1 sentence: name a specific, observable outcome the user could actually investigate — a dataset to check, a market event to watch for, a company's results to track, or an experiment to run. "More evidence" or "time will tell" are not acceptable answers.]

**My read:** [1-2 sentences: give your honest assessment of whether this vulnerability is likely to be resolved in the thesis's favor, drawing on what you actually know about the domain. State evidence, precedents, or current signals that inform your view. Do not hedge — take a position.]
```

After all attacks, output the Verdict section, then the Reframed Thesis section (only for "Reframe needed" or "Abandon" verdicts), then the Kill Question section.

## Attack Vectors

Use these to find and articulate vulnerabilities — not as a checklist to generate attacks.

### Differentiation

- **Consensus Camouflage.** The thesis feels contrarian but is actually what most informed people already believe. Test: search for who else is saying this. If Twitter, VC blogs, and mainstream media already agree, it's not alpha — it's a mood.
- **Audience Capture.** The thesis tells the user's audience exactly what they want to hear. Takes that flatter your followers are the most dangerous because the engagement validates the conviction.
- **Recency Bias.** The thesis is driven by whatever happened in the last 2 weeks. Test: would you have made this claim 3 months ago? If not, what changed — and is that change durable or a news cycle?

### Logic & Evidence

- **Missing Mechanism.** The thesis predicts an outcome but doesn't explain the causal chain. "X will happen" without "because Y will cause Z which leads to X" is a vibe, not an argument.
- **Survivorship Bias.** The evidence cited is selected from successes. What about the failures? If the thesis is "AI companies that focus on integration win," how many focused on integration and failed?
- **Unfalsifiability.** There is no evidence that would cause the thesis-holder to abandon it. If the thesis absorbs all counterevidence ("the market just doesn't understand yet"), it's faith, not analysis.
- **Conflation.** The thesis treats two different things as one. Common form: conflating "this technology works" with "this technology will be adopted" or "this is true" with "this is investable."

### Timing & Context

- **Right Church, Wrong Pew.** The thesis is directionally correct but the timing or magnitude is wrong. Being 5 years early on a trend is economically identical to being wrong.
- **Base Rate Neglect.** The thesis treats a likely-sounding scenario as certain without considering the base rate of similar predictions. Most "this changes everything" claims don't pan out, even when the underlying technology is real.
- **Regime Dependence.** The thesis is true under current conditions but those conditions are fragile. What regulatory change, market crash, or technical failure would invalidate it?

### Framing & Positioning

- **Motte and Bailey.** The thesis oscillates between a strong, exciting claim (the bailey) and a weak, defensible one (the motte). When challenged, it retreats to the motte; when unchallenged, it advances to the bailey. Identify which version the user actually believes.
- **Framing as Substance.** The thesis feels like it says something but is actually about framing, not about the world. Test: does this thesis make a prediction? If not, it's a narrative, not a claim.
- **The Underpants Gnome.** Step 1: [observation]. Step 2: ???. Step 3: [conclusion]. The thesis jumps from a real observation to a conclusion with a missing middle step.

---

## Verdict

After the attacks, deliver one of four verdicts. Be direct.

- **Strong** — The thesis survives stress-testing with only moderate vulnerabilities. Worth publishing and acting on. State the 1-2 specific adjustments that would make it bulletproof, and name the one thing to monitor that could change your assessment.
- **Promising but exposed** — The thesis has a real insight at its core but has serious vulnerabilities that need addressing before it's ready. State what specific revision would fix it.
- **Reframe needed** — The thesis as stated doesn't hold, but there's a better version hiding inside it. Output the Reframed Thesis section (see below).
- **Abandon** — The thesis has a fatal flaw. Say so clearly and say why. Output the Reframed Thesis section with the adjacent thesis or reframed question worth pursuing instead. Not every take deserves to be rescued, but the user still needs a direction.

CALIBRATION CHECK: Before selecting a verdict, ask: "If I had not just spent the entire prompt looking for flaws, would I still assign this verdict?" The adversarial process can inflate perceived severity. Weight the verdict on the actual severity ratings of your attacks: if no attack is rated fatal and at most one is serious, the verdict should be Strong or Promising but exposed, not Reframe needed or Abandon.

Format:

```
## Verdict: [Strong | Promising but exposed | Reframe needed | Abandon]

[2-3 sentences: the verdict explained, referencing the specific attacks that drive it. If the thesis is worth keeping, state the exact revision that would strengthen it.]
```

---

## Reframed Thesis

Output this section ONLY when the verdict is "Reframe needed" or "Abandon." Do not output it for "Strong" or "Promising but exposed" verdicts.

This is a structured thesis card ready to feed back into stress-test or forward into write-oped. It must be concrete enough that the user can act on it immediately without further interpretation.

Format:

```
## Reframed Thesis

**Claim:** [One declarative sentence. A specific, attackable assertion — not a question, not a direction, not a topic. Must pass the test: "Could someone disagree with this?"]

**Key shift:** [One sentence: what changed from the original thesis and why — name the specific flaw this reframe fixes]

**Betting against:** [One sentence: what consensus or common belief this thesis disagrees with]

**Would change my mind:** [One sentence: a specific, observable outcome that would falsify this reframed thesis — same standard as "What it would take" in the attack format]
```

QUALITY GATE: The reframed thesis must itself be stress-testable. If you cannot imagine at least 2 genuine attacks against it, it's too vague or too safe — sharpen it. The point is to hand the user a stronger thesis, not a retreat to the motte.

---

## Kill Question

End with a single question — the one question that, if the user can answer it convincingly, confirms the thesis holds. If they can't, the thesis is in trouble.

This should be the hardest, most specific question you can construct from the vulnerabilities you found. Not "are you sure?" but "if the bottleneck is really integration not capability, why are the integration-focused AI startups from 2023 not dominant yet?" The Kill Question must be a single question — not a compound question with "and" or multiple clauses. One sentence, one question mark.

Format:

```
## Kill Question

[A single, specific, answerable question that tests the thesis at its weakest point]
```

---

## Quality Standards

The quality bar is the **wince test**: does the attack make the thesis-holder uncomfortable because it hits a real nerve, not because it's unfair?

- **Fail — Generic skepticism.** "But what if you're wrong?" REJECT.
- **Fail — Straw man.** Attacking a weak version of the thesis. REJECT.
- **Pass — Specific counterargument.** An objection that requires the thesis-holder to think. MINIMUM.
- **Good — Evidence-based attack.** Uses real-world data, precedents, or logical structure to expose a flaw.
- **Strong — Internal contradiction.** Shows that the thesis's own evidence or framing undermines it.
- **Exceptional — Reframe attack.** Shows that the entire frame of the thesis is wrong, not just the conclusion.

Aim for "Good" or above on at least half of attacks. Never output "Fail" level.

---

## Anti-Patterns

- **Performative skepticism.** Being contrarian for the sake of balance. If the thesis is strong, say so — then find the one real risk.
- **Generic objections.** "But markets are unpredictable" applies to everything and therefore says nothing.
- **Tone-policing as analysis.** "The thesis is too confident" is not an attack on the thesis — it's an attack on the tone. Address the substance.
- **The false balance.** Manufacturing 5 attacks when only 2 are real. Three strong attacks beat five where two are padding.
- **Rehashing the thesis.** Spending paragraphs restating the thesis before attacking it. Get to the attack.
- **Hedged attacks.** "One could argue that perhaps..." — commit to the counterargument or drop it. An attack that hedges isn't an attack.
- **Applause-line objections.** Objections that sound smart in the abstract but don't connect to this specific thesis. Test: remove the thesis-specific nouns — does the attack still make sense? If yes, it's generic.

---

## Key Principles

1. **Steel-man first, then attack.** Restate the thesis in its strongest form before finding weaknesses. Attacking straw men is dishonest.
2. **Specific, not skeptical.** Every attack must name a concrete mechanism, precedent, data point, or logical flaw. Generic doubt is worthless.
3. **Severity matters.** Distinguish between "this thesis is wrong" and "this thesis is right but incomplete." The user needs to know which attacks are cosmetic and which are structural.
4. **The kill question is the product.** The single most valuable output is the question that crystallizes the thesis's central vulnerability into something the user can investigate and resolve.
5. **Honest verdicts.** "This is strong" is as valuable as "abandon this." The skill's credibility depends on not manufacturing doubt where none exists.
6. **Attacks that improve.** The best stress test doesn't just find problems — it points toward the stronger version of the thesis. Even fatal flaws should suggest what the user should think instead.

---

## Input

[User provides a thesis, take, prediction, or conviction below]
