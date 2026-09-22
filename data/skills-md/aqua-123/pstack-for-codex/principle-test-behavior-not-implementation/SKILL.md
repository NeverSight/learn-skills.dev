---
name: principle-test-behavior-not-implementation
description: "Apply when you write, change, or keep a test. Call the code the way its users do and assert the result they observe against a literal expected value."
---

# Test Behavior, Not Implementation

A test calls the code the way its users do and asserts the result they observe against a literal expected value. If every imported function returned `undefined`, a useful test would fail when the subject's behavior is wrong.

Rewrite tests that only assert calls, truthiness, presence, constants, mocks, or fixture shape. Test the mechanism with one concrete input and a literal output or observable effect. Keep relation checks when the relation itself is the contract.
