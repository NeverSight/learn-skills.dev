---
name: documentation
description: Write, review, and organize project documentation, including READMEs, guides, product comparisons, release notes, code comments, TSDoc/JSDoc, and public API reference. Use when editing documentation or comments, writing comparison content, reviewing a diff that touches them, or deciding what to document and where it belongs.
---

# Documentation

Write the explanation the reader needs at the place they need it. Document useful intent, behavior, constraints, and usage. Names, types, and obvious implementation usually need no prose.

## Choose the reference

Read only the references relevant to the task. Their scopes overlap when public API comments feed a generated reference or a user guide demonstrates an API.

* [Code documentation](references/code.md): comments on public or internal symbols, implementation comments, configuration, and module headers.
* [API documentation](references/api.md): supported public interfaces, generated reference, and required `@since` tags. For source comments, also read the code reference.
* [External documentation](references/external.md): READMEs, guides, announcements, release notes, changelogs, CLI documentation, examples, and interactive documentation.
* [Comparison content](references/comparison-content.md): product or tool comparisons, "X vs Y" pages, alternatives, and "best tools" roundups. Use for comparisons that help readers choose, not ordinary before/after release descriptions.

## Shared rules

### Add information the reader cannot easily infer

Use the minimum explanation that preserves useful meaning. Describe consumer contracts for symbols, and reasons or failure consequences for maintainers. A symbol's consumers include code that uses it within the repository. Explain implementation mechanics only when they matter to usage or safe changes.

If confusing code is the only reason a comment is needed, first consider clearer names, types, control flow, or structure. Keep warnings about non-obvious behavior even when the code is otherwise clear.

### Put information in its appropriate home

Choose by the reader's task and how the information will be maintained. Internal or external describes the audience; it does not determine whether the text belongs in a work record, maintained documentation, or a release communication.

| Destination | What belongs there |
| --- | --- |
| Issue | Problem or request, reproduction, scope, acceptance criteria, open questions, and work tracking. |
| Pull or merge request | Proposed change and rationale, review context, validation results, comparison baselines, and rollout details for that change. |
| Internal documentation | Architecture, operating procedures, project requirements, and decision records that maintainers need beyond a particular change. Preserve relevant constraints and tradeoffs. |
| External documentation | Supported behavior, concepts, tasks, and troubleshooting that users need for the documented version. |
| Source comments and API reference | Symbol contracts, local implementation constraints, and supported interfaces, close to the code or generated from it. |
| Release notes | Changes in a release, their impact on existing users, and compatibility or migration actions. |
| Changelog | A version-indexed record of changes, often assembled from release notes or changesets. Follow the project's format and generation process. |
| Announcement | Selected news for a particular audience, why it matters, availability, and where to learn more or act. |

These roles may share a file or publishing channel. A changeset is input to release tooling; write its published body for the audience of the resulting release note or changelog entry.

Keep work-specific investigation, reconciliation passes, and unreleased branch history in the issue or PR/MR. Carry conclusions needed for future use or maintenance into the appropriate documentation. Internal docs need that distinction too; they should not become a transcript of how the change was produced.

Follow the project's existing source of truth. If an issue is the canonical requirement or decision record, link to it rather than creating a competing specification. Otherwise use the existing notes or specification area. Create a new structure only when the project needs one.

Derive or link to canonical information where practical, while keeping each destination useful on its own. An issue or PR/MR link does not replace a necessary contract, local warning, or migration instruction. Writing one artifact does not require creating all the others.

Explain decisions through project requirements, constraints, and consequences. Include private discussions or personal preferences only when the user requests that context and it suits the audience. Mention a rejected alternative only when its concrete tradeoff helps a current decision or prevents a plausible harmful change.

### Respect audience boundaries

Decide who can encounter the text from the actual output. A comment may reach consumers through IDE hovers, generated reference, declaration files, or package tooling, even if its implementation looks internal.

When one source feeds several outputs, check the complete text each audience receives. A heading or metadata label does not necessarily filter the content for that destination.

Consumer-facing text must stand on its own and link only to public documentation intended for those readers.

Write consumer-facing text around behavior, constraints, and actions the reader needs. Publicly accessible process context can still be irrelevant to the reader. Include history when it helps the reader use, understand, or migrate the product.

### Explain local consequences of external facts

Ask who owns a fact and where someone would correct it. For language rules, tool behavior, and other externally maintained facts, repeat only the detail needed to explain a local consequence.

Keep the essential explanation in the documentation itself. An external issue or discussion can support it, but should not be needed to understand the project's decision or constraint.

### Follow conventions and keep facts current

Inspect nearby documentation for terminology, formatting, tag usage, and tooling. Reuse established patterns rather than introducing a competing style.

Check claims against the implementation or release the text describes. Update maintained documentation when behavior changes. Preserve accurate historical release entries and announcements; correct errors without rewriting them to describe today's behavior.

## Review

Before finishing, check that:

* The text adds useful information for its audience and sits where readers need it.
* Contracts and local warnings remain clear without duplicating specifications or reference manuals.
* Links and context suit every audience that receives the text.
* Lasting contracts and decisions are documented where future readers need them; work-specific process context stays in the issue or PR/MR.
* Links, examples, signatures, and claims match the documented version or release.
* The edit follows project conventions and contains no unnecessary explanation.
