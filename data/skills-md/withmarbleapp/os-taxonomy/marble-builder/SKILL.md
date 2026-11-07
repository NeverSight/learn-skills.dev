---
name: marble-builder
description: Design a learning experience for a child with the user, ground it in os-taxonomy and teaching research, then build and validate a standalone HTML experience. Use for creating or revising child-facing learning activities, rather than general curriculum lookup.
---

# Marble Builder

Turn a user-confirmed learning goal into an educationally sound, standalone HTML
experience through a short design conversation. Use this repository's topics,
prerequisites and teaching research; develop targeted research when it is missing
or insufficient. Design the interaction and its assessment together, then render,
inspect and revise the experience in a browser. A working HTML file is an initial
prototype, not sufficient evidence of a good learning experience.

## Establish just enough context

Use information already available in the conversation. Before designing, obtain:

- The child's age, if unknown. Do not require a name, birthday or other identifiers.
- A clear learning goal provided or confirmed by the user. Help turn a broad
  request such as “fractions” into an observable goal, without silently choosing
  the goal for them.

Ask only additional questions whose answers would materially change the design.
Prior knowledge, reading independence, access needs, interests, available time,
adult support and device may matter; they are not a mandatory questionnaire.
Bundle necessary questions into one short turn. For other details, make reasonable
assumptions and disclose the consequential ones in the concept. Do not infer
mastery or reading ability from age alone. A brief entry task can help calibrate
prerequisites when the adult does not know the child's starting point.

When the request already implies an observable goal, propose that goal and the
concrete concept in the same turn, ending with one confirmation question covering
both. Ground this provisional goal as described below before presenting it; do
not require a separate goal-approval round trip. If the goal is genuinely unclear,
clarify it first. Full implementation still waits for concept confirmation.

## Language and locale

Use the child's language for all child-facing copy: the cover question,
instructions, feedback, buttons, accessible names and vocabulary definitions.
Use it for the adult note too, unless another language is explicitly requested.
Set `<html lang>` to the appropriate language tag. Apply that locale's casing
and typography while preserving the sentence-case house style. For French,
keep punctuation attached with non-breaking spaces: a narrow no-break space
(U+202F) before `; ? !`, and a no-break space before `:` (narrow where the chosen
locale/style calls for it). Check wrapping at narrow widths; punctuation must
not wrap alone. Configure the shared helpers as shown in
[examples.md](references/examples.md#localising-the-shared-helpers).

## Ground the design

Read [data-and-research.md](references/data-and-research.md) to locate this
repository's data, join topic research and interpret its limitations. Select a
small scope matched to the confirmed goal (or the clearly implied goal being
proposed alongside the concept), using topic evidence and prerequisite
edges to identify the intended outcome and likely starting requirements. Age
bands guide selection; they do not override known readiness.

Use existing pedagogy, activity guidance, constraints, misconceptions, assessment
and sources to inform the experience. Check that they fit this goal and child;
resolve contradictions and verify consequential factual claims. Existing
activities are proposals to adapt, not a script or evidence of effectiveness.
Do not display publication omission markers as instructional content.

For a missing or inadequate research record, prepare a focused teaching brief:

- The learning objective and prerequisites.
- Suitable representations, instructional approach and scaffold progression.
- Likely misconceptions, feedback and a plan to assess independent understanding.
- Supporting sources and important uncertainty, distinguishing findings from
  your own proposed design.

Use available web/research tools to inspect relevant primary research, evidence
syntheses or authoritative teaching guidance. Record what each source actually
supports; a curriculum standard establishes alignment rather than efficacy.
Never invent references or imply that an unread source was checked. If source
access is unavailable, disclose it and label the brief provisional; ask about
alternatives only if that limitation prevents a sound design. Keep personal child
context out of research queries and reusable research artifacts.

When this new research would help an existing taxonomy topic, suggest an optional
os-taxonomy contribution. Follow the contribution guidance in the reference only
if the user wants to pursue it. Continue the learning experience independently.
Creating an experience does not authorize publishing research or child context.

## Develop the concept with the user

Read [interaction-design.md](references/interaction-design.md) and
[visual-design.md](references/visual-design.md) before proposing the concept. Design what the child will see
and do, and what that action will reveal about understanding. Use the
[example index](references/examples.md) to select a relevant example: read its
short design note and inspect its key-state screenshots before proposing the
concept. After approval, run the example and inspect relevant readable source
when adapting its interaction. Examples illustrate specific decisions and carry
annotated limits; current skill rules take precedence. Do not copy every example
or force its sequence onto a different goal. Before building the full HTML,
present a compact, concrete proposal containing:

- The observable learning goal and selected topic(s).
- The central question and richly illustrated opening, followed by the central
  visual/interactive activity, with an example interaction or short screen sequence. Explain the representation choice, viewpoint and controls;
  check that they preserve the relationships the child needs to understand.
- How the activity teaches the idea, including the important research basis and
  any significant uncertainty.
- The flow: guided sequence, branching investigations, open exploration or a
  combination. Explain meaningful choices, prerequisites and how learners can
  return to unfinished work; do not default to a fixed sequence of screens.
- How support will be introduced, adjusted and faded.
- An independent task the interface can assess: the child's action, the observable
  response, the scoring rule and a plausible misconception it distinguishes.
  Prefer a prediction on a fresh transfer problem when it fits the goal. Explain
  what changes from practice and how the answer stays hidden until commitment.
- Expected duration, device/adult-support assumptions and optional extension.

Invite refinement and wait for the user to confirm the direction before full
implementation. This concept checkpoint is required by this workflow; do not
one-shot a completed experience from the initial request. If the user already
provided an approved concept, validate any missing essentials without repeating
an approval ceremony. A small sketch may help the decision, but is not the full
experience. After agreement, make routine implementation decisions autonomously.

## Optional connected LLM mode

Default to local, deterministic interactions. Consider runtime LLM calls only when
achieving the learning goal requires open-ended reasoning or text production
that local rules, simulation or prepared content cannot adequately provide. Do
not add an LLM just for conversational decoration, generic hints, personalization
or grading answers the browser can already check. Using an LLM to author the
experience does not justify LLM calls while the child uses it.

If this condition applies, read [llm-connected-experiences.md](references/llm-connected-experiences.md).
During concept design, explain the essential learning role, connection/provider,
data sent, account usage/cost and loss of offline operation. Obtain **explicit
approval from the experience's author before including runtime LLM calls**.
General concept approval or approval to update this skill is not permission for
this capability. An explicit request that already approves these terms counts;
do not repeat approval. Without it, continue with an agreed local alternative or
explain which part of the goal cannot be met locally. Never silently substitute
a narrower task and claim it assesses the original goal.

## Build the experience

By default, deliver one HTML file with embedded CSS, JavaScript and required
assets that opens directly in a browser without accounts, a build step, a server
or network access. Author-approved connected LLM mode is the narrow exception:
keep the experience UI and assets self-contained, and disclose the required
connection service, parent authentication and network access. Do not call that
mode offline or promise that HTML alone supplies the connection. Keep any
research/design companion outside the child-facing flow. Use local interactions
and no tracking or transmission of child responses by default.
Use the bundled **Baloo 2** throughout with the Marble component
baseline: small sentence-case titles at 500, prominent explanations at
550, and icon-plus-label buttons at 500. Read the exact roles and usage in
[component-styling.md](references/component-styling.md). Embed the actual font
bytes; font substitutions or fallbacks require an explicit project-level
exception to the house style. Keep instructions and button labels in sentence case.
Use Three.js for spatial experiences involving viewpoint, illumination, depth,
occlusion or moving physical objects, including the daytime-Moon example. Build
one coherent, polished 3D scene with direct manipulation: drag the Earth, place an
observer, or select a prediction in the scene. All 3D uses a crafted cel-shaded
look: flat color, deliberate stepped light/shadow bands and clean black outlines.
Visual simulations must be beautiful, crafted and polished as well as functional;
a working model with placeholder art is not a finished experience.
Do not substitute flat comparison
panels and external step buttons for spatial interaction. Use 2D for goals whose
reasoning is genuinely two-dimensional, such as fraction bars or sentence work.
Follow [visual-design.md](references/visual-design.md) for Marble-derived fonts,
colors, tactile controls, scene composition and the standalone Three.js workflow.
Respect explicit user constraints.

Choose a coherent learning flow rather than defaulting to a linear sequence.
Use guided steps where prerequisites matter; offer selectable investigations,
revisiting and open exploration where these serve the goal. A clear next action
can be a meaningful choice. For dynamic simulations, read
[simulation-design.md](references/simulation-design.md).

Design the experience around these principles:

- Begin every experience with a **richly illustrated title screen that poses the
  central question** in child-friendly language. Make the question the large,
  primary heading and compose it with crafted artwork specific to the experience.
  Show one clear icon-plus-label start action, such as “Let’s find out”. No
  introductory paragraphs, objectives list or lesson controls. The large question
  is an intentional opening-screen exception to the small-title lesson baseline;
  use the selected Baloo 2, sentence case and established button styling.
  After entry, switch to the lesson's small title and single prominent instruction.
  Keep the cover outside assessment: opening it, waiting or starting earns no
  credit, and its imagery must not reveal a fresh independent task's answer.
  Restart returns to the opening with fresh response/support evidence. See
  [visual-design.md](references/visual-design.md) for composition and behavior.
- Start with an approachable task and a clear purpose. Teach the idea through
  meaningful actions or representations, not decoration around a quiz.
- Let the child learn through looking, acting, predicting and seeing consequences.
  During the lesson, keep the title small, sentence case and anchored at the top left; keep instructions
  and button labels in sentence case.
  Make the current instruction
  or short explanation large, prominent and part of the experience's composition;
  it is the main text, not a caption beneath a dominant heading.
  During the lesson, show only **one title and one short instruction
  at a time**. Use that same instruction slot for feedback; replace it rather than
  appending explanation. No subtitles, legends, visible object labels, status
  paragraphs or textual tabs. Buttons should combine an icon with a concise
  visible action label; these functional labels are allowed alongside the title
  and instruction. Reserve icon-only buttons for a good reason, such as a small
  action bar or an unmistakable scene affordance, and give them accessible names.
  Do not turn button labels into additional instructions or explanations.
  Keep adult notes and credits in
  a separate companion. For a goal that genuinely requires visible reading
  material or mathematical notation, resolve that conflict explicitly with the user during concept design
  rather than silently relaxing this rule.
- Give every child-facing technical term a **dashed underline and an on-demand
  meaning**, including terms in the opening question, instructions, feedback,
  non-interactive labels and extensions. **Never add definition underlines or
  triggers inside buttons or other action controls, including their labels.**
  Keep the whole control available for its action on click, tap and keyboard
  activation. Explain unfamiliar control vocabulary in the instruction or other
  non-interactive lesson text instead. Examples include photon, nitrogen, molecule,
  horizon and volume. Hover on desktop or tap on mobile reveals a brief,
  age-appropriate explanation; keyboard focus/activation must also work.
  Keep definitions contextual and generic, without revealing the current answer.
  Show only one definition at a time, dismissible by close, Escape or tapping
  elsewhere. This requested word-help popover is a narrow exception to the text
  budget, not another persistent explanation panel. See
  [interaction-design.md](references/interaction-design.md) for behavior and
  assessment boundaries.
- Make feedback visual first: reveal the relevant consequence or relationship,
  connect errors to likely misconceptions and offer a useful retry. A short
  replacement instruction can direct attention; do not add a feedback card.
- Offer support when needed, then fade it toward independent practice. Avoid
  overwhelming reading demands or requiring an adult unless agreed.
- Separate supported practice from the independent mastery check. Choose evidence
  suited to the goal: explanation, construction, performance or interpretation
  may reveal more than recognition alone.
- Define success using the concept's agreed evidence; no universal percentage or
  item count. Completion, hinted answers and repeated guessing do not by
  themselves demonstrate mastery. Build assessable actions into the core UI;
  design around an observable response rather than defaulting to “ask a parent
  to judge.” If the goal requires evidence the browser genuinely cannot assess,
  propose a suitable alternative or explicitly agree adult assessment during
  concept design. Never claim to assess the whole goal from a narrower proxy.
- When evidence is insufficient, replace the current instruction with “needs more
  practice” or “not yet checked” and offer targeted support through the scene;
  never add a separate result/status label. Describe the result as evidence from this session,
  rather than a lasting diagnosis or proof of retained mastery.
- Include optional “going further” content that deepens or transfers the idea;
  it must not be required to finish the core goal.

Provide basic keyboard operation, readable contrast, responsive layout and
non-colour-only feedback. Offer a practical alternative to any essential
interaction that requires precise dragging, sound or similar capabilities.
Keep progress, hints, retries and restart behavior understandable using scene
state, icons and non-text progress marks. Put source acknowledgements and required
attribution in the separate adult companion and retain embedded asset license
notices in the HTML source; follow the repository's README and provenance notices
for reused material. Do not turn the learning canvas into a branded webpage.

## Validate and hand over

Use [validation.md](references/validation.md) during development, starting with
the central interaction before polishing the rest. Render in a browser, inspect
screenshots and exercise controls, revise the design, then render and check the
revision. Assess visual clarity and teaching behavior as well as correct code;
a screenshot captured but not inspected is not a UX review. Compare the rendered
composition with the Water Lab reference and the explicit visual acceptance
criteria; “it loads” is not a polish pass. Use browser tools
available in the environment, without requiring a particular automation stack.
If browser access is unavailable, report the artifact as a prototype awaiting
browser validation rather than presenting the UX as validated. Automated checks
cannot establish effectiveness for a particular child.

Deliver the HTML and a short adult-facing note covering the goal, topic IDs,
prerequisites/assumptions, research used or newly developed, mastery evidence,
optional extension and any remaining limitations. Include a way to open the file
and summarize what was actually tested. Do not claim browser or child testing
that did not happen. Invite observations from actual use to guide the next
revision; do not turn that invitation into a required extra questionnaire.
