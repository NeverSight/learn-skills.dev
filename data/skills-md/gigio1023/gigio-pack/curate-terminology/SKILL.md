---
name: curate-terminology
description: >
  Settle which name a project uses for a concept when names compete. Survey how
  established projects, papers, and competitor products name it, adopt one
  standard name, and record it in the project glossary with sources. Use when a
  new, contested, or misused term comes up, a recorded entry is wrong or stale,
  the user corrects or bans a wording, or a company-local name is unconfirmed.
  NOT for applying recorded names (use-terminology), undisputed field terms, or
  sentence style and claim strength in documents (copydesk).
---

# Curate Terminology

A project glossary answers three questions per concept: which name the project uses, what it means here, and what others call it. It is a short lookup table, not a writing guide. Terms stay in the field's standard language, usually English; meanings are written in the reader's language.

## Inclusion test

A concept gets a row only when at least one of these holds:

- Names compete, or one name carries different meanings across industry projects, papers, or competitor products.
- A company or local meaning differs from the field's meaning.
- The user made an explicit wording decision, such as banning a word.

Undisputed field terms stay out even when the project uses them constantly. Sentence patterns, "do not write X" advice, and project explanations are not rows. Claim strength and sentence style belong to `copydesk`.

## Survey and decision

1. Read root `terminology.md` and the relevant topic file. A correct entry needs no work. A wrong or stale one is updated in place and keeps its reference ID.
2. Find how two or three recognizable sources in each relevant class name the concept, and whether their meaning matches: established projects, defining papers, and competitor products. [Naming survey](references/naming-survey.md) says which sources count and how to settle a split.
3. Adopt one name in its established spelling. When no established name exists, describe the thing plainly and mark the row unresolved instead of coining one.
4. Confirm local names with the user before recording them, as in [company usage](references/company-usage.md).
5. Write the row and its reference records as in [records and layout](references/records-and-layout.md).

## Entry format

| Term | Meaning | Elsewhere called | Reference |
| --- | --- | --- | --- |
| subagent definition | The configured record that fixes a subagent's model, tools, and instructions | Codex: role; Claude Agent SDK: `AgentDefinition` | R002, R004 |

Meaning is one line. Elsewhere called lists `source: name` pairs, including names the project did not adopt. A one-line caveat goes under the table only where misuse actually recurs. Local names and wording decisions have their own tables.

## Scope of changes

Write records in the project being worked on. After adopting or changing a name, update the documents the current task already edits and list other affected documents rather than sweeping the repository. Quotations, code identifiers, APIs, and data labels keep their original form. In a read-only task, return the proposed row instead of writing it.

## Project instruction snippet

A skill description does not load either terminology skill on every task. The project's instruction entry point does. Add this to `AGENTS.md` or the file the project's harnesses read:

```markdown
## Terminology

Read `terminology.md` at task start and use its recorded names, local names, and wording decisions. When a needed term is missing, contested, or wrong, or a local name is unconfirmed, use `curate-terminology`.
```

Link the glossary rather than copying it. `gigio-project-setup` adds the snippet during a requested project setup.

## Finish

Check that every new or changed row cites a reference record that exists and that the root index reaches every topic file. Report adopted or changed names, rows left unresolved, and local names still waiting for the user.
