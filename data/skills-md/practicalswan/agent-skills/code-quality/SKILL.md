---
name: code-quality
description: Code review, refactoring, and quality improvement. Use when reviewing code, eliminating code smells, reducing technical debt, refactoring methods, running self-critique loops, or improving maintainability and readability.
license: Complete terms in LICENSE.txt
---

# Code Quality Management

Comprehensive skill for improving code quality through code review, surgical refactoring, and self-evaluation loops.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Code Review:**
- Performing code reviews, analyzing pull requests
- Checking code quality, security auditing, performance reviews
- Examining code for bugs, vulnerabilities, best practices violations
- "Review code", "check for issues", "audit code", "analyze PR"

**Refactoring:**
- Code is hard to understand or maintain
- Functions/classes are too large, code smells need addressing
- Adding features is difficult due to code structure
- User asks "clean up this code", "refactor this", "improve this"

**Self-Evaluation:**
- Implementing self-critique and reflection loops for agent outputs
- Building evaluator-optimizer pipelines for quality-critical generation
- Creating test-driven code refinement workflows
- Designing rubric-based or LLM-as-judge evaluation systems
- Adding iterative improvement to agent outputs (code, reports, analysis)
- Measuring and improving agent response quality

## Part 1: Code Review

### Review Priorities

When performing a code review, prioritize issues in this order:

#### 🔴 CRITICAL (Block merge)
- **Security**: Vulnerabilities, exposed secrets, authentication/authorization issues
- **Correctness**: Logic errors, data corruption risks, race conditions
- **Breaking Changes**: API contract changes without versioning
- **Data Loss**: Risk of data loss or corruption

#### 🟡 IMPORTANT (Requires discussion)
- **Code Quality**: Severe violations of SOLID principles, excessive duplication
- **Test Coverage**: Missing tests for critical paths or new functionality
- **Performance**: Obvious performance bottlenecks (N+1 queries, memory leaks)
- **Architecture**: Significant deviations from established patterns

#### 🟢 SUGGESTION (Non-blocking improvements)
- **Readability**: Poor naming, complex logic that could be simplified
- **Optimization**: Performance improvements without functional impact
- **Best Practices**: Minor deviations from conventions
- **Documentation**: Missing or incomplete comments/documentation

### Review Principles

1. **Be specific**: Reference exact lines, files, and provide concrete examples
2. **Provide context**: Explain WHY something is an issue and potential impact
3. **Suggest solutions**: Show corrected code when applicable, not just what's wrong
4. **Be constructive**: Focus on improving code, not criticizing the author
5. **Recognize good practices**: Acknowledge well-written code and smart solutions
6. **Be pragmatic**: Not every suggestion needs immediate implementation
7. **Group related comments**: Avoid multiple comments about the same topic

### Review Checklist

#### Code Quality
- [ ] Code follows project conventions and style guide
- [ ] Functions and classes have single responsibility
- [ ] Proper error handling throughout
- [ ] No code duplication (DRY principle maintained)
- [ ] Appropriate use of design patterns
- [ ] No obvious security vulnerabilities

#### Testing
- [ ] New functionality has tests
- [ ] Edge cases are covered
- [ ] Tests are meaningful and not brittle
- [ ] Test coverage meets project requirements

#### Performance
- [ ] No obvious performance bottlenecks
- [ ] Efficient algorithms and data structures
- [ ] Proper database query optimization
- [ ] Appropriate caching strategies

#### Security
- [ ] No hardcoded credentials or secrets
- [ ] Input validation and sanitization
- [ ] Proper authentication and authorization
- [ ] Protection against common attacks (XSS, SQL injection, etc.)

---

## Part 2: Refactoring

### The Golden Rules

1. **Behavior is preserved** - Refactoring doesn't change what code does, only how
2. **Small steps** - Make tiny changes, test after each
3. **Version control is your friend** - Commit before and after each safe state
4. **Tests are essential** - Without tests, you're not refactoring, you're editing
5. **One thing at a time** - Don't mix refactoring with feature changes

### When NOT to Refactor

- Code that works and won't change again (if it ain't broke...)
- Critical production code without tests (add tests first)
- When you're under a tight deadline
- "Just because" - need a clear purpose

### Refactoring Techniques

#### Extract Method
```javascript
// Before
function processOrder(order) {
    if (order.status === 'pending') {
        // 20 lines of validation logic
        // 15 lines of calculation logic
        // 10 lines of notification logic
    }
}

// After
function processOrder(order) {
    if (order.status === 'pending') {
        validateOrder(order);
        calculateTotals(order);
        sendNotification(order);
    }
}
```

#### Rename Variable/Function
Use meaningful names that describe purpose:
```javascript
// Before
const d = new Date();
process(v, u);

// After
const currentDate = new Date();
processValidation(validatedValue, userId);
```

#### Extract Class
```javascript
// Before
function calculateCartTotal(cart, user, shippingMethod, taxRate) {
    // Complex logic mixing user details, cart items, shipping, tax
}

// After
class OrderCalculator {
    constructor(cart, user) {
        this.cart = cart;
        this.user = user;
    }

    calculate(shippingMethod, taxRate) {
        const subtotal = this.calculateSubtotal();
        const shipping = this.calculateShipping(shippingMethod);
        const tax = this.calculateTax(taxRate);
        return subtotal + shipping + tax;
    }
}
```

### Common Code Smells and Fixes

#### Long Method
**Problem**: Methods longer than 30-50 lines
**Fix**: Extract smaller, focused methods

#### Duplicate Code
**Problem**: Same logic in multiple places
**Fix**: Extract to shared function/method

#### Large Class
**Problem**: Classes with too many responsibilities
**Fix**: Extract smaller, focused classes

#### Magic Numbers
**Problem**: Unnamed numeric literals
```javascript
// Before
if (status > 3) { ... }

// After
const MAX_PENDING_DURATION_DAYS = 3;
if (status > MAX_PENDING_DURATION_DAYS) { ... }
```

#### Feature Envy
**Problem**: Method uses data from another class more than its own
**Fix**: Move method to class it's envious of

---

## Part 3: Self-Evaluation Patterns

### Pattern 1: Basic Reflection

Agent evaluates and improves its own output through self-critique.

```python
def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    """Generate with reflection loop."""
    output = llm(f"Complete this task:\n{task}")

    for i in range(max_iterations):
        # Self-critique
        critique = llm(f"""
        Evaluate this output against criteria: {criteria}
        Output: {output}
        Rate each: PASS/FAIL with feedback as JSON.
        """)

        critique_data = json.loads(critique)
        all_pass = all(c["status"] == "PASS" for c in critique_data.values())
        if all_pass:
            return output

        # Refine based on critique
        failed = {k: v["feedback"] for k, v in critique_data.items() if v["status"] == "FAIL"}
        output = llm(f"Improve to address: {failed}\nOriginal: {output}")

    return output
```

**Key insight**: Use structured JSON output for reliable parsing of critique results.

### Pattern 2: Evaluator-Optimizer

Separate generation and evaluation into distinct components for clearer responsibilities.

```python
class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8):
        self.score_threshold = score_threshold

    def generate(self, task: str) -> str:
        return llm(f"Complete: {task}")

    def evaluate(self, output: str, task: str) -> dict:
        return json.loads(llm(f"""
        Evaluate output for task: {task}
        Output: {output}
        Return JSON: {{"overall_score": 0-1, "dimensions": {{"accuracy": ..., "clarity": ...}}}
        """))

    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"Improve based on feedback: {feedback}\nOutput: {output}")

    def run(self, task: str, max_iterations: int = 3) -> str:
        output = self.generate(task)
        for _ in range(max_iterations):
            evaluation = self.evaluate(output, task)
            if evaluation["overall_score"] >= self.score_threshold:
                break
            output = self.optimize(output, evaluation)
        return output
```

### Pattern 3: Code-Specific Reflection

Test-driven refinement loop for code generation.

```python
class CodeReflector:
    def reflect_and_fix(self, spec: str, max_iterations: int = 3) -> str:
        code = llm(f"Write Python code for: {spec}")
        tests = llm(f"Generate pytest tests for: {spec}\nCode: {code}")

        for _ in range(max_iterations):
            result = run_tests(code, tests)
            if result["success"]:
                return code
            code = llm(f"Fix error: {result['error']}\nCode: {code}")
        return code
```

### Evaluation Strategies

#### Outcome-Based
Evaluate whether output achieves expected result.

```python
def evaluate_outcome(task: str, output: str, expected: str) -> str:
    return llm(f"Does output achieve expected outcome? Task: {task}, Expected: {expected}, Output: {output}")
```

#### LLM-as-Judge
Use LLM to compare and rank outputs.

```python
def llm_judge(output_a: str, output_b: str, criteria: str) -> str:
    return llm(f"Compare outputs A and B for {criteria}. Which is better and why?")
```

#### Rubric-Based
Score outputs against weighted dimensions.

```python
RUBRIC = {
    "accuracy": {"weight": 0.4},
    "clarity": {"weight": 0.3},
    "completeness": {"weight": 0.3}
}

def evaluate_with_rubric(output: str, rubric: dict) -> float:
    scores = json.loads(llm(f"Rate 1-5 for each dimension: {list(rubric.keys())}\nOutput: {output}"))
    return sum(scores[d] * rubric[d]["weight"] for d in rubric) / 5
```

---

## Best Practices

### For Code Reviews
- Focus on code behavior, not personal style preferences
- Provide actionable feedback with examples
- Balance critique with recognition of good work
- Consider project context and constraints

### For Refactoring
- Always have tests before refactoring
- Commit frequently to maintain safety
- Keep changes small and verifiable
- Document non-obvious refactoring decisions

### For Self-Evaluation
- Define clear, measurable evaluation criteria upfront
- Set iteration limits (3-5) to prevent infinite loops
- Add convergence detection if scores aren't improving
- Log full iteration trajectory for debugging and analysis
- Use structured output (JSON) for reliable parsing

---

## Quality Improvement Checklist

### Code Review Checklist
```markdown
## Code Review Assessment

### Functionality
- [ ] Logic is correct and achieves intended purpose
- [ ] Edge cases are handled appropriately
- [ ] Error handling is comprehensive
- [ ] No obvious bugs or race conditions

### Code Quality
- [ ] Code is readable and maintainable
- [ ] Naming is descriptive and consistent
- [ ] Functions/classes have single responsibility
- [ ] No unnecessary complexity or obfuscation

### Architecture
- [ ] Follows established project patterns
- [ ] Appropriate use of design patterns
- [ ] Proper separation of concerns
- [ ] No tight coupling or hidden dependencies
```

### Refactoring Checklist
```markdown
## Refactoring Safety Checklist

### Pre-Refactoring
- [ ] Tests exist and pass
- [ ] Version control branch is clean
- [ ] Understand current behavior thoroughly

### During Refactoring
- [ ] Making small, incremental changes
- [ ] Running tests after each change
- [ ] Committing each working intermediate state
- [ ] Preserving external behavior

### Post-Refactoring
- [ ] All tests still pass
- [ ] Code is simpler and clearer
- [ ] No new bugs introduced
- [ ] Documentation updated if needed
```

### Self-Evaluation Checklist
```markdown
## Evaluation Implementation Checklist

### Setup
- [ ] Define evaluation criteria/rubric
- [ ] Set score threshold for "good enough"
- [ ] Configure max iterations (default: 3)

### Implementation
- [ ] Implement generate() function
- [ ] Implement evaluate() function with structured output
- [ ] Implement optimize() function
- [ ] Wire up to refinement loop

### Safety
- [ ] Add convergence detection
- [ ] Log all iterations for debugging
- [ ] Handle evaluation parse failures gracefully

---

## References & Resources

### Documentation
- [Refactoring Catalog](./references/refactoring-catalog.md) — 12 refactoring techniques with before/after code examples and pitfalls
- [Code Smells](./references/code-smells.md) — 17 code smells organized by category with detection signals and remedies

### Scripts
- [Review Checklist](./scripts/review-checklist.py) — Python script for automated static analysis of JS/TS files

### Examples
- [Refactoring Walkthrough](./examples/refactoring-walkthrough.md) — Step-by-step React component refactoring from 160 lines to clean architecture

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [development-workflow](../development-workflow/SKILL.md) | Quality gates within the development lifecycle |
| [documentation-quality](../documentation-quality/SKILL.md) | Consistent quality standards for code and docs |
| [serena-usage](../serena-usage/SKILL.md) | Symbol-based refactoring via Serena code navigation |

---
