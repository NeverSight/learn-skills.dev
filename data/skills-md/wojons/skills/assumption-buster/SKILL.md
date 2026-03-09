---
name: assumption-buster
description: Aggressively challenge and attempt to disprove assumptions through counterexamples, edge cases, and adversarial thinking
license: MIT
compatibility: opencode
metadata:
  audience: developers, architects, security professionals
  category: critical-thinking
---

# Assumption Buster

Aggressively identify, challenge, and attempt to disprove assumptions through systematic counterexample generation, edge case exploration, and adversarial thinking to reveal hidden weaknesses and false beliefs.

## When to use me

Use this skill when:
- Critical decisions rely on untested assumptions
- Systems have high failure costs (safety, financial, reputation)
- You suspect team is suffering from confirmation bias
- Preparing for adversarial environments (security, competition, regulation)
- Testing resilience of core system beliefs
- Validating fundamental premises before major investments
- Challenging "industry best practices" that may not apply
- Stress-testing architectural decisions
- Preparing for audits, penetration tests, or regulatory reviews

## What I do

### 1. Assumption Aggression
- **Actively seek to disprove** rather than just test assumptions
- **Generate counterexamples** that break the assumption
- **Find edge cases** where assumption fails catastrophically
- **Identify contradiction patterns** in evidence
- **Pressure-test boundary conditions** until they break

### 2. Disproof Methodology
- **Attempt falsification** using Popperian scientific method
- **Search for black swans** - rare but catastrophic counterexamples
- **Construct stress scenarios** that maximize assumption failure
- **Apply Murphy's Law** - "anything that can go wrong, will"
- **Explore combinatorial explosions** of failure modes

### 3. Adversarial Testing
- **Think like an attacker** trying to break the system
- **Adopt competitor mindset** looking for weaknesses to exploit
- **Simulate hostile environments** (limited resources, malicious actors)
- **Test under extreme conditions** beyond design specifications
- **Provoke failure cascades** and ripple effects

### 4. Cognitive Bias Countermeasures
- **Target confirmation bias** by seeking disconfirming evidence
- **Challenge availability heuristic** by looking for rare cases
- **Counter anchoring effect** by exploring extreme values
- **Overcome overconfidence** with rigorous stress testing
- **Break groupthink** by introducing dissenting perspectives

## Assumption Busting Techniques

### For Technical Assumptions:
- **Load to failure**: "What load breaks this assumption?"
- **Resource starvation**: "What happens with minimal resources?"
- **Dependency failure**: "What if every dependency fails simultaneously?"
- **Version hell**: "What if all versions are mismatched?"
- **Data corruption**: "What if data is intentionally malformed?"

### For Business Assumptions:
- **Market reversal**: "What if customer preferences change overnight?"
- **Competitor innovation**: "What if a competitor solves this better/cheaper?"
- **Regulatory shock**: "What if regulations completely change?"
- **Economic collapse**: "What if funding disappears?"
- **Team dissolution**: "What if key people leave?"

### For Process Assumptions:
- **Communication breakdown**: "What if all communication fails?"
- **Tool failure**: "What if primary tools become unavailable?"
- **Knowledge loss**: "What if institutional knowledge disappears?"
- **Timeline compression**: "What if deadlines move up 90%?"
- **Quality erosion**: "What if quality standards steadily decline?"

## Examples

```bash
# Aggressively test a technical assumption
npm run assumption-buster:disprove -- --assumption "database-always-available" --method "chaos-engineering"

# Find counterexamples for a business assumption
npm run assumption-buster:counterexamples -- --assumption "users-prefer-mobile" --data "analytics-export.csv"

# Stress-test architectural decisions
npm run assumption-buster:stress-test -- --architecture "event-driven" --scenario "complete-network-partition"

# Generate failure scenarios for a process
npm run assumption-buster:failure-scenarios -- --process "ci-cd-pipeline" --intensity extreme

# Comprehensive assumption busting
npm run assumption-buster:all -- --criticality high --thoroughness maximum
```

## Output format

```
Assumption Busting Report
──────────────────────────────
Target: Payment Processing System
Assumptions Targeted: 14
Busting Duration: 2 hours
Busting Intensity: Aggressive

Assumption Busting Results:

1. Assumption: "Payment gateway responses always within 2 seconds"
   Status: ❌ BUSTED (Catastrophically)
   
   Counterexamples Found:
   - Network partition causes indefinite hangs (no timeout)
   - Gateway DDoS attack results in 30+ second responses
   - SSL certificate expiration causes silent failures
   - DNS poisoning redirects to malicious endpoints
   - Gateway vendor bankruptcy (no responses at all)
   
   Stress Test Results:
   - Under simulated attack: 85% of requests exceed 2 seconds
   - Failure cascade: timeouts cause thread pool exhaustion
   - Worst-case latency: 47 seconds (complete system stall)
   
   Impact if Believed:
   - Payment system becomes unresponsive during attacks
   - Financial losses from failed transactions
   - Customer trust destroyed
   - Recovery requires complete system restart
   
   Recommendation:
   Implement circuit breakers, aggressive timeouts, fallback providers

2. Assumption: "Users always complete checkout in single session"
   Status: ⚠️ PARTIALLY BUSTED (Significant weaknesses)
   
   Counterexamples Found:
   - Mobile network drops during payment (common)
   - Browser crashes after cart creation (frequent)
   - Users comparison shop across tabs (standard behavior)
   - Payment requires external verification (bank 2FA)
   - Users interrupted by real-world events (constant)
   
   Stress Test Results:
   - 41% of simulated users experience session-breaking events
   - Recovery rate without persistence: 12%
   - Data loss probability: 29%
   
   Impact if Believed:
   - Significant abandoned cart revenue loss
   - User frustration and negative reviews
   - Competitive disadvantage against persistent carts
   
   Recommendation:
   Implement cart persistence, resume functionality, email reminders

3. Assumption: "Fraud detection catches 99% of fraudulent transactions"
   Status: ❌ BUSTED (Dangerously false)
   
   Counterexamples Found:
   - New fraud patterns not in training data (always emerging)
   - Low-and-slow attacks evade threshold detection
   - Synthetic identity fraud has no historical patterns
   - Insider threats bypass external detection
   - Collusion attacks distribute suspicious activity
   
   Adversarial Testing Results:
   - Simulated novel fraud: 67% detection rate (not 99%)
   - Adaptive attackers: detection degrades over time
   - False positive rate forces threshold lowering
   - Detection latency allows transaction completion
   
   Impact if Believed:
   - Financial losses from undetected fraud
   - Regulatory penalties for inadequate controls
   - Reputation damage from fraud incidents
   
   Recommendation:
   Implement multi-layered fraud detection, continuous model updates

4. Assumption: "Database transactions always rollback on failure"
   Status: ✅ WITHSTOOD TESTING (But edge cases found)
   
   Stress Test Results:
   - Normal failures: proper rollback (assumption holds)
   - Edge Cases Discovered:
     * Connection pool exhaustion during rollback
     * Deadlock during distributed transaction cleanup
     * Storage engine corruption preventing rollback
     * Partial network failure leaving transactions dangling
   
   Recommendation:
   Implement transaction monitoring, orphan detection, manual cleanup procedures

Assumption Survival Rate:
- Completely Busted: 6 assumptions (43%)
- Partially Busted: 5 assumptions (36%)
- Withstood Testing: 3 assumptions (21%)

Critical Vulnerabilities Exposed:
1. Payment timeout handling (catastrophic failure possible)
2. Session persistence (significant revenue loss)
3. Fraud detection gaps (financial and regulatory risk)
4. Transaction cleanup (data consistency risk)

Busting Effectiveness Metrics:
- Novel failure modes discovered: 23
- Catastrophic scenarios identified: 7
- Previously unknown risks: 11
- Testing time vs value: Extremely high ROI
- Confidence adjustment: From 85% to 42% (more realistic)

Actionable Insights:
1. IMMEDIATE: Implement circuit breakers for payment gateway
2. HIGH PRIORITY: Add cart persistence and resume functionality
3. HIGH PRIORITY: Enhance fraud detection with behavioral analysis
4. MEDIUM PRIORITY: Add transaction monitoring and cleanup
5. MEDIUM PRIORITY: Create assumption registry with busting schedule

Next Busting Cycle Recommendations:
- Schedule: Monthly for critical assumptions
- Focus: New features and changed assumptions
- Method: Rotate between technical, business, process assumptions
- Participants: Include external perspectives for fresh eyes

Philosophical Notes:
- The assumptions that hurt most are those we don't know we're making
- A busted assumption is a gift - it reveals a hidden risk
- The goal isn't to prove assumptions wrong, but to find where they fail
- The most dangerous assumption is "our assumptions are mostly correct"
- Assumption busting creates antifragility - systems that improve when stressed
```

## Notes

- Assumption busting is intentionally aggressive - it tries to break things
- Balance between thorough busting and practical constraints
- Document both busted assumptions and those that withstand testing
- Use busting findings to improve systems, not just criticize them
- The value is in discovering unknown unknowns
- Some assumptions should remain (but now you know their limits)
- Busting creates knowledge about system boundaries and failure modes
- Share busting results transparently to build organizational learning
- Regular assumption busting prevents accumulation of false beliefs
- The best busting often comes from outsiders with different perspectives