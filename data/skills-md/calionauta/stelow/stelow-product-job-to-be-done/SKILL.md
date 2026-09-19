---
name: stelow-product-job-to-be-done
description: >
  [stelow] Complete set of specialized prompts for Jobs To Be Done (JTBD) analysis and discovery,
  based on the methodology by calionauta. Use this skill whenever the user wants
  to perform any kind of JTBD analysis: contextual market segmentation, thinking styles
  (Indi Young), JTBD discovery, competitor mapping, job actors, situational variables,
  job map steps, functional needs (desired outcomes), financial needs, or emotional/social
  jobs. Contains 10 professional prompts ready to run with AI agents. Trigger whenever the
  user mentions: jobs to be done, JTBD, contextual segmentation, thinking styles, Indi Young,
  job map, job steps, desired outcomes, user needs, JTBD competitors, job actors, situational
  variables, emotional jobs, social jobs, or any combination of these terms.
metadata:
  frequency: monthly
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
---

# Jobs To Be Done — Complete Skill

This skill contains **10 specialized prompts** for conducting comprehensive Jobs To Be Done analyses.
Each prompt corresponds to a specific step or dimension of the JTBD methodology.

---

## Prompt Map — When to Use Each

| # | Prompt | When to use |
|---|--------|-------------|
| 1 | **Contextual Segmentation** | Create market segments based on situational factors (not demographics) |
| 2 | **Thinking Styles (Indi Young)** | Identify significantly different thinking patterns of a performer toward a purpose |
| 3 | **JTBD Discovery** | Discover and reframe Jobs from a solution, action, or outcome |
| 4 | **Competitor Discovery** | Map direct, indirect, and hidden competitors through the JTBD lens |
| 5 | **Job Actors** | Identify all actors involved in the job and market |
| 6 | **Situational Variables** | Discover factors and variables that impact job execution |
| 7 | **Functional Needs** | Discover functional success criteria (desired outcomes) |
| 8 | **Financial Needs** | Discover financial success criteria for solution acquisition |
| 9 | **Emotional & Social Jobs** | Discover emotional and social jobs related to the functional job |
| 10 | **Job Map Steps** | Map the stages and steps of the job to build a Job Map |

---

## Recommended Flow

For a complete JTBD analysis, follow this logical sequence:

```
1. Contextual Segmentation      → define the market
   ↓
2. Thinking Styles              → segment by cognition/behavior
   ↓
3. JTBD Discovery               → define the jobs
   ↓
4. Job Actors                   → identify who is involved
   ↓
5. Situational Variables        → understand the context
   ↓
6. Job Map Steps                → map the journey
   ↓
7. Functional Needs             → success criteria
   ↓
8. Financial Needs              → financial criteria
   ↓
9. Emotional & Social Jobs      → human dimension
   ↓
10. Competitor Discovery        → who else solves the job
```

---

## Interaction Tool Guidelines

**IMPORTANT**: When the user needs to choose between predefined options, ALWAYS ask through the portable ask contract (`../stelow-workflow-orchestrator/references/cli-tools/ask.md` — host-native question tool, else `stelow ask`, else enumerated text) with enumerated format:
- Options with short `label` and `description`
- Examples: prompt selection (1-10), analysis type, next steps, etc.

---

## General Instructions for the Agent

- **Ask which prompt the user wants to run** (unless already clear from context) — offer three modes: **Full Mapping** (run all ten prompts sequentially), **Targeted** (exactly one prompt), or **Recommend** (agent picks from context):
  - Use the portable ask contract with options 1-10 for the 10 JTBD prompts
  - Always include option: "I want you to recommend based on context" (in the user's language)
  - Fallback: "Which JTBD analysis do you want to perform? (1-10, or 'recommend based on context')"
- **Fill in the variables** indicated by `[brackets]` or `{{braces}}` with the information provided by the user before executing the prompt.
- **Chain prompts sequentially** when the user wants a full analysis — the output of one prompt feeds into the next (e.g., Situational Variables → Functional Needs).
- **Language of output**: The prompts are written in English (instructions to the LLM), but results should be delivered in the language used by the user.
- Read the appropriate file from `references/` before executing a prompt.

---

## Research Mode (current or niche context)

JTBD is grounded first in the user's context and in interviews. The LLM and
external research can generate useful candidates — they do not invent evidence
about people or replace validation.

Use the shared web-research contract (`../stelow-workflow-orchestrator/references/cli-tools/web-research.md`)
when current or niche-specific material can help discover or test candidates:

- language people use for a struggle, workaround, or desired progress;
- possible Jobs, situational variables, Job Map steps, and desired outcomes;
- named competitors or alternatives, a changing category, or an emerging
  practice; and
- a score that relies on the current solution landscape.

Use host-native search and primary sources to establish what exists and what
has changed. Add `last30days` when recent launches, practitioner discussion,
or a current niche signal could change the candidate set or its priority. It
complements primary evidence; a frequent discussion or launch is never proof
of a Job, a struggle, prevalence, or causal relationship.

### Hypothesis and Bet Discipline

When research contributes to a JTBD output, call it a **draft guide**, not a
market finding. Mark each research-led Job, step, desired outcome, or ranking
as a **hypothesis**. Prioritize hypotheses as **bets** using the decision
context, fit with the supplied evidence, source coverage, and recency — not as
a scientific measurement of demand or truth.

For a prioritized research-led bet, record:

- **Bet:** the candidate Job, step, outcome, or segment;
- **Why now:** the supplied context and signals that made it worth exploring;
- **Evidence, origin, and bias:** whether it is user-provided input, external
  research, or a simulation; source types, gaps, recency, and whose
  perspective is overrepresented or missing;
- **Confidence:** directional only (low, medium, or high), never a statistical
  claim; and
- **Next validation:** the cheapest interview, observation, or behavioral-data
  check that could disconfirm it.

### Source and Status for Evidence

User-provided interviews and research are first-class inputs. Use them when
they support the analysis, and make their origin clear without inventing a
sample size, method, or representativeness. Use one of these statuses wherever
an insight, example, or voice depends on supplied material:

- **Input-derived — direct quote:** exact wording present in the material the
  user supplied; preserve its meaning and do not add a participant identity.
- **Input-derived — paraphrase:** a faithful restatement of one supplied
  account; do not put it in quotation marks.
- **Input-derived — synthesis:** a pattern drawn from multiple supplied
  interviews or research artifacts; state the supplied scope and limitations.
- **Simulated hypothesis — not participant data:** a plausible invented
  example used to make a candidate concrete, never evidence about a group.

This provenance discipline applies to every JTBD prompt. Only call a finding
validated when the supplied material actually supports it; otherwise preserve
it as a hypothesis or bet. Keep participant information anonymized and avoid
repeating unnecessary sensitive details.

### Required Research Appendix

When research contributed to the output, append this section after the native
prompt output. Do not add an empty appendix when no research was used.

```markdown
## Research-led Draft Bets

> Directional guide, not a market measurement or validated JTBD finding.

### Bet: [candidate Job, step, outcome, segment, or alternative]
- **Why now:** [decision context and signals]
- **Evidence, origin, and bias:** [user-provided input, external sources, or simulation; recency, coverage gaps, and missing or overrepresented perspectives]
- **Confidence:** [low | medium | high — directional only]
- **Next validation:** [the cheapest interview, observation, or behavioral-data check that could disconfirm it]
```

Interviews and user-provided behavioral evidence establish why people hire,
switch, or struggle. Record coverage limitations and do not fabricate findings
when research is unavailable.

---

## References

The 10 complete prompts are located in:
- `references/01-contextual-segmentation.md`
- `references/02-thinking-styles.md`
- `references/03-jtbd-discovery.md`
- `references/04-competitors.md`
- `references/05-job-actors.md`
- `references/06-situational-variables.md`
- `references/07-functional-needs.md`
- `references/08-financial-needs.md`
- `references/09-emotional-social-jobs.md`
- `references/10-job-map-steps.md`

Read the specific prompt file before executing it.

---

## Attribution

This skill and all its prompts were developed by **calionauta** 🇧🇷 — product strategist and JTBD practitioner from Brazil.

These prompts are the result of years of experimentation and refinement, documented and shared through:

- 📚 **E-book**: [Jobs To Be Done in Portuguese](https://calionauta.substack.com/p/e-book-jobs-to-be-done-em-portugues) — comprehensive guide to JTBD methodology
- 🔗 **Resources**: [Recursos Principais](https://calionauta.substack.com/p/recursos-principais) — collection of prompts, frameworks, and tools
- ✍️ **Substack**: Regular articles and experiments on JTBD, product strategy, and innovation

The prompts in this skill represent a curated, production-ready selection of the most effective JTBD analyses developed through extensive real-world application.

## Examples

### Example: why users hire a note app

**Input:** "Users say they love us but keep churning. Why?"

**Steps:**
1. Run a JTBD interview (past-tense, struggle-first, no feature questions).
2. Extract the job (e.g. "feel in control Monday morning").
3. Map competing hires (spreadsheets, memory, nothing).

**Output:** Job statement + forces diagram + what the product must do to win the hire.

## Edge Cases

### Interviewee talks features
- Redirect to the last time they struggled; features are solutions, not jobs.
### Multiple jobs surface
- Rank by struggle intensity; design for the strongest, note the rest.
### Job is emotional, not functional
- Keep it: progress has functional, emotional, and social dimensions.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : context
description    : Strategic context. Market analysis, JTBD, domain detection. Gated by `context:5` (appetite/review mode): Product Spec Ga
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : shape
gate           : none
rework-on      : setup
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **context** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Strategic context. Market analysis, JTBD, domain detection. Gated by `context:5` (appetite/review mode): Product Spec Gate+Auto skips; others use reduced ask. S

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.
