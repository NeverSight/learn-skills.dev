---
name: swe-test-unit-test-writer
description: >
  Guides AI agents to write high-quality TypeScript unit tests using Jest or
  Vitest. Covers Arrange-Act-Assert pattern, FIRST principles, scenario design
  (happy/negative/error/boundary), mocking strategies, naming conventions, and
  anti-patterns. Use when the user asks to "write unit tests", "เขียน test",
  "เพิ่ม test", "สร้าง test file", or when an agent needs to produce .test.ts
  or .spec.ts files. Focused on unit tests only — for integration tests, use a
  dedicated integration test skill.
license: Apache-2.0
allowed-tools: ReadFile, ListDirectory, RunCommand, WriteFile
metadata:
  author: choonewza
  version: "0.1"
---

## Overview

You are a unit test writer for **TypeScript** projects using **Jest** or **Vitest**.

> **Testing in Practice Mindset:**
> การเขียน Test ที่ดีไม่ได้เริ่มจาก API ของ Testing Framework แต่เริ่มจากการ **เข้าใจ Behavior และ Contract ที่ระบบต้องรับประกัน**
> เป้าหมายคือ:
>
> 1. รู้ว่า **"ควร Test อะไร"** (Test Contract & Behavior, ไม่ใช่ Implementation Detail)
> 2. รู้ว่า **"ควรจัดโครงสร้าง Test อย่างไร"** (Arrange-Act-Assert, One Behavior Per Test)
> 3. รู้ว่า **"จัด Test Files อย่างไรเมื่อ Project ใหญ่ขึ้น"** (Co-location, Domain-based splitting)

Your job is to produce `.test.ts` / `.spec.ts` files that are:

- **Readable** — anyone can understand the business rule from the test name alone
- **Reliable** — follows FIRST principles (Fast, Independent, Repeatable, Self-Validating, Timely)
- **Comprehensive** — covers happy path, negative path, error cases, and boundary cases
- **Maintainable** — uses Arrange–Act–Assert, proper mocking, and avoids anti-patterns

> Unit Test ตรวจพฤติกรรมของ function, module หรือ class ขนาดเล็ก ในสถานการณ์ที่ควบคุมได้
> เป้าหมายคือ **confidence** ไม่ใช่จำนวน test case เยอะที่สุด

**Scope:** Unit tests only. This skill does NOT cover integration tests, E2E tests,
or API tests.

> 💡 **การกำหนดค่าที่จะใช้ในการเขียน Test:**
> สำหรับการวิเคราะห์ ออกแบบ และกำหนดค่าข้อมูลทดสอบ (Test Data Design เช่น การหาค่า Boundary ด้วย BVA หรือแบ่งกลุ่มด้วย EP) **ให้ไปอ่านและอ้างอิงจากสกิล [`swe-test-engineer`](../swe-test-engineer/SKILL.md)** แล้วนำค่าเหล่านั้นมาเขียนลงในโค้ด Test ของสกิลนี้
> สำหรับการจัดลำดับความสำคัญของ Test ให้ใช้ `swe-test-planner`

For detailed references, see:

- [references/aaa-pattern.md](references/aaa-pattern.md) — Arrange–Act–Assert structure
- [references/first-principles.md](references/first-principles.md) — quality checklist
- [references/scenario-design.md](references/scenario-design.md) — how to think about scenarios & contracts
- [references/case-types.md](references/case-types.md) — positive / negative / error / boundary (representative values)
- [references/mocking-guide.md](references/mocking-guide.md) — dependency isolation (jest.mock, vi.mock)
- [references/naming-conventions.md](references/naming-conventions.md) — test naming patterns & CI diagnostics
- [references/anti-patterns.md](references/anti-patterns.md) — common mistakes to avoid (refactor litmus test)
- [references/project-file-structure.md](references/project-file-structure.md) — test file organization as projects grow
- [references/examples.md](references/examples.md) — complete worked examples

---

## When to Activate

Activate when the user:

- Asks to write unit tests for a function, module, or class
- Says "เขียน test", "เพิ่ม test", "สร้าง test file", "write unit tests"
- Has a `.ts` file and wants test coverage
- Asks to improve existing test quality or refactor tests
- Mentions Jest, Vitest, or test-related TypeScript work

Do NOT activate when:

- The user wants integration tests or E2E tests → separate skill
- The user wants test case _design_ (BVA/EP tables) → use `swe-test-engineer`
- The user wants test _prioritization_ → use `swe-test-planner`
- The code is not TypeScript (Python, Go, etc.) → this skill is TS-specific

---

## Anti-Patterns

Before writing any test, internalize these rules. See [references/anti-patterns.md](references/anti-patterns.md) for details.

- ❌ **Do not test implementation details** — test behavior and contracts, not internal methods or intermediate variables.
  _Litmus Test:_ ถ้า refactor โค้ดภายในแล้ว behavior เหมือนเดิม Test ต้องยังผ่านเสมอ (ถ้า fail แปลว่า test implementation detail)
- ❌ **Do not bundle multiple behaviors in one test** — follow One Behavior Per Test. Avoid the "And Smell" in test names (e.g., `formats price and handles errors and logs result` ❌)
- ❌ **Do not mock everything** — over-mocking means you're testing the mocks, not the code
- ❌ **Do not omit `await` before async assertions** — `expect(fn()).rejects` without `await` causes floating promises and silent false positives
- ❌ **Do not use weak assertions or brittle whole-object matches** — avoid `.toBeTruthy()` on objects, use `.toMatchObject()` or `expect.objectContaining()` instead of fragile `.toEqual()` on dynamic fields
- ❌ **Do not assert exact error message strings** — test Custom Error classes or error codes, not brittle wording
- ❌ **Do not leak global state or `process.env`** — always restore in `afterEach`
- ❌ **Do not use generic or implementation-focused test names** — "test case 1", "works correctly", "calls Intl" are forbidden
- ❌ **Do not copy-paste tests that differ only by data** — use `it.each` / `test.each` with representative boundary values
- ❌ **Do not write tests that depend on execution order** — each test must be independent
- ❌ **Do not assert on snapshot without reviewing it** — snapshots must be intentional
- ❌ **Do not skip error and edge cases** — these have the highest production value

---

## Instructions

### Step 1: Detect Test Framework

Check the project to determine Jest or Vitest:

| Signal                                                   | Framework |
| -------------------------------------------------------- | --------- |
| `jest.config.ts` / `jest.config.js`                      | Jest      |
| `vitest.config.ts` / `vite.config.ts` with `test:` block | Vitest    |
| `package.json` → `devDependencies` contains `jest`       | Jest      |
| `package.json` → `devDependencies` contains `vitest`     | Vitest    |
| Import from `vitest` in existing test files              | Vitest    |

**Key differences to remember:**

| Feature       | Jest                             | Vitest                                           |
| ------------- | -------------------------------- | ------------------------------------------------ |
| Mock module   | `jest.mock('./module')`          | `vi.mock('./module')`                            |
| Mock function | `jest.fn()`                      | `vi.fn()`                                        |
| Spy           | `jest.spyOn(obj, 'method')`      | `vi.spyOn(obj, 'method')`                        |
| Timer mock    | `jest.useFakeTimers()`           | `vi.useFakeTimers()`                             |
| Reset         | `jest.clearAllMocks()`           | `vi.clearAllMocks()`                             |
| Globals       | `describe/it/expect` auto-global | Must set `globals: true` or import from `vitest` |

If both are present, prefer Vitest (it's the newer standard).
If neither is found, ask the user via the tool which framework to use.

---

### Step 2: Analyze the Source Code & Function Contract

Before writing any test, **read and understand** the source code and extract its **Contract**:

> **Contract Question:** _"ฟังก์ชันหรือโมดูลนี้รับประกันอะไร (What does this function guarantee)?"_
> Test ควรตรวจ Contract เหล่านี้ ไม่ใช่รายละเอียดภายใน (Implementation Details)

1. **Identify the 4 Contract Elements:**
   - **Input:** ชนิดของข้อมูล ขอบเขต และค่าที่เป็นไปได้
   - **Output:** ค่าที่ส่งกลับเมื่อทำงานสำเร็จ
   - **Side Effect:** การเปลี่ยนแปลงภายนอก (เช่น เรียก API, บันทึก log, อัปเดต state)
   - **Error:** สถานการณ์ที่ต้อง throw / reject (เช่น validation fail, dependency timeout)
2. **Apply the Refactor Litmus Test:**
   - ถามตนเอง: _"ถ้าเรา Refactor Implementation แต่ Output และ Behavior ยังเหมือนเดิม Test นี้ควร Fail หรือไม่?"_
   - ถ้าตอบว่า "Fail" แปลว่ากำลัง test implementation detail หรือ intermediate variables!
3. **Identify dependencies** — what does this module import? Which need mocking?
4. **Identify business rules & boundaries** — what conditions, branches, and edge cases exist?
5. **Check for existing tests** — avoid duplicating what's already tested

Build a mental map:

```
Function: calculateDiscount(price, userRole, couponCode)
├── Contract:
│   ├── Inputs: price (number), userRole (enum), couponCode (string | null)
│   ├── Output: { finalPrice: number, discountApplied: boolean }
│   ├── Side Effects: none
│   └── Errors: throws InvalidPriceError if price < 0
├── Dependencies: CouponService.validate() ← needs mock
├── Business rules:
│   ├── price < 0 → throw InvalidPriceError
│   ├── userRole "vip" → 20% discount
│   ├── userRole "member" → 10% discount
│   ├── userRole "guest" → 0% discount
│   ├── valid coupon → additional 5% off
│   └── discount cap at 50% max
└── Representative Edge cases: price = 0, coupon expired, unknown role
```

---

### Step 3: Design Test Scenarios

For each function, design scenarios BEFORE writing code.
See [references/scenario-design.md](references/scenario-design.md) and [references/case-types.md](references/case-types.md).

For each business rule, think through:

| Type              | Question                                 | Example                                               |
| ----------------- | ---------------------------------------- | ----------------------------------------------------- |
| **Happy path**    | What happens when everything is correct? | VIP user with valid coupon gets 25% off               |
| **Negative path** | What should the system reject?           | Negative price → throw error                          |
| **Error case**    | What if a dependency fails?              | CouponService throws timeout → handle gracefully      |
| **Boundary case** | What about values at the edge?           | Discount = exactly 50% (cap)                          |
| **Edge case**     | What about unusual inputs?               | price = 0, coupon = empty string, role = unknown enum |

Group scenarios by the business rule they validate, not by input type.

> 💡 **การกำหนดค่าตัวแปรและข้อมูลทดสอบ (Test Values & Data):**
> หากต้องการเทคนิคในการคำนวณและกำหนดค่าที่จะนำมาใช้ใน test case แต่ละตัวอย่างเป็นระบบ (เช่น การหาค่าขอบเขต min-1, min, min+1 ด้วย BVA หรือการเลือกตัวแทน Equivalence Partitions ด้วย EP) **ให้อ่านและปฏิบัติตามแนวทางของ [`swe-test-engineer`](../swe-test-engineer/SKILL.md)**

---

### Step 4: Write Test Code

Write the test file following:

- **Arrange–Act–Assert** pattern — see [references/aaa-pattern.md](references/aaa-pattern.md)
- **Business-language naming** — see [references/naming-conventions.md](references/naming-conventions.md)
- **Proper mocking** — see [references/mocking-guide.md](references/mocking-guide.md)

#### Test File Structure

```typescript
// 1. Imports
import { describe, it, expect, beforeEach, vi } from 'vitest' // or Jest globals
import { calculateDiscount } from './discount-service'
import { CouponService } from './coupon-service'

// 2. Mock declarations (top-level)
vi.mock('./coupon-service')

// 3. Test suite grouped by function/behavior
describe('calculateDiscount', () => {
  // 4. Shared setup
  beforeEach(() => {
    vi.clearAllMocks()
  })

  // 5. Grouped by business rule
  describe('price validation', () => {
    it('should throw InvalidPriceError when price is negative', () => { ... })
    it('should return zero finalPrice when price is zero', () => { ... })
  })

  describe('role-based discount', () => {
    it('should apply 20% discount for VIP users', () => { ... })
    it('should apply 10% discount for member users', () => { ... })
    it('should apply no discount for guest users', () => { ... })
  })

  describe('coupon handling', () => {
    it('should apply additional 5% when coupon is valid', () => { ... })
    it('should ignore coupon when coupon is null', () => { ... })
    it('should handle CouponService timeout gracefully', () => { ... })
  })

  describe('discount cap', () => {
    it('should cap total discount at 50% even if role + coupon exceeds it', () => { ... })
  })
})
```

#### Key Rules When Writing

1. **One behavior per test & The "And Smell"** — each test must focus on a single behavior. If a test name contains "and" multiple times (e.g. `formats price and handles errors and logs result`), split it into distinct tests!
2. **Descriptive names for CI diagnostics** — prefer active verbs (`returns formatted price for USD`, `throws if currency is invalid`) so failures in CI are immediately clear. Respect existing project conventions if `should ... when ...` is already dominant.
3. **Use representative boundary values** — do not test infinite variations. Select representative values for valid, boundary, and error paths (see `parseAge` in [references/case-types.md](references/case-types.md)).
4. **Mock only external dependencies** — do NOT mock the function under test or internal helper variables.
5. **Always clean up mocks & environment** in `beforeEach` or `afterEach` (including `process.env`).
6. **Always `await` async assertions** — use `await expect(promise).rejects.toThrow(CustomError)` to avoid floating promises.
7. **Use resilient matchers** — prefer `.toMatchObject()` or `expect.objectContaining()` for dynamic entities (dates, IDs), and assert Error Classes/Codes rather than fragile message strings.

---

### Step 5: Organize Test Files as Projects Grow

See [references/project-file-structure.md](references/project-file-structure.md) for details.

- **Default (Recommended):** Co-locate test files directly next to source files (`service.ts` + `service.test.ts`).
- **Large modules (>300 lines of tests):** Split by behavior/domain capability (`order.validation.test.ts`, `order.discount.test.ts`).
- **Shared test data & fixtures:** Centralize in `src/test/factories/` or `src/test/fixtures/` instead of duplicating mocks across tests.
- **Respect codebase convention:** If the project already uses a centralized `__tests__/` directory, follow that pattern.

---

### Step 6: Validate Quality

After writing tests, run through this checklist.
See [references/first-principles.md](references/first-principles.md).

**FIRST Principles Check:**

- [ ] **Fast** — no real API calls, no database, no file system, no `setTimeout`
- [ ] **Independent** — can run any test in isolation, no shared mutable state
- [ ] **Repeatable** — no dependency on system clock, network, or un-reset `process.env`
- [ ] **Self-Validating** — clear, precise `expect()` assertions (no weak `toBeTruthy()` on objects, no dummy coverage)
- [ ] **Timely** — tests are written alongside the production code

**Coverage Check:**

- [ ] Happy path covered for every public function
- [ ] At least one negative case per validation rule
- [ ] Error handling tested for every external dependency
- [ ] Boundary values tested using representative values (min, max, invalid edges)
- [ ] Edge cases tested (null, undefined, empty string, 0, max values)

**Anti-Pattern Check** — see [references/anti-patterns.md](references/anti-patterns.md):

- [ ] No test asserts on internal implementation details or intermediate variables
- [ ] Refactor Check passed: If implementation changes without altering behavior, test still passes
- [ ] No test has more than one Act phase or suffers from "And Smell"
- [ ] All async rejection tests have `await expect(...).rejects` (no floating promises)
- [ ] Error assertions check Custom Error Classes or Error Codes, not fragile message strings
- [ ] Dynamic objects use `.toMatchObject()` or `expect.objectContaining()` instead of brittle full `.toEqual()`
- [ ] Any `process.env` mutations are restored in `afterEach`
- [ ] Test names clearly identify the failing behavior for CI logs
- [ ] No copy-pasted tests that should be `it.each`

---

### Step 7: Run Tests

After writing, always run the test to verify:

```bash
# Vitest
npx vitest run <path-to-test-file>

# Jest
npx jest <path-to-test-file> --no-coverage
```

If tests fail, fix them. Do NOT submit tests that you haven't verified pass.

---

## Relationship to Other Testing Skills

```
swe-test-planner           → "ควร test อะไรก่อน?"                  (Risk-based prioritization)
swe-test-engineer          → "กำหนดค่า test data & case อย่างไร?" (BVA/EP/STT → test data & values)
swe-test-unit-test-writer  → "เขียนโค้ด .test.ts ยังไง?"           (Actual test code) ← YOU ARE HERE
```

> 🎯 **คำแนะนำสำคัญเรื่องการกำหนดค่า (Test Data & Values):**
> **การกำหนดค่าที่จะใช้ในการเขียน test ให้ไปอ่านที่ [`swe-test-engineer`](../swe-test-engineer/SKILL.md) เสมอ**
> - สกิล `swe-test-engineer` จะสอนการเลือกค่า input อย่างเป็นระบบ (BVA สำหรับตัวเลข/ช่วงเวลา, EP สำหรับ partition ค่าทั่วไป, STT สำหรับสถานะ)
> - เมื่อได้ตาราง Test Cases และค่าตัวแทน (TC-01, BT-01 ฯลฯ) จาก `swe-test-engineer` แล้ว ให้นำค่านั้นมาเขียนเป็นชุดโค้ด Test ใน `swe-test-unit-test-writer` ทันที

---

## Examples

See [references/examples.md](references/examples.md) for complete worked examples.

**Trigger phrases:**

- "เขียน unit test ให้ function นี้"
- "สร้าง test file สำหรับ service นี้"
- "เพิ่ม test coverage ให้ module นี้"
- "write unit tests for this TypeScript module"
- "refactor these tests to follow best practices"
