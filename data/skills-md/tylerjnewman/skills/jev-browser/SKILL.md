---
name: jev-browser
description: "Browser work in Dex Work Chrome tabs the agent opens with `jb`: deep links, authorized chat input and PDF attachment, and Jev autopilot for unfamiliar navigation on approved sites. Use for quantum.loan QA or smoke tests, clicking through a website, a repeated form with a saved runner, or when Tyler says jev browser."
---

# Jev browser

`jb` (on PATH; otherwise `node <this skill's folder>/jb.mjs`) drives Chrome tabs it opened in the Dex Work profile. You fly every task and own its permissions, typing, and verification. Jev, TypeSafe's choice model at about 0.3 s a decision, is an optional **autopilot** for routine navigation: given one goal, it clicks and scrolls until it claims arrival or **disengages**. You **hand-fly** every other step, and you **land** every task yourself: autopilot's arrival is a claim until your own evidence shows the goal.

## Fly a task

1. **Choose the route.** Dex Work tasks go through `jb`. Localhost dev servers use the in-app browser preview tools with a minted session (`apps/quantum/CLAUDE.md`), except the isolated `jb` integration fixture at `http://jb-fixture.localhost:4173`, including its declared wrong-origin alias, which `jb` drives; other localhost servers keep that route. Oracle keeps its own route. Dex Personal stays closed to agents, including for recovery.
2. **Reuse a saved runner** before you explore a form: `grep -rlF "# jb-run origin=<origin> " runs/` in this skill's folder (the trailing space is part of the header). Read the header of each hit; when its `entry` and `account` fit your task, write the items as a JSON list of `{request_id, name, amount}` strings and, when this batch's consequential clicks are authorized by the task, launch it once: `python3 -I runs/<host>/<workflow>/run.py <items.json> --yes`. Skip to Close. The runner opens, verifies, and closes its own tabs, so read its result JSON against your request. Exit 2 (applicability stop) and 3 (uncertain write) hand the task back to you: read the reason line and resume reasoning from the printed state. After 3 never Create again until a readback shows whether the record exists. With no hit, continue.
3. **Open** with `jb open <url>` and note the tab id. On quantum.loan, `jb` prints `signed in as tnewman@quantafinance.com`, and re-checks that account, the app shell, and the address before every action and before every page goes to Jev. When it prints `NOT VERIFIED`, use the identity-recovery row below before requesting sign-in; keep the same owned Work tab and its guards.
4. **Name the landing** before acting: the record, the destination, the selected control, the loaded content, relevant errors, and any checkpoint the path itself must pass. Verify each checkpoint when you reach it; never chain across checkpoints that need their own evidence.
5. **Route each step** by the first row of the routing table that fits it.
6. **After autopilot**, do what its `next:` line says, starting from the state it printed; a menu or dialog it opened may still be open. Once you have hand-flown past a disengage, a fresh `jev` run can take over from the current page; after two disengages on one goal, hand-fly the rest. A disengage prints what Jev was torn between and the path of the run's record; an arrival claimed under 0.85 confidence is reported as a disengage.
7. **Land** with fresh evidence for every condition from step 4: `jb <tab> snap` (`snap <regex>` keeps matching lines; `snap --text <regex>` also searches page text such as prices, which can be clipped). A line in the snapshot does not prove it is on screen, so a visual claim needs `jb <tab> shot`, which prints the image's path, and your own look at the image. Missing evidence is Not covered, never Pass.
8. **Close** every tab you opened or were given with `jb <tab> close`. Use only tab ids from your own task, one agent per tab.

## Routing

| The step | Fly it |
|---|---|
| Profile, account, destination, or permission evidence is incomplete | Recover with bounded reads in the same owned Work tab: inspect the site's account/session state and task authorization, let a loading page settle, and retry the known entry URL once if needed. Resume when live evidence matches the authorized target. Ask only for a remaining account/target choice, required human sign-in, or materially broader authority; continue independent work. |
| Live evidence confirms a different account or destination | Pause actions that depend on that identity. Report the exact mismatch and request the missing account/target choice; keep independent authorized work moving. |
| Typing or keys | Hand-fly: `type "<field name>" "<text>"` (`""` names the focused field), `press` (arrows, Enter, Escape) |
| Attach a local PDF to Quantum full chat | `jb <tab> attach /absolute/path/file.pdf --yes`. Chrome selects the file directly; verify the filename and completed preview in `snap` before sending. |
| A known URL, when the clicks on the way are not under test | `jb <tab> go <url>` |
| Controls you have already seen, each with a unique name | Hand-fly: `jb <tab> click "A" "B"` with each name exactly as `snap` prints it; each waits up to 10 s to appear, so one call crosses page changes. A repeated name carries the text that sets it apart, as in `Open (in: 39 Crown Lane)`; pass it whole |
| A form you have already scripted on this origin | A saved runner: step 2 |
| An unfamiliar path on an approved origin | Autopilot: `jb <tab> jev "<one observable goal>"` |
| A native file chooser opened by an authorized chat `Attach file` click | Bring that same verified, owned tab forward with `shot --front`, then use `cua_repl` only on the observed file chooser to choose the approved file. Return to `jb snap` to verify the attachment. |
| A native dropdown, a frame, a drag | Not supported by `jb`: stop and tell Tyler |
| None of these, clearly | Snap and plan it yourself |

When the page opens a new tab, or asks to, `jb` stops before its next action or Jev request on the original tab, which ends a click chain or an autopilot run, and prints `opened new tab <id>` for each tab that appeared, even between commands. Each is yours to verify, drive, and close.

A profile label, plan/upgrade page or Google chooser is not proof of the site's signed-in identity. Recovery uses existing authorized Work sessions; it does not change accounts, open Dex Personal or weaken `jb` guards.

Autopilot runs only on origins Tyler approved in `~/.config/jev-browser/origins`, and only on the origin a run starts from. Each decision sends Jev the snapshot, minus the values of fields `jb` can type into, the goal, and the run's last ten actions through the AI SDK on Vercel AI Gateway, with zero data retention; `--allow "<regex>"` narrows what it may click but redacts nothing more. Keep mail, sign-in pages, and borrower lists hand-flown. Autopilot clicks only enabled, named, unique controls, never types, and skips toggles and consequential names such as save, send, delete, approve, fund, and sign; on quantum.loan it clicks only tabs and links.

A runner is a frozen script that hand-flies a repeated form. Freeze one only after the candidate itself has created and read back one item on a fixture or a scratch record and rejected one mismatch (wrong account, origin, or form state). Save it at `runs/<origin-host>/<workflow>/run.py` in this skill's folder. Line 1 is the header `# jb-run origin=<origin> entry=<path glob> account=<marker>`, for example:

    # jb-run origin=https://app.hubspot.com entry=/payment-links/*/create account=quanta-work
    # jb-run origin=http://jb-fixture.localhost:4173 entry=/ account=acme-test

Write the manifest, holding SHA-256 of every runner file, the applicability contract, and the per-item command limits, to `~/.config/jev-browser/manifests/<origin-host>/<workflow>.json`, beside `origins` and outside the runner folder. A runner exits 0 on success, 2 when the contract fails before any edit, 3 when a write's outcome is unknown. A consequential click inside a runner needs task authorization for that batch; `--yes` acknowledges it, rather than requiring a second approval.

## quantum.loan map

- A loan is `https://quantum.loan/loans/next/<id>` and opens on Funding Overview. Its other overview tabs are `?tab=<slug>`, for example `status`, `loan-fees`, `escrow-title`, `valuation`, `liens`; clicking a tab shows its slug in the URL.
- Loan sections are paths under the loan: `/loan-documents` (sub-tab `/loan-documents/templates`), `/asset`, `/insurance`.
- To find a loan without its id: click the search button (named like `Search... ⌘ K`; take its exact name from `snap`), `jb <tab> type "" "<LID, address, or borrower>"`, then check in the output that the `(selected)` option is the loan you mean before `jb <tab> press Enter`; when another option such as `Add to Favorites` is selected, `jb <tab> press ArrowDown` moves to the result first. The result opens in a new tab. Verify the new tab's record, then close both tabs when done.

## Boundaries

- quantum.loan supports navigation, search, and authorized chat input. `Open chat` opens the loan drawer. For the actual chat composer, use `type "Message Quantum" "<text>" --yes` in the loan drawer or `type "Message composer" "<text>" --yes` on the full-page `/chat`, then `click "Send message" --yes`; `Attach file`, queued follow-ups, and stop generation use the same task authorization. `--yes` acknowledges authorization already present in the conversation; do not ask again for an approved task. Loan edits, deletion, and other business actions remain outside this gate.
- `attach` uses the same verified Work session and authorization as `Attach file`, selects only the full-chat composer's PDF input, and triggers the app's normal preview. It does not submit a message. On an uncertain upload, inspect the draft before retrying; upload success requires the preview filename and ready state, then a saved document/result after sending.
- `cua_repl` is only for the file chooser an authorized chat `Attach file` click opens, in the same verified, owned Work tab; native tools do not create authority. After choosing the file, verify the filename and upload result before submitting the chat.
- Elsewhere, use `--yes` for consequential clicks, toggles and value-changing keys already authorized by the task. Ask only when the target or scope remains materially unclear; a retry, technical warning or already-approved action does not require fresh approval.
- `jb` keeps its tab rendering and sends real pointer and key input whether or not the Dex window is covered, and `shot` captures the tab without raising the window; it raises the window, and says so, only when no frame arrives within 3 s. Use `shot --front` only when the window itself must be on screen, such as for a native file chooser.
- `jb` touches only the tabs it opened and the tabs those opened.
- `JB_PROFILE=dev jb open <url>` opens the tab in the test profile signed in as dev@quantafinance.com, for sending test messages to Tyler's work account. Verify the account in the first `snap` before typing. Every other command works on that tab as usual. Dex Personal stays closed.

`jb --help` lists every verb and flag.
