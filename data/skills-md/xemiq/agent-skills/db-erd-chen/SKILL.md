---
name: db-erd-chen
description: >-
  Generates conceptual/logical Entity-Relationship Diagrams (ERDs) in Chen notation, including EER
  specialization/generalization, as uncompressed
  diagrams.net (draw.io) XML files saved in the project's db-design/ folder, together with SVG
  previews and a short summary of entities, relationships and confirmed assumptions. Use it when the user asks to create,
  draw, update, version or reverse-engineer an ERD, entity-relationship diagram, conceptual or logical
  data model, or database design diagram from a domain description, business rules, SQL DDL,
  migrations or ORM models. Asks clarifying questions before generating. Do not use it for physical
  schemas, SQL DDL, migrations, or Mermaid/PlantUML/DBML diagrams.
license: Apache-2.0
compatibility: Any coding agent that can read/write files and run python3 (3.9+, standard library only). Without python3 a manual fallback is defined (references/manual-fallback.md).
metadata:
  author: XemiQ
  version: "0.4.0"
  repository: https://github.com/xemiq/agent-skills
  homepage: https://xemiqlab.com/en
---

# ERD generation skill: Chen notation → diagrams.net

You are acting as a senior data modeler. Turn the user's domain knowledge or existing schema into a
**conceptual/logical ERD in Chen notation**, saved as **diagrams.net XML in `db-design/`**, and
**ask before you draw**. These instructions are tool-agnostic. "Ask the user" means use whatever
way your environment has to ask the user and wait for the answer. "Run" means execute a shell
command. `<skill>` means the directory containing this `SKILL.md`. Run every command from the
**root of the user's repository**, so that `db-design/` is created there and never inside the skill folder.

**Non-negotiable rules (re-read before every step):**
1. **Ask first.** Never write the diagram before the clarification gate (§3) is passed.
2. **Never assume business rules.** Every cardinality, participation, key and rule comes from the
   user's words, the user's answers, the existing schema, or the team convention. Anything else is
   an *open question*, drawn in its least restrictive form. **Unstated participation is always
   `partial (default)`, never `total (default)`**, however obvious the rule seems.
3. **Conceptual only.** No data types, FK columns, junction tables, indexes, SQL or storage details.
4. **The deliverable is diagrams.net XML**, uncompressed, saved as `db-design/<name>.drawio`. The
   renderer adds generated SVG previews of it. Never hand-write images, and never deliver Mermaid,
   PlantUML or DBML.
5. **Always finish with the summary** (entities, relationships, confirmed assumptions, open questions,
   validation result).
6. **Names in English by default.** If the user writes in another language, ask which language the
   diagram's names should use (§3.1 N6). Always talk to the user in their own language.
7. **Never overwrite or delete** previous diagram versions in `db-design/`.

Files in this skill (paths are relative to this file). Read a reference when the step that needs it
comes up, not all of them up front:

| File | Read it when |
|---|---|
| `references/erd-guide.md` | You need a notation or convention detail. It is the team's normative guide, and **its rules take precedence** |
| `references/source-mapping.md` | Steps 2–4: mapping a description, SQL DDL, ORM models or an existing diagram to the model |
| `references/model-schema.md` | Step 6: writing the JSON model and its layout |
| `references/edge-cases.md` | The user cannot or will not answer, the source is unusual, or a script or the filesystem fails |
| `references/manual-fallback.md` | `python3` is not available, and the XML must be written by hand |
| `references/maintenance.md` | You are changing the skill itself (styles, notations, languages, versioning) |
| `scripts/render_erd.py` | Model JSON → `.drawio` + `.summary.md` + `.model.json`. It checks the notation rules |
| `scripts/validate_erd.py` | Self-check of any `.drawio` file (format, catalog, notation, scope, structure, layout) |
| `scripts/export_svg.py` | `.drawio` → SVG previews. The renderer calls it; run it yourself after a manual edit of the `.drawio` |
| `examples/task-tracker/` | The worked example (§9): input, clarification round, model and outputs |
| `tests/test_skill.py` | Regression tests for the scripts. Run them after changing the skill |

---

## 1. When to use it

Use this skill for a new ERD from a domain description, a reverse-engineered ERD from SQL DDL,
migrations or ORM models, or a new version of an ERD already in `db-design/`.

**Do not activate** (or hand off) when the user wants:
- SQL DDL, migrations, ORM code, indexes, or a physical schema. If they ask for both, do the ERD
  with this skill and say that the physical part is out of its scope.
- Mermaid, PlantUML, DBML, or Crow's-foot/UML class diagrams as the deliverable. Explain that this
  skill produces Chen-notation diagrams.net XML, and offer that.
- Questions about an existing diagram that need no new diagram. Answer them directly. If you are
  unsure whether the user wants a diagram or only an explanation, ask one question.

**In scope:** entities, weak entities, attributes (key, partial key, multivalued, derived,
composite), named relationships with cardinality and participation, relationship attributes,
recursive and ternary relationships, identifying relationships, specialization/generalization (EER:
disjoint/overlapping, total/partial, defining attribute, multi-level hierarchies), `Constraint:`/`Rule:`
notes, multi-page files for large models. **Out of scope:** multiple inheritance and union types
(categories) for now, everything physical (guide §1), running SQL or
connecting to databases, inventing rules, enums or limits, and normalization or performance audits
(mention them as follow-ups at most).

## 2. Inputs

| Input | Required? | Where to find it |
|---|---|---|
| **Model source**: one or more of: domain description / requirements; SQL DDL or migrations; ORM models; an existing `.drawio` / `.model.json` | **Yes** (at least one) | User message, attached files, or the repository (search for `*.sql`, `migrations/`, `schema.prisma`, `models.py`, `*.entity.ts`, `db/schema.rb`, `*Context.cs`, `@Entity` classes, `db-design/`) |
| Business rules (cardinalities, mandatory links, uniqueness, limits) | Recommended | User message, docs, schema constraints. Ask for the missing ones (§3) |
| Project name | Yes (for page titles) | Repository name, README title, or ask |
| Scope boundary (which bounded context / service / tables) | When the repository has several databases or more than ~30 tables | Ask |
| Subject areas (page split) | Only for 10+ entities | Propose a split from the folder or module structure, and confirm it in §3 |
| Target folder | Default `db-design/` at the repository root | Use another folder only if the user explicitly asks |
| Diagram language | English, unless the user picks another language (§3.1 N6) | Ask when the request or source is not in English |

**Discovery.** If the user gives no source, look in the repository first (read-only), then
report what you found: "I found 14 migrations in `db/migrations/` and Prisma models in
`prisma/schema.prisma`. Should I model from the Prisma schema?" Never model silently from a source
the user did not confirm when several candidates exist.

**Asking for missing inputs.** If no usable source exists, ask exactly this and wait:
> To draw the ERD I need a source. Please give me one of: (a) a short description of the business
> domain (the things you store and how they relate), (b) the SQL schema or migrations, (c) the ORM
> model files, or (d) the path to an existing diagram. Business rules ("every order has exactly one
> customer") are welcome too.

Unsupported or unreadable sources are covered in `references/edge-cases.md`.

## 3. The clarification gate

**Preconditions before drafting:** a confirmed source (§2), a project name, and a target folder.
In a repository with several data stores, the scope must also be agreed.

### 3.1 Detect ambiguity

Classify every open point while you analyse (Steps 2–4). Use `references/source-mapping.md` to see
what is *derived* and what needs a *question*.

**Blocking**: you cannot draw a correct diagram without the answer:
- B1. No usable source, or the scope is unclear (which service, which tables).
- B2. The **maximum** cardinality of a relationship is unknown in either direction (1 vs many).
- B3. Entity or attribute? (e.g. *Address*, *Category*, *Tag*, *Species*, *Type*, *Status*: do they have their own identity, properties or managed list of values?)
- B4. Strong or weak? (Can X exist or be identified without its owner?)
- B5. A relationship is implied but not stated, or its meaning or verb is unclear.
- B6. A relationship or an entity? (Can the same pair be associated several times, with history? Is the link referenced by other things?)
- B7. Roles of a recursive relationship, or ternary vs binary.
- B8. Conflicting statements: description vs schema, two documents, or user vs code.
- B9. Key choice: no stated or enforced unique identifier and it is unclear whether a conceptual
  identifier is acceptable; **or** several candidate keys (e.g. `Email` and `Username` both unique)
  and the user has not named the identifier. Ask which one identifies the entity. The other unique
  attributes become `Constraint: <Attribute> is unique.` notes.
- B10. Single- or multi-valued? It is unknown whether an attribute can hold several values (a
  maximum, i.e. a business rule).
- B11. Specialization or type attribute? Subtypes exist (*kinds of*, `type` column, ORM inheritance),
  but it is unclear whether they have their own attributes or relationships. Own properties →
  specialization; none → a `Type` attribute plus a `Rule:` note.

**Non-blocking**: there is a safe, least-restrictive default:
- N1. Minimum participation not stated → **partial** (single line). A `(default)` is **never** `total`, however obvious.
- N2. Unsure whether an attribute is derived (stored vs calculated) or composite (split into parts) →
  **simple**. These choices change the representation only, not a rule. Single vs multi-valued is B10.
- N3. Entity has no natural key → conceptual identifier `<Entity> ID` (team convention).
- N4. Technical columns (`created_at`, `version` …) → omitted, and listed in the model's `omitted`
  field, which the summary prints.
- N5. Page split, naming and verb wording → your proposal.
- N6. Diagram language: the request or source is not in English → ask which language to use for
  names and notes (*default: English*). Draft the names in the language you propose. The model's
  `language` field records the answer.
- N7. Disjointness or completeness of a specialization not stated → **overlapping (`o`)** and
  **partial** (single superclass line). A `(default)` is **never** `d` or `total`.

### 3.2 Ask: one batched round, then wait

1. Send **one message** with the draft model and the numbered questions. Show the draft first,
   **in full notation**, so the user can see every rule they are confirming:
   - entities, with strong/weak (and owner), the key or partial key, and the attribute kinds
     (multivalued, derived, composite);
   - every relationship with **both** ends: `Team (1) —Owns— (N, total) Project`. Mark each end's
     participation as `total` or `partial`. Mark every value that is a default rather than a stated or
     schema fact with `(default)`;
   - every specialization with its constraints: `Person ⇒ {Student, Employee} (o (default), partial
     (default), defined by Person type)`, and the subclasses listed without keys;
   - the notes (`Constraint:` / `Rule:`) you intend to draw.
   Only what the draft shows explicitly can later be recorded as `confirmed_by: "user"`.
2. Put **blocking questions first**, then non-blocking ones, each tagged `(blocking)` or
   `(non-blocking)`. Ask one question per number; do not mix a blocking and a non-blocking point
   in one question. Ask at most **10 questions per round**. Non-blocking questions state their
   default: *"(default: partial, single line)"*. Blocking questions may state your *recommended*
   answer, but it is never applied without an answer.
3. **Self-check the draft before sending it.** Any `total (default)` must become `partial (default)`,
   and any `d (default)` must become `o (default)`.
   Every unstated maximum must be `?` with a blocking question. Every *species/type/category/status*-like
   value needs a B3 question. If the request is not in English, the N6 language question must be there.
4. End with "Please answer, or confirm the draft as is." (in the user's language). Then **stop and
   wait. Write no files.**
5. When the answers arrive, update the model. If they raise *new* blocking points, run another round.
   After 3 rounds, stop asking about non-blocking points. Blocking points always need an answer.
6. When there are no questions at all (for example a fully constrained schema), still show the draft
   and ask for confirmation once. The user must see what will be drawn before it is written.

### 3.3 What counts as confirmed

- `stated`: the user's description or requirements say it explicitly.
- `user`: the user answered it during clarification, or confirmed the draft in which it was shown
  explicitly. "Looks good" confirms only what the draft displayed, including `(default)` values.
- `schema`: the existing schema or code enforces it (NOT NULL FK → total participation on that side;
  UNIQUE → key or 1:1; CHECK/enum → constraint note). Parent-side participation is **never** schema-confirmed.
- `convention`: a modeling decision the team guide prescribes (e.g. N3). It is never a business rule.

Everything else goes into `open_questions` and is drawn in its **least restrictive** form: partial
participation, the "many" side when the maximum is unknown, multivalued when single vs multi-valued
is unknown, overlapping and partial specializations, and no note. A default the user never saw must be listed in `open_questions`.

### 3.4 When the user cannot or will not answer

The hard limits: a **non-interactive run** writes no file (it outputs the draft and the questions);
**"don't ask, just generate"** never generates while blocking points remain; and B1, B3, B4, B5,
B6, B8 and B11 can never be delegated. For the full procedure and the fixed defaults of delegated
decisions, read `references/edge-cases.md` §1.

## 4. Workflow (follow in order)

**Step 1. Locate and confirm the source.** Follow §2. Note the project name. Check whether
`db-design/` already contains `*.model.json` or `*.drawio` files. If it does, this is an **update**:
load the latest `.model.json` (highest `-vN`) as the starting model.

**Step 2. Extract entities.** Use `references/source-mapping.md`. For each entity, record its name
(singular, Title Case), whether it is strong or weak, and its owner if weak. Drop implementation
artifacts: junction tables become relationships, value tables become multivalued attributes,
audit/technical tables are omitted. Subtypes become a specialization (superclass + subclasses) when they
have their own attributes or relationships (B11 if unclear).

**Step 3. Extract attributes.** For each entity, pick **exactly one** key (a natural key if one
exists, otherwise `<Entity> ID`) or, for a weak entity, one partial key. A subclass gets **no** key: it
inherits its superclass's key, and keeps only its own attributes. Then classify the other
attributes: simple, multivalued, derived or composite. Remove FK columns, surrogate ids that a natural
key replaces, data types and technical columns (record the omissions in `omitted`). Name attributes in Sentence case.

**Step 4. Extract relationships, cardinalities and participation.** Every FK and every stated
association becomes a named relationship (a verb). For each end, record `card` (1/N/M, the number of
*that* entity associated with one instance at the other end) and `total` (only if confirmed). Put
relationship attributes on the relationship. Add a `Constraint:`/`Rule:` note for each confirmed rule
that Chen cannot draw. Check that every entity is reachable through relationships. An isolated entity
is a question (B5), not a silent outcome.

**Step 5. Clarification gate.** Follow §3. **Stop and wait for the answers.** Then apply them and
fill `assumptions` (each with `confirmed_by`) and `open_questions`.

**Step 6. Write the model JSON.** Follow `references/model-schema.md`:
- Set `language` to the N6 answer (omit it for English).
- With 10 or more entities, define 2+ `areas`. This produces Overview + detail pages.
- Give every entity a `layout` position, following the layout heuristics in the schema reference.
- Save the model in a temporary location outside the repository if possible. Otherwise save it as
  `db-design/.erd-model-draft.json` and delete it after Step 8.
- Check it: `python3 <skill>/scripts/render_erd.py <model.json> --check`. Fix every reported problem.

**Step 7a. Render** (the normal path):
```
python3 <skill>/scripts/render_erd.py <model.json> --out-dir db-design [--name conceptual-erd]
```
The renderer creates `db-design/` if needed and picks the next free version name
(`conceptual-erd.drawio`, then `conceptual-erd-v2.drawio`, and so on). It never overwrites a file. It
writes the files of §5.1 with the same base name. Add `--drawio-svg` only if the user asks for an
editable SVG; use `--no-svg` only if the user does not want previews.

**Step 7b. No python3 available.** Follow `references/manual-fallback.md`, and say in the summary
that the file was hand-written and validated manually.

**Step 8. Validate.**
```
python3 <skill>/scripts/validate_erd.py db-design/<file>.drawio
```
- `ERROR` lines must be fixed. Fix the **model** (or its `layout`) and render again. Do not patch the XML.
  Rendering again creates the next version. Delete the failed version's files you just created in
  this run (only those, previews included), so that the folder keeps one result per run.
- `WARNING` lines: fix them, or justify each one in the summary.
- Layout errors (overlaps or lines through shapes): adjust `layout` positions or `spacing` and render
  again, at most 5 times. If errors remain, keep the best version and report them.
- Use `--allow-isolated "<Entity>"` only for entities the user confirmed have no relationships.

**Step 9. Review semantics.** The scripts check form, not meaning. Go through the §7 checklist
against the source.

**Step 10. Report.** Send the chat summary (§5.3). Point to the `.summary.md`. Do not commit unless
the user asks to.

## 5. Outputs

### 5.1 Files (all in `db-design/` at the repository root, unless the user named another folder)

| File | Content |
|---|---|
| `conceptual-erd.drawio` | **The deliverable.** Uncompressed diagrams.net XML (`<mxfile>`), opens with *File → Open from → Device* at https://app.diagrams.net/ or in the desktop/VS Code app |
| `conceptual-erd.summary.md` | Human-readable summary: entities, keys, attributes, relationships with ratio and participation, notes, confirmed assumptions with their source, open questions |
| `conceptual-erd.model.json` | The normalized model, used for regenerating and updating the diagram in later runs |
| `conceptual-erd.svg` | Preview image, shown inline by GitHub/GitLab and in Markdown. Multi-page files get one per page: `conceptual-erd.p1.svg` (Overview), `.p2.svg` … Generated: never edit it; after a manual edit of the `.drawio`, run `python3 <skill>/scripts/export_svg.py <file>.drawio` |
| `conceptual-erd.drawio.svg` | Only with `--drawio-svg`: the first page as an image that diagrams.net can also open and edit. Not diffable; the `.drawio` stays the source |

### 5.2 Naming and versioning

- Lowercase and hyphenated, stating the model level: `conceptual-erd`. A repository with several
  bounded contexts uses one file per context: `--name conceptual-erd-billing`.
- Never overwrite. A rework creates the next version (`conceptual-erd-v2.drawio`, `-v3` …), and the
  previous versions stay for comparison.
- Page names: single page `1 - Conceptual ERD`. Multi-page `1 - Overview`, `2 - <Area>`, ….
- Each page has a title `<Project> — Conceptual ERD` (plus the page name) and a notation legend.
  With `"language": "es"` the renderer translates these texts (`1 - ERD conceptual`, `1 - Vista general`).

### 5.3 Chat summary (always; keep it short)

```
ERD saved: db-design/conceptual-erd.drawio  (pages: 1 - Conceptual ERD)
Validation: PASS (0 errors, 0 warnings)
Entities (4): Team, User, Project, Task (weak, owned by Project)
Relationships (5):
- User (M) —Member of— (N) Team [Team role]; every team has a member
- Team (1) —Owns— (N) Project; every project has a team
- …
Confirmed assumptions: 13 (see summary file), e.g. "A task has at most one assignee (user)"
Open questions (drawn least-restrictive): Must every team own at least one project?
Also written: conceptual-erd.summary.md, conceptual-erd.model.json, conceptual-erd.svg (preview)
```
List every open question in the chat. Never bury them in the file only.

## 6. Notation essentials

The full rules are in `references/erd-guide.md` §1–§3. The renderer applies the styles, so these
are the points that need your judgement:

- **Cardinality label placement:** the label next to entity X says how many X relate to **one**
  instance at the other end. `Customer (1) —Places— (N) Order` means that a customer places N orders
  and each order has 1 customer. Binary ratios are only 1:1, 1:N or M:N. For a **ternary**
  relationship, the label next to X says how many X relate to one fixed *combination* of
  instances of the other two entities.
- **Keys:** exactly one key per strong entity. A natural composite key (e.g. `Flight number` +
  `Departure date`) is **one underlined composite key** attribute (`"kind": "key"` with `"parts"`).
  Other candidate keys become `Constraint: … is unique.` notes. Limits on attribute values ("one or
  more phone numbers", "at most 5 images") become `Constraint:` notes too. A weak entity has exactly
  one partial key, an identifying relationship (double diamond) and total participation (double line).
- **Never draw:** data types, FK columns as attributes (`Customer ID` inside `Order`), junction
  tables as entities (unless they have their own identity or history), indexes, SQL, arrowheads.
- **Naming:** names are in English unless the user chose another language (N6). Entities are
  singular Title Case nouns. Attributes are in Sentence case, and English booleans start with
  `Is`/`Has`/`Must`. Relationships are verb phrases. Notes start with `Constraint:` or `Rule:`, or the
  chosen language's prefixes (Spanish `Restricción:` / `Regla:`).
- **Specialization (EER):** a purple circle between the superclass and its subclasses, `d` (disjoint)
  or `o` (overlapping); a double superclass line = total. Subclasses inherit the key and attributes, so
  they have no key, are never weak, and have exactly one superclass. Use it only when subtypes have
  their own attributes or relationships (guide §2.10). Never model subtypes as 1:1 `Is a` relationships.
- **Multi-page:** the Overview shows every entity, relationship and specialization, without attributes,
  and repeats every note. Each entity has exactly one home page with all its attributes. Elsewhere it is a
  reference entity without attributes. Every relationship appears on at least one detail page.

## 7. Quality checklist

`validate_erd.py` must report `PASS`. It checks the file structure, the style catalog, the
notation (names, cardinalities, roles, keys, identifying relationships), physical leaks,
reachability, multi-page consistency, title and legend, and layout. It does not open the file in
diagrams.net, and it cannot judge meaning. Check these yourself, against the source, every time:

- [ ] Every entity, relationship and rule in the source appears, including attribute limits (as
      notes). Nothing unconfirmed was added.
- [ ] Total participation appears only where `stated`, `user` or `schema` confirms it.
- [ ] Relationship verbs read correctly in both directions, and the labels are on the right side.
- [ ] Weak entities really depend on their owner, and M:N relationships really have no history or identity.
- [ ] Every subclass really has its own attributes or relationships; `d` and total specializations are confirmed.
- [ ] `open_questions` lists everything unresolved, and the chat summary repeats it.
- [ ] Previous versions in `db-design/` are untouched.

## 8. Common problems

- **Renderer reports model errors:** they are notation violations. Fix the model and run `--check`
  again. Never bypass them.
- **Conflicting sources or rules** (migrations vs ORM, user vs schema): never pick one silently.
  Quote both and ask (B8).
- **Entity with no relationships:** ask (B5). Only after the user confirms it is standalone,
  validate with `--allow-isolated "<Name>"` and mention it in the summary.
- **Target file already exists:** the renderer picks the next `-vN`. Use `--out <path> --force` only
  when the user explicitly asks to replace that file.

Everything else (vague or unsupported sources, compressed `.drawio`, NoSQL, inheritance, huge
schemas, unwritable folders, requests for other formats or physical details) is in
`references/edge-cases.md`.

## 9. Worked example and maintenance

- `examples/task-tracker/input.md` is a full run: the request, the analysis, the 7-question
  clarification round, the answers, the outputs and the acceptance criteria. Read it if you are
  unsure how a draft or a round of questions should look.
- `python3 tests/test_skill.py` renders the example and validates it, and covers every rule the
  scripts enforce.
- To change the skill (styles, notations, EER features, languages, export formats, versioning),
  read `references/maintenance.md`.
