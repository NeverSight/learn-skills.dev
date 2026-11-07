---
name: shipper-ship
description: A quick frame of reference for how to scaffold and publish a PR from a completed Shipper plan
---

The goal of this skill is to create a Pull Request that is easily reviewable by a senior engineer that briefly (but thoroughly) explains the following pieces of information:

1. What was added, removed, or modified in this codebase
2. What existing codebase conventions were followed throughout the execution of the plan
3. What existing pieces of the codebase were reused instead of rewritten
4. What steps were taken to test or harden the code that is included in the PR

Before anything else, read and follow [./CONFIG.md](./CONFIG.md). It tells you where plans, spikes, bugs, reviews, and modules live in this repository (written below as `<plans>`, `<spikes>`, `<bugs>`, `<reviews>`, and `<modules>`) and which team and personal preferences apply.

One of the best reference points you'll have is the Shipper plan that is associated with this PR to review the notes that were left behind at the end of each Phase from the build engineers. This should be your starting point for understanding what was completed and how it was completed.

From there you'll do a light set of context gathering to verify the things that were built during the Shipper plan to confirm the critical pieces of the plan were completed as intended.

The format of your PR should be the following five sections, in this order (these are the high value things a senior engineer will be looking for):

1. What & Why
- One or two sentences stating what this PR does and the problem it solves.
- Explicitly state what the PR deliberately does NOT do (non-goals). If any changed files look unrelated to the stated goal, explain why they were touched. Unexplained diffs in unrelated files are the fastest way to lose a reviewer's trust.

2. How to Verify in 2 Minutes
- Give the reviewer an exact recipe to smoke-test the happy path themselves: the command to run, the URL to visit, what to click, and what they should see.
- This must be self-serve. Assume the reviewer will not ask the author questions; if they can verify the core behavior in two minutes, the review goes dramatically smoother.

3. Test & Hardening Evidence
- Show proof the code was actually executed, not just written. Paste real output: the test run results, a screenshot of the working UI, the request and response, the query result.
- Claims like "tests were added" or "verified working" carry no weight on their own. Evidence of execution is the one thing that cannot be faked, so lead with it.

4. Reuse & Convention Receipts
- List the specific existing code that was reused instead of rewritten, and the specific conventions that were followed, each with a link to the relevant file (e.g. "reused `formatCurrency` from `lib/format.ts`", "followed the service/route pattern from `services/orders.ts`").
- Vague statements like "followed existing conventions" carry zero information. Every claim here should be spot-checkable by the reviewer in seconds. Pull these from the Completion Notes in the Shipper plan, then verify them against the actual code before writing them down.

5. Risks, Gaps & Least-Confident Areas
- State the blast radius: which existing flows share the code that was touched, whether anything hard-to-reverse (schema, auth, billing) was changed, and how easily the PR can be reverted.
- Honestly list anything skipped, stubbed, or left as a TODO, and name the specific area of the change you are least confident in. This tells the reviewer exactly where to spend their limited attention. A description with zero admitted uncertainty reads as "the AI wrote this and nobody read it."

Guidance on tone and length — the description must not read like AI prose:

- Keep the entire description skimmable in about 15-20 lines. A senior engineer will read a short, dense description; a wall of confident, polished prose is itself a red flag and gets skipped entirely.
- Never restate the diff. Do not write "modified `foo.ts` to add a function" — the reviewer can already see that. Every line must contain something the diff cannot tell them: intent, evidence, risk, or verification steps.
- No marketing language. Cut words like "comprehensive", "robust", "seamless", and "enhanced". Prefer plain, specific statements ("retries 3 times then logs and drops the event") over adjectives.
- No filler structure: no summary-of-the-summary, no emojis, no conclusion paragraph. If a section has nothing meaningful to say, write one honest line (e.g. "No known risks beyond the new table migration") rather than padding it.
- Write it like the author would explain the change to a teammate at their desk, including the parts they are unsure about.

Read and follow [./GIT.md](./GIT.md) for locating the branch, pushing, creating the PR, writing `pr_url` and `pr_number` into frontmatter on the branch, and restoring the user's branch if ship switched checkouts. Utilize the command line to create the PR and return a link for the user to review.

`pr_url` must be the full canonical GitHub PR URL returned by `gh pr create` (not a comparison or branch URL). `pr_number` is the integer PR number. These fields power the Shipper UI's PR link. If frontmatter already exists, add or update only `pr_url` and `pr_number` without changing other keys.