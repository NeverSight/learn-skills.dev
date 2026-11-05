---
name: shredding-solicitations
description: Shreds a US Federal solicitation into a requirements and compliance matrix. Use when the user needs to shred or analyze an RFP, RFQ, RFI, or task order, build a compliance matrix or requirements matrix, extract shall statements, or cross-walk Section L instructions, Section M evaluation factors, and the Section C/SOW/PWS/SOO requirements. Produces a numbered compliance matrix that maps every requirement to the proposal location that will address it, plus a register of format and submission rules.
---

# Shredding Solicitations

Take a federal solicitation apart, requirement by requirement, and build the
compliance matrix — the table that maps every requirement to the proposal
location that answers it. The compliance matrix is the spine of a compliant
proposal. Every later proposal skill works against it. A requirement that is not
in the matrix is a requirement the proposal will miss, and a missed material
requirement is a deficiency.

## When to use this skill

Use this skill as the first proposal-development step after the RFP releases (or
on a draft RFP, to get a head start). It precedes outlining, drafting, and every
volume-specific skill.

It does not build the proposal outline — that is `outlining-proposals`, which
consumes this matrix. This skill produces the requirements inventory; the
outline turns it into a document structure.

## Inputs

**Required:** the solicitation itself — at minimum Sections L, M, and C (or the
SOW/PWS/SOO and the instructions/evaluation equivalents). Place the document in
the pursuit workspace `source/` directory. Include all amendments and the Q&A.

**Preferred upstream artifacts:**
- `00-opportunity-profile.md`: orienting context.
- `05-win-strategy.md`: lets the matrix flag where themes will be threaded.

**Without the win strategy**, the matrix is still complete; it simply omits the
theme-placement column.

Read `../../shared/federal-solicitation-primer.md`,
`../../shared/glossary.md`, and `../../shared/pursuit-workspace.md` if not
already read this session. The primer's "proposal triad" guidance governs this
skill.

## Intake

Ask these as a numbered list. Skip what the solicitation itself answers.

1. **The document set.** Is the full solicitation available — Sections L and M,
   the SOW/PWS/SOO, Section H, attachments, all amendments, and the Q&A? What is
   missing?
2. **Document structure.** Does the solicitation use the standard Uniform
   Contract Format, or a compressed task-order/commercial format? Where are the
   instructions, the evaluation factors, and the requirement located?
3. **Volumes.** Does Section L define the proposal volumes and their separation
   (e.g., Technical, Management, Past Performance, Cost)? What are they?
4. **Amendments.** Have all amendments been incorporated? Did any amendment
   change Section L, Section M, the requirement, or the due date?
5. **Win strategy.** Is there a `05-win-strategy.md` to cross-reference for theme
   placement?

If the document set is incomplete, shred what is available and list precisely
what is missing — an incomplete shred is dangerous if it is mistaken for a
complete one.

## Workflow

```
Solicitation Shred:
- [ ] Step 1: Read the primer's triad guidance; complete intake
- [ ] Step 2: Identify the governing sections and the volume structure
- [ ] Step 3: Extract Section L instruction requirements
- [ ] Step 4: Extract Section M evaluation requirements
- [ ] Step 5: Extract Section C / SOW / PWS / SOO requirements
- [ ] Step 6: Cross-walk L <-> M <-> C; flag conflicts and gaps
- [ ] Step 7: Extract format, page, and submission rules
- [ ] Step 8: Write the compliance matrix (10-compliance-matrix.md) and validate
```

**Step 1: Triad and intake.** Re-read the primer's "read M, then L, then C"
guidance. Run intake.

**Step 2: Governing sections and volumes.** Locate the instructions, the
evaluation factors, and the requirement, by function (the primer explains how
when the format is non-standard). Record the volume structure from Section L —
it is the top level of the matrix.

**Step 3: Section L requirements.** Extract every instruction: what each volume
must contain, in what order, what each section must address. Use the requirement
extraction method in `references/shredding-method.md` — capture every
directive ("shall", "must", "will", and instructional imperatives), each as one
atomic, separately verifiable requirement.

**Step 4: Section M requirements.** Extract every evaluation factor, subfactor,
and element, and the basis of evaluation. Each becomes a matrix row: the
proposal must not just *address* it but *win* on it.

**Step 5: Section C / SOW / PWS / SOO requirements.** Extract every performance
requirement, deliverable, and standard. For a PWS, capture the outcomes and
their measurement; for a SOO, capture the objectives the offeror's proposed
SOW must satisfy.

**Step 6: Cross-walk.** This is the step that distinguishes a real compliance
matrix from a checklist. Link each requirement across the triad: which Section M
factor evaluates this Section C requirement; which Section L instruction tells
the offeror where to write it. Flag two failure types: an **L/M conflict or
ambiguity** (an instruction and an evaluation factor that do not align) and a
**gap** (a Section M factor with no Section L instruction, or a Section C
requirement no factor evaluates). Conflicts and ambiguities are candidate
questions for the contracting officer.

**Step 7: Format and submission rules.** Extract every page limit, font and
margin rule, file format and naming rule, volume separation rule, the due date
and time, the submission method, and required forms, certifications, and
representations. These go in a separate register (`checking-submission-compliance`
relies on it). A proposal can be rejected on these alone.

**Step 8: Write and validate.** Write `10-compliance-matrix.md` using
`templates/compliance-matrix.md` and the ID scheme in
`references/compliance-matrix-format.md`. Run the template's validation
checklist: every requirement is atomic and traceable to its source location,
the cross-walk is complete, conflicts and gaps are flagged, and the format
register is complete.

## Output

One artifact: `10-compliance-matrix.md` in the pursuit workspace, including the
format and submission register as a labeled section.

Present the user with: the volume structure, the requirement count by section,
the flagged L/M conflicts and gaps (with suggested CO questions), and the
binding format constraints (page limits especially).

## References

- `references/shredding-method.md`: requirement extraction, requirement language, atomic requirements, the L/M/C cross-walk, handling PWS and SOO.
- `references/compliance-matrix-format.md`: the matrix structure, the requirement ID scheme, the columns, and the compliance status values.
- `templates/compliance-matrix.md`: the compliance matrix artifact template and its validation checklist.

## Guardrails

- **Atomic requirements.** One requirement per row. A compound instruction split
  into three checkable parts is three rows. Compounds hide missed obligations.
- **Trace everything.** Every row cites its exact source location (section and
  paragraph). A requirement with no traceable source is suspect.
- **Do not invent or soften.** Extract what the solicitation says. Do not add
  requirements that are not there, and do not downgrade a "shall" to a "should".
- **Flag, do not resolve, ambiguity.** Where L and M conflict or a requirement
  is genuinely unclear, flag it as a CO question. Guessing the government's
  intent is how proposals become non-compliant.
- **Section L wins.** Where this package's conventions differ from the
  solicitation's instructions, the solicitation governs.
