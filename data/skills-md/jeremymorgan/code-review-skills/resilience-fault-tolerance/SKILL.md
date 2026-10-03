---
name: resilience-fault-tolerance
description: Evaluates resilience and fault tolerance, including failure modes, retries, timeouts, and graceful degradation. Use when reviewing reliability under failure conditions.
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

Evaluate system resilience:

Check for:

1. TIMEOUT HANDLING
   - HTTP request timeouts
   - Database query timeouts
   - Long-running operation limits

2. RETRY LOGIC
   - Exponential backoff
   - Maximum retry limits
   - Idempotency considerations

3. CIRCUIT BREAKER PATTERN
   - Service failure detection
   - Fallback mechanisms
   - Recovery testing

4. BULKHEAD PATTERN
   - Resource isolation
   - Thread pool separation
   - Connection pool limits

5. GRACEFUL DEGRADATION
   - Feature flags
   - Fallback data sources
   - Cached responses
   - Default values

Rate resilience (1-10) with improvement recommendations.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
