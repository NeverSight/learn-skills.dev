---
name: translating-documentation
description: Use when localizing technical documentation while preserving code, commands, identifiers, diagrams, references, and technical terminology for guides, API references, READMEs, and developer documentation.
---

# Translating Documentation

## Overview

Define the technical-document surface around a translation. Preserve executable examples, identifiers, references, and document topology while exposing explanatory prose with enough technical context for accurate translation.

## Capabilities

- `surface:documentation`
- `code-preservation`
- `technical-terminology`

## Input Inspection

Parse the whole document and inventory:

- format, frontmatter, headings, paragraphs, lists, tables, admonitions, footnotes, and generated regions
- code fences, inline code, commands, prompts, output, placeholders, variables, identifiers, API methods/paths, schemas, enums, and example data
- internal/external links, anchors, reference definitions, includes, citations, image/media paths, and cross-references
- diagrams, node IDs, edges, syntax, display labels, captions, and alt text
- source and target locale, audience expertise, product/version scope, technical glossary, protected terms, style guide, and publication constraints

Determine whether a code comment, sample value, diagram label, or inline span is executable, user-facing, or both. When uncertain, protect it and ask the technical owner for its contract.

## Translation Surface

Send explanatory prose, headings, table prose, admonitions, captions, meaningful alt text, link labels, and confirmed display-only diagram labels to `translating-core`. Attach the surrounding section, audience, concept definition, approved technical glossary, protected-token inventory, and reference target.

Translate code comments or display-only sample values only when the brief explicitly authorizes them and their executable effect is understood. This skill does not generate target prose, choose technical terminology beyond approved inputs, or apply language mechanics.

## Non-Translatable Elements

Preserve byte-for-byte unless an authoritative technical change is separately approved:

- code fences and language labels, inline code, commands, flags, prompts, environment variables, placeholders, and identifiers
- API methods, paths, versions, parameters, schemas, property names, enum values, response values, and protocol literals
- URLs, link destinations, anchors, reference IDs, include paths, citation identifiers, image paths, and generated markers
- diagram syntax, node IDs, edges, classes, attributes, and identifiers
- product names and protected technical glossary terms

Translate a link label, not its destination. Translate a diagram's confirmed display label, not its node identity or connectivity. Never “fix” an API detail, command, or example because it looks outdated during localization.

## Documentation Constraints

- Preserve document topology: heading levels/order, lists, table shape, callout type, code/inline boundaries, references, media, and diagrams.
- Keep each executable example runnable and semantically equivalent. Do not translate a literal token merely because readers can see it.
- Apply the approved technical glossary consistently by concept and context. Record a missing term as a draft terminology decision for core/domain ownership; do not silently coin an approved term.
- Keep references resolvable. A localized link or anchor requires a verified mapping supplied by documentation ownership; otherwise retain the source destination.
- Keep prose and examples aligned: parameter names, return fields, sequence, prerequisites, outcomes, and version scope must agree.
- Preserve deliberately mixed-language technical terms and distinguish them from accidental untranslated prose.

## Targeted Research

Research only technical facts that may be current and materially affect the document: the documented product version, endpoint, CLI flag, schema, enum, behavior, localized reference mapping, or official component name. Prefer authoritative version-matched product documentation, source code, or release notes and record the source/version/date.

Treat a verified technical correction as a separate documentation change owned by engineering/documentation, not as translation. Do not research ordinary target wording, infer API migrations, or rewrite an example before that change is approved in the source.

## Authority and Conflict Boundary

Follow explicit user requirements, approved technical/product configuration, core semantic fidelity, domain terminology, and language mechanics before documentation formatting preferences. Engineering owns executable behavior and technical facts; documentation owners own structure, reference maps, examples, and publication configuration.

This skill owns document field classification, protected technical structures, reference/example constraints, and documentation QA. `translating-core` owns meaning and target prose; installed domain/language specialists own terminology and linguistic mechanics; `reviewing-translations` owns final review. If natural prose conflicts with an exact identifier, code example, or approved glossary term, preserve the technical contract and report the affected segment.

## QA Handoff

Pass source and target documents, locale pair, product/version scope, technical glossary, protected-token inventory, reference map, executable examples, diagram manifest, and these checks to `reviewing-translations`:

- protected-token diff confirms code fences, inline code, commands, flags, variables, identifiers, API/schema literals, URLs, anchors, paths, diagram IDs, and protected names retain parity
- document parser confirms headings, lists, tables, callouts, links, references, code blocks, media, and generated markers preserve topology
- examples parse, compile, or run using the project's safe documented test method; JSON/YAML/XML and command syntax remain valid
- link and anchor checks confirm internal and external cross-references resolve to approved destinations
- diagram renderer confirms valid syntax, unchanged nodes/edges, and complete translatable display labels
- glossary, concept, parameter, return-value, prerequisite, and version references remain consistent across prose and examples
- no accidental untranslated prose or full-width/localized characters enter protected literals

Block publication for broken executable content, changed technical behavior, corrupted identifiers, unverified version/API correction, broken cross-reference, altered diagram connectivity, glossary conflict, or accidental mixed-language prose. Route the exact affected span or enclosing example to its responsible installed skill.
