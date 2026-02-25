---
name: process-flowchart-designer
description: Create process flowcharts and workflow diagrams from descriptions, with optimization suggestions and bottleneck identification. Use when mapping processes, designing workflows, or improving operational efficiency.
---

# Process Flowchart Designer

Frameworks for translating business processes into clear visual diagrams, identifying inefficiencies, and designing optimized workflows.

## Flowchart Notation

### Standard Symbols

```
FLOWCHART SYMBOL REFERENCE:

  ┌─────────┐
  │ Rectangle│  = Process / Action step
  └─────────┘

  ◇ Diamond    = Decision point (Yes/No, True/False)

  ┌─────────┐
  │/ Parallel/│  = Parallelogram = Input/Output
  └─────────┘

  ( Oval )     = Start / End (Terminal)

  ┌─────────┐
  │ Cylinder │  = Database / Data store
  └─────────┘

  ┌─────────┐
  │ Document │  = Document / Report
  └~~~~~~~~~~┘

  ○ Circle     = Connector (links to another part)

  →  Arrow     = Flow direction
```

### Text-Based Flowchart Template

```
PROCESS FLOWCHART: [Process Name]
Version: [X.X]
Owner: [Department/Role]
Last Updated: [Date]

  ( START )
      │
      ▼
  ┌──────────────┐
  │ Step 1:       │
  │ [Action]      │
  └──────┬───────┘
         │
         ▼
     ◇ Decision?
    / \
  Yes   No
  │      │
  ▼      ▼
┌────┐ ┌────┐
│ A  │ │ B  │
└──┬─┘ └──┬─┘
   │      │
   └──┬───┘
      │
      ▼
  ( END )
```

## Process Mapping

### Process Documentation Template

```
PROCESS MAP: [Name]

METADATA:
  Process Owner:     [Name/Role]
  Department:        [Department]
  Frequency:         [Daily/Weekly/Monthly/Ad hoc]
  Average Duration:  [Time]
  Trigger:           [What initiates this process]
  Output:            [What the process produces]

STEPS:
  #  | Step Name          | Actor       | Action              | System/Tool | Duration | Notes
  ---|--------------------| ------------|----------------------|-------------|----------|------
  1  | [Name]             | [Role]      | [What they do]       | [Tool]      | [Time]   |
  2  | [Name]             | [Role]      | [What they do]       | [Tool]      | [Time]   |
  3  | DECISION: [Query]  | [Role]      | [Evaluate criteria]  | [Tool]      | [Time]   |
  3a | [If Yes]           | [Role]      | [Action]             | [Tool]      | [Time]   |
  3b | [If No]            | [Role]      | [Action]             | [Tool]      | [Time]   |
  4  | [Name]             | [Role]      | [What they do]       | [Tool]      | [Time]   |

HANDOFFS:
  From         → To           | Trigger              | Method
  [Role A]     → [Role B]     | [When]               | [Email/System/etc.]

EXCEPTIONS:
  Exception              | Handling Procedure       | Escalation Path
  [What can go wrong]    | [What to do]             | [Who to contact]
```

### SIPOC Diagram

```
SIPOC: [Process Name]

S - SUPPLIERS        I - INPUTS           P - PROCESS          O - OUTPUTS          C - CUSTOMERS
(Who provides?)      (What's needed?)     (High-level steps)   (What's produced?)   (Who receives?)

[Supplier 1]         [Input 1]            1. [Step]            [Output 1]           [Customer 1]
[Supplier 2]         [Input 2]            2. [Step]            [Output 2]           [Customer 2]
[Supplier 3]         [Input 3]            3. [Step]            [Output 3]           [Customer 3]
                     [Input 4]            4. [Step]
                                          5. [Step]

BOUNDARIES:
  Start: [Trigger event]
  End:   [Completion criteria]
```

## Workflow Optimization

### Bottleneck Identification

```
BOTTLENECK ANALYSIS: [Process Name]

For each step, evaluate:

Step | Duration | Wait Time | Handoff? | Rework Rate | Bottleneck Score
-----|----------|-----------|----------|-------------|------------------
1    | [time]   | [time]    | Yes/No   | [%]         | [1-10]
2    | [time]   | [time]    | Yes/No   | [%]         | [1-10]
3    | [time]   | [time]    | Yes/No   | [%]         | [1-10]

BOTTLENECK SCORING:
  Duration weight:    x3 (longest steps)
  Wait time weight:   x4 (idle time is waste)
  Handoff weight:     x2 (each handoff adds delay and error risk)
  Rework weight:      x5 (rework multiplies all other costs)

  Score = (Duration x 3) + (Wait x 4) + (Handoff x 2) + (Rework x 5)

TOP BOTTLENECKS (highest scores):
  1. Step [N]: [Description] — Score: [X]
     Root cause: [Why this step is slow/problematic]
     Recommendation: [How to fix]

  2. Step [N]: [Description] — Score: [X]
     Root cause: [Why]
     Recommendation: [Fix]
```

### Waste Identification (Lean)

| Waste Type | Definition | Signs | Solution |
|-----------|-----------|-------|----------|
| **Waiting** | Idle time between steps | Queues, backlogs | Parallel processing, SLAs |
| **Overprocessing** | Doing more than needed | Excessive approvals, gold-plating | Simplify, reduce sign-offs |
| **Rework** | Fixing errors | High rejection rate, loops | Error-proofing, validation |
| **Motion** | Unnecessary movement | Multiple systems, context switching | Consolidate tools |
| **Transport** | Moving information unnecessarily | Excessive handoffs | Direct routing |
| **Inventory** | Work piling up | Large queues at steps | Flow-based processing |
| **Overproduction** | Producing more than needed | Reports no one reads | Demand-driven output |
| **Defects** | Errors that reach downstream | Customer complaints | Quality at source |

### Process Improvement Template

```
IMPROVEMENT PROPOSAL: [Process Name]

CURRENT STATE:
  Total steps:          [N]
  Total duration:       [Time]
  Number of handoffs:   [N]
  Rework rate:          [%]
  Customer satisfaction: [Score]

PROPOSED CHANGES:
  Change #1: [Description]
    Current: [How it works now]
    Proposed: [How it will work]
    Impact: [Time saved / errors reduced / etc.]

  Change #2: [Description]
    Current: [How it works now]
    Proposed: [How it will work]
    Impact: [Time saved / errors reduced / etc.]

FUTURE STATE:
  Total steps:          [N] (was [N])
  Total duration:       [Time] (was [Time])
  Number of handoffs:   [N] (was [N])
  Rework rate:          [%] (was [%])
  Expected satisfaction: [Score]

IMPLEMENTATION:
  Phase 1: [Quick wins — Week 1-2]
  Phase 2: [System changes — Week 3-6]
  Phase 3: [Training and rollout — Week 7-8]
```

## Swimlane Diagrams

### Cross-Functional Process Map

```
SWIMLANE DIAGRAM: [Process Name]

                    TIME →
         ┌─────────────────────────────────────────┐
Customer │ (Request) ──→ [Wait] ──→ [Receive]      │
         ├─────────────────────────────────────────┤
Sales    │         [Review] ──→ [Approve] ──→       │
         ├─────────────────────────────────────────┤
Ops      │                    [Fulfill] ──→         │
         ├─────────────────────────────────────────┤
Finance  │                              [Invoice]   │
         └─────────────────────────────────────────┘

LEGEND:
  (  ) = External event
  [  ] = Process step
  ──→  = Flow direction
  Each row = one actor/department
```

### RACI Matrix

```
RACI MATRIX: [Process Name]

Task / Step              | Role A | Role B | Role C | Role D
-------------------------|--------|--------|--------|-------
1. [Step name]           | R      | A      | C      | I
2. [Step name]           | I      | R      | A      |
3. [Decision point]      | C      | R      | A      | I
4. [Step name]           | A      | I      | R      |

R = Responsible (does the work)
A = Accountable (approves / owns the outcome)
C = Consulted (provides input before)
I = Informed (notified after)

RULES:
  - Every task has exactly ONE "A"
  - Every task has at least one "R"
  - Minimize C's and I's (reduce communication overhead)
  - "A" should not also be "R" if possible (separation of duties)
```

## Decision Flow Design

### Decision Tree Template

```
DECISION TREE: [Decision Name]

Question 1: [First evaluation criterion]
  │
  ├── YES → Question 2a: [Follow-up]
  │         ├── YES → OUTCOME A: [Action/Result]
  │         └── NO  → OUTCOME B: [Action/Result]
  │
  └── NO  → Question 2b: [Alternative path]
            ├── YES → OUTCOME C: [Action/Result]
            └── NO  → OUTCOME D: [Action/Result]

DECISION CRITERIA:
  Criterion           | Threshold        | Data Source
  [What to evaluate]  | [Pass/fail line] | [Where to check]
```

### Escalation Matrix

```
ESCALATION MATRIX: [Process Name]

Severity | Definition              | Response Time | Escalation To    | Communication
---------|-------------------------|---------------|------------------|---------------
P1       | [Service down]          | 15 min        | [VP + On-call]   | All-hands alert
P2       | [Major degradation]     | 1 hour        | [Manager]        | Team channel
P3       | [Minor issue]           | 4 hours       | [Team lead]      | Ticket update
P4       | [Enhancement request]   | Next sprint   | [Product owner]  | Backlog
```

## Automation Assessment

### Automation Candidate Scoring

```
AUTOMATION ASSESSMENT: [Process Name]

For each step, score automation potential:

Step | Repetitive? | Rule-Based? | Digital? | Volume | Error Rate | Score
     | (1-5)       | (1-5)       | (1-5)    | (1-5)  | (1-5)      | (sum)
-----|-------------|-------------|----------|--------|------------|------
1    | [score]     | [score]     | [score]  | [score]| [score]    | [/25]
2    | [score]     | [score]     | [score]  | [score]| [score]    | [/25]

SCORING GUIDE:
  5 = Highly automatable (always the same, clear rules, fully digital)
  3 = Partially automatable (some variation, some judgment needed)
  1 = Not automatable (creative, subjective, requires human judgment)

RECOMMENDATIONS:
  Score 20-25: Automate fully (RPA, workflow automation)
  Score 15-19: Automate with human review checkpoints
  Score 10-14: Augment with tools (templates, checklists)
  Score 5-9:   Keep manual (human judgment essential)

TOP AUTOMATION CANDIDATES:
  1. Step [N]: Score [X]/25 — Tool: [Recommended tool]
  2. Step [N]: Score [X]/25 — Tool: [Recommended tool]
```

## Diagramming Tools Reference

| Tool | Type | Best For | Cost |
|------|------|----------|------|
| **Mermaid** | Code-based | Developers, version control | Free |
| **draw.io** | Visual editor | General business users | Free |
| **Lucidchart** | Cloud visual | Teams, collaboration | Freemium |
| **Figma/FigJam** | Collaborative | Design teams | Freemium |
| **Whimsical** | Simple visual | Quick wireframes | Freemium |
| **PlantUML** | Code-based | Developers, UML | Free |

### Mermaid.js Quick Reference

```
graph TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E
```

## See Also

- [Options Comparator](../options-comparator/SKILL.md)
- [Supply Chain Optimizer](../supply-chain-optimizer/SKILL.md)
- [Event Planner](../event-planner/SKILL.md)
