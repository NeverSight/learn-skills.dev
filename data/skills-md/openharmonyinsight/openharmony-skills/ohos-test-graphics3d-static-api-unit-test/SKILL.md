---
name: ohos-test-graphics3d-static-api-unit-test
display_name: Graphics 3D API Unit Test Generator
scope: domain
stage: testing
domain: graphics3d
capability: static-api-unit-test
version: 0.1.0
status: trial
description: Use when generating unit tests for ETS/ArkTS static API classes in OpenHarmony graphic_3d module, when adding new test cases for MaterialETS, CameraETS, SceneETS or similar wrapper classes, or when setting up test environment for GTest-based ETS unit tests
---

# Graphics 3D API Unit Test Generator

## Overview

Guide for generating ETS/ArkTS static API unit tests based on OpenHarmony GTest framework. Provides test generation workflow, naming conventions, and core patterns.

## When to Use

- Adding unit tests for new ETS wrapper classes (e.g., `CameraETS`, `MaterialETS`)
- Extending existing test cases with new test scenarios
- Setting up new test modules or test environment

**Do NOT use when:**
- Testing Lume engine core layer (use other test frameworks)
- Writing integration tests or performance tests (require different fixtures)

## Quick Reference

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Test class name | `<Module>ETSUnitTest` | `MaterialETSUnitTest` |
| Test case name | `<Class>_<Method>_<Number>` | `MaterialETS_Create_001` |
| Test file name | `<module>_ets_unit_test.cpp` | `material_ets_unit_test.cpp` |

### Test Macros

| Macro | Purpose |
|-------|---------|
| `HWTEST_F` | Fixed test fixture (required for all ETS unit tests) |

**Test Levels**: Use appropriate `TestSize.Level0-Level4` based on test complexity.

### Selection Rule

- **Default**: `TestSize.Level1` for most API method tests
- **Adjust**: Use higher levels for complex scenarios (error handling, performance)

See UNITTEST_GUIDE.md "Test Case Macros" section for complete Level0-Level4 definitions.

### Required Comment Template

```cpp
/**
 * @tc.name: <TestCaseName>
 * @tc.desc: <Description>
 * @tc.type: FUNC / PERF
 */
```

## Core Pattern: AAA Testing

Use Arrange-Act-Assert pattern:

```cpp
/**
 * @tc.name: MaterialETS_Create_001
 * @tc.desc: Test MaterialETS creation and initialization
 * @tc.type: FUNC
 */
HWTEST_F(MaterialETSUnitTest, MaterialETS_Create_001, TestSize.Level1)
{
    auto material = std::make_shared<MaterialETS>();
    EXPECT_TRUE(material->IsValid());  // EtsTest provides engine context automatically
}
```

## Implementation Workflow

1. **Create test file**: `api_unit_test/<module>_ets_unit_test.cpp`
2. **Write test cases**: Use AAA pattern with required annotations
3. **Update BUILD.gn**: Add file to `sources` list

**Complete implementation details**: UNITTEST_GUIDE.md provides:
- EtsTest fixture class implementation
- Complete BUILD.gn template
- Environment setup and build commands
- Error handling examples

For loading guidance, see "When to Load References" section below.

## When to Load References

### ✅ Load UNITTEST_GUIDE.md when:

- Setting up **new test module** (first-time setup)
- Writing **first test** for a class (need complete workflow)
- Need **complete BUILD.gn template** (copy-paste ready)
- Troubleshooting **build/run errors** (detailed solutions)
- Need **EtsTest fixture details** (engine lifecycle understanding)

### ❌ Do NOT Load when:

- **Quick test generation** (SKILL.md Quick Reference sufficient)
- **Simple naming queries** (conventions in SKILL.md)
- **Familiar scenarios** (standard patterns known)
- Only need **Quick Reference tables** (no deep dive required)

**Rule**: Start with SKILL.md. Load UNITTEST_GUIDE.md only when blocked or setting up new environment.

**Link**: [UNITTEST_GUIDE.md](references/UNITTEST_GUIDE.md) (load only when above conditions apply)

## Common Mistakes

| Issue | Solution |
|-------|----------|
| Header not found | Check BUILD.gn `include_dirs` |
| Library not found | Ensure `libAGPDLL.z.so` deployed |
| Tests interfere | Use SetUp/TearDown for isolation |

## NEVER Do This

| ❌ Wrong | ✅ Right | Reason |
|----------|----------|--------|
| `MaterialETS_Test` | `MaterialETSUnitTest` | OpenHarmony requires `UnitTest` suffix |
| `MaterialETS_Create` | `MaterialETS_Create_001` | Test naming MUST include `_Number` suffix |
| Skip `@tc.name` | Always add annotation | Required for test report generation |
| Use GTest macro directly | Use `HWTEST_F` macro | OpenHarmony test framework requires it |
| Write test without annotations | Include complete annotation block | Missing annotations break test discovery |

## Real-World Impact

Tests generated following this skill:
- Comply with OpenHarmony testing standards
- Automated engine lifecycle management
- Complete resource cleanup mechanism

## References

| Document | Description |
|----------|-------------|
| [UNITTEST_GUIDE.md](references/UNITTEST_GUIDE.md) | Complete BUILD.gn template, EtsTest base class, environment setup |