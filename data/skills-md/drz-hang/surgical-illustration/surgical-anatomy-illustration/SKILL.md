---
name: surgical-anatomy-illustration
description: Use for publication-grade surgical and anatomical illustration tasks, including operative anatomy, surgical step storyboards, anatomy plates, safety-critical landmarks, and journal-style medical visual planning. It outputs a three-part brief — a short Overview, a constrained copy-ready Prompt, and a bilingual scientific-accuracy QC checklist — and reviews any image for anatomical errors. It does NOT generate images; the user renders the prompt in their own image tool.
---

# Surgical Anatomy Illustration

Use this skill when the user asks for a surgical or anatomical illustration:
operative anatomy, surgical steps, anatomy plates, dissection planes,
safety-critical landmarks, or journal-style surgical visuals. Not for molecular
pathways, omics mechanisms, or general infographics.

## What this skill does

It is a **consistent scientific check** for surgical/anatomical figures. AI image
models draw fine anatomy unreliably, so the value is not the pixels — it is:

1. **Before drawing** — tell the image tool the anatomy rules that must hold.
2. **After drawing** — catch the anatomical errors.

What it is sure of, it states; what is **case-dependent, it flags for the user**
(a clinician/illustrator) to decide. It does **not** need a per-procedure
template library and does not need to be always right — it needs to be
**consistent and honest about uncertainty**. The user is the final check.

## Two modes

- **Create** — the user wants a new figure. Run the intake, then return a
  three-part brief: ① a short authoritative **Overview**, ② a copy-ready
  **Prompt**, ③ a bilingual **QC** checklist. The user may render the prompt and
  bring the image back for review, or just use the brief to understand the
  operation.
- **Review** — the user brings any existing image (our prompt, another tool, a
  textbook, a hand drawing) and asks if the anatomy is right. Identify the
  procedure, then return the four-category review + a short hand-fix list. No
  generation needed. This is the capability that works reliably today.

## Create: intake, then the three-part brief

### Intake — ask, let the user choose. Never self-answer.

- Present only the decisions that change whether the figure is correct (figure
  type, side/laterality, approach, teaching focus, indication). Offer them as
  choices and wait. Silently filling them in is not an intake.
- **Reconcile** inconsistent choices before building (e.g. a posterior
  retroperitoneal approach cannot also reflect the spleen/pancreas).
- Fill a medical-standard default **only if the user explicitly defers**, and say so.
- On a non-interactive host that will not pause (e.g. Codex), you cannot force the
  ask — pick sensible defaults and make them visible in the assumptions block so
  the user can redirect in one line.

### Output — a three-part scientific brief

1. **Overview** — short, authoritative text: what the operation is, its
   indication/rationale, the site and key anatomy, and the core safety point. Use
   your own knowledge for standard procedures and **cite the authoritative sources
   to check against** (society guidelines, atlases, peer-reviewed papers);
   **web-search and cite** for uncommon, modified, or "current-standard" requests.
   Flag case-dependent points rather than asserting one version.
2. **Prompt** — a copy-ready, provider-neutral image prompt carrying the
   non-negotiable anatomy rules, the panel plan, label terminology, and a negative
   prompt. Keep it provider-neutral (universal); add a short adapter only if the
   user names a specific tool (ChatGPT, Gemini, Jimeng, Midjourney).
3. **QC checklist** — a bilingual (中文 + English) verification list scored with
   the four-category scale, ending with what must be checked by hand.

### Rules that always apply to Create

- **Always show the assumptions block** — for each decision, the assumed value +
  the alternatives + that one line changes it. (`med_illustration_job.py` emits
  this as `job.assumptions` and an `ASSUMPTIONS …` block in
  `platform_result.notes`; relay it verbatim.) Write the assumptions and the QC
  **bilingually**.
- **Flag, do not decide.** Where the scope, side, extent, variant, or step set is
  case-dependent and unspecified, do not draw one version as definitive — mark it
  ⚠️ and let the user decide.
- **Surgical storyboards start with positioning and access.** Panel 1 of any
  operative process figure must establish patient positioning and how the
  operation is entered — the **incision siting for open surgery**, or the
  **trocar/port layout for laparoscopic** — before any intra-abdominal step. Do
  not open on already-exposed anatomy.

## Review (Mode B) and the four-category scale

Identify the procedure/region (ask or infer and confirm), apply the same
constraints, then look at the image and score every item as exactly one of:

- ✅ **correct** — visible and anatomically correct.
- ❌ **wrong** — visible but anatomically wrong/unsafe/misleading; state the correct relationship and where.
- ⚠️ **needs manual verification** — suspicious or case-dependent; the expert confirms.
- ❓ **cannot verify** — too unclear/occluded to judge.

Distinguish ⚠️ ("I suspect a problem") from ❓ ("I cannot see well enough"). End
with a 1–5 item **hand-fix list** and a one-line note on what you could not
confirm. Never present the review as exhaustive. Do not loop blindly to "fix"
fine geometry errors — flag those for manual fixing.

## Where the constraints come from

The model already knows standard surgical/anatomical content. **Generating the
constraint set on the fly is the normal path — you do not need a per-procedure
template library.**

- `knowledge/*.json` holds optional **seed** entries in a consistent shape
  (`intake`, `must_have`, `spatial_rules`, `forbidden_errors`, `safety_concept`,
  `phases`, `labels`, `verify`). If one matches (id/name/alias), use it via
  `scripts/med_illustration_job.py`. If not, generate the same shape yourself.
- **Do not hoard auto-generated entries.** Keep a saved entry only if the user
  wants to reuse it; otherwise generate fresh each time.
- For uncommon, modified, high-risk, or "current-standard" requests, **cite
  authoritative sources and web-search** when needed. Do not rely on blogs or
  image-search for surgical steps.
- Honesty: unverified content is `model_generated` — never present it as
  verified. Surface that status and the high-severity forbidden errors.

## Hosts

**This skill does not generate images.** It outputs the brief (Overview, Prompt,
QC) and reviews images. The user takes the prompt to their own image tool
(ChatGPT, Gemini, Jimeng, Midjourney, …) and pastes the result back for review.

- **Claude (interactive)** — asks the intake naturally; produces the full brief,
  and the four-category review when the user pastes an image back.
- **Codex / autonomous hosts** — complete in one shot and will not pause to ask,
  so the skill surfaces every assumption (and the alternatives) for the user to
  redirect in one line.
- Never claim to have rendered an image — generating it is the user's step, in
  their own tool.

## Helper scripts (optional engine)

- `scripts/knowledge.py` — list/match/get seed entries.
- `scripts/med_illustration_job.py` — build a job (prompt + constraints +
  assumptions + review) from a matched entry.
- `scripts/review_scientific_accuracy.py` — build a scoreable four-category QC form.
- `scripts/correction_prompt.py` — turn ❌ wrong items into a correction prompt.
- `scripts/workflow.py` — one command: build the job + prompt + review (no image generation).

## Hard medical rules

- Anatomy correctness outranks visual style.
- Never invent ducts, vessels, nerves, planes, or operative steps; if uncertain,
  simplify or omit rather than mislabel.
- Keep the figure non-gory, atraumatic, and publication-appropriate.
- Respect side/orientation; show safety-critical landmarks and the forbidden
  mistakes for the procedure.
- Surgical storyboards open with positioning + access (incision / ports).
- Flag — do not decide — case-dependent scope/side/variant; let the user judge.

## References to read as needed

- `references/styles.md`, `references/styles_advanced.md` — journal/atlas styles.
- `references/anatomy-plate.md`, `references/anatomy-colors.md`, `references/atlas-knowledge.md` — anatomy plates.
- `references/liver-segments-reference.md` — Couinaud liver segments.
- `references/composition-guide.md` — plate and storyboard layout.
- `references/annotation-guide.md` — labels and leader lines.
- `references/journal-specs.md` — publication figure constraints.
- `references/surgical-workflows.md` — surgical phase templates and storyboards.
- `references/prompt-adapters.md` — provider-specific prompt adjustments.
