---
name: deep-learn
description: >-
  Manual-only deep research workflow for systematically learning an unfamiliar topic, technology, product, mechanism, research question, or source packet. Use only when the user explicitly invokes $deep-learn and wants more than a single Web search: independent research routes, subagent collaboration, primary evidence, real cases and failures, adversarial verification, a transferable knowledge model, clear boundaries, and unresolved unknowns. Do not use for quick fact lookup, article drafting, choosing an editorial stance, or replacing professional review.
license: MIT
disable-model-invocation: true
---

# Deep Learn

Turn an unfamiliar subject into an evidence-backed, human-readable knowledge model the user can explain, test, apply, and extend. Do not measure completion by source count or agent consensus. Finish when the core questions have reliable answers, the evidence boundaries are explicit, and the resulting understanding transfers to new situations.

Follow the user's language for interaction and the final deliverable. Keep research instructions, route contracts, evidence states, and technical identifiers precise even when the user works in another language.

## Preserve the boundary

- Handle learning, research, evidence verification, cognitive modeling, and unknown management.
- Design the knowledge pack's own explanatory order so a human can learn from it. Do not draft a downstream article, choose its position or title, design its editorial narrative, or publish it. Downstream work may use the adjudicated knowledge pack, not unreviewed intermediate reports.
- Do not treat one agent's search summary as deep research or several agents repeating the same source as independent confirmation.
- Work read-only by default. Unless the user explicitly requests persistence, deliver in the conversation. When a host project specifies a destination, write only the final knowledge pack and do not persist subagent reports.

## Establish the learning contract

Before searching, derive these fields from the request and available local material:

- **Core question**: what must be understood or decided;
- **Intended use**: learning, technical selection, product judgment, problem solving, or upstream support for writing;
- **Starting point**: what the user already knows, tried, or observed;
- **Success criteria**: what the user should be able to explain, distinguish, apply, predict, or decide;
- **Scope**: inclusions, exclusions, time, region, version, population, and operating conditions;
- **Evidence standard**: which claims require primary documents, source code, data, experiments, or real cases;
- **Stop conditions**: what closes the evidence loop and what must wait for new data, access, experiments, or expertise.

Keep the user's experience and intuitions as motivations or observations to test. Do not promote them to facts. If the contract is sufficiently clear, proceed. Ask one necessary question only when different answers would materially change the research portfolio.

## Select the research intensity

- Use **focused research** when the question is narrow, authoritative sources are concentrated, and there are no independent evidence mechanisms. Focused narrows the scope; it does not imply short or shallow work. Unless the user explicitly asks for a quick or brief pass, assume the default high-investment evidence loop and reader pass. The lead agent completes the full evidence loop.
- Use **portfolio deep research** when the subject is unfamiliar, spans multiple mechanisms, depends on real cases, contains source conflict, or the user explicitly requests systematic multi-angle or subagent research. Prefer this mode when at least two high-value routes can advance independently.

Research may branch across routes, but understanding must converge in one integrated model and one canonical knowledge pack. Route or subagent order is a research operation, not the structure of the final reading experience.

Do not start subagents to simulate effort. When the host cannot use subagents, execute the routes sequentially. Record the lack of independent discovery only when the learning contract or a high-impact claim depended on that independence; do not expose orchestration trivia merely to prove that work happened.

## Design the research portfolio

First map what is known, unknown, disputed, and dependent. Design routes around unknowns that could most change the answer. Separate routes by **reasoning or evidence mechanism**, not by website, keyword, or desired wording.

Possible route families include, but are not limited to:

- definitions, history, and authoritative facts;
- mechanism, causality, and end-to-end system behavior;
- source code, data, experiments, or runtime evidence;
- real adoption, successful cases, and failed cases;
- alternatives, counterexamples, disputes, and applicability limits;
- correspondence between the user's observations and external evidence.

Maintain a lightweight route registry:

| Field | Meaning |
| --- | --- |
| Route family | Distinct mechanism or evidence type |
| Core question | High-value unknown this route must reduce |
| State | active / stalled / blocked / supported / falsified |
| Concrete artifact | Primary source, data, code, experiment, case, counterexample, or model |
| Largest gap | Critical premise still unsupported |
| Reopen condition | New mechanism or evidence that would justify another round |

Merge routes that are substantively identical and redirect capacity toward underexplored mechanisms. A polished reformulation that stops at the same hard premise is not progress.

## Explain the present through time and comparison

For subjects whose current shape may depend on earlier choices, add a historical × current × path-dependence route family to the portfolio. Do not force this route family onto a narrow question where it cannot change the answer.

- **Historical evolution**: establish the starting problem, meaningful turning points, reversals, and constraints. Separate documented chronology from a retrospective story about why the outcome was inevitable.
- **Current comparison**: compare relevant alternatives on aligned dimensions and the same time slice. Normalize definitions, versions, incentives, resources, evaluation settings, and operating conditions before interpreting a difference.
- **Path dependence**: trace which earlier choices locked in or opened later options—such as standards, interfaces, data, capital, regulation, or organizational capability. Distinguish a contingent advantage that persisted from a necessary causal constraint, and ask what evidence would show a different branch was viable.
- **Cross-explanation**: use the historical record to explain present differences, then use current cases and counterexamples to test whether that historical mechanism still matters. Mark documented links, inferences, and disputes separately; do not reduce the result to slogans such as “first mover” or “the market decided.”

Keep the three lenses connected but not interchangeable: chronology supplies candidate mechanisms, comparison tests them against alternatives, and path dependence explains which earlier conditions still constrain the present.

## Orchestrate independent discovery

Keep discovery routes independent during their first pass:

- Give each subagent only the learning contract, its assigned route, allowed inputs, and acceptance criteria.
- Do not reveal the favored explanation, expected conclusion, or findings from other routes.
- Assign only bounded routes that can advance independently and require an auditable research packet.
- Keep subagents read-only and have them return results by message. Do not let them write to the shared source of truth.
- Do not assume subagents inherit this Skill. Pass the route contract and acceptance packet explicitly in each assignment.
- The lead agent must own the integrated model, cross-route relationships, and at least one highest-value gap. Never act as a report concatenator.

Require every route packet to contain:

1. the route and question;
2. consequential claims with direct primary sources;
3. what each source supports and does not support;
4. counterevidence, failures, conflicting sources, and applicability limits;
5. a distinction among confirmed, inferred, disputed, and unknown;
6. the exact point where searching or execution stalled;
7. the precise next action most likely to change the overall judgment.

Reject unsupported status prose, vague optimism, unannotated source lists, and claims such as “the industry generally agrees.”

## Run the claim-evidence loop

Integrate evidence rather than report prose:

1. Extract the claims that could change understanding or a decision.
2. Deduplicate by original provenance. Syndication and repeated agent citations count as one source.
3. Mark each claim as verified, conditional, disputed, insufficient, or false.
4. Check whether definitions, samples, time, region, version, test settings, and operating conditions actually match.
5. Use new evidence to support, refute, constrain, or eliminate explanations.
6. Launch the next round only for the highest-value remaining gap.
7. Reopen a stalled or blocked route only when new data, mechanisms, tools, access, or experiment designs become available.

Prefer official documentation, original papers, source code, primary datasets, regulations, standards, and first-party statements for consequential facts. Use expert analysis for context. Use community material to discover terminology, cases, failure modes, and counterexample leads, but not as sole proof of generality.

## Audit research and search sufficiency

Before closing any round or the whole run, audit coverage rather than counting links or search activity:

- The claim map covers the definitions, mechanism or causes, relevant historical transitions, current alternatives or benchmarks, strongest failure or counterexample, and scope conditions. Omit a dimension only with a stated reason.
- Search uses the vocabulary of the field and its competing explanations, follows important citations back to original sources, and includes a disconfirming route when the claim could change a decision.
- Every high-impact claim has evidence that directly matches its definition, sample, time, region, version, test setting, and operating conditions. Where possible, pair primary evidence with an independent artifact, case, dataset, or execution; label what remains static or unexecuted.
- For technical or product research, verify the real chain separately: documentation claims, source capability, build or configuration, runtime behavior, persistence or delivery, and the target user environment. Automated tests, vendor demos, and isolated success cases do not establish universal behavior.
- Search is not sufficient when results are only snippets or marketing material, all come from one provenance, current claims rely on stale versions, comparisons use incompatible metrics, or a known alternative explanation was never tested.
- Stop only when the stop conditions below are met. If the remaining gap requires new data, access, experiments, execution, or expertise, record that exact blocker instead of searching indefinitely or filling it with fluent inference.

## Apply an independent verification gate

After the leading explanation stabilizes, separate verification from discovery:

- Have a verifier reopen high-impact primary sources rather than trusting agent summaries.
- Attack the strongest current explanation. Check circular support, hidden conditions, common provenance, proxy metrics, selection effects, and causal leaps.
- For implementation claims, inspect code, data, experiments, or the target runtime when possible. Label static inspection and unexecuted claims honestly.
- Classify source conflict as factual, scope, version, or interpretation conflict.
- Preserve unresolved questions as unknowns. Do not fill them with consensus language or fluent prose.

For medical, legal, financial, safety-critical, or publishable academic conclusions, require the appropriate expert, formal standard, real-world data, or peer review. This workflow does not replace professional judgment.

## Build transferable understanding

Do not stop at source summaries. Use the cognitive ladder as an internal coverage gate for each central concept, not as a fixed seven-part output template. The integrated model should cover, as applicable:

- **Definition**: what it is and how it differs from adjacent concepts;
- **Motivation**: what problem requires it;
- **Mechanism**: how inputs, process, outputs, and constraints connect;
- **Example**: how a real case exhibits the mechanism;
- **Counterexample**: where the intuitive explanation fails;
- **Transfer**: how the model predicts or explains a new situation not copied from a source;
- **Boundary**: what remains conditional, disputed, or dependent on expert judgment.

Let the topic determine how these pieces are introduced and combined. Do not expose the ladder as mandatory headings or use route order as the explanation order. If the model cannot explain the mechanism, predict a new case, or name its failure conditions, return to the evidence loop instead of polishing the prose.

## Route the knowledge delivery

When preparing the final pack or checking its quality, read [references/knowledge-pack.md](references/knowledge-pack.md). Infer the delivery profile from the learning contract; do not ask the user to choose one unless the ambiguity would materially change the work:

- **Study Reference** supports learning and upstream writing with a transferable concept model, evidence boundaries, and reusable vocabulary without deciding an article's stance, title, or editorial narrative.
- **Decision Dossier** supports selection or product judgment with aligned options, criteria, conditions, trade-offs, failure modes, and decision-relevant unknowns without making an unsupported choice for the user.

The reference defines how either profile becomes one human-readable canonical Markdown pack, including its compact audit appendix and the Evidence Gate and Reader Gate. It complements this file's research core; it does not replace the learning contract, independent discovery, claim-evidence loop, search sufficiency, or verification requirements above.

## Deliver one canonical knowledge pack

Return or write exactly one self-contained Markdown knowledge pack as the canonical source. Follow the body, appendix, citation, and reader-quality rules in [references/knowledge-pack.md](references/knowledge-pack.md). Respect an upstream project's required destination and format, but keep the pack independent of personal profiles and private project context. Do not retain route reports, chat transcripts, or rejected conclusions as parallel sources of truth, and do not turn the pack into a downstream article.

## Stop on evidence, not activity

Do not use fixed source, agent, round, word, section, or citation counts as quality targets. Stop only when the Evidence Gate and Reader Gate in [references/knowledge-pack.md](references/knowledge-pack.md) both pass, and all of these are true:

- the core question has a scoped answer, or the exact reason it cannot yet be answered is established;
- the central concepts can be explained, distinguished, and transferred to a new case;
- high-impact claims have direct evidence;
- the strongest counterexamples, failure conditions, and competing explanations were tested;
- source conflicts were explained or explicitly preserved;
- another round would add repeated material without changing the knowledge model;
- remaining gaps require new data, experiments, access, or expertise rather than more language inference.

End with the minimum useful closure: what matters for the user's purpose and, when one exists, the highest-value next action. Keep confirmed, inferred, disputed, and unverified states available in the pack's audit appendix without mechanically repeating the entire classification in the conclusion.
