---
name: error-handling-resilience
description: Performs a comprehensive error-handling review across the codebase, checking coverage, propagation, and recovery. Use when auditing how the system handles and recovers from failures.
license: CC0-1.0
metadata:
  category: code-quality
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

Evaluate this entire software package. 

Perform a comprehensive error handling review:

Evaluate:

1. ERROR HANDLING CONSISTENCY
   - Is there a centralized error handler?
   - Are errors handled uniformly?
   - Custom error classes vs generic errors?

2. ERROR CATEGORIES
   - Validation errors (400)
   - Authentication errors (401)
   - Authorization errors (403)
   - Not found errors (404)
   - Server errors (500)
   - Rate limit errors (429)
   - Are they properly categorized?

3. ASYNC ERROR HANDLING
   - Unhandled promise rejections
   - Async middleware wrapper usage
   - Callback error handling
   - Event emitter error handling

4. ERROR RECOVERY
   - Graceful degradation
   - Retry mechanisms
   - Circuit breakers
   - Fallback strategies

5. ERROR INFORMATION
   - Development vs production error details
   - Stack trace exposure
   - Error logging completeness
   - User-friendly error messages

Identify error handling gaps and provide improved implementation.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
