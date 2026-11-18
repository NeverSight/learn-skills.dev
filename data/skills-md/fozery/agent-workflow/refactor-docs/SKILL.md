---
name: refactor-docs
description: Refactor existing documentation and factual memory for clarity and structure while preserving technical meaning. Use for ADRs, specifications, READMEs, guides, CONTEXT.md and LESSONS.md.
---

# Refactor docs

Edit the expression and organization of existing artifacts, not their decisions or requirements. This includes factual context and lesson entries. Reusable execution rules are outside this procedure; handle them as a separate, authorized change under the project contract. Classify mixed sections by purpose. File retirement and code refactoring are separate work.

## 1. Establish the writing rules

Read applicable project instructions for language, style, document formats and required sources.
This package works without another writing skill. If the project requires one, treat it as a project prerequisite and resolve missing access before affected edits.
Do not silently install packages or change session-wide instructions.

**Done when:** the applicable writing rules are known and any required project source is readable.

## 2. Establish scope and preserve meaning

Read project instructions and the requested documents before proposing changes. Identify the reader, purpose, authoritative sources, required format, language, editable scope and approval restrictions. Reuse project conventions and existing terminology. Ask only about unresolved choices that materially affect the edit; an explicit request to edit named documents needs no repeated permission for that same scope.

For ADRs, specifications, READMEs and project memory, read the applicable sections of [document-type rules](references/document-types.md). Keep an original version available for comparison. Identify each document's substantive claims, requirements, decisions, rationale, alternatives, limitations, examples and open questions, including their scope and source links.

Treat commands, code, paths, identifiers, API names, errors, dates, quantities and units as protected technical content. Preserve negation, conditions, exceptions, defaults, ordering, approval gates and normative strength such as MUST versus SHOULD. For ambiguous or contradictory content, consult available authoritative sources; leave unresolved meaning intact and ask the owner rather than inventing a resolution.

**Done when:** the target files, required structures and protected meanings are identified, and any ambiguity blocking a safe rewrite is resolved or excluded from the edit.

## 3. Rewrite within that contract

Write clear artifact prose in the project's format and language. Lead with the supported fact, name the actor and action, keep one idea per sentence and group related information. Replace filler, unsupported praise and repetition with supported content. Flag claims without evidence instead of inventing precision. Follow additional styles only when the task or project requires them.

Remove wording or repetition only when no distinct fact, condition or reasoning is lost. Keep one authoritative explanation and a usable pointer where another reader needs it. Concision is not a word-count target: necessary caveats, counterexamples and trade-offs stay. Preserve deliberate terminology and document structure even when a general style preference suggests another form.

Keep conversational questions and closing conventions in the conversation unless the required document format calls for them. Prefer targeted edits. Preview moves, file splits, heading/anchor changes or altered document ownership when they exceed the authorized scope; include affected references in their approval. Leave unrelated files and concurrent edits untouched.

**Done when:** every edited passage has a concrete clarity or structure improvement, and every protected meaning remains represented in its proper authoritative location.

## 4. Verify and report

Compare the original and edited documents by meaning, not just length. Account for the substantive content identified in step 2, especially negations, normative requirements, values, prerequisites and permissions. Restore anything accidentally weakened, strengthened or omitted. Editorial cleanup must not turn a proposal into an accepted decision or a historical claim into a claim about the current system.

Check changed headings, internal anchors, links, image references and any generated table of contents. Run the project's narrow Markdown/documentation check when available. Distinguish editorial verification from technical fact-checking; report claims or external references you could not verify rather than calling them validated.

Report the edited files, material structural changes, checks performed and unresolved questions. Keep the result in the existing documents; create a separate report only if requested or required by project policy. If the text already meets the requested standard, report that result without manufacturing edits.

**Done when:** protected content is accounted for, the affected structure and references have been checked, and any remaining uncertainty is explicit.
