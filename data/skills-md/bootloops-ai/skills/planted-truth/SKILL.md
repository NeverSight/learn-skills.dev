---
name: planted-truth
description: Synthetic-truth controls for analysis pipelines. Use before running any statistical fit, solver, audit, or search on real data — the pipeline must first prove it can recover a known planted answer and catch a deliberately corrupted input.
---

# planted-truth — the pipeline runs on synthetic truth first

**A pipeline that has only ever seen real data has never been tested, because
nobody knew what the right answer was. The only inputs whose correct output
is known are the ones you construct. Construct them, run them, and do it
before real data is touched.**

Real data cannot grade a pipeline. Whatever comes out looks like a finding:
a slope, an evidence ratio, a list of anomalies, an empty list of anomalies.
If the pipeline drops half its input on a parsing error, the output is
smaller and still looks like a finding. If a sign convention is inverted, the
conclusion reverses and still looks like a finding. The one situation in
which output can be graded is when the answer was written down first — a
plant: data generated from known parameters, fed through the full analysis,
with recovery demanded to the accuracy the real analysis will claim.

The order rule is not a nicety. Controls designed after the real output has
been inspected drift toward blessing it: the plant's parameters get chosen in
the region where the pipeline is already known to behave, the corruption
tests get chosen from the failure classes already ruled out, and the
tolerance gets set just wide enough for what was seen. Plant first, look
second. Once real output has been seen, the controls you design are no longer
independent of it.

## The procedure

**0. Freeze the controls before the first real run.** Write down the plants,
the corruptions, the null tests, and the pass criteria for each while the
real data is still unopened. A control invented later, to answer a doubt
about a result already in hand, is evidence of much less.

**1. Recover a plant, through the full path.** Generate data from the model
with known parameters and confirm the pipeline recovers them, to the accuracy
the real analysis will claim. Two hard requirements hide in that sentence.
First, *the full path*: the plant goes through the exact production entry
point, same configuration, same options, same file formats — not a
simplified call that skips the reader, the preprocessor, or the assembly
step, because those are precisely where pipelines break. Second, *the claimed
accuracy*: if the analysis will report an error bar, the planted value must
come back inside it; if it will report evidence for a model, the plant
generated under that model must yield that verdict. Recovery to worse
accuracy than the claim tests a weaker claim than the one being made. Plant
more than once, and include awkward corners of the parameter range along
with the comfortable middle.

**2. Catch corruptions.** Feed the pipeline inputs deliberately broken in
the ways it is supposed to detect — a sign flip, two swapped rows, two
swapped column labels, a block scaled by a constant, a shifted grid, a
duplicated record, a truncated file — one corruption at a time, and confirm
every one is caught, loudly, at the step that claims to catch it. Run a
clean twin alongside: an uncorrupted copy that must pass, proving the alarm
is responding to the corruption and not to everything. A checker that has
never fired is untested; a checker that fires on everything is noise.

**3. Null the machinery.** Where the pipeline sums, averages, or assembles
contributions: push a table of zeros through the full path and demand exactly
the baseline back — not approximately, exactly, because "approximately zero"
is where sign errors and double-counting hide. Re-insert a component the
system already contains and demand its recorded effect back, identically.
Nulls test the plumbing separately from the statistics, and plumbing is where
most real failures live.

**4. Author the fixtures independently of the code under test.** The
expected answer must not come from the pipeline being tested. Generate the
plant by construction — write the answer first, then produce data from it —
or with a separate implementation. An expected-output file regenerated from
the current code turns the test into a check that the code agrees with
itself; every bug present at generation time is baked into the fixture and
certified forever after.

**5. Prove each control can fail.** For every check in the battery, break
its input once on purpose and watch it fire. This is the only way to find
the checks that cannot fail — the aliased comparison, the unreachable
assertion, the tolerance that spans the whole range. A control's first
demonstrated failure is its birth certificate; before that it is a hope.

**6. Record the controls with the result.** The plants, the catches, and the
nulls are part of the deliverable, not scaffolding to delete. A result
whose controls were run but discarded cannot be distinguished, later, from a
result whose controls were never run — and later is when the question gets
asked.

**7. When a control fires on real data: stop.** Diagnose to the root before
any further run. The forbidden move is the plausible benign story — "that
check is oversensitive", "it's probably the known formatting quirk" —
followed by an override. A fired control that gets explained away is worse
than no control: it converts a working alarm into false confidence, and it
trains everyone touching the pipeline to override the next one.

## Failure modes the controls exist to catch

Each is a class seen in practice, in agent-built and human-built pipelines
alike. The vignette states the mechanism.

- **The check that cannot fail.** A comparison of a quantity against itself
  through an aliased variable; an assertion inside a branch nothing reaches;
  a tolerance wider than the range of possible answers. The test suite is
  green from the day it is written to the day the pipeline dies, and it was
  never once capable of turning red. Step 5 is the cure: no check counts
  until it has been watched to fire.

- **The string-compared verifier.** Two numbers formatted through the same
  printer and compared as text: the formatter rounds both sides identically,
  so values differing beyond the printed precision compare equal — and the
  comparison silently tests fewer digits than anyone believes. Worse, when
  both sides pass through the same serializer, a bug in the serializer
  equalizes genuinely different values. Compare numbers as numbers, at a
  stated precision, with the precision printed in the pass message.

- **Fixtures authored by the code under test.** The "expected" file was
  produced by an earlier run of the same pipeline, and gets regenerated
  whenever it drifts. The suite now enforces self-agreement: any bug present
  at fixture time is preserved, and a later fix that changes the output
  reads as a regression. Expected answers come from construction or from an
  independent implementation, never from the thing being graded.

- **The silent-pass leg.** A loop over cases catches exceptions per case and
  moves on; the summary counts the cases that ran. A missing input file
  yields an empty case list, zero failures, and a green banner — "all passed"
  where the denominator was silently zero. Every summary states its
  denominator, and the harness fails when the denominator is smaller than
  declared.

- **The tuned threshold.** A plant is not recovered; instead of finding the
  cause, the tolerance is loosened until it is. Repeat a few times and the
  tolerance is exactly wide enough to pass a broken pipeline — a real error
  of the same size as the widening now passes by construction. A control
  that needs its threshold moved has found something; find out what.

- **The plant designed after peeking.** Real output is inspected first, then
  a synthetic control is built "to confirm" — with parameters, corruption
  types, and pass criteria all chosen in the shadow of what was seen. The
  control confirms; it was never able to do anything else. This is why step
  0 freezes the battery before the real data opens.

- **The simplified-path plant.** The control runs through a convenience
  entry point — smaller grid, mocked reader, the assembly step stubbed out —
  and passes. The real run uses the full path, and the failure lives in a
  step the control skipped. A plant certifies exactly the code path it
  traversed and nothing else.

- **Self-consistency mistaken for a control.** The calculation's own
  convergence diagnostics stay clean orders of magnitude past a real
  failure, because a pipeline that is consistently wrong is still
  consistent. Internal agreement, stability under iterations, and smooth
  residuals are properties of the machinery, not of the answer. Only a check
  with an independent notion of truth counts: a plant, a positivity or
  symmetry constraint the answer must obey, a second route.

- **The explained-away alarm.** A control fires on real data; a plausible
  story is found; the run proceeds. When the failure finally surfaces
  through some other channel, the record shows the alarm worked and was
  overridden — the most expensive possible way to learn the control was
  right. Firing means stop; the story, if true, will survive a root-cause
  diagnosis.

- **The unconditional banner.** The driver prints its completion message
  outside the conditional that checks the results, so a run that verified
  nothing announces success. The verdict text must be produced by the
  verification itself, from measured quantities — and the deliberate break
  of step 5 exposes this class immediately, because the banner also blesses
  the broken run.

## Two micro-examples

*A regression pipeline.* Write down a slope and intercept. Generate data
from them with the noise model the analysis assumes. Run the production
entry point — the same command the real data will get — and demand the
planted values back inside the reported intervals. Then swap two column
labels in a copy of the input and demand the consistency check names the
columns; run the unswapped copy alongside and demand silence. Only then open
the real data.

*An assembler of contributions.* Before trusting a total, push a table of
zeros through the assembly and demand the exact baseline. Then take one
component whose individual effect is already on record, re-insert it alone,
and demand that recorded effect back to the digit. If the zeros come back
nonzero or the known component comes back changed, the plumbing is broken,
and no statistic computed through it means anything.

## Checklist before the first real-data run

- [ ] Control battery — plants, corruptions, nulls, pass criteria — written down before real data was opened.
- [ ] Plant recovered through the full production path, to the accuracy the real analysis will claim, including awkward parameter corners.
- [ ] Every claimed detector shown to catch its corruption, loudly; clean twin passed alongside.
- [ ] Zeros through the assembly returned the exact baseline; a known component returned its recorded effect identically.
- [ ] No fixture was authored by the code under test.
- [ ] Every control has been watched to fail at least once, on a deliberate break.
- [ ] Pass messages state counts and denominators; no banner prints outside the verification.
- [ ] Controls filed with the result, not deleted.
- [ ] Standing order acknowledged: a control that fires on real data stops the run until the root cause is known.

**Sources and acknowledgments.** Planted-truth recovery is what statisticians
call simulation-based calibration (Cook, Gelman and Rubin, J. Comput. Graph.
Stat. 15 (2006) 675; Talts, Betancourt, Simpson, Vehtari and Gelman,
arXiv:1804.06788) and what experimental collaborations call injection tests or
mock-data challenges; "prove each control can fail" is mutation testing
(DeMillo, Lipton and Sayward, IEEE Computer 11(4) (1978) 34); positive and
negative controls are borrowed, name and all, from the wet lab. We claim only
the checklist.
