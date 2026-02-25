---
name: tdd-practices
description: Guide TDD workflow, design tests, and create mocking strategies
sasmp_version: "1.3.0"
bonded_agent: 06-testing-design
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# TDD Practices Skill

> Atomic skill for test-driven development guidance and test design

## Skill Definition

```yaml
skill_id: tdd-practices
responsibility: Single - TDD guidance and test design
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  action: 'design_tests' | 'tdd_guide' | 'mock_strategy' | 'coverage_analysis';
  language: string;

  // Conditional
  code?: string;                  // For design_tests
  feature_description?: string;   // For tdd_guide
  dependencies?: string[];        // For mock_strategy

  // Optional
  test_framework?: string;        // jest, pytest, junit
  test_level?: 'unit' | 'integration' | 'e2e';
}

interface SkillResult {
  test_cases?: TestCase[];
  tdd_steps?: TDDStep[];
  mock_strategy?: MockStrategy;
  coverage_analysis?: CoverageAnalysis;
}
```

## Validation Rules

```yaml
input_validation:
  action:
    required: true
    enum: [design_tests, tdd_guide, mock_strategy, coverage_analysis]

  language:
    required: true
    allowed: [typescript, javascript, python, java, csharp, go, ruby]

  test_framework:
    defaults:
      typescript: jest
      python: pytest
      java: junit
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 1000
    max_delay_ms: 8000
    multiplier: 2

  retryable_errors:
    - TIMEOUT
    - RATE_LIMIT

  non_retryable_errors:
    - INVALID_CODE
    - UNSUPPORTED_FRAMEWORK
```

## TDD Workflow

### Red-Green-Refactor Cycle

```yaml
red_phase:
  goal: Write failing test
  rules:
    - Test must fail for the right reason
    - Test must be specific about expected behavior

green_phase:
  goal: Make test pass
  rules:
    - Write minimum code to pass
    - No premature optimization

refactor_phase:
  goal: Improve design
  rules:
    - Tests must stay green
    - Remove duplication
```

### Mock Types

```yaml
stub:
  purpose: Provide canned answers
  when: Simple dependency

mock:
  purpose: Verify interactions
  when: Need to verify method was called

fake:
  purpose: Working implementation for testing
  when: Complex dependency

spy:
  purpose: Record calls for later verification
  when: Need to verify without changing behavior
```

## Usage Examples

### Test Design
```typescript
// Input
{
  action: "design_tests",
  code: `
    class OrderService {
      async placeOrder(items: Item[], customerId: string): Promise<Order> {
        const order = new Order(customerId, items);
        await this.payment.charge(order.total);
        await this.repo.save(order);
        return order;
      }
    }
  `,
  language: "typescript"
}

// Output
{
  test_cases: [
    {
      name: "should create order with items and customer",
      type: "unit",
      priority: "critical",
      code_template: `
        it('should create order with items and customer', async () => {
          // Arrange
          const mockRepo = { save: jest.fn() };
          const mockPayment = { charge: jest.fn() };
          const service = new OrderService(mockRepo, mockPayment);

          // Act
          const order = await service.placeOrder(items, 'customer-1');

          // Assert
          expect(order.customerId).toBe('customer-1');
        });
      `
    }
  ]
}
```

### TDD Guidance
```typescript
// Input
{
  action: "tdd_guide",
  feature_description: "Add discount code support to checkout",
  language: "typescript"
}

// Output
{
  tdd_steps: [
    {
      phase: "red",
      description: "Write test for valid discount code",
      code_example: `
        it('should apply 10% discount for valid code', () => {
          const checkout = new Checkout();
          checkout.addItem({ price: 100 });
          checkout.applyDiscount('SAVE10');
          expect(checkout.total).toBe(90);
        });
      `
    },
    {
      phase: "green",
      description: "Implement minimal discount logic"
    },
    {
      phase: "refactor",
      description: "Extract discount strategy"
    }
  ]
}
```

## Unit Test Template

```typescript
describe('TDDPracticesSkill', () => {
  describe('design_tests', () => {
    it('should generate test cases for all public methods', async () => {
      const code = `
        class Calculator {
          add(a: number, b: number): number { return a + b; }
        }
      `;

      const result = await skill.execute({
        action: 'design_tests',
        code,
        language: 'typescript'
      });

      expect(result.test_cases.length).toBeGreaterThanOrEqual(1);
    });
  });

  describe('tdd_guide', () => {
    it('should provide red-green-refactor steps', async () => {
      const result = await skill.execute({
        action: 'tdd_guide',
        feature_description: 'User login feature',
        language: 'typescript'
      });

      const phases = result.tdd_steps.map(s => s.phase);
      expect(phases).toContain('red');
      expect(phases).toContain('green');
      expect(phases).toContain('refactor');
    });
  });
});
```

## Error Handling

```yaml
errors:
  INVALID_CODE:
    code: 400
    message: "Cannot parse provided code"
    recovery: "Fix syntax errors in code"

  UNSUPPORTED_FRAMEWORK:
    code: 400
    message: "Test framework not supported"
    recovery: "Use supported framework for language"
```

## Integration

```yaml
requires:
  - code_parser
  - test_generator

emits:
  - tests_designed
  - tdd_guidance_provided
  - mock_strategy_created

consumed_by:
  - 06-testing-design (bonded agent)
  - 04-refactoring (for testability analysis)
```
