---
name: semantic-html-structure
description: "Chooses and writes semantic HTML for a page or component: landmarks, heading outline, native elements for links, buttons, lists, tables, and forms, accessible names, and ARIA only where native elements cannot express the need. Use when markup is being written or restructured, or when markup built from generic elements must be corrected for keyboard and assistive-technology users."
---

# Semantic HTML Structure

## Purpose
Produce markup whose structure and native behavior carry meaning and operation, so the accessibility tree, keyboard behavior, and browser features come from the platform instead of from scripts.

## When to use
- Use when: writing or restructuring the markup of a page, section, or component.
- Use when: markup made of generic elements and click handlers must be converted to native controls.
- Do not use as a conformance audit. It does not replace an accessibility review or testing with assistive-technology users.
- Do not use to decide a component's public interface or its visual appearance.

## Inputs
- Required: the content and its purpose, and the interactions it must support (navigate, act, choose, expand, submit). When restructuring, the existing markup.
- Optional: design or specification, accessibility requirements, existing component conventions, supported browsers.
- Assumptions: text not supplied, such as headings and labels, is marked as placeholder and never presented as final copy.

## Process
1. List the content blocks and what each is (navigation, main content, supporting content, form, data set, list, media) and what a user does with it.
2. Set the landmark structure with native sectioning elements. Use one main region. When a landmark type repeats, give each instance a distinct accessible name.
3. Write the heading outline from the content hierarchy. Do not skip levels, and do not choose a level for its visual size. Size is a styling concern.
4. Choose the native element for each interaction: going to another location is a link, performing an action in the page is a button, choosing among options is a native choice control, and disclosure and dialogs use their native elements where supported.
5. Mark up lists as lists. Mark up tabular data as tables with a caption, header cells, and scope where headers are not simple. Never use tables for layout.
6. Structure forms: a visible label programmatically tied to each control, related controls grouped with a group label, hints and errors tied to their control, and input types and autocomplete values that match the data. Required fields are indicated both visually and programmatically.
7. Decide the text alternative for each image by purpose: informative gets a description of the content, functional names the action, decorative gets an empty alternative. Record needed captions or transcripts as requirements and do not invent them.
8. Set the document language, mark passages in other languages, and give each page a distinct title.
9. List the accessible name of every interactive element and where it comes from.
10. Add ARIA only for a need no native element covers. Record the gap, the exact role or state added, and the keyboard and focus behavior that must now be implemented, because ARIA changes no behavior.

## Rules and heuristics
- Required: native semantics come from native elements. ARIA never replaces choosing the right element and never contradicts native semantics.
- Required: do not attach click handlers to non-interactive elements in place of a native control. If unavoidable, state why and the full role, name, focus, and keyboard obligations.
- Required: DOM order matches reading order and the visual order. Reordering with CSS is a check, not a fix.
- Required: content hidden from assistive technology is not focusable, and focusable content is not hidden from it.
- Recommended: use fewer landmarks, and use a generic section only when it has a name.
- Recommended: link and button text makes sense out of context.
- Recommended: choose elements by meaning, then style them. Do not add elements to get a look.

## Checks
- Exactly one main region, sequential headings, and distinct names on repeated landmarks.
- Every interactive element is native or has documented ARIA obligations, and every control has a label.
- Tabbing through a rendered page follows reading and visual order. If it was not rendered, mark focus order unverified.
- Run a markup validator when one is available. State that validators and automated checks detect only some problems and do not show that the page is accessible.
- Record whether a manual keyboard pass and an assistive-technology pass were performed.

## Output
Return the markup, the landmark and heading outline, the element choices that were not obvious, the accessible-name list, an ARIA ledger (gap, attribute, obligation), placeholders, and the checks performed and not performed.

## Completion criteria
- Each need is met by a native element, or the ARIA use is justified in the ledger.
- Every control has an accessible name and a label, and every placeholder is labeled.
- Checks performed and their limits are stated.
