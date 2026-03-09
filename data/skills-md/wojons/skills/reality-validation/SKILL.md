---
name: reality-validation
description: Compare system behavior against real-world expectations and domain knowledge rather than just technical specifications
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Reality Validation

Compare system behavior against real-world expectations, domain knowledge, and practical constraints rather than just technical specifications to ensure software makes sense in actual usage contexts.

## When to use me

Use this skill when:
- Building systems for complex real-world domains (finance, healthcare, logistics)
- Validating that technical solutions solve actual user problems
- Testing business logic against domain expert knowledge
- Ensuring data models match real-world entities and relationships
- Verifying that algorithms produce realistic and practical results
- Checking that user interfaces reflect real user workflows
- Validating reports and analytics against business reality
- Preparing for production deployment in mission-critical domains
- Debugging issues where technical correctness ≠ real-world correctness

## What I do

### 1. Domain Understanding & Context Building
- **Research real-world context**:
  - Study domain terminology, concepts, and relationships
  - Understand business processes and workflows
  - Learn about user roles, responsibilities, and goals
  - Identify constraints, regulations, and industry standards
  - Map real-world entities to system representations

- **Gather domain knowledge sources**:
  - Subject matter experts (SMEs) and stakeholders
  - Industry documentation and standards
  - Historical data and case studies
  - User observations and interviews
  - Competitor and market analysis
  - Regulatory and compliance requirements

### 2. Reality Gap Analysis
- **Compare system behavior to real-world expectations**:
  - Data validation: Does system data match real-world data patterns?
  - Process validation: Do workflows match actual business processes?
  - Calculation validation: Do calculations produce realistic results?
  - Timing validation: Do time-based behaviors match reality?
  - Scale validation: Does system scale match real-world volumes?
  - Edge case validation: Do edge cases reflect real-world scenarios?

- **Identify mismatches and anomalies**:
  - Technical correctness vs practical usefulness
  - Specification compliance vs real-world applicability
  - Algorithmic precision vs business acceptability
  - System limitations vs real-world requirements
  - Assumed user behavior vs actual user behavior

### 3. Reality-Based Testing
- **Test with real-world data**:
  - Production data samples (sanitized)
  - Historical transaction data
  - Real user scenarios and cases
  - Actual business events and conditions
  - Real-time data feeds and updates

- **Validate against domain expertise**:
  - Expert review of system outputs
  - SME validation of calculations and logic
  - User acceptance testing with real users
  - Business stakeholder verification
  - Regulatory compliance validation

- **Execute context-aware validation**:
  - Seasonal variation testing
  - Peak load and stress scenario testing
  - Geographic and regional variation testing
  - Market condition simulation
  - Regulatory change impact testing

### 4. Practical Correctness Assessment
- **Evaluate beyond technical correctness**:
  - Are results practically useful?
  - Do outputs make business sense?
  - Are workflows efficient in practice?
  - Is data quality sufficient for decision-making?
  - Does system support real user goals?

- **Assess real-world impact**:
  - Business value delivered vs expected
  - User satisfaction and adoption
  - Operational efficiency improvements
  - Risk reduction and compliance
  - Competitive advantage gained

## Reality Validation Areas

### Data & Model Validation:
- **Data patterns**: Do system data distributions match real-world distributions?
- **Entity relationships**: Do modeled relationships reflect real relationships?
- **Data quality**: Is data accurate, complete, and timely enough for real use?
- **Temporal patterns**: Do time-based behaviors match real-world timing?
- **Geographic patterns**: Do location-based behaviors make geographic sense?

### Process & Workflow Validation:
- **Business processes**: Do automated processes match manual processes?
- **User workflows**: Do system workflows support actual user tasks?
- **Decision points**: Do system decisions reflect real decision criteria?
- **Approval flows**: Do approval processes match organizational reality?
- **Exception handling**: Do exceptions reflect real exceptional situations?

### Calculation & Logic Validation:
- **Business calculations**: Do calculations produce business-valid results?
- **Pricing logic**: Does pricing match market reality and business strategy?
- **Risk assessments**: Do risk calculations reflect actual risk factors?
- **Forecasting**: Do forecasts align with historical patterns and expert expectations?
- **Optimization**: Do optimization results provide practical improvements?

### User Experience Validation:
- **User mental models**: Does UI match user understanding of the domain?
- **Workflow efficiency**: Do interfaces support efficient real work?
- **Information presentation**: Is information presented for practical use?
- **Decision support**: Does system help users make better real decisions?
- **Learning curve**: Can users apply domain knowledge to system use?

## Examples

```bash
# Domain-specific reality validation
npm run reality:validate -- --domain healthcare --system "patient-scheduling"
npm run reality:validate -- --domain finance --system "portfolio-management"
npm run reality:validate -- --domain ecommerce --system "inventory-management"

# Data reality validation
npm run reality:validate:data -- --dataset production-samples
npm run reality:validate:data -- --compare historical-actual
npm run reality:validate:data -- --expert-review business-analyst

# Process reality validation
npm run reality:validate:process -- --workflow "order-fulfillment"
npm run reality:validate:process -- --observe real-users
npm run reality:validate:process -- --compare manual-process

# Calculation reality validation
npm run reality:validate:calculations -- --expert finance-director
npm run reality:validate:calculations -- --compare industry-benchmarks
npm run reality:validate:calculations -- --test real-scenarios

# Integration with other testing
npm run reality:validate:with -- --test-type usability --focus "workflow-reality"
npm run reality:validate:with -- --test-type performance --focus "real-world-load"
npm run reality:validate:with -- --test-type security --focus "regulatory-compliance"

# Context-aware validation
npm run reality:validate:context -- --season holiday-peak
npm run reality:validate:context -- --market-condition recession
npm run reality:validate:context -- --geographic-region europe
npm run reality:validate:context -- --regulatory-environment gdpr
```

## Output format

```
Reality Validation Report
──────────────────────────────
Domain: Healthcare - Patient Appointment Scheduling
System: MedSchedule v2.1
Validation Method: Expert review + historical data analysis
Duration: 2 days

Data Reality Assessment:

1. Patient Appointment Duration Modeling:
   System Assumption: All appointments are 30 minutes
   Reality Check: ❌ MISMATCH FOUND
   - Historical data shows: 15% are 15min, 60% are 30min, 20% are 45min, 5% are 60min
   - Specialist appointments vary by department
   - Follow-up visits often shorter than initial consultations
   Impact: Schedule inefficiencies, doctor idle time, patient waiting
   Recommendation: Implement variable appointment durations by type

2. Doctor Availability Patterns:
   System Assumption: Doctors available 9-5, Monday-Friday
   Reality Check: ⚠️ PARTIAL MATCH
   - Reality: Varies by department (ER: 24/7, Surgery: 7-7, Clinic: 8-6)
   - Reality: Weekend and holiday coverage differs
   - Reality: On-call schedules not represented
   Impact: Appointment booking outside real availability
   Recommendation: Department-specific availability modeling

3. Patient No-Show Rate:
   System Assumption: Constant 10% no-show rate
   Reality Check: ❌ MISMATCH FOUND
   - Reality: Varies by department (5-25%)
   - Reality: Higher for Medicaid patients (18%)
   - Reality: Lower for established patients (7%)
   - Reality: Time-of-day and day-of-week patterns exist
   Impact: Schedule optimization ineffective, resource waste
   Recommendation: Dynamic no-show prediction model

Process Reality Assessment:

1. Appointment Rescheduling Workflow:
   System Design: Patient calls → receptionist checks availability → confirms
   Reality Check: ✅ GOOD MATCH
   - Matches observed clinic workflows
   - Receptionist role accurately modeled
   - Phone channel primary for rescheduling
   Impact: System supports actual process well

2. Emergency Appointment Handling:
   System Design: Treated as regular appointment with priority flag
   Reality Check: ❌ MISMATCH FOUND
   - Reality: ER has separate booking system
   - Reality: Urgent care uses walk-in model
   - Reality: True emergencies go to ER, not scheduled
   Impact: System doesn't support real emergency handling
   Recommendation: Separate emergency/urgent care workflow

3. Referral Process Integration:
   System Design: Doctor creates referral in system
   Reality Check: ⚠️ PARTIAL MATCH
   - Reality: Paper referrals still common (40% of cases)
   - Reality: Insurance pre-authorization often required
   - Reality: Specialist availability check happens separately
   Impact: Digital workflow incomplete, manual workarounds needed
   Recommendation: Integrate paper referral scanning and insurance checks

Calculation Reality Assessment:

1. Schedule Optimization Algorithm:
   System Output: Maximizes doctor utilization
   Reality Check: ❌ PRACTICALLY INVALID
   - Doctors report algorithm creates "inhuman" schedules
   - No buffer between patients for charting
   - Doesn't account for doctor preferences or energy patterns
   - Patient travel time between buildings not considered
   Impact: Algorithmically optimal but practically unusable
   Recommendation: Incorporate human factors and practical constraints

2. Wait Time Calculation:
   System Calculation: Based on schedule gaps
   Reality Check: ⚠️ INACCURATE
   - Reality: Actual wait times 2-3x calculated times
   - Reasons: Doctor running late, emergency interruptions, complex cases
   - Patients care about actual wait, not scheduled wait
   Impact: Patient dissatisfaction due to inaccurate expectations
   Recommendation: Implement actual wait time tracking and prediction

Expert Validation Results:
  - Clinical Director: "System doesn't understand real clinic workflow"
  - Head Nurse: "Missing critical nurse coordination aspects"
  - IT Director: "Technically sound but practically limited"
  - Patients: "Easy to use but schedules often inaccurate"

Business Impact Assessment:
  - Schedule Efficiency: Current 68%, Potential 85% with improvements
  - Patient Satisfaction: Current 3.2/5, Potential 4.5/5 with fixes
  - Doctor Utilization: Current 75%, Potential 82% with better modeling
  - Administrative Burden: Current high, Potential medium with improvements

Reality Gap Summary:
  - Major Gaps: 4 (critical impact on system usefulness)
  - Moderate Gaps: 6 (significant impact on efficiency)
  - Minor Gaps: 3 (noticeable but manageable)
  - Well Aligned: 5 aspects match reality well

Recommendations by Priority:
  1. High: Implement variable appointment durations
  2. High: Add emergency/urgent care workflow separation
  3. Medium: Develop dynamic no-show prediction
  4. Medium: Incorporate human factors in scheduling
  5. Low: Improve wait time calculation accuracy

Validation Confidence:
  - Data Alignment: Low (significant mismatches found)
  - Process Alignment: Medium (some mismatches, mostly aligned)
  - Calculation Alignment: Low (theoretically sound, practically weak)
  - Overall Reality Fit: Medium-Low (needs substantial improvements)

Next Steps:
  1. Schedule workshops with clinical staff to redesign key workflows
  2. Implement highest priority reality fixes before next release
  3. Establish ongoing reality validation process with domain experts
  4. Track reality alignment metrics over time
```

## Notes

- Reality validation requires deep domain understanding, not just technical skill
- Involve domain experts early and often
- Real-world data often contradicts assumptions and simplifications
- Technical elegance doesn't guarantee practical usefulness
- Balance theoretical correctness with practical constraints
- Different domains have different reality validation needs
- Reality changes over time - validation should be ongoing
- Document reality gaps and their business impacts clearly
- Use reality validation to bridge technical and business perspectives
- The most successful systems align closely with reality, not just specifications
- Reality validation often reveals that the real problem differs from the technical problem being solved
