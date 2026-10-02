---
name: prove-protocol
description: Multi-agent protocol for proving or refuting mathematical statements. Use when trying to prove a mathematical statement with agents, when a claimed lemma keeps dying under scrutiny, or when the true statement itself is still unknown (theory-finding regime).
---

# prove-protocol — the full proving playbook

## 0. The discipline, and why it is shaped like this

**Within this protocol, no mathematical claim is graded closed on agreement.
It is graded VERIFIED-CLOSED only when an agent assigned to refute it — armed
with executed exact arithmetic — has failed, and when a second agent who
authored nothing has rebuilt the chain from the spec alone, reproducing every
pre-registered value with fresh code.** This is a working standard for agent
output, not a substitute for a refereed or formally verified proof. Everything
below is machinery for manufacturing those two events on purpose.

The paranoia is calibrated to three observations from practice and from the
literature (Sources, below):

1. **Agreement is free.** Provers built on the same or similarly trained
   models share blind spots and converge on the same form — including the same wrong form.
   Consensus measures correlation of priors, not truth. Independence must be
   forced structurally (separate contexts,
   forbidden cross-reading, named-distinct routes), never requested in a
   prompt.
2. **Self-review approves its own bugs.** The reasoning that produced a
   flawed step is the same reasoning that re-reads it and finds it
   convincing.
3. **Talk is a null instrument.** Natural-language-only critique ("step 7
   seems under-justified") does not move a proof's state — a measured null
   (the intrinsic self-correction null measured by Huang, Chen, Mishra,
   Zheng, Yu, Song and Zhou, arXiv:2310.01798, ICLR 2024). The only signal that cannot be socially
   generated is an executed exact computation at a hostile instance; every
   check in this protocol bottoms out in a script that ran.

Two regimes. Know which one you are in before spending tokens:

- **REGIME 1 — the statement is known**: run the pipeline in §1 (target-pin →
  adversary-first hunt → prover/skeptic core → forced-diversity provers →
  fresh-context cross-verify → interface trace).
- **REGIME 2 — the statement is UNKNOWN or keeps dying**: theory-finding (§4).
  The failure smell: you pin formulation after formulation and a competent
  adversary kills each within hours. A consistent pattern: target reshapings
  come from adversaries, essentially never from provers — provers
  do not find theorems; searchers and adversaries do.

## 1. The pipeline core (REGIME 1)

0. **ADVERSARY FIRST (X0)** — reliably the highest-value step per token
   spent. Before any proving run, spend one run hunting the exact witness that
   makes the claim FALSE (in-regime, exact-arithmetic witness). Ladder
   discipline: shift the target ONLY on a certified fire (exact witness,
   inside the claimed regime); a NO-FIRE changes nothing. A certified kill is
   constructive — with pre-registered alternative forms (see step 1), the kill
   licenses the surviving form instead of ending the run.

   *Micro-example of the X0 posture.* Claim: "over the whole family, the
   quantity is minimized at the symmetric configuration." The adversary does
   not read the heuristic argument; it writes a short exact enumerator over
   the family's smallest members and aims it where symmetry arguments die —
   degenerate members, boundary parameters, the smallest asymmetric
   instance. A minimizer that moves at a degenerate member is a certified
   kill, and the witness names the repair (exclude the degenerate class, or
   weaken to non-strict). One agent-run; it often saves ten.

1. **TARGET-PIN as a shared SPEC**: one spec file every prover reads,
   containing (a) the statement/hole verbatim with source citations; (b) a
   MAY-ASSUME list (granted lemmas WITH their stated hypotheses) and a
   MUST-NOT-ASSUME list (the thing being proven); (c) licensed alternative
   delivery forms WITH acceptance criteria ("closes the consuming target at
   the printed exponents; constants may be flagged, exponents may not move");
   (d) an exact test instance T1 — pre-registered rational/integer values plus
   named FAIL conditions ("a route whose T1 prediction fails is DEAD");
   (e) an erratum channel — specs contain bugs (independent arms have
   repeatedly falsified claims that turned out to be bugs in the spec itself,
   not the mathematics), so the spec must
   be correctable without invalidating prover runs already in flight.
   Pre-register which outcome changes what. The pin agent and the X0
   adversary agent are SEPARATE agents — merging them invites an output-cap
   death; any stage mixing statement-extraction with construction dies.

2. **SKEPTIC LOOP** (the highest-yield loop in practice):
   - ONE workfile is the sole shared state; pre-load the skeptic's danger list
     before proving starts.
   - The PROVER drafts the full chain with every displayed identity tied to an
     executed exact-arithmetic script.
   - A hostile fresh-context SKEPTIC does grounded spot-checks at adversarial
     instances and emits machine-readable bug reports —
     `{failing step index, exact instance, value of each side, residual}` —
     never an essay. Prose-only critique counts for NOTHING.
   - Revise against the report. Accept only after 2–3 CONSECUTIVE clean
     fresh-context passes.
   - One SNEAKY-PLANT audit, on a COPY: plant a known-false step and verify
     the harness CATCHES it. If the plant survives, the harness is
     unfalsifiable and the arm is invalid.
   - Any import outside MAY-ASSUME: flag it verbatim, verify it in the source,
     and PRE-REGISTER the downgrade path ("if ruled inadmissible → OPEN-AT
     step k with the rest intact"). This adversarial self-audit is what
     makes one-pass external verification possible.

3. **FORCED-DIVERSITY RIDER** (mandatory): ≥2 extra provers on named distinct
   routes, parallel fresh contexts, no cross-reading. Lesson from practice:
   independent arms converge unanimously on the same form with ease — and the
   artifact that reshapes a target tends to come only from a forced-divergent
   route, at any budget. The redundancy (including DNFs and failed
   certifiers) buys the one artifact nothing else produces.
   RULE: a closure without a diversity pass is
   graded PROVISIONAL. Cheap version: ONE skeptic chain (the proof) + ONE
   small tournament of 2–3 forced-distinct provers (the falsifier).

4. **FRESH-CONTEXT CROSS-VERIFY + INTERFACE TRACE** (both mandatory before
   VERIFIED-CLOSED). Every arm self-grades CLOSED-UNVERIFIED; nothing counts
   until BOTH:
   (a) **verify pass**: an agent that authored NOTHING re-derives the chain in
       its own words under hostile instructions, treats every "clearly" as a
       check-site, writes a FRESH independent enumerator (no code reuse) that
       reproduces every pre-registered exact value, and greps the load-bearing
       imports for circularity. Verdict: CONFIRMED / refuted, constants
       printed.
   (b) **interface ruling**: trace EVERY use-site of the delivered object in
       the consuming document; rule per-site whether the delivered form
       satisfies the consumer's STATED hypothesis (not its wording — wording
       is often shaped like the strong form over content the weak form
       covers); machine-check the composed arithmetic. This is where an
       alternative-form delivery gets legitimized or killed.

## 2. Failure-mode catalogue

Each class is the reason a rule above exists; the vignettes describe
mechanisms, not one-off accidents.

- **Proof by agreement.** Provers converge on the same conclusion and the
  convergence is filed as verification. Mechanism: shared priors produce
  identical errors at any N — the agreement was determined before the first
  token was generated. Cure:
  §1.3 forced diversity plus §1.4(a); a verdict only counts from an agent
  that could have profited by disagreeing.
- **Steps verified by their author.** The prover "double-checks" its own
  chain and reports all steps sound. Mechanism: the blind spot that wrote the
  bug re-approves it. Cure: skeptic and verifier are fresh contexts that
  authored nothing, always.
- **The skipped hunt.** No counterexample search was run because the claim
  "obviously" holds — the heuristic is clean and the small cases in the
  prover's head work. Mechanism: obviousness is a fact about the prover's
  prior, not about the statement; the witness usually
  lives exactly where the intuition was trained not to look (degenerate and
  boundary instances). Cure: X0 is unconditional; it runs first even when
  everyone is sure.
- **Talk-only skepticism.** The skeptic writes paragraphs of doubt, the
  prover writes paragraphs of reassurance, the workfile grows, the proof
  state does not move. Mechanism: language models happily co-author
  confidence. Cure: bug reports are machine-readable; anything without an
  executed instance is noise.
- **The harness that cannot fail.** The verification loop passes everything —
  because it would pass anything. Mechanism: a checker that has never caught
  a planted bug has an unmeasured false-negative rate; its passes carry no
  information. Cure: the sneaky-plant audit — no trust before a demonstrated
  catch.
- **The silent import.** Somewhere in step 9 the chain uses a fact outside
  MAY-ASSUME — often a disguised paraphrase of the target itself. Mechanism:
  circularity arrives dressed as a "standard fact." Cure: the verbatim
  import flag (§1.2) plus the verify pass's circularity grep.
- **The unexecuted certificate.** The journal says "the attached script
  verifies this" and the script was never run to completion; one measured
  "certificate" failed its own pre-registered asserts when actually executed.
  Mechanism: writing a plausible checker and running one are different acts.
  Cure: script-of-record with output quoted verbatim (§3).
- **Verification against wording.** An alternative-form delivery is accepted
  (or rejected) because it matches the consumer's sentence rather than its
  hypothesis. Mechanism: statements are routinely written stronger than
  their proofs use. Cure: the interface trace (§1.4b).
- **The spec trusted as ground truth.** All arms faithfully attack a
  statement mis-transcribed at pin time — an index off by one, a hypothesis
  dropped. Mechanism: the pin has the same error rate as any other artifact.
  Cure: the erratum channel; treat a unanimous early kill as a possible spec
  bug first.
- **Pin-thrash (the zombie statement).** The tenth reformulation of a
  repeatedly-killed claim is being pinned with fresh hope. Mechanism: the
  true object is usually a continuum or a mechanism, not the crisp dichotomy
  being re-pinned; each new pin samples the same doomed neighborhood. Cure:
  switch to REGIME 2 (§4).

## 3. Infrastructure rules (each learned from an agent failure)

- **Skeleton-first, corrected form** (a recurring agent failure shape:
  bulk-read everything, then die at the output cap having planned but never
  written): (1) read the TARGET PIN ONLY; (2) IMMEDIATELY write the
  workfile skeleton, one pre-filled line per planned section; (3) read
  supporting files ONE AT A TIME, per section, transcribing each check into
  its section before opening the next file. Never hold more than one
  unwritten conclusion. For symbolic work: scripts write their own output
  files; quote ≤5-line summaries; never paste large expressions into
  messages.
- **Never steer a running proof agent mid-run** — corrections go in relaunch
  prompts. Mid-run messages trigger a fatal re-planning burst.
- **Disk-incremental journals with executed evidence**: the workfile is the
  proof state; write as you go. Transient infrastructure errors are not state
  changes — resume, never re-derive. A run that dies with zero bytes on disk
  is ungradeable: no journal = no arm. Script-of-record + output file quoted
  VERBATIM in the journal, so graders can replay exactly.
- **AMBIGUOUS-refusal beats silent improvisation**: on a broken or ambiguous
  spec, halt-and-flag or redesign-with-logged-deviation (legal, gradeable).
  Silently improvising out-of-model parameters is a measured downgrade-to-
  OPEN.
- **Detach all compute expected to outlive the agent's turn** (e.g.
  setsid/nohup or your framework's background-job facility); non-detached
  children die with the tool session.
- **Budget honesty**: parallelism premium charged; DNFs and failed certifiers
  count against the arm; the metric is reusable-progress-per-token, not
  closure count.

## 4. THEORY-FINDING (REGIME 2 — when the statement itself is unknown)

The signature of this regime: formulation after formulation gets hand-pinned,
and a competent adversary kills each one within hours or days. When repeated
pins die, STOP hand-guessing and search statement-space mechanically:

**4a. Build the exact evaluator first** (the FunSearch / AlphaEvolve
precondition: generate-and-score against an exact evaluator is the pattern
behind the published machine-discovered mathematics we know of — Romera-Paredes
et al., Nature 625 (2024) 468, doi:10.1038/s41586-023-06924-6; Novikov et al.,
arXiv:2506.13131; Georgiev, Gómez-Serrano, Tao and Wagner, arXiv:2511.02864). Assemble a LABELED CORPUS of every
certified object the effort has produced (witnesses, counterexamples,
controls; label quality = certified/measured/screened as an explicit field,
receipt-traced). Then a FEATURE LIBRARY of computable functionals spanning
the project's mechanistic vocabulary. The corpus + evaluator turn "is this
candidate statement true so far?" into an exact, instant check.

**4b. Forced-distinct THEORY TOURNAMENT**: 2–4 agents, no cross-reading, each
LOCKED to a different organizing principle (e.g., bifurcation /
symmetry-breaking; information geometry; real algebraic geometry;
probabilistic / genericity). Each must deliver: the organizing picture in its
lens; CANDIDATE THEOREMS fully quantified and falsifiable; an explicit
object-by-object consistency table against the certified corpus; the 3
sharpest first tests; honest scoping of which certified objects fall outside
its lens. Divergence between arms is data.

**4c. Invariant synthesis** over the feature matrix (searchers: sparse
inequality synthesis, monotone-lattice search, program search) — candidates
scored by the exact evaluator, survivors handed IMMEDIATELY to an X0
adversary — never pin a synthesized statement that has not survived a
dedicated falsification run.

**4d. Formulation-ladder bookkeeping**: every dead formulation gets its
killer recorded (witness + mechanism). The kill LIST is itself a deliverable
— after enough kills it becomes a theorem-grade impossibility map, and the
mechanisms usually name the surviving statement's true shape (in practice the
kills typically trace to a small number of identifiable degeneracy
structures).

## 5. Preconditions & priors (do not deploy blind)

Published base rates without preconditions, as of the cited evaluations (Mar 2025 /
Feb 2026; capabilities move quickly): 10-15% cold success (pass@1) on fresh self-contained
research lemmas (LemmaBench — Peyronnet, Gloeckle and Hayat, arXiv:2602.24173); <5% average proof score on USAMO 2025
for most models evaluated at release despite strong final-answer benchmark results (Proof or Bluff —
Petrov, Dekoninck, Baltadzhiev, Drencheva, Minchev, Balunović, Jovanović and Vechev,
arXiv:2503.21934). Projects
beat the base rate only when THREE preconditions held — check all three
first:
1. **Exact-computable test instance**: T1 with exact rationals, fully
   enumerable in seconds — every chain and every bug falsifiable by a CAS the
   same hour. Absent this, the skeptic loop degenerates to natural-language
   self-critique (measured null).
2. **A falsifiable, pre-registered alternative**: both forms NAMED in the
   spec with acceptance criteria, so the adversary has a concrete statement
   to kill and a kill constructively licenses the survivor. Absent this, the
   adversary step has no target.
3. **Mature interface**: the consumers of the result already exist with
   stated hypotheses and a may-assume list — quantifier-completion against
   known consumers, not open-sea invention. Absent this, expect the ~15%
   prior.
For REGIME 2 add: (4) a corpus of certified objects rich enough to score
candidates — if you lack one, run adversary/instance-building rounds first.

## 6. What has worked in practice, and what has not

WORKS (in our campaigns and in the literature cited in §5): generate-against-exact-evaluator; self-contained
stuck-step consultation with CAS re-derivation; candidate-object search for
analysis proofs (Lyapunov/ansatz enumeration, falsify-each-cheaply);
decomposition into sublemma STATEMENTS first, split-on-verification-failure;
literature retrieval (typed as retrieval, never as discovery).
HAS NOT WORKED, for us or at the base rates cited in §5: autonomous end-to-end proving without a mechanical certifier;
self-reported confidence; final-answer benchmarks as proving ability;
natural-language-only critique.

Grading: VERIFIED-CLOSED only after §1.4's two passes. Log every run — arm,
budget, grade, artifacts — to a scoreboard so DNFs and failed certifiers
stay visible.

**Sources and acknowledgments.** This protocol was distilled from our own
multi-agent proving campaigns, but its parts have antecedents we are glad to
name: the verification-and-refinement loop of Huang and Yang (arXiv:2507.15855)
and the practitioner techniques collected by Woodruff, Cohen-Addad et al.
(arXiv:2602.03837) — problem decomposition, iterative refinement against error
feedback, and the model deployed as an adversarial reviewer of existing proofs;
counterexample-guided inductive synthesis (Solar-Lezama, Tancau, Bodik, Seshia
and Saraswat, ASPLOS 2006) for the adversary/prover alternation; mutation
testing (DeMillo, Lipton and Sayward, IEEE Computer 11(4) (1978) 34) for the
planted-bug audit; Knight and Leveson's (IEEE Trans. Softw. Eng. SE-12 (1986)
96) demonstration that independently written versions fail together, which is
why diversity is forced rather than requested; and, older than all of these,
Lakatos's *Proofs and Refutations* (Cambridge, 1976). The exact-evaluator
regime follows FunSearch and AlphaEvolve (refs in §4a); the base rates are from
LemmaBench and Proof or Bluff (§5) and the self-correction null from Huang et
al. (§0).

## 7. Closing checklist

- [ ] Regime identified; after two dead pins, the REGIME 2 question was
      asked on the record.
- [ ] Spec file exists: statement verbatim, MAY/MUST-NOT-ASSUME, alternative
      forms with acceptance criteria, exact T1 with FAIL conditions, erratum
      channel.
- [ ] X0 adversary ran BEFORE any prover; fire/no-fire verdict recorded with
      witness or search transcript.
- [ ] Every displayed identity tied to an executed script, output quoted
      verbatim in the journal.
- [ ] Sneaky-plant audit run on a copy; the plant was CAUGHT.
- [ ] ≥2 forced-distinct provers, no cross-reading — else graded
      PROVISIONAL.
- [ ] Verify pass by an agent that authored nothing, fresh enumerator (zero
      code reuse), every pre-registered value reproduced.
- [ ] Interface trace covers EVERY use-site; rulings on stated hypotheses;
      composed arithmetic machine-checked.
- [ ] Imports outside MAY-ASSUME flagged verbatim with pre-registered
      downgrade paths.
- [ ] Journal on disk for every arm; DNFs and failed certifiers logged, not
      erased.
- [ ] Nothing labeled VERIFIED-CLOSED without both §1.4 passes. A wrong
      proof is worse than an honest OPEN.
