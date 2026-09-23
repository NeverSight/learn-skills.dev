---
name: glossary
description: Writes or audits a project's GLOSSARY.md. Use when the user wants a glossary, or says the documents use one word for two things or leave a term undefined.
license: MIT
argument-hint: <glossary path | files to read | words to define>
---

# Glossary

Find the words a project uses with two readings that no other word settles.
Find the words it uses in a sense a reader would not take from the word
alone. Write the glossary that defines each once. Write only the glossary
and the reference line of Step 4. Report where other documents disagree with
the glossary, and rewrite them with the `unambiguity` skill when it is
available.

The glossary is `GLOSSARY.md` at the repository root, unless the user names
another path. The evidence set is the files research reads for usages. A
term is a word or phrase with a glossary entry. A candidate is a word
research found that has no entry yet. A usage is one occurrence of a word in
the evidence set, as path and line. A restatement is a glossary entry copied
into another document, such as a `## Terms` section.

## Hard rules

1. **Read-only on the project.** Write, or delete, only the glossary, in
   Step 7. The one exception is the reference line of Step 4, which Step 7
   adds to the project's agent instructions. Write drafts in a scratch
   directory outside the repository (in Claude Code, the scratchpad
   directory).
2. **Never ask what research can answer.** Consult the evidence set, the
   code, and the existing glossary first.
3. **Never assume.** When a definition changes the glossary and research
   cannot settle it, ask the user.
4. **Never edit another document yourself.** A usage that disagrees with
   the glossary goes in the glossary report. Only the `unambiguity` skill
   rewrites a document, when Step 7 invokes it. The reference line of Step 4
   is the one exception: Step 7 adds that line and changes nothing else in
   that file.
5. **Write nothing before the user approves the full glossary text and that
   reference line** (Step 6).

## Workflow

### Step 1: State the evidence

Take the glossary path, the evidence set, and the words to define from the
invocation text or the conversation. Without a path, use `GLOSSARY.md` at
the repository root. Without named files, read every Markdown file tracked
by git, minus the files the user excludes.

When the invocation text starts with `from <skill name>:`, that skill
invoked this run. Take the glossary path after `glossary`, the files after
`files`, and the words after `words`. The evidence set is those files, plus
every tracked Markdown file that uses a term of the existing glossary. Step
7 then invokes no skill.

Write one sentence: *Research reads <the files> for usages of the project's
words.* Name the files, or the rule that selects them. Ask one question:
whether that evidence is complete, and which files to add or drop. Ask it
before any research.

### Step 2: Research

**2a. Existing glossary.** When the glossary exists, read it in full. Record
every term, its definition, and its section. When it does not exist, record
that. Record whether the repository root has an `AGENTS.md` or a
`CLAUDE.md`, and whether that file names the glossary.

**2b. Evidence set.** Read every document in full. Use a read-only subagent
for broad sweeps when the agent offers one (in Claude Code, the `Explore`
subagent). Record, with path and line:
- every candidate:
  - a word whose usages point at two things;
  - a word the project uses in a sense that its ordinary sense and its
    common sense in the project's field do not give;
  - a word that a `## Terms`, `## Definitions`, or `## Glossary` section of
    a document defines;
  - every word named in the invocation text or by the user;
- every synonym pair: two words whose usages point at one thing;
- every usage of every candidate and of every existing term;
- every restatement: a `## Terms`, `## Definitions`, or `## Glossary`
  section, and every bullet `- **X**: ...` outside the glossary;
- every verbatim third-party excerpt, such as a quoted vendor page.

A usage inside a verbatim third-party excerpt is evidence of a conflict and
never a rewrite. A rewritten quotation stops being a quotation.

**2c. Code.** Search the project's code for each candidate. Record the
identifier that carries the word and what the code does with it, so that
the definition matches the code, not the prose.

**2d. Findings.** Run the entry test on every candidate and every existing
entry. A word gets an entry when Gate A holds or Gate B holds.

Gate A, a conflict. All three hold:
- the word points at two things;
- no word or phrase with one reading fits every usage;
- the sentence around at least one usage does not settle the reading.

Gate B, an opaque sense. All three hold:
- the project gives the word a meaning that its ordinary sense and its
  common sense in the project's field do not give;
- no document defines that meaning where the word is used;
- a reader who takes the ordinary sense acts wrongly.

A word that holds every condition of Gate A but the second gets a rename in
the glossary report, never an entry. A word that passes neither gate gets
nothing.

Write each finding with its usages:
- a conflict: one word used for two things;
- a synonym pair;
- a candidate that passes a gate, with the gate;
- an entry, in the glossary or a restatement, that passes neither gate,
  with the gate it comes closest to and the condition it fails;
- a fact of an instruction inside a definition: a path, a placeholder, a
  format, a list of allowed values, a section list, or a condition, with
  the document and line that use it;
- an unused entry: a glossary term that no document uses;
- a mismatch: a restatement whose text differs from the glossary;
- a weak definition: one that breaks a writing rule of Step 4.

**2e. Research notes.** Write a private file in the scratch directory with
two parts:
1. *Facts*: every candidate and every finding, with its path and line.
2. *Open decisions*: every decision research did not settle, with the
   entries it affects.

### Step 3: Interview

Order the open decisions: conflicts first, then synonym pairs, then entries
to remove, then meanings research did not settle, then sections.

For each open decision:
- State it in one sentence, with the usages that depend on it.
- Give 2 to 4 options grounded in research. For a conflict, offer a
  qualifier per thing and a new word per thing: `backend component` and
  `frontend component`, never `component`. For a synonym pair, offer each
  word as the one name. For the entries to remove, the entries of 2d that
  pass no gate or are unused, ask one question. It lists each with its
  gate and condition, or the word `unused`: remove all, some by name, or
  none.
- Name the option you recommend.

After each answer, record the decision as a fact in the research notes and
add every new decision the answer creates.

Never ask about:
- a candidate that passes neither gate;
- a meaning the documents or the code settle;
- a word with one reading and one name;
- the wording of a settled meaning.
Continue until no open decision remains.

### Step 4: Write the glossary

Read `references/glossary-template.md` now and fill it, in the scratch
directory, with the terms that pass the entry test. Writing rules:
- Start a definition with a noun phrase that names the kind of thing:
  `a user assigned the patient role in the app`, never `handles patients`.
- Say what the term is, never how it works, never with its own term, and
  never with a banned word. The grep helper of
  `references/quality-checklist.md` lists the banned words.
- Write at most two sentences of at most 25 words: what the term is, then a
  boundary or an example.
- Put no fact of an instruction, as 2d lists them, in a definition.
- Give every term one definition, and no definition two meanings.
- Write the retired word of a synonym pair, and the words of a settled
  conflict, in the glossary report, not in the glossary.

When 2a found no glossary, write one reference line for the project's agent
instructions, in the scratch directory next to the draft. Its file is the
repository root's `AGENTS.md`, or the root's `CLAUDE.md` when the root has
no `AGENTS.md`. The line is:

```markdown
- Read `GLOSSARY.md` first. Use every word it defines with that meaning.
```

Place it as the first bullet under that file's first heading, above every
other rule and every other section. A root instructions file loads at the
start of a session and a folder's file loads later, so the reference belongs
in the root file. Write no line when that file already names `GLOSSARY.md`,
and write none when the root has no `AGENTS.md` and no `CLAUDE.md`. Name
either case in the glossary report.

When no term passes the entry test, write no draft and no reference line. Go
to Step 6 with the glossary report alone and ask whether the user confirms
an empty glossary. On confirmation, Step 7 deletes an existing glossary and
writes no new one.

### Step 5: Quality check

Run every check in `references/quality-checklist.md`, grep helpers
included, over the draft. Fix every failure. When a failure needs a
decision, return to Step 3 for that decision, then run the checks again.

### Step 6: Approval

Show the complete glossary in chat. Show the reference line of Step 4 with
its file and its place in that file. Then show the glossary report as it
stands. Ask whether the user approves the glossary and that line as written
or wants a change. Apply each change, run Step 5 again, and ask again until
the user approves.

### Step 7: Save

Write the approved glossary to its path, unchanged. When Step 4 found no
term, delete the existing glossary instead. When Step 4 wrote a reference
line, add the approved line at the place Step 4 names, and change nothing
else in that file.

Then rewrite the documents that disagree with the `unambiguity` skill when
all of these hold:
- the glossary report holds at least one disagreement;
- a skill named `unambiguity` is available to the agent;
- no other skill invoked this run.
Ask one question: which documents with disagreements to rewrite now. Offer
every listed document that is not a verbatim third-party excerpt, the
documents the user names, and none. For each chosen document, in the order
listed, invoke the `unambiguity` skill (in Claude Code, with the `Skill`
tool) with the invocation text `from glossary: <file path>`. Wait for it to
finish: it shows its rewrite, asks its own approval, and prints its clarity
report.

Finish with the glossary report:
- *Added*: each new term.
- *Changed*: each term whose name or definition changed, with the old text.
- *Removed*: each term removed, with the gate and condition it failed, or
  the word `unused`.
- *Renamed*: each word replaced by a word with one reading. Give the new
  word, every usage in the evidence set, and a count of the usages
  elsewhere.
- *Facts to place*: each fact taken out of a definition, with the document
  and line that use it. The user places these: the `unambiguity` skill adds
  no fact.
- *Instructions*: the file the reference line was added to, or the reason
  no line was added.
- *Disagreements*: every usage in another document that disagrees with the
  glossary, with its path and line and the change that settles it. Add the
  word `rewritten` when the `unambiguity` skill rewrote that document. Add
  the word `quoted` when the usage sits in a verbatim third-party excerpt,
  which stays as written.
Ask nothing else.
