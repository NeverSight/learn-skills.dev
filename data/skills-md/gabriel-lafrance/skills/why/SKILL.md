---
name: why
description: Answers why code is shaped this way with evidence tiers (found, inferred, unknown) and the sources consulted, including empty searches. Use when the user asks why something was built this way or wants the design rationale. Does not write tickets or code.
category: Documents
---

# Why

Answer "why is it this way?" with evidence. A fact, an inference, and a gap are different sentences.

`/how` answers how it works. `/analyze` writes the broader memo. This skill does not write tickets or code, and it does not start a build. The selected execution skill owns any later build.

The evidence tiers are adapted from poteto's [pstack](https://github.com/backnotprop/pstack) `/why` (MIT). The steps below are this pack's.

## Read when

- About to search history or read large files? Open [main-context.md](../rules/main-context.md). Skip it and raw logs bury the reason.
- About to judge whether the shape is still the right one? Open [code-quality.md](../rules/code-quality.md) and [code-structure.md](../rules/code-structure.md). Skip them and the rationale endorses a messy layout.
- About to reply? Open [Plain language](../rules/writing-style.md#plain-language) and [Unslop](../rules/writing-style.md#unslop). Skip them and the answer sounds more certain than the evidence.
- About to ask the user anything? Open [Asking the user](../rules/writing-style.md#asking-the-user). Skip it and you ask what git already answers.

## Contract

- Anchor in the code before any parallel search: paths, symbols, then recent commits and pull requests (`git`, `gh`).
- A missing connector is a gap. Do not invent tickets, chat, metrics, or errors.
- Label every inference. Confidence matches the evidence.

## Process

1. Name the decision you are explaining: a shape, a name, or a rejected alternative.
2. Read the code that embodies it. Record paths and symbols.
3. Run source control on those paths: `git log`, `git blame`, and `gh` for recent commits and pull requests. This category always runs.
4. Only then cover the other categories below. Parallel lookups are fine after the anchor. When the harness allows model choice, use a strong reasoning model to separate found facts from inferences. Do not hardcode a vendor or a model slug.
5. Standalone, write the answer below. Nested, follow
   [nested capabilities](../rules/planning.md#nested-capabilities) and return
   the bounded decision rationale without a full standalone answer. Preserve
   Found / Inferred / Unknown, confidence, and source evidence in either mode.
   List every search you ran, including the empty ones. Keep each lookup tied
   to the named historical decision; do not widen into a new design investigation.

## Evidence categories

Cover every row. When this session has no connector for a category, write "no connector" in Sources consulted. Do not skip the row and do not fill it.

| Category | Where to look when a tool exists |
| --- | --- |
| Source control | `git` and `gh` on the anchoring paths. Always. |
| Issue tracker | The connected tracker (GitHub issues, Linear, or whatever this session can query) |
| Long-form docs | ADRs, RFCs, and design docs in the repo or a connected doc tool |
| Team chat | The connected chat tool |
| Infra observability | Connected logs, traces, or dashboards |
| Error tracking | The connected error tracker |
| Product analytics | The connected analytics tool |

## Answer

### Why

The decision, in a few sentences. Each sentence is a fact or is labeled as an inference.

### Evidence

- **Found:** paths, symbols, commit subjects, pull request numbers, issue ids. Something you opened.
- **Inferred:** the conclusion, and the found facts it rests on.
- **Unknown:** what would change the answer, and was not available.

### Sources consulted

Every search, including ones that returned nothing. Name the tool and the query. A category with no connector is "no connector".

### Confidence

High, medium, or low, and the one reason.

### If this is a precursor to a change

Optional. Omit when the user only wanted the history.

- **Preserve:** what the evidence says to keep
- **Change:** what the evidence says is safe to change
- **Avoid:** the approach the history already rejected
- **Risk:** what the evidence does not cover

## Anti-patterns

- A why with no path or symbol
- Treating an inference as a fact
- Filling a gap with a plausible story
- Starting Slack, tickets, or metrics before the code anchor
- Writing a ticket or editing code
