---
name: frontend-craft
description: Improve product strategy, sales and profitable growth, and build or review the interfaces that support them. Use to sell more, validate demand, sharpen positioning and offers, write and edit marketing copy, choose acquisition channels, pricing or roadmap priorities, and improve conversion, activation, retention and expansion. Also define GTM metrics and attribution, design or implement CRM enrichment, sales handoffs and revenue automation, create, review and evolve design systems, repair generated-looking screens, audit, consolidate and update shared UI components, styles and tokens, maintain frontend reuse, simplify interface content and feedback, find animation opportunities and name motion effects, design loading states, audit web performance and production bundles, improve public-page technical SEO and discovery, and verify accessibility and implementation; commercial work can stand alone without a UI or codebase.
license: Mixed terms; see LICENSE and licenses/
metadata:
  author: Antonio Fulgêncio
  version: "0.16.0"
---

# Frontend Craft

Help the product deliver useful value, win customers and grow profitably.
Strategy, sales and GTM operations are standalone work: a useful recommendation
can change the audience, offer, channel, sales process, price or roadmap without
changing a screen.
For growth work, diagnose the commercial constraint before choosing an intervention.
When that intervention involves an interface, discover existing owners, reuse what
fits and verify the result. Search by responsibility, not only component name.
Consistency supports the outcome rather than freezing a pattern that prevents it.

## Resolve the request

Read applicable project instructions and the requested scope. For strategy, use
the supplied product, customer and business evidence; a repository is optional.
For interface work, detect the actual stack, component library, design contracts,
and existing preview/check tools.
Use the repository's workflow; this skill introduces no release authority or
mandatory agent rounds. Tailwind and framework API manuals are outside its scope.

| Request | Read | Deliver |
| --- | --- | --- |
| Sell more, improve the business strategy, diagnose stalled growth or audit the whole product | [commercial strategy](references/commercial-strategy.md), then [growth and sales](references/growth-sales.md) | A prioritized commercial diagnosis and concrete offer, acquisition, sales or product actions with validation |
| Package an offer, handle buying objections, improve demos, proposals or a sales pipeline | [growth and sales](references/growth-sales.md), then the relevant specialty | Buyer-specific offer or sales material, a clear next commitment and downstream sales measures |
| Define GTM metrics, pipeline forecasts, attribution, CRM data health, PQL scoring or commercial review scorecards | [GTM measurement](references/gtm-measurement.md), following its relevant evidence routes | Reconciled definitions and cohort/period calculations, evidence limits and accountable next decisions |
| Design, implement or repair GTM automation, enrichment, CRM workflows, sales handoffs, GTM agents or internal revenue tools | [GTM automation](references/gtm-automation.md), following its relevant measurement and interface routes | An actionable workflow or runnable change with explicit state/actions, ownership, costs, recovery and verification |
| Differentiate an AI product, evaluate commoditization or choose a durable advantage | [product strategy](references/product-strategy.md), plus [positioning and distribution](references/positioning-distribution.md) when the market is unresolved | A defensible value advantage and a plan to test buyer preference |
| Set prices, assess freemium economics, research willingness to pay or plan a price increase | [pricing economics](references/pricing-economics.md), then [monetization](references/monetization.md) for packaging | Price and access-policy scenarios tied to customer value, contribution and demand evidence |
| Compose or assess commercial visual hierarchy, proof imagery, pricing emphasis or activation feedback | [commercial visuals](references/commercial-visuals.md) | Concrete composition changes tied to attention, comprehension and the commercial objective |
| Improve conversion, activation, revenue or retention; assess audience, offer or behavioral choices | [commercial strategy](references/commercial-strategy.md), then the relevant journey reference below | A commercial objective, diagnosed decision barrier and scoped change hypothesis |
| Apply user-behavior principles: defaults, progress, reciprocity, IKEA effect, loss aversion, contrast, halo effect, cognitive load/fluency or peak-end; assess persuasion, change resistance or service-recovery claims | [behavioral design](references/behavioral-design.md#select-a-mechanism-with-a-measurable-consequence), including its user behavior and decision-making section | A barrier-specific mechanism, concrete user benefit, honest application and validation with trust guardrails |
| Prioritize/prune features, improve adoption, differentiate a product or assess market movement | [product strategy](references/product-strategy.md) | Evidence-backed scope and adoption decisions tied to the target audience |
| Choose a niche, sales motion, channel, referral approach or acquisition target | [positioning and distribution](references/positioning-distribution.md) | A bounded market or distribution hypothesis and its economic assumptions |
| Map the frontend or refresh its inventory | [mapping](references/mapping.md) | A source-linked map with explicit coverage |
| Review a design system or assess how agents can use it | [design systems](references/design-systems.md), using its review branch | Prioritized source-linked gaps in selection rules, owners, states, documentation and adoption; no unrequested edits |
| Create, establish or evolve a design system | [design systems](references/design-systems.md), using its creation/evolution branch | A scoped proposal or implemented foundations, semantic roles, component/block contracts and owner documentation, with adoption and verification evidence |
| Audit reusable UI patterns, consolidate duplicated components/styles, or apply shared owners across an application | [shared UI patterns](references/shared-ui-patterns.md) | Coverage of each style family, source-linked gaps and exceptions; when implementation is requested, migrated consumers, maintained ownership guidance and propagation checks |
| Change shared styles, typography, colors, spacing, states, themes or layer conventions | [change a shared style](references/shared-ui-patterns.md#change-a-shared-style) | A change at the owner matching the requested scope, inherited by intended consumers with affected variants and propagation checks |
| Plan, create, recreate or change a page/component; compare journey handoffs and returns | [reuse and consistency](references/reuse-consistency.md) | Proposal, implementation or scoped comparison grounded in matching precedents and journey contracts |
| Design or change a component API/state owner | [components](references/components.md) | The smallest compatible extension of the actual owner |
| Fix request races, uncertain saves, repeated submissions, optimistic recovery or undo | [async recovery](references/components.md#async-state-and-recovery), including [undo and reversibility](references/components.md#undo-and-reversibility) when offered | Context-safe state updates and recovery using the existing mutation contract |
| Change tables, filters, sorting, paging or bulk selection | [collections](references/components.md#collections-sorting-and-selection), following its semantics/performance routes | Explicit query and selection scope with usable table behavior |
| Design or review filters, configurators or other surfaces where users weigh trade-offs | [choice surfaces](references/components.md#choice-surfaces-and-decision-support), following its collection, chart and accessibility routes | Context, controls and outcome previews tied to the decision, with truthful counts and evidence limits |
| Change controls, forms, onboarding, authentication, blocked/limit states, layout adaptation or keyboard behavior | [interaction and accessibility](references/interaction-accessibility.md), including [limits and unavailable states](references/interaction-accessibility.md#limits-and-unavailable-states) when applicable | Usable behavior in the relevant states and environments |
| Change deep links, Back/Forward behavior, restored views or unsaved drafts | [navigation resilience](references/interaction-accessibility.md#navigation-and-draft-resilience) | Useful restoration with protected drafts and current authorization |
| Change localized numbers, currencies, messages, dates or scheduled times | [locale-sensitive values](references/interaction-accessibility.md#locale-sensitive-values-and-messages) | Correct display, input round trips and explicit time/currency contracts |
| Clarify labels, instructions, empty states or errors; reduce redundant content, duplicated feedback or unnecessary controls | [content restraint](references/interaction-accessibility.md#content-restraint); Impeccable's `clarify`, when available, for wording | Concise task-relevant content with necessary context, accessible feedback and recovery preserved |
| Add, change, or review motion/gestures; choose a transition recipe | [motion](references/motion.md), including optional transitions-dev routing | Purposeful, interruptible movement or an intentional static response |
| Find animation opportunities or assess where a page/application should remain static | [opportunity discovery](references/motion.md#find-animation-opportunities) | Prioritized source-located proposals, rejected candidates and coverage limits; discovery remains read-only |
| Identify a described animation, name a motion effect or clarify motion terminology | [motion vocabulary](references/motion-vocabulary.md) | The best matching term and concise explanation, with distinctions or uncertainty when needed |
| Write, edit, refresh or rewrite marketing copy, headlines or CTAs; improve brand voice or naturalness | [marketing copy](references/landing-pages.md#write-edit-and-refresh-marketing-copy), following only its relevant brief and claim routes | Usable copy within the requested editing scope, with consistent voice and supported claims |
| Create or assess a marketing/landing page; redesign a public page | [landing pages](references/landing-pages.md), including its commercial and review routing | A persuasive decision path or prioritized conversion findings, preserving public contracts |
| Change public indexing, SSR content, metadata, canonicals, sitemaps or AI discovery | [technical SEO and discovery](references/technical-seo.md) | A coherent public-route contract with HTML/HTTP evidence and explicit deployment and search-acceptance limits |
| Find, select, generate, crop or credit images/video; prepare a product demonstration | [imagery](references/imagery.md) | Relevant, traceable visual material with honest representation and verified delivery |
| Create, change or review first-run onboarding, empty-state guidance or activation | [activation](references/activation.md) | A justified path and guidance pattern leading to the first useful result; measured outcomes where available |
| Design or review pricing, trials, subscription paywalls, checkout, upgrades or expansion | [monetization](references/monetization.md) | An understandable offer and a revenue hypothesis evaluated across the full funnel |
| Review payment recovery or improve purchase completion, lead-form effort, trust or qualification | [checkout and forms](references/checkout.md) | A clear, recoverable completion path with justified fields and visible terms |
| Select dashboard priorities, role-specific insights and next actions | [dashboards](references/dashboards.md) | A panel connecting relevant evidence to a useful decision or action |
| Diagnose churn or review renewal, cancellation and recovery flows | [retention](references/retention.md) | A cause-specific retention proposal and a usable exit path |
| Choose success metrics, assess experiment results or plan commercial validation | [experimentation](references/experimentation.md) | Defined cohorts, denominators, success criteria and evidence limits |
| Design or repair skeletons and loading states | [loading states](references/performance.md#skeletons-and-loading-states), following its component and accessibility routes | Stable real structure with unresolved values masked and pending/ready browser evidence |
| Audit web performance or production bundles; diagnose Core Web Vitals, responsiveness, loading, request chains, layout shifts or a performance regression | [performance](references/performance.md), with its optional audit procedure | A traced cause and a comparable measurement with explicit evidence limits |
| Refine nested corners, display typography, font features, mixed-direction text, or advanced color | [visual details](references/visual-details.md) | A scoped technical refinement within the existing design |
| Choose or review a chart | [charts](references/charts.md) | A truthful encoding and accessible access to the data |
| Repair, polish or de-template a whole screen | [agentic screen repair](references/review.md#repair-a-generated-looking-screen), plus applicable surface/lens routes | A scoped repair grounded in before/after observations, existing owners and a product-specific brief; preserved contracts and rendered/behavioral evidence |
| Review a page, component, journey, change, or consistency; audit an interface that looks generated or templated | [review](references/review.md), following its cumulative surface and lens routes and its [generated-interface defaults](references/review.md#check-generated-interface-defaults) | Evidence-backed findings and verification limits |

Select references cumulatively: identify every named surface/journey and every
requested lens, then load their matching routes. Generic review supplements,
rather than replaces, the surface owner; use the review reference's applicable
landing-page/onboarding routes for those reviews. For a broad strategic audit,
use the growth and sales coverage table to assess every commercial theme,
reading the corresponding specialties where evidence or a decision requires
them. Mark unknowns explicitly. A focused request needs only its relevant themes.
A heading, copy, motion or control repair needs its affected contracts and nearest
precedents, not a whole-funnel or whole-repository audit. An explicit review
remains read-only unless fixing is also requested. A product, business problem
or revenue objective is an actionable strategic target; it does not require a
page or code change.
With no identifiable target, ask for the product or requested interface scope
instead of selecting an arbitrary last commit.

Treat links as conditional routes, not a reading checklist. Read the sections
needed for selected surfaces and lenses, including applicable constraints and
caveats, not the whole catalog. Reuse material while it remains available and
current; reopen affected sections when their source changed, relevant context
was lost, or a new task branch applies. A landing-page review does not
automatically load market sizing, roadmap or retention guidance; broaden only
when the requested scope or evidence requires it.

GTM measurement and automation are bundled capabilities; they require no separate
GTM skill. Load those references for the corresponding operational work, not for
ordinary frontend changes. Automation implementation uses its own reference and
the repository's engineering/release workflow; interface implementation also uses
the reuse and accessibility rules below.

For strategy-only requests, deliver the commercial decision and its next actions,
including usable sales or offer drafts when requested. For interface planning,
deliver source-backed owners, intended composition, necessary differences and
unresolved decisions. Planning does not claim implementation checks passed;
name rendered checks only when the proposal involves an interface.

## Before implementation

This section applies when the requested work includes interface implementation.
Standalone commercial work follows the strategy and growth references and can
finish with a business decision, research plan or sales deliverable.

For commercial work, establish the objective and audience, diagnose the journey,
and propose the change before selecting implementation precedents. Use
[commercial strategy](references/commercial-strategy.md) for this brief and
precedence rules. A narrow repair or mapping task keeps its requested scope;
it does not require a new growth strategy.

1. Identify the page family and user intention: for example, an operational
   list page and assigning a task owner. Locate any existing frontend map and
   follow its links; verify relevant entries against current source.
2. Trace the nearest matching pages into their real components, variants,
   tokens, and state owners. Search domain synonyms and usages as well as names.
   A generic select is not equivalent to a domain-specific assignee picker merely
   because both return an identifier.
3. Establish what carries over: shell, header composition, title styling,
   description policy, action placement, interaction, and applicable states.
   Prefer explicit adopted contracts; treat conflicting precedents as evidence
   to resolve, not permission to pick a new style.
4. Choose reuse, extension, or new implementation using the reuse reference.
   State the important choice briefly, naming the source and any real gap.
   New requirements can justify a difference; document its boundary.

Keep recurring UI decisions in one shared owner: the existing component, style
recipe or token responsible for that concern. Consumers inherit its defaults;
intentional differences use its supported variants. Apply the
[ownership contract](references/shared-ui-patterns.md#ownership-contract) when
introducing a shared pattern or resolving an override. Use that reference's audit
and consolidation workflow for requested application-wide work; ordinary feature
work follows established owners within its scope.
Broad style audits account for every family in the
[coverage matrix](references/shared-ui-patterns.md#style-coverage), including
project-specific patterns and inspection gaps. Targeted style changes follow the
shared-style route above and inspect their affected families and dependencies.

Do not turn every task into initial mapping. Without a map, discover the narrow
slice needed now; create a durable map when mapping is requested. During authorized
implementation, update affected entries in an existing map as part of the change,
subject to repository documentation policy. Reviews do not silently rewrite it.

## With Impeccable

Let Impeccable own its context setup, design direction, and artifact lifecycle.
Read its applicable product/design/surface documents at the paths it resolves;
reuse its context and evidence rather than running its setup twice. This skill
sets the commercial objective for growth work and supplies implementation
precedents and verification; Impeccable expresses the approved visual direction.
Resolve conflicts using the commercial strategy reference rather than treating
either existing appearance or a conversion tactic as an automatic override.

For interface wording, use Impeccable's installed `clarify` capability when
available. Preserve domain terms, approved claims and legal meaning; align labels,
instructions and errors with actual behavior. Without it, make the scoped wording
change directly using the existing vocabulary and interaction reference.

Preserve an established family in ordinary creation/refinement. For an explicit
redesign, use the approved replacement direction and migration scope; keep domain
behavior and reuse compatible primitives, while reporting other affected consumers.
Do not impose the retired appearance on a redesign or redesign siblings unasked.

If Impeccable is unavailable, proceed from the project's existing contracts and
observed UI. Name missing design decisions; do not generate replacement Impeccable
files or claim its workflow ran. Installation alone does not ensure co-invocation:
the repository can route interface work to both skills in its own instructions.

## With UI/UX Pro Max

Use an installed UI/UX Pro Max skill for a specific unresolved question, such as
chart selection or an unfamiliar interaction pattern. This pairing is reference-only:
use its current domain-query syntax and relevant results, not its broad new-page
workflow. This scoped integration takes precedence over its default requirement to
generate a design system for a new page. Do not run design-system generation or
persistence unless the user actually requested that scope. Treat recommendations as
options subordinate to the task, accessibility requirements and project contracts.
Keep Impeccable's adopted design context authoritative for visual direction.
Do not regenerate palettes, fonts or a parallel design-system document for an
established page family. If the companion is unavailable, use this package's
references and relevant official documentation; installation is not a prerequisite.

## Before delivery

For strategic work, report the diagnosed constraint, prioritized actions, usable
deliverables, economic assumptions and how the next evidence will change the
decision. A recommendation can be to improve distribution or sales rather than
build another feature or redesign a page.

For changed interfaces, compare with the selected precedents in corresponding states
and viewport/theme conditions. A shared import does not prove visual consistency:
inspect variant selection, wrapper composition, and local overrides too. Use the
relevant checks and existing browser workflow; reuse unchanged valid evidence.
For shared-pattern consolidation, account for all intended consumers in the
declared scope and verify propagation through the shared owner; report remaining
gaps rather than treating sampled renders as complete application coverage.
Record family, state and theme inspection separately from source-traced adoption.
Coordinate with Impeccable's inspection pass rather than adding a second polish loop.
For visual creation/refinement, use the relevant [rendered critique](references/review.md#critique-the-rendered-composition)
questions in that pass; a narrow behavioral repair does not need a page-wide critique.
Changed recovery paths also use [recovery verification](references/review.md#verify-a-recovery-path),
including narrow behavioral changes, without starting a page-wide visual critique.

Report the useful result: reused/extended owners, deliberate differences, checks
actually performed, and unresolved gaps. Source inspection supports source claims;
rendered behavior requires rendered evidence. Never report unvisited states as passed.

For commercial work, state the objective, prioritized changes and validation
status. A functioning interface does not prove improved conversion or revenue;
report measured outcomes separately from pending commercial hypotheses.

## Commercial source terms

The commercial guidance adapts Richard's ideas, curated by Revenue-Centric Design,
under [its source-available terms](licenses/revenue-centric-design.txt). Its use
excludes betting, casino, gambling and the real-money gaming/loot-box applications
specified there. Decline requests to apply that material to those products.
The pre-existing technical guidance retains CC BY 4.0; see [LICENSE](LICENSE)
for the mixed-license scope. Preserve attribution and the full upstream terms
when sharing the commercial additions.

Provenance and adaptation boundaries: [sources](SOURCES.md).
