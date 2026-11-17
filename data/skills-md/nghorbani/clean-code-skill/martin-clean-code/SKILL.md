---
name: martin-clean-code
description: "An independent quick-reference for the clean-code principles popularized by Robert C. Martin. Use when applying clean-code frameworks for naming, functions, error handling, classes (SRP/OCP/DIP), unit testing (TDD/F.I.R.S.T.), refactoring, and the smells & heuristics catalog (G1–G36), or when reviewing code for cleanliness."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, framework name, or smell code (e.g. G14)]
---

# Clean Code Principles — Quick Reference

> **Disclaimer** — This is an independent quick-reference for the clean-code *principles and craftsmanship practices* popularized by Robert C. Martin. It does **not** reproduce the book's text, code listings, examples, figures, or chapter structure; it restates the named frameworks and terminology in original, condensed form. It is a practical aid, **not a substitute** for the book — read *Clean Code: A Handbook of Agile Software Craftsmanship* (Robert C. Martin, Prentice Hall, 2008) for the complete, authoritative treatment. All frameworks, terminology, and heuristics are the intellectual property of Robert C. Martin and his publisher.

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference while coding or reviewing.
- **With a topic** — ask about `naming`, `error handling`, `TDD`, `SRP`, `concurrency`; I answer from the Core Frameworks below and the supporting files.
- **With a smell code** — ask about `G14` or `F3`; see the smell-code groups in [cheatsheet.md](cheatsheet.md).
- **For terms or techniques** — see [glossary.md](glossary.md) (definitions) and [patterns.md](patterns.md) (when / how / trade-offs).

When you ask about something not in Core Frameworks, I read the relevant glossary/patterns/cheatsheet file first.

---

## Core Frameworks & Mental Models

**The prime directive.** Clean code does one thing well and *reads like well-written prose*. The only way to go fast is to keep the code clean — always. Apply the **Boy Scout Rule**: leave the code cleaner than you found it on every check-in. Beware **LeBlanc's Law**: *Later equals never.*

**Functions.** Small, then smaller. **Do one thing**, at **one level of abstraction**, and read top-down (**Stepdown Rule**). Arguments: 0 > 1 > 2 > 3; **no flag arguments** (they announce the function does >1 thing), **no output arguments**. **Command Query Separation**: do something or answer something, never both. Prefer **exceptions over return codes**; eliminate duplication (**DRY** — "the root of all evil").

**Naming.** Use intention-revealing, pronounceable, searchable names; avoid disinformation and encodings (no Hungarian/`m_`/`I`-prefix). Classes are nouns, methods are verbs. **One word per concept.** Name length scales with scope. A name that needs a comment is a failed name.

**Comments.** A comment is a failure to express intent in code; the best comment is the one you found a way not to write. **Comments lie** as code drifts. **Delete commented-out code immediately** — version control remembers.

**Objects vs. Data (anti-symmetry).** Objects hide data and expose behavior → easy to add new *types*. Data structures expose data → easy to add new *functions*. Don't build **hybrids**. Obey the **Law of Demeter** — talk only to immediate friends; no train wrecks. **Tell, don't ask.**

**Error handling.** Use **unchecked exceptions** with meaningful context; **wrap third-party APIs**. **Never return null; never pass null** — use a **Special Case object** or empty collection.

**Boundaries.** Wrap foreign types so a vendor change costs little. Write **learning tests** to pin third-party behavior. For not-yet-built code, **code to the interface you wish you had** + Adapter.

**Tests are first-class code.** **Three Laws of TDD**: (1) no production code without a failing test, (2) write only enough test to fail, (3) write only enough code to pass. Clean tests are **F.I.R.S.T.** — Fast, Independent, Repeatable, Self-Validating, Timely. One concept per test. Dirty tests are worse than none, because they rot and take your freedom-to-change with them.

**Classes.** Keep them small — count **responsibilities**, not lines. **SRP**: one reason to change. Maximize **cohesion** (falling cohesion = a class wants to split). Organize for change: **OCP** (extend, don't modify) and **DIP** (depend on abstractions).

**Systems.** **Separate construction from use** — move wiring to `main`/factories/**Dependency Injection**; don't let objects build their own dependencies. Architectures grow incrementally when concerns stay separated; defer decisions to the last responsible moment.

**Emergent design — the Four Rules of Simple Design** (priority order): (1) Runs all the tests, (2) Contains no duplication, (3) Expresses programmer intent, (4) Minimizes classes/methods. Tests first; then refactor (rules 2–4) under green.

**Concurrency.** Decouples *what* from *when* — powerful but hard. Isolate concurrency code (SRP); limit and protect shared mutable data; prefer copies and thread-confinement; learn `java.util.concurrent`. Treat every intermittent failure as a likely threading bug.

**Definition of done.** It **works (tested)** *and* it's **right (clean)**. Working alone is not done — refine successively (stop and clean the moment code starts to rot).

---

## Topic Index

Each topic maps to its entry in **Core Frameworks & Mental Models** above; the smell-code
groups (C/E/F/G/J/N/T) are summarized in [cheatsheet.md](cheatsheet.md).

- **Adapter / boundaries** → Boundaries
- **Architecture / systems** → Systems
- **Cohesion / classes** → Classes
- **Comments** → Comments (smell group C1–C5)
- **Concurrency / threads / deadlock** → Concurrency
- **Dependency Injection / IoC** → Systems
- **DIP / OCP / SRP** → Classes
- **DRY / duplication** → Functions, Emergent design (smell G5)
- **Error handling / exceptions / null** → Error handling
- **F.I.R.S.T. / TDD / testing** → Tests (smell group T1–T9)
- **Formatting** → see [cheatsheet.md](cheatsheet.md)
- **Functions / arguments / flag args** → Functions (smell group F1–F4)
- **Law of Demeter / train wreck** → Objects vs. Data (smell G36)
- **Naming** → Naming (smell group N1–N7)
- **Objects vs data structures** → Objects vs. Data
- **Polymorphism vs switch** → Functions (smell G23)
- **Refactoring / successive refinement** → Definition of done; [patterns.md](patterns.md)
- **Simple Design (four rules)** → Emergent design
- **Smells & heuristics catalog (G/N/F/C/T/E/J)** → [cheatsheet.md](cheatsheet.md)
- **Special Case Pattern** → Error handling; [patterns.md](patterns.md)

## Supporting Files

- [glossary.md](glossary.md) — key terms with concise definitions
- [patterns.md](patterns.md) — concrete techniques (when / how / trade-offs)
- [cheatsheet.md](cheatsheet.md) — one-page quick reference of every rule

---

## Scope & Limits

The principles here are language-agnostic; the original book's examples are written in Java.
This is a condensed reference for *applying* the principles — for the full treatment,
worked examples, and case studies, read the book. For applying these to a specific codebase,
combine with project tools and reviews.
