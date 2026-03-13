---
name: ai-native-product
description: This skill should be used when the user needs to build AI-native products with agency-control tradeoffs, calibration loops, and eval strategies. Use when building AI agents, LLM features, or products where AI handles user tasks autonomously. Part of the Modern Product Operating Model collection.
license: MIT
---

# AI-Native Product Development

> "AI products aren't deterministic. They require continuous calibration, not just A/B tests."

This skill covers **AI-Native Product Development** — the overlay that modifies discovery, architecture, and delivery when AI is at the core. It addresses the unique challenges of building products where AI agents perform tasks autonomously.


**Related skills**: `product-strategy`, `product-discovery`, `product-architecture`, `product-delivery`, `product-leadership`

---

## When to Use This Skill

Use this skill when:
- Building AI agents that act on behalf of users
- Adding LLM-powered features to existing products
- Designing human-AI interaction patterns
- Deciding how much autonomy to give AI
- Setting up eval strategies and calibration loops
- Managing the "agency-control tradeoff"

**Not needed for**: Traditional software products, ML models used only for backend optimization (no user-facing autonomy)

---

## Progress Tracking

Display progress during AI-native product work:

```
[████░░░░░░░░░░░░░░░░] 25% — Phase 1/4: Agency-Control Tradeoff Design
[████████░░░░░░░░░░░░] 50% — Phase 2/4: Discovery & Assumption Mapping
[████████████░░░░░░░░] 75% — Phase 3/4: Eval Strategy & Calibration Loop
[████████████████████] 100% — Phase 4/4: Delivery, Monitoring & Trust-Building
```

---

## What Makes AI Products Different

### Traditional Software vs. AI Products

| Dimension | Traditional Software | AI-Native Products |
|-----------|---------------------|-------------------|
| **Behavior** | Deterministic | Probabilistic |
| **Testing** | Unit tests, QA | Evals, calibration |
| **Correctness** | Binary (works or doesn't) | Spectrum (good enough?) |
| **User role** | Operator | Delegator + Reviewer |
| **Failure mode** | Error messages | Plausible but wrong outputs |
| **Iteration** | Ship → Measure → Iterate | Ship → Observe → Calibrate |
| **Trust building** | Feature completeness | Demonstrated reliability |

### The Core Challenge

AI products must navigate a fundamental tension:

**More autonomy** = More value (fewer steps, faster outcomes)  
**More autonomy** = More risk (errors affect real work)

This is the **Agency-Control Tradeoff**.

---

## Framework: The CCCD Loop

> Credit: Aishwarya Goel & Kiriti Gavini

AI products require a **Continuous Calibration and Confidence Development (CCCD)** loop:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CCCD LOOP                                │
│                                                                 │
│    CALIBRATE → CONFIDENCE → CONTINUOUS DISCOVERY → CALIBRATE   │
│         ↓           ↓              ↓                 ↓         │
│     Eval and    Build user    Observe AI       Update evals    │
│     adjust AI    trust over   interactions     and models      │
│     behavior     time         at scale                         │
└─────────────────────────────────────────────────────────────────┘
```

**CCCD Components:**

| Component | Purpose | Activities |
|-----------|---------|------------|
| **Calibrate** | Tune AI behavior to match user expectations | Run evals, adjust prompts/models, set guardrails |
| **Confidence** | Build appropriate user trust | Show AI reasoning, enable verification, demonstrate reliability |
| **Continuous Discovery** | Observe AI-user interactions at scale | Log interactions, identify failure patterns, surface edge cases |
| **→ Back to Calibrate** | Update based on learnings | Improve evals, retrain, adjust prompts |

---

## The Agency-Control Progression

### Five Levels of AI Agency

| Level | Description | AI Does | User Does | Example |
|-------|-------------|---------|-----------|---------|
| **1. Assist** | AI suggests, user executes | Generates options | Chooses and acts | Autocomplete, suggestions |
| **2. Recommend** | AI ranks, user approves | Analyzes and recommends | Reviews and approves | "AI recommends these 3 actions" |
| **3. Execute with confirmation** | AI acts after approval | Prepares action | Confirms before execution | "Send this email?" → Yes/No |
| **4. Execute with notification** | AI acts, notifies after | Acts autonomously | Reviews outcomes | "I scheduled the meeting and sent invites" |
| **5. Fully autonomous** | AI acts without notification | Handles end-to-end | Sets goals, reviews exceptions | AI handles routine tasks silently |

### Progression Strategy

**Start lower, earn higher:**

```
Level 1 → Build trust → Level 2 → Demonstrate reliability → Level 3 → ...
```

**Graduation Criteria:**

| From Level | To Level | Requires |
|------------|----------|----------|
| 1 → 2 | Assist → Recommend | User accepts suggestions > 70% |
| 2 → 3 | Recommend → Execute with confirm | User approves recommendations > 80% |
| 3 → 4 | Execute+confirm → Execute+notify | User confirms without edit > 90% |
| 4 → 5 | Execute+notify → Autonomous | User overrides < 5%, high-stakes scenarios excluded |

**Never fully autonomous for:**
- Irreversible actions (delete, send, purchase)
- High-stakes decisions (financial, legal, health)
- Novel situations outside training distribution
- Actions affecting third parties

---

## AI-Native Discovery

Standard discovery practices need adaptation for AI products.

### Modified Discovery Focus

| Standard Discovery | AI-Native Adaptation |
|-------------------|----------------------|
| "What job are you trying to do?" | + "How much do you want to delegate?" |
| "What's your current workflow?" | + "Which steps are you comfortable AI handling?" |
| "What would success look like?" | + "What errors would be unacceptable?" |
| "Show me how you do this today" | + "Show me how you verify AI work today" |

### AI-Specific Discovery Questions

**Delegation appetite:**
- "Which parts of this task feel tedious vs. require your judgment?"
- "If AI made an error here, what would the consequences be?"
- "How would you want to verify AI's work?"

**Trust calibration:**
- "What would AI need to demonstrate before you'd trust it to [action]?"
- "Have you used AI tools before? What built or broke your trust?"
- "Would you prefer AI to do more but occasionally err, or do less perfectly?"

**Failure tolerance:**
- "What kinds of errors are annoying vs. damaging?"
- "How quickly do you need to catch and fix AI mistakes?"
- "What's your 'undo' option if AI gets it wrong?"

### Observing AI Interactions

In addition to interviews, AI discovery includes:

| Method | What to Look For |
|--------|------------------|
| **Session recordings** | Where do users override AI? Where do they accept blindly? |
| **Interaction logs** | Patterns in edits, rejections, corrections |
| **Feedback analysis** | Explicit signals (thumbs down, ratings) |
| **Support tickets** | AI-related complaints and confusion |

---

## AI-Native Architecture

### Solution Brief Additions

For AI features, add to standard solution brief:

```
AI-SPECIFIC SECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AGENCY LEVEL
Target: [Level 1-5]
Graduation path: [How might this evolve?]

FAILURE MODES
• [Failure mode 1]: [Consequence] → [Mitigation]
• [Failure mode 2]: [Consequence] → [Mitigation]

EVAL STRATEGY
• [Eval type 1]: [What we measure, how often]
• [Eval type 2]: [What we measure, how often]

CALIBRATION PLAN
• Initial calibration: [Approach]
• Ongoing calibration: [Cadence, triggers]

CONFIDENCE BUILDING
• How AI explains itself: [Approach]
• How users verify: [Mechanisms]
• Trust-building milestones: [Progression]
```

### AI Bet Categories

In addition to standard bet categories:

| Category | Description | Example |
|----------|-------------|---------|
| **Capability expansion** | AI can handle new task types | "AI can now summarize documents" |
| **Agency graduation** | Move to higher autonomy level | "AI sends emails without confirmation" |
| **Calibration improvement** | Better accuracy/reliability | "Reduce hallucination rate from 5% to 2%" |
| **Confidence building** | Better user trust | "Show AI reasoning before action" |
| **Guardrail strengthening** | Prevent harmful outputs | "Add content policy enforcement" |

---

## AI-Native Delivery

### Eval Strategy (Replaces Traditional Testing)

**Eval Types:**

| Eval Type | Purpose | When to Run |
|-----------|---------|-------------|
| **Unit evals** | Test specific capabilities | Every code change |
| **Behavioral evals** | Test end-to-end flows | Daily/weekly |
| **Adversarial evals** | Test edge cases and attacks | Before major releases |
| **Human evals** | Test subjective quality | Weekly sample |
| **Production evals** | Test on real traffic | Continuous |

**Eval Metrics:**

| Metric | What It Measures | Target |
|--------|------------------|--------|
| **Task success rate** | Does AI complete the intended task? | > 95% |
| **Factual accuracy** | Is output factually correct? | > 98% |
| **Hallucination rate** | Does AI make things up? | < 2% |
| **Harmful output rate** | Does AI produce unsafe content? | < 0.1% |
| **User acceptance rate** | Do users accept AI output? | > 80% |
| **Override rate** | How often do users correct AI? | < 15% |

**Eval Cadence:**

```
Code change → Unit evals (automated)
Daily → Behavioral evals (automated)
Weekly → Human evals (sample)
Release → Adversarial evals (red team)
Continuous → Production evals (monitoring)
```

### Staged Rollout for AI Features

AI features require more cautious rollout:

| Stage | Audience | Focus | Duration |
|-------|----------|-------|----------|
| **Internal** | Team | Find obvious failures | 1 week |
| **Alpha** | 5-10 trusted users | Qualitative feedback on AI behavior | 2 weeks |
| **Beta** | 5% of users | Quantitative eval metrics | 2-4 weeks |
| **Gradual GA** | 5% → 25% → 50% → 100% | Monitor at each stage | 4+ weeks |

**AI-Specific Rollout Gates:**

| Gate | Criteria to Proceed |
|------|---------------------|
| Alpha → Beta | Eval metrics above threshold, no harmful outputs |
| Beta → Gradual GA | User acceptance > 80%, override rate < 15% |
| Each GA increment | Metrics stable, no new failure modes |

### Calibration Loop

**Continuous calibration process:**

```
OBSERVE → IDENTIFY → CALIBRATE → VALIDATE → DEPLOY
   ↑                                           │
   └───────────────────────────────────────────┘
```

| Step | Activities | Cadence |
|------|------------|---------|
| **Observe** | Monitor production interactions, logs, feedback | Continuous |
| **Identify** | Surface failure patterns, edge cases, drift | Daily/weekly |
| **Calibrate** | Adjust prompts, fine-tune, add guardrails | As needed |
| **Validate** | Run evals on calibrated version | Before deploy |
| **Deploy** | Ship updates, continue observing | Staged |

**Calibration Triggers:**

- Eval metrics below threshold
- New failure pattern identified
- User feedback trend (negative)
- Model update available
- New use case discovered

### AI Metrics Hierarchy

```
LAGGING
├── User retention (AI users vs. non-AI users)
├── Task completion rate (with AI assist)
└── Revenue from AI features

CORE
├── User acceptance rate
├── Override rate
├── Time-to-completion (with AI)
└── User-reported satisfaction

LEADING
├── Eval metrics (accuracy, hallucination, etc.)
├── Interaction volume
├── Feature discovery rate
└── Feedback sentiment

GUARDRAILS
├── Harmful output rate
├── Latency P95
├── Error rate
└── Cost per interaction
```

---

## AI-Specific Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Ship and hope** | AI behavior drifts without monitoring | Continuous calibration |
| **Autonomous by default** | Users don't trust, don't adopt | Earn autonomy progressively |
| **Black box AI** | Users can't verify, won't trust | Show reasoning, enable verification |
| **No evals** | Quality degrades silently | Comprehensive eval strategy |
| **Ignore overrides** | Miss calibration signals | Override patterns inform calibration |
| **One-size-fits-all agency** | Different tasks need different levels | Task-specific agency levels |

---

## Templates

This skill includes templates in the `templates/` directory:
- `agency-assessment.md` — Determine appropriate agency level
- `eval-strategy.md` — Design eval suite for AI feature
- `calibration-plan.md` — Set up continuous calibration

---

## Using This Skill with Claude

Ask Claude to:

1. **Assess agency level**: "What agency level should [AI feature] have?"
2. **Design agency progression**: "Create a graduation path from assist to autonomous for [feature]"
3. **Identify failure modes**: "What could go wrong with [AI feature]? How do we mitigate?"
4. **Design eval strategy**: "Design an eval suite for [AI feature]"
5. **Plan calibration**: "Create a calibration plan for [AI feature]"
6. **Adapt discovery**: "What AI-specific questions should I ask in discovery for [use case]?"
7. **Design confidence building**: "How should [AI feature] show its reasoning?"
8. **Plan AI rollout**: "Create a staged rollout plan for [AI feature]"
9. **Set AI metrics**: "What metrics should we track for [AI feature]?"
10. **Review AI brief**: "Critique this solution brief for AI considerations"

---

## Connection to Other Skills

| When you need to... | Use skill |
|---------------------|-----------|
| Define overall product strategy | `product-strategy` |
| Run discovery (with AI adaptations) | `product-discovery` |
| Structure bets and roadmap | `product-architecture` |
| Plan rollout and metrics | `product-delivery` |
| Scale AI products across teams | `product-leadership` |

---

## Quick Reference: AI Product Checklist

Before shipping AI features:

- [ ] **Agency level defined** — Clear level for this feature
- [ ] **Graduation criteria set** — How we'll earn higher autonomy
- [ ] **Failure modes mapped** — Know what can go wrong
- [ ] **Evals in place** — Automated quality checks
- [ ] **Human evals scheduled** — Subjective quality review
- [ ] **Calibration loop running** — Continuous improvement process
- [ ] **Confidence mechanisms built** — Users can verify AI work
- [ ] **Guardrails active** — Prevent harmful outputs
- [ ] **Rollout staged** — More cautious than traditional features
- [ ] **Override tracking** — Learning from user corrections

---

## Sources & Influences

- **Aishwarya Goel & Kiriti Gavini** — CCCD Loop, Agency-Control Trade-off
- **Anthropic** — Constitutional AI, RLHF approaches
- **OpenAI** — Eval best practices
- **Google DeepMind** — AI safety frameworks

---

