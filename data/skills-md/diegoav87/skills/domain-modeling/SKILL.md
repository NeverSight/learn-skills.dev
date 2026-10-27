---
name: domain-modeling
description: Build and sharpen a project's domain language. Use when discussing codebase terminology, or when writing or editing a GLOSSARY.md.
---

# Domain Modeling

Actively build and sharpen the project's domain language as you design: challenge terms, invent edge-case scenarios, and write the glossary down the moment a term settles. (Reading `GLOSSARY.md` for vocabulary is a habit any skill has. This skill is for changing the language, not consuming it.)

## The glossary

One `GLOSSARY.md` at the repo root, in a monorepo too. Create it lazily, when the first term is resolved. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

It is a glossary and nothing else. A decision settled in the session lives in the conversation, then in the spec; once built, the code holds it.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there, as it happens.

When a term's meaning changes, rewrite its entry so it states the new meaning. When the project stops using a term, delete its entry.
