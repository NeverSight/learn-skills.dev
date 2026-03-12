---
name: design-patterns
description: Identify, implement, and teach GoF design patterns
sasmp_version: "1.3.0"
bonded_agent: 02-design-patterns
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# Design Patterns Skill

> Atomic skill for design pattern identification and implementation

## Skill Definition

```yaml
skill_id: design-patterns
responsibility: Single - Pattern identification, implementation, teaching
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  action: 'identify' | 'implement' | 'detect_antipattern' | 'teach';

  // Conditional
  problem_description?: string;    // Required for 'identify'
  pattern_name?: string;           // Required for 'implement', 'teach'
  code?: string;                   // Required for 'detect_antipattern'
  language?: string;               // Required for 'implement'

  // Optional
  category?: 'creational' | 'structural' | 'behavioral';
  include_uml?: boolean;
}

interface SkillResult {
  patterns?: PatternMatch[];       // For identify
  implementation?: string;         // For implement
  antipatterns?: AntipatternReport[]; // For detect
  explanation?: PatternExplanation;   // For teach
}
```

## Validation Rules

```yaml
input_validation:
  action:
    required: true
    enum: [identify, implement, detect_antipattern, teach]

  problem_description:
    required_when: action == 'identify'
    min_length: 20

  pattern_name:
    required_when: action in ['implement', 'teach']
    valid_patterns: [singleton, factory, builder, adapter, decorator, observer, strategy, command, ...]

  language:
    required_when: action == 'implement'
    allowed: [typescript, javascript, python, java, csharp, go, ruby, kotlin]
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
    - INVALID_PATTERN
    - UNSUPPORTED_LANGUAGE
```

## Logging & Observability

```yaml
logging:
  level: INFO
  events:
    - pattern_identification_started
    - pattern_matched
    - implementation_generated
    - antipattern_detected
    - teaching_session_started

metrics:
  - name: pattern_match_confidence
    type: gauge
  - name: patterns_identified_count
    type: counter
  - name: implementation_generation_time_ms
    type: histogram

tracing:
  span_name: design_patterns_skill
  attributes:
    - action
    - pattern_name
    - language
```

## Pattern Catalog

### Creational Patterns

```yaml
singleton:
  intent: Ensure single instance with global access
  indicators:
    - Global state requirement
    - Resource pooling
    - Configuration management
  implementation_variants:
    - eager
    - lazy
    - thread_safe

factory_method:
  intent: Delegate object creation to subclasses
  indicators:
    - Multiple product types
    - Creation logic varies by context
  implementation_variants:
    - simple_factory
    - factory_method
    - abstract_factory

builder:
  intent: Construct complex objects step by step
  indicators:
    - Many constructor parameters
    - Optional parameters
    - Immutable objects with variations
```

### Structural Patterns

```yaml
adapter:
  intent: Make incompatible interfaces compatible
  indicators:
    - Legacy system integration
    - Third-party library wrapping
  implementation_variants:
    - class_adapter
    - object_adapter

decorator:
  intent: Add behavior dynamically
  indicators:
    - Feature combinations
    - Subclass explosion risk
  implementation_variants:
    - inheritance_based
    - composition_based

facade:
  intent: Simplified interface to complex subsystem
  indicators:
    - Multiple subsystem interactions
    - Complex initialization sequences
```

### Behavioral Patterns

```yaml
observer:
  intent: One-to-many dependency notification
  indicators:
    - Event systems
    - State change propagation
  implementation_variants:
    - push_model
    - pull_model
    - reactive_streams

strategy:
  intent: Encapsulate interchangeable algorithms
  indicators:
    - Multiple algorithm variants
    - Runtime algorithm selection
  implementation_variants:
    - interface_based
    - function_based

command:
  intent: Encapsulate requests as objects
  indicators:
    - Undo/redo requirements
    - Request queuing
    - Macro recording
```

## Usage Examples

### Pattern Identification
```typescript
// Input
{
  action: "identify",
  problem_description: "I need to create different types of documents (PDF, Word, HTML) and the creation logic is complex for each type"
}

// Output
{
  patterns: [
    {
      name: "Factory Method",
      fit_score: 0.92,
      rationale: "Multiple product types with varying creation logic",
      category: "creational"
    },
    {
      name: "Abstract Factory",
      fit_score: 0.78,
      rationale: "Could work if document families are needed",
      category: "creational"
    }
  ]
}
```

### Pattern Implementation
```typescript
// Input
{
  action: "implement",
  pattern_name: "observer",
  language: "typescript"
}

// Output
{
  implementation: `
    interface Observer<T> {
      update(data: T): void;
    }

    class Subject<T> {
      private observers: Observer<T>[] = [];

      subscribe(observer: Observer<T>): void {
        this.observers.push(observer);
      }

      unsubscribe(observer: Observer<T>): void {
        this.observers = this.observers.filter(o => o !== observer);
      }

      notify(data: T): void {
        this.observers.forEach(o => o.update(data));
      }
    }
  `
}
```

## Unit Test Template

```typescript
describe('DesignPatternsSkill', () => {
  describe('identify', () => {
    it('should recommend Factory for object creation scenarios', async () => {
      const result = await skill.execute({
        action: 'identify',
        problem_description: 'Need to create different payment processors based on payment type'
      });

      expect(result.patterns[0].name).toBe('Factory Method');
      expect(result.patterns[0].fit_score).toBeGreaterThan(0.8);
    });
  });

  describe('implement', () => {
    it('should generate valid TypeScript for Observer pattern', async () => {
      const result = await skill.execute({
        action: 'implement',
        pattern_name: 'observer',
        language: 'typescript'
      });

      expect(result.implementation).toContain('interface Observer');
      expect(result.implementation).toContain('subscribe');
      expect(result.implementation).toContain('notify');
    });
  });

  describe('detect_antipattern', () => {
    it('should detect God Object antipattern', async () => {
      const code = `class AppManager { /* 50 methods */ }`;

      const result = await skill.execute({
        action: 'detect_antipattern',
        code
      });

      expect(result.antipatterns).toContainEqual(
        expect.objectContaining({ name: 'God Object' })
      );
    });
  });
});
```

## Error Handling

```yaml
errors:
  INVALID_PATTERN:
    code: 400
    message: "Unknown pattern name"
    recovery: "Check pattern catalog for valid names"

  UNSUPPORTED_LANGUAGE:
    code: 400
    message: "Language not supported for implementation"
    recovery: "Use supported language or request teaching mode"

  INSUFFICIENT_CONTEXT:
    code: 400
    message: "Problem description too vague"
    recovery: "Provide more specific requirements"
```

## Integration

```yaml
requires:
  - code_generator
  - pattern_matcher

emits:
  - pattern_identified
  - pattern_implemented
  - antipattern_detected

consumed_by:
  - 02-design-patterns (bonded agent)
  - 01-design-principles (for pattern suggestions)
  - 04-refactoring (for antipattern fixes)
```
