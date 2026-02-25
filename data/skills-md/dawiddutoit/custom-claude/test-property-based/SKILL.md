---
name: test-property-based
description: |
  Property-based testing with Hypothesis for Python projects. Use when writing property tests,
  testing invariants, generating test cases, fuzz testing, roundtrip testing, or validating
  behavior across many inputs. Triggers on "property test", "hypothesis test", "generate test
  cases", "invariant testing", "edge case testing", "stateful testing", "roundtrip test".
  Works with Python (.py) test files, pytest, pytest-asyncio, and Pydantic models.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
  - Write
---

# Property-Based Testing with Hypothesis

## Quick Start

Property-based testing automatically generates hundreds of test cases to validate invariants:

```python
from hypothesis import given, strategies as st

# Instead of writing many example tests...
# def test_sort_1(): assert sorted([3,1,2]) == [1,2,3]
# def test_sort_2(): assert sorted([]) == []
# ... (20 more examples)

# Write ONE property test that covers ALL cases
@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    """Property: Sorting twice gives same result as once."""
    once_sorted = sorted(lst)
    twice_sorted = sorted(once_sorted)
    assert once_sorted == twice_sorted
```

**Hypothesis automatically generates 100+ test cases** including edge cases you'd never think of:
empty lists, single elements, duplicates, large lists, negative numbers, etc.

## Table of Contents

1. [When to Use This Skill](#when-to-use-this-skill)
2. [What This Skill Does](#what-this-skill-does)
3. [Core Concepts](#core-concepts)
   - [Strategies](#strategies)
   - [The @given Decorator](#the-given-decorator)
   - [Shrinking](#shrinking)
   - [Custom Strategies](#custom-strategies)
4. [Step-by-Step Workflow](#step-by-step-workflow)
5. [Common Property Patterns](#common-property-patterns)
6. [Integration with pytest](#integration-with-pytest)
7. [Async Property Testing](#async-property-testing)
8. [Pydantic Model Testing](#pydantic-model-testing)
9. [Configuration](#configuration)
10. [Supporting Files](#supporting-files)
11. [Expected Outcomes](#expected-outcomes)
12. [Requirements](#requirements)
13. [Red Flags to Avoid](#red-flags-to-avoid)

## When to Use This Skill

### Explicit Triggers
Use this skill when users mention:
- "property test"
- "hypothesis test"
- "generate test cases"
- "fuzz testing"
- "invariant testing"
- "roundtrip test"
- "stateful testing"
- "edge case testing"
- "test with random data"

### Implicit Triggers
Use when you observe:
- Manual writing of many similar example tests
- Testing parsing/serialization (perfect for roundtrip properties)
- Validating configuration classes (especially Pydantic models)
- Testing algorithms with mathematical properties
- Protocol message handling (IPC, API requests/responses)
- State machine behavior

### Debugging Triggers
Use when:
- Edge case bugs slip through example-based tests
- Need more comprehensive input coverage
- Test suite misses corner cases
- Validating refactored code behavior

## What This Skill Does

This skill guides you through:

1. **Installing Hypothesis** - Add to project dependencies
2. **Writing property tests** - Transform example tests into property-based tests
3. **Choosing strategies** - Select appropriate data generators
4. **Creating custom strategies** - Build domain-specific generators
5. **Async integration** - Combine with pytest-asyncio
6. **Pydantic integration** - Test Pydantic models automatically
7. **Configuration** - Set up profiles for dev/CI/thorough testing
8. **Stateful testing** - Test state machines and complex workflows

**Philosophy:** Instead of "here are 5 examples that should work", write "here's a property that should ALWAYS hold" and let Hypothesis find edge cases.

## Core Concepts

### Strategies

Strategies describe the type of data Hypothesis should generate:

```python
from hypothesis import strategies as st

# Basic types
st.integers()                           # All integers
st.integers(min_value=0, max_value=100) # Constrained range
st.floats(allow_nan=False)              # Floats without NaN
st.text()                               # Unicode strings
st.text(alphabet="abc", min_size=1)     # Limited alphabet
st.binary()                             # Bytes

# Collections
st.lists(st.integers())                 # Lists of integers
st.dictionaries(st.text(), st.integers()) # Dict[str, int]
st.sets(st.text(), min_size=1)          # Non-empty sets
st.tuples(st.text(), st.integers())     # (str, int) tuples

# Special
st.one_of(st.integers(), st.text())     # Union types
st.none()                               # None values
st.uuids()                              # UUID objects
st.datetimes()                          # datetime objects
```

**See [references/strategies-reference.md](references/strategies-reference.md) for complete strategy catalog.**

### The @given Decorator

The `@given` decorator runs your test function with generated data:

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition should be commutative."""
    assert a + b == b + a

@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    """Sorting preserves list length."""
    assert len(sorted(lst)) == len(lst)
```

**Default behavior:** Runs 100 examples (configurable via settings).

### Shrinking

When Hypothesis finds a failing test, it **automatically minimizes** the input:

```python
@given(st.lists(st.integers()))
def test_sum_positive(lst):
    assert sum(lst) >= 0  # Fails for negative numbers

# Hypothesis reports: lst=[-1]
# NOT lst=[-9999, -42, -1, -8888] (the random case it found)
```

**This is invaluable for debugging** - you get the minimal failing case, not a complex random one.

### Custom Strategies

For complex domain objects, build custom strategies with `@composite`:

```python
from hypothesis import strategies as st
from hypothesis.strategies import composite

@composite
def valid_emails(draw):
    """Generate valid email addresses."""
    username = draw(st.text(alphabet=st.characters(
        whitelist_categories=('Ll', 'Lu', 'Nd'),
        min_codepoint=ord('a')
    ), min_size=1, max_size=20))

    domain = draw(st.text(alphabet=st.characters(
        whitelist_categories=('Ll',),
        min_codepoint=ord('a')
    ), min_size=1, max_size=15))

    tld = draw(st.sampled_from(['com', 'org', 'net', 'io']))

    return f"{username}@{domain}.{tld}"

@given(valid_emails())
def test_email_parsing(email):
    """Test parsing of valid email addresses."""
    assert '@' in email
    assert '.' in email.split('@')[1]
```

**See [references/patterns-catalog.md](references/patterns-catalog.md) for more custom strategy patterns.**

## Step-by-Step Workflow

### Step 1: Install Hypothesis

```bash
# Add to project dependencies
uv add --dev hypothesis

# Verify installation
python -c "import hypothesis; print(hypothesis.__version__)"
```

### Step 2: Identify Properties to Test

Look for:
- **Invariants** - Things that should always be true
- **Roundtrips** - Serialize → Deserialize → Should equal original
- **Idempotency** - Operation twice = operation once
- **Commutativity** - Order doesn't matter
- **Consistency** - Related operations agree

**Example:** Testing a JSON serializer:
- Property: `parse(serialize(obj)) == obj` (roundtrip)
- Property: `serialize(obj)` returns valid JSON string
- Property: All serialized objects are parseable

### Step 3: Choose Strategies

Map your data types to Hypothesis strategies:

```python
# Simple types
int → st.integers()
str → st.text()
bool → st.booleans()

# Collections
List[int] → st.lists(st.integers())
Dict[str, int] → st.dictionaries(st.text(), st.integers())
Optional[str] → st.one_of(st.text(), st.none())

# Domain models (Pydantic)
MyModel → builds(MyModel)
```

### Step 4: Write Property Test

```python
from hypothesis import given, strategies as st

@given(st.dictionaries(st.text(), st.text()))
def test_json_roundtrip(data):
    """Property: All dicts should roundtrip through JSON."""
    import json
    serialized = json.dumps(data)
    parsed = json.loads(serialized)
    assert parsed == data
```

### Step 5: Run and Observe

```bash
# Run property test
pytest tests/test_properties.py -v

# Show statistics
pytest --hypothesis-show-statistics

# Reproduce specific failure
pytest --hypothesis-seed=12345
```

### Step 6: Refine if Needed

If test generates invalid inputs:
- Add constraints to strategy
- Use `assume()` to filter (sparingly)
- Create custom strategy with `@composite`

```python
from hypothesis import given, assume, strategies as st

@given(st.lists(st.integers()))
def test_with_filtering(lst):
    # AVOID: Too much filtering (slow)
    assume(len(lst) > 0)  # Better: st.lists(st.integers(), min_size=1)
    assume(all(x >= 0 for x in lst))  # Better: st.lists(st.integers(min_value=0))
    ...
```

## Common Property Patterns

### 1. Roundtrip Testing

**Pattern:** Serialize → Deserialize → Should equal original

```python
@given(builds(MyModel))
def test_model_json_roundtrip(model):
    """Property: Models roundtrip through JSON."""
    json_str = model.model_dump_json()
    restored = MyModel.model_validate_json(json_str)
    assert restored == model
```

### 2. Invariant Testing

**Pattern:** Some property should always hold

```python
@given(st.lists(st.integers()))
def test_sort_ordered(lst):
    """Property: Sorted list should be in ascending order."""
    sorted_lst = sorted(lst)
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

### 3. Idempotency Testing

**Pattern:** Operation twice = operation once

```python
@given(st.text())
def test_normalize_idempotent(text):
    """Property: Normalizing twice gives same result."""
    once = normalize(text)
    twice = normalize(once)
    assert once == twice
```

### 4. Commutativity Testing

**Pattern:** Order doesn't matter

```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Property: a + b == b + a."""
    assert a + b == b + a
```

### 5. Consistency Testing

**Pattern:** Different paths to same result should agree

```python
@given(st.lists(st.integers()))
def test_sum_consistency(lst):
    """Property: Manual sum equals built-in sum."""
    manual_sum = 0
    for x in lst:
        manual_sum += x
    assert manual_sum == sum(lst)
```

**See [references/patterns-catalog.md](references/patterns-catalog.md) for 15+ common patterns.**

## Integration with pytest

Hypothesis works seamlessly with pytest:

```python
import pytest
from hypothesis import given, strategies as st

# Combine with fixtures
@pytest.fixture
def temp_config(tmp_path):
    """Fixture providing temp configuration."""
    return Config(data_dir=tmp_path)

@given(st.text())
def test_with_fixture(temp_config, text):
    """Hypothesis + fixture: temp_config from fixture, text from Hypothesis."""
    result = process_with_config(temp_config, text)
    assert result is not None
```

**Important:** Fixtures are called **once per test function**, not once per Hypothesis example (100 runs).

### pytest Command-Line Options

```bash
# Show statistics about data generation
pytest --hypothesis-show-statistics

# Use a specific Hypothesis profile
pytest --hypothesis-profile=ci

# Set verbosity level
pytest --hypothesis-verbosity=debug

# Reproduce a specific failure
pytest --hypothesis-seed=12345
```

## Async Property Testing

### Basic Async Pattern

Hypothesis works with pytest-asyncio:

```python
import pytest
from hypothesis import given, strategies as st

@pytest.mark.asyncio
@given(st.text())
async def test_async_property(text):
    """Property test for async function."""
    result = await async_process(text)
    assert isinstance(result, str)
```

### Critical: Decorator Order

**MUST follow this order:**

```python
@pytest.mark.asyncio  # Innermost (closest to function)
@given(st.text())      # Outermost
async def test_async_property(text):
    pass
```

**If you get "Hypothesis doesn't know how to run async test functions", check decorator order.**

### Example: Testing Async IPC

```python
import pytest
from hypothesis import given, strategies as st

@pytest.mark.asyncio
@given(
    command=st.sampled_from(["execute", "status", "cancel"]),
    prompt=st.text(),
    correlation_id=st.uuids().map(str)
)
async def test_ipc_command_roundtrip(command, prompt, correlation_id):
    """Property: All IPC commands should roundtrip through serialization."""
    request = create_command_request(
        command=command,
        prompt=prompt,
        correlation_id=correlation_id
    )

    import json
    serialized = json.dumps(request)
    deserialized = json.loads(serialized)

    assert deserialized == request
    assert deserialized["command"] == command
```

## Pydantic Model Testing

Hypothesis **automatically supports Pydantic models**:

```python
from hypothesis import given
from hypothesis.strategies import builds
from pydantic import BaseModel, EmailStr, PositiveFloat

class PaymentModel(BaseModel):
    amount: PositiveFloat
    email: EmailStr
    description: str

# Hypothesis automatically respects Pydantic constraints!
@given(builds(PaymentModel))
def test_payment_validation(payment):
    """Hypothesis generates valid PaymentModel instances."""
    assert payment.amount > 0
    assert '@' in payment.email
    assert isinstance(payment.description, str)
```

### Overriding Specific Fields

```python
@given(builds(
    PaymentModel,
    amount=st.floats(min_value=100, max_value=1000),
    description=st.text(min_size=10, max_size=100)
))
def test_large_payments(payment):
    """Test with payments between $100-$1000."""
    assert 100 <= payment.amount <= 1000
    assert 10 <= len(payment.description) <= 100
```

### Testing Configuration Models

```python
from hypothesis import given, strategies as st
from hypothesis.strategies import builds
from my_project.config import AgentConfig

@given(builds(AgentConfig))
def test_agent_config_invariants(config):
    """Any valid AgentConfig should satisfy these invariants."""
    assert config.agent_id is not None
    assert config.system_prompt is not None
    assert len(config.agent_id) > 0
```

## Configuration

### Profile Setup (conftest.py)

Create profiles for different environments:

```python
# tests/conftest.py
from hypothesis import settings, HealthCheck

# Configure Hypothesis profiles
settings.register_profile(
    "ci",
    max_examples=200,
    deadline=1000  # milliseconds
)

settings.register_profile(
    "dev",
    max_examples=50,
    deadline=None
)

settings.register_profile(
    "thorough",
    max_examples=1000,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow]
)

# Activate based on environment
import os
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```

### Per-Test Settings

```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=1000, deadline=None)
@given(st.integers())
def test_expensive_operation(n):
    """Run 1000 examples with no time limit."""
    result = very_slow_computation(n)
    assert result >= 0
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `max_examples` | 100 | Number of test cases to generate |
| `deadline` | 200ms | Time limit per test case |
| `suppress_health_check` | [] | Disable specific warnings |
| `verbosity` | normal | Output verbosity (quiet, normal, verbose, debug) |
| `derandomize` | False | Use deterministic randomness |

## Supporting Files

### [references/strategies-reference.md](references/strategies-reference.md)
Complete catalog of built-in Hypothesis strategies with examples:
- Basic types (integers, floats, text, binary)
- Collections (lists, sets, dicts, tuples)
- Special types (UUIDs, datetimes, emails)
- Combinators (one_of, builds, recursive)
- Advanced patterns (composite, shared, data)

### [references/patterns-catalog.md](references/patterns-catalog.md)
Common property test patterns with examples:
- Roundtrip testing (serialization, encoding)
- Invariant testing (order, size, consistency)
- Idempotency testing (normalization, deduplication)
- Commutativity testing (operations, transformations)
- State machine testing (lifecycle, protocols)

### [templates/property-test-templates.md](templates/property-test-templates.md)
Copy-paste ready templates for:
- Basic property test
- Async property test
- Pydantic model property test
- Custom strategy
- State machine test
- conftest.py Hypothesis configuration

## Expected Outcomes

### Successful Property Test Creation

```
✓ Property Tests Added

Module: tests/unit/test_ipc_protocol_properties.py
Properties tested:
  - JSON roundtrip for command requests
  - Correlation ID preservation
  - Valid command types

Generated examples: 100 per property
Edge cases found: 0 (all tests passed)

Test results:
  ✓ All properties hold
  ✓ 300 examples generated (3 properties × 100 each)
  ✓ No shrinking needed (no failures)

Configuration:
  Profile: dev (50 examples/property)
  Deadline: None (development)

Time: 2.3 seconds
Confidence: High (comprehensive input coverage)
```

### Property Test Finding Bug

```
⚠️ Property Violation Found

Test: test_json_roundtrip
Property: All dicts should roundtrip through JSON
Falsifying example: data={'key': float('inf')}

Error: JSON cannot serialize infinity
Shrinking: Reduced from complex dict to minimal case

Root cause: Missing validation for special float values
Fix required: Add constraint to strategy or handle inf/nan

Next steps:
  1. Decide: Should code handle inf/nan or reject them?
  2. Update strategy: st.floats(allow_nan=False, allow_infinity=False)
  3. OR: Add validation in serializer
  4. Re-run property tests to verify fix
```

## Requirements

**Tools needed:**
- Bash (for running tests)
- Read (for examining test files)
- Grep (for finding test patterns)
- Glob (for file discovery)
- Edit/Write (for creating/modifying tests)

**Dependencies:**
- Python 3.8+
- pytest
- hypothesis (install with: `uv add --dev hypothesis`)
- pytest-asyncio (for async tests)

**Test Framework:**
- pytest with Hypothesis integration
- pytest-asyncio for async property tests

**Knowledge:**
- Basic understanding of property-based testing concepts
- Familiarity with pytest
- Understanding of type annotations (helpful for strategies)

## Red Flags to Avoid

### ❌ WRONG: Over-Constraining Strategies
```python
# BAD: Too specific, loses property testing benefits
@given(st.integers(min_value=42, max_value=42))
def test_specific_value(n):
    assert n == 42  # This is just an example test!
```

**✅ RIGHT: Test properties that hold for all inputs**
```python
@given(st.integers())
def test_absolute_value_non_negative(n):
    assert abs(n) >= 0
```

---

### ❌ WRONG: Filtering Too Much
```python
# BAD: Rejecting most generated examples
@given(st.integers())
def test_primes(n):
    assume(is_prime(n))  # Rejects 99% of inputs!
    # ... test code
```

**✅ RIGHT: Use a strategy that generates valid inputs**
```python
@composite
def primes(draw):
    return draw(st.sampled_from([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]))

@given(primes())
def test_primes(n):
    # All inputs are primes
```

---

### ❌ WRONG: Testing Implementation, Not Properties
```python
# BAD: Duplicating implementation in test
@given(st.lists(st.integers()))
def test_sum_implementation(lst):
    result = sum(lst)
    # Bad: Reimplementing sum() in test
    expected = 0
    for item in lst:
        expected += item
    assert result == expected
```

**✅ RIGHT: Test properties**
```python
@given(st.lists(st.integers()))
def test_sum_commutative(lst):
    assert sum(lst) == sum(reversed(lst))

@given(st.lists(st.integers()))
def test_sum_with_zero(lst):
    assert sum(lst + [0]) == sum(lst)
```

---

### ❌ WRONG: Wrong Decorator Order for Async
```python
# BAD: Will fail with "Hypothesis doesn't know how to run async"
@given(st.text())
@pytest.mark.asyncio
async def test_async_property(text):
    pass
```

**✅ RIGHT: pytest.mark.asyncio innermost**
```python
@pytest.mark.asyncio
@given(st.text())
async def test_async_property(text):
    pass
```

---

### ❌ WRONG: Not Using Pydantic Integration
```python
# BAD: Manually constructing Pydantic models
@given(
    amount=st.floats(min_value=0.01),
    email=st.text(),  # Not valid emails!
)
def test_payment(amount, email):
    payment = PaymentModel(amount=amount, email=email)  # Will fail validation
```

**✅ RIGHT: Use builds() for Pydantic models**
```python
@given(builds(PaymentModel))
def test_payment(payment):
    # Hypothesis automatically generates valid instances
    assert payment.amount > 0
```

---

### ❌ WRONG: Mixing Hypothesis with pytest.mark.parametrize
```python
# BAD: Redundant - Hypothesis already does this
@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
@given(st.integers())
def test_redundant(n, generated_int):
    # Why both? Pick one approach!
    pass
```

**✅ RIGHT: Use Hypothesis for data generation**
```python
@given(st.integers(min_value=1, max_value=5))
def test_small_integers(n):
    assert 1 <= n <= 5
```

## Notes

**Start Small:**
1. Pick one simple function to test
2. Write one property test
3. Run it, observe results
4. Expand to more properties

**Think in Properties, Not Examples:**
- Instead of: "sort([3,1,2]) == [1,2,3]"
- Think: "sorted list should be ordered" (invariant)
- Or: "sorting twice == sorting once" (idempotency)
- Or: "sort preserves all elements" (conservation)

**Hypothesis Finds Edge Cases You Miss:**
- Empty collections
- Single elements
- Duplicates
- Very large/small numbers
- Unicode edge cases
- Boundary conditions

**When Property Tests Fail:**
1. Read the minimal failing example (shrinking gives you this)
2. Understand why the property doesn't hold
3. Decide: Is code wrong or property too strict?
4. Fix and re-run

**Further Reading:**
- Hypothesis documentation: https://hypothesis.readthedocs.io/
- Strategies reference: [references/strategies-reference.md](references/strategies-reference.md)
- Pattern catalog: [references/patterns-catalog.md](references/patterns-catalog.md)
