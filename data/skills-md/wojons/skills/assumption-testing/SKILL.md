---
name: assumption-testing
description: Identify, document, and explicitly test assumptions rather than leaving them implicit and untested
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Assumption Testing

Identify, document, and explicitly test implicit assumptions in code, tests, design, and documentation to prevent failures caused by untested beliefs about how the system should work.

## When to use me

Use this skill when:
- Building new features with uncertain requirements
- Working with legacy code or undocumented systems
- Integrating with external systems or third-party services
- Designing complex algorithms or business logic
- Testing edge cases and boundary conditions
- Preparing for production deployment of critical features
- Debugging mysterious or intermittent failures
- Reviewing code or architecture designs
- Onboarding to a new codebase or system

## What I do

### 1. Assumption Discovery & Documentation
- **Scan code for implicit assumptions**:
  - Data format and validation assumptions
  - Dependency availability and behavior assumptions
  - Performance and resource availability assumptions
  - User behavior and interaction assumptions
  - Error handling and recovery assumptions
  - Time and timing-related assumptions
  - Security and authorization assumptions

- **Analyze tests for hidden assumptions**:
  - Test data assumptions (representative? comprehensive?)
  - Test environment assumptions (matches production?)
  - Test execution order assumptions (independent?)
  - Test assertion assumptions (complete? accurate?)
  - Test coverage assumptions (what's actually tested?)

- **Review design and documentation**:
  - Architectural assumptions (scalability, availability)
  - Integration assumptions (APIs, protocols, formats)
  - User experience assumptions (workflows, expectations)
  - Business logic assumptions (rules, calculations)
  - Operational assumptions (monitoring, maintenance)

### 2. Assumption Categorization & Prioritization
- **Categorize by risk and impact**:
  - Critical assumptions: Failure causes system failure
  - High-impact assumptions: Failure causes major issues
  - Medium-impact assumptions: Failure causes noticeable issues
  - Low-impact assumptions: Failure causes minor issues

- **Prioritize based on**:
  - Likelihood of assumption being wrong
  - Impact if assumption is wrong
  - Cost to test the assumption
  - Age and staleness of the assumption
  - Evidence supporting the assumption

### 3. Assumption Testing & Validation
- **Design explicit assumption tests**:
  - Boundary tests: What if assumption boundaries are exceeded?
  - Negation tests: What if the assumption is false?
  - Variation tests: What if assumption parameters vary?
  - Stress tests: What if assumption limits are pushed?
  - Reality checks: Does assumption match real-world behavior?

- **Execute assumption validation**:
  - Automated tests for testable assumptions
  - Manual verification for complex assumptions
  - Simulation and modeling for theoretical assumptions
  - User research for behavioral assumptions
  - Monitoring and observation for operational assumptions

### 4. Assumption Management & Communication
- **Document assumptions explicitly**:
  - Create assumption registry or catalog
  - Link assumptions to code and tests
  - Track assumption validation status
  - Document assumption sources and rationale

- **Communicate assumption risks**:
  - Share assumption catalog with team
  - Highlight critical untested assumptions
  - Recommend assumption testing priorities
  - Report assumption validation results

## Common Assumption Types to Test

### Technical Assumptions:
- "The database will always be available"
- "API responses will match the documented schema"
- "Network latency will never exceed 100ms"
- "Memory will always be sufficient for operations"
- "Third-party services will always respond within SLA"

### Business Logic Assumptions:
- "Users will always enter valid data"
- "Currency conversion rates will be available"
- "Business hours are 9-5 Monday-Friday"
- "Tax calculations follow current regulations"
- "Inventory levels are accurately tracked"

### User Experience Assumptions:
- "Users understand how to use this feature"
- "Mobile users have stable internet connections"
- "Users will notice and read error messages"
- "Users prefer this workflow over alternatives"
- "Accessibility requirements are being met"

### Operational Assumptions:
- "Monitoring will alert us of failures"
- "Backups are complete and restorable"
- "Scaling will handle peak traffic"
- "Security patches are applied promptly"
- "Documentation matches current implementation"

## Examples

```bash
# Discover assumptions in code
npm run assumption:discover -- --path src/payment/
npm run assumption:discover -- --type technical
npm run assumption:discover -- --type business-logic

# Document and categorize assumptions
npm run assumption:catalog -- --output assumptions.json
npm run assumption:prioritize -- --risk high

# Test specific assumptions
npm run assumption:test -- --assumption "database-always-available"
npm run assumption:test -- --assumption "api-schema-matches-docs"
npm run assumption:test -- --assumption "user-enters-valid-data"

# Comprehensive assumption testing
npm run assumption:test:all              # Test all documented assumptions
npm run assumption:test:critical         # Test only critical assumptions
npm run assumption:test:untested         # Test assumptions without validation

# Integration with other testing
npm run assumption:test:with -- --test-type chaos --assumption "system-resilient"
npm run assumption:test:with -- --test-type performance --assumption "scales-linearly"
npm run assumption:test:with -- --test-type security --assumption "no-unauthorized-access"

# Assumption management
npm run assumption:track -- --status validated     # Show validated assumptions
npm run assumption:track -- --status untested      # Show untested assumptions
npm run assumption:track -- --status risky         # Show high-risk assumptions
```

## Output format

```
Assumption Testing Report
──────────────────────────────
Scope: Payment Processing Module
Assumptions Discovered: 28
Assumptions Tested: 15 (priority order)
Testing Duration: 3 hours

Critical Assumption Test Results:

1. Assumption: "Payment gateway API always returns within 2 seconds"
   Location: src/payment/gateway.js:45-78
   Source: Initial implementation, never validated
   Risk: Critical (payment failures impact revenue)
   Test Strategy: Load testing + network simulation
   Result: ❌ ASSUMPTION FALSE
   - Gateway responses vary from 200ms to 8 seconds
   - 5% of requests exceed 2-second threshold
   - Timeouts occur during peak business hours
   Impact: Payment timeouts cause failed transactions
   Recommendation: Implement timeout handling and retry logic

2. Assumption: "Currency conversion rates are always available"
   Location: src/payment/currency.js:112-145
   Source: Third-party service documentation
   Risk: High (international payments fail)
   Test Strategy: Service failure simulation
   Result: ⚠️ PARTIALLY VALID
   - Rates available 99.5% of time
   - Service outages occur approximately 4 hours/month
   - No fallback mechanism implemented
   Impact: International payments fail during outages
   Recommendation: Add caching and fallback rate sources

3. Assumption: "Users always complete payment in single session"
   Location: src/payment/checkout.js:89-134
   Source: Initial user research (6 months old)
   Risk: Medium (abandoned carts, user frustration)
   Test Strategy: Analytics review + user testing
   Result: ❌ ASSUMPTION FALSE
   - 35% of users abandon and return later
   - Session timeout causes payment data loss
   - No save/resume functionality
   Impact: User frustration and lost revenue
   Recommendation: Implement payment session persistence

4. Assumption: "Fraud detection rules catch all fraudulent transactions"
   Location: src/payment/fraud.js:56-89
   Source: Third-party fraud service claims
   Risk: Critical (financial loss)
   Test Strategy: Historical data analysis + test transactions
   Result: ⚠️ PARTIALLY VALID
   - Catches 92% of known fraud patterns
   - Misses new fraud techniques
   - False positive rate: 1.2%
   Impact: Some fraud gets through, legitimate transactions declined
   Recommendation: Regular fraud rule review and updating

5. Assumption: "Database transactions always rollback on failure"
   Location: src/payment/processor.js:203-245
   Source: ORM documentation
   Risk: High (data inconsistency)
   Test Strategy: Failure injection testing
   Result: ✅ ASSUMPTION VALID
   - Transactions properly rollback on all tested failures
   - Database consistency maintained
   - Edge cases handled correctly
   Impact: None (assumption correct)
   Recommendation: Continue current implementation

Assumption Risk Summary:
  - Critical Assumptions: 8 total, 2 false, 3 partially valid, 3 valid
  - High Risk Assumptions: 12 total, 3 false, 4 partially valid, 5 valid
  - Medium Risk Assumptions: 6 total, 1 false, 2 partially valid, 3 valid
  - Low Risk Assumptions: 2 total, 0 false, 0 partially valid, 2 valid

False Assumption Impact Analysis:
  - Immediate Risks: Payment timeouts causing failed transactions
  - Short-term Risks: International payment failures during outages
  - Long-term Risks: Fraud gaps and user frustration
  - Financial Impact: Estimated $45,000/month in lost/recovered revenue
  - Reputation Impact: User trust erosion due to payment issues

Validation Coverage:
  - Technically testable assumptions: 85% validated
  - Business logic assumptions: 60% validated
  - User experience assumptions: 40% validated
  - Operational assumptions: 70% validated

Recommended Actions:
  1. High Priority: Fix payment timeout handling (critical risk)
  2. High Priority: Add currency rate fallback mechanism
  3. Medium Priority: Implement payment session persistence
  4. Medium Priority: Enhance fraud detection rule updates
  5. Low Priority: Document all validated assumptions

Assumption Testing ROI:
  - Testing time: 3 hours
  - Issues prevented: 4 critical assumptions found false
  - Potential cost savings: $540,000/year (estimated)
  - Risk reduction: Significant reduction in payment failures
  - Confidence increase: Much higher understanding of system limits
```

## Notes

- Assumption testing is most valuable when assumptions are implicit and untested
- Start with high-risk, high-impact assumptions
- Document assumptions as you discover them for future reference
- Re-test assumptions periodically as systems and contexts change
- Share assumption testing findings across the team
- Use assumption testing to inform design and architecture decisions
- Balance assumption testing effort with other testing activities
- Consider cultural and domain-specific assumptions
- Assumption testing complements other testing types but focuses on beliefs rather than specifications
- The most dangerous assumptions are those we don't know we're making
