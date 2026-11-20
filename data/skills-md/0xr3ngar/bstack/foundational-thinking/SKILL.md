---
name: foundational-thinking
description: "Apply before you write logic: the data shapes, the contracts between parts, the one source of truth, and the order of the work."
disable-model-invocation: true
license: MIT
compatibility: "No tools needed."
---

# Foundational-thinking

Get the data right and the code becomes obvious.

- Name the shapes first: the stored record, the settings that a person writes, the payload between two parts. Write each one as an example before any function.
- Keep one source of truth for each fact. Every other copy is derived from it by code, or checked by a test that fails when the two differ.
- Follow the standard when there is one: a specification, the platform's model, the library's types. Name things as the domain names them. Do not invent a second vocabulary.
- An interface takes what its caller knows and returns what its caller needs. Use one options object, not a row of optional parameters.
- Ask what two actors share. If both can write it, give it one owner.
- Order the work so that each step helps the next: remove dead code, then the shared types and contracts, then the features.
