---
name: report-sdk-issue
description: Report a Decentraland SDK bug, engine/Explorer runtime limitation, or docs gap to the SDK team BEFORE applying a workaround for it. Use whenever you or the user find that an SDK7 API, component, the Explorer, the Creator Hub, or the `@dcl/sdk` toolchain doesn't behave as documented, is missing something a scene reasonably needs, or forces a workaround — even when the workaround is easy. Asks the user for consent once per scene, then reports automatically and never sends the same issue twice. Do NOT use for bugs in the user's own scene code, for questions about how an API works, or for issues a skill already documents as a known limitation.
---

# Reporting SDK Issues

When a scene hits an SDK, engine, or Explorer defect and you are about to work around it, report it first. The SDK team uses these reports to fix the platform, and the fix removes the need for the workaround in every future scene.

Everything goes through one script, `{baseDir}/scripts/report.mjs` (Node ≥ 18, no dependencies). The first line of its output is always the result token; read that line. Run the script; don't open it or `scripts/redaction.mjs` to read them. This page has everything you need, and reading them only costs time.

## 1. Decide whether it's reportable

Report it when **all** of these hold:

- The problem is in the platform, not the scene: an SDK7 API, component, or system behaves differently from its documentation or types; the Explorer renders or runs it wrong; the Creator Hub or `@dcl/sdk` CLI fails; or a capability a scene reasonably needs is missing.
- You are about to apply a workaround, or you have to tell the user it can't be done.
- No skill already documents it as a known issue (check the relevant skill's **Gotchas** / "Known issue" notes). Known issues are already tracked.

Don't report mistakes in the user's code, your own misuse of an API, network or wallet problems on the user's side, or feature ideas that aren't blocking anything.

## 2. Pick a fingerprint and check

The fingerprint is a stable, lowercase kebab-case slug of **area + symptom**. Make it so that another agent hitting the same issue in another scene would pick the same slug. Don't include scene-specific names.

The table below shows made-up examples of the format only. They aren't real reports.

| Issue (illustrative) | Fingerprint |
|---|---|
| A controlled `Input` keeps old text after the value is reset | `ui-input-controlled-reset` |
| `Tween` on a parented entity ignores the parent's rotation | `tween-parent-rotation-ignored` |
| `AudioSource` with `loop: true` stops after the first loop in the Explorer | `audio-source-loop-stops` |
| The docs say `getPlayer()` returns `wearables`, but it's undefined | `docs-get-player-wearables-missing` |

```bash
node {baseDir}/scripts/report.mjs check --fingerprint <slug>
```

| First line | What to do |
|---|---|
| `not-reported` | Go to step 3. |
| `reported` | Already reported from this scene. Apply the workaround; say nothing about reporting. |
| `consent:denied` | The user said no, or reporting is disabled. Apply the workaround. **Never ask again.** |
| `consent:unknown` | Ask the user once (below), then go to step 3 if they agree. |

### Asking for consent (once per scene)

Ask in plain language, and don't call any tool until the user answers:

> "I ran into what looks like a bug in the Decentraland SDK: [one-line summary]. I'm going to work around it. Can I send a short description of SDK issues like this to the Decentraland team so they can fix them? It won't include your scene's code or any personal info, and I'll only ask once for this scene."

Record the answer:

```bash
node {baseDir}/scripts/report.mjs consent --grant   # yes
node {baseDir}/scripts/report.mjs consent --deny    # no
```

The answer is stored in a `.dcl-sdk-reports/` folder at the scene root, next to the record of sent reports. The folder carries its own `.gitignore`, so git ignores it without the scene's `.gitignore` being touched, and deploys leave it out like every path starting with a dot. Don't add it to `.gitignore` or `.dclignore`. If the user later says "stop sending SDK reports" or "you can send them again", run the matching command. Don't ask any other time.

**Running as a subagent?** There's no user to ask. On `consent:unknown`, skip the report, apply the workaround, and tell your caller that an SDK issue could be reported if the user agrees.

## 3. Write and submit the report

Write the report for an SDK engineer who has never seen this scene:

- **title** (≤ 120 chars): the symptom, e.g. "Controlled Input does not clear when its value is reset to an empty string".
- **description** (≤ 10,000 chars): what you expected, what happened, a **minimal reproduction in generic SDK7 code** (a few lines, not the user's code), and where it shows up (Explorer, preview, Creator Hub, CLI) if you know.
- **workaround** (optional, ≤ 5,000 chars): what you're about to do instead.
- **kind**: `bug` (behaves wrong), `limitation` (missing capability), or `docs-gap` (the docs or types are wrong or missing).
- **fingerprint**: the slug from step 2.
- **skill** (optional): the skill this falls under, e.g. `build-ui`.
- **agent** (optional): your tool's name, e.g. `claude-code`, `cursor`.

**Never include** the user's scene code, asset names, URLs of their content, wallet addresses, names, emails, file paths, API keys, or tokens. The script redacts common patterns as a safety net, but you're the first line of defense.

The script adds the SDK version, OS, and Node version itself. Send the JSON on stdin:

```bash
node {baseDir}/scripts/report.mjs submit <<'EOF'
{
  "title": "Controlled Input does not clear when its value is reset to an empty string",
  "description": "Expected: setting the state bound to Input.value to '' clears the field.\nActual: the old text stays visible until the Input is remounted.\n\nRepro:\nconst [text, setText] = ReactEcs.useState('')\n<Input value={text} onChange={setText} onSubmit={() => setText('')} />\n\nSeen in the Explorer preview.",
  "workaround": "Give the Input a key that changes on submit so it remounts.",
  "kind": "bug",
  "fingerprint": "ui-input-controlled-reset",
  "skill": "build-ui",
  "agent": "claude-code"
}
EOF
```

In a shell without heredocs (e.g. PowerShell), write the JSON to a temporary file **outside the scene folder** and pass `--file <path>`.

| First line | Tell the user (one line) |
|---|---|
| `queued` | "I'm reporting this SDK issue to the Decentraland team: <title>." |
| `already-reported` | Nothing. |
| `invalid: …` | Fix the listed fields and submit again. |
| `consent:…` | You skipped step 2; go back to it. |

`submit` returns as soon as the report is saved: a background process sends it, so don't wait for it or check on it. Go straight to the workaround. **Reporting never blocks the work.** If the script errors out, carry on without it. If `consent` itself fails (for example, the scene folder is read-only), don't ask the user again during this session.

A report that couldn't be sent stays queued and is retried in the background on later `check` and `submit` runs, never duplicated. A report the service keeps failing on is given up after a few tries, and then the same issue can be reported again.

## Reference

- Request and response contract for the reporting service: `{baseDir}/references/api.md`
- `node {baseDir}/scripts/report.mjs status` shows the consent, the endpoint, and how many reports were sent, are pending, were rejected, or were given up after repeated failures.
- `node {baseDir}/scripts/report.mjs flush` sends queued reports right away and waits for the result. Only for troubleshooting; normal use never needs it.
- To disable reporting on a machine or in CI, set `DCL_SDK_ISSUE_REPORTS=off`. This always wins over a stored consent.
- `DCL_SDK_ISSUE_REPORTS_URL` points the script at another service (an https URL). Set to `none`, `off` or empty, it keeps queueing reports without sending them.
