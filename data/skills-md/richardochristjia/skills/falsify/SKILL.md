---
name: falsify
description: Argues against review findings before anyone fixes them. For each must-fix finding it tries to reproduce it, asks who actually hits it and how bad that is, and picks the cheapest answer, which can be cutting the feature or leaving the finding open. It rejects findings whose only fix is a defensive check nothing shows is needed, and sends fixes that need a new rule or special case to the user. Read-only. Use between a review and its fixes, as the autopilot's falsify step, or for "falsify these findings", "do we really need to fix these", or "which of these review comments matter".
---

# Falsify

Reviewers are asked to find problems, so they always find some. You argue the other side: each finding must earn its fix. A fix costs code, and more code costs reading time, review rounds and new bugs. You rule on findings and never edit code.

## Input

- **The findings to rule on:** the review's must-fix list, with who raised each one.
- **The intent:** the plan folder or the PR description.
- **The branch's diff** against its base.

## For each finding

1. **Reproduce it.** Run something that shows it happening: a test, a script, a live command. A finding nobody can show happening is unproven, however good the argument, and an unproven finding is never **fix**, except as **Limits** says. When a finding comes with a run, check that the run shows what the finding claims.
2. **Find who hits it.** Which caller or user, doing what, and how often. Trace the call site. If the input can't occur (checked upstream, ruled out by the types, or only in a setup nobody uses), it's hypothetical.
3. **Weigh the harm.** What does someone see when it happens? From worst to mildest:
   - lost data or a wrong state
   - an action taken that nobody asked for
   - a wrong message the caller can recover from
   - slowness
   - looks
4. **Pick the cheapest answer that removes the harm.**
   - **cut:** remove the feature that causes it. Prefer this when the feature guesses, or exists only to save the caller one step.
   - **narrow:** keep the feature, but shrink where it applies.
   - **fix:** change the code. Say what the fix buys, and name the test that proves it: one that fails now and passes with the fix.
   - **your call:** the only fix needs a new rule or special case (a branch for one input, a new setting or flag). That often means the design is wrong, so the user decides whether to cut instead.
   - **leave open:** real, but not worth code now. It goes in the PR as one line.
   - **dismiss:** wrong, or the code already handles it.

## Defensive checks

A finding whose fix is a guard, a retry, a fallback, a re-check or a timeout for a state that might happen is rejected unless it has both:

- a reproduction, and
- harm worse than a wrong message the caller can recover from.

Without both, rule it **leave open**, or **dismiss** when the state can't happen, with the reason "defensive check; nothing shows it's needed". Guards already in the diff face the same test: raise any that fail it as **cut** findings of your own.

## Limits

- **The repo's written rules stand.** A broken rule from its agent instructions or its lint stays **fix**.
- **Security findings need a path, not a run.** Rule one with a plausible attacker path **fix** or **leave open**, never **dismiss** for lack of a reproduction.

## Output

One line per finding, worst harm first:

```
<verdict>: <the finding, short> (<who raised it>). <why: the run or the trace; say unproven or hypothetical when it is>
```

Then three lists:

- **For the fixer:** cut, narrow and fix.
- **For the user:** your call, each with the rule the fix would add.
- **For the PR's open findings:** leave open, each as its one line.
- **Dismissed,** each with its reason.
