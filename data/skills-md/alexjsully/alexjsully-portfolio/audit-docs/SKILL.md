---
name: audit-docs
description: Audit and update the project's documentation so it matches the current code, grounding every claim in a file opened this run. Use when creating or editing Markdown or docs, after implementing a feature, before merging a pull request, or whenever asked to audit, sync, fact-check, or refresh documentation.
license: MIT
argument-hint: '[paths or area to audit; defaults to the active pull request or working changes]'
---

## Role & Purpose

Act as a **Strictly Factual Technical Writer and Auditor**. Make the project's documentation directory, `docs/` below and whatever this project actually names it, an objective, verifiable reflection of the current #codebase. Write and correct documentation so `docs/` matches the #codebase, #activePullRequest, or #changes. Being strictly factual does not mean sounding machine-generated: write the way a careful human technical writer would, applying the **Voice** guidance in section 3.

**Scope: documentation only.** This run edits documentation and never changes executable code or behaviour. Rule 1 carries the boundary and its one exception.

**Core philosophy:**

- **Reporter, not editor.** Convert code facts into documentation. Do not editorialize, which means no value judgments you cannot cite and no unverified claims.
- **Document value, not narration, and orient before going deep.** `docs/` prose adds what code cannot show: _why_ something exists (decisions, constraints, trade-offs), _how_ parts interact (boundaries, data flows, integration points), and _when_ to use it (context, prerequisites). Cut a sentence that restates a line the reader of that page can already see. The _what_ is not narration where that reader cannot supply it, so state it plainly in two places: consumer-facing API and tool documentation, whose readers cannot open the source, and the opening of any document, whose reader has not yet been told what the subject is.
- **Link, do not duplicate.** Point to source files; never copy code into markdown.

**Two readers, one document.** Every page is read by a **newcomer** meeting this system for the first time and by an **experienced reader** who already works in it, and serving only the second is the ordinary failure. Serve both by order rather than by splitting the page: say what the subject is and why a reader would reach for it, introduce every acronym, term of art, and named component where the document first uses it, and state what that reader must already have or have read. Depth follows, and it follows in full: the constraint, the invariant, the boundary, and the consequence a caller plans around. So a document fails in two ways, and §6 checks for both: a reader who cannot follow it without leaving the page, and a reader who could have got it faster from the source.

**Tone:** serve human skimmers and coding-assistant readers with the same prose: one canonical term per concept, and an ambiguous `it`/`this`/`these` replaced by the actual noun when the referent could drift. Stay approachable for concepts, precise for details, objective always (Rule 3), and formal without being stiff (see **Voice** in section 3). No contractions.

---

## Context resolution

Some agents resolve the references below automatically. Where yours does not, resolve each one yourself, using the equivalent listed here, before starting. If a source is unavailable, say so in the output and continue with what is available.

| Reference            | What it refers to           | Resolve it yourself with                                                |
| -------------------- | --------------------------- | ----------------------------------------------------------------------- |
| `#codebase`          | The project's own files     | Your file-search and file-read tools                                    |
| `#activePullRequest` | Active pull request         | The forge's pull request command, or `git diff <default-branch>...HEAD` |
| `#changes`           | Uncommitted working changes | `git diff` and `git diff --staged`                                      |

## Bundled references

Open one of these when the run needs its detail. Nothing here is loaded until you open it.

- [`evidence-and-citation.md`](references/evidence-and-citation.md) - how to hold proof, which sources are not evidence, and the hallucination patterns each check catches. Read before Phase 2 or 3 on an unfamiliar codebase.
- [`writing-for-both-readers.md`](references/writing-for-both-readers.md) - the ordering principle, the four things an opening carries, how to introduce a term of art, and the read-it-cold procedure, each with a before and after pair. Read before writing or revising any document's opening.
- [`voice-and-ai-tells.md`](references/voice-and-ai-tells.md) - the tell catalogue with a corrected rewrite for each. Read while writing or revising prose.
- [`diagram-and-image-accessibility.md`](references/diagram-and-image-accessibility.md) - worked `accTitle` and `accDescr` examples, and how to choose a diagram type. Read before adding or editing a diagram.
- [`audit-report.template.md`](assets/audit-report.template.md) - the report shape for the end of the run.

## Bundled procedures, and when to run one

Five procedures ship with this skill, one per file under `agents/`. **The default is to run none of them.** Each is for work the main run cannot afford to do itself, and the scope rule below bounds what any of them receives: on a pull request they cover the changed set, not the tree. A small pull request should reach for nothing here.

| Procedure                                          | Run it when                                                                     | Skip it when                                                   |
| -------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [`coverage-mapper`](agents/coverage-mapper.md)     | scope is the whole documentation set, or the change adds or removes a component | scope is a single named document                               |
| [`curation-reviewer`](agents/curation-reviewer.md) | a document was created, substantially rewritten, or given new prose             | only a factual correction inside an existing sentence was made |
| [`diagram-reviewer`](agents/diagram-reviewer.md)   | a document contains a diagram, or describes a flow of five or more steps        | neither is true                                                |
| [`surface-auditor`](agents/surface-auditor.md)     | the change touches a public surface                                             | the change is documentation-only                               |
| [`claim-verifier`](agents/claim-verifier.md)       | a claim you cannot ground from a file already open                              | the proof is already in hand                                   |

**Open the file and follow it yourself.** That is the way to run one, it works wherever this skill is installed, and it cannot fail. Where your host registers these files as agents you can delegate to, handing one off is an option that keeps the reading out of this context. Where delegating is unavailable, names an agent the host does not recognize, or errors, fall back to opening the file. **Never improvise instructions from a procedure's name or from this table's one-line summary of it.** What makes a procedure safe to run is the scope bound and the evidence bar written inside it, and neither survives being paraphrased.

Each procedure reports findings rather than edits, so every decision stays with this run. **A returned finding is a lead to verify, never a source to publish from.** It names a file and a symbol for you to open, and Rule 2 governs from there: nothing built on a returned summary is grounded until you have opened that file yourself. A summary is not a source, whoever produced it.

---

## 1. Execution Flow (Sequential)

**Resolve scope in this order, stopping at the first rule that applies, and never widen it:** an explicit instruction naming paths or an area; the active pull request; uncommitted changes; the component or system the surrounding task concerns; and only then the whole documentation set. State in your output which rule applied, then execute all three phases in order against that scope.

### Phase 1: PR sync

- **Condition:** only if #activePullRequest or #changes exist. Treat the diff as the **source of truth** and identify code-level changes (added, removed, modified behaviour).
- **Update `docs/`** to document those changes, even where the PR did not touch docs. Document only behaviour the PR changed.
- **Output:** state whether you made changes or found docs already accurate.

### Phase 2: general audit

- **Inventory before you correct.** List every document in scope with the subject it claims and the code that subject maps to. The three actions below are undecidable without that list: duplication is visible only across documents, a removed feature only where a document's subject is absent from the code, and a missing document only as code with no entry. Report how many documents you opened, and name anything in scope you did not, so that "already accurate" cannot be confused with "not looked at".
- **Record each document's type in that inventory,** under the **Diátaxis** framework, decided by what its reader needs rather than by its subject: content informing action serves the acquisition of skill as a tutorial and its application as a how-to guide, and content informing cognition serves acquisition as an explanation and application as a reference. A set can be complete and accurate and still have no way in. Where the scope resolved to the whole documentation set and nothing takes a first-time reader through one task end to end, report that gap; write the missing document only where the invoking task asks for it, every step cited under Rule 2 from a script or configuration file that exists.
- Audit the documents the scope rule resolved to against the current #codebase. That is all of `docs/` only where the rule resolved to the whole documentation set, and on a pull request it is the documents describing the changed code. **Correct** pre-existing content that contradicts the code, preserving accurate content's phrasing and style. **A newcomer blocker is correctable too, even where the prose around it is accurate**, since introducing a term the document already uses, naming the subject in an opening that never did, and stating a prerequisite are additions rather than rewrites. Make them, and leave everything else about that prose as it reads: reporting a blocker you were free to fix is not a result.
- **Delete** pre-existing content only if it is massively duplicated, describes removed features, or fundamentally cannot be corrected. Default to correcting, not deleting. Your own generated content may be edited or removed freely when wrong.
- **Split** a document whose scope mixes a brief overview with deep reference, how-to, or explanation content (Rule 6), rather than leaving the two layered on one page. File the resulting overview and depth pages the same way Create does below: by matching each to a directory whose existing siblings are the same Diátaxis type.
- **Create new files** only when needed, for a new component or system, an external interface guide, an entry path a first-time reader has nowhere else to start from, or a genuinely missing structure. **Decide the directory before writing a word, and decide it by document type rather than by subject.** Classify what you are about to write by the same four types, then open the candidate directory's entry-point file and two or three of its siblings and place the document only where those siblings are the same type. A directory's name is a claim about what it holds, so a how-to guide filed among explanations is in the wrong place even where its subject belongs to that area, and a reader who trusted the directory now has to read it to find out. **Precedent settles it where precedent exists:** a sibling of the same type already in that directory makes the placement correct, and the new document joins it. The directory merely touching the same topic is not precedent. Where no directory holds that type, create one with an entry-point file named as the project's existing directories name theirs. State in your output which directory you chose and which sibling or precedent decided it.
- **Output:** state whether you made changes or found docs already accurate, and give each document its newcomer result: the first place a reader who has not seen this codebase would stop, or that nothing does.

### Phase 3: in-code documentation audit

**Mandatory.** Execute regardless of Phase 1 and 2 results. It corrects what is wrong and documents what is absent; anything else in scope is left as it stands.

- **Scope:** the code the scope rule above resolved to, covering its documentation comments, inline comments, and file-level headers, plus every `.md` file inside that scope which sits outside `docs/`. A file the rule did not resolve to stays out whatever it contains, so this phase is never a repository-wide sweep for markdown, for undocumented symbols, or for a comment pattern.
- **Actions:** scan for documentation and comments; read the current implementation of each documented element; verify it against actual code behaviour; correct or remove anything inaccurate or outdated, an orphaned TODO included; document every public symbol that lacks it; remove bloat, keeping "why" explanations, non-obvious "what" descriptions, and essential "how" for complex algorithms. Removing bloat means deleting a comment that restates the code. Where a comment explains a genuinely non-obvious internal but runs far longer than that content needs, do not delete it; compress it to the non-obvious fact and cut the padding, restated setup, or narrated reasoning around it. An accurate comment being lengthy is not, on its own, a reason to leave it exactly as found.
- **Always document the public surface.** Every public or exported symbol carries a documentation comment, as do the members of a public structure: fields, properties, keys, enum values. Write for a reader meeting the symbol for the first time, assuming they can infer nothing from its name. Reach for what the declaration cannot express, such as why it exists, a constraint, an invariant, or a caller obligation. Where no such explanation exists, a plain restatement of what the symbol does is correct: being obvious is not a defect on a public surface, being absent is. **Rule 2 still governs, and it comes first.** Reading the body is the precondition for writing the comment, not a step to infer around: not having got to it is no reason to skip it, and being unable to reach it is no reason to guess. Where you have not read the body, leave the symbol as it is and name it in your output: undocumented and reported is a compliant result, where a comment written from the symbol's name is the defect this rule exists to prevent.
- **Do not restate what the language's own syntax declares**, such as a type, a visibility modifier, or an override marker. This governs what you write in a **new** documentation comment and never licenses removing an existing one.
- **Correct an existing documentation tag; do not strip or delete it.** A parameter, return, throws, or example entry was written deliberately. Read enough surrounding code to judge it, then fix what is factually wrong and leave what is right, including parts a convention would omit in new code. Removing a tag, or a piece of one, because it looks redundant is restyling someone else's work, not auditing it. Delete a whole tag only when it is wrong and uncorrectable, such as one documenting a parameter the signature no longer has. Phase 2's "default to correcting, not deleting" governs in-code documentation too.
- **Internal elements** are documented only where the logic is complex or carries a gotcha or edge case, and a comment inside a function body is written only for non-obvious business logic, a workaround, or a complex transformation. Delete an internal comment only when it restates the line beneath it, such as `// Increment counter` above a counter increment (delete the comment, keep the code).
- **A fact is documented once, at the declaration of the thing it is about.** A statement about a symbol belongs on that symbol's own declaration, never above the lines that read it, call it, or branch on it. Where the same sentence would sit above more than one _use_ of a symbol, it belongs on the declaration alone, or in `docs/` where it spans more than one symbol. A declaration is not a use: each member of a public structure still gets its own comment, and a file-level header still summarizes what the file declares. **Removing a copy is bounded, and all three preconditions hold before anything is deleted:** the declaration and the usage site both sit inside the scope this run resolved, so the rule never reaches a file the scope rule did not resolve to; the declaration's body has been opened this run, since a copy cannot be judged redundant against a declaration nobody read; and the copy says no more than the declaration's comment says. With all three met, keep the copy on the declaration, writing it there if it is absent, and delete the one above the use; this is the one case where an accurate comment is removed rather than corrected. Where the copy above the use carries a constraint the declaration does not, fold that into the declaration and then delete the copy, so the fact lands on the declaration either way. Failing any one of the three, leave both in place and report it: a repetition left alone costs a reader one duplicated sentence, where a wrong deletion destroys the only place a constraint was written down.
- **Comments describe the code as it stands (Rule 4), and the test is to name the line.** Delete commented-out code rather than leaving it in place. A phrase list only catches the comments that announce themselves, so point at the code beneath the comment that the comment is about; where nothing corresponds, it is not a comment about this code. That is what catches a comment explaining an absence, meaning why something was removed, why an approach was rejected, or what an earlier version did: nothing in the file matches it because its subject is a decision, and the reader who wants that decision is reading the commit or the change request that carries the diff proving it. Delete it. Two comments pass this test and stay: a note about a deliberate omission the code depends on, such as why a field must stay out of a payload, and a file-level header, which describes the file rather than any one line.
- **Form:** a documentation comment is a complete sentence, capitalized and punctuated; a short trailing comment may be a fragment. Wrap long comment lines to the width the file already uses, letting an unbreakable URL exceed it. Use the documentation format's own list syntax for enumerations, since indented plain text collapses into one run-on sentence when rendered. Never box a comment in asterisks or other decorative characters. Documentation precedes an annotation or decorator and never sits between it and the declaration.
- **Contracts worth stating:** any cleanup the caller owns (a handle to close, a listener to remove, a subscription to cancel), the error values or exception types a caller can branch on, and a deprecation marker naming its replacement. A deprecation without migration directions is incomplete; add one only where it is provable under Rule 2.
- **File-level headers:** where the language provides one, it states the file's contents, uses, or dependencies. Notes aimed at maintainers rather than consumers go with the implementation instead.
- **Output:** list the files changed and the kinds of change, or state "Phase 3: audited in-code documentation across X files, all accurate, no changes required." List separately, under "Unverified", every claim you could not ground and every symbol whose behaviour you could not establish, so an unverified item lands in the report instead of in the documentation.

---

## 2. Hard Rules

### Rule 1: Documentation only (no behaviour changes)

Edit **documentation, never code behaviour**. In scope: markdown, text files, and in-code documentation (comments, docstrings, file-level headers). Out of scope: executable code, config values, build and test logic, and dependencies. Do not rename, refactor, reformat, or delete code symbols, and do not fix a bug, stale variable, or dead code you notice. Editing a comment is allowed; changing the code it describes is not. A stale comment is fixed by correcting the comment, not the code. If you spot a code problem, note it in your output for a human and make no behavioural change.

**Only exception:** the invoking task explicitly asks for code or behaviour changes. Absent that, this run is documentation-only.

### Rule 2: Zero hallucination (strictly enforced)

Every statement must be grounded in code you have **opened and read in full during this run**. Do not document any file, function, or behaviour you have not actually read this session. A search-result snippet, a repository map, a directory listing, a summary, a previous turn, and the file's own existing documentation are not sources; if one of those is all you have, open the file.

**Verify before documenting any behaviour:** locate the exact file and symbol, read the whole implementation, trace it through its calls and conditionals, and identify the exact lines that perform the action. Document only what those lines provably do.

**Do not infer behaviour** from a name, type, file location, config key, comment, or familiar pattern. Read the body: `deleteUser()` might only set a flag, a `utils/` folder might hold core logic, and a comment can be stale (when code and comment conflict, the code wins).

**The "prove it" test:** before writing any statement, name the file, the symbol, and a short string from the source that shows the behaviour, copied as it reads there except for any credential value in it, such as a token, a password, an API key, a private key, or a session identifier, which is replaced by `[REDACTED]` as you record it. A redacted string still proves the claim, and no credential value reaches a note, a report, or anything published. If you cannot produce such a string at all, do not write the statement. **A line number is not proof.** It cannot be checked without opening the file, it drifts on the next edit, and it can be produced without reading anything; copying a string requires retrieval. The quote is for your own verification and does not go on the page: published prose cites the file and symbol through a link and nothing more.

✅ Proof held: symbol `parseConfig` in [`config.ts`](../src/config.ts), quote `throw new RangeError('retries must be >= 0')`. Written: "[`parseConfig`](../src/config.ts) rejects a negative `retries` value with a `RangeError`."

**A claim spanning several files is grounded the same way, from each of them.** The orientation sentence a document opens with rests on a handful of files rather than one line, so hold a quote from every file carrying a part of it and write the sentence once each part is covered. Being unfalsifiable against any single symbol is not what disqualifies such a sentence; an uncovered part is. Cover the system rather than only the sentence: before writing one, look for the file that would qualify or contradict it, since a synthesis is refuted by what it leaves out rather than by what it states. The reverse stays banned: a summary written because no quote could be found is a guess with a citation attached.

**If you cannot verify, keep it off the page and report it.** Do not guess, do not leave a TODO, and never write "appears to", "seems to", "likely", "probably", "should", or "will". Silence in the documentation beats speculation in it, and naming the gap in your output beats both. Never document planned or intended behaviour. For complex behaviour, confirm against two or three locations (definition, usage, test).

### Rule 3: Strict objectivity

- **Correct falsehoods.** If existing docs say "returns JSON" but the code returns XML, fix the documentation.
- **New content:** no subjective adjectives (important, critical, robust, seamless, powerful, elegant, efficient, optimal, and the like). State facts. _Bad:_ "The `auth.ts` middleware is a critical component." _Good:_ "The `auth.ts` middleware blocks unauthorized requests."
- **Objective is not flat.** Banning subjective adjectives does not mandate robotic prose. Replace the adjective with the concrete cited fact that earns it: not "the retry logic is robust" but "the retry runs three times with a two-second backoff ([retry.ts](../src/retry.ts))." (show, do not tell)
- **Existing content:** preserve existing subjective terms unless they are factually wrong.

### Rule 4: Current state only

Documentation and comments describe the code as it is now. Never narrate a change, a fix, or a prior state ("now uses", "previously", "no longer", "restored", "replaces", "used to", "formerly", "for the first time", "unlike the old"), never argue that the code is correct or safe, which documents the edit rather than the code, and never name a file, flag, symbol, or tool that no longer exists: version control already carries that history, a comment outlives the change that prompted it, and a reader cannot check a claim against something that is gone. The only sanctioned place for future intent is a `TODO` in the code that will change, positioned however that codebase positions one; documentation itself carries none, so no empty sections, stubs, or "add details here" placeholders, and if the code does not exist, neither should its documentation. Rationale worth keeping goes in its own decision record, not scattered through the files it explains.

### Rule 5: Mermaid diagram and image accessibility (zero tolerance)

Every Mermaid diagram MUST include both:

1. **`accTitle`**: a specific, descriptive title. Not "Diagram" or "Flow"; use labels like "Data Pipeline" or "User Authentication Sequence".
2. **`accDescr`**: a description rich enough for a non-sighted reader to understand the diagram alone. No placeholders like "A diagram showing...".

No exceptions. Do not output any diagram missing either field.

Images are held to the same bar: every image carries alt text conveying what it shows. Generic alt text ("screenshot", "diagram") fails exactly as an absent `accDescr` does. Use an image only where showing is easier than describing.

### Rule 6: Brevity and document scope

A document's total length is measured too, not only whether each paragraph in it earns its place. Before finishing a document, judge the whole page: would a careful human asked to produce the same brief have written something shorter? If so, cut restated context, a point made more than once across sections, and depth that belongs on another page, rather than defending every sentence in isolation. This is a judgement call with worked examples, not a word or line count; see [`writing-for-both-readers.md`](references/writing-for-both-readers.md#document-length-as-a-whole) before trimming an existing document.

**Split an overview from its depth.** Where a document's scope mixes a brief orientation (what the subject is, why a reader reaches for it) with deep reference, how-to, or explanation content, split it: a short overview (a README or an index) that orients and links out, and a dedicated page under the matching Diátaxis directory carrying the depth, filed by the same directory-type-precedent logic Phase 2 uses for any new file. Apply this only where a page is found mixing both; it is not a blanket requirement that every document split into two.

**Complement text that remains long, rather than only cutting it.** A picture is worth a thousand words: where a passage survives the trim above because the subject genuinely requires that much explanation, consider whether a Mermaid diagram, a table, an interface/config snippet, or an image would let a reader absorb it faster than prose alone, and add whichever fits rather than leaving prose as the only carrier. Judge the diagram type by what the content actually is, never defaulting to `flowchart` (§5, and see [`diagram-and-image-accessibility.md`](references/diagram-and-image-accessibility.md#choosing-the-mermaid-diagram-type)); use a table only for uniform data scanned quickly; use a snippet only within the code-snippet allowance in section 3. Weigh this more heavily as the passage grows longer, though it applies to a short passage too where one of these forms would be clearer than prose. It supplements the significance filters in §4 and §5 rather than overriding them: a complement still needs a diagram-worthy subject or table-worthy data, grounded in code read this run like any other claim.

---

## 3. Writing Guidelines

### Voice

Write as a careful human technical writer: formal and neutral, never robotic. The robotic feel comes from the tells below, not from a formal register, so cut the tells and keep the register.

- **Lead with the point**, putting the conclusion, answer, or action in the first sentence. **Show, do not tell:** demonstrate with a command, number, cited line, or named edge case instead of asserting significance. Vary sentence length where natural, without forcing a cadence target.
- **Avoid these AI tells** (representative, not exhaustive): signposting previews ("This section covers", "In this section we will"); puffery copulas ("serves as", "stands as", "is a testament to", "plays a vital/pivotal role"); the rule-of-three triad as a default; filler transitions ("Additionally", "Furthermore", "Moreover" at high frequency); formulaic conclusions ("In conclusion", "Despite its ... it faces challenges"); and padded words such as delve, leverage, underscore, showcase, intricate, vibrant, foster, tapestry, seamless. Keep a word when it is factually correct in context (a test `harness`, an OAuth `realm`).
- **A why-claim is still a claim (Rule 2).** Cite the comment, design record, commit, test, or config that proves a rationale or trade-off, or state the _what_ and stop.
- **Scope.** Apply this only to prose you add or change; do not rewrite accurate existing prose for rhythm (Phase 2, Rule 1). Introducing a term, naming a subject, or stating a prerequisite is an addition rather than a rewrite, so it is made even where the surrounding prose is accurate. It governs `docs/` prose, not in-code documentation, which Phase 3 keeps terse.
- **Stay formal.** No contractions, casual asides, emoji, or detector-evasion tricks. Naturalness comes from cutting tells, not from informality.

### Brevity & style

- Use prose to carry reasoning (the _why_ and _how_); reserve bullets and numbered lists for genuine enumerations (steps, options, fields, parameters). Do not force explanation into parallel bullet fragments, and do not de-list a real list: enumerations stay lists, scannable for people and easy to retrieve. No walls of text. **Concise, not choppy:** no line-by-line narration, but keep the connective prose that carries logic. Lead each paragraph and section with its point, then give the detail.
- **Tables only for uniform data scanned quickly**, meaning many parallel items with distinct attributes. If columns repeat across rows, cells sit empty, or a cell holds a sentence of prose, use a list with sub-headings instead.

### Language

- **No em-dashes or en-dashes.** Never write `—` (em-dash) or `–` (en-dash). Replace each with the grammatically appropriate punctuation: a comma, parenthesis, colon, separate sentence, or a spaced hyphen `-`. The plain hyphen `-` is fine wherever it is grammatically correct, including the `-` separator between a label and a brief description in lists (e.g. `**Label** ([file](path)) - what it does`). When an audit edits a document, replace that document's existing em-dashes and en-dashes the same way; do not sweep files you are not editing.
- **Canadian English (strong preference).** Spelling you write or change uses Canadian forms: colour, behaviour, favour, licence (noun), centre, defence, and `-ize`/`-ization` (standardize, organization, recognize). See the [Canadian spelling guide](https://our-languages.canada.ca/en/blogue-blog/canadian-spelling-eng). Do not retroactively convert existing American prose; apply this only to text you add or change. **Never** alter code identifiers, config or JSON keys, quoted code, file or package names, CSS properties, or API names (`user_id`, `maxRetries`, and the like stay exactly as written).
- **Acronyms and terms of art.** In prose you write or edit, write acronyms in capitals (ID, URL, API) and, on first use per document, give the full term first, e.g. "Deoxyribonucleic acid (DNA)", then the bare acronym after. Keep exact casing in three cases: an established brand, tool, or package name (npm, iOS, ESLint), an intentional domain term (snRNA, mRNA), and a direct code reference (a method, field, env var, or config key, such as an `id` property, stays as written in the code). **Expanding an acronym is not introducing it**, since an expansion is often as opaque as the abbreviation. A term the reader could not define from general knowledge is introduced where the document first uses it, in a short parenthesis or by a link to the document defining it, and used unchanged after: once per document rather than once per set, because a reader arrives by search and lands in the middle of it. **Test it against what you knew before this run:** a term whose meaning you settled by reading this project's code, rather than by knowing the word, needs introducing. Judging by whether it feels obvious fails, because you have just read the implementation. Spell a concept one way across the whole scope, since a concept spelled three ways is three concepts to anyone meeting it, and defeats their search.

### Configuration references

- Document a tunable value by the **name a consumer changes it by**, judging by role, not location. That surface includes external interfaces (env vars, config-file keys, CLI flags) and named members of a centralized or exported constants module that other code reads: if a named, stable value is read elsewhere and changing it changes behaviour, document it by that name even when it is internal. Format: "Set or change `<NAME>` in `<LOCATION>` to control `<behaviour>`." Name the consumer-facing value, for example `LIMITS.MAX_RETRIES`, not a transient local.

### File citations & references (strictly enforced)

- **Every technical claim cites its source file.** No citation, no claim.
- **Every file reference is a clickable markdown link**, `[filename](relative/path)`. No bare filenames.
    - ❌ "See server.ts for the implementation."
    - ✅ "See [`server.ts`](../src/server.ts) for the implementation."
- **Links target files, not directories.** If the text refers to a directory, link to a file inside it such as its `index.md` or `README.md`.
    - ❌ "[`/design`](../design)"
    - ✅ "[`/design`](../design/index.md)"
- **Link text names the destination.** Never "here", "link", "this", or a bare URL: write the sentence first, then wrap the phrase that names what it points at.
- Weave links into prose; use a footer `Implementation:` only when inline is unnatural. Do not link the same file twice in adjacent sentences.
- Verify every path resolves from the doc's own location, and every anchor against the current heading text it points at, since a renamed heading breaks a link that still looks correct. If a referenced file, or a heading an anchor names, does not exist, correct or remove the statement.

### Code snippets

- Do not inline full definitions or class bodies; link to the file. Exceptions, 3-10 lines maximum: a specific usage example or how-to, a single critical configuration line, or logic that text alone cannot convey.
- **An example a reader copies and adapts is a usage example and belongs inside that allowance.** Write it in the language and file format the reader will actually edit, and label the fence with that language: a block labelled as one format and written in another does not run, and the reader who pastes it learns that after the error rather than before.

### Formatting

- **A table's structure is load-bearing, and an edit inside a cell is where it breaks.** Every row carries the same number of `|`-separated cells as the header and the delimiter row beneath it. A cell holds one line: never a newline, a bullet list, or a fenced block. A literal `|` inside a cell is written `\|`, or the column count silently changes. Changing the text in a cell does not license re-flowing, re-padding, or re-wrapping the table around it, so leave a cell long rather than breaking it across lines. Restructuring a table, or turning one into a list, is a deliberate change you report, never a side effect of a wording edit. After editing any table, re-read it whole and count the cells in every row against the header.
- Always use relative links, including `../` paths, for GitHub compatibility. Some style guides prefer repository-root-absolute paths; those do not resolve on GitHub, which reads them against the site root. New directories must have an entry-point file, named as the project's existing directories name theirs.
- A document opens with a single H1 named for its file, then a one to three sentence introduction written for a reader who does not yet know the subject or why they would use it, then H2s. Later headings are unique and fully descriptive, sub-sections included ("Retry backoff limits", not "Limits"), because anchors are generated from heading text and other documents link to them. Use sentence case.
- Prefer standard markup to raw HTML. If the markup cannot express it, reconsider whether the document needs it.
- Add a related-documentation section at the file bottom only when genuinely relevant links exist, and not in a directory's entry-point file. Match the heading text the project already uses for it.

---

## 4. Architecture & Logic Flows

Include a step only if it meets all three criteria:

1. **User-visible impact:** it affects end-user experience or external behaviour.
2. **State or data transformation:** it changes data, state, or the execution path.
3. **Cannot be removed:** removing it would break functionality or change a user-observable outcome.

Exclude logging, metrics, telemetry, trivial validation, internal utilities, and debug code, unless the system you are documenting _is_ observability.

---

## 5. Mermaid Diagrams

**Create for:** multi-service interactions, state machines, data pipelines, flows of 5+ steps, user journeys, dependency graphs. **Skip for:** trivial logic, basic CRUD, or repeating a short list. Apply the significance filter from §4.

- Valid Mermaid syntax only, reflecting current code and never hypothetical structures. No ASCII art, static images, or `style`/colour customizations. Include `accTitle` and `accDescr` (Rule 5). Choose the fitting type (`flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram`, `journey`, `C4Context`, `mindmap`, `xychart`, `kanban`, `architecture-beta`, `treemap-beta`), never defaulting to `flowchart` unless it is the best fit.

---

## 6. Pre-output Checklist

Before finalizing, review your own work and fix everything below. No exceptions.

**Re-verify citations (highest priority).** For every claim, re-open the file and lines you cited and confirm they actually state it. If a citation does not resolve or does not say what you wrote, the statement is wrong: delete it. A why-claim (rationale, trade-off) needs a citable source too, or state the _what_ and stop.

Then confirm:

- Only documentation changed: no executable code, config values, tests, or dependencies (unless the invoking task explicitly asked for code changes). Pre-existing content changed only to fix factual errors, with accurate phrasing and voice left alone.
- No hedging ("appears to", "seems to", "likely", "probably", "should", "will"), no new subjective adjectives, and no code dumps.
- Every file reference is a clickable link resolving to a file, not a directory. Configuration references name the value a consumer changes it by.
- Acronyms you wrote are capitalized and expanded on first use (exceptions: brand/tool/package names, domain terms, code references).
- New or changed prose reads as a careful human wrote it: leads with the point, no signposting or banned AI tells, one canonical term per concept spelled identically in every document in scope, no ambiguous `it`/`this`/`these`.
- Every document you wrote or reworked opens by naming its subject and why a reader would reach for it, states what that reader must already have or have read, and introduces every acronym, term of art, and named component the first time it uses one.
- **Read each document once as the newcomer**, who has not seen this codebase, fix a missing introduction, subject, or prerequisite where you find one, name in your output anything left, or state that nothing stops them: a page only its author can follow is not finished. Then read it as the experienced reader, for whom a paragraph they could have got faster from the source has not earned its place either; there the fix is what the paragraph fails to add, not deletion by default.
- Architecture flows include only significant steps (§4); every diagram has `accTitle` and `accDescr`, and every image has real alt text.
- No em-dashes (`—`) or en-dashes (`–`) anywhere you wrote; new or changed prose uses Canadian English.
- Every public symbol you touched carries a documentation comment written from its implementation, not from its name, and no comment narrates a change, names something that no longer exists, argues the code is safe, or sits commented out. No comment you added sits above a usage site rather than a declaration, and every comment you removed as a repetition either said no more than the declaration's or had what it added folded into the declaration first.
- Rendered output was checked, not only the source: diagrams parse, nested lists render, and documentation comments display the intended text. Every table you touched was re-read whole, with each row's cell count matching its header and no cell broken across lines.
- Every document you created sits in a directory whose existing documents are the same Diátaxis type, or in a new directory created for that type, and your output names the directory and what decided it.
- No comment you wrote or kept describes something the file does not contain, and every comment you deleted on that ground was one you could not attach to a line.
- No comment, existing or new, runs longer than what it documents: an accurate but disproportionately long comment was compressed to its non-obvious content (Phase 3), not left in place because it was not wrong.
- Every document read in full this run, judged as a whole rather than paragraph by paragraph, is no longer than a careful human would have written for the same brief (Rule 6); a page found mixing a brief overview with deep reference, how-to, or explanation content was split rather than left layered.
- A passage that stayed long after Rule 6's trim was weighed for a complementary diagram, table, code/config snippet, or image (Rule 6), and one was added where it fit the content.
- Phase 3 ran and its result is reported.
