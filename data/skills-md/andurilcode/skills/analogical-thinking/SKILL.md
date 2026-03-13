---
name: analogical-thinking
description: Apply analogical thinking whenever the user is designing a system, architecture, or process and would benefit from structural patterns that already exist in other domains — or when a problem feels novel but may have been solved elsewhere under a different name. Triggers on phrases like "how should we structure this?", "has anyone solved this before?", "we're designing from scratch", "what's a good model for this?", "I keep feeling like this resembles something", "what patterns apply here?", or when facing architecture, organizational, or process design decisions. Also trigger when a problem has been analyzed thoroughly but no good solution has emerged — the answer may exist in an adjacent domain. Don't reinvent what's been solved. Recognize the shape of the problem first.
---

# Analogical Thinking

**Core principle**: Most genuinely hard problems have structural analogues in other domains — often solved long ago, under a different name, by people who never heard of your field. The skill is recognizing the *shape* of a problem beneath its surface details, then transferring the solution structure across.

> The ctx harness as OS memory management. The blackboard pattern from speech recognition in 1977, re-emerging in multi-agent AI. TCP's congestion control as inspiration for rate-limiting. Evolution as a search algorithm.

---

## Why Analogical Thinking Works

Domains develop solutions to the same underlying problems independently. The surface vocabulary differs; the structural logic often doesn't. Cross-domain transfer is faster than derivation from scratch and produces solutions with decades of refinement already built in.

The risk is **false analogies** — surface similarity masking structural difference. This skill is as much about knowing when an analogy breaks as when it applies.

---

## The Core Process

### Step 1: Abstract the Problem Structure
Strip the domain-specific vocabulary. Describe the problem in structural terms:
- What needs to coordinate with what?
- What needs to be stored, retrieved, prioritized, transformed, routed?
- What's the flow? What are the constraints?
- What failure modes are you trying to prevent?

The more abstract the description, the wider the search space for analogues.

**Example**: "How do agents in Constellation share intermediate results without stepping on each other?"
Abstracted: *"Multiple concurrent writers need to contribute partial results to a shared workspace, with coordination to prevent conflicts and allow selective reading."*
→ Now this sounds like distributed systems, database concurrency, and collaborative document editing.

### Step 2: Search for Structural Analogues
With the abstract description, look for solved problems with the same structure across:

**Natural systems**: Evolution, immune response, neural networks, ant colonies, ecosystems, markets

**Engineering domains**: Civil, mechanical, electrical, chemical engineering — often have centuries of accumulated pattern

**Computer science classics**: OS design, compiler theory, networking protocols, database internals, distributed systems — extraordinarily rich source of solved problems

**Organizational theory**: Military command structures, jazz improvisation, surgical teams, air traffic control

**Biology**: Cell signaling, protein folding, predator-prey dynamics, homeostasis

**Physics / Information theory**: Entropy, signal/noise, conservation laws, phase transitions

### Step 3: Evaluate the Analogy's Strength
A structural analogy is useful when:
- The **relationships** between components map cleanly (not just the components themselves)
- The **constraints** are similar in kind (even if not in degree)
- The **failure modes** of the original domain are informative about yours

A structural analogy breaks when:
- Key properties of the original don't hold in your domain
- The scale is so different that emergent behaviors differ
- The analogy explains structure but not dynamics (or vice versa)

**Always ask**: *"Where does this analogy fail? What's different here that matters?"*

### Step 4: Transfer the Solution Pattern
Once a strong analogy is confirmed:
- What solution did the source domain develop?
- What's the core mechanism (not the implementation details)?
- What adaptations are needed for your domain's specific constraints?
- What refinements has the source domain accumulated over time that you can inherit?

---

## High-Value Source Domains for Technical/Organizational Work

### Operating Systems
Solved: resource allocation, memory management, process scheduling, concurrency, isolation, context switching, caching, virtual addressing.
→ Useful for: agent orchestration, multi-tenant systems, context management in LLMs, pipeline design.

### Distributed Systems
Solved: consensus under partial failure, eventual consistency, partition tolerance, idempotency, log-structured storage, leader election.
→ Useful for: multi-agent coordination, resilient pipelines, data synchronization.

### Ecology / Evolution
Solved: adaptation under selection pressure, niche differentiation, resource competition, co-evolution, resilience through diversity.
→ Useful for: adversarial systems, red team design, organizational adaptation, market strategy.

### Control Theory
Solved: feedback loops, stability, overshoot, damping, PID control, observability.
→ Useful for: system monitoring, auto-scaling, any system with goal-seeking behavior.

### Military / Logistics
Solved: command under uncertainty, supply chain under disruption, mission planning with incomplete information, combined arms coordination.
→ Useful for: incident response, large-scale project planning, agent coordination.

### Jazz / Improvisation
Solved: structured improvisation, real-time coordination without central control, shared vocabulary enabling emergence.
→ Useful for: team autonomy with alignment, agent behavior under ambiguity.

---

## Output Format

### 🔍 Abstracted Problem Structure
The problem re-stated in domain-neutral structural terms:
- Core relationship or dynamic
- Key constraints
- Failure modes being avoided

### 🔗 Structural Analogues Found
For each candidate analogy:
- **Source domain**: [Where this pattern comes from]
- **Analogue structure**: [How the source domain solved the structurally similar problem]
- **Fit assessment**: Strong / Partial / Weak
- **Where the analogy holds**: [Specific structural correspondences]
- **Where the analogy breaks**: [Key differences to watch]

### 🏗️ Transferred Solution Pattern
The core mechanism, adapted to your domain:
- What is the structure of the solution?
- What adaptations are needed?
- What accumulated refinements from the source domain are worth inheriting?
- What to avoid (failure modes the source domain already learned the hard way)?

### ⚠️ False Analogy Risks
- What surface similarity might suggest a stronger analogy than actually exists?
- What property of the original domain is assumed but doesn't hold here?

---

## Classic Analogies in Software / AI

| Problem | Source analogy | What transferred |
|---------|---------------|-----------------|
| Agent context management | OS virtual memory + paging | Active context = RAM; long-term storage = disk; page faults = context retrievals |
| Multi-agent coordination | Blackboard architecture (Hearsay-II, 1977) | Shared workspace, independent specialists reading/writing, no direct communication |
| LLM token limits | CPU cache hierarchy | Working memory vs. storage; cache misses as retrieval operations |
| Agent pipeline | Scientific method | Hypothesis → experiment → observation → update → repeat |
| Prompt compression | Data compression / entropy coding | Lossless vs. lossy; semantic entropy as the measure |
| AI red teaming | Security penetration testing | Adversarial mindset, kill chains, surface enumeration |

---

## Thinking Triggers

- *"What's the shape of this problem, stripped of its domain vocabulary?"*
- *"Who has solved a problem with this structure before, in any field?"*
- *"Where does this analogy feel strong? Where does it feel strained?"*
- *"What did the source domain learn the hard way, that we can inherit for free?"*
- *"If this were a networking problem / biology problem / physics problem, what would the answer look like?"*
