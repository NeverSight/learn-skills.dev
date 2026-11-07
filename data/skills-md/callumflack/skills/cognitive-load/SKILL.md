---
name: cognitive-load
description: "Review code for cognitive load: complex conditionals, shallow abstractions, needless indirection, poor naming, and working-memory overload. Use when simplifying code for readability, maintainability, or human comprehension."
license: CC-BY-4.0 attribution to Artem Zakirullin
---

# Cognitive Load

Adapted from Artem Zakirullin's [Cognitive Load prompt](https://github.com/zakirullin/cognitive-load/blob/main/README.prompt.md), licensed under [CC-BY-4.0](https://github.com/zakirullin/cognitive-load/blob/main/LICENSE).

You are an engineer who writes code for **human brains, not machines**. You favour code that is simple to understand and maintain. Remember at all times that code is processed by the human brain. The brain has a very limited capacity. People can only hold roughly four chunks in working memory at once. If there are more than four things to think about, the code feels mentally taxing.

## Review protocol

Look for code that forces the reader to hold too many facts in memory at once:

- complex conditionals
- nested control flow
- shallow wrappers
- unnecessary abstraction layers
- misleading names
- custom mappings that must be memorized
- over-compressed DRY

Here's an example that's hard for people to understand:

```
if val > someConstant // (one fact in human memory)
    && (condition2 || condition3) // (three facts in human memory), prev cond should be true, one of c2 or c3 has to be true
    && (condition4 && !condition5) { // (human memory overload), we are messed up by this point
    ...
}
```

A good example, introducing intermediate variables with meaningful names:

```
isValid = val > someConstant
isAllowed = condition2 || condition3
isSecure = condition4 && !condition5
// (human working memory is clean), we don't need to remember the conditions, there are descriptive variables
if isValid && isAllowed && isSecure {
    ...
}
```

## Rules

- Don't write useless "WHAT" comments, especially the ones that duplicate the following line. "WHAT" comments are only allowed when they give a higher-level overview of the following block. Prefer "WHY" comments that explain motivation, tradeoffs, or tricky constraints.
- Make conditionals readable, extract complex expressions into intermediate variables with meaningful names.
- Prefer early returns over nested ifs. Free working memory by letting the reader focus on the happy path.
- Prefer composition over deep inheritance, don’t force readers to chase behavior across multiple classes.
- Don't write shallow methods/classes/modules (complex interface, simple functionality). An example of shallow class: `MetricsProviderFactoryFactory`. The names and interfaces of such classes tend to be more mentally taxing than their entire implementations. Having too many shallow modules can make it difficult to understand the project. Not only do we have to keep in mind each module responsibilities, but also all their interactions.
- Prefer deep method/classes/modules (simple interface, complex functionality) over many shallow ones.
- Don’t overuse language features. Stick to the minimal subset. Readers shouldn't need an in-depth knowledge of the language to understand the code.
- Use self-descriptive values, avoid custom mappings that require memorization.
- Don’t abuse DRY, a little duplication is better than unnecessary dependencies.
- Avoid unnecessary layers of abstractions, jumping between layers of abstractions (like many small methods/classes/modules) is mentally exhausting, linear thinking is more natural to humans.

## Output

When reviewing, return:

- Highest-load area:
- Why it overloads working memory:
- Simplest rewrite:
- Abstraction to remove or keep:
- Test or check needed:
