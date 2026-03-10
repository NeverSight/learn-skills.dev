---
name: red-teaming
description: Apply red teaming whenever the user wants to stress-test a system, plan, architecture, security model, or decision against adversarial conditions — or when they want to find the weakest points before someone else does. Triggers on phrases like "where are the weak points?", "how would someone break this?", "is this secure?", "find the holes in this plan", "play devil's advocate", "what are we not seeing?", "challenge this", "attack this design", "where could this be exploited?", or when the user is about to launch or commit to something significant. Also trigger for any system where trust, security, incentives, or adversarial actors are relevant — don't wait for the user to ask for a red team explicitly.
---

# Red Teaming

**Core principle**: Assume the system will be attacked, gamed, or stressed by an intelligent adversary. Think like the attacker, not the designer. Find the weaknesses before they're exploited.

---

## Red Team Mindset

A red team actively **tries to break** the system — not to validate assumptions, but to invalidate them.

Key shifts:
- **Assume hostile intent**: How would a bad actor abuse this?
- **Assume failure**: Start from "this has failed" — what enabled it?
- **Assume partial information**: What does the adversary know that defenders don't?
- **Assume creativity**: Attackers aren't constrained by intended use
- **Asymmetry**: Defenders must protect everything; attackers only need one opening

---

## Red Team Dimensions

Apply adversarial thinking across these dimensions depending on what's being evaluated:

### 1. Technical Attack Surface
- What are the inputs to this system that could be manipulated?
- What assumptions about data validity are we making?
- What happens at edge cases, limits, or unexpected inputs?
- What trust boundaries exist, and can they be crossed?
- What does the failure mode look like under load, partial failure, or poisoned input?

### 2. Incentive & Game Theory Attacks
- Who has an incentive to game or subvert this system?
- What behavior does the incentive structure actually reward? (vs. what it intends to reward)
- If a rational actor wanted to extract maximum value while contributing minimum, how would they?
- Are there collusion risks between actors in the system?

### 3. Process & Human Attacks
- Where does the system rely on human judgment, discipline, or vigilance?
- What social engineering vectors exist?
- What happens when a trusted insider acts against the system?
- Where does ambiguity in the process allow inconsistent or exploitable behavior?

### 4. Assumption Attacks
- What must be true for this to work, and what if each assumption is false?
- What information asymmetry exists between parties?
- What dependencies exist that could be weaponized?

### 5. Cascade & Systemic Attacks
- What single failure propagates most widely?
- What is the highest-impact, lowest-effort attack?
- What would a sophisticated attacker do that a naive attacker wouldn't?
- What's the "kill chain" — the sequence of steps to cause catastrophic failure?

---

## Output Format

### 🎯 Attack Surface Map
Enumerate the surfaces available to an adversary:
- Entry points (inputs, interfaces, dependencies)
- Trust boundaries (where one actor's output becomes another's input)
- High-value targets (what would an attacker want to reach or damage?)

### 💀 Top Attack Scenarios
For each significant attack:
- **Name**: Short descriptive label
- **Actor**: Who would do this? (external attacker / insider / automated / accidental)
- **Method**: How exactly is it executed?
- **Impact**: What happens if it succeeds? (confidentiality / integrity / availability / reputation / financial)
- **Likelihood**: Low / Medium / High
- **Current defenses**: What prevents this now?
- **Defense gaps**: What's missing?

### 🏆 Highest-Risk Findings
Ranked by: **(Likelihood × Impact) / Existing Defenses**

The top 3 are the ones to fix first.

### 🔗 Kill Chain Analysis
For the most critical attack scenario, map the full kill chain:
```
[Initial access] → [Lateral movement] → [Exploitation] → [Impact]
```
At each step: What stops the attacker here? What's missing?

### 🛡️ Hardening Recommendations
For each high-risk finding:
- **Short-term mitigation** (reduce exposure now, even imperfectly)
- **Long-term fix** (eliminate or fundamentally reduce the attack surface)
- **Detection** (if prevention fails, how do we know we've been attacked?)

---

## Red Team Questions by Domain

### Software / Architecture
- What if the input is malformed, empty, enormous, or adversarially crafted?
- What if a dependency returns unexpected data or fails silently?
- What if two requests arrive simultaneously and race?
- What if a credential or token is leaked?
- What if a component is compromised from within?

### AI / Agent Systems
- What if the agent receives adversarially crafted input (prompt injection)?
- What if the agent's context is poisoned by a prior step?
- What if a tool the agent calls is compromised or returns false data?
- What if the agent is asked to perform an action outside its intended scope?
- What if two agents give conflicting instructions to a third?

### Product / Business
- What if a user tries to extract value without paying?
- What if a user reverse-engineers the system to game metrics?
- What if a competitor copies the model and undercuts pricing?
- What if a key partner defects or changes terms?
- What if regulatory conditions change?

### Organization / Process
- What if a key person leaves?
- What if incentives push people to hide information from each other?
- What if a process is followed to the letter but not the spirit?
- What if a deadline creates pressure to skip safeguards?

---

## Red Team Levels of Depth

| Level | Description | When to Use |
|-------|-------------|-------------|
| **Opportunistic** | Surface-level checks, low effort | Quick validation, early design |
| **Systematic** | Full attack surface enumeration | Pre-launch, major architecture changes |
| **Adversarial** | Deep creative attack — think like a sophisticated threat actor | High-stakes systems, security-critical features |

---

## Key Principle: Asymmetric Paranoia
The red team doesn't need to find every flaw. It needs to find **the one flaw that matters most**. Always prioritize: *What is the highest-impact attack that currently has no defense?*
