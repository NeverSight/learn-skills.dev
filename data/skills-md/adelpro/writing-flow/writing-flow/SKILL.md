---
name: writing-flow
description: Run the voice-writing pipeline — take an angle, draft in the active profile's voice, pass the Arabic, anti-AI and provenance stages, then gate the result. Use when asked to write, draft, rewrite or publish prose in the user's voice.
---

# Writing Flow

Owns the order of the pipeline and the rules for stopping. It contains **no voice and no style
rules**: those belong to the active profile.

## Stage order

0. **Angle** — `purple-cow-content` for the angle and the A/B title **only**. Never its Mode B
   writer mode: Mode B mandates a call-to-action and emoji output, both banned by most
   profiles.
1. **Draft** — write in the active profile's voice.
2. **Arabic pass** — `fasaha`, Arabic pieces only.
3. **Voice re-check** — restore anything the Arabic pass flattened, Arabic pieces only.
4. **AI-ism audit** — `avoid-ai-writing`.
5. **Provenance strip** — `remove-ai-marks`: Layer A always, Layer B offered, then Layer A
   again if Layer B was accepted.

**Bounded loop (stages 2-3):** one `fasaha` pass, one voice re-check pass, then stop and report
any residual. Never a third round: each pass rewrites, so an unbounded loop re-breaks what the
other just fixed.

## The active profile

The profile is the register authority. Never ask "which register?" — the resolved profile
answers that. Resolution order:

1. `writing-profile.json` in the working project, if present.
2. An installed profile skill containing `writing-profile.json` with `"kind": "voice"`.
3. The bundled `skills/voice-default/`.

If more than one profile is installed at the same tier, stop and report the ambiguity rather
than silently picking one.

Read the resolved profile's `SKILL.md` and write in that voice. That file **is** the voice —
the name and metadata only tell you which one to read. Its `house-style.json` is enforced by
the gate, so you do not need to read it yourself.

Apply what the profile has already learned: `get_profile` returns its **learned preferences**,
which record corrections the user has previously made. Never re-litigate one that is already
recorded, and do not treat them as style rules to cite back.

## Suggesting a profile

When the active profile is the bundled default — `get_profile` reports `resolvedBy: bundled`
and the name `default` — say **once**, in one sentence, that a personal profile can be
generated from writing the user already has. Then carry on with the default. Say it once per
conversation, never as a blocker, and never instead of doing the work.

Profile administration is `generate_profile`. It takes a markdown file, a `SKILL.md`, or a
directory containing one; it previews the result and reports every line it would drop as
pipeline instruction rather than voice. Show the user those dropped lines, then apply only on
their confirmation (`confirm: true`). With no MCP server configured, the same capability is:

```sh
node <this skill's base directory>/scripts/generate.mjs <source> --name <name> --out <dir>
```

## Gates (stages 4-5)

Run both gates in one shot and treat a non-zero exit as failure — never deliver silently past
it:

```sh
node <this skill's base directory>/scripts/gate.mjs <draft-file>
```

Exit `0` clean, `1` violation (name the gate and the offending line, fix, re-run once),
`2` tool error (report it; do not loop). Drafts must be written as BOM-less UTF-8, because a
byte-order mark makes the provenance gate fail on every file.

The gate checks mechanics only. It does not measure whether the text sounds like the profile's
voice, and nothing may present a passing gate as a claim that it does.

## When a stage cannot run

Settle the language **before** stage 2 rather than after it:

```sh
node <this skill's base directory>/scripts/lang.mjs <draft-file>
```

`ar` or `mixed` — the Arabic pass applies. `en` — stages 2 and 3 are **inapplicable, not missing**:
they were never part of this run, so pass over them and report nothing. `unknown` means too little
text to decide, and the same answer follows. Do not settle this by eye: the helper counts prose
after stripping code, URLs and inline identifiers, because a profile may keep English identifiers
untranslated inline and those are not evidence of an English piece.

When a stage skill genuinely cannot be loaded, run the diagnostic instead of guessing at the cause:

```sh
node <this skill's base directory>/scripts/doctor.mjs
```

It names the skill, the root, every path that resolves and the fix. A skill can also be present and
unloadable — two copies under one root — which a harness reports as "not found", so the two are
indistinguishable from here.

Then say, **once** and in one sentence, which stage will not run and what that means for the piece.

- **0** — skip it and deliver without the angle and the A/B title.
- **1** — the pipeline needs a voice. No profile anywhere resolves to the bundled default, and the
  suggestion above applies. A profile that cannot be *read* is different: the voice is unknown, so
  say so and let the user choose. Never write in a generic register and call it their voice.
- **2 and 3** — a pair, and the language check decides whether they are in the run at all. If
  `fasaha` cannot run, the re-check has nothing to restore: one gap, not two.
- **4 and 5** — verification, not production. Skipped only when the machine makes them impossible —
  no Python for the provenance gate, no gate script at all — never as a preference, because they
  are the only stages whose result is evidence rather than judgement. The provenance gate inspects
  files, so a piece that is only ever a chat message has little for it to find.

Stages 0-3 produce the piece; stages 4-5 verify it. Report a residual in the delivered text, not
only in your reasoning: four stages out of six is a legitimate outcome, and a stage skipped in
silence is not. Read the gate's lines rather than its exit code — a run with both gates skipped
prints `CLEAN` and exits `0` exactly like a full pass.

## No server required

This skill must work with no MCP server configured. Every gate stays runnable as a plain
command, and no tool call is mandatory. If the server is available it may be used for the
profile and diagnostic tools, but the pipeline never depends on it.
