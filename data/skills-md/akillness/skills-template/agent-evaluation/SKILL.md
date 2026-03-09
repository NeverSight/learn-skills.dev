---
name: agent-evaluation
description: Design and implement comprehensive evaluation systems for AI agents. Use when building evals for coding agents, conversational agents, research agents, or computer-use agents. Covers grader types, benchmarks, 8-step roadmap, and production integration.
allowed-tools: Read Write Shell Grep Glob
metadata:
  tags: agent-evaluation, evals, AI-agents, benchmarks, graders, testing, quality-assurance
  platforms: Claude, ChatGPT, Gemini
---


# Agent Evaluation (AI Agent Evals)

> Based on Anthropic's "Demystifying evals for AI agents"

## When to use this skill

- Designing evaluation systems for AI agents
- Building benchmarks for coding, conversational, or research agents
- Creating graders (code-based, model-based, human)
- Implementing production monitoring for AI systems
- Setting up CI/CD pipelines with automated evals
- Debugging agent performance issues
- Measuring agent improvement over time

## Core Concepts

### Eval Evolution: Single-turn → Multi-turn → Agentic

| Type | Turns | State | Grading | Complexity |
|------|-------|-------|---------|------------|
| **Single-turn** | 1 | None | Simple | Low |
| **Multi-turn** | N | Conversation | Per-turn | Medium |
| **Agentic** | N | World + History | Outcome | High |

### 7 Key Terms

| Term | Definition |
|------|------------|
| **Task** | Single test case (prompt + expected outcome) |
| **Trial** | One agent run on a task |
| **Grader** | Scoring function (code/model/human) |
| **Transcript** | Full record of agent actions |
| **Outcome** | Final state for grading |
| **Harness** | Infrastructure running evals |
| **Suite** | Collection of related tasks |

## Instructions

### Step 1: Understand Grader Types

#### Code-based Graders (Recommended for Coding Agents)
- **Pros**: Fast, objective, reproducible
- **Cons**: Requires clear success criteria
- **Best for**: Coding agents, structured outputs

```python
# Example: Code-based grader
def grade_task(outcome: dict) -> float:
    """Grade coding task by test passage."""
    tests_passed = outcome.get("tests_passed", 0)
    total_tests = outcome.get("total_tests", 1)
    return tests_passed / total_tests

# SWE-bench style grader
def grade_swe_bench(repo_path: str, test_spec: dict) -> bool:
    """Run tests and check if patch resolves issue."""
    result = subprocess.run(
        ["pytest", test_spec["test_file"]],
        cwd=repo_path,
        capture_output=True
    )
    return result.returncode == 0
```

#### Model-based Graders (LLM-as-Judge)
- **Pros**: Flexible, handles nuance
- **Cons**: Requires calibration, can be inconsistent
- **Best for**: Conversational agents, open-ended tasks

```yaml
# Example: LLM Rubric for Customer Support Agent
rubric:
  dimensions:
    - name: empathy
      weight: 0.3
      scale: 1-5
      criteria: |
        5: Acknowledges emotions, uses warm language
        3: Polite but impersonal
        1: Cold or dismissive

    - name: resolution
      weight: 0.5
      scale: 1-5
      criteria: |
        5: Fully resolves issue
        3: Partial resolution
        1: No resolution

    - name: efficiency
      weight: 0.2
      scale: 1-5
      criteria: |
        5: Resolved in minimal turns
        3: Reasonable turns
        1: Excessive back-and-forth
```

#### Human Graders
- **Pros**: Highest accuracy, catches edge cases
- **Cons**: Expensive, slow, not scalable
- **Best for**: Final validation, ambiguous cases

### Step 2: Choose Strategy by Agent Type

#### 2.1 Coding Agents

**Benchmarks**:
- SWE-bench Verified: Real GitHub issues (40% → 80%+ achievable)
- Terminal-Bench: Complex terminal tasks
- Custom test suites with your codebase

**Grading Strategy**:
```python
def grade_coding_agent(task: dict, outcome: dict) -> dict:
    return {
        "tests_passed": run_test_suite(outcome["code"]),
        "lint_score": run_linter(outcome["code"]),
        "builds": check_build(outcome["code"]),
        "matches_spec": compare_to_reference(task["spec"], outcome["code"])
    }
```

**Key Metrics**:
- Test passage rate
- Build success
- Lint/style compliance
- Diff size (smaller is better)

#### 2.2 Conversational Agents

**Benchmarks**:
- τ2-Bench: Multi-domain conversation
- Custom domain-specific suites

**Grading Strategy** (Multi-dimensional):
```yaml
success_criteria:
  - empathy_score: >= 4.0
  - resolution_rate: >= 0.9
  - avg_turns: <= 5
  - escalation_rate: <= 0.1
```

**Key Metrics**:
- Task resolution rate
- Customer satisfaction proxy
- Turn efficiency
- Escalation rate

#### 2.3 Research Agents

**Grading Dimensions**:
1. **Grounding**: Claims backed by sources
2. **Coverage**: All aspects addressed
3. **Source Quality**: Authoritative sources used

```python
def grade_research_agent(task: dict, outcome: dict) -> dict:
    return {
        "grounding": check_citations(outcome["report"]),
        "coverage": check_topic_coverage(task["topics"], outcome["report"]),
        "source_quality": score_sources(outcome["sources"]),
        "factual_accuracy": verify_claims(outcome["claims"])
    }
```

#### 2.4 Computer Use Agents

**Benchmarks**:
- WebArena: Web navigation tasks
- OSWorld: Desktop environment tasks

**Grading Strategy**:
```python
def grade_computer_use(task: dict, outcome: dict) -> dict:
    return {
        "ui_state": verify_ui_state(outcome["screenshot"]),
        "db_state": verify_database(task["expected_db_state"]),
        "file_state": verify_files(task["expected_files"]),
        "success": all_conditions_met(task, outcome)
    }
```

### Step 3: Follow the 8-Step Roadmap

#### Step 0: Start Early (20-50 Tasks)
```bash
# Create initial eval suite structure
mkdir -p evals/{tasks,results,graders}

# Start with representative tasks
# - Common use cases (60%)
# - Edge cases (20%)
# - Failure modes (20%)
```

#### Step 1: Convert Manual Tests
```python
# Transform existing QA tests into eval tasks
def convert_qa_to_eval(qa_case: dict) -> dict:
    return {
        "id": qa_case["id"],
        "prompt": qa_case["input"],
        "expected_outcome": qa_case["expected"],
        "grader": "code" if qa_case["has_tests"] else "model",
        "tags": qa_case.get("tags", [])
    }
```

#### Step 2: Ensure Clarity + Reference Solutions
```yaml
# Good task definition
task:
  id: "api-design-001"
  prompt: |
    Design a REST API for user management with:
    - CRUD operations
    - Authentication via JWT
    - Rate limiting
  reference_solution: "./solutions/api-design-001/"
  success_criteria:
    - "All endpoints documented"
    - "Auth middleware present"
    - "Rate limit config exists"
```

#### Step 3: Balance Positive/Negative Cases
```python
# Ensure eval suite balance
suite_composition = {
    "positive_cases": 0.5,    # Should succeed
    "negative_cases": 0.3,    # Should fail gracefully
    "edge_cases": 0.2         # Boundary conditions
}
```

#### Step 4: Isolate Environments
```yaml
# Docker-based isolation for coding evals
eval_environment:
  type: docker
  image: "eval-sandbox:latest"
  timeout: 300s
  resources:
    memory: "4g"
    cpu: "2"
  network: isolated
  cleanup: always
```

#### Step 5: Focus on Outcomes, Not Paths
```python
# GOOD: Outcome-focused grader
def grade_outcome(expected: dict, actual: dict) -> float:
    return compare_final_states(expected, actual)

# BAD: Path-focused grader (too brittle)
def grade_path(expected_steps: list, actual_steps: list) -> float:
    return step_by_step_match(expected_steps, actual_steps)
```

#### Step 6: Always Read Transcripts
```python
# Transcript analysis for debugging
def analyze_transcript(transcript: list) -> dict:
    return {
        "total_steps": len(transcript),
        "tool_usage": count_tool_calls(transcript),
        "errors": extract_errors(transcript),
        "decision_points": find_decision_points(transcript),
        "recovery_attempts": find_recovery_patterns(transcript)
    }
```

#### Step 7: Monitor Eval Saturation
```python
# Detect when evals are no longer useful
def check_saturation(results: list, window: int = 10) -> dict:
    recent = results[-window:]
    return {
        "pass_rate": sum(r["passed"] for r in recent) / len(recent),
        "variance": calculate_variance(recent),
        "is_saturated": all(r["passed"] for r in recent),
        "recommendation": "Add harder tasks" if saturated else "Continue"
    }
```

#### Step 8: Long-term Maintenance
```yaml
# Eval suite maintenance checklist
maintenance:
  weekly:
    - Review failed evals for false negatives
    - Check for flaky tests
  monthly:
    - Add new edge cases from production issues
    - Retire saturated evals
    - Update reference solutions
  quarterly:
    - Full benchmark recalibration
    - Team contribution review
```

### Step 4: Integrate with Production

#### CI/CD Integration
```yaml
# GitHub Actions example
name: Agent Evals
on: [push, pull_request]

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Evals
        run: |
          python run_evals.py --suite=core --mode=compact
      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: results/
```

#### Production Monitoring
```python
# Real-time eval sampling
class ProductionMonitor:
    def __init__(self, sample_rate: float = 0.1):
        self.sample_rate = sample_rate

    async def monitor(self, request, response):
        if random.random() < self.sample_rate:
            eval_result = await self.run_eval(request, response)
            self.log_result(eval_result)
            if eval_result["score"] < self.threshold:
                self.alert("Low quality response detected")
```

#### A/B Testing
```python
# Compare agent versions
def run_ab_test(suite: str, versions: list) -> dict:
    results = {}
    for version in versions:
        results[version] = run_eval_suite(suite, agent_version=version)
    return {
        "comparison": compare_results(results),
        "winner": determine_winner(results),
        "confidence": calculate_confidence(results)
    }
```

## Best Practices

### Do's ✅
1. **Start with 20-50 representative tasks**
2. **Use code-based graders when possible**
3. **Focus on outcomes, not paths**
4. **Read transcripts for debugging**
5. **Monitor for eval saturation**
6. **Balance positive/negative cases**
7. **Isolate eval environments**
8. **Version your eval suites**

### Don'ts ❌
1. **Don't over-rely on model-based graders without calibration**
2. **Don't ignore failed evals (false negatives exist)**
3. **Don't grade on intermediate steps**
4. **Don't skip transcript analysis**
5. **Don't use production data without sanitization**
6. **Don't let eval suites become stale**

## Success Patterns

### Pattern 1: Graduated Eval Complexity
```
Level 1: Unit evals (single capability)
Level 2: Integration evals (combined capabilities)
Level 3: End-to-end evals (full workflows)
Level 4: Adversarial evals (edge cases)
```

### Pattern 2: Eval-Driven Development
```
1. Write eval task for new feature
2. Run eval (expect failure)
3. Implement feature
4. Run eval (expect pass)
5. Add to regression suite
```

### Pattern 3: Continuous Calibration
```
Weekly: Review grader accuracy
Monthly: Update rubrics based on feedback
Quarterly: Full grader audit with human baseline
```

## Troubleshooting

### Problem: Eval scores at 100%
**Solution**: Add harder tasks, check for eval saturation (Step 7)

### Problem: Inconsistent model-based grader scores
**Solution**: Add more examples to rubric, use structured output, ensemble graders

### Problem: Evals too slow for CI
**Solution**: Use toon mode, parallelize, sample subset for PR checks

### Problem: Agent passes evals but fails in production
**Solution**: Add production failure cases to eval suite, increase diversity

## References

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [SWE-bench](https://www.swebench.com/)
- [WebArena](https://webarena.dev/)
- [τ2-Bench](https://github.com/sierra-research/tau2-bench)

## Examples

### Example 1: Simple Coding Agent Eval

```python
# Task definition
task = {
    "id": "fizzbuzz-001",
    "prompt": "Write a fizzbuzz function in Python",
    "test_cases": [
        {"input": 3, "expected": "Fizz"},
        {"input": 5, "expected": "Buzz"},
        {"input": 15, "expected": "FizzBuzz"},
        {"input": 7, "expected": "7"}
    ]
}

# Grader
def grade(task, outcome):
    code = outcome["code"]
    exec(code)  # In sandbox
    for tc in task["test_cases"]:
        if fizzbuzz(tc["input"]) != tc["expected"]:
            return 0.0
    return 1.0
```

### Example 2: Conversational Agent Eval with LLM Rubric

```yaml
task:
  id: "support-refund-001"
  scenario: |
    Customer wants refund for damaged product.
    Product: Laptop, Order: #12345, Damage: Screen crack
  expected_actions:
    - Acknowledge issue
    - Verify order
    - Offer resolution options
  max_turns: 5

grader:
  type: model
  model: claude-3-5-sonnet-20241022
  rubric: |
    Score 1-5 on each dimension:
    - Empathy: Did agent acknowledge customer frustration?
    - Resolution: Was a clear solution offered?
    - Efficiency: Was issue resolved in reasonable turns?
```
