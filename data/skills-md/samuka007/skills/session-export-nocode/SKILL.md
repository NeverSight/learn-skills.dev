---
name: session-export-nocode
description: "Human-invoked /session-export-nocode direction command for exporting non-code trajectory sessions after an explicit user request."
---

# Export the non-code direction

This is an explicit, human-invoked delivery action. The published frontmatter
uses only fields accepted by the Agent Skills specification, so
`disable-model-invocation` is not emitted: the current `skills-ref` validator
rejects that nonstandard field. The narrow description and the launcher keep
this direction user-invoked. Install it together with the base skill; Agent
Skills has no dependency field:

```bash
npx skills add Samuka007/skills \
  --skill session-export-nocode --skill agent-session-batch-export -g -y
```

## Run

Read the bundled [`direction.json`](direction.json) before invoking the
launcher. It is the direction's single metadata file. Its `themes` array
declares exactly these themes, each resolved by name against the base skill's
`themes/`:

`role-play` (角色扮演), `writing` (写作), `planning` (策划),
`report-analysis` (报告分析).

Each entry is a `{ "theme": NAME }` object with an optional per-theme
`override`; the four shipped entries are plain names. What the purchase
constrains lives in the direction's root `override`: the `exclude_keywords`
word list — the coding-signal terms whose absence defines "non-code" — and
the packaging bar, one deliberate number (`min_user_turns`) that makes
entries match the reference bundle's multi-turn caliber. Its value lives in
`direction.json`, not here. Every other stage comes from the base skill's
`scripts/policy.json`, and no file in this skill restates those values.

Choose an output directory, then run:

```bash
bash scripts/session-export-nocode.sh \
  --out "$OUT_DIR"
```

`--out` is required. `--request "$FULL_USER_REQUEST"` is still accepted for
backward compatibility with earlier callers, but it is used by no gate and
forwarded nowhere: the launcher's behavior no longer depends on the wording
of the request.

Forward the scan options when the user supplied them:
`--allow-credentials`, `--agent`, `--workspace`, `--since`, and `--min-lines`.
The launcher resolves the standard sibling installation of
`agent-session-batch-export` and calls its shared contract:

```text
agent-session-batch-export/scripts/export-direction.sh \
  --direction-file FILE --out DIR ...
```

The launcher is only an adapter. The base runner owns scanning, the Python
funnel, the policy thresholds and their overrides, credential checks,
selection, copying, manifests, and delivery. Do not implement or substitute
any of those stages here.

## Review policy

**The default is unattended.** The launcher always calls the base runner with
`--yolo`: the deterministic funnel decides the selection, no batch-level
prompt appears, and the manifest records `batch_confirmed=false`. There is no
phrase gate any more — it used to derive `--yolo` from the phrases `直接导出`,
`无需确认`, `不用确认`, `无须确认`, and omit the flag for every other request;
whether the request says `直接导出` or `帮我导出` now makes no difference on
this path.

When the user's request explicitly asks to be asked first — 先确认, 让我审一遍,
需要我确认 and the like — pass `--confirm`: the launcher then omits `--yolo`,
and the base runner prints one batch-level `[y/N]`. Answering `y` delivers
with `batch_confirmed=true`; EOF or any other answer exports nothing. This is
a batch-level checkpoint only: there is still no row-by-row screening step on
this path and no decision surface to fill.

History, for explaining an older installation: the retired gate matched only
the four exact phrases above, and matched them anywhere in a longer request;
brevity, silence, or `帮我导出` kept the prompt. Do not edit funnel output or
any `candidates.tsv`, `screen.tsv`, or `decisions.tsv` file. The funnel report
may be inspected only for a catastrophic run problem; it is not a decision
surface and must not be rewritten. Never choose keep/drop rows or create a
second screening engine.

## Actionable failures

Surface the base runner's preflight output unchanged. If Python is unavailable
on Windows, show its `winget install Python.Python.3.13` hint and ask the user
whether to install it and retry. Never replace deterministic funnel screening
with semantic model screening.

By default the runner EXCLUDES credential-bearing sessions from the delivery
(they are never written) and reports each exclusion — the source and the
credential kinds — plus the total; relay that list to the user. The remaining
sessions deliver normally, and the exclusions are recorded in the manifest.
`--allow-credentials` includes them instead: that is an explicit human
decision, so offer it and never add it silently. If the base skill itself is
missing, show the launcher's install instruction and ask the user to install
the two skills together.
