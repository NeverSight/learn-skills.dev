---
name: chofex-hackathon
description: Apply to Hack the Andes for a human with the andes CLI, work through a challenge with them, check an existing application, or guide accepted-participant next steps. Use when a person wants an agent to apply, solve a Hack the Andes challenge, check status, understand requirements, reapply after rejection, or confirm attendance.
---

# Hack the Andes

Use the andes CLI to act on the participant's behalf while keeping identity,
consent, challenge direction, and final submission decisions with the participant.

## Pace

Move quickly and proactively. Run routine, non-destructive setup, schema, status,
and requirements commands without asking permission or narrating each command.
Batch participant questions into the fewest practical turns. Pause only for:

- browser authentication;
- confirmation that the authenticated email belongs to the participant;
- application answers that are missing or genuinely ambiguous;
- the participant's own consent decisions;
- challenge experiment selection, continuation checkpoints, evidence review,
  and release judgment;
- final submission approval; and
- private accepted-participant details.

Mechanical formatting is not personal-data invention. Normalize obvious handles
and domains, show the result in the final application summary, and let the
participant correct it before submission:

- GitHub `cuevaio` or `@cuevaio` becomes `https://github.com/cuevaio`.
- LinkedIn `cuevaio` or `@cuevaio` becomes
  `https://linkedin.com/in/cuevaio`.
- A profile URL or bare domain missing a scheme gets `https://`.

Ask a follow-up only when the input is malformed or has more than one plausible
meaning that would materially change the application. State low-risk parsing in
a concise interpretation note immediately before the final summary instead of
interrupting the interview. Preserve participant-provided wording and casing for
personal answers.

## Command setup

1. Check for the current CLI capabilities with `andes --version` and
   `andes validate --help`.
2. If either command is unavailable, install or upgrade proactively with
   `npm install --global hacktheandes-cli@latest`; do not delegate installation
   to the participant.
3. Verify both commands. If global installation is unsupported or fails for
   lack of permission, use `npx --yes hacktheandes-cli@latest` as the command
   prefix. When working inside the Hack the Andes repository,
   `bun run --filter chofex-cli dev --` is also an acceptable fallback. Ask the
   participant for help only when installation requires an interactive
   administrator or credential step that the agent cannot perform.
4. Use `--output json` for every command the agent needs to interpret. JSON
   responses are versioned envelopes with `ok`, `requestId`, and either `data`
   or `error`.

Use one consistent command prefix for the whole session. The CLI already targets
the Hack the Andes service, so use the default URL.

## Authenticate the participant

Run:

```sh
andes --output json whoami
```

If authentication is required, ask the participant to run `andes login` in
their own interactive terminal and finish the browser flow. Then run `whoami`
again and ask them to confirm that the returned email is theirs. Login tokens
belong in the operating-system credential store. Treat `CHOFEX_TOKEN` as a
secret and keep it out of chat, command arguments, logs, and files.

Authentication is complete only when `whoami` succeeds and the participant
confirms the email.

## Apply

First, check whether the participant already has an application:

```sh
andes --output json status
```

If one exists, report its status and follow **Next steps**. Start an application
when there is no application, resume and submit it when the status is `draft`,
or let a rejected participant apply again. A rejected application remains in
history. The participant may submit the application before completing a
challenge, but the application alone never reserves a seat. Technical challenges
are mandatory for admission, and organizers select the strongest engineers from
their ranked results. Only the latest server-advertised challenge version counts;
legacy attempts remain historical. Every selected engineer must also have a
submitted application before being accepted.

Get a fresh input template instead of relying on a memorized schema:

```sh
andes schema --stage application
```

The output is an example shape, not an application draft. It contains every
supported JSON key. Copy those keys exactly; for example, use `fullName`,
`role`, `phone`, `bio`, `portfolioUrl`, and `shippedProject`. Never save or
submit the example values.

Collect every field in one compact batch when practical. Accept a natural,
unlabeled reply and map it using context; numbered formatting is optional. For
open-ended fields, ask directly in chat or use an input whose selectable choices
are actual answers such as “Omit.” A placeholder choice such as “Enter all
answers” is not an answer and must not be offered. Ask only for fields the
participant has not already answered. Group the questionnaire so the participant
can scan and answer it naturally:

- required profile: full name, role, and country of residence;
- optional profile: phone number, bio, portfolio URL, something they have
  shipped, LinkedIn, and GitHub URLs; and
- required Terms and Conditions.

Explain these rules while collecting answers:

- Registration is for the in-person event in Lima, Peru. The application uses
  the authenticated account's primary email.
- `fullName`, `role`, and `countryCode` are required. Ask for the participant's
  country of residence and use its ISO two-letter code. Do not assume Peru.
- The participant chooses their country once. Only the organizers can correct
  it after reviewing LinkedIn or other social profiles. Reuse the saved country
  on reapplication. Existing participants with no country can select it with
  `andes country --code PE`, replacing `PE` with their actual country.
- Before submitting a country other than Peru, explain that the event is in
  Lima and participants outside Peru must cover their travel costs. Travel
  support is reserved for exceptional talent residing in Peruvian cities other
  than Lima. Do not promise travel support.
- Every field grouped under optional profile is optional.
- `codeOfConductAccepted` must be the participant's explicit `true`; an agent
  cannot consent for them.

Treat the fresh schema as authoritative. On local validation errors, use
`error.details.acceptedFields` to correct payload keys. Inspect CLI source only
when the schema and error details do not resolve the problem.

Before requesting required consent, give the participant this link:

- `https://hacktheandes.com/terms`

Ask for the Terms and Conditions decision by name. An agent cannot consent for
the participant. If they do not accept, do not discard the answers already
collected. Ask whether they want to cancel registration or read the document and
explicitly accept it. Continue from the consent step if they accept; do not
submit if they cancel.

Once every answer and consent choice is settled, submit the application. Do not
claim success until `registration.status` is `submitted`. Create exactly one
mode-600 temporary application file outside the project. On a POSIX system:

```sh
application_file="$(mktemp)"
chmod 600 "$application_file"
printf '%s\n' "$application_file"
```

Record the exact printed path and reuse it for every later operation. When shell
state does not persist between commands, use that literal path; never guess,
shorten, or replace it. One application uses one payload file, one recorded path,
and one cleanup.

Write only participant-provided answers to that file and omit unanswered optional
fields. Validate it locally before asking for submission approval:

```sh
andes --output json validate --stage application --input "$application_file"
```

Resolve validation errors before continuing. First state every low-risk
interpretation or normalization in a concise note. Then show a readable summary
of the exact validated payload, include every consent, and ask: **Submit this
application now?** Run the submission only after an explicit yes given at this
point.

```sh
andes --output json register --input "$application_file"
```

A successful submission returns `status: "submitted"`. Keep the mode-600
temporary file through correctable validation failures so a retry does not
require rebuilding it.

## Work through challenges together

Challenge solving is a participant-directed conversation. Routine setup,
reading the contract, and checking existing status or observations may proceed
without interruption. Before spending queries or implementing a solution,
explain the next hypothesis or change in plain language and ask the participant
which direction to take. Wait for their reply before proceeding.

Keep each approved round small: one hypothesis, at most three new oracle
queries, or one agreed implementation change with its free local tests. Explain
what the inputs distinguish before querying. Do not launch a script that spends
the whole query budget, chain multiple rounds, or continue solving in the
background while waiting for the participant.

After each round, show the evidence, what it supports, what remains uncertain,
and the remaining budgets. Ask the participant to choose the next hypothesis,
change the plan, or stop. They may select a proposed option or say "continue"
after a concrete next round has been described. Their reply authorizes only
that round. A general "solve it for me", "keep going until finished", silence,
or an earlier approval does not replace later checkpoints in this challenge
workflow. Do not invent the participant's direction or answers.

Before every official evaluation, show the solution changes, free-test results,
unverified assumptions, and remaining evaluation count. Ask whether to spend
one evaluation on that exact solution and wait for an explicit reply. After the
result, explain its limits and pause again before edits, more queries, or another
evaluation. A notebook-perfect result does not prove hidden correctness; an
aggregate score does not identify a missing rule.

These conversational checkpoints supplement the source-bound participant
reviews required by Broken Agent and Slow Service. They do not replace those
reviews or claim that the server verifies human involvement.

## Black Box challenge

**The Shipping Machine** is one of the technical admission challenges. It does
not block application submission, but challenge participation is mandatory to
compete for a seat. Rankings—not the application prose alone—identify the
strongest engineers, and organizers record acceptance manually on the submitted
application. The challenge slug always resolves to the latest version; never use
a historical attempt as completion. List challenges, then inspect the currently
available challenge:

```sh
andes --output json challenge list
andes --output json challenge show --challenge black-box
```

AI tools are allowed. The oracle is personalized, so a leaked solution will not
match this participant's function. Design experiments: change one variable at a
time, look for thresholds, then test combinations such as fragile and express
together. Each successful new input consumes one of 25 queries; duplicate or
failed queries are free. Follow the participant-directed rounds above.

```sh
andes --output json challenge query --distance 1 --weight 1 --hour 12 --fragile false --express false
andes --output json challenge notebook --format json
```

After collecting observations, write `function calculateShipping(input)` in a
local file. Test against the notebook (does not consume an official evaluation),
then evaluate against the hidden set (limited to 3 official attempts):

```sh
andes --output json challenge test --source "$PWD/shipping.js"
andes --output json challenge evaluate --source "$PWD/shipping.js"
```

Never ask the participant to paste a solution that they did not run. Application
submission and challenge completion are separate operations, but both belong to
the admission path. Report application success only when the envelope has
`ok: true` and `registration.status` is `submitted`. Never describe that state as
waiting with no action: proceed to the open challenge and explain that a seat is
earned through ranked challenge performance.

Public rankings are read-only:

```sh
andes --output json challenge ranking --challenge black-box
```

## Broken Agent challenge

When the participant asks to solve, submit, or evaluate challenge 2 or
`broken-agent`—including when the default `andes challenge` guide identifies
Broken Agent—read and follow
[`references/broken-agent.md`](references/broken-agent.md). It defines the
required human–agent reasoning loop and the source-bound review needed before an
official evaluation.

## Slow Service challenge

When the server lists challenge 3, `make-it-fast`, as open, read
[`references/slow-service.md`](references/slow-service.md). Its canonical version
is `slow-service-v3`. It uses source-bound companion review and browser/passkey
approval of the exact implementation. AI help is allowed in both stages. Do not
invent evidence or the participant's decision. The approval records responsibility,
not proof of understanding or independent authorship.
Check `challenge list` before starting; a closed challenge retains its ranking
and historical results but does not accept new submissions.

## Power Grid challenge

When the participant asks to solve challenge 4 or `power-grid`, or the server
advertises it as available to their account, read
[`references/power-grid.md`](references/power-grid.md). Apply the conversation
checkpoints above throughout discovery, implementation, and evaluation.

## Next steps

Read the application and server-calculated requirements together:

```sh
andes --output json status
```

The `status` response includes `requirements`. Run the separate `requirements`
command only when the status response omits them or the participant specifically
asks for requirements alone.

Interpret the returned state as follows:

- `draft`: this is an application left by an older CLI flow. Show
  `requirements.parts` and missing fields, collect the complete application,
  and use `andes register` to submit it. Then continue to the open mandatory
  admission challenge; do not delay application submission for challenge work.
- `submitted`, `under_review`, or `waitlisted`: report the exact status and
  requirements. Make clear that the application has been received but no seat
  is assigned. Run `andes challenge list`, identify the open challenge, and
  continue its required human–agent flow. Never tell the participant to merely
  wait while an admission challenge is open.
- `rejected`: show the review feedback when present. Offer a new application
  only if `canSubmitNewApplication` is true. Interactive `andes register`
  presents the rejected application's answers as editable defaults. Obtain a
  fresh submission approval rather than silently resubmitting old answers.
- `accepted`: congratulate the participant and explain any `missing`
  acceptance fields. Continue to **Confirm attendance** only when
  `canSubmitAcceptedDetails` is true.
- `withdrawn`: report the status and follow only the actions returned by the
  server.
- requirements stage `complete`: attendance details are complete; report that
  there is no remaining CLI action.

Return the exact rejection reason, missing-field reasons, and server state.
The server response is authoritative when it differs from this summary.

## Confirm attendance

Acceptance details include the participant's full name exactly as it appears on
their ID document, birth date, national ID or passport number, emergency
contact, a required profile-picture confirmation, and other private information.
The participant must explicitly choose their Clerk picture, their
GitHub avatar, or a custom upload; never infer this choice from an available
image. Recommend that the
participant keep these values out of agent chat by running this themselves in
an interactive terminal:

```sh
andes confirm
```

If the participant explicitly asks the agent to submit them instead, fetch a
fresh template with `andes schema --stage acceptance`, collect every required
value without guessing, store it in a mode-600 temporary file outside the
project, and avoid printing its contents. `dateOfBirth` uses `YYYY-MM-DD` and
must be a real date in the past. Shirt size is required for this in-person
event. Validate the file with
`andes --output json validate --stage acceptance --input /path/to/private-attendance.json`;
the success response does not echo its contents. Resolve validation errors, then
obtain a fresh **Submit these private attendance details now?** approval and run:

```sh
andes --output json confirm --input /path/to/private-attendance.json
```

When `pictureSource` is `upload`, ask for the image's path on the participant's
computer and add `--picture /that/path/image.png` to the confirm command. Do not
copy image bytes into the JSON file or chat. The CLI accepts JPEG, PNG, and WebP
files up to 5 MB, waits for the upload and verification to finish, and displays
upload progress on stderr. Custom uploads are available only after acceptance
and are limited to five attempts per 24 hours.

Delete the file immediately after the command completes. Run `status` again
and verify that the requirements stage is `complete` before reporting that
attendance confirmation is done.

## Failures

On `ok: false`, report `error.code`, `error.message`, and `requestId`. Resolve
local validation failures before showing the final summary. Correct mechanical
issues directly when the participant's answers do not change; involve them when
an answer or consent must change. Any payload change after final approval
invalidates that approval: show the updated summary and ask again. Retry an
unchanged failed request only when `retryable` is true and after fresh submission
approval. For authentication failures, return to **Authenticate the
participant**. Preserve the request ID for support instead of claiming success
or bypassing a failed state.
