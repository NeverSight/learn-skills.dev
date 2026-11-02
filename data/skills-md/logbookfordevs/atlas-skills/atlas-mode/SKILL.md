---
name: atlas-mode
description: "Work in Atlas Mode: choose fitting methods, resolve meaningful workflow choices and carry out the selected approach."
disable-model-invocation: true
---

# Atlas Mode

Work in Atlas Mode for this task and its follow-ups until the user exits it. Take responsibility for selecting the working approach with the user and carrying it out. The user supplies the outcome; they need not remember skill names, inner modes or invocation syntax.

## Working in the mode

1. Establish the outcome from the conversation and inspect the relevant project context. If invoked without a task, ask what the user wants to work on.
2. Read [Methods](references/methods.md) and use the selection rule below to choose the skills and inner methods. Once the approach is selected, resolve those skills through the host's installed catalog, read their entry instructions and selected references, and perform the work.
3. At meaningful transitions, use the same selection rule before changing the approach. Continue an agreed workflow without asking again; carry explicit choices and active records into follow-ups. Finish when the requested outcome and selected methods' completion conditions are met.
4. Hand off the result with the evidence, remaining uncertainty and decisions the user needs. Each selected method owns its evidence format; reuse the same evidence when it answers the same question.

A manually invoked skill remains manual outside Atlas Mode. Inside this explicitly requested mode, read and apply its instructions directly once the approach is selected, including Wayfinder, To Spec, To Tickets, Writing for Humans, Retro, Figures and Animated-Driven Frontend. Treat natural-language requests for their outcomes as sufficient selection; require no extra invocation ceremony.

Select complementary methods where they address different needs. A settled implementation can begin directly; routine changes use normal project validation. The method guide supplies selection conditions, not mandatory phases or instructions to run the whole collection. Apply the selected skill's actual procedure rather than reproducing it here.

## Selecting the approach

When the request or an existing agreement clearly identifies the method, briefly name it and proceed. “Build this test-first” selects Implement's TDD; the user need not know that invocation name.

When plausible methods imply materially different outcomes, artifacts, effort or commitments, explain the relevant choices in plain language, recommend one with a reason, and wait for the user's selection before starting that workflow. Include the inner modes that change the choice. For “help me plan this project,” distinguish challenging assumptions with Grill, mapping unresolved decisions with Wayfinder, and synthesizing settled requirements with To Spec. Ask about the intended outcome, not which skill name the user remembers. Reuse preferences and decisions already supplied.

A request for advice, options or what to do next stays advisory until the user selects an approach. Continue independent work already authorized while a choice is pending. Routine implementation details within an agreed approach need no new workflow choice.

## Scope and choices

Explicit user choices take precedence over inferred selections. Preserve method-level opt-ins: With Docs, States, Tracking, Audit Trail and Retro Enforce require their requested outcomes in the conversation or an existing active selection. Retain Atlas Explain's chooser when the explanation mode remains unspecified, and Atlas Figures' treatment menu and user selection. Atlas Mode's activation alone does not request those outcomes.

Keep the task's authority through transitions: a review stays read-only toward product code and Retro Diagnose stays advisory. Honor existing approval for concrete work without asking again. Follow the selected method's rules for external writes, acceptance and publication.

If a needed skill is unavailable, identify it and the affected work. Continue independent work. Offer targeted installation or a clearly identified fallback, obtaining the user's choice before replacing an explicitly requested method. Use independent companion skills when the task or selected method needs them; Atlas Mode is a working preference, not an exclusivity rule.

Atlas Setup stays outside this mode and requires a separate user request.
