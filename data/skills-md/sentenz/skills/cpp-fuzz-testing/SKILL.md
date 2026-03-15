---
name: cpp-fuzz-testing
description: Automates fuzz test creation for C++ projects using Google FuzzTest with consistent software testing patterns. Use when creating fuzz tests, mutation testing, or when the user mentions fuzzing, AFL, or coverage-guided testing.
metadata:
  version: "1.1.0"
  activation:
    implicit: true
    priority: 2
    triggers:
      - "fuzz"
      - "fuzzing"
      - "fuzztest"
      - "afl"
      - "mutation testing"
      - "coverage-guided"
    match:
      languages: ["cpp", "c", "c++"]
      paths: ["src/**/*_fuzz.cpp", "tests/**/*_fuzz.cpp", "fuzz/**/*.cpp"]
      prompt_regex: "(?i)(fuzz|fuzzing|fuzztest|afl|mutation test|coverage-guided)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# Fuzz Testing

Instructions for AI coding agents on automating fuzz test creation using consistent software testing patterns in this C++ project.

<!-- TODO: Add fuzz testing instructions -->
