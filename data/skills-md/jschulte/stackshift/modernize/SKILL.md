---
name: modernize
description: Brownfield Upgrade - Upgrade all dependencies and modernize the application while maintaining spec-driven control. Runs after Gear 6 for brownfield projects with modernize flag enabled. Updates deps, fixes breaking changes, improves test coverage, updates specs to match changes.
---

# Modernize (Brownfield Upgrade)

**Optional Step** after Gear 6 for Brownfield projects with `modernize: true` flag.

**Estimated Time:** 2-6 hours (depends on dependency age and breaking changes)
**Prerequisites:** Gears 1-6 completed, 100% spec coverage established
**Output:** Modern dependency versions, updated tests, synchronized specs

---

## When to Use This Skill

Use this skill when:
- Brownfield path with `modernize: true` flag set
- Gears 1-6 are complete (specs established, gaps implemented)
- Ready to upgrade all dependencies to latest versions
- Want to modernize while maintaining spec-driven control

**Trigger Conditions:**
- State file has `path: "brownfield"` AND `modernize: true`
- Gear 6 (implement) is complete
- User requested "Brownfield Upgrade" during Gear 1

---

## What This Skill Does

Systematically upgrades the entire application to modern dependency versions:

1. **Detect Package Manager** - npm, yarn, pnpm, pip, go mod, cargo, etc.
2. **Audit Current Versions** - Document what's installed before upgrade
3. **Upgrade Dependencies** - Use appropriate upgrade command for tech stack
4. **Run Tests** - Identify breaking changes
5. **Fix Breaking Changes** - Iteratively fix with spec guidance
6. **Update Specs** - Synchronize specs with API/behavior changes
7. **Validate Coverage** - Ensure tests meet 85%+ threshold
8. **Verify Specs Match** - Run /speckit.analyze to confirm alignment

---

## Process Overview

### Phase 1: Pre-Upgrade Audit

**Document current state**:
```bash
# Create upgrade baseline
cat package.json > .modernize/baseline-package.json

# Run tests to establish baseline
npm test > .modernize/baseline-test-results.txt

# Document current coverage
npm run test:coverage > .modernize/baseline-coverage.txt
```

**Analyze upgrade scope**:
```bash
# Check for available updates
npm outdated > .modernize/upgrade-plan.txt

# Identify major version bumps (potential breaking changes)
# Highlight security vulnerabilities
# Note deprecated packages
```

---

### Phase 2: Dependency Upgrade

**Tech stack detection** (from analysis-report.md):

**For Node.js/TypeScript**:
```bash
# Update all dependencies
npm update

# Or for major versions:
npx npm-check-updates -u
npm install

# Check for security issues
npm audit fix
```

**For Python**:
```bash
# Update all dependencies
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Or use pip-upgrader
pip-upgrade requirements.txt
```

**For Go**:
```bash
# Update all dependencies
go get -u ./...
go mod tidy
```

**For Rust**:
```bash
# Update dependencies
cargo update

# Check for outdated packages
cargo outdated
```

---

### Phase 3: Breaking Change Detection

**Run tests after upgrade**:
```bash
# Run full test suite
npm test

# Capture failures
npm test 2>&1 | tee .modernize/post-upgrade-test-results.txt

# Compare to baseline
diff .modernize/baseline-test-results.txt .modernize/post-upgrade-test-results.txt
```

**Identify breaking changes**:
- TypeScript compilation errors
- Test failures
- Runtime errors
- API signature changes
- Deprecated method usage

---

### Phase 4: Fix Breaking Changes (Spec-Guided)

**For each breaking change**:

1. **Identify affected feature**:
   - Match failing test to feature spec
   - Determine which spec the code implements

2. **Review spec requirements**:
   - What behavior SHOULD exist (from spec)
   - What changed in the upgrade
   - How to preserve spec compliance

3. **Fix with spec guidance**:
   - Update code to work with new dependency
   - Ensure behavior still matches spec
   - Refactor if needed to maintain spec alignment

4. **Update tests**:
   - Fix broken tests
   - Add tests for new edge cases from upgrade
   - Maintain 85%+ coverage threshold

5. **Verify spec alignment**:
   - Behavior unchanged from user perspective
   - Implementation may change but spec compliance maintained

---

### Phase 5: Spec Synchronization

**Check if upgrades changed behavior**:

Some dependency upgrades change API behavior:
- Date formatting libraries (moment → date-fns)
- Validation libraries (joi → zod)
- HTTP clients (axios → fetch)
- ORM updates (Prisma major versions)

**If behavior changed**:
1. Update relevant feature spec to document new behavior
2. Update acceptance criteria if needed
3. Update technical requirements with new dependencies
4. Run /speckit.analyze to validate changes

**If only implementation changed**:
- No spec updates needed
- Just update technical details (versions, file paths)

---

### Phase 6: Test Coverage Improvement

**Goal: Achieve 85%+ coverage on all modules**

1. **Run coverage report**:
   ```bash
   npm run test:coverage
   ```

2. **Identify gaps**:
   - Modules below 85%
   - Missing edge case tests
   - Integration test gaps

3. **Add tests with spec guidance**:
   - Each spec has acceptance criteria
   - Write tests to cover all criteria
   - Use spec success criteria as test cases

4. **Validate**:
   ```bash
   npm run test:coverage
   # All modules should be 85%+
   ```

---

### Phase 7: Final Validation

**Run complete validation suite**:

1. **Build succeeds**:
   ```bash
   npm run build
   # No errors
   ```

2. **All tests pass**:
   ```bash
   npm test
   # 0 failures
   ```

3. **Coverage meets threshold**:
   ```bash
   npm run test:coverage
   # 85%+ on all modules
   ```

4. **Specs validated**:
   ```bash
   /speckit.analyze
   # No drift, all specs match implementation
   ```

5. **Dependencies secure**:
   ```bash
   npm audit
   # No high/critical vulnerabilities
   ```

---

## Output

**Upgrade Report** (`.modernize/UPGRADE_REPORT.md`):
```markdown
# Dependency Modernization Report

**Date**: {date}
**Project**: {name}

## Summary

- **Dependencies upgraded**: {X} packages
- **Major version bumps**: {X} packages
- **Breaking changes**: {X} fixed
- **Tests fixed**: {X} tests
- **New tests added**: {X} tests
- **Coverage improvement**: {before}% → {after}%
- **Specs updated**: {X} specs

## Upgraded Dependencies

| Package | Old Version | New Version | Breaking? |
|---------|-------------|-------------|-----------|
| react | 17.0.2 | 18.3.1 | Yes |
| next | 13.5.0 | 14.2.0 | Yes |
| ... | ... | ... | ... |

## Breaking Changes Fixed

1. **React 18 Automatic Batching**
   - Affected: User state management
   - Fix: Updated useEffect dependencies
   - Spec: No behavior change
   - Tests: Added async state tests

2. **Next.js 14 App Router**
   - Affected: Routing architecture
   - Fix: Migrated pages/ to app/
   - Spec: Updated file paths
   - Tests: Updated route tests

## Spec Updates

- Updated technical requirements with new versions
- Updated file paths for App Router migration
- No functional spec changes (behavior preserved)

## Test Coverage

- Before: 78%
- After: 87%
- New tests: 45 tests added
- All modules: ✅ 85%+

## Validation

- ✅ All tests passing
- ✅ Build successful
- ✅ /speckit.analyze: No drift
- ✅ npm audit: 0 high/critical
- ✅ Coverage: 87% (target: 85%+)

## Next Steps

Application is now:
- ✅ Fully modernized (latest dependencies)
- ✅ 100% spec coverage maintained
- ✅ Tests passing with high coverage
- ✅ Specs synchronized with implementation
- ✅ Ready for ongoing spec-driven development
```

---

## Configuration in State File

The modernize flag is set during Gear 1:

```json
{
  "path": "brownfield",
  "modernize": true,
  "metadata": {
    "modernizeRequested": "2024-11-17T12:00:00Z",
    "upgradeScope": "all-dependencies",
    "targetCoverage": 85
  }
}
```

---

## When Modernize Runs

**In Cruise Control**:
- Automatically runs after Gear 6 if `modernize: true`

**In Manual Mode**:
- Skill becomes available after Gear 6 completes
- User explicitly invokes: `/stackshift.modernize` or skill auto-activates

---

## Success Criteria

Modernization complete when:
- ✅ All dependencies updated to latest stable versions
- ✅ All tests passing
- ✅ Test coverage ≥ 85% on all modules
- ✅ Build successful (no compilation errors)
- ✅ /speckit.analyze shows no drift
- ✅ No high/critical security vulnerabilities
- ✅ Specs updated where behavior changed
- ✅ Upgrade report generated

---

## Benefits of Brownfield Upgrade

### vs. Standard Brownfield:
- ✅ **Modern dependencies** (not stuck on old versions)
- ✅ **Security updates** (latest patches)
- ✅ **Performance improvements** (newer libraries often faster)
- ✅ **New features** (latest library capabilities)
- ✅ **Reduced technical debt** (no old dependencies)

### vs. Greenfield:
- ✅ **Faster** (upgrade vs. rebuild)
- ✅ **Lower risk** (incremental changes vs. rewrite)
- ✅ **Spec-guided** (specs help fix breaking changes)
- ✅ **Keeps working code** (only changes dependencies)

### Use Case:
Perfect for teams that want to modernize without full rewrites. Get the benefits of modern tooling while maintaining existing features.

---

## Technical Approach

### Spec-Driven Upgrade Strategy

1. **Specs as Safety Net**:
   - Every feature has acceptance criteria
   - Run tests against specs after each upgrade
   - If tests fail, specs guide the fix

2. **Incremental Upgrades**:
   - Upgrade in phases (minor first, then majors)
   - Run tests after each phase
   - Rollback if too many failures

3. **Coverage as Quality Gate**:
   - Must maintain 85%+ throughout upgrade
   - Add tests for new library behaviors
   - Ensure edge cases covered

4. **Spec Synchronization**:
   - If library changes behavior, update spec
   - If implementation changes, update spec
   - /speckit.analyze validates alignment

---

**Result**: A fully modernized application under complete spec-driven control!
