---
name: stepwise-testing
description: Verify every step exhaustively - debug with detailed tracing and test each component individually to leave no stone unturned
license: MIT
compatibility: opencode
metadata:
  audience: developers, QA engineers
  category: testing
---

# Stepwise Testing

Exhaustive verification approach that validates every step, line of execution, and component - not just end-to-end outcomes. When debugging, instrument each step; when testing, verify every intermediate state; never assume, always verify.

## When to use me

Use stepwise testing when:
- **Debugging complex failures** and need to trace exactly where things break
- **Implementing multi-step workflows** where each step must be verified
- **Testing critical path scenarios** in production code
- **Investigating intermittent bugs** that require exhaustive tracing
- **Building complex features** where components interact
- **Establishing test coverage** for new codebases

## What I do

### 1. Debug Instrumentation
- Add print/log statements at **every decision point, function entry/exit, and state change**
- Trace data flow through the entire call stack
- Log variable states before/after each transformation
- Capture intermediate results for comparison

### 2. Stepwise Verification
- Test **each function individually** with edge cases and boundary conditions
- Verify **data transformations** at each step, not just final output
- Ensure **state transitions** only occur under valid conditions
- Validate **side effects** (file IO, network calls, memory operations)

### 3. Component Isolation
- Break complex flows into **testable units**
- Mock dependencies to verify **interface contracts**
- Test **error paths** and failure scenarios for each component
- Verify **resource lifecycle** (cleanup, leaks, handles)

### 4. Exhaustive Coverage
- Don't skip steps just because they "should" work
- Verify **assumptions** about third-party libraries/APIs
- Test **concurrency and race conditions** where applicable
- Validate **error handling** and exception recovery

## Examples

### Debugging with Stepwise Tracing

Before (missing details):
```python
def process_user(data):
    validated = validate(data)
    result = transform(validated)
    save(result)
    return result
```

After (stepwise instrumentation):
```python
def process_user(data):
    print(f"[ENTER] process_user with data: {data}")
    
    # Step 1: Validation
    print("[STEP] Starting validation...")
    validated = validate(data)
    print(f"[AFTER] validate returned: {validated}, keys: {validated.keys()}")
    
    # Step 2: Transformation
    print("[STEP] Starting transformation...")
    result = transform(validated)
    print(f"[AFTER] transform returned: {result}")
    
    # Step 3: Persistence
    print("[STEP] About to save result...")
    save(result)
    print(f"[SUCCESS] Saved result")
    
    print(f"[EXIT] process_user returning: {result}")
    return result
```

### Testing Each Step Individually

Don't just test the final output:
```python
# Bad - only tests final result
def test_process_user():
    result = process_user({"name": "test"})
    assert result["status"] == "success"
```

Test each intermediate step:
```python
# Good - tests each transformation
def test_validate_step():
    invalid_data = {"name": ""}
    result = validate(invalid_data)
    assert result is None or get_error(result) == "name_required"
    
def test_transform_step():
    validated = {"name": "test", "email": "test@example.com"}
    result = transform(validated)
    assert result is not None
    assert "status" in result
    assert "processed_at" in result  # Timestamp added
    
def test_save_step():
    result = {"name": "test", "email": "test@example.com"}
    saved_id = save(result)
    assert isinstance(saved_id, str)
    # Verify actually saved
    retrieved = retrieve(saved_id)
    assert retrieved == result
```

### Verifying Complex Multi-Step Workflows

```python
# Example: Payment processing flow
# Step 1: Validate payment method
print("[1/6] Validating payment method...")
payment_method = validate_payment_method(card_data)
print(f"    Result: {payment_method.get('status', 'invalid')}")
assert payment_method["status"] == "valid", f"Invalid: {payment_method}"

# Step 2: Check balance/funds
print("[2/6] Checking available balance...")
balance = check_balance(payment_method["account_id"])
print(f"    Balance: {balance}/ Required: {amount}")
assert balance >= amount, f"Insufficient funds"

# Step 3: Hold funds
print("[3/6] Placing funds on hold...")
hold_id = place_hold(payment_method["account_id"], amount)
print(f"    Hold ID: {hold_id}")
assert hold_id is not None

# Step 4: Execute transfer
print("[4/6] Executing transfer...")
transfer = execute_transfer(hold_id, recipient_account)
print(f"    Transfer ID: {transfer['id']}")
assert transfer["status"] == "pending"

# Step 5: Verify receipt
print("[5/6] Verifying recipient received funds...")
recipient_check = check_transaction(transfer["id"])
print(f"    Recipient status: {recipient_check['status']}")
assert recipient_check["status"] == "completed"

# Step 6: Finalize
print("[6/6] Finalizing and releasing hold...")
finalize(transfer["id"])
print("    ✅ Complete")
```

### Network Request Verification

Don't assume a library works:
```python
# Don't just use requests library
response = requests.get(url)
assert response.ok

# Verify each step:
print("[1/3] Testing DNS resolution...")
import socket
try:
    ip = socket.gethostbyname(urlparse(url).hostname)
    print(f"    Resolved to: {ip}")
except socket.gaierror as e:
    print(f"    ❌ DNS failed: {e}")
    raise

print("[2/3] Testing TCP connection...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
try:
    sock.connect((ip, 443))
    print(f"    ✅ Connected")
except Exception as e:
    print(f"    ❌ Connection failed: {e}")
    raise
finally:
    sock.close()

print("[3/3] Testing HTTP handshake...")
response = requests.get(url, timeout=10)
print(f"    Status: {response.status_code}")
print(f"    Headers: {dict(response.headers)}")
print(f"    Body length: {len(response.text)}")
assert response.ok, f"HTTP error: {response.status_code}"
```

## Output format

Stepwise testing produces detailed, line-by-line output:

```
[STEP 1/5] Validating input parameters...
    Input: {'user_id': 123, 'amount': 50.0}
    ✅ All required fields present
    ✅ Data types valid

[STEP 2/5] Checking user permissions...
    User role: 'standard'
    Permission check: 'can_withdraw' -> False
    ❌ Permission denied
    [FAIL] User 123 cannot withdraw permissions
```

## Debugging Patterns

### Pattern 1: Function Entry/Exit
```python
def function_name(arg1, arg2):
    print(f"[ENTER] function_name: arg1={arg1}, arg2={arg2}")
    try:
        result = # ... work ...
        print(f"[EXIT] function_name -> {result}")
        return result
    except Exception as e:
        print(f"[ERROR] function_name: {e}")
        raise
```

### Pattern 2: Loop Instrumentation
```python
for i, item in enumerate(items):
    print(f"[LOOP] Iteration {i}/{len(items)}: item={item}")
    result = process(item)
    print(f"[LOOP] Result: {result}")
```

### Pattern 3: State Changes
```python
print(f"[STATE] Before: counter={counter}")
counter += 1
print(f"[STATE] After: counter={counter}")
```

### Pattern 4: Conditional Branches
```python
if condition:
    print(f"[BRANCH] Taking 'if' path: condition={condition}")
    # ... work ...
else:
    print(f"[BRANCH] Taking 'else' path: condition={condition}")
    # ... work ...
```

## Testing Patterns

### Pattern 1: Unit Test Each Function
```python
def test_validate():
    # Valid input
    assert validate({"name": "test"}) is not None
    # Missing field
    assert validate({"missing": True}) is None
    # Invalid type
    assert validate({"name": []}) is None

def test_transform():
    # Normal case
    assert transform({"name": "test"}) is not None
    # Test data transformation
    result = transform({"name": "test"})
    assert "processed_at" in result
```

### Pattern 2: Verify Assumptions
```python
def test_third_party_behavior():
    """Don't assume the library behaves as documented"""
    response = library.action(input)
    # Verify the actual behavior
    assert response.structure == expected
    assert response.timing < threshold
```

### Pattern 3: Edge Cases
```python
def test_edge_cases():
    # Empty input
    assert transform({}) == expected_empty
    # Very large input
    assert transform(large_data) == expected_large
    # Unicode/special chars
    assert transform({"name": "🚀"}) == expected_unicode
```

## Implementation Guidelines

### 1. Add Instrumentation First
Before adding complex logic, instrument the simple version:
```python
def simple():
    print("[START]")
    print("[STEP 1] ...")
    print("[STEP 2] ...")
    print("[DONE]")
```

### 2. Test Each Component
Never combine untested components. Test separately first:
```python
# Test A alone
result_a = component_a()
# Test B alone
result_b = component_b(result_a)
# Only then integrate
integrated = integrate(result_b)
```

### 3. Verify External Dependencies
Don't trust third-party code:
```python
# Verify it actually works
test_result = external_library.call(test_input)
assert test_result == expected_external_behavior
```

### 4. Capture Evidence
Save intermediate states for inspection:
```python
debug_states = []
for step in workflow:
    state_before = copy.deepcopy(current_state)
    result = execute(step)
    state_after = copy.deepcopy(current_state)
    debug_states.append({
        "step": step,
        "before": state_before,
        "result": result,
        "after": state_after
    })
```

## Notes

- **Stepwise testing takes time** but saves debugging time later
- **Instrument everywhere** - you can remove it after debugging  
- **Test assumptions** about libraries/frameworks - don't assume documentation is accurate
- **Log both success and failure** - knowing where it succeeded is as important as where it failed
- **Keep it granular** - one assertion/verification per line where practical
- **Version control the instrumentation** - you can comment it out but keep it for future debugging
- **Use debug levels** - ERROR, WARN, INFO, DEBUG, TRACE for different detail levels
