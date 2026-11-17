---
name: okf-project-knowledge-base
description: Durable project knowledge as Git-native OKF bundles (docs/knowledge/, one concept per file, with provenance and trust tiers). Use to record a decision, finding, or rule that must outlive the session. Not session state or agent instructions.
metadata:
  version: "0.3.1"
  categories: "agents, knowledge"
  topics: "okf, knowledge-base, agent-memory, provenance, documentation"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/okf-project-knowledge-base
    emoji: "📚"
---

# OKF Project Knowledge Base

Durable project knowledge - decisions with rationale, findings with evidence,
rules with what they protect against - lives in the repository as an
[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle: plain Markdown concepts with YAML frontmatter, readable by humans,
parseable by any agent, diffable in git. This skill is the discipline for
creating, writing, reading, and maintaining such bundles. It standardizes the
mechanics; without it every model invents its own incompatible structure.

## Finding the bundle

A bundle root is any directory whose `index.md` declares `okf_version` in its
frontmatter. That marker, not the path, is authoritative: to discover bundles,
search the repository's `index.md` files for `okf_version`. The canonical
location for a NEW bundle is `docs/knowledge/` at the scope it serves - the
repo root for project knowledge, `<subproject>/docs/knowledge/` for a
subproject - but respect existing bundles wherever they live (`knowledge/` at
the root is a common alternative).

## The local law

Before reading or writing anything else, read the bundle's root `index.md`.
Its preamble states what belongs in this bundle and its local conventions
(type vocabulary, directory layout). The preamble may tighten or loosen the
rules below for its bundle; only the instructions fence is never relaxed.

## Three fences

Route by what the information is about, never by how you discovered it. A
finding about a tool this project depends on is project knowledge even when
a session-local tool surfaced it; the default admission test is whether it
is true and useful in a fresh clone, to a reader who never used this
session's tools.

1. **Durability fence (knowledge vs state).** By default, state - counts,
   versions, hashes, in-flight work, "where we left off" - stays out of the
   bundle; it lives in its authoritative source (ledger, git, the tracker
   for work items). A number belongs in a concept only when the number IS
   the finding. Eventual mutability is NOT state: the test is what
   invalidates it - the next commit or session means state; an upstream
   release or vendor decision means knowledge, captured with `stale_after`
   to absorb the decay.
2. **Publicity fence.** Never commit secrets or credentials - git history
   is forever, even in private repositories.
3. **Instructions fence (knowledge vs AGENTS.md).** Agent instruction files
   hold standing orders obeyed every session; the bundle holds facts consulted
   when relevant. When a decision produces both, the instruction file gets one
   line stating the law with a link to the concept; the rationale, history,
   and evidence live in the concept. Never grow an instruction file with a
   rationale paragraph.

## Concept format

Every concept is one Markdown file: YAML frontmatter, then a body. Minimal
conformance is a parseable frontmatter block with a non-empty `type`, a
`description`, and a `generated` record; everything else below strengthens
trust and should be present.

```markdown
---
type: Decision
title: OAuth2 flow standardized on PKCE
description: One sentence a reader or index can reuse verbatim.
tags: [auth, security]
status: stable
generated: { by: claude-code/fable-5, at: "2026-09-07T14:00:00Z" }
sources:
  - id: rfc
    resource: https://datatracker.ietf.org/doc/html/rfc7636
    title: RFC 7636 (PKCE)
---

# Decision

Chosen because public clients cannot hold a secret.[^rfc]

[^rfc]: RFC 7636 (PKCE)
```

Field reference (`type`, `description`, `generated` required; the rest
optional but encouraged):

| Field | Meaning |
|---|---|
| `type` | Kind of concept, producer-defined: `Decision`, `Finding`, `Reference`, `Runbook`, ... The bundle preamble may fix a vocabulary. |
| `title`, `description` | Display name; one-sentence summary reused by indexes and search. |
| `tags` | Cross-cutting labels, a YAML list of short strings. |
| `status` | `draft` / `stable` (default). The spec's `deprecated` is never written here (invariant 5). |
| `stale_after` | Absolute ISO 8601 instant after which the content must be re-verified before use. |
| `generated` | `{ by, at }` - who produced the current content and when it last meaningfully changed. |
| `verified` | List of `{ by, at }` confirmation events. See Actors below for who may write it. |
| `sources` | What the concept derives from. Each entry has a `resource` (URL, bundle-relative path, or an honest scope descriptor for things no link reaches) and an `id` when body claims cite it. |

Attribute specific claims with Markdown footnotes whose labels are
`sources[].id` values - keyed, never positional, so reordering the list
cannot misattribute. Link concepts to each other with normal Markdown links,
bundle-relative (starting with `/`) preferred. All timestamps are ISO 8601
with explicit UTC offset.

## Actors

Identity is derived from the environment, never hardcoded:

- **Humans**: `human:<id>` where `<id>` is the git `user.name` configured in
  the repository holding the bundle.
- **Agents**: `<harness>/<model>` as the session knows itself, e.g.
  `claude-code/fable-5`, `codex-cli/gpt-5.6-sol`.
- **Automated processes**: `process:<id>`.

`generated` is written on every create or content update. `verified` with a
`human:` actor is written ONLY when the human explicitly instructs it or made
the edit themselves - an agent never volunteers human verification. An
unverified concept is honest, not deficient; consumers derive trust tiers
(unverified, machine-confirmed, human-reviewed) from what is actually there.

## Invariants

1. **Search before write.** Query the index and existing concepts before
   authoring. Prefer updating an existing concept over creating a near
   duplicate.
2. **A bundle is never created empty.** Create it at the moment of first
   capture, with that real concept as its first entry - never scaffolding,
   never a placeholder. The first concept is the convention every later
   writer imitates, so give it full frontmatter and real sources.
3. **Every claim is traceable.** Record `sources` for whatever the concept
   derives from; when no durable link exists, write an honest scope
   descriptor rather than dropping the source or inventing a URL.
4. **Indexes are generated, never hand-edited.** A bundle SHOULD carry its
   own index generator and pre-commit hook - in the bundle's repo, not in
   this skill - that rebuilds every `index.md` and fails the commit on a
   missing or empty `type`, or a type outside the folder's declared set
   (a stdlib-only script taking `folder=Type,...` rules is enough).
   Hand-edit `index.md` (a bullet with title, link, and the concept's
   description) only in a bundle without a generator. There is no `log.md`:
   git history is the log.
5. **Only what is true now.** An outdated concept is a hallucination waiting
   to happen, so a concept that stops being true is deleted, not deprecated -
   git history is the archive. This covers a fact that changed upstream, a
   decision about something since retired, and a reversed decision; a
   successor may state what it replaced and why, in the present tense, never
   as a link back. Fix it in the same commit as the change that made it
   false: a change that retires, replaces or upgrades something searches the
   bundle for it and deletes or rewrites what it falsified, including the
   sentences that linked there. A concept only partly outdated is rewritten
   in place.
6. **Progressive disclosure on read.** Enter through `index.md` and open only
   the concepts the task needs; never bulk-dump a bundle into context.
7. **Verify before claiming conformance.** After writing, confirm what the
   format requires: the frontmatter parses with the required fields, links
   you added resolve, and the index is current - run the bundle's generator,
   or in a hand-indexed bundle confirm the index matches the directory. Use
   whatever tools the session has; the checks, not the commands, are the
   contract.

## Workflows

**Cold start** (a repo with knowledge to keep and no bundle): create
`docs/knowledge/` with a root `index.md` whose frontmatter declares
`okf_version: "0.2"` and whose preamble states, in a few sentences, what this
bundle holds and what it refuses (the three fences, localized); the first
real concept (invariant 2); and the bundle's index generator with its
pre-commit hook, or a preamble note that the bundle is hand-indexed
(invariant 4). Then add one line to the repo's agent instruction file
naming the location, telling agents to load this skill before reading or
writing the bundle, and asking for an end-of-task capture review.

**Capture** (mid-work or on request): decide with the fences whether it is
knowledge; search first (invariant 1); write or update the concept with full
frontmatter; regenerate or update the index (invariant 4); verify
(invariant 7). If
the knowledge also implies a standing order, apply the instructions fence:
one line in the instruction file, linking here.

**Recall** ("why did we choose X", "have we established Y"): find the bundle
by its marker, read the index, open only matching concepts. Treat `status`,
`stale_after`, and the trust tier as part of the answer. A concept past its
`stale_after` is checked against its source before use: if it holds, propose a
new `stale_after`; if not, it is false. A concept found false is never used or
reported as current: say so in the answer and propose deleting it - never
delete it during a recall.

**End-of-task review** (after substantial work, when the repo's instruction
file asks for it): scan the work for decisions taken, findings established,
or rules adopted; capture what passes the fences; search the bundle for
anything the work retired, replaced or upgraded (invariant 5); say plainly
when nothing does.
