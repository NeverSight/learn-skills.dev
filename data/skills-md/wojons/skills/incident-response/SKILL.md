---
name: incident-response
description: Use when you need to manage incidents and conduct post-mortem analysis to improve system reliability and security
license: MIT
compatibility: opencode
metadata:
  audience: devops, security-engineers, incident-managers
  category: operations
---

# Incident Response

Manage incidents effectively and conduct comprehensive post-mortem analysis to improve system reliability, security, and operational excellence. This skill covers incident management processes, communication protocols, technical investigation, and blameless post-mortems.

## When to use me

Use this skill when:
- An incident occurs affecting system availability, performance, or security
- You need to establish or improve incident response processes
- You're conducting post-mortem analysis to prevent recurrence
- You need to coordinate cross-functional incident response teams
- You want to implement incident severity classification and escalation
- You need to document incidents and create actionable follow-up items
- You're building incident response playbooks and runbooks
- You want to improve mean time to detection (MTTD) and mean time to resolution (MTTR)
- You need to comply with incident reporting requirements (SLAs, regulatory)

## What I do

- **Incident severity classification**: Classify incidents by severity and impact
- **Incident coordination**: Coordinate cross-functional incident response teams
- **Communication management**: Manage incident communication (internal, external, stakeholders)
- **Technical investigation**: Conduct technical root cause analysis
- **Timeline reconstruction**: Reconstruct incident timeline
- **Impact assessment**: Assess business and technical impact
- **Remediation coordination**: Coordinate immediate remediation actions
- **Post-mortem facilitation**: Facilitate blameless post-mortem analysis
- **Action item tracking**: Track and monitor post-mortem action items
- **Process improvement**: Improve incident response processes based on learnings
- **Playbook development**: Develop and maintain incident response playbooks
- **Metrics and reporting**: Track incident metrics and generate reports

## Examples

```bash
# Start incident response process
./scripts/analyze-incident-response.sh --severity sev1 --type availability --start

# Conduct post-mortem analysis
./scripts/analyze-incident-response.sh --post-mortem --incident-id INC-2025-001 --output post-mortem.md

# Generate incident report
./scripts/analyze-incident-response.sh --report --incident-id INC-2025-001 --format pdf

# Analyze incident metrics
./scripts/analyze-incident-response.sh --metrics --period monthly --output metrics.json

# Develop incident playbook
./scripts/analyze-incident-response.sh --playbook --type security --output security-playbook.md
```

## Output format

```
Incident Response Analysis
─────────────────────────────────────
Incident ID: INC-2025-001
Severity: SEV-1 (Critical)
Type: Availability Incident
Start Time: 2025-01-15T02:30:00Z
Resolution Time: 2025-01-15T04:45:00Z
Duration: 2 hours 15 minutes

INCIDENT SUMMARY:
──────────────────
Title: Database cluster failover failure causing 100% API error rate
Impact: Complete service outage for all customers
Affected Systems: Primary database cluster, API services, customer applications
Root Cause: Automated failover script bug combined with network partition
Resolution: Manual failover to standby cluster, script fix, validation

SEVERITY CLASSIFICATION:
────────────────────────
Severity: SEV-1 (Critical)
Criteria:
• Customer Impact: 100% of customers affected
• Revenue Impact: Estimated $85,000/hour
• Service Level: SLA violation (99.95% target, actual 99.12%)
• Duration: 2 hours 15 minutes (> 5 minute target for SEV-1)

TIMELINE RECONSTRUCTION:
────────────────────────
02:30:00 - Monitoring alerts detect 100% API error rate
02:32:15 - Incident declared SEV-1, incident commander assigned
02:35:00 - Technical team begins investigation
02:45:00 - Identified database primary node failure
02:50:00 - Automated failover script fails due to bug
03:00:00 - Manual investigation reveals network partition
03:15:00 - Decision to perform manual failover to standby cluster
03:30:00 - Manual failover initiated
03:45:00 - Standby cluster promoted to primary
04:00:00 - Application connections redirected
04:15:00 - Service begins recovery
04:30:00 - 50% traffic restored
04:45:00 - 100% traffic restored, incident resolved

TECHNICAL INVESTIGATION:
─────────────────────────
Primary Cause: Automated failover script bug (line 245: incorrect condition check)
Contributing Factors:
1. Network partition between database nodes
2. Insufficient failover script testing
3. Lack of circuit breaker pattern in application connections
4. Monitoring gaps in failover process
5. Single point of failure in network configuration

Root Cause Analysis (5 Whys):
1. Why did service outage occur? Database primary node failed
2. Why did automatic failover not work? Failover script had bug
3. Why did bug exist in script? Insufficient testing of edge cases
4. Why insufficient testing? Test suite didn't include network partition scenarios
5. Why no network partition tests? Not considered in risk assessment

IMPACT ASSESSMENT:
───────────────────
Customer Impact:
• 100% of customers unable to access service
• 15,842 failed transactions
• 8,750 customer support tickets generated

Business Impact:
• Revenue loss: $191,250 (estimated)
• SLA credits: $42,500 (estimated)
• Reputation damage: Significant social media complaints

Technical Impact:
• 2 hours 15 minutes of complete outage
• 45 minutes of partial degradation
• Database corruption risk (mitigated by backups)

COMMUNICATION LOG:
───────────────────
02:35:00 - Internal alert: #incidents channel created
02:40:00 - Stakeholder notification: Executive team notified
02:45:00 - Status page update: Investigating increased error rates
03:00:00 - Customer notification: Email sent to enterprise customers
03:30:00 - Status page update: Identified issue, working on fix
04:00:00 - Status page update: Implementing fix, estimated recovery 60 minutes
04:30:00 - Status page update: Service recovering
04:50:00 - Status page update: Service restored, monitoring
05:00:00 - Post-mortem scheduled notification

REMEDIATION ACTIONS:
─────────────────────
Immediate (During Incident):
1. Manual failover to standby cluster (completed)
2. Application connection pool reset (completed)
3. Traffic redistribution (completed)

Short-term (24 hours):
1. Fix failover script bug (completed)
2. Enhance monitoring for failover events (in progress)
3. Update runbook with manual failover steps (in progress)
4. Review network configuration (scheduled)

Long-term (30 days):
1. Implement circuit breaker pattern in all services
2. Add network partition testing to test suite
3. Conduct failover drills quarterly
4. Implement chaos engineering for resilience testing
5. Review and update all automated failover scripts

POST-MORTEM ANALYSIS:
──────────────────────
What Went Well:
• Quick incident declaration and response
• Effective communication throughout incident
• Backup systems worked as designed
• Team coordination across time zones
• Documentation available and useful

What Could Be Improved:
• Automated failover reliability
• Testing coverage for edge cases
• Monitoring visibility into failover process
• Incident playbook completeness
• Stakeholder communication templates

Lessons Learned:
1. Automated systems require regular testing of failure scenarios
2. Network partitions must be considered in high-availability designs
3. Circuit breaker patterns are essential for resilient microservices
4. Regular failover drills build muscle memory for real incidents
5. Blameless culture enables honest post-mortem analysis

ACTION ITEMS:
─────────────
1. HIGH PRIORITY: Fix failover script bug and deploy to all environments
   Owner: Database Engineering
   Due: 2025-01-16
   Status: In Progress

2. HIGH PRIORITY: Implement circuit breaker pattern in API services
   Owner: Platform Engineering
   Due: 2025-01-30
   Status: Not Started

3. MEDIUM PRIORITY: Add network partition testing to test suite
   Owner: Quality Engineering
   Due: 2025-02-15
   Status: Not Started

4. MEDIUM PRIORITY: Update incident playbook with manual failover steps
   Owner: DevOps
   Due: 2025-01-20
   Status: In Progress

5. LOW PRIORITY: Conduct quarterly failover drills
   Owner: SRE
   Due: 2025-04-01 (recurring)
   Status: Scheduled

INCIDENT METRICS:
─────────────────
Mean Time To Detection (MTTD): 2 minutes 15 seconds
Mean Time To Acknowledgment (MTTA): 5 minutes
Mean Time To Resolution (MTTR): 2 hours 15 minutes
Mean Time Between Failures (MTBF): 45 days
Incident Count (30 days): 3
Severity Distribution: SEV-1: 1, SEV-2: 2, SEV-3: 0

PROCESS IMPROVEMENTS:
─────────────────────
1. Update incident severity classification guidelines
2. Implement automated incident timeline generation
3. Create stakeholder communication templates
4. Establish incident commander rotation
5. Implement incident metrics dashboard

RECOMMENDATIONS:
────────────────
1. Implement automated failover testing in CI/CD pipeline
2. Conduct chaos engineering exercises quarterly
3. Establish incident response training for all engineers
4. Implement service-level objectives (SLOs) and error budgets
5. Create incident severity playbooks for common scenarios

INCIDENT RESPONSE MATURITY ASSESSMENT:
───────────────────────────────────────
Current Level: 3/5 (Defined)
• Process: Defined incident response process
• People: Trained incident responders
• Technology: Basic incident management tools
• Culture: Blameless post-mortems established
• Metrics: Basic incident metrics tracked

Target Level: 4/5 (Managed)
• Process: Integrated incident response with DevOps
• People: Cross-functional incident response teams
• Technology: Advanced incident management platform
• Culture: Continuous learning from incidents
• Metrics: Comprehensive metrics with trend analysis
```

## Notes

- Incident response should follow a blameless culture focusing on systems and processes, not individuals
- Communication is critical during incidents; establish clear communication channels and protocols
- Post-mortems should be conducted within 48 hours of incident resolution while details are fresh
- Action items from post-mortems must be tracked to completion to prevent recurrence
- Incident metrics (MTTD, MTTA, MTTR) help measure and improve response effectiveness
- Regular incident response drills and tabletop exercises improve preparedness
- Incident severity classification should be based on business impact, not technical symptoms
- Documentation and runbooks should be living documents updated based on incident learnings
- Consider regulatory and compliance requirements for incident reporting and documentation
- Integrate incident response with change management and problem management processes