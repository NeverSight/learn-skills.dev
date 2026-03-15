---
name: multigrade-planner
description: "Specialized tool for creating unified lesson plans for classrooms with multiple grade levels. Essential for rural Indian schools where one teacher manages multiple grades simultaneously."
license: Proprietary - SahayakAI Internal
---

# Multigrade Planner Skill

This skill is designed to solve the **Multigrade Chaos** pain point by synchronizing instruction across different learning levels.

## 📋 Core Capability

When a teacher handles two or more grades (e.g., Grade 1 and Grade 2) in the same 45-minute period, the AI should generate a **Parallel Rotation Plan**.

### The Rotation Model:
1. **Direct Instruction (Grade A)**: Teacher works directly with one group.
2. **Independent Task (Grade B)**: Other groups work on peer-to-peer or self-guided activities.
3. **Switch**: Groups rotate halfway through the period.

## 🛠️ Usage Patterns

### Input Schema Requirement:
The triggering flow must provide a `grades` array (e.g., `['1st Grade', '2nd Grade']`) and a shared `subject`.

### Output Structure:
The generated plan MUST use a split-column table or a clearly marked rotation schedule.

```markdown
| Time | Teacher Action (Grade 1) | Student Action (Grade 2) |
| :--- | :--- | :--- |
| 0-10m | **Engage**: Common story for all | Listening |
| 10-25m | **Direct**: Math foundational (G1) | **Independent**: Grade 2 Workbook |
| 25-40m | **Independent**: G1 Practice | **Direct**: Math advanced (G2) |
| 40-45m | **Consolidate**: Shared summary | Shared summary |
```

## 🎯 Alignment
- Must align with **FLN (Foundational Literacy and Numeracy)** goals for lower grades.
- Must use **Offline-Activity** logic (requiring only chalk, blackboard, or local stones/leaves).
