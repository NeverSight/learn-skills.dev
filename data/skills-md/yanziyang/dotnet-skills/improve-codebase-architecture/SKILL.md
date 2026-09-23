---
name: improve-codebase-architecture
description: Scan a .NET codebase (.NET 8–10, ASP.NET Core or class libraries) for architectural deepening opportunities — pass-through layers, one-implementation interfaces, generic repositories over EF Core, anemic entities, MediatR ceremony, layer-per-project sprawl — and present them as a visual HTML report with before/after diagrams. Use this skill whenever the user asks to review or improve the architecture, find refactoring or simplification opportunities, reduce layers/interfaces/boilerplate, assess tech debt or over-engineering, or asks "how can I make this codebase better/simpler/more testable" — even if they never say the word "architecture".
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 (ASP.NET Core and class libraries)
---

# Improve Codebase Architecture (.NET)

Scan a .NET solution for **deepening opportunities** — refactors that turn shallow modules into deep ones — and present them as a self-contained HTML report with before/after diagrams. The goal is testability and navigability, not style points.

This is a **read-only analysis**. Do not modify any source file during the scan. The output is the report plus a question to the user; refactoring only starts after they pick a candidate.

## Vocabulary — Use These Terms Exactly

Every finding in the report must be phrased with this vocabulary. Consistent terms are what make the report readable; do not drift into synonyms.

| Term | Meaning |
|------|---------|
| **Module** | A unit with an interface and an implementation — a class, an endpoint group, a project. |
| **Interface** | Everything a caller must know to use a module: method signatures, DTOs, exceptions, required call order, config. Bigger than the C# `interface` keyword. |
| **Deep module** | Small interface, lots of functionality behind it. `DbContext` is deep: one class hides change tracking, SQL generation, identity resolution. |
| **Shallow module** | Interface nearly as complex as the implementation. It adds indirection, not abstraction. A service method that forwards to a repository method with the same signature is shallow. |
| **Seam** | A point where implementations can be swapped. In .NET the seam mechanism is DI registration: `AddScoped<IPayments, StripePayments>()`. |
| **Adapter** | An implementation plugged into a seam. **One adapter = hypothetical seam; two adapters = real seam.** An interface whose only second "implementation" is a test mock has one adapter. |
| **Locality** | Related logic lives in one place, so a bug can be found by reading one module instead of five. |
| **Leverage** | One interface serving many call sites. High leverage justifies abstraction cost. |
| **Deletion test** | The core judgment call: *if this module were deleted and its code inlined into its callers, would complexity concentrate (good — delete it) or scatter (keep it)?* |

Never substitute: "component" or "service" for module (except when naming an actual ASP.NET/DI service), "boundary" for seam, "clean" or "maintainable" for a specific win you can name.

## Process

### 1. Map the solution

Build a factual picture before judging anything. Collect:

1. **Projects** — glob for `**/*.sln` and `**/*.csproj`. For each `.csproj`, read the `TargetFramework` and `PackageReference` list. Package references are architecture evidence: `MediatR`, `AutoMapper`, `FluentValidation`, `Dapper`, EF Core providers each imply patterns to check.
2. **Composition root** — read `Program.cs` (and any `ServiceCollectionExtensions` / `DependencyInjection.cs` files it calls). The DI registrations are a census of the app's seams.
3. **Shape** — for each project: rough file count, folder names (`Controllers/`, `Handlers/`, `Repositories/`, `Services/`, `Interfaces/`), and which projects reference which.
4. **Existing decisions** — if `docs/adr/`, `ARCHITECTURE.md`, or `CONTEXT.md` exist, read them. Do not propose reversing a recorded decision unless the friction is severe — and if you do, flag the conflict explicitly in the report card.

Summarize this as a small table (project → role → notable packages) before moving on. If the solution has more than ~15 projects, pick the 3–5 projects where the app's actual behavior lives and scan those deeply rather than skimming everything.

### 2. Scan for shallow patterns

Read [references/dotnet-smells.md](references/dotnet-smells.md) **before** scanning — it contains the detection heuristics (including grep patterns), counter-signals, and the deepening move for each smell. Do not improvise smells from memory; the counter-signals matter as much as the detections.

The catalog, in the order most likely to pay off:

| # | Smell | One-line detection |
|---|-------|--------------------|
| 1 | Pass-through service layer | Service methods that only forward to the next layer with the same parameters |
| 2 | One-implementation interfaces | `IFoo` + exactly one `Foo : IFoo`, referenced only by DI and test mocks |
| 3 | Generic repository over EF Core | `IRepository<T>` / `IUnitOfWork` wrapping what `DbContext` already is |
| 4 | Anemic entities, fat services | Entities that are all auto-properties; invariants enforced by if-throw in services |
| 5 | MediatR/CQRS ceremony for CRUD | Request+handler pairs under ~10 lines with no pipeline behaviors doing real work |
| 6 | AutoMapper hiding the projection | Profile-based mapping where an explicit `Select` would be compile-checked and SQL-translated |
| 7 | Layer-per-project ceremony | 4+ projects in a straight dependency line, some holding <10 files of interfaces/DTOs |
| 8 | Leaky seams | `IQueryable` escaping repositories, EF entities on the wire, `DbContext` used on both sides of a seam |
| 9 | Helper/Manager/Util wrappers | Static classes that wrap one BCL or framework call 1:1 |

For every hit, record **evidence**: file paths, the specific members involved, and a count ("14 of 17 methods on `OrderService` are single-line forwards"). A finding without file-level evidence does not go in the report.

### 3. Grade the candidates

Apply the deletion test to each finding, then assign a strength:

- **Strong** — deletion test clearly passes; two or more smells reinforce each other (e.g. pass-through service + one-implementation interface + repository over EF); the change is mechanical and low-risk; tests get simpler.
- **Worth exploring** — deletion test passes but the change touches many files, or there's a plausible counter-signal you couldn't rule out from reading alone.
- **Speculative** — real friction, but the fix needs a design conversation (e.g. collapsing projects, moving invariants into entities across a large domain).

Cap the report at **6 candidates**. If you found more, keep the ones with the strongest evidence and the most reinforcement between smells. Do not pad with weak findings to look thorough — three Strong candidates beat six Speculative ones.

### 4. Render the HTML report

Read [references/html-report.md](references/html-report.md) for the full scaffold, the candidate card template, diagram patterns, and styling rules. Follow it closely — the scaffold is complete and tested; do not redesign it.

Mechanics:

- Write one self-contained HTML file to the OS temp directory — never into the repo. Resolve the temp dir from `$env:TEMP` (Windows) or `$TMPDIR`/`/tmp` (macOS/Linux); name the file `architecture-review-<yyyyMMdd-HHmmss>.html`.
- Open it for the user: `Start-Process <path>` on Windows, `open <path>` on macOS, `xdg-open <path>` on Linux.
- Tell the user the absolute path in your reply, in case auto-open fails.

Each candidate card must contain: the files involved, the problem (one sentence), the solution (one sentence), a **before/after diagram** (this is the centerpiece — Mermaid for graph-shaped structure, hand-built divs for mass/cross-section shapes), win bullets phrased in the vocabulary (*"locality: pricing bugs concentrate in one module"*, not *"cleaner code"*), and the strength badge. End the report with a **Top recommendation** section naming the one candidate to tackle first and why.

### 5. Stop and ask

Do not start refactoring, do not propose new interfaces, do not write code. After the report is written and opened, summarize the top recommendation in one or two sentences in chat and ask:

> "Which of these would you like to explore?"

When the user picks one, work through it with them: confirm the evidence in detail, agree on the target shape (what the deepened module's interface looks like, what tests survive), and only then edit code. If the user rejects a candidate for a durable reason ("we keep the repository interface because a Dapper implementation ships next quarter"), offer to record it — an ADR if the repo has `docs/adr/`, otherwise a note in `ARCHITECTURE.md` — so a future scan doesn't re-suggest it.

## Rules

- **Read-only until the user picks.** The scan phase changes nothing.
- **Evidence or it doesn't ship.** Every claim in the report cites files and counts.
- **Deepening, not fashion.** Never propose adopting a framework, package, or pattern (CQRS, DDD, vertical slices) as the fix. The fix is always: fewer/deeper modules, closed seams, invariants moved to where the data lives.
- **Counter-signals are findings too.** If a suspicious pattern turns out to be justified (a second real adapter exists, pipeline behaviors carry real leverage), leave it out of the report — or mention it in one line as "checked, justified" if the user would likely ask.
- **Respect recorded decisions.** An ADR conflict gets an explicit amber callout in the card, and only appears at all if the friction genuinely warrants reopening the decision.
