---
name: naming-review
description: Review filenames and source-code identifiers for clarity, precision, consistency, and ambiguity. Use when the user asks to inspect or improve names of files, modules, types, functions, methods, parameters, argument labels, properties, variables, constants, enum cases, or related code resources. Do not use for a general code review that has no naming focus.
---

# Naming Review

## Goal

Choose the shortest name that still communicates the correct domain meaning at both its declaration and use sites. A good name should let a reader predict what something represents or does without first opening its implementation.

Judge names in context rather than as isolated words. Concision is not fewer characters at any cost, and precision is not maximum verbosity.

## Scope and Authorization

- For requests to check, audit, review, or recommend names, perform a read-only review. Do not rename code unless the user explicitly asks for changes.
- For explicit rename or refactor requests, update the declarations and every in-scope use while preserving external compatibility where required.
- Stay focused on naming. Mention a non-naming defect only when it prevents a correct naming judgment or creates a material risk during a requested rename.
- Follow the target language's established API design guidance and the repository's consistent local terminology. Do not impose conventions from another language.

## Review Workflow

1. Establish the requested scope. Read the complete target files, then inspect relevant call sites, neighboring types, tests, and configuration with fast code search such as `rg`.
2. Infer each name's actual role from behavior and usage: domain concept, ownership, cardinality, lifecycle, side effects, units, representation, and whether it is internal or externally visible.
3. Inventory every requested naming category. For a comprehensive review, include acceptable names as well as problematic ones so the user can tell the scope was fully checked.
4. Evaluate names with the criteria below and distinguish material ambiguity from personal stylistic preference.
5. Lead the report with the overall verdict, then present prioritized findings and one coherent recommended naming scheme.

## Evaluation Criteria

For every name, ask:

- **Meaning:** Does it describe the domain concept or behavior rather than merely its storage type or implementation?
- **Precision:** Could a reasonable reader interpret it in another materially different way?
- **Context:** Does the surrounding type, namespace, or call site already supply words that the name repeats?
- **Abstraction:** Is the name at the same abstraction level as the code it represents?
- **Consistency:** Does the repository use one term for this concept, or does the name introduce a synonym?
- **Truthfulness:** Do words such as `default`, `fallback`, `cached`, `current`, `selected`, `required`, or `async` match actual behavior?
- **Representation:** If the type does not reveal an important format or unit, does the name distinguish values such as seconds versus milliseconds, an asset name versus an image, or a hex string versus a color?
- **Durability:** Is the name tied unnecessarily to an implementation detail likely to change?
- **Call-site readability:** Do functions and argument labels form a natural, non-repetitive phrase where called?

## Category Guidance

### Files, directories, and modules

- A filename should reflect its primary declaration or clear responsibility.
- Avoid catch-all names such as `Helpers`, `Utils`, `Common`, or `Misc` unless the contents genuinely share that stable concept.
- Check case, singular/plural form, suffixes, and extension conventions against neighboring files.

### Types

- Classes, structs, enums, protocols, and type aliases should normally be precise noun or role phrases.
- Prefer a domain noun over generic suffixes such as `Item`, `Object`, `Data`, `Info`, `Manager`, `Handler`, or `Group` when the code represents a more specific concept.
- Keep a generic word when the abstraction itself is genuinely generic; do not rename it only to sound more elaborate.
- Make protocol and generic-parameter names communicate a capability, role, or constraint when the language's conventions support that style.

### Functions and methods

- Use a verb or verb phrase that exposes the operation and material side effects.
- Distinguish operations such as finding, fetching, loading, parsing, creating, updating, saving, and deleting according to their real behavior.
- A name should not promise success, persistence, caching, ordering, validation, or idempotency that the implementation does not provide.
- Avoid repeating argument types or enclosing-type context when the call remains clear without them.

### Parameters and argument labels

- Read the complete call expression aloud. Labels should explain the argument's role, not just restate its type.
- Distinguish source from destination, old from new, minimum from maximum, and identifier from display text when multiple values could be confused.
- Names such as `value`, `data`, `item`, `object`, or `result` are acceptable only when their role is truly generic or fully established by a very small scope.

### Properties, variables, and constants

- Name collections with an accurate plural noun and individual elements with the corresponding singular noun.
- Use names that distinguish an identifier, index, count, key, label, title, path, URL, asset name, localization key, raw value, and rendered value when those differences matter.
- Boolean names should read as predicates at use sites, commonly using language-appropriate forms of `is`, `has`, `can`, `should`, or `did`. Avoid negative names that create double negatives.
- Include units or encoding only when the type and context do not make them clear. Prefer a stronger type over a permanently encoded representation name when a requested refactor can safely introduce one.
- Apply the language and repository convention for initialisms such as ID, URL, HTTP, or UUID consistently.

### Resources and serialized names

- Clarify when a string is really an asset catalog name, localization key, database key, environment variable, notification name, route, or wire-format field.
- Do not assume such strings can be renamed together with a source identifier; first locate their external consumers.

## Findings and Recommendations

Classify each reviewed name as:

- **Keep:** concise, clear, and appropriately scoped.
- **Consider:** understandable, but a proposed name would improve consistency or precision with moderate value.
- **Rename:** materially misleading, ambiguous, inconsistent, or broader/narrower than the represented concept.

For non-trivial reviews, use a compact table containing location, current name, verdict, recommended name, and reason. Prioritize names that can cause misuse or force readers to inspect implementations. Avoid filling the report with low-value synonym swaps.

When several names form a hierarchy, recommend them as one coherent set. For example, do not rename a collection without checking the element type, element variable, default identifier, and related function labels.

## Implementing Requested Renames

Before editing, search for all syntactic and string-based uses. Check especially:

- public APIs and downstream modules;
- serialized keys, `CodingKeys`, database columns, migrations, and wire formats;
- reflection, selectors, dependency injection, route registration, and dynamic lookup;
- analytics events, notifications, environment/configuration keys, localization keys, and asset names;
- tests, previews, documentation, scripts, and generated-code boundaries.

Preserve stable external names with adapters, explicit coding keys, migrations, or deprecation shims when appropriate. Make the smallest coherent rename, avoid unrelated cleanup, and run the narrowest useful build, type-check, or tests after changes.
