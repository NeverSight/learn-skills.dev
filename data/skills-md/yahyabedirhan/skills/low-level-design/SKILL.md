---
name: low-level-design
description: Design, explain or redesign code at the level of modules, classes, files and folders, through the low-level design delivery framework. Use when designing a new project or feature from a spec, explaining how an existing codebase is structured, restructuring one, or deciding where code should live.
---

# Low-level design

A low-level design decides which modules exist, what state and rules each one owns, how they call each other, and where each file sits. A good one lets a newcomer find what they came for (where the program starts, how to add an endpoint, where the shared logic lives, what a change touches) without reading everything. Produce and present it through the **delivery framework** in every session, whether you are designing, explaining or redesigning, so the user always finds the same things in the same places. The user chooses what the session is for; the framework sets how you lay out the answer. Stop once the user agrees to the design, since building it is done later, from tickets.

The recurring failure is structure added before it is needed: factories with one product, interfaces with one implementation, a file per function. Start from the simplest design that meets the requirements, and add a class, an interface or a pattern only for a named reason, such as a second implementation today or the same edit repeated across several files. Before designing a module, check whether a dependency the project already has provides it, and build only the difference.

## The flow

1. **Restate the session's purpose in one line**, read from the request and its context, so a misreading costs one reply: designing something new, explaining existing code, redesigning it, deciding one thing, or a mix.
   - **Invoked with no instructions inside a project:** write down that project's current design.
   - **When the purpose isn't clear:** ask what the user wants from the session: a new design, an explanation of the existing code, or a change to it. Check yourself whether the code exists.
2. **Work through the delivery framework** below, stage by stage, reading a principles, concepts or patterns reference when a decision calls for it.
3. **Present, take feedback and revise** until the user agrees.
4. **Keep the design where the user wants it.**

The purpose decides how the stages are walked. The cases below are common, not the only options: a session can mix them, move from one to another, such as an explanation turning into a redesign, or be something else, so fit the framework to what the user asked for.

- **Designing something new:** a complete first draft through every stage, from the user's spec.
- **Explaining existing code:** walk the code through the stages as it is, without changing it.
  - Build each stage from the evidence. Start from an existing design document and check it against the code, then the code itself: entry points, types, folders and tests. The user's description is evidence too. Cite the file behind each claim.
  - Mark requirements read from behaviour and tests **inferred**. Mark what the code can't show, such as why a choice was made or what is planned, **unknown**, and ask about it rather than filling it in.
  - Show what each file owns and, where a file mixes several things, what it mixes. Report weaknesses as observations without proposing changes, since this session leaves the code as it is.
  - Answer follow-up questions by tracing a call through the design.
- **Redesigning existing code:** explain it first and get the user's agreement that it's right. Then redesign it through the same stages, changing only what the redesign needs: a small change runs only the stages it touches, a restructure runs them all. Show the before and after of every stage that changed, including the folder tree.
- **Deciding one thing,** such as "should this be an interface?" or "where does this module go?": answer it with the part of the design it touches, the requirement behind it, the options with their trade-offs, and a recommendation.

## The delivery framework

```text
Requirements → Entities and relationships → Class design → Implementation → Extensibility
```

Each stage rests on the one before it: the entities come from the requirements, the classes give the entities state and behaviour, the implementation proves the classes work, and extensibility tests them against what comes next. Move to the next stage once the current one has everything its product lists. Go back to an earlier stage when a later one exposes a gap. Avoid two opposite failures: writing code before the structure is clear, and polishing details so long that the design never comes together.

### Requirements

Turn the request or spec into something to design against, working down four themes:

- **Capabilities**: the operations the system must support.
- **Rules and completion**: what defines success and failure, and when the system stops or changes state.
- **Error handling**: how it responds to invalid input and illegal actions.
- **Scope**: what is in (core logic, business rules), and what is explicitly out (UI, storage, concurrency, whatever the user excludes). The exclusions keep the design from growing features nobody asked for.

Show them as a short numbered list. A mapping from requirement to module fits as a small table once the modules exist.

### Entities and relationships

Take the nouns from the requirements. A noun that holds changing state or enforces rules is an entity; one that is only information attached to another is a field on it. This keeps the design from splitting into many tiny objects.

Then settle how they relate: which entity is the orchestrator, which own durable state, which has, uses or contains which, and where each rule lives.

Show the entities as a short list and the relationships as arrows (`Game -> Board`). Boxes and arrows are enough; skip formal UML.

### Class design

Turn each entity into a class or module, top-down from the orchestrator, and derive its state and behaviour from the requirements rather than from intuition:

- **State**: what it must remember to enforce the requirements it owns.
- **Behaviour**: what callers must be able to ask or tell it, each operation with what it returns and rejects, in a small API where each method matches a real action or question.

Keep each rule with the module that owns its state (**tell, don't ask**): lifecycle rules ("can this run now?") belong to the orchestrator, data rules ("is this cell taken?") to the module holding the data, so when something breaks you know which module to open. Place the modules in folders following [layout.md](references/layout.md).

Show the folder tree with one comment per line saying what each file or folder owns.

### Implementation

Sketch the methods that carry the logic, not every method: the happy path first (the steps, the calls into other modules, the state changed), then the edge cases (invalid input, illegal operations, calls in the wrong state). Write pseudocode unless the project needs real code.

Then verify: trace one concrete scenario step by step, with the state after each step, plus one rejection, and fix what the trace reveals, such as a state never set or a rule checked too late.

Show a traced flow as a call tree, with the owning file beside each call.

### Extensibility

List the changes likely to come next, and for each one name the part of the design that absorbs it and what changes. A design that routes every state change through one place takes a feature like undo without restructuring. A change that lands in one new file plus a registration is already absorbed; one that repeats the same edit across several files needs a seam. Refuse the changes the current requirements don't need, rather than designing for them.

Show the changes as a small "change → what you touch" table.

## Presenting and revising

Load `/show-me` and present every stage visually, with prose only for the reasons behind choices.

- Keep one current version of the design and revise it rather than starting over.
- Open each revision with what changed and why, as a before/after `diff` of the tree or list that changed, and carry a change through every part it affects.
- Leave a point the user settled as it is unless they reopen it.
- When the design has more than one reasonable option, number the options side by side, each with its cost, and lead with your recommendation.
- Ask only what the code, the spec and the project's docs can't settle, one question at a time. Decide the rest and say what you decided.

## Keeping the design

The user decides what is kept and where. While the design is being refined, keep it in a draft in the project's temp or scratch folder, following the repository's conventions; when it has none, ask where. An explanation can stay in the conversation. Once the user agrees and wants the design kept, write it into the project's documentation, and update an existing design document rather than adding a second, so the project has one. Open it with what a newcomer needs first, then give each stage its own section.

## References

### Principles, concepts and patterns

| Reference | Covers |
|---|---|
| [design-principles.md](references/design-principles.md) | KISS, DRY, YAGNI, separation of concerns, Law of Demeter, SOLID |
| [oop-concepts.md](references/oop-concepts.md) | Encapsulation, abstraction, polymorphism, inheritance and composition |
| [design-patterns.md](references/design-patterns.md) | Creational, structural and behavioural patterns, and when each is over-engineering |
| [layout.md](references/layout.md) | Folders, generic and business code, naming, when to split a file |

---

Source: Hello Interview, [Introduction](https://www.hellointerview.com/learn/low-level-design/in-a-hurry/introduction) and [Delivery Framework](https://www.hellointerview.com/learn/low-level-design/in-a-hurry/delivery).
