---
name: validate
description: Use when running comprehensive project validation including tests, type checking, linting, API connectivity checks, and server startup verification
---

Run comprehensive validation of the project to ensure all tests, type checks, linting, and deployments are working correctly.

Execute the following commands in sequence and report results:

## 1. Test Suite

```bash
uv run pytest -v
```

**Expected:** All tests pass (currently 34 tests), execution time < 1 second

## 2. Type Checking

```bash
uv run mypy app/
```

**Expected:** "Success: no issues found in X source files"

```bash
uv run pyright app/
```

**Expected:** "0 errors, 0 warnings, 0 informations"

## 3. API Integration Tests

### Purpose
Verify external API integrations work correctly with real API calls.

### Prerequisites
- All required API keys configured in environment
- APIs must be accessible (network connectivity)
- Test accounts/projects exist in external services

### Validation Steps

#### 3.1 Configuration Validation
Check that all required API configuration is present:

```bash
# Check environment variables
env | grep -E "(API_KEY|API_TOKEN|LANGSMITH|OPENAI)"

# Verify config file (if applicable)
cat backend/.env | grep -E "^[A-Z_]*API"
```

**Expected:**
- All required API keys: SET (not empty)
- Configuration file readable and valid

**If Failed:**
- Error: Missing API keys
- Action: Check .env file, environment setup

#### 3.2 API Connectivity Tests
Test that each API is accessible and credentials work:

```bash
# LangSmith connectivity test
python -c "
from langsmith import Client
client = Client()
projects = list(client.list_projects(limit=1))
print(f'✓ LangSmith: {len(projects)} projects')
"

# OpenAI API test
python -c "
from openai import OpenAI
client = OpenAI()
models = client.models.list(limit=1)
print(f'✓ OpenAI: API accessible')
"
```

**Expected:**
- Each API returns successful response
- Credentials validated
- No authentication errors

**If Failed:**
- Error: Invalid API key / Unauthorized
- Action: Verify API key in dashboard, regenerate if needed

#### 3.3 API Response Format Verification
Verify API responses match expected format:

```bash
# Test actual API call and response structure
python -c "
# Test streaming response event types
# Test data structure
# Verify against documented schema
"
```

**Expected:**
- Response matches documented schema
- Event types match API documentation
- Data structure is parseable

**If Failed:**
- Error: Unexpected response format
- Action: Check API version, update integration code

#### 3.4 Integration Flow Test
Test complete integration flow end-to-end:

```bash
# Example: Create trace, verify it appears
# Example: Make API call, verify logging
# Example: Test error handling
```

**Expected:**
- Complete flow executes successfully
- Data persists correctly
- No integration errors

**If Failed:**
- Error: Integration flow broken
- Action: Debug with verbose logging, check API status page

### Summary
```
API Integration Tests:
- Configuration: ✅/❌
- Connectivity: ✅/❌
- Response Format: ✅/❌
- Integration Flow: ✅/❌
```

**Note:** Skip this section if no external APIs are used.

## 4. Linting

```bash
uv run ruff check .
```

**Expected:** "All checks passed!"

### 4.1 Async Generator Pattern Check

Check for async generators without finally blocks (potential resource leak):

```bash
# Find async generators
grep -rn "async def.*yield" --include="*.py" . | grep -v test_ | grep -v "#" > /tmp/async_gens.txt

# For each async generator, check if it has a finally block
if [ -s /tmp/async_gens.txt ]; then
    echo "Checking async generators for finally blocks..."
    while read -r line; do
        file=$(echo "$line" | cut -d: -f1)
        linenum=$(echo "$line" | cut -d: -f2)
        # Check next 30 lines for finally block
        if ! sed -n "${linenum},$((linenum+30))p" "$file" | grep -q "finally:"; then
            echo "⚠️  Potential missing finally block: $line"
        fi
    done < /tmp/async_gens.txt
fi
```

**Expected:** No warnings about missing finally blocks (or manual verification that resource cleanup is handled elsewhere)

**Why:** Async generators need finally blocks to guarantee cleanup (trace closure, DB connections, file handles) even when interrupted

## 5. Local Server Validation

Start the server in background:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8123 &
```

Wait 3 seconds for startup, then test endpoints:

```bash
curl -s http://localhost:8123/ | python3 -m json.tool
```

**Expected:** JSON response with app name, version, and docs link

```bash
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8123/docs
```

**Expected:** HTTP Status: 200

```bash
curl -s -i http://localhost:8123/ | head -10
```

**Expected:** Headers include `x-request-id` and status 200

Stop the server:

```bash
lsof -ti:8123 | xargs kill -9 2>/dev/null || true
```

## 6. Summary Report

After all validations complete, provide a summary report with:

```
Validation Results:
1. Test Suite: ✅/❌ (X tests passed in Y.Zs)
2. Type Checking: ✅/❌ (mypy + pyright passed)
3. API Integration: ✅/❌/⊘ (connectivity + response validation)
4. Linting: ✅/❌ (ruff check passed)
5. Local Server: ✅/❌ (server starts, endpoints respond)

Overall Status: ✅ PASS / ❌ FAIL / ⚠ PARTIAL
```

Note: ⊘ = Skipped (no external APIs)

- Any errors or warnings encountered
- Overall health assessment (PASS/FAIL)

**Format the report clearly with sections and status indicators (✅/❌)**