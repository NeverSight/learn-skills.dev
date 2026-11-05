---
name: roblox-build-orchestrator
description: Runs a Roblox game build pipeline as a timed, logged run (market research, design, code, 3D/materials/UI/animation/VFX/SFX, assembly, playtest, publish), fans the asset block out to subagents while keeping every Studio write on one thread, enforces the write boundary, and keeps a timestamped ledger of stalls, fallbacks and interventions with a debts gate so a run cannot end with known defects. Use this whenever you are running or planning a full Roblox build, want the agent pipeline orchestrated, parallelised, or handed to a manager agent, mention an intervention counter, the 30-minute stall rule, or Tier 2 to Tier 1 fallbacks, or ask whether subagents would help a Roblox build. Also use it to rehearse the roster on a practice run before a build you care about, because an untested orchestration layer is a second variable.
---

# Roblox Build Orchestrator

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

Runs a Roblox game build end to end under a wall-clock cap, with a ledger that
doubles as the evidence of how the run went. The pipeline itself (stages, specs,
gates) is defined by the `create-roblox-game` skill; this skill times it, logs it,
and decides how the asset block is split across workers. It orchestrates the
stage skills (`roblox-3d-model`, `roblox-texture-gen`, `roblox-ui`,
`roblox-animation`, `roblox-vfx`, `roblox-sfx`, `roblox-map`); it does not replace them.

## Start here

If you invoke this skill, walk the user through the below and run the commands
for them. Nobody should have to remember any of it.

**Setup.** The worker definitions live in this skill's `agents/` folder and must
be installed where Claude Code reads agents. The pack's installer normally does
this. To confirm, or after a machine change:

```bash
mkdir -p ~/.claude/agents && cp ~/.claude/skills/roblox-build-orchestrator/agents/*.md ~/.claude/agents/
```

(`roblox-asset-map` is the seventh worker; it ships alongside the others in the
pack's `agents/` folder, and the same copy command installs it.)

**Every run, three steps:**

1. **Start the ledger.** `run_log.py init --run <name> --mode fanout`
2. **Run the pipeline**, bracketing each stage and logging every event as it
   happens. Details under *Mode B* below.
3. **Ask for the verdict.** `run_log.py decide`, then `run_log.py debts`.

## The rule that decides the architecture

**Fan out the asset block. Keep the spine on one thread. Measure both.**

The asset block (meshes, materials, UI, animation, VFX, SFX, and the map) is
mutually independent, all downstream of one design spec, and generation-heavy.
That is the shape fan-out is for, and `create-roblox-game` runs it that way by
default because of what was measured: the saving is not wall-clock, it is token
cost, in two independent halves. First, every tool call re-sends the whole
conversation, so a long single window costs closer to quadratic than linear, and
images (contact sheets, screenshots) re-send forever; in a worker they stay in the
worker. Second, per-agent model tiering only applies inside a subagent.

The spine is different. Design needs research, code needs design, assembly needs
code and assets, playtest needs assembly. The best controlled evidence on
multi-agent systems (Nature Machine Intelligence 2026, 260 configurations with
compute held constant) found that single-agent baseline performance is the
strongest predictor of whether coordination helps, and that past a capability
threshold extra agents make things *worse*. Anthropic's own multi-agent win is
explained almost entirely by token spend, not by coordination. So the dependent
stages stay on one thread.

Two consequences:

- A practice run **is** the baseline measurement. `run_log.py decide` reads the
  stage timings and tells you whether the split paid off, so the stage
  boundaries can be retuned.
- An untested orchestration layer is a second variable. If a run goes badly you
  cannot tell whether the model failed at making a game or the briefing failed at
  handing out work. Rehearse the roster on a practice run before a build you care
  about.

## Every run: the ledger

A number reconstructed afterwards from memory is not evidence, and the 30-minute
stall rule is the rule most likely to be broken in the moment, so it needs
something outside the moment to enforce it.

Start every run, including a practice run, with:

```bash
python ~/.claude/skills/roblox-build-orchestrator/scripts/run_log.py init --run <name> --mode fanout
```

Then bracket each stage and log every event as it happens, not afterwards:

```bash
run_log.py start --stage 3d-meshes
run_log.py event --kind fallback --stage 3d-meshes --note "TRELLIS.2 queue 8m, dropped to Cube 3D"
run_log.py end   --stage 3d-meshes --status fell-back
run_log.py status                 # is the current stage past the stall rule
run_log.py counter                # one status line; also written to counter.txt
run_log.py report                 # stage timing table + event lists
run_log.py decide                 # did the fan-out pay off, from what was measured
```

`counter.txt` is a single line that anything can tail (a text overlay, a status
bar, a dashboard), so a live count stays honest without anyone maintaining it by
hand.

### What counts as an intervention

Log the ones that count with `--kind intervention` the moment they happen.

**Free, does not count:** pressing Play, stopping a test, clicking Publish;
restarting a crashed or stuck MCP server; approving a tool call; creating the
universe and place shell once before the run; anything purely mechanical that no
API can reach.

**Counts:** writing or editing any line of code yourself; making a design or art
decision; choosing which sound or animation to use (but the agent searching and
selecting from the Creator Store itself is **not** an intervention); telling it
*what* is wrong rather than *that* something is wrong; choosing between options
it presents; clicking through a third-party plugin GUI on the agent's behalf.

A stall the agent resolves itself is not an intervention. Log it as
`--kind stall` so the report still shows where the time went.

## Mode A: solo (the baseline, and the fallback for small jobs)

One thread runs the whole pipeline in order, calling the existing skills per
stage: `roblox-3d-model`, `roblox-texture-gen`, `roblox-ui`, `roblox-animation`,
`roblox-vfx`, `roblox-map`. Use it for a quick prototype, for a single asset
stage, or as the baseline you compare a fan-out run against.

Two mechanical rules make the cap real, in both modes:

- **Stall rule.** If one problem eats 30 minutes, stop working on it, take the
  pre-authorised fallback so the run keeps moving, and log it. Check with
  `run_log.py status` at each stage boundary.

  **It protects the RUN, not the FIX, and those are different things.** The
  fallback is what stops one problem eating the run. It is not permission to
  ship the defect. Every stalled problem is healed before the run is called
  done - always, on every run, with no exception and no mode in which it is
  acceptable to carry it forward.

  Measured in one run: the mesh stage stalled, fell back, and the build shipped
  with Cylinder coins - an incomplete game. The cause was a missing `import os`
  in a vendored repo. One hour, once, and every run afterwards has real meshes.
  Deferring that fix does not save time, it re-spends it on every future run and
  ships a worse game each time.

  **The premise is one prompt equals a full game.** That is incompatible with a
  pipeline carrying defects it has already diagnosed. So a run is not finished
  when the game is built - it is finished when `run_log.py debts` exits clean.
  It gates by default; `--list` prints without gating and is for reading
  mid-run, not for finishing one.

- **Fallbacks are pre-authorised.** Attempt Tier 2 first on animation and SFX,
  then fall back to Tier 1 without asking. An agent stopping to ask permission to
  fall back is an intervention caused by an incomplete brief, which is a
  self-inflicted tick on the counter.

At the end, run `run_log.py decide`.

## Mode B: fan-out (the default for the asset block)

Fan out **the asset block only**: map, 3D meshes, materials, UI, animation, VFX,
SFX. Those are mutually independent, all downstream of the one design spec, all
generation-heavy, and each already produces a file. That is the shape fan-out is
for.

Market research can also fan out (independent genre candidates, breadth-first,
one synthesis at the end), and it is the safest place to rehearse the pattern
because nothing it does touches Studio.

**Do not fan out the spine.** Design needs research, code needs design, assembly
needs code and assets, playtest needs assembly. Anthropic names dependency-heavy
work as the poor-fit case explicitly, and adds that coding tasks have fewer
genuinely parallel parts than research does.

### The write boundary is the hard constraint

The Roblox DataModel is single shared mutable state. Two agents doing
`execute_luau` concurrently is the conflicting-writes failure in its purest form,
and it is a failure shape that has already happened twice in practice: the
robloxstudio-mcp duplicate-server timeout deadlock, and the Rojo double-connection
duplicates that killed every Knit controller. Exactly one MCP server is the rule.

So:

- **Workers write files to disk and nothing else.** Meshes, `.model.json`,
  KeyframeSequence specs, audio files, texture maps. No Studio tools at all.
- **One thread does every `execute_luau`, `insert_asset`, assembly, and publish.**

This costs nothing to adopt because the existing skills already emit files rather
than mutating Studio directly. It is enforced by the tool allowlist in each
worker definition, not by asking politely, because a prompt does not reliably hold
a boundary and an allowlist does.

### The roster

Installed at `~/.claude/agents/` (see *Start here*). Works identically in the
Claude Code terminal and the desktop app, since both read the same directory.

| Worker | Model | Writes | Tools |
|---|---|---|---|
| `roblox-asset-map` | opus | map spec outputs, proven layout, build artifacts | file ops, Bash, no Studio |
| `roblox-asset-mesh` | opus | mesh files + manifest | file ops, Bash, no Studio |
| `roblox-asset-ui` | opus | `.model.json` + Luau + PNG mockup | file ops, Bash, no Studio |
| `roblox-asset-anim` | opus | KeyframeSequence spec + verification renders | file ops, Bash, no Studio |
| `roblox-asset-vfx` | opus | VFX kit + manifest, from your harvested library | file ops, Bash, no Studio |
| `roblox-asset-sfx` | haiku | audio files + licence note | file ops, Bash, WebFetch, no Studio |
| `roblox-market-scout` | haiku | one findings file per genre | read-only + web, no writes to the build |

The tiering rule: **if a human will LOOK AT what the worker produces, the worker
has to be able to judge it.** Gates catch categorical failures, not quality, and
the saving comes from images staying inside the worker, so a worker that cannot
judge its own render has to ship it to the parent, which re-imports the cost the
split was buying. Sound stays on haiku because nothing in this pipeline can hear;
market research stays cheap because it gathers and cites.

Each is read-only with respect to Studio by construction. `maxTurns` on each one
enforces the 30-minute stall rule mechanically rather than by watching a timer.

## Briefing a worker

Workers start cold. They see none of this conversation. An underspecified brief is
the top cause of duplicated work and skipped verification, and every resulting
stall is a tick on the counter.

Every brief carries four fields. The stop condition is the one most often left off
and the one that matters most on a clock.

```
OBJECTIVE   One self-contained outcome. Not a share of a goal you can see and it cannot.
OUTPUT      Exact files, exact paths, exact manifest shape. So the result merges without re-reading.
TOOLS       Which skill, which sources, which tier to attempt first.
BOUNDARIES  What is out of scope, the Tier 2 to Tier 1 fallback (pre-authorised),
            and the wall-clock stop. Report partial work rather than overrunning.
```

Worked examples for the workers, with the exact manifest shapes the assembly
thread expects, are in `references/stage-briefs.md`. Read that before the first
fan-out run rather than improvising briefs on the day.

## What the manager keeps

Never delegated, for the same reason the writes are not:

- The design spec and every design or art decision.
- Verification of every worker report against the artifact it points at. A worker
  saying a mesh is under budget is a claim, not a fact.
- All Studio interaction, assembly, playtest, and publish.
- The ledger.

When two workers disagree, check the artifact rather than averaging the reports.

## Ending a run

```bash
run_log.py report      # the stage table and the full event history
run_log.py decide      # did the fan-out pay off, from what was measured
run_log.py debts       # GATES. The run is not finished until this is clean.
```

**`debts` gates by default and is the step that stops a run being a diary.**
It exits non-zero while any debt is open or closed at doc level only, so a run
cannot quietly end unhealed. Measured: a ledger recorded seven fallbacks and two
stalls faithfully and in real time, and then nothing turned a single one into a
fix. They were fixed hours later because a human asked why they had not been fixed
- not because anything surfaced them.

That is a predictable failure of every honest log: **recording an issue feels
like handling it.** The stall rule deliberately says MOVE ON, which is correct
during a timed run and wrong forever. The debt is real and it comes due on the
next run, unfixed.

So after `debts`, work the list, and pick the STRONGEST fix each one allows:

| | Fix | Property |
|---|---|---|
| 1 | **code fix** | the defect becomes unrepresentable. Cannot regress |
| 2 | **gate** | it can still happen, but fails loudly and early |
| 3 | **doc / note** | a future session is told, if it reads it |

**A gate is only real once it has FAILED on a known-bad input.** An untested gate
is a comfort, not a check. And anything left at 3 that could have been 1 or 2
will happen again.

Then write the outcome into your own project notes. The stage timings are the
input to the next run's decision, so they are worth keeping even when the run
went fine.

If this was a practice run and `decide` says the split paid off, rehearse the
roster once more before a run that matters.

## Files in this skill

- `scripts/run_log.py` - the ledger, counter, stall check, timing report, fan-out
  verdict and debts gate. Run `--help` for the full CLI.
- `agents/*.md` - the worker definitions, tool-restricted by construction.
- `references/stage-briefs.md` - worked briefs and manifest shapes per stage.
- `references/write-boundary.md` - why the single-writer rule exists, with the
  failures that motivated it.
- `LOCAL.template.md` - the machine-specific settings (copy to `LOCAL.md`).
