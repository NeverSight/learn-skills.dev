---
name: accessibility-testing
description: Use for testing the accessibility of a web project
license: MIT
metadata:
  author: conesible.de
  version: "0.1"
---

Implementing accessibility correctly is crucial to deliver quality web experiences for everyone, including developers. 

## Software requirements & programmatic testing

To catch accessibility defects quickly and reliably, employ automated and rule-based accessibility checks. For this, set up a development requirement for the `pa11y/pa11y` CLI tool and the axe-core runner, and run it against fresh development builds. Also cover individual features and components, isolated from the rest of the page.

Include these checker tools into an existing CI pipeline. 

## Manual checks

For each component, check each component for its full WCAG 2.2 level AAA conformance, and create a table that contains the number of the success criterion, its name, a short description, and the conformance status (pass, fail, not applicable, untested)

If it helps, you may also make this as a template and re-use it accordingly. 

You may use browser based tools (like Playwright) to run checks yourself that traditionally required real users for testing. If you can't make a judgement or it might be un-reliable, note a todo with a clear and concise assessment instruction for a developer.  

## Generate deliverables

Whenever you have made an accessibility assessment or judgement, produce a short writeup of all documented issues and suggested fixes. Never suggest quick-wins or shorthand fixes if a complete architectural overhaul would be the better and correct choice. This is especially true if the quick fix would involve ARIA patterns. 

## Accessibility information (European Accessibility Act requirement)

As required per EU law and local equivalents (e.g. Barrierefreiheitsstärkungsgesetz/BFSG in Germany), projects are required to have a public-facing information page about the accessibility of the page, with the following contents in natural language:

- the name of the service
- a general description of the service
- email address and phone number of the provider, and a physical address if available
- names of the applicable laws
- a mention of used tools and processes to ensure accessibility, as well as the names of any agent that is used for the assessment
- accessibility details for each criterion in simple language (pass, fail, not applicable)
- contact details of the governing body (in Germany for example, Marktüberwachungsstelle der Länder für die Barrierefreiheit von Produkten und Dienstleistungen, MLBF AöR, Magdeburg)
- the date of the last assessment
- a date at which all failed requirements are fixed

The law also mandates that developers inform the governing bodies of their offerings pro-actively. Draft an email for that and research the relevant email address. 

This page must be available on every page, near other regulatory links such as a privacy policy.

Implement this page in any case, even if the service may not be directly covered by the law.