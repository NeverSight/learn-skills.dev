---
name: browser-strategy-management
description: Use browser automation to enable/disable trading strategies and correct API configurations in OpenAlgo web UI. Use when managing strategies via web interface, enabling/disabling strategies, configuring API keys, or troubleshooting strategy access issues.
---

# Browser Strategy Management

Automate strategy management and API configuration through the OpenAlgo web interface using browser automation.

## Quick Start

**Default URLs:**
- Strategy Management: `http://127.0.0.1:5001/python`
- API Key Configuration: `http://127.0.0.1:5001/apikey`
- Login/Auth: `http://127.0.0.1:5001/auth/login`

**Common Ports:**
- Port 5001: Default OpenAlgo instance
- Port 5002: Alternative instance (DHAN-specific)

## Browser Automation Workflow

### 1. Initialize Browser Session

```python
# Check existing tabs first
browser_tabs(action="list")

# Navigate to strategy page
browser_navigate(url="http://127.0.0.1:5001/python")

# Lock browser for interactions
browser_lock()

# Get page snapshot to see structure
browser_snapshot()
```

### 2. Handle Authentication

If redirected to login page:

```python
# Check if login is required
browser_snapshot()  # Look for login form

# Fill login credentials if needed
browser_fill(selector="input[name='email']", value="user@example.com")
browser_fill(selector="input[name='password']", value="password")
browser_click(selector="button[type='submit']")

# Wait for navigation
browser_wait_for(selector=".strategy-card", timeout=5000)
```

### 3. Enable/Disable Strategies

**Find Strategy by Name:**

```python
# Search for strategy name in page
browser_search(query="strategy_name_here")

# Or use snapshot to find strategy card
browser_snapshot()  # Look for strategy cards with name
```

**Start Strategy:**

```python
# Find the Start button for specific strategy
# Strategy cards contain buttons with onclick="startStrategy('ID')"
browser_click(selector="button:has-text('Start')", 
              options={"all": False, "timeout": 3000})

# Wait for status change
browser_wait_for(selector=".badge-success", timeout=5000)
```

**Stop Strategy:**

```python
# Find the Stop button
browser_click(selector="button:has-text('Stop')")

# Wait for confirmation
browser_wait_for(selector=".badge-ghost", timeout=5000)
```

**Toggle Strategy (Alternative Route):**

For strategies using `/strategy/toggle/<id>` route:

```python
# Navigate to strategy view page
browser_navigate(url=f"http://127.0.0.1:5001/strategy/{strategy_id}")

# Click toggle button
browser_click(selector="button.toggle-strategy")
```

### 4. Configure API Keys

**Navigate to API Key Page:**

```python
browser_navigate(url="http://127.0.0.1:5001/apikey")
browser_snapshot()  # See available API key fields
```

**Update API Configuration:**

```python
# Fill API key field
browser_fill(selector="input[name='api_key']", value="new_api_key")

# Fill API secret if separate field
browser_fill(selector="input[name='api_secret']", value="new_api_secret")

# Save configuration
browser_click(selector="button:has-text('Save')")
```

**For Strategy-Specific Environment Variables:**

```python
# On strategy page, click environment variables icon
browser_click(selector="button[title*='Environment Variables']")

# Wait for modal to open
browser_wait_for(selector=".modal", timeout=3000)

# Fill environment variable fields
browser_fill(selector="input[name='BROKER_API_KEY']", value="key_value")
browser_fill(selector="input[name='BROKER_API_SECRET']", value="secret_value")

# Save environment variables
browser_click(selector="button:has-text('Save')")
```

### 5. Verify Strategy Status

**Check Strategy Status:**

```python
# Get snapshot to see current status badges
browser_snapshot()

# Look for status indicators:
# - .badge-success = Running
# - .badge-ghost = Stopped  
# - .badge-error = Error
# - .badge-warning = Waiting/Issue
```

**Read Strategy Status Text:**

```python
# Get text content of status badge
status_text = browser_get_attribute(
    selector=".strategy-card .badge",
    attribute="textContent"
)
```

## Common Patterns

### Pattern 1: Enable Multiple Strategies

```python
strategy_names = ["strategy1", "strategy2", "strategy3"]

browser_navigate(url="http://127.0.0.1:5001/python")
browser_lock()
browser_snapshot()

for name in strategy_names:
    # Find strategy card
    browser_search(query=name)
    browser_snapshot()  # Verify found
    
    # Check if already running
    is_running = browser_is_visible(selector=".badge-success")
    
    if not is_running:
        browser_click(selector="button:has-text('Start')")
        browser_wait_for(selector=".badge-success", timeout=10000)
```

### Pattern 2: Fix API Configuration for Stopped Strategy

```python
strategy_id = "123"

# Navigate to strategy
browser_navigate(url=f"http://127.0.0.1:5001/python")
browser_lock()

# Find strategy and stop if running
browser_search(query="strategy_name")
if browser_is_visible(selector="button:has-text('Stop')"):
    browser_click(selector="button:has-text('Stop')")
    browser_wait_for(selector="button:has-text('Start')", timeout=5000)

# Open environment variables modal
browser_click(selector="button[title*='Environment Variables']")
browser_wait_for(selector=".modal", timeout=3000)

# Update API keys
browser_fill(selector="input[name='BROKER_API_KEY']", value="correct_key")
browser_fill(selector="input[name='BROKER_API_SECRET']", value="correct_secret")

# Save and close
browser_click(selector="button:has-text('Save')")
browser_wait_for(selector=".modal", timeout=2000, visible=False)

# Start strategy
browser_click(selector="button:has-text('Start')")
```

### Pattern 3: Check and Fix Error States

```python
browser_navigate(url="http://127.0.0.1:5001/python")
browser_lock()
browser_snapshot()

# Find all error badges
error_cards = browser_search(query="Error")

for card in error_cards:
    # Check error message
    error_msg = browser_get_attribute(
        selector=".text-error",
        attribute="textContent"
    )
    
    if "master contract" in error_msg.lower():
        # Wait for master contracts (auto-resolves)
        continue
    elif "api" in error_msg.lower() or "403" in error_msg:
        # Fix API configuration
        browser_click(selector="button[title*='Environment Variables']")
        # ... update API keys
    else:
        # Clear error and restart
        browser_click(selector="button:has-text('Clear Error')")
        browser_click(selector="button:has-text('Restart')")
```

## Element Selectors Reference

### Strategy Page Elements

| Element | Selector |
|---------|----------|
| Strategy card | `.card.bg-base-100` |
| Strategy name | `.card-title` |
| Running badge | `.badge-success` |
| Stopped badge | `.badge-ghost` |
| Error badge | `.badge-error` |
| Start button | `button:has-text('Start')` |
| Stop button | `button:has-text('Stop')` |
| Environment vars icon | `button[title*='Environment Variables']` |
| Edit icon | `a[title='Edit']` |
| Logs icon | `a[title='View Logs']` |

### Modal Elements

| Element | Selector |
|---------|----------|
| Modal backdrop | `.modal-backdrop` |
| Modal content | `.modal-box` |
| Save button | `button:has-text('Save')` |
| Cancel button | `button:has-text('Cancel')` |
| Close button | `button:has-text('close')` |

## Error Handling

### Handle Login Redirects

```python
# After navigation, check if redirected to login
snapshot = browser_snapshot()
if "login" in snapshot.lower() or browser_is_visible(selector="form[action*='login']"):
    # Perform login
    browser_fill(selector="input[name='email']", value=email)
    browser_fill(selector="input[name='password']", value=password)
    browser_click(selector="button[type='submit']")
    browser_wait_for(selector=".strategy-card", timeout=10000)
```

### Handle Network Errors

```python
# Check for network errors
console_messages = browser_console_messages()
for msg in console_messages:
    if "error" in msg.lower() or "failed" in msg.lower():
        # Log error and retry
        print(f"Browser error: {msg}")
        browser_reload()
        browser_wait_for(selector=".strategy-card", timeout=10000)
```

### Handle Element Not Found

```python
# Use try-except pattern with visibility checks
if browser_is_visible(selector="button:has-text('Start')", timeout=3000):
    browser_click(selector="button:has-text('Start')")
else:
    # Strategy might already be running or not found
    browser_snapshot()  # Debug: see current state
```

## Best Practices

1. **Always lock browser before interactions:**
   ```python
   browser_lock()  # Prevents other processes from interfering
   ```

2. **Use snapshots for debugging:**
   ```python
   browser_snapshot()  # See page structure before interactions
   ```

3. **Wait for elements before clicking:**
   ```python
   browser_wait_for(selector=".strategy-card", timeout=5000)
   browser_click(selector="button")
   ```

4. **Unlock when done:**
   ```python
   browser_unlock()  # Release browser for other operations
   ```

5. **Handle port variations:**
   - Check if port 5001 is accessible, try 5002 if not
   - Verify which port OpenAlgo is running on

6. **Verify changes:**
   ```python
   # After starting strategy, verify status changed
   browser_wait_for(selector=".badge-success", timeout=10000)
   browser_snapshot()  # Confirm final state
   ```

## Troubleshooting

**Strategy button not found:**
- Use `browser_snapshot()` to see actual page structure
- Strategy might be in different section (running vs stopped)
- Check if strategy name matches exactly

**API configuration not saving:**
- Ensure strategy is stopped (running strategies are read-only)
- Check for validation errors in browser console
- Verify modal is fully loaded before filling fields

**Login issues:**
- Clear browser cookies if session expired
- Check if using correct port (5001 vs 5002)
- Verify credentials are correct

**403 Errors:**
- Usually indicates API key issues
- Update API keys in environment variables
- Restart strategy after updating keys
