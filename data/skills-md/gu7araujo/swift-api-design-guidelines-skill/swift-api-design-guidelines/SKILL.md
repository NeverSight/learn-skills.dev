---
name: swift-api-design-guidelines
description: Applies Apple's Swift API Design Guidelines when writing or reviewing Swift code. Use when writing Swift APIs, naming types and methods, designing Swift libraries, or when the user asks for Swift style, naming, or API design.
---

# Swift API Design Guidelines

Follow Apple's [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/) so code feels consistent with the Swift ecosystem. For full detail and examples, see [reference.md](reference.md).

## When to Apply

- Writing or refactoring Swift types, functions, methods, properties, or parameters
- Reviewing Swift code for API clarity and naming
- User asks for Swift style, naming conventions, or API design

## Fundamentals

- **Clarity at the point of use** is the top goal. Design so call sites read clearly, not just the declaration.
- **Clarity over brevity.** Avoid minimizing character count for its own sake.
- **Document every declaration** with a doc comment. Use Swift's Markdown dialect. Start with a one-line summary (sentence fragment, period). If the API is hard to describe simply, reconsider the design.
- **Document non-O(1) computed properties** so callers don't assume cheap access.

## Naming Checklist

### Promote clear usage

- [ ] Include words needed to avoid ambiguity at the call site (e.g. `remove(at: x)` not `remove(x)`).
- [ ] Omit needless words; avoid repeating type information (e.g. `remove(_ member:)` not `removeElement(_ member:)`).
- [ ] Name variables, parameters, and associated types by **role**, not type (e.g. `ContentView`, `supplier`, not `ViewType`, `widgetFactory`).
- [ ] For weak types (`Any`, `NSObject`, `Int`, `String`), add a noun that clarifies role (e.g. `addObserver(_:forKeyPath:)`).

### Fluent usage

- [ ] Method names should form grammatical phrases at use: e.g. `x.insert(y, at: z)`, `x.capitalizingNouns()`.
- [ ] Factory methods start with **make**: e.g. `x.makeIterator()`.
- [ ] Initializer/factory first argument should **not** continue the base name as a phrase (e.g. `Color(red: 32, green: 64, blue: 128)`; avoid `Color(havingRGBValuesRed: 32, ...)`).
- [ ] **Side-effect-free** → noun phrase: `x.distance(to: y)`. **With side effects** → imperative verb: `x.sort()`, `x.append(y)`.
- [ ] Mutating/nonmutating pairs: verb imperative for mutating, **-ed** or **-ing** for nonmutating (e.g. `reverse()` / `reversed()`; `stripNewlines()` / `strippingNewlines()`). Noun-based: nonmutating = noun, mutating = **form** prefix (e.g. `union(_:)` / `formUnion(_:)`).
- [ ] Boolean uses read as assertions: `x.isEmpty`, `line1.intersects(line2)`.
- [ ] **Types/protocols (what something is)** → nouns (e.g. `Collection`). **Capability protocols** → `-able`, `-ible`, or `-ing` (e.g. `Equatable`, `ProgressReporting`).

### Terminology

- [ ] Prefer common words unless a term of art is needed; use terms in their established meaning.
- [ ] Avoid abbreviations unless meaning is easy to find (e.g. web search). Prefer precedent (e.g. `Array`, `sin(x)`).

## Conventions Checklist

### General

- [ ] Prefer methods and properties over free functions unless: no obvious `self`, unconstrained generic, or domain notation (e.g. `min(x,y,z)`, `print(x)`, `sin(x)`).
- [ ] **Case**: types and protocols `UpperCamelCase`; everything else `lowerCamelCase`. Acronyms follow case: `utf8Bytes`, `userSMTPServer`; others as words: `radarDetector`.
- [ ] Methods can share a base name only when meaning is the same or domains are distinct. Avoid overloading on return type.

### Parameters

- [ ] Parameter names should read well in documentation (e.g. `filter(_ predicate:)`, `replaceRange(_ subRange:, with newElements:)`).
- [ ] Use defaulted parameters to simplify common uses; prefer one method with defaults over method families.
- [ ] Put parameters with defaults at the end.
- [ ] Production APIs: prefer `#fileID`; use `#filePath` only for dev-only helpers; use `#file` for Swift 5.2 compatibility.

### Argument labels

- [ ] Omit all labels when arguments can't be distinguished: `min(a, b)`, `zip(s1, s2)`.
- [ ] **Value-preserving type conversion** initializers: omit first label, e.g. `Int64(someUInt32)`, `String(veryLargeNumber, radix: 16)`. Narrowing conversions: use a descriptive label (e.g. `init(truncating:)`, `init(saturating:)`).
- [ ] First argument in a prepositional phrase → label starting at preposition: `x.removeBoxes(havingLength: 12)`. Single abstraction (e.g. coordinates) → label after preposition: `a.moveTo(x:b, y:c)`.
- [ ] First argument that completes a grammatical phrase → omit label, e.g. `x.addSubview(y)`. Otherwise use a label: `view.dismiss(animated: false)`, `words.split(maxSplits: 12)`.
- [ ] All other arguments have labels.

## Special instructions

- [ ] Name tuple members and closure parameters where they appear in the API.
- [ ] With unconstrained polymorphism (`Any`, `AnyObject`, unconstrained generics), avoid overload ambiguity (e.g. name `append(contentsOf:)` distinctly from `append(_:)` when `Element` could be `Any`).

## Doc comment summary rules

- **Function/method**: what it does and what it returns; omit void and no-op.
- **Subscript**: what it accesses.
- **Initializer**: what instance it creates.
- **Other declarations**: what the entity is.

Use symbol command bullets when useful: `Parameter`, `Returns`, `Throws`, `Note`, `SeeAlso`, etc.

## Additional resources

- Full guidelines and code samples: [reference.md](reference.md)
- Official source: [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
