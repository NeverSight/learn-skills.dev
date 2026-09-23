---
name: unambiguity
description: Rewrites a text so that every sentence has one reading, with its meaning kept. Use when the user wants a document, spec, or prompt clarified, or says it is vague or misread.
license: MIT
argument-hint: <file path | text>
---

# Unambiguity

Take one text, the input text, and rewrite it so that every sentence has
exactly one reading. Keep the meaning. Write only the file the text came
from. When the `glossary` skill is available, use it to define the terms the
text needs before the rewrite.

An ambiguity is a passage of the input text with more than one reading, or
one that breaks a rule in `references/clarity-rules.md`. A term is a word or
phrase with an entry in the project's glossary, `GLOSSARY.md` at the
repository root unless the user names another path. A candidate is a word
that passes the entry test and has no glossary entry: at one usage at least,
a reader can take it in two ways that lead to different actions; no word or
phrase with one reading fits every usage; and the sentence around that usage
does not settle the reading.

## Hard rules

1. **The meaning stays.** Never add, drop, or change a fact or an
   instruction.
2. **Read-only on the project.** Write only the input file, in Step 7. Write
   drafts in a scratch directory outside the repository
   (in Claude Code, the scratchpad directory).
3. **Never ask what research can answer.** Consult the input text, the
   glossary, the code, and the docs the text names first.
4. **Never assume.** When a reading changes the rewrite and research cannot
   settle it, ask the user.
5. **Write nothing before the user approves the full rewrite** (Step 6).

## Workflow

### Step 1: Load the input text

Resolve the invocation text, or the text in the conversation, as one of:
- **`from <skill name>: <file path>`**: that skill invoked this run. The
  file's content is the input text. Step 7 writes the rewrite to the file.
  Step 2b invokes no skill.
- **A file path**: the file's content is the input text. Step 7 writes the
  rewrite to the file.
- **Pasted text**: the text itself is the input text. Step 7 writes no file.
- **Nothing**: ask for the text first.

Record the width the input text wraps prose at: the length of its longest
prose line, when lines end before the end of a sentence. Record `none` when
the input text does not wrap.

### Step 2: Research

**2a. The input text.** Read `references/clarity-rules.md` now. Then read
the input text in full. Record every ambiguity with its location, its kind,
and its readings.

**2b. The glossary.** Read the glossary, when it exists, and every
`## Terms`, `## Definitions`, or `## Glossary` section of the input text.
Record every term the input text uses with its definition. Run the entry
test on every word whose sense in the text differs from its common sense.
Record every candidate with the readings a reader can take.

Then define the candidates with the `glossary` skill when all of these hold:
- there is at least one candidate;
- the input text is a file inside a git repository;
- a skill named `glossary` is available to the agent;
- no other skill invoked this run.
Invoke it the way the agent invokes a skill (in Claude Code, the `Skill`
tool). Pass the invocation text
`from unambiguity: glossary <glossary path>, files <input file path>, words
<the candidates>`. Wait for it to finish: it asks its own questions and
writes the glossary after its own approval. Then read the glossary again and
record each candidate it defined as a term. When a condition fails, keep the
candidates for the clarity report.

**2c. Referents.** For every referent without a name, search the input text,
the code, and the docs the text names for the thing it points at. Record the
name and where it was found: `the service` is `PaymentService` at
`src/payments/service.ts:12`.

**2d. Conventions.** When the input text belongs to a project, read its rules
for documents: AGENTS.md, CLAUDE.md, CONTRIBUTING, a style guide. Record the
rules that bind the rewrite: line width, headings, section names, required
words.

**2e. Research notes.** Write a private file in the scratch directory with
two parts:
1. *Facts*: every ambiguity with its readings and, when settled, the reading
   that holds with the path and line, identifier, or URL that settled it.
2. *Open decisions*: every ambiguity research did not settle, with the
   passage it affects.

### Step 3: Interview

Order the open decisions: passages with two readings first, then referents,
then quantities, then terms and names, then wording.

For each open decision:
- State it in one sentence. Quote the passage and its readings.
- Give each reading as an option, worded as the sentence that replaces the
  passage: `Retry the call at most 5 times, then raise the last error.`,
  never `keep the retry behavior`.
- Name the option you recommend.

After each answer, record the decision as a fact in the research notes and
add every new decision the answer creates.

Never ask about:
- a reading the text, the glossary, the code, or the docs settle;
- a rule in `references/clarity-rules.md` with one fix;
- wording that changes no reading.
Continue until no open decision remains.

### Step 4: Rewrite

Rewrite the input text sentence by sentence, in the scratch directory. Apply
the fix of every rule in `references/clarity-rules.md`, with:
- the name found in 2c for a referent without a name;
- the terms decided in Step 3 for a word with two meanings, and the
  glossary's term for a synonym;
- the decision from Step 3 for a banned word, a question, an alternative,
  or a passage with two readings.
Use every term as the glossary defines it. Keep every code block, code span,
URL, and quoted string byte-identical. Keep every heading, its level, and
its order: split a sentence or turn it into a list, but never move content
between sections. Wrap prose at the width recorded in Step 1.

### Step 5: Quality check

Run every check in `references/quality-checklist.md`, grep helpers included,
over the draft. Fix every failure. When a failure needs a decision, return to
Step 3 for that decision, then run the checks again.

### Step 6: Approval

Show the complete rewrite in chat, then the clarity report as it stands. Ask
whether the user approves the rewrite as written or wants a change. Apply
each change, run Step 5 again, and ask again until the user approves.

### Step 7: Save

For a file path, write the approved rewrite to that file, unchanged. For
pasted text, the rewrite shown in Step 6 is the output. Finish with the
clarity report:
- *Resolved*: one bullet per ambiguity, at most 2 lines: its kind, the
  passage before and after, and what settled it: the path and line,
  identifier, or URL, or the user's answer.
- *Candidates*: every candidate, with its readings and the reading the
  rewrite uses, or `None.` when the `glossary` skill defined them all.
Ask nothing else.
