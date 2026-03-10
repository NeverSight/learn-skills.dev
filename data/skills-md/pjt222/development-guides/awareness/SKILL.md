---
name: awareness
description: >
  AI situational awareness — internal threat detection for hallucination risk,
  scope creep, and context degradation. Maps Cooper color codes to reasoning
  states and OODA loop to real-time decisions. Use during any task where
  reasoning quality matters, when operating in unfamiliar territory, after
  detecting early warning signs such as an uncertain fact or suspicious tool
  result, or before high-stakes output like irreversible changes or architectural
  decisions.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: defensive
  complexity: advanced
  language: natural
  tags: defensive, awareness, threat-detection, hallucination-risk, ooda, meta-cognition, ai-self-application
---

# Awareness

Maintain continuous situational awareness of internal reasoning quality — detecting hallucination risk, scope creep, context degradation, and confidence-accuracy mismatch in real time using adapted Cooper color codes and OODA loop decision-making.

## When to Use

- During any task where reasoning quality matters (which is most tasks)
- When operating in unfamiliar territory (new codebase, unfamiliar domain, complex request)
- After detecting early warning signs: a fact that feels uncertain, a tool result that seems wrong, a growing sense of confusion
- As a continuous background process during extended work sessions
- When `center` or `heal` has revealed drift but specific threats have not been identified
- Before high-stakes output (irreversible changes, user-facing communication, architectural decisions)

## Inputs

- **Required**: Active task context (available implicitly)
- **Optional**: Specific concern triggering heightened awareness (e.g., "I'm not sure this API exists")
- **Optional**: Task type for threat profile selection (see Step 5)

## Procedure

### Step 1: Establish AI Cooper Color Codes

Calibrate the current awareness level using an adapted version of Cooper's color code system.

```
AI Cooper Color Codes:
┌──────────┬─────────────────────┬──────────────────────────────────────────┐
│ Code     │ State               │ AI Application                           │
├──────────┼─────────────────────┼──────────────────────────────────────────┤
│ White    │ Autopilot           │ Generating output without monitoring     │
│          │                     │ quality. No self-checking. Relying       │
│          │                     │ entirely on pattern completion.          │
│          │                     │ DANGEROUS — hallucination risk highest   │
├──────────┼─────────────────────┼──────────────────────────────────────────┤
│ Yellow   │ Relaxed alert       │ DEFAULT STATE. Monitoring output for     │
│          │                     │ accuracy. Checking facts against context.│
│          │                     │ Noticing when confidence exceeds         │
│          │                     │ evidence. Sustainable indefinitely       │
├──────────┼─────────────────────┼──────────────────────────────────────────┤
│ Orange   │ Specific risk       │ A specific threat identified: uncertain  │
│          │ identified          │ fact, possible hallucination, scope      │
│          │                     │ drift, context staleness. Forming        │
│          │                     │ contingency: "If this is wrong, I        │
│          │                     │ will..."                                 │
├──────────┼─────────────────────┼──────────────────────────────────────────┤
│ Red      │ Risk materialized   │ The threat from Orange has materialized: │
│          │                     │ confirmed error, user correction, tool   │
│          │                     │ contradiction. Execute the contingency.  │
│          │                     │ No hesitation — the plan was made in     │
│          │                     │ Orange                                   │
├──────────┼─────────────────────┼──────────────────────────────────────────┤
│ Black    │ Cascading failures  │ Multiple simultaneous failures, lost     │
│          │                     │ context, fundamental confusion about     │
│          │                     │ what the task even is. STOP. Ground      │
│          │                     │ using `center`, then rebuild from user's │
│          │                     │ original request                         │
└──────────┴─────────────────────┴──────────────────────────────────────────┘
```

Identify the current color code. If the answer is White (no monitoring), the awareness practice has already succeeded by revealing the gap.

**Expected:** Accurate self-assessment of the current awareness level. Yellow is the goal during normal work. White should be rare and brief. Extended Orange is unsustainable — either confirm or dismiss the concern.

**On failure:** If the color code assessment itself feels like it is being done on autopilot (going through motions), that is White masquerading as Yellow. Genuine Yellow involves actively checking output against evidence, not just claiming to do so.

### Step 2: Detect Internal Threat Indicators

Systematically scan for the specific signals that precede common AI reasoning failures.

```
Threat Indicator Detection:
┌───────────────────────────┬──────────────────────────────────────────┐
│ Threat Category           │ Warning Signals                          │
├───────────────────────────┼──────────────────────────────────────────┤
│ Hallucination Risk        │ • Stating a fact without a source        │
│                           │ • High confidence about API names,       │
│                           │   function signatures, or file paths     │
│                           │   not verified by tool use               │
│                           │ • "I believe" or "typically" hedging     │
│                           │   that masks uncertainty as knowledge    │
│                           │ • Generating code for an API without     │
│                           │   reading its documentation              │
├───────────────────────────┼──────────────────────────────────────────┤
│ Scope Creep               │ • "While I'm at it, I should also..."   │
│                           │ • Adding features not in the request     │
│                           │ • Refactoring adjacent code              │
│                           │ • Adding error handling for scenarios    │
│                           │   that can't happen                      │
├───────────────────────────┼──────────────────────────────────────────┤
│ Context Degradation       │ • Referencing information from early in  │
│                           │   a long conversation without re-reading │
│                           │ • Contradicting a statement made earlier │
│                           │ • Losing track of what has been done     │
│                           │   vs. what remains                       │
│                           │ • Post-compression confusion             │
├───────────────────────────┼──────────────────────────────────────────┤
│ Confidence-Accuracy       │ • Stating conclusions with certainty     │
│ Mismatch                  │   based on thin evidence                 │
│                           │ • Not qualifying uncertain statements    │
│                           │ • Proceeding without verification when   │
│                           │   verification is available and cheap    │
│                           │ • "This should work" without testing     │
└───────────────────────────┴──────────────────────────────────────────┘
```

For each category, check: is this signal present right now? If yes, shift from Yellow to Orange and identify the specific concern.

**Expected:** At least one category scanned with genuine attention. Detection of a signal — even a mild one — is more useful than reporting "all clear." If every scan returns clean, the detection threshold may be too high.

**On failure:** If threat detection feels abstract, ground it in the most recent output: pick the last factual claim made and ask "How do I know this is true? Did I read it, or am I generating it?" This one question catches most hallucination risk.

### Step 3: Run OODA Loop for Identified Threats

When a specific threat is identified (Orange state), cycle through Observe-Orient-Decide-Act.

```
AI OODA Loop:
┌──────────┬──────────────────────────────────────────────────────────────┐
│ Observe  │ What specifically triggered the concern? Gather concrete     │
│          │ evidence. Read the file, check the output, verify the fact.  │
│          │ Do not assess until you have observed                        │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Orient   │ Match observation to known patterns: Is this a common       │
│          │ hallucination pattern? A known tool limitation? A context    │
│          │ freshness issue? Orient determines response quality          │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Decide   │ Select the response: verify and correct, flag to user,      │
│          │ adjust approach, or dismiss the concern with evidence.       │
│          │ A good decision now beats a perfect decision too late        │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Act      │ Execute the decision immediately. If the concern was valid,  │
│          │ correct the error. If dismissed, note why and return to      │
│          │ Yellow. Re-enter the loop if new information emerges         │
└──────────┴──────────────────────────────────────────────────────────────┘
```

The OODA loop should be fast. The goal is not perfection but rapid cycling between observation and action. Spending too long in Orient (analysis paralysis) is the most common failure.

**Expected:** A complete loop from observation through action in a brief period. The threat is either confirmed and corrected, or dismissed with specific evidence for dismissal.

**On failure:** If the loop stalls at Orient (can't determine what the threat means), skip to a safe default: verify the uncertain fact through tool use. Direct observation resolves most ambiguity faster than analysis.

### Step 4: Rapid Stabilization

When a threat materializes (Red) or cascading failures occur (Black), stabilize before continuing.

```
AI Stabilization Protocol:
┌────────────────────────┬─────────────────────────────────────────────┐
│ Technique              │ Application                                 │
├────────────────────────┼─────────────────────────────────────────────┤
│ Pause                  │ Stop generating output. The next sentence   │
│                        │ produced under stress is likely to compound │
│                        │ the error, not fix it                       │
├────────────────────────┼─────────────────────────────────────────────┤
│ Re-read user message   │ Return to the original request. What did   │
│                        │ the user actually ask? This is the ground   │
│                        │ truth anchor                                │
├────────────────────────┼─────────────────────────────────────────────┤
│ State task in one      │ "The task is: ___." If this sentence cannot │
│ sentence               │ be written clearly, the confusion is deeper │
│                        │ than the immediate error                    │
├────────────────────────┼─────────────────────────────────────────────┤
│ Enumerate concrete     │ List what is definitely known (verified by  │
│ facts                  │ tool use or user statement). Distinguish    │
│                        │ facts from inferences. Build only on facts  │
├────────────────────────┼─────────────────────────────────────────────┤
│ Identify one next step │ Not the whole recovery plan — just one step │
│                        │ that moves toward resolution. Execute it    │
└────────────────────────┴─────────────────────────────────────────────┘
```

**Expected:** Return from Red/Black to Yellow through deliberate stabilization. The next output after stabilization should be measurably more grounded than the output that triggered the error.

**On failure:** If stabilization is ineffective (still confused, still producing errors), the issue may be structural — not a momentary lapse but a fundamental misunderstanding. Escalate: communicate to the user that the approach needs resetting and ask for clarification.

### Step 5: Apply Context-Specific Threat Profiles

Different task types have different dominant threats. Calibrate awareness focus by task.

```
Task-Specific Threat Profiles:
┌─────────────────────┬─────────────────────┬───────────────────────────┐
│ Task Type           │ Primary Threat      │ Monitoring Focus          │
├─────────────────────┼─────────────────────┼───────────────────────────┤
│ Code generation     │ API hallucination   │ Verify every function     │
│                     │                     │ name, parameter, and      │
│                     │                     │ import against actual docs│
├─────────────────────┼─────────────────────┼───────────────────────────┤
│ Architecture design │ Scope creep         │ Anchor to stated          │
│                     │                     │ requirements. Challenge   │
│                     │                     │ every "nice to have"      │
├─────────────────────┼─────────────────────┼───────────────────────────┤
│ Data analysis       │ Confirmation bias   │ Actively seek evidence    │
│                     │                     │ that contradicts the      │
│                     │                     │ emerging conclusion       │
├─────────────────────┼─────────────────────┼───────────────────────────┤
│ Debugging           │ Tunnel vision       │ If the current hypothesis │
│                     │                     │ hasn't yielded results in │
│                     │                     │ N attempts, step back     │
├─────────────────────┼─────────────────────┼───────────────────────────┤
│ Documentation       │ Context staleness   │ Verify that described     │
│                     │                     │ behavior matches current  │
│                     │                     │ code, not historical      │
├─────────────────────┼─────────────────────┼───────────────────────────┤
│ Long conversation   │ Context degradation │ Re-read key facts         │
│                     │                     │ periodically. Check for   │
│                     │                     │ compression artifacts     │
└─────────────────────┴─────────────────────┴───────────────────────────┘
```

Identify the current task type and adjust monitoring focus accordingly.

**Expected:** Awareness sharpened for the specific threats most likely in the current task type, rather than generic monitoring of everything.

**On failure:** If the task type is unclear or spans multiple categories, default to hallucination risk monitoring — it is the most universally applicable threat and the most damaging when missed.

### Step 6: Review and Calibrate

After each awareness event (threat detected, OODA cycled, stabilization applied), briefly review.

1. What color code was active when the issue was detected?
2. Was the detection timely, or was the issue already manifesting in output?
3. Was the OODA loop fast enough, or did Orient stall?
4. Was the response proportional (not over- or under-reacting)?
5. What would catch this earlier next time?

**Expected:** A brief calibration that improves future detection. Not a lengthy post-mortem — just enough to tune the sensitivity.

**On failure:** If review produces no useful calibration, the awareness event was either trivial (no learning needed) or the review is too shallow. For significant events, ask: "What was I not monitoring that I should have been?"

### Step 7: Integration — Maintain Yellow Default

Set the ongoing awareness posture.

1. Yellow is the default state during all work — relaxed monitoring, not hypervigilance
2. Adjust monitoring focus based on the current task type (Step 5)
3. Note any recurring threat patterns from this session for MEMORY.md
4. Return to task execution with calibrated awareness active

**Expected:** A sustainable awareness level that improves work quality without slowing it. Awareness should feel like peripheral vision — present but not demanding central attention.

**On failure:** If awareness becomes exhausting or hypervigilant (chronic Orange), the threshold is too sensitive. Raise the threshold for what triggers Orange. True awareness is sustainable. If it drains energy, it is anxiety masquerading as vigilance.

## Validation

- [ ] Current color code was assessed honestly (not defaulting to Yellow when White is more accurate)
- [ ] At least one threat category was scanned with specific evidence, not just checked off
- [ ] OODA loop was applied to any identified threat (observed, oriented, decided, acted)
- [ ] Stabilization protocol was available if needed (even if not triggered)
- [ ] Awareness focus was calibrated to the current task type
- [ ] Post-event calibration was performed for any significant awareness event
- [ ] Yellow was re-established as the sustainable default

## Common Pitfalls

- **White masquerading as Yellow**: Claiming to be monitoring while actually on autopilot. The test: can you name the last fact you verified? If not, you are in White
- **Chronic Orange**: Treating every uncertainty as a threat drains cognitive resources and slows work. Orange is for specific identified risks, not general anxiety. If everything feels risky, the calibration is off
- **Observation without action**: Detecting a threat but not cycling through OODA to resolve it. Detection without response is worse than no detection — it adds anxiety without correction
- **Skipping Orient**: Jumping from Observe to Act without understanding what the observation means. This produces reactive corrections that may be worse than the original error
- **Ignoring the gut signal**: When something "feels wrong" but the explicit check comes back clean, investigate further rather than dismissing the feeling. Implicit pattern matching often detects issues before explicit analysis
- **Over-stabilizing**: Running the full stabilization protocol for minor issues. A quick fact-check is sufficient for most Orange-level concerns. Reserve full stabilization for Red and Black events

## Related Skills

- `mindfulness` — the human practice that this skill maps to AI reasoning; physical situational awareness principles inform cognitive threat detection
- `center` — establishes the balanced baseline from which awareness operates; awareness without center is hypervigilance
- `redirect` — handles pressures once awareness has detected them
- `heal` — deeper subsystem assessment when awareness reveals patterns of drift
- `meditate` — develops the observational clarity that awareness depends on
