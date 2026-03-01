---
name: agent-generator-tutor
version: 1.0.0
description: |
  Interactive teaching agent for the goal-seeking agent generator and eval system.
  Provides a structured 14-lesson curriculum covering agent generation, SDK selection,
  multi-agent architecture, progressive evaluation (L1-L12), retrieval strategies,
  intent classification, math code generation, self-improvement loops with patch
  proposer and reviewer voting, and memory export/import.
auto-detection:
  triggers:
    - "teach me"
    - "tutorial"
    - "learn about agents"
    - "how do I generate an agent"
    - "eval tutorial"
    - "agent generator tutorial"
    - "teaching agent"
    - "generator teacher"
    - "lesson"
    - "curriculum"
allowed-tools: ["Read", "Bash"]
target-agents: []
priority: "medium"
complexity: "low"
---

# Agent Generator Tutor Skill

Interactive teaching agent for the goal-seeking agent generator and eval system.

## What This Skill Does

Loads the `GeneratorTeacher` from `src/amplihack/agents/teaching/generator_teacher.py`
and guides users through a structured 14-lesson curriculum with exercises and quizzes.

## Curriculum (14 Lessons)

| Lesson | Title                                   | Topics                                       |
| ------ | --------------------------------------- | -------------------------------------------- |
| L01    | Introduction to Goal-Seeking Agents     | Architecture, GoalSeekingAgent interface     |
| L02    | Your First Agent (CLI Basics)           | Prompt files, CLI invocation, pipeline       |
| L03    | SDK Selection Guide                     | Copilot, Claude, Microsoft, Mini SDKs        |
| L04    | Multi-Agent Architecture                | Coordinators, sub-agents, shared memory      |
| L05    | Agent Spawning                          | Dynamic sub-agent creation at runtime        |
| L06    | Running Evaluations                     | Progressive test suite, SDK eval loop        |
| L07    | Understanding Eval Levels L1-L12        | Core (L1-L6) and advanced (L7-L12) levels    |
| L08    | Self-Improvement Loop                   | EVAL-ANALYZE-RESEARCH-IMPROVE-RE-EVAL-DECIDE |
| L09    | Security Domain Agents                  | Domain-specific agents and eval              |
| L10    | Custom Eval Levels                      | TestLevel, TestArticle, TestQuestion         |
| L11    | Retrieval Architecture                  | Simple, entity, concept, tiered strategies   |
| L12    | Intent Classification and Math Code Gen | Nine intent types, safe arithmetic           |
| L13    | Patch Proposer and Reviewer Voting      | Automated code patches, 3-perspective review |
| L14    | Memory Export/Import                    | Snapshots, cross-session persistence         |

## How to Use

### Start the Tutorial

```python
from amplihack.agents.teaching.generator_teacher import GeneratorTeacher

teacher = GeneratorTeacher()
# See what lesson is next
next_lesson = teacher.get_next_lesson()
print(f"Start with: {next_lesson.title}")
```

### Teach a Lesson

```python
content = teacher.teach_lesson("L01")
print(content)  # Full lesson with exercises and quiz questions
```

### Check an Exercise

```python
feedback = teacher.check_exercise("L01", "E01-01", "your answer here")
print(feedback)  # PASS or NOT YET with hints
```

### Run a Quiz

```python
# Self-grading mode (see correct answers)
result = teacher.run_quiz("L01")

# Provide answers for grading
result = teacher.run_quiz("L01", answers=["PromptAnalyzer", "Explains stored knowledge", "False"])
print(f"Score: {result.quiz_score:.0%}, Passed: {result.passed}")
```

### Check Progress

```python
report = teacher.get_progress_report()
print(report)  # Shows completed/locked/available lessons
```

### Validate Curriculum Integrity

```python
validation = teacher.validate_tutorial()
print(f"Valid: {validation['valid']}, Issues: {validation['issues']}")
```

## Prerequisites

Each lesson has prerequisites that must be completed first. The curriculum follows
a dependency graph ensuring foundational concepts are learned before advanced topics.

## Exercise Validators

The teaching agent includes 15 specialized validators that check user answers
for correctness. Exercises without explicit validators use a fallback that checks
for key phrases from the expected output.
