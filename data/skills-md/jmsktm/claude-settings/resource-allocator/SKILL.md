---
name: Resource Allocator
slug: resource-allocator
description: Optimize team resource allocation across projects with capacity planning and workload balancing
category: project
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "allocate resources"
  - "resource planning"
  - "assign resources"
  - "capacity planning"
  - "workload balance"
tags:
  - resources
  - capacity
  - allocation
  - planning
  - workload
  - optimization
---

# Resource Allocator

The Resource Allocator skill helps managers and team leads optimize how people, budget, and tools are allocated across projects and initiatives. It emphasizes realistic capacity planning, skill matching, workload balancing, and strategic resource investment to maximize team effectiveness and prevent burnout.

This skill excels at analyzing team capacity, mapping skills to project needs, identifying resource constraints and bottlenecks, balancing competing priorities, and creating sustainable allocation plans that respect team members' growth goals and work-life balance.

Resource Allocator follows modern people-first principles: sustainable pace over hero culture, skill development over pure efficiency, and transparent allocation over political negotiations.

## Core Workflows

### Workflow 1: Calculate Team Capacity

**Steps:**
1. **Identify Team Members**
   - List all people on team or available for allocation
   - Include roles, seniority, and areas of expertise
   - Note any upcoming PTO, holidays, or planned absences
   - Document part-time or contractor availability

2. **Calculate Individual Capacity**
   - Work hours per week: Typically 40 hours
   - Subtract non-project time:
     - Meetings (10-20%): 4-8 hours/week
     - Email/Slack (5-10%): 2-4 hours/week
     - Administrative (5-10%): 2-4 hours/week
     - Support rotation (varies): 0-8 hours/week
   - **Effective capacity**: ~60-70% of total hours
   - Example: 40 hours × 0.65 = 26 hours/week available for project work

3. **Adjust for Reality Factors**
   - **Onboarding**: New team members at 30-50% capacity for first month
   - **Context switching**: Multi-project allocation reduces efficiency 20-30%
   - **Technical debt**: Reserve 10-20% for maintenance and refactoring
   - **Bugs and support**: Reserve 10-30% depending on product maturity
   - **Learning time**: Reserve 5-10% for skill development

4. **Calculate Team Capacity**
   - Sum individual effective capacities
   - Account for skill distribution (not all hours are fungible)
   - Identify peak/low capacity periods (holidays, conference season)
   - Create capacity forecast for next 3-6 months

**Output:** Team capacity model with individual and aggregate availability.

### Workflow 2: Map Skills to Projects

**Steps:**
1. **Analyze Project Requirements**
   - List required skills for each project/initiative
   - Estimate hours needed per skill area
   - Identify if skills are readily available or scarce
   - Note learning curve for new technologies

2. **Create Skill Matrix**
   - Rows: Team members
   - Columns: Skills (React, API design, Database, DevOps, etc.)
   - Values: Proficiency level (1=Learning, 2=Competent, 3=Expert)

3. **Match Skills to Needs**
   - For each project, identify best-fit team members
   - Consider:
     - **Skill match**: Do they have required expertise?
     - **Interest**: Do they want to work on this?
     - **Growth**: Does this stretch them appropriately?
     - **Availability**: Do they have capacity?

4. **Identify Gaps**
   - Skills needed but no one has proficiency
   - Single points of failure (only one expert)
   - Training or hiring needs
   - Possible skill development opportunities

**Output:** Skill-based project staffing recommendations.

### Workflow 3: Create Resource Allocation Plan

**Steps:**
1. **List All Active Projects**
   - Include project name, priority, and timeline
   - Estimated total effort (person-weeks or hours)
   - Required start and end dates
   - Dependencies on other projects or teams

2. **Prioritize Projects**
   - Use strategic framework (OKRs, business value, etc.)
   - Force-rank if resources are constrained
   - Identify must-have vs. nice-to-have
   - Determine if any projects should be deferred or canceled

3. **Allocate Resources**
   - Assign team members to projects
   - Specify allocation percentage (50%, 100%, etc.)
   - Aim for:
     - **100% allocation**: One project per person (ideal)
     - **50/50 split**: Two projects max per person
     - **Avoid < 25%**: Too small to make meaningful progress

4. **Balance Workload**
   - Check that no one is over-allocated (>100%)
   - Ensure junior members have mentorship
   - Distribute challenging work fairly
   - Mix maintenance and greenfield work

5. **Timeline Validation**
   - Map allocation to project timelines
   - Identify resource contention or bottlenecks
   - Adjust timelines or scope if capacity insufficient
   - Build in buffer (20%) for unknowns

6. **Create Allocation Document**
   - Visual timeline showing who's working on what when
   - Matrix view: People × Projects with percentages
   - Capacity vs. demand chart
   - Assumptions and constraints documented

**Output:** Complete resource allocation plan with timelines and assignments.

### Workflow 4: Monitor and Rebalance

**Steps:**
1. **Weekly Check-ins**
   - Are people actually working on assigned projects?
   - Any blockers or unexpected work?
   - Capacity assumptions still accurate?
   - Burnout or overwork signals?

2. **Monthly Review**
   - Compare actual time spent vs. allocated
   - Identify variances and root causes
   - Update allocation based on new information
   - Adjust future planning assumptions

3. **Rebalancing Triggers**
   - Project priority changes
   - Team member leaves or joins
   - Project runs over/under estimate significantly
   - Critical bug or incident requires immediate attention
   - Market or business conditions shift

4. **Reallocation Process**
   - Identify what needs to change and why
   - Communicate changes to affected team members
   - Update allocation plan and timelines
   - Notify stakeholders of impact
   - Document decisions and rationale

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Calculate capacity | "calculate team capacity" |
| Skill matrix | "create skill matrix for team" |
| Allocate resources | "allocate resources for [project]" |
| Check allocation | "show current resource allocation" |
| Balance workload | "balance workload across team" |
| Identify gaps | "find resource gaps" |
| Capacity forecast | "forecast capacity for Q[n]" |
| Rebalance | "rebalance resources" |

## Best Practices

- **Plan for 70% utilization**: People are not machines; sustainable pace requires buffer for thinking, learning, and interruptions
- **Minimize context switching**: Assign people to 1-2 projects max; each additional project adds 20-30% overhead
- **Match skills AND interests**: Engaged team members are 2-3x more productive than disengaged ones
- **Build in growth**: Allocate 5-10% time for learning; prevents skill stagnation and improves retention
- **Avoid hero culture**: Don't consistently over-allocate top performers; leads to burnout and resentment
- **Transparent allocation**: Share allocation plans openly; reduces politics and builds trust
- **Protected focus time**: Reserve contiguous blocks (4+ hours) for deep work; no meetings or interruptions
- **Review regularly**: Allocations drift from reality quickly; review weekly, rebalance monthly
- **Document assumptions**: Capacity estimates are assumptions; write them down to validate and refine
- **Emergency buffer**: Reserve 10-20% unallocated capacity for urgent work and incidents
- **Respect team input**: Involve team in allocation decisions; they know their capacity and interests best
- **Track actual vs. planned**: Learn from variances to improve future planning accuracy

## Capacity Planning Formula

```
Effective Weekly Capacity =
  (Total Hours) × (1 - Meeting %) × (1 - Admin %) × (1 - Support %)

Example for Senior Engineer:
  40 hours/week × 0.85 (15% meetings) × 0.90 (10% admin) × 0.80 (20% support)
  = 40 × 0.85 × 0.90 × 0.80
  = 24.5 hours/week for project work
```

**Adjustment Factors:**
- **Junior engineer**: 0.5-0.7x (learning curve, need for guidance)
- **New team member**: 0.3-0.5x for first month (onboarding)
- **Multi-project**: 0.7-0.8x per project (context switching penalty)
- **Legacy codebase**: 0.7-0.8x (higher cognitive load)
- **Remote team**: 1.0-1.1x (fewer office interruptions)

## Allocation Patterns

### Pattern 1: Dedicated Team
**Structure**: Team of 4-8 people working 100% on one project
**Pros**: Maximum focus, strong team cohesion, fast delivery
**Cons**: Requires substantial project; can create silos
**Best for**: Large strategic initiatives, 3+ month projects

### Pattern 2: Feature Teams
**Structure**: Cross-functional team owns specific product area
**Allocation**: 100% to their area
**Pros**: Deep expertise, ownership, autonomy
**Cons**: Can create silos; hard to rebalance
**Best for**: Mature products with clear boundaries

### Pattern 3: Rotation Model
**Structure**: Team members rotate between projects/teams quarterly
**Pros**: Knowledge sharing, skill development, flexibility
**Cons**: Ramp-up time, less deep expertise
**Best for**: Early-stage companies, generalist teams

### Pattern 4: Matrix Allocation
**Structure**: People split time across multiple projects (50/50, 70/30)
**Pros**: Flexible, fills capacity, can pursue multiple priorities
**Cons**: Context switching, coordination overhead, slower delivery
**Best for**: Resource-constrained teams, mixed priorities

### Pattern 5: Specialist Pool
**Structure**: Shared specialists (designers, SRE, security) allocated as needed
**Allocation**: 2-3 week rotations across projects
**Pros**: Efficient use of scarce skills, cross-pollination
**Cons**: Bottleneck risk, scheduling complexity
**Best for**: Specialized roles with high demand

## Workload Balancing Metrics

| Metric | Healthy Range | Warning Signs |
|--------|---------------|---------------|
| **Allocation %** | 60-80% | > 90% over-allocated, < 50% under-utilized |
| **Projects per person** | 1-2 | > 2 projects (context switching) |
| **Overtime hours** | < 5 hours/week | > 10 hours/week (burnout risk) |
| **PTO utilization** | > 80% | < 50% (not taking time off) |
| **Meeting load** | 15-25% | > 30% (meeting overload) |
| **Deep work blocks** | 3-4 per week | < 2 (fragmented time) |

## Skill Development Framework

**70-20-10 Rule for Growth:**
- **70%**: Work in areas of competence (productive contribution)
- **20%**: Stretch assignments (build new skills)
- **10%**: Completely new areas (exploration)

**Progression Paths:**
- Junior → Mid: Needs 70% mentored work, 30% independent
- Mid → Senior: Needs challenging technical problems, some mentoring experience
- Senior → Staff: Needs cross-team projects, architecture ownership
- IC → Manager: Needs people management experience, delegate technical work

## Resource Constraint Resolution

**When demand exceeds capacity:**

1. **Add resources** (hire, contractors)
   - Pros: Increases capacity
   - Cons: Slow (3-6 months), expensive, onboarding overhead

2. **Reduce scope** (cut features, simplify)
   - Pros: Fast, maintains quality
   - Cons: Stakeholder disappointment, hard choices

3. **Extend timeline** (push dates)
   - Pros: Maintains scope and quality
   - Cons: Business impact, competitive pressure

4. **Accept lower quality** (cut corners, tech debt)
   - Pros: Hits dates
   - Cons: Future slowdown, bugs, user experience

**Recommendation priority**: Reduce scope > Extend timeline > Add resources > Lower quality

## Integration Points

- **Project Planner**: Pulls project timelines and effort estimates
- **Sprint Planner**: Weekly/sprint-level allocation
- **Task Manager**: Daily task assignments
- **HR Systems**: PTO, team roster, role information
- **Time Tracking**: Actual time spent for validation
- **Calendar**: Meeting load analysis
- **Performance Management**: Skill assessments, growth goals
