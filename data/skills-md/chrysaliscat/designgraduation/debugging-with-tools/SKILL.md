---
name: debugging-with-tools
description: Use when encountering bugs or test failures - systematic debugging using debuggers, internet research, and agents to find root cause before fixing
---

<skill_overview>
Random fixes waste time and create new bugs. Always use tools to understand root cause BEFORE attempting fixes. Symptom fixes are failure.
</skill_overview>

<rigidity_level>
MEDIUM FREEDOM - Must complete investigation phases (tools → hypothesis → test) before fixing.

Can adapt tool choice to language/context. Never skip investigation or guess at fixes.
</rigidity_level>

<quick_reference>

| Phase | Tools to Use | Output |
|-------|--------------|--------|
| **1. Investigate** | Error messages, internet-researcher agent, debugger, codebase-investigator | Root cause understanding |
| **2. Hypothesize** | Form theory based on evidence (not guesses) | Testable hypothesis |
| **3. Test** | Validate hypothesis with minimal change | Confirms or rejects theory |
| **4. Fix** | Implement proper fix for root cause | Problem solved permanently |

**FORBIDDEN:** Skip investigation → guess at fix → hope it works
**REQUIRED:** Tools → evidence → hypothesis → test → fix

**Key agents:**
- `internet-researcher` - Search error messages, known bugs, solutions
- `codebase-investigator` - Understand code structure, find related code
- `test-runner` - Run tests without output pollution

</quick_reference>

<when_to_use>
**Use for ANY technical issue:**
- Test failures
- Bugs in production or development
- Unexpected behavior
- Build failures
- Integration issues
- Performance problems

**ESPECIALLY when:**
- "Just one quick fix" seems obvious
- Under time pressure (emergencies make guessing tempting)
- Error message is unclear
- Previous fix didn't work
</when_to_use>

<the_process>

## Phase 1: Tool-Assisted Investigation

**BEFORE attempting ANY fix, gather evidence with tools:**

### 1. Read Complete Error Messages

- Entire error message (not just first line)
- Complete stack trace (all frames)
- Line numbers, file paths, error codes
- Stack traces show exact execution path

### 2. Search Internet FIRST (Use internet-researcher Agent)

**Dispatch internet-researcher with:**
```
"Search for error: [exact error message]
- Check Stack Overflow solutions
- Look for GitHub issues in [library] version [X]
- Find official documentation explaining this error
- Check if this is a known bug"
```

**What agent should find:**
- Exact matches to your error
- Similar symptoms and solutions
- Known bugs in your dependency versions
- Workarounds that worked for others

### 3. Use Debugger to Inspect State

**Claude cannot run debuggers directly. Instead:**

**Option A - Recommend debugger to user:**
```
"Let's use lldb/gdb/DevTools to inspect state at error location.
Please run: [specific commands]
When breakpoint hits: [what to inspect]
Share output with me."
```

**Option B - Add instrumentation Claude can add:**
```rust
// Add logging
println!("DEBUG: var = {:?}, state = {:?}", var, state);

// Add assertions
assert!(condition, "Expected X but got {:?}", actual);
```

### 4. Investigate Codebase (Use codebase-investigator Agent)

**Dispatch codebase-investigator with:**
```
"Error occurs in function X at line Y.
Find:
- How is X called? What are the callers?
- What does variable Z contain at this point?
- Are there similar functions that work correctly?
- What changed recently in this area?"
```

## Phase 2: Form Hypothesis

**Based on evidence (not guesses):**

1. **State what you know** (from investigation)
2. **Propose theory** explaining the evidence
3. **Make prediction** that tests the theory

**Example:**
```
Known: Error "null pointer" at auth.rs:45 when email is empty
Theory: Empty email bypasses validation, passes null to login()
Prediction: Adding validation before login() will prevent error
Test: Add validation, verify error doesn't occur with empty email
```

**NEVER:**
- Guess without evidence
- Propose fix without hypothesis
- Skip to "try this and see"

## Phase 3: Test Hypothesis

**Minimal change to validate theory:**

1. Make smallest change that tests hypothesis
2. Run test/reproduction case
3. Observe result

**If confirmed:** Proceed to Phase 4
**If rejected:** Return to Phase 1 with new information

## Phase 4: Implement Fix

**After understanding root cause:**

1. Write test reproducing bug (RED phase - use test-driven-development skill)
2. Implement proper fix addressing root cause
3. Verify test passes (GREEN phase)
4. Run full test suite (regression check)
5. Commit fix

**The fix should:**
- Address root cause (not symptom)
- Be minimal and focused
- Include test preventing regression

</the_process>

<examples>

<example>
<scenario>Developer encounters test failure, immediately tries "obvious" fix without investigation</scenario>

<code>
Test error:
```
FAIL: test_login_expired_token
AssertionError: Expected Err(TokenExpired), got Ok(User)
```

Developer thinks: "Obviously the token expiration check is wrong"

Makes change without investigation:
```rust
// "Fix" - just check if token is expired
if token.expires_at < now() {
    return Err(AuthError::TokenExpired);
}
```

Commits without testing other cases.
</code>

<why_it_fails>
**No investigation:**
- Didn't read error completely
- Didn't check what `expires_at` contains
- Didn't debug to see token state
- Didn't search for similar issues

**What actually happened:** Token `expires_at` was being parsed incorrectly, always showing future date. The "fix" adds dead code that never runs.

**Result:** Bug not fixed, new dead code added, time wasted.
</why_it_fails>

<correction>
**Phase 1 - Investigate with tools:**

```bash
# 1. Read complete error
FAIL: test_login_expired_token at line 45
Expected: Err(TokenExpired)
Got: Ok(User { id: 123 })
Token: { expires_at: "2099-01-01", ... }
```

**Dispatch internet-researcher:**
```
"Search for: token expiration always showing future date
- Check date parsing bugs
- Look for timezone issues
- Find JWT expiration handling"
```

**Add instrumentation:**
```rust
println!("DEBUG: expires_at = {:?}, now = {:?}, expired = {:?}",
         token.expires_at, now(), token.expires_at < now());
```

**Run test again:**
```
DEBUG: expires_at = 2099-01-01T00:00:00Z, now = 2024-01-15T10:30:00Z, expired = false
```

**Phase 2 - Hypothesis:**
"Token `expires_at` is being set to 2099, not actual expiration. Problem is in token creation, not validation."

**Phase 3 - Test:**
Check token creation code:
```rust
// Found the bug!
fn create_token() -> Token {
    Token {
        expires_at: "2099-01-01".parse()?, // HARDCODED!
        ...
    }
}
```

**Phase 4 - Fix root cause:**
```rust
fn create_token(duration: Duration) -> Token {
    Token {
        expires_at: now() + duration,  // Correct
        ...
    }
}
```

**Result:** Root cause fixed, test passes, no dead code.
</correction>
</example>

<example>
<scenario>Developer skips internet search, reinvents solution to known problem</scenario>

<code>
Error:
```
error: linking with `cc` failed: exit status: 1
ld: symbol(s) not found for architecture arm64
```

Developer thinks: "Must be a linking issue, I'll add flags"

Spends 2 hours trying different linker flags:
```toml
[target.aarch64-apple-darwin]
rustflags = ["-C", "link-arg=-undefined dynamic_lookup"]
# Doesn't work, tries more flags...
```
</code>

<why_it_fails>
**Skipped internet search:**
- This is a common error with known solutions
- Stack Overflow has exact fix
- Official docs explain the issue
- Wasted 2 hours reinventing solution

**Why it happens:** Impatience, thinking "I can figure this out faster"
</why_it_fails>

<correction>
**Dispatch internet-researcher FIRST:**

```
"Search for: 'symbol not found for architecture arm64' Rust linking
- Check Stack Overflow solutions
- Look for Xcode/macOS specific fixes
- Find Cargo configuration for Apple Silicon"
```

**Agent returns (30 seconds):**
```
Found on Stack Overflow (2.4k upvotes):
This occurs when Xcode Command Line Tools aren't installed or outdated.

Solution:
xcode-select --install

Or update existing:
softwareupdate --all --install --force
```

**Apply solution:**
```bash
xcode-select --install
# Wait for installation
cargo build
# Success!
```

**Result:** Fixed in 5 minutes, not 2 hours.
</correction>
</example>

<example>
<scenario>Developer fixes symptom without understanding root cause, bug returns different way</scenario>

<code>
Bug: Users can delete other users' posts

Developer notices: DELETE /posts/:id doesn't check ownership

"Fix":
```python
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, user: User):
    post = get_post(post_id)
    if post.author_id != user.id:
        raise Forbidden()
    delete(post)
```

Bug "fixed"... but bug report comes back: "Users can edit other users' posts"
</code>

<why_it_fails>
**Symptom fix:**
- Fixed DELETE endpoint
- Didn't investigate root cause
- Didn't check other endpoints

**Root cause:** No authorization middleware checking ownership across ALL endpoints.

**Result:** Whack-a-mole fixing symptoms, not the underlying issue.
</why_it_fails>

<correction>
**Phase 1 - Investigate with codebase-investigator:**

```
"User can delete other users' posts. Investigate:
- What authorization exists across all post endpoints?
- Is there a pattern for ownership checks?
- Which other endpoints access posts?
- Is there middleware handling this?"
```

**Agent reports:**
```
Found:
- DELETE /posts/:id - NO ownership check
- PUT /posts/:id - NO ownership check
- GET /posts/:id - NO ownership check (allows viewing private posts!)
- No authorization middleware found
- Similar pattern in comments, likes endpoints
```

**Phase 2 - Hypothesis:**
"Missing authorization layer. Need middleware checking resource ownership across ALL endpoints."

**Phase 4 - Fix root cause:**
```python
# Add authorization middleware
class OwnershipMiddleware:
    def check_ownership(self, resource, user):
        if resource.author_id != user.id:
            raise Forbidden()

# Apply to all endpoints
@app.delete("/posts/{post_id}")
@require_ownership(Post)
def delete_post(...):
    ...

@app.put("/posts/{post_id}")
@require_ownership(Post)
def update_post(...):
    ...
```

**Result:** Root cause fixed, ALL endpoints secured, not just one symptom.
</correction>
</example>

</examples>

<critical_rules>

## Rules That Have No Exceptions

1. **Tools before fixes** → Never guess without investigation
   - Use internet-researcher for errors
   - Use debugger or instrumentation for state
   - Use codebase-investigator for context

2. **Evidence-based hypotheses** → Not guesses or hunches
   - State what tools revealed
   - Propose theory explaining evidence
   - Make testable prediction

3. **Test hypothesis before fixing** → Minimal change to validate
   - Smallest change that tests theory
   - Observe result
   - If wrong, return to investigation

4. **Fix root cause, not symptom** → One fix, many symptoms prevented
   - Understand why problem occurred
   - Fix the underlying issue
   - Don't play whack-a-mole

## Common Excuses

All of these mean: Stop, use tools to investigate:
- "The fix is obvious"
- "I know what this is"
- "Just a quick try"
- "No time for debugging"
- "Error message is clear enough"
- "Internet search will take too long"

</critical_rules>

<verification_checklist>

Before proposing any fix:
- [ ] Read complete error message (not just first line)
- [ ] Dispatched internet-researcher for unclear errors
- [ ] Used debugger or added instrumentation to inspect state
- [ ] Dispatched codebase-investigator to understand context
- [ ] Formed hypothesis based on evidence (not guesses)
- [ ] Tested hypothesis with minimal change
- [ ] Verified hypothesis confirmed before fixing

Before committing fix:
- [ ] Written test reproducing bug (RED phase)
- [ ] Verified test fails before fix
- [ ] Implemented fix addressing root cause
- [ ] Verified test passes after fix (GREEN phase)
- [ ] Ran full test suite (regression check)

</verification_checklist>

<integration>

**This skill calls:**
- internet-researcher (search errors, known bugs, solutions)
- codebase-investigator (understand code structure, find related code)
- test-driven-development (write test for bug, implement fix)
- test-runner (run tests without output pollution)

**This skill is called by:**
- fixing-bugs (complete bug fix workflow)
- root-cause-tracing (deep debugging for complex issues)
- Any skill when encountering unexpected behavior

**Agents used:**
- hyperpowers:internet-researcher (search for error solutions)
- hyperpowers:codebase-investigator (understand codebase context)
- hyperpowers:test-runner (run tests, return summary only)

</integration>

<resources>

**Detailed guides:**
- [Debugger reference](resources/debugger-reference.md) - LLDB, GDB, DevTools commands
- [Debugging session example](resources/debugging-session-example.md) - Complete walkthrough

**When stuck:**
- Error unclear → Dispatch internet-researcher with exact error text
- Don't understand code flow → Dispatch codebase-investigator
- Need to inspect runtime state → Recommend debugger to user or add instrumentation
- Tempted to guess → Stop, use tools to gather evidence first

</resources>
