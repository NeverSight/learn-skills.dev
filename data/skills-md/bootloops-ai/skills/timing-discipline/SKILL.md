---
name: timing-discipline
description: Compute-planning rules. Use before launching any calculation whose runtime is not already measured — and whenever an agent proposes a long run, an overnight grind, or a bigger machine as the way forward.
---

# timing-discipline — measure first, restructure early

The expensive mistake in computational work is rarely the wrong algorithm. It
is the run that consumes a night, a weekend, or a machine-week and returns
something a ten-minute pilot would have predicted. Runtime intuition is
systematically optimistic — in people, and worse in language models, which
produce fluent, confident durations for jobs they have never timed, because
plausible-sounding ETAs are easy to generate and nothing in the generation
process consults a clock. Hence the founding rule:

**An estimate not derived from a measurement of this calculation, in this
configuration, on this machine, is a guess.** Every projection is either
(a) fit from the job's own time-stamped log, (b) taken from a measured prior
run of identical configuration on the same hardware, or (c) reported as
"unknown — measuring now." There is no fourth category.

The second rule is what to do with the measurement. When a projection comes
out long — past a couple of hours — the right response is almost never a
bigger run, a bigger machine, or an overnight slot. It is restructuring the
problem so the run shrinks. Measured honestly, most long projections are the
computation telling you that you are solving it the wrong way.

## Procedure

1. **Pilot before anything that might be long.** Same code, same machine,
   same settings, same distribution of cases — scaled down in size only, with
   a time-stamped log. If the job cannot be scaled down, that is itself a
   design defect worth fixing before launch, because it also means the job
   cannot be checkpointed or partially salvaged.

2. **Fit the rate from the steady-state window.** Discard the startup
   transient: the first items carry compilation, cache fill, and input
   loading, and a rate fit across them is wrong in whichever direction hurts
   more. Then check the per-item cost trend across the pilot. If cost grows
   with index — swelling expressions, accumulating state, rising memory — a
   linear extrapolation is a floor, not a forecast: run the pilot at two
   sizes and fit the growth exponent instead.

3. **Write the projection down with its provenance** before launching: pilot
   size, window used, measured rate, scaling assumption. A projection whose
   provenance cannot be stated in one line is an estimate wearing a number.

4. **Apply the threshold.** If the projection exceeds a couple of hours,
   stop. Do not launch, do not reach for more cores. Restructure instead, and
   actually enumerate the candidates: a better representation or basis; an
   exact reduction that shrinks the object before any numerics touch it; a
   symmetry that collapses the case count; a split into independent pieces; a
   cheap method for the bulk of the cases with the expensive one reserved for
   the residue; a limit or special case that answers the actual question
   without the general computation. The restructured route usually exists,
   and when it exists it beats hardware by more than hardware can give.

5. **Fresh eyes before any long run.** Before committing to a projection near
   or over the threshold, have someone — or a separately prompted agent with
   no stake in the current plan — spend a short, bounded effort on one
   question: is there a structurally smarter route? Record the verdict either
   way. "Current route is right because X" is a valid outcome; silence is
   not, because the absence of a recorded verdict is indistinguishable from
   the question never having been asked.

6. **Define real progress before launch.** Name the output unit the run
   exists to produce and the file or table where it accumulates. Monitoring
   watches that count. Log volume, CPU load, and process liveness are not
   progress; they are signs of activity, and activity is what a stuck job
   emits too.

7. **A rate collapse voids the projection.** If the measured rate drops
   severalfold mid-run, stop quoting the old ETA that instant. Diagnose,
   re-measure, re-plan. A projection is conditional on the rate it was fit
   from; when the rate goes, the projection is gone with it.

8. **Re-measure on any change.** New machine, new input regime, new working
   precision, new parameter range: the old rate does not transfer, however
   similar the job looks. Rates are properties of a configuration, not of an
   algorithm.

## Failure modes

Each of these has burned real time. Each looks reasonable from the inside
while it is happening.

**The unmeasured overnight launch.** A job goes up at the end of the day
because the day is ending, on the theory that the night is free anyway.
Morning finds it a small fraction done, dead, or wedged — and the night was
not free: it cost the diagnosis time, the cleanup, and a day of schedule
built on the assumption it would finish. The launch decision was made by the
calendar, not by a measurement.

**The intuition ETA.** "About an hour, probably." From a person this is
optimism; from a model it is fluent confabulation with the grammar of a
measurement. The tell is that no log exists from which the number could have
been derived. The question that kills it is three words: measured from what?

**The startup-transient fit.** A rate fit from the first items either
includes one-time warm-up costs — projecting the run as far grimmer than it
is, so a feasible job gets canceled — or is taken after caches are warm and
omits a cost the full run pays over and over. Both are cured by fitting the
steady-state window and saying which window was used.

**Linear extrapolation of a superlinear cost.** Every item slightly costlier
than the last: growing intermediate expressions, an accumulating store,
memory pressure building toward swap. The pilot's rate is the best rate the
run will ever see, the projection is a lower bound presented as a forecast,
and the wall arrives hours after the promised finish. The two-size pilot with
a fitted exponent exists for exactly this.

**Grinding past the rethink.** The most expensive class in the catalog. A
route measured to be long gets ground through anyway, because grinding feels
like progress and rethinking feels like starting over. A day goes into
babysitting the run — restarts, memory tweaks, partial salvage — while a
reformulation that would remove most of the work sits unexamined. When the
reformulation is finally tried, it finishes before the grind would have. The
threshold rule exists to force this comparison while it is still cheap.

**The bigger-machine reflex.** The projection is bad, so the plan becomes
more cores. Parallelism pays at most the width factor, and only when the
problem splits cleanly; a restructure removes the work itself, which no
amount of width can do. Hardware comes after the structure is right, not
instead of it.

**The rate collapse ignored.** Mid-run the rate drops severalfold — the hard
cases arrive, memory tightens, another job lands on the same machine — but
the original ETA keeps being quoted because it is written down and quoting it
is easier than re-measuring. Every "almost done" derived from the dead rate
is fiction, and every plan built on it inherits the fiction.

**Log lines mistaken for progress.** The job prints steadily, therefore it is
working — except the printing is a heartbeat, a retry loop, or a progress
indicator over a phase that finished long ago, and the output file has not
grown in hours. Liveness is measured on the output class the run exists to
produce; everything else is the sound of a fan.

**Sunk-cost continuation.** "It has been running too long to kill now." The
hours already spent are not an argument for spending the rest; they are
spent either way. The only live comparison is the measured remaining time of
this run against the total time of the restructured route — and the
restructured route often wins even starting from zero.

**The unfaithful pilot.** The pilot ran with different flags, lower
precision, warm caches, or the easy slice of the input, so the projection
describes a different computation. The sharpest variant: case difficulty
grows with index, and the pilot sampled the easy head of the list. The pilot
is the run, scaled down, with nothing else changed — and drawn from the same
distribution of cases as the real thing.

## The worked shape

The whole discipline in symbols. The pilot's steady-state window yields n
items in time t, so the rate is r = n/t. The full run has N items, so the
projection is N/r — under an explicitly stated linearity assumption. If two
pilot sizes disagree with that assumption, fit cost ∝ N^α and project with
the fitted α, saying so. Then the branch: projection under the threshold —
launch, with the progress unit defined and a standing rule that a rate
collapse voids the ETA; projection over the threshold — restructure first,
with the fresh-eyes verdict recorded before any long launch is even
considered.

The same shape covers monitoring. Before launch, write down: progress is the
row count of the results file, expected to grow at roughly r. During the run,
the check is that count against that expectation — never "the log is still
scrolling," and never "the process is still alive."

## Checklist

Before launching anything that might be long:

- [ ] Pilot run: same code, machine, settings, and case distribution;
      time-stamped log kept.
- [ ] Rate fit from the steady-state window; per-item cost trend checked;
      scaling assumption stated.
- [ ] Projection written down with one-line provenance before launch.
- [ ] Projection over the threshold? Restructuring candidates enumerated and
      tried, and a fresh-eyes verdict recorded, before any long launch.
- [ ] Real-progress unit defined, with where it accumulates and the expected
      rate; monitoring watches it, not the log.
- [ ] Standing rule armed: a severalfold rate drop voids the ETA and triggers
      a re-plan, not a wait.
- [ ] Any change of machine, input regime, or precision → re-measure before
      re-projecting.
