---
name: explore-new-capabilities
description: Discover and discuss new capabilities for a project, one evidence-grounded idea at a time, with persistent exploration history.
disable-model-invocation: true
---

# Explore New Capabilities

Find capabilities that could create value for a project's users, then refine one idea at a time through discussion. A Feature Opportunity can be a small convenience or a substantial direction. It needs a concrete scenario and a plausible implementation path, while demand, scope, and feasibility may remain unsettled.

This explicitly invoked workflow serves contributors, maintainers, and product developers. It works without a supplied feature idea. Discovery is the agent's responsibility; the user owns priorities, trade-offs, and whether to pursue an opportunity. Work ends at discussion, bounded evidence gathering, and exploration records. Product implementation and external publication require a further instruction.

## 1. Establish the project and history

Read the project's guidance, purpose, and public capabilities. Use the user's direction, role, and available effort when supplied; ask only for missing context that would change the exploration. Establish enough grounding to identify concrete user outcomes without requiring a whole-project audit.

When the user also selects Just Use It, follow its [outcome scope](../just-use-it/SKILL.md#establish-the-outcome-scope) before usage and preserve its source and tracker gates. Otherwise, read relevant source as part of project grounding.

Use [Assess Findings](../assess-findings/SKILL.md), installed with `investigate-with-evidence`, for common evidence, relationship and action judgment. Read its [working-record contract](../assess-findings/references/working-records.md) to resolve configured history, match the project and prior opportunities, save records, check delivery and handle their lifecycle. Reuse configured paths without another question; when unavailable, continue project grounding but defer presenting a new opportunity until its history can be checked and saved. Missing assessment support leaves the judgment pending rather than claimed complete.

Match ideas by user problem and intended capability. Continue an unfinished match in its existing record. Reopen a concluded match only for material new evidence or an explicit request, retaining its previous outcome; otherwise skip that lead. Repeat this identity check before first presentation. Preserve the existing layout and previously authorized commit scope.

**Ready when:** the project identity and relevant constraints are established, the record location is usable, relevant earlier records have been read, and any supplied idea has been matched to the history branches above.

## 2. Find and ground an opportunity

Start from a concrete situation and what the user is trying to understand, decide, or do. For clues involving missing context, information organization or presentation, simultaneous reference, preparation before action, or users' existing tools, consult [discovery entrypoints](references/discovery-entrypoints.md). Follow the relevant clue rather than treating these routes as a coverage checklist.

When exploring combinations of existing capabilities, follow the user's next task after an operation succeeds. Identify repeated transfer, conversion, or setup needed to carry its result forward. Locate the information and behavior the connection needs and who already owns them. Follow relevant clues into comparable projects, complementary tools, and user-assembled workflows. Explain which part of an outside idea transfers and what must change for this project. Another product having a feature is inspiration, not evidence that this project's users need it.

When an existing capability affects content from several sources, trace one user outcome through who supplies the content and where it is used. Compare product-owned content, extension-provided content, and materially different consumers where they exist. Follow a concrete gap into the existing data and integration interfaces to assess an incremental extension. Preserve compatibility requirements that current consumers rely on. Use this as a discovery route when the project has such boundaries, not a requirement to invent extensions or cover every consumer.

Favor opportunities that fit the project's purpose, while allowing a compelling broader direction if its changed assumptions and maintenance burden are explicit. Consider small and large ideas on their merits rather than favoring novelty or size. The agent may compare several leads internally; choose one for discussion instead of presenting a candidate list.

Before settling on a solution, compare materially different ways to meet the same need when plausible alternatives exist. Judge each by the additional user outcome, useful behavior it preserves, and complexity it adds. Keep the strongest approach for discussion and explain the trade-offs that could change the choice. A clear solution needs no invented alternatives; new evidence or user feedback can reopen the comparison.

Before adding an investigation, name the current decision and the unknown most likely to change it. This may concern value, an existing alternative, or feasibility; choose the smallest phase-eligible check that can distinguish the relevant answers. When value is unsettled, compare the closest working alternative before deepening implementation evidence if that comparison can decide whether to continue. When feasibility is the blocker, test that assumption instead. A user-requested technical comparison remains the decision to answer, and a useful optional improvement need not prove necessity.

Use documentation, source, actual usage, or a small disposable check as appropriate. State what the result resolves and which uncertainties remain before choosing further work. Keep checks isolated from product changes and clean up resources created for them. Distinguish source inference from observed execution, and record failed checks as well as successful ones. Costly prototypes can remain proposed next steps.

Start from the user question or task. Exercise the closest existing public route, including relevant companion tools or a practical manual workflow, when it can settle whether the outcome is already available. Describe the result it supplies and the result still missing; keep the capability need separate from a proposed command or UI. Prefer an ordinary working scenario when known defects would confound the comparison. If a supporting example fails, revise that example and investigate any concrete surviving lead before judging the whole idea.

Supply the existing Assess owner with the following evidence before presenting the opportunity; use its judgment and investigate only the gaps it identifies:

- **Value:** a concrete user situation and the additional outcome the capability could enable. Separate observed needs from hypothesized benefits.
- **Feasibility:** traceable evidence in the target project's interfaces, data, architecture, or demonstrated behavior supporting a plausible implementation path. Check the assumptions required to transfer an outside example.
- **Prior work:** whether existing capabilities already satisfy the scenario, and whether exploration records or relevant project issues, PRs, and discussions already cover it. Before checking community work or using it to refine an idea, read [prior work and discussion](references/prior-work.md).

Use the history branches above for local matches. For related community work, retain its status, scope, and reasoning; an unchanged idea already covered there or a scenario satisfied by shipped capabilities sends discovery to another lead. Revisit it when the user asks or material evidence or conditions change, linking the earlier work. If a source cannot be checked, state the uncertainty and avoid claims of novelty.

**Ready when:** one opportunity has a concrete scenario, a supported plausible path, and an account of prior work and remaining uncertainty. If relevant leads yield no such opportunity, report the examined scope and evidence limits instead of filling the gap with an unsupported idea. Do not keep widening the search merely to produce a result.

### Delegate a factual question when useful

Use the shared [coordination method](../assess-findings/references/coordination.md) when an independent question about the user scenario, alternatives, prior work or feasibility merits a research worker. Give it the current opportunity, the decision-changing question, relevant records and phase permissions, allowed checks and a stopping condition. It returns evidence, limits and record-update suggestions; it does not choose a different opportunity, implement the product or write shared records. Keep the user discussion with the main agent and send material results to the same Assess owner. Small or tightly coupled research stays inline.

## 3. Present one idea and discuss it

Save the initial record with its assessment or explicit pending state when first presenting the idea. Explain what users could do, why it is worth discussing now, why it appears feasible, and what remains uncertain. Cite the supporting sources and explain why this opportunity was selected. Keep the initial proposal understandable without treating it as a settled specification.

Invite the user's reaction, then follow the questions it opens. Investigate factual uncertainties yourself; ask the user about goals and trade-offs with concrete alternatives and a recommendation when warranted. Use answers to revise the current idea, narrow or broaden its scope, or discard it. Ask dependent questions after their prerequisites are answered. Respect settled choices unless new evidence changes their basis.

Keep discussion on this opportunity. Related alternatives that solve the same user problem can clarify it; a distinct capability waits until the user chooses to explore another opportunity. Size does not determine identity: a large direction can still be one coherent idea.

The skill works independently. When the user also invokes a grilling skill, let it deepen the current opportunity's questions while this workflow owns discovery, evidence, and history. With `grill-with-docs`, resolved vocabulary and qualifying decisions follow that skill's documentation rules; exploration history still retains the idea's evidence and outcome. These are optional companions, installed separately.

**Complete when:** the user chooses to pursue, defer, or dismiss the idea, or ends the discussion. Retain unresolved questions without forcing a complete design.

## 4. Preserve the outcome and return control

Update the opportunity record at meaningful discussion boundaries and before closing. Keep a concise current account plus dated material changes, preserving why earlier judgments changed. Each record should let a later conversation recover:

- The project identity, idea, user scenario, and intended capability.
- Inspiration and evidence, with source links or code references, checked revisions or dates where useful, and what each source actually establishes.
- Prior related work and the scope or limitations of duplicate checks.
- Open assumptions, feasibility limits, and results of any disposable checks.
- The discussion's current state, decisions and reasons, and conditions for reconsideration.

Keep the index consistent with the record. Complete authorized local commits at these same boundaries using the [working-record checkpoint procedure](../assess-findings/references/working-records.md#save-and-commit-a-checkpoint). An unfinished discussion remains unfinished; silence does not select a disposition. If saving fails, retain the update in the conversation, report the failure, and resolve persistence before presenting another idea. These records preserve exploration, not formal feature specifications or tracker items; follow the project's conventions when the user later requests those artifacts.

Close with the current conclusion, unresolved evidence, record location, and the commit result when committing was authorized. Let the user decide whether to continue this idea, explore another, or stop. Choosing to pursue an idea does not itself start implementation.

**Complete when:** the record and index are saved and consistent, each authorized commit is verified or reported as pending with its cause, and the user has the current conclusion, unresolved questions, and record location.
