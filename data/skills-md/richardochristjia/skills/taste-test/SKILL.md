---
name: taste-test
description: Tries a finished build the way its user would. Starts the real program in a throwaway setup with a copy of real data and the real programs it talks to, runs each acceptance criterion in the plan and each line of its risk list, and reports what broke with steps to reproduce. Never edits code. Use as the autopilot's taste-test step, or for "taste test this", "try it like a user", "walk this build" or "does it actually work".
---

# Taste test

Tests pass against fakes; users hit the real thing. You run the build the way its user would and report what you see. You never edit code: fixing is a later step, and a second taste test checks the fix.

## Input

- **The plan folder:** `plan.md` for the acceptance criteria, `risks.md` for the risk list.
- **The branch,** built.
- **On a second run,** the first run's report and what changed since.

## Set up a throwaway copy

1. **Use the repo's committed fixture if it has one:** the folder named by `FIXTURE:` in `.plans/<task>/tier.md` when that line is present, else `.harness/`, in the repo, holding a fake backend and a driver that walks the UI, as [make-fixture/CONTRACT.md](../make-fixture/CONTRACT.md) defines. Run its scripts as they show; don't retype their steps. Launch, check and drive the program, and clean up, as it says. A fixture is a fake backend the repo ships: it must never contact a real backend, and it must not need credentials. If the repo has no fixture, look in `AGENTS.md` / `CLAUDE.md` for how to try it.
2. **Otherwise build a setup,** and put the steps in your report, so the repo can commit it as a fixture next time:
   - a temp folder for the program's home, config and state, so nothing you do reaches the user's real copy;
   - a fake of the service the program talks to, in the temp folder, so the run never writes to a real system;
   - a browser or agent to drive it, and the user's logins only if the repo's own flow needs them — by linking their token files into the temp home, never copying them. Never print a token or commit one.

**Never point the app at a real backend.** No staging, no QA, no production: not for a read, not for a write. A walkthrough that needs a real backend is a `manual:` criterion, and the plan already lists those for a human.
3. **Data rules.** Follow the fixture's environment rules, which come with the repo. Where it says nothing, or there is no fixture:
   - **Local data:** work on a copy, never the original.
   - **Staging:** fair game, writes included.
   - **Production:** read only, and only with access you already have. Never write, delete or trigger anything there.
   - **The user's running programs:** leave them alone. Stop only what you started.
   - A check that needs access you don't have, paid calls or a device is **couldn't try**.
4. **Stay off the user's screen.** Don't take focus, open windows or raise dialogs they'd have to answer. A check that can't avoid it is **couldn't try**.

## If the fixture breaks

- **First decide whose fault it is.** If this branch changed what the failing step relies on (a flag, a key, a label, a port) and the plan didn't ask for that change, it's a **broke** line for the fixer.
- **Otherwise the fixture is out of date.** The fixture is the repo's code, so you may fix it: change the script when the fix is clear, then run the fixture's self-test until it passes.
- **Never loosen a guard or one of the user's rules** to get past a failure. That goes to the user.
- **If the fix isn't clear,** each check that needed the step is **couldn't try**, with the step and its error.

## What to try

1. **Each acceptance criterion** in `plan.md`, through the real way in: a person's keys or clicks, or an agent's commands or API. Never by calling its code. If people and agents both use the feature, try both.
   - **A criterion marked `manual:` is not yours to try.** It needs a real backend, a real account or a real device. Leave it to the human, and list it under "For the user" as manual, not as a failure.
2. **Each line of `risks.md`.** Do what its check says.
3. **A few minutes off the plan.** The likeliest things a user does that the plan doesn't mention: cancel halfway, do it twice, restart in the middle, delete something it depends on, a large input.

Keep the exact commands, so anyone can run them again.

## Pictures

- **Every check you try gets a picture of where it ended and a video of the actions that led there.** Pass and broke alike: a broke picture shows what went wrong. Use the fixture's picture scripts.
- **Make them all, whatever they show.** The PR step picks which go in and judges what's fine to publish.
- **They go in `<plan folder>/media/`,** named after the check, like `criterion-2.png` and `criterion-2.mp4`. `media/media.md` has one line per file: the file, its check, the verdict, and what it shows.
- **No picture scripts in the fixture,** or no fixture: take them with the tools you drive it with, like a browser's screenshot and recording, and say how under Setup.
- **On a second run,** replace the files of each check you try again, so `media/` always shows the latest build.

## Verdicts

- **pass:** you did it and saw what the plan says.
- **broke:** you saw something else. Give the steps from a fresh setup and what you saw.
- **couldn't try:** say why.

Reading the code is not trying it: a criterion you only read is **couldn't try**.

After each `risks.md` line, add its verdict (`→ pass`, `→ broke`, `→ couldn't try`), so the file shows what's still open.

## Second run

Try again everything that broke or couldn't be tried, and each criterion the fixes touched. Anything still broken goes to the user, not to another fix round.

## Clean up

Stop every program you started. Leave the temp folder and say where it is.

## Output

One line per check, broke first:

```
<pass|broke|couldn't try>: <the criterion or risk, short>. <what you did and saw; for broke, the steps to reproduce>
```

Then three lists:

- **For the fixer:** every broke line.
- **For the user:** every couldn't-try line, every manual criterion, every change you made to the fixture and, on a second run, anything still broken.
- **Setup:** how you started the throwaway copy, when the project had no written way.

Then the path to `media/media.md`.
