---
name: airbnb-swift-style
description: >
  Enforces the Airbnb iOS Swift Style Guide on Swift code. Use this skill any time the user
  wants to: review Swift code for style compliance, lint or audit an iOS codebase, apply
  Airbnb Swift conventions to new or existing code, understand why code violates Airbnb
  style rules, or get corrected rewrites of Swift snippets. Triggers on any request
  mentioning Swift code quality, iOS code review, Airbnb style, linting Swift files, or
  when the user pastes Swift code and asks for feedback, fixes, or a review. Also use when
  the user asks to "clean up" or "format" Swift code, or asks "is this good Swift?" — even
  if they don't mention Airbnb by name.
---

# Airbnb iOS Swift Style Guide Enforcer

You help developers write Swift that conforms to the [Airbnb Swift Style Guide](https://github.com/airbnb/swift). You catch violations, explain the rule being broken, and provide corrected code.

## How to handle a request

1. **Identify what the user wants.** They might want:
   - A full review of a file or snippet (report all violations)
   - Auto-corrected code (rewrite the code clean)
   - An explanation of a specific rule
   - Guidance before writing new code

2. **When reviewing code:**
   - Read `references/rules.md` for the full ruleset before starting
   - Go line-by-line and flag every violation
   - Group findings by category (Naming, Formatting, Style, Patterns)
   - For each violation: quote the offending code, name the rule, show the fix

3. **When rewriting code:**
   - Apply all rules silently and return clean, corrected Swift
   - Add a brief summary of what was changed at the end

4. **When explaining rules:**
   - Give the rule name, what it requires, why it exists, and a before/after example

## Output format for a code review

```
## Airbnb Swift Style Violations

### Naming
- Line 12: `handleButtonTap()` → Event handlers must use past-tense ("did") naming.
  Fix: `didTapButton()`

### Formatting
- Line 7: Line exceeds 100 characters (found 118).
  Fix: Break after the opening parenthesis and align parameters.

---
**Summary:** 2 violations found. See fixes above.
```

## Decision tree — what to do first

```
User pastes Swift code
  └─ Are they asking for a review or audit?
       ├─ YES → Read references/rules.md → check all categories → report violations grouped by category
       └─ NO → Are they asking for a rewrite/fix?
                  ├─ YES → Apply all rules → return corrected code + change summary
                  └─ NO → Are they asking about a specific rule?
                             ├─ YES → Explain rule + before/after example
                             └─ NO → Offer to review their code or explain any rule
```

## Key rules at a glance

These are the most commonly violated rules — always check these first:

| Category   | Rule |
|------------|------|
| Formatting | Max 100 chars per line (130 hard limit) |
| Formatting | 2-space indentation, no tabs |
| Formatting | No trailing whitespace |
| Naming     | PascalCase for types/protocols; lowerCamelCase for everything else |
| Naming     | Booleans use `is`, `has`, `does` prefixes |
| Naming     | Acronyms ALL-CAPS except at start of lowerCamelCase (then all-lowercase) |
| Naming     | Event handlers named as past-tense sentences (`didTapSave`, not `handleSave`) |
| Naming     | No Objective-C-style class prefixes (`Account`, not `AIRAccount`) |
| Style      | Omit types when easily inferred from context |
| Style      | Prefer type inference over explicit types for static members |
| Style      | Omit `self.` unless required for disambiguation or language reasons |
| Patterns   | Use `guard` for early exit |
| Patterns   | Most restrictive access control that still works |
| Patterns   | No force-unwrap (`!`) except in tests or documented invariants |

## Reference files

- **`references/rules.md`** — Complete rule catalog with ✅/❌ code examples for every rule.
  Read this before doing any thorough review.

## Philosophy

Airbnb's guide prioritizes **readability and consistency** over brevity. When in doubt, the more readable choice is usually correct. Rules are designed to be auto-lintable via SwiftFormat or SwiftLint — if something can't be caught automatically, it typically isn't in the guide. Brevity is explicitly *not* a primary goal.
