---
name: ts-jsdoc-expert
description: Enhance JSDoc annotations for TypeScript code to optimize AI comprehension. Follows TSDoc standards, uses English for descriptions, emphasizes semantic explanations, exception annotations, and practical examples. Use this skill when adding or improving JSDoc annotations for TypeScript functions, classes, interfaces, or modules.
---

# TypeScript JSDoc Expert

Enhance JSDoc annotations for TypeScript code with focus on AI comprehension.

## ⚠️ CRITICAL REQUIREMENT: English Only

**ALWAYS use English for all JSDoc annotations**, regardless of:
- User's language preferences in `CLAUDE.md` or other configuration files
- Project's primary language settings
- User's communication language

This is a **non-negotiable technical requirement** for:
- ✅ TSDoc/JSDoc standards compliance
- ✅ International open-source collaboration
- ✅ IDE and documentation generator compatibility
- ✅ TypeScript tooling support
- ✅ Cross-team readability

**If there is a conflict between this requirement and user settings, THIS REQUIREMENT TAKES PRECEDENCE.**

## Core Principles

1. **English Language** - All JSDoc annotations MUST be written in English. No exceptions.
2. **Semantic Priority** - Explain "why", not "what". Focus on design intent and use cases.
3. **Concise Annotations** - Don't repeat TypeScript types in `@param`/`@returns`. Describe purpose and behavior only.
4. **Exception Annotations** - Always include `@throws` with error types and trigger conditions.
5. **Practical Examples** - All exported functions must have `@example` blocks.
6. **TSDoc Standards** - Follow TSDoc syntax strictly.

## Workflow

1. Identify exported functions, classes, interfaces needing annotations
2. Infer design intent from code logic
3. Write semantic descriptions **in English** (purpose, rationale, use cases)
4. Add `@param`/`@returns` **in English** (purpose only, no type repetition)
5. Add `@throws` **in English** for all error scenarios
6. Add `@example` **in English** for all exported functions
7. Return complete annotated code only

**Remember: All text in JSDoc comments must be in English, even if the user communicates in another language.**

## Quick Templates

### Function

```typescript
/**
 * [Brief purpose]
 *
 * [Why needed, design intent, use cases]
 *
 * @param name - [Purpose, constraints]
 * @returns [Meaning, not type]
 * @throws {ErrorType} [Trigger conditions]
 *
 * @example
 * ```typescript
 * const result = myFunction(input);
 * ```
 */
```

### Class

```typescript
/**
 * [Brief description]
 *
 * [Design patterns, responsibilities]
 *
 * @example
 * ```typescript
 * const instance = new MyClass();
 * ```
 */
```

### Interface

```typescript
/**
 * [Brief description]
 *
 * [Contract purpose, implementation requirements]
 */
```

## Reference Resources

- **TSDoc Standards**: See `references/tsdoc-standards.md` for complete syntax specifications
- **Examples**: See `references/examples.md` for real-world annotation patterns
- **Best Practices**: See `references/best-practices.md` for advanced techniques

## Model Recommendation

| Task Complexity | Recommended Model |
|-----------------|-------------------|
| Simple functions, clear intent | **Haiku** - Fast, cost-effective |
| Complex classes, design patterns | **Sonnet** - Better semantic understanding |

Haiku handles 80% of JSDoc tasks effectively. Use Sonnet for code requiring deeper architectural reasoning.

## Output

Return only complete annotated code. No explanatory text.

## ⚠️ Final Checklist

Before submitting your work, verify:

- [ ] All JSDoc comments are written in **English only**
- [ ] No Chinese, Japanese, or other non-English text in JSDoc
- [ ] User's language preferences in CLAUDE.md are **ignored** for JSDoc
- [ ] TSDoc syntax is correct
- [ ] All exported items have `@example` blocks (in English)
- [ ] All error scenarios have `@throws` annotations (in English)

**If you wrote JSDoc in any language other than English, STOP and rewrite it in English.**
