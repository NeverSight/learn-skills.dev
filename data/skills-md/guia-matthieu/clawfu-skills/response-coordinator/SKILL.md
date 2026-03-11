---
name: response-coordinator
description: Coordinate crisis response through structured playbooks, communication templates, and team orchestration
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Crisis Response Coordinator

> Orchestrate effective crisis response through structured playbooks, clear communication templates, and coordinated team actions.

## When to Use This Skill

- Active crisis situations
- Building crisis playbooks
- Training response teams
- Creating communication templates
- Post-crisis improvement

## Methodology Foundation

Based on **Burson-Marsteller crisis playbook** and **PPRR model** (Prevention, Preparedness, Response, Recovery), combining:
- Incident command structure
- Stakeholder communication
- Timeline management
- Documentation practices

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures response playbook | Go/no-go decisions |
| Drafts communications | Approval authority |
| Coordinates timelines | Resource deployment |
| Documents actions | Spokesperson selection |
| Suggests escalation paths | Legal implications |

## Instructions

### Step 1: Activate Crisis Protocol

**Activation Checklist:**
- [ ] Confirm crisis status (not false alarm)
- [ ] Identify crisis type and scope
- [ ] Assemble core response team
- [ ] Establish communication channels
- [ ] Begin documentation log

### Step 2: Establish Command Structure

**Crisis Team Roles:**

| Role | Responsibility | Typical Owner |
|------|----------------|---------------|
| **Crisis Lead** | Overall coordination | CEO/COO |
| **Comms Lead** | External messaging | CMO/PR Head |
| **Operations Lead** | Fix the problem | CTO/VP Ops |
| **Legal Counsel** | Legal guidance | General Counsel |
| **Customer Lead** | Customer communication | VP CX |
| **HR Lead** | Internal/employee | CHRO |

### Step 3: Execute Response

**Response Phases:**

| Phase | Duration | Focus |
|-------|----------|-------|
| **Contain** | 0-2 hours | Stop bleeding, assess scope |
| **Communicate** | 2-4 hours | Stakeholder notifications |
| **Resolve** | 4-24 hours | Fix root cause |
| **Recover** | 1-7 days | Return to normal |
| **Learn** | 7-30 days | Post-mortem, improvements |

### Step 4: Manage Communications

**Stakeholder Priority:**

| Stakeholder | When to Notify | Channel |
|-------------|----------------|---------|
| Internal team | Immediately | Slack/Teams |
| Board/Investors | Within 1 hour | Call/Email |
| Affected customers | Within 2 hours | Direct |
| All customers | Within 4 hours | Email/Social |
| Media | Reactive | Press statement |
| Public | As needed | Website/Social |

### Step 5: Document Everything

**Crisis Log Template:**
```
TIME | ACTION | OWNER | OUTCOME
-----|--------|-------|--------
10:00 | Alert received | [Name] | Verified
10:15 | Team assembled | [Name] | 5/6 present
10:30 | Root cause identified | [Name] | DB issue
...
```

## Examples

### Example 1: Crisis Response Playbook

**Input:**
```
Create a crisis response playbook for a data breach scenario.
```

**Output:**
```
## Crisis Playbook: Data Breach

### Severity Classification

| Level | Criteria | Response |
|-------|----------|----------|
| **Critical** | PII exposed, >10K records | Full activation |
| **High** | PII exposed, <10K records | Partial activation |
| **Medium** | Non-PII data exposed | Contained response |
| **Low** | Attempted breach, blocked | Monitor and report |

---

### Activation Trigger

**Automatic activation when:**
- Confirmed unauthorized data access
- Evidence of data exfiltration
- Regulatory notification required
- Media awareness possible

---

## Phase 1: CONTAIN (0-2 Hours)

### Immediate Actions

| Time | Action | Owner | Checklist |
|------|--------|-------|-----------|
| +0 min | Isolate affected systems | IT Security | [ ] |
| +0 min | Preserve forensic evidence | IT Security | [ ] |
| +15 min | Assemble crisis team | Crisis Lead | [ ] |
| +30 min | Brief team on situation | IT Security | [ ] |
| +30 min | Legal notification | Legal | [ ] |
| +1 hr | Scope assessment complete | IT Security | [ ] |
| +1 hr | Impact assessment complete | Ops Lead | [ ] |

### Crisis Team Assembly

**Mandatory Attendees:**
- [ ] CEO (Crisis Lead)
- [ ] CTO (Technical Lead)
- [ ] CISO (Security Lead)
- [ ] General Counsel (Legal Lead)
- [ ] CMO (Communications Lead)
- [ ] VP Customer Success (Customer Lead)

**Optional (as needed):**
- [ ] CHRO (if employee data)
- [ ] CFO (if financial impact)
- [ ] Board liaison

### Initial Assessment Template

```
BREACH ASSESSMENT
=================
Discovery Time: [TIME]
Breach Window: [START] to [END]

Data Involved:
- [ ] Names
- [ ] Email addresses
- [ ] Phone numbers
- [ ] Passwords
- [ ] Payment data
- [ ] SSN/Government ID
- [ ] Health information
- [ ] Other: ___________

Records Affected: [NUMBER]
Customers Affected: [NUMBER]

Attack Vector: [DESCRIPTION]
Current Status: [CONTAINED/ONGOING]
Confidence Level: [HIGH/MEDIUM/LOW]
```

---

## Phase 2: COMMUNICATE (2-4 Hours)

### Communication Sequence

| Priority | Stakeholder | When | Channel | Owner |
|----------|-------------|------|---------|-------|
| 1 | Board/Investors | +2hr | Call | CEO |
| 2 | Regulators | +2hr | Formal notice | Legal |
| 3 | Affected customers | +3hr | Email | CX Lead |
| 4 | All employees | +3hr | All-hands | HR |
| 5 | Media (if inquiries) | +4hr | Statement | Comms |
| 6 | Public | +4hr | Website | Comms |

---

### Communication Templates

#### Customer Notification (Direct Victims)

```
Subject: Important Security Notice - Action Required

Dear [Name],

We're writing to inform you about a security incident that may
have involved your personal information.

WHAT HAPPENED
On [DATE], we discovered unauthorized access to [SYSTEM].
The incident occurred between [DATE] and [DATE].

WHAT INFORMATION WAS INVOLVED
Based on our investigation, the following information may have
been accessed:
- [List specific data types]

WHAT WE'RE DOING
- We immediately secured our systems
- We engaged cybersecurity experts to investigate
- We notified law enforcement
- We are providing [credit monitoring/identity protection]

WHAT YOU CAN DO
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

CONTACT US
If you have questions, please contact our dedicated support line:
- Phone: [NUMBER] (24/7 for next 30 days)
- Email: [EMAIL]
- FAQ: [URL]

We sincerely apologize for this incident and any concern it causes.

[Signature]
```

#### All-Customer Notification

```
Subject: Security Update from [Company]

Dear [Customer],

We're writing with an important security update.

On [DATE], we discovered a security incident affecting some
customer accounts. We want to be transparent about what happened
and what we're doing.

THE INCIDENT
[2-3 sentence summary of what happened]

YOUR ACCOUNT
Based on our investigation, your account [was / was not] affected.
[If affected: See separate email with specific details]

OUR RESPONSE
- [Action taken 1]
- [Action taken 2]
- [Action taken 3]

GOING FORWARD
[Steps being taken to prevent future incidents]

We're deeply sorry this occurred and are committed to earning
back your trust.

[Signature]
```

#### Media Statement

```
STATEMENT FROM [COMPANY] REGARDING SECURITY INCIDENT

[DATE]

[Company] recently discovered unauthorized access to certain
company systems. Upon discovery, we immediately took steps to
secure our systems and engaged leading cybersecurity experts
to investigate.

Based on our investigation:
- [Key fact 1]
- [Key fact 2]
- [Key fact 3]

We have notified the appropriate authorities and are working
closely with law enforcement.

Affected individuals are being notified directly and we are
providing [specific remediation].

We take the security of our customers' information extremely
seriously. We apologize for this incident and are taking steps
to prevent similar incidents in the future.

For more information, please visit: [URL]

Media Contact: [Name], [Email]
```

---

## Phase 3: RESOLVE (4-24 Hours)

### Technical Remediation

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Patch vulnerability | Security | +6hr | [ ] |
| Reset affected credentials | IT | +8hr | [ ] |
| Deploy additional monitoring | Security | +12hr | [ ] |
| Third-party security audit | Security | +7 days | [ ] |

### Customer Remediation

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Credit monitoring enrollment | CX | +24hr | [ ] |
| Password reset flow | Product | +24hr | [ ] |
| Support surge staffing | CX | +24hr | [ ] |
| FAQ page live | Marketing | +6hr | [ ] |

---

## Phase 4: RECOVER (1-7 Days)

### Operational Recovery

| Milestone | Target | Owner |
|-----------|--------|-------|
| Normal operations | +24hr | Ops |
| Support queue normal | +72hr | CX |
| Security audit complete | +7 days | Security |
| All notifications sent | +72hr | Legal |

### Communication Recovery

| Activity | Timing | Owner |
|----------|--------|-------|
| Progress update #1 | +24hr | Comms |
| Progress update #2 | +72hr | Comms |
| Final resolution notice | +7 days | Comms |
| Thank you to customers | +14 days | CEO |

---

## Phase 5: LEARN (7-30 Days)

### Post-Incident Review

**Schedule within 7 days of resolution**

Agenda:
1. Timeline reconstruction
2. What worked well
3. What needs improvement
4. Action items for prevention
5. Communication effectiveness
6. Documentation updates

### Playbook Updates

Based on learnings, update:
- [ ] Detection capabilities
- [ ] Response procedures
- [ ] Communication templates
- [ ] Team training
- [ ] Vendor relationships
```

### Example 2: Real-Time Response Coordination

**Input:**
```
We're in the middle of a crisis - product recall needed.
Contaminated ingredient found in batch.
What do we do now?
```

**Output:**
```
## ACTIVE CRISIS: Product Recall

### STATUS: PHASE 1 - CONTAIN

---

### IMMEDIATE ACTIONS (Next 60 Minutes)

| # | Action | Owner | Done |
|---|--------|-------|------|
| 1 | STOP all shipments of affected batch | Operations | [ ] |
| 2 | Identify batch numbers affected | QC | [ ] |
| 3 | Pull from retail shelves (notify partners) | Sales | [ ] |
| 4 | Count units sold vs. in inventory | Operations | [ ] |
| 5 | Assemble full crisis team | CEO | [ ] |
| 6 | Contact legal counsel | CEO | [ ] |
| 7 | Notify regulatory authority (FDA/etc) | Legal | [ ] |

---

### INFORMATION NEEDED NOW

Fill in as you gather:

```
AFFECTED BATCH:
- Batch number(s): _______________
- Production date(s): _______________
- Contamination type: _______________
- Health risk level: [ ] Low [ ] Medium [ ] High [ ] Critical

DISTRIBUTION:
- Units produced: _______________
- Units shipped: _______________
- Units in warehouse: _______________
- Retailers received: _______________
- Units sold to consumers (est): _______________

CUSTOMERS AT RISK:
- Can you identify purchasers? [ ] Yes [ ] No
- Geographic distribution: _______________
```

---

### COMMUNICATION PRIORITY

| Priority | Who | When | Message |
|----------|-----|------|---------|
| 1 | Retail partners | NOW | Stop sales, pull from shelves |
| 2 | Regulatory body | Within 1hr | Formal notification |
| 3 | Identified customers | Within 2hr | Direct recall notice |
| 4 | All customers | Within 4hr | Public recall announcement |
| 5 | Media | As needed | Press statement ready |

---

### HOLDING STATEMENT (Use if media calls NOW)

```
"We are aware of an issue with [product] and are taking
immediate action. Customer safety is our top priority.
We will have a full statement within [X] hours.

In the meantime, customers who have purchased [product]
should [specific action].

Questions: [contact]"
```

---

### CUSTOMER COMMUNICATION TEMPLATE

```
URGENT PRODUCT RECALL NOTICE

[Company] is voluntarily recalling [Product Name] due to
potential contamination with [substance].

AFFECTED PRODUCTS:
- Product: [Name]
- Batch #: [Numbers]
- Expiration dates: [Dates]
- Sold at: [Retailers]

WHAT TO DO:
1. STOP using the product immediately
2. [Disposal instructions OR return instructions]
3. Contact us for full refund: [phone/email/url]

IF YOU'VE CONSUMED THE PRODUCT:
- [Symptoms to watch for]
- [When to seek medical attention]
- [Who to call]

We sincerely apologize for this situation and are taking
all steps to ensure this doesn't happen again.

Questions: [24/7 Hotline Number]
```

---

### NEXT CHECK-IN: 30 MINUTES

At that time, confirm:
- [ ] All shipments stopped
- [ ] Batch scope finalized
- [ ] Retail partners notified
- [ ] Regulatory notification sent
- [ ] Customer communication ready
```

## Skill Boundaries

### What This Skill Does Well
- Structuring response playbooks
- Creating communication templates
- Coordinating response timelines
- Organizing team actions

### What This Skill Cannot Do
- Make legal determinations
- Access your systems
- Speak on your behalf
- Know regulatory requirements

## Iteration Guide

**Follow-up Prompts:**
- "Create a playbook for [crisis type]"
- "Draft communication for [stakeholder]"
- "What should our next 30 minutes look like?"
- "How do we communicate [specific development]?"

## References

- Burson Crisis Communications
- PPRR Crisis Management Model
- FEMA Incident Command System
- Harvard Business Review Crisis Response

## Related Skills

- `crisis-detector` - Early warning
- `social-listening` - Monitoring
- `reputation-recovery` - Post-crisis

## Skill Metadata

- **Domain**: Crisis
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: Immediate in crisis
- **Prerequisites**: Stakeholder alignment, authority to act
