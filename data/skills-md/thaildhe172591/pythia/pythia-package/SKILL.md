---
name: pythia-package
description: Use when designing or writing a new package, procedure, function or trigger, or restructuring one - "viet package", "tao procedure", "them function", "them trigger", an API another team will call, an error-handling or logging design, a spec change. Applies the industry-standard PL/SQL design rules - the spec as a contract, named exceptions, one transaction owner, thin triggers - beneath the house conventions, which always win.
---

# Designing Packages, Procedures, Functions, Triggers

**Announce at start:** "Using pythia-package — designing the spec before the body."

**Phase:** Learn → Ask → Do — neighbours and callers first, the contract agreed, then spec and body as two files

`pythia-write` makes new code indistinguishable from the codebase. This
skill adds what the codebase may not show: how a unit should be *shaped*
so that callers can trust it. When the house does it differently, the house
wins — `.pythia/conventions.md` first, `reference/plsql-standards.md` for
everything it does not decide.

## The Iron Law

```
THE SPEC IS A CONTRACT: DESIGN IT FIRST, AND NEVER BREAK IT SILENTLY
```

A package spec change invalidates every dependent at once; a body change
invalidates nothing. That asymmetry decides most of the design.

## The Workflow

1. **Learn** — `pythia similar <NAME>` and `pythia src` on the top two or
   three; `pythia args` for every unit you will call; `pythia impact <PKG>`
   when the package exists (a spec change reaches all of it); `pythia cols`
   for every table touched.
2. **Shape the contract** (open behaviour goes to `pythia-spec` first):
   - **Package, not standalone**, unless the house writes standalone units:
     encapsulation, private helpers, and body changes that invalidate nobody.
   - **Public surface = what callers need.** Everything else private, in
     the body only. New public items go at the **end** of the spec — with
     fine-grained dependency tracking (11g+) existing dependents stay VALID.
   - **Parameters** anchored with `%TYPE`; `IN` by default; `OUT` only in
     procedures; `NOCOPY` for large `IN OUT` collections and LOBs; defaults
     only for genuinely optional inputs.
   - **Functions** return one thing, have no `OUT` parameters, and do no
     DML when they can be called from SQL.
   - **Error contract**: named exceptions in the spec, or one documented
     `-20xxx` range per package; callers can tell "not found" from "broken".
   - **Transaction contract**: the outermost caller commits. A unit that
     commits says so in its name or its spec comment — it cannot be
     composed into a larger transaction.
   - **Logging/instrumentation** through the house logger;
     `DBMS_APPLICATION_INFO.SET_MODULE/SET_ACTION` on long-running entry
     points so a DBA can see what runs.
   - **Security**: `AUTHID DEFINER` unless the spec needs invoker rights;
     `ACCESSIBLE BY` (12c) for internal helpers; `DBMS_ASSERT` for any
     identifier that reaches dynamic SQL; no credentials in code.
3. **Write two files** — spec, then body (one object per file, `/` at the
   end, `pythia unistr` for Vietnamese messages). Templates in
   `reference/plsql-standards.md`; comments through `pythia-comment`.
4. **Triggers stay thin**: derivation and audit only — no business process,
   no `COMMIT`, no calls to remote systems. Several timing points on one
   table → one compound trigger (also the cure for ORA-04091, mutating
   table). Business rules belong in the API package the trigger would
   otherwise hide.
5. **Check** — `pythia lint spec.sql body.sql`, then `pythia-review`.
6. **Land** — spec first, then body: `pythia deploy spec.sql body.sql`
   (one approval, in order) or two `pythia apply` runs. Exit 3 is broken,
   never done.
7. **Verify** — `pythia errors <PKG>`, `pythia invalid` against the
   baseline, `pythia plscope <PKG>` for unused or never-assigned
   identifiers.

## Red Flags — STOP if you catch yourself thinking

| Thought | Reality |
|---------|---------|
| "I'll just add a parameter to the existing procedure" | Every caller breaks or recompiles. Add an overload or a new unit at the end of the spec. |
| "WHEN OTHERS THEN log; is enough" | Without `RAISE` the caller believes it worked. Log, then re-raise. |
| "COMMIT at the end to be safe" | Now nobody can call it inside their transaction. The caller owns the commit. |
| "The trigger is the easiest place for this rule" | And the hardest to find, test and bypass for a data fix. API package. |
| "PRAGMA AUTONOMOUS_TRANSACTION fixes the mutating table" | It hides the error and reads stale data. Compound trigger. |
| "Concatenating the table name is fine, it's internal" | Internal today. `DBMS_ASSERT.SQL_OBJECT_NAME` costs one call. |
| "Standards say X, the codebase does Y" | The codebase wins; propose X separately. |

## When NOT to use this skill

- A small edit inside an existing unit → `pythia-write` is enough.
- Table design → `pythia-table`. Performance → `pythia-tune`.
- Reviewing someone else's unit → `pythia-review`.
