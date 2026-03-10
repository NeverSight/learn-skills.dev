---
name: chrysopoeia
description: >
  Extract maximum value from existing code — performance optimization, API
  surface refinement, and dead weight elimination. The art of turning base code
  into gold through systematic identification and amplification of value-bearing
  patterns. Use when optimizing a working but sluggish codebase, refining an
  API surface that has accumulated cruft, reducing bundle size or memory
  footprint, or preparing code for open-source release — when code works
  correctly but doesn't shine and needs polish rather than a full rewrite.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: alchemy
  complexity: intermediate
  language: multi
  tags: alchemy, optimization, value-extraction, performance, refinement, gold
---

# Chrysopoeia

Systematically extract maximum value from existing code — identify what's golden (high-value, well-designed), what's lead (resource-heavy, poorly optimized), and what's dross (dead weight). Then amplify the gold, transmute the lead, and remove the dross.

## When to Use

- Optimizing a working but sluggish codebase for performance
- Refining an API surface that has accumulated cruft over iterations
- Reducing bundle size, memory footprint, or startup time
- Preparing code for open-source release (extracting the valuable core)
- When code works correctly but doesn't shine — it needs polish, not rewrite

## Inputs

- **Required**: Codebase or module to optimize (file paths)
- **Required**: Value metric (performance, API clarity, bundle size, readability)
- **Optional**: Profiling data or benchmarks showing current performance
- **Optional**: Budget or target (e.g., "reduce bundle by 40%", "sub-100ms response")
- **Optional**: Constraints (can't change public API, must maintain backward compat)

## Procedure

### Step 1: Assay — Classify the Material

Systematically classify every element by its value contribution.

1. Define the value metric from Inputs (performance, clarity, size, etc.)
2. Inventory the codebase elements (functions, modules, exports, dependencies)
3. Classify each element:

```
Value Classification:
+--------+---------------------------------------------------------+
| Gold   | High value, well-designed. Amplify and protect.         |
| Silver | Good value, minor imperfections. Polish.                |
| Lead   | Functional but heavy — poor performance, complex API.   |
|        | Transmute into something lighter.                       |
| Dross  | Dead code, unused exports, vestigial features.          |
|        | Remove entirely.                                        |
+--------+---------------------------------------------------------+
```

4. For performance optimization, profile first:
   - Identify hot paths (where time is spent)
   - Identify cold paths (rarely executed code that may be dross)
   - Measure memory allocation patterns
5. Produce the **Assay Report**: element-by-element classification with evidence

**Expected:** Every significant element classified with evidence. Gold elements are identified for protection during optimization. Lead elements are prioritized by impact.

**On failure:** If profiling tools aren't available, use static analysis: function complexity (cyclomatic), dependency count, and code size as proxies. If the codebase is too large, focus on the critical path first.

### Step 2: Refine — Amplify the Gold

Protect and enhance the highest-value elements.

1. For each Gold element:
   - Ensure it has comprehensive tests (these are your most valuable assets)
   - Document its interface clearly if not already done
   - Consider whether it could be extracted as a reusable module
2. For each Silver element:
   - Apply targeted improvements (better naming, clearer types, minor optimizations)
   - Bring test coverage to Gold-level
   - Resolve minor code smells without restructuring
3. Do not modify Gold/Silver behavior — only improve their polish and protection

**Expected:** Gold and Silver elements are better tested, documented, and protected. No behavioral changes, only quality improvements.

**On failure:** If a "Gold" element reveals hidden problems during closer inspection, reclassify it. Better to be honest about value than to protect flawed code.

### Step 3: Transmute — Convert Lead to Gold

Transform heavy, inefficient elements into optimized equivalents.

1. Prioritize Lead elements by impact (highest resource consumption first)
2. For each Lead element, choose a transmutation strategy:
   - **Algorithm optimization**: Replace O(n^2) with O(n log n), eliminate redundant computation
   - **Caching/memoization**: Store expensive results that are requested repeatedly
   - **Lazy evaluation**: Defer computation until results are actually needed
   - **Batch processing**: Combine many small operations into fewer large ones
   - **Structural simplification**: Reduce cyclomatic complexity, flatten deep nesting
3. Apply the strategy and measure the improvement:
   - Before/after benchmarks for performance changes
   - Before/after line counts for complexity changes
   - Before/after dependency counts for coupling changes
4. Verify behavioral equivalence after each transmutation

**Expected:** Measurable improvement on the target value metric. Each transmuted element performs better than its Lead predecessor while maintaining identical behavior.

**On failure:** If a Lead element resists optimization within its current interface, consider whether the interface itself is the problem. Sometimes the transmutation requires changing how the element is called, not just how it's implemented.

### Step 4: Purge — Remove the Dross

Eliminate dead weight systematically.

1. For each Dross element, verify it's truly unused:
   - Search for all references (grep, IDE find-usages)
   - Check for dynamic references (string-based dispatch, reflection)
   - Check for external consumers (if the code is a library)
2. Remove confirmed dross:
   - Delete dead code, unused exports, vestigial features
   - Remove unused dependencies from package manifests
   - Clean up configuration for removed features
3. Verify nothing breaks after each removal (run tests)
4. Document what was removed and why (in commit messages, not in code)

**Expected:** The codebase is lighter. Bundle size, dependency count, or code volume measurably reduced. All tests still pass.

**On failure:** If removing an element breaks something, it wasn't dross — reclassify it. If dynamic references make it hard to verify usage, add temporary logging before deletion to confirm no runtime access.

### Step 5: Verify — Weigh the Gold

Measure the overall improvement.

1. Run the same benchmarks/metrics used in Step 1
2. Compare before/after on the target value metric
3. Document the chrysopoeia results:
   - Elements refined (Gold/Silver improvements)
   - Elements transmuted (Lead → Gold conversions with measurements)
   - Elements purged (Dross removed with size/count impact)
   - Overall metric improvement (e.g., "47% faster", "32% smaller bundle")

**Expected:** Measurable, documented improvement on the target value metric. The codebase is demonstrably more valuable than before.

**On failure:** If overall improvement is marginal, the original code may have been better than assumed. Document what was learned — knowing that code is already near-optimal is itself valuable.

## Validation Checklist

- [ ] Assay report classifies all significant elements with evidence
- [ ] Gold elements have comprehensive tests and documentation
- [ ] Lead transmutations show measurable before/after improvement
- [ ] Dross removal verified with reference checks before deletion
- [ ] All tests pass after each stage
- [ ] Overall improvement measured and documented
- [ ] No behavioral regressions introduced
- [ ] Constraints from Inputs are satisfied

## Common Pitfalls

- **Premature optimization**: Optimizing without profiling. Always measure first, optimize the hot paths
- **Polishing dross**: Spending effort improving code that should be deleted. Classify before refining
- **Breaking Gold**: Optimization that degrades the best code. Gold elements should only get better, never worse
- **Unmeasured claims**: "It feels faster" is not chrysopoeia. Every improvement must be quantified
- **Optimizing cold paths**: Spending effort on code that runs once at startup when the bottleneck is the request loop

## Related Skills

- `athanor` — Full four-stage transformation when chrysopoeia reveals the code needs restructuring, not just optimization
- `transmute` — Targeted conversion when a Lead element needs a paradigm shift
- `review-software-architecture` — Architecture-level evaluation that complements code-level chrysopoeia
- `review-data-analysis` — Data pipeline optimization parallels code optimization
