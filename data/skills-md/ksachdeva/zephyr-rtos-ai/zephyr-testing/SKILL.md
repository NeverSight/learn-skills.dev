---
name: zephyr-testing
description: "Comprehensive guidance for unit testing and integration testing Zephyr RTOS applications. Use this skill when you need to: (1) Create test suites using the Ztest framework, (2) Write test cases with fixtures, assertions, and expectations, (3) Configure testcase.yaml for Twister test runner, (4) Mock functions using FFF (Fake Function Framework), (5) Run tests with Twister on emulators or hardware, (6) Debug failing tests or configure test infrastructure, (7) Implement pytest-based integration tests."
---

# Zephyr Testing Skill

Expert guidance for testing Zephyr RTOS applications using Ztest framework, Twister test runner, and FFF mocking.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Test Project Structure](#test-project-structure)
3. [Ztest Framework Basics](#ztest-framework-basics)
4. [Running Tests with Twister](#running-tests-with-twister)
5. [Advanced Topics](#advanced-topics)
6. [References](#references)

---

## Quick Start

### Minimal Integration Test

```
tests/foo/bar/
├── CMakeLists.txt
├── prj.conf
├── testcase.yaml
└── src/
    └── main.c
```

**CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(my_test)
target_sources(app PRIVATE src/main.c)
```

**prj.conf:**
```
CONFIG_ZTEST=y
```

**testcase.yaml:**
```yaml
tests:
  mysubsystem.feature.basic:
    tags: feature
    platform_allow:
      - native_sim
    integration_platforms:
      - native_sim
```

**src/main.c:**
```c
#include <zephyr/ztest.h>

ZTEST_SUITE(my_suite, NULL, NULL, NULL, NULL, NULL);

ZTEST(my_suite, test_example)
{
    zassert_true(1, "1 was false");
    zassert_equal(2 + 2, 4, "math is broken");
}
```

**Run:**
```bash
./scripts/twister -T tests/foo/bar/ -p native_sim
```

### Minimal Unit Test

Unit tests compile only the module under test (no full Zephyr OS).

**CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.20.0)
project(app)
find_package(Zephyr COMPONENTS unittest REQUIRED HINTS $ENV{ZEPHYR_BASE})
target_sources(testbinary PRIVATE main.c)
```

**testcase.yaml:**
```yaml
tests:
  mymodule.unit:
    tags: unit
    type: unit
```

**Run:**
```bash
./scripts/twister -T tests/unit/mymodule/
```

---

## Test Project Structure

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Test scenario ID | `subsystem.component[.variant]` | `kernel.semaphore.stress` |
| Ztest suite name | snake_case, descriptive | `semaphore_tests` |
| Test function | `test_<what_is_tested>` | `test_sem_give_take` |

### testcase.yaml Key Options

| Key | Purpose | Example |
|-----|---------|---------|
| `tags` | Categorize tests | `tags: kernel thread` |
| `platform_allow` | Only run on these | `platform_allow: [native_sim]` |
| `platform_exclude` | Never run on these | `platform_exclude: [qemu_x86]` |
| `depends_on` | Require board features | `depends_on: gpio i2c` |
| `build_only` | Compile but don't run | `build_only: true` |
| `timeout` | Seconds before kill | `timeout: 120` |
| `extra_configs` | Merge Kconfig options | `extra_configs: [CONFIG_LOG=y]` |
| `harness` | Test harness type | `harness: ztest` |
| `type` | Test type | `type: unit` |
| `filter` | Expression-based filter | `filter: CONFIG_BT` |

---

## Ztest Framework Basics

### Suite Definition

```c
ZTEST_SUITE(suite_name, predicate, setup, before, after, teardown);
```

| Parameter | Type | Purpose |
|-----------|------|---------|
| `suite_name` | identifier | Unique suite name |
| `predicate` | `bool (*)(const void *)` | Optional: decides if suite runs |
| `setup` | `void *(*)(void)` | Optional: runs once, returns fixture |
| `before` | `void (*)(void *)` | Optional: runs before each test |
| `after` | `void (*)(void *)` | Optional: runs after each test |
| `teardown` | `void (*)(void *)` | Optional: runs once at end |

### Test Macros

| Macro | When to Use |
|-------|-------------|
| `ZTEST(suite, test)` | Standard test |
| `ZTEST_F(suite, test)` | Test with fixture access |
| `ZTEST_USER(suite, test)` | Runs in userspace thread |
| `ZTEST_USER_F(suite, test)` | Userspace + fixture |
| `ZTEST_P(suite, test)` | Parameterized test |

### Assertions (Fail Immediately)

| Assertion | Checks |
|-----------|--------|
| `zassert_true(cond, msg)` | cond is true |
| `zassert_false(cond, msg)` | cond is false |
| `zassert_equal(a, b, msg)` | a == b |
| `zassert_not_equal(a, b, msg)` | a != b |
| `zassert_is_null(ptr, msg)` | ptr is NULL |
| `zassert_not_null(ptr, msg)` | ptr is not NULL |
| `zassert_mem_equal(a, b, sz, msg)` | memory equal |
| `zassert_str_equal(a, b, msg)` | strings equal |
| `zassert_within(a, b, delta, msg)` | \|a - b\| <= delta |
| `zassert_ok(ret, msg)` | ret == 0 |

### Expectations (Continue, Fail at End)

Replace `zassert_` with `zexpect_` for non-fatal assertions that continue execution.

### Assumptions (Skip on Failure)

Replace `zassert_` with `zassume_` to skip the test if condition fails.

### Skipping Tests

```c
ZTEST(common, test_feature)
{
    Z_TEST_SKIP_IFDEF(CONFIG_FEATURE_DISABLED);
    // or
    ztest_test_skip();
}
```

### Expected Failures

```c
ZTEST_EXPECT_FAIL(suite, test_known_broken);
ZTEST(suite, test_known_broken)
{
    zassert_true(false, NULL);  // Marked as PASS because failure expected
}
```

---

## Running Tests with Twister

### Common Commands

```bash
# Run all tests in a directory
./scripts/twister -T tests/kernel/

# Run on specific platform
./scripts/twister -p native_sim -T tests/kernel/threads/

# Run specific test scenario
./scripts/twister --scenario tests/kernel/semaphore/kernel.semaphore

# List available tests
./scripts/twister --list-tests -T tests/kernel/

# Build only (no execution)
./scripts/twister --build-only -T tests/subsys/

# Run on hardware
./scripts/twister --device-testing --device-serial /dev/ttyACM0 -p nrf52840dk/nrf52840 -T tests/
```

### Test on Hardware

**Single device:**
```bash
./scripts/twister --device-testing --device-serial /dev/ttyACM0 -p frdm_k64f -T tests/kernel
```

**Multiple devices (hardware map):**
```bash
# Generate hardware map
./scripts/twister --generate-hardware-map map.yml

# Edit map.yml to set correct platform names, then:
./scripts/twister --device-testing --hardware-map map.yml -T tests/
```

### Twister Output Files

| File | Content |
|------|---------|
| `twister.json` | Full results in JSON |
| `twister.log` | Build/run logs |
| `twister_discard.csv` | Skipped tests with reasons |

---

## Advanced Topics

### Test Fixtures

```c
struct my_fixture {
    int value;
    uint8_t buffer[256];
};

static void *my_suite_setup(void)
{
    struct my_fixture *f = malloc(sizeof(*f));
    f->value = 42;
    return f;
}

static void my_suite_before(void *f)
{
    struct my_fixture *fixture = f;
    memset(fixture->buffer, 0, sizeof(fixture->buffer));
}

static void my_suite_teardown(void *f)
{
    free(f);
}

ZTEST_SUITE(my_suite, NULL, my_suite_setup, my_suite_before, NULL, my_suite_teardown);

ZTEST_F(my_suite, test_with_fixture)
{
    zassert_equal(fixture->value, 42, "fixture not initialized");
}
```

### Test Rules (Global Hooks)

Apply logic to every test across all suites:

```c
#include <zephyr/fff.h>
#include <zephyr/ztest.h>

DEFINE_FFF_GLOBALS;

static void reset_mocks_before(const struct ztest_unit_test *test, void *fixture)
{
    ARG_UNUSED(test);
    ARG_UNUSED(fixture);
    // Reset all fakes here
}

ZTEST_RULE(mock_reset_rule, reset_mocks_before, NULL);
```

### Mocking with FFF

- **FFF mocking patterns**: See [references/mocking.md](references/mocking.md)

### Pytest Integration

For complex integration tests requiring host-side logic:

- **Pytest harness usage**: See [references/twister.md](references/twister.md#pytest-integration)

### Stress Testing (Ztress)

Test code resilience to preemptions:

```c
#include <zephyr/ztest.h>

ztress_set_timeout(K_MSEC(10000));
ZTRESS_EXECUTE(
    ZTRESS_TIMER(timer_handler, NULL, 10000, Z_TIMEOUT_TICKS(20)),
    ZTRESS_THREAD(thread_handler, NULL, 10000, 0, Z_TIMEOUT_TICKS(20))
);
```

---

## References

- [references/ztest.md](references/ztest.md) - Complete Ztest API, macros, and patterns
- [references/twister.md](references/twister.md) - Twister configuration, harnesses, hardware testing
- [references/mocking.md](references/mocking.md) - FFF fake function framework patterns
- [references/examples.md](references/examples.md) - Complete working test examples
