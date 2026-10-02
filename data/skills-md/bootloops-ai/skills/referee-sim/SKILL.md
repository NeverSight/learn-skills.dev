---
name: referee-sim
description: Use before circulating any outward-facing scientific document — simulate the strongest standard objection from every audience it claims and verify the document answers each where that reader would look.
---

# referee-sim — the frame linter

Fact-checking and frame-checking are different audits. A verification pass confirms every sentence is true; this pass checks what a reader *concludes*. A document whose every claim is sourced can still mislead by assembly: the caveats live in the body while impressions form in the abstract; the comparison is honest but the baseline is one nobody uses; the theorem is real but the reader leaves believing it covers the case it excludes. That exact failure can survive multiple honesty passes and surface only when an outside expert finally reads the document — the expensive way to catch it, because by then the impression has already formed in the one reader whose report matters.

This is an audit of the IMPLICATURE — what each kind of reader walks away believing — run before anyone outside sees the document. Run your sentence-level style and honesty linter separately; the two passes catch disjoint failures, and neither substitutes for the other.

## Procedure

### 1. Enumerate the audiences, explicitly and in writing

List every community that could plausibly write a report on this document. Sources for the list, in order:

- The introduction's "this matters to X, Y, and Z" sentence. That sentence is a contract; every community it names gets an audit row.
- Every community whose **methods** the document borrows. Using their machinery invokes their standards, whether or not the document ever addresses them.
- Every community whose **results** the document takes as input or uses as a comparison.
- The **incumbent**: whoever currently does the thing the document claims to do better, faster, or differently. This audience exists even when the introduction never mentions them — especially then.
- The **practitioner** who would act on the result, whose question is never "is it interesting" but "what breaks if I rely on this."
- The venue's general reader, who determines which claims must survive without the surrounding expertise.

Two rules. First, any community borrowed from for authority — a method, a dataset, a benchmark, a motivating application — gets a row without exception; the missing-audience failure below is almost always one of these. Second, a claim of interdisciplinarity RAISES the bar. Each additional audience brings its own standard objection, and outsiders read less charitably than insiders: they apply their home field's first-order standard and have no reason to extend the benefit of the doubt.

### 2. Generate each audience's strongest STANDARD objection — on two axes

For each audience row, generate two separate objections:

- **Correctness**: "is this right, and does it hold in the cases my community cares about?"
- **Novelty**: "is this new, and what exactly is the advance over what we already do?"

These are different referee reports, answered in different places — correctness in scope statements, controls, and comparisons; novelty in the introduction's positioning and its engagement with prior work. A document that answers only one axis dies on the other, and conflating them produces a characteristic hybrid: a document that proves everything and never says what is new, or one that claims a first while the incumbent community's state of the art goes unexamined.

"Standard" means the first thing that community's referee asks, not an exotic one. Calibration by community type:

- *Engineering/applications*: "does this survive the generic case (generic noise, generic inputs, adversarial settings), or only the structured case you studied?"
- *Experimentalists*: "what does the apparatus actually measure, and is it the same object you computed? Which parts of the prediction survive the differences?"
- *Numericists*: "is anything converged? In which units or scheme — and does the flattering choice hide the drift? What is the null hypothesis your signal must reject?"
- *Formal theorists*: "is the named object well-defined here (does the symmetry, charge, or protection actually exist in this setting)? What is conjecture vs theorem, and does the abstract distinguish them?"
- *The incumbent method's community*: "we already do this better — what is your edge, precisely, and have you checked our state of the art?"

### 3. Steelman every objection

The objection must be one a well-informed, unsympathetic expert would sign — steelmanned, never strawmanned. Three tests:

- **The sting test.** If the document as written already answers the objection cleanly, you have probably written a weak one; sharpen until acting on it would require an edit. Occasionally the document really has pre-answered the strongest standard objection — treat that verdict as suspect and earn it, because a clean sweep is also exactly what a strawman pass produces.
- **The knowledge test.** Write the objection in the referee's own voice and name what they know that the document ignores: the prior result, the standard control, the benchmark their community demands. If you cannot name what the objector knows, you have not simulated them; you have simulated yourself in their seat.
- **The lead test.** A real referee leads with the standard objection. If your simulated objection is clever but nonstandard, generate the standard one first; the exotic one may follow as a second row, never as a substitute.

### 4. Verify each answer sits where the objector would look

Hostile readers read in a fixed order: title, abstract, figures, conclusions — then, only if still engaged, the one section their objection lives in. "Derivable by assembling facts scattered across the document" is a FAIL: the test is whether the objector meets the answer on their actual reading path, at or before the point where the objection forms. A disqualifying caveat that first appears mid-body has already lost — the report was drafted at the abstract.

Severity: **HIGH** — unanswered objection a referee would lead with, or a claim the project's own data or files contradict. **MEDIUM** — answered in the body but absent where the impression forms. **LOW** — answered, could be more prominent.

### 5. Audit the abstract separately and last

The recurring failure: body honest, abstract clean of every caveat. The abstract must carry (a) any scope limitation a claimed audience would consider disqualifying if discovered later, and (b) conjecture-vs-established labeling for the headline claim. Audit it cold, as someone who will read nothing else — most referees form their frame there, and some readers are abstract-only.

### 6. Apply minimal defensive edits only

Scope sentences, null-hypothesis statements, prominence moves (caveat from body to abstract or scope paragraph), unit and convention consistency for headline numbers, conjecture labeling, terminology corrections. NO new claims, NO new results, and no hedge-blur: the correct response to an objection is one sentence stating the claim's boundary, never a softening of the claim everywhere it appears. Run all new text through the machine-voice/honesty linter; recompile or re-render and confirm clean.

### 7. Write the verdict table

To `referee_sim_<doc>.md` beside the document: audience / objection / axis (correctness or novelty) / answered-where-or-NOT / severity / fix applied. The table is the deliverable even when no edits are needed — it records that the audit ran and what it covered, and the next revision's audit starts from it.

## Failure-mode catalogue

- **The friendly reader.** The simulated referee inherits the author's framing and raises only objections the document already answers; the pass returns clean, and the first genuine outsider leads with something the audit never generated. This is how the audit itself fails, and the reason for the sting test and the fresh-context rule.
- **The strawman objection.** A cousin of the friendly reader: each objection is phrased just weakly enough that the existing text answers it, so the verdict table fills with reassuring rows and the audit certifies the very frame it was built to attack.
- **The unread answer.** The objection is answered — thoroughly, honestly — in a subsection the objector never reaches. The referee formed the objection at the abstract and drafted the report before meeting the answer. Prominence is part of the answer, and an answer off the reading path is no answer.
- **Novelty–correctness conflation.** One objection per audience instead of two. The document defends correctness exhaustively and never states its advance over the incumbent, or claims an advance while a prior result the incumbent community knows goes unengaged. Either way the report writes itself.
- **The missing audience.** A community whose method, dataset, or benchmark the document borrows never gets a row — and it is exactly their standard objection that goes unanswered, because the borrowing invoked their standards without the audit noticing.
- **The abstract firewall.** Every caveat lives in the body; the abstract is clean. Sentence-level honesty passes confirm each sentence individually and never see the assembly. Impressions form in the abstract; the body is the appeal, and most readers never hear the appeal.
- **The charitable outsider.** The audit assumes a second field will read generously because the work is outside their specialty. The opposite holds: outsiders fall back on their home field's first-order concern and bring none of the insider's context for why a shortcut was reasonable.
- **Hedge-blur.** The fix pass answers an objection by weakening the claim everywhere instead of scoping it once. The document now claims less than it established, reads as unconfident, and still leaves the objection unanswered.
- **Author-context contamination.** The audit runs in the same context that wrote the document, so the "referees" judge each objection answered the way the author already did, blind spots intact. Distinct from the friendly reader: here even a well-generated objection receives a self-serving verdict on whether and where it was answered.

## A worked example

A document claims a faster method for a standard computation, demonstrated on a class of structured instances. The audience table, before any objection is written:

| audience | why they get a row |
|---|---|
| incumbent method's community | the document claims to beat them |
| practitioners of the computation | they would act on the claim |
| numericists | the evidence is numerical |
| the structured-instance community | their instances serve as the benchmark |

Steelmanned objections: the incumbent, on the novelty axis — "your comparison baseline is an implementation nobody uses; our current version handles your benchmark class in comparable time." The answer must live in the comparison section AND the abstract's claim must scope to what was actually beaten. Practitioners, on the correctness axis — "does this survive generic instances, or only the structured class you demonstrated?" The answer belongs in the scope paragraph and the abstract, since a practitioner discovering the restriction later would consider it disqualifying. Numericists — "converged in what sense, and against what null?" The answer belongs beside the headline figure, where the convergence impression forms. None of these objections is exotic; each is the first question its community asks. A version of this document that answers all three in those places is a materially safer document than the one that merely contains the answers somewhere.

## Cross-checks that pay off (run them every time)

- **Headline-number units**: is the quoted number in the same units and convention the document's own equations define? (Failure shape: a drift quoted in a convenient intermediate scheme's units comes out at roughly half the value the paper's own equations define — the flattering choice hides a factor of two.)
- **Claims vs the project's own files**: search the result notes for statements the document contradicts. (Failure shape: a document asserts a quantity must shrink with system size while the project's own larger-size results show it growing.)
- **Necessity language**: every "must / guarantees / ensures" — is it derived, or is it hope written as necessity?
- **Null hypothesis**: for any claimed signal (degeneracy, convergence to a special value, pattern), does the document state what chance would look like and why the data rejects it?
- **Temporal honesty**: if an interpretation was found *after* the data forced it, the document may present theory-then-confirmation; restore the actual order. Independent prior results can still be cited as independent.
- **Conjecture labeling at the title and abstract level**: "candidate / consistent with / designed for" vs language implying the claim is established.

## Operational notes

- Run the pass in a **fresh agent context** — never the context that authored the document. The simulated referees must not inherit the author's framing (see the catalogue's last entry).
- The cost is one agent session per document. Against a referee report that leads with the objection you failed to simulate, it is cheap.
- The exercise is a pre-mortem in Gary Klein's sense (Harvard Business Review, September 2007) run per audience.

## Expected yield (why this pass is mandatory)

First runs of this pass on finished, fact-verified documents reliably surface findings, often HIGH-severity ones: a generic-case scope statement missing from exactly the place an outside expert looks first; an abstract with no conjecture language over a fully-caveated body; a units choice that flatters a headline convergence figure; a claim the project's own files contradict. Each of these is a future referee-report finding, which is why the pass runs before circulation rather than after.

## Checklist

- [ ] Audiences enumerated in writing, including every borrowed-authority community and the incumbent.
- [ ] Two objections per audience — correctness and novelty — generated separately.
- [ ] Every objection passes the sting, knowledge, and lead tests.
- [ ] Every answer located on the objector's reading path, at or before where the objection forms.
- [ ] Abstract audited cold, last, as an abstract-only reader.
- [ ] Fixes are scope statements and prominence moves, never hedge-blur; new text linted.
- [ ] Verdict table written beside the document, even when no edits were needed.
- [ ] The pass ran in a fresh context.
