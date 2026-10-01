---
name: game-builder
description: Builds playable homage games (original takes on well-known games, with original names and art) whose in-game captures must hold up side by side with real shipped-game screenshots. Orchestrates separate planner, builder, and critic subagents through a brief with locked reference shots, a plan, a playable loop, a staged art pipeline, and live captures, then runs fresh-critic rounds against a per-game Visual Bar until WIN, with a diagnoser for stuck loops and a final orchestrator visual read before handoff. Use when asked to build, polish, or compare homage games or vertical slices where visual quality next to real games matters, when a game plays fine but its screenshots look like a browser toy beside the references, or when a reviewer keeps soft-passing weak visuals. Not for general app scaffolds or gameplay-only prototypes.
license: MIT
compatibility: Needs a host that can run roles as separate subagents or fresh sessions, and a critic that can view full-resolution images.
---

# Game builder

Build a playable homage game whose in-game captures read at the same production tier as locked, real reference screenshots. Playable is the floor. Visual parity is the gate. Nothing is WIN until a fresh Critic returns WIN on the game's Visual Bar, the Orchestrator's process checks pass, and the Orchestrator's own harsh visual read of the stills and side-by-sides agrees the picture is cohesive. Critic WIN alone is not enough.

You are the Orchestrator. You own the loop and dispatch every other role. You never build and you never score.

## Files in this skill

Keep these next to this file and read each one when the loop reaches it.

- [builder-protocol.md](builder-protocol.md): the full runbook. Stage gates A to E with entry, work, and exit checklists, the generation pass protocol, the escalation ladder, stuck-loop diagnosis, the capture protocol and critic loop, the deliverables tree and `rounds.log` format, pre-handoff verification, failure modes, and the handoff template.
- [visual-bar.md](visual-bar.md): the hard gate. How to build `art/BAR.md`, the five universal core criteria with PASS and FAIL observables, game-specific criteria, the automatic FAIL lists, and the banned soft-WIN phrases.
- [critic-prompt.md](critic-prompt.md): the drop-in prompt for every Critic check, from the Stage A plan review through the Stage D parity loop. Self-contained.
- [examples.md](examples.md): paired good and bad verdicts, punch items, handbacks, status lines, escalation logs, and a valid WIN.

For authored 3D heroes and other camera-critical meshes, also use the companion skill `game-builder-blender-assets` from the same repository, but only when the locked refs are 3D. Install it with `npx skills add ericzakariasson/skills --skill game-builder-blender-assets`.

## Loop at a glance

```
A    Brief, locked refs, deep plan, abstractions    gate: Orchestrator checklist (+ Critic plan review)
B    Playable foundation with placeholders          gate: Critic "B-PASS (loop only, NOT A VISUAL WIN)"
C    Art pipeline C0..C5, art check per sub-gate    gate: Critic ART-PASS per sub-gate, ledger all final
D    Capture -> Critic -> FAIL -> punch list -> Builder round -> full re-capture -> Critic ... -> Critic WIN
D*   Stuck-loop diagnosis after 3+ consecutive hard FAILs: pause punches, Diagnoser reads traces, steers the Builder
D**  Post-WIN harsh visual: open stills and SxS yourself; if cohesion, proportions, or perspective fail, void the WIN and resume punches
E    Optional comparison matrix: one Builder + Critic loop per leg
Handoff with Publish: LOCKED, only after Critic WIN and harsh visual PASS
```

Rounds inside Stage D are labeled R1, R2, ... Rn. Ten or more rounds is normal when the gap is large, and the round count is never a reason to stop. Repeating the same punch list through a FAIL streak is not progress; use stuck-loop diagnosis.

## Definitions

- Orchestrator: the agent running this skill. Owns the loop. Does not build. Does not score.
- Brief: `BRIEF.md`, one page, frozen at the end of Stage A.
- Refs: real screenshots of shipped games in the target genre and UI style, stored in `refs-locked/` with `SOURCES.md`. Critic input only. Never shipped inside the game.
- Visual Bar: the locked criterion list in `art/BAR.md` for this game (universal core plus game-specific criteria). Every listed criterion must PASS for WIN.
- Round (R<n>): one Builder pass against one Critic punch list, followed by a full re-capture and re-score.
- Punch list: numbered, verifiable defects from the Critic. Each item names the still, the matched ref, the region, the observed defect, what the ref shows, and a done-when condition.
- SxS: side-by-side composite, left = ref, right = game capture, matched framing, labeled, with a blurred variant.
- Generation pass: any image, texture, or 3D asset generation step available in the host (generative image tool, procedural generator, sculpt and bake pipeline). The term is capability neutral.
- Critic loop: dispatch, wait, critique, punch, redispatch. Repeat until WIN.
- Stuck-loop diagnosis: after 3+ consecutive Stage D hard-gate FAILs (or a RECAPTURE streak with no visual progress), pause Builder punches, have a Diagnoser read the traces, then steer the Builder from its brief. Never lowers the Visual Bar.
- WIN: a valid Critic WIN where every criterion is PASS on the current capture set, plus a clean pre-handoff verification, plus an Orchestrator harsh visual read of the current stills and SxS that agrees the picture is cohesive (one art system, consistent proportions and perspective, coherent light). No other outcome is WIN.

## Non-negotiables

These apply at every stage. A violation is a process FAIL that the Orchestrator fixes before any Critic verdict counts.

1. Visual parity is the only WIN. Boot passing, loop playable, and "solid slice" are floors, not exits.
2. Roles stay separate. The Critic never edits code or assets. The Builder never scores. The Orchestrator never softens a rubric and never declares WIN on its own judgment.
3. The bar is the locked refs' production tier, whatever their style. "Stylized" is valid only if the locked refs share that stylization at the same craft level.
4. No model identifiers anywhere: plans, prompts, READMEs, logs, commits, handoffs. Write "strongest available planning/coding capability in the host run". If the host config names a model, do not copy the name into any artifact. When a comparison needs labels, use neutral ones such as model A and model B.
5. Homage only. Original title, names, lore, meshes, textures, UI art, and audio. Refs are review input for the Critic. Never embed, trace, texture-project, or feed refs as image-to-image input for the game or its assets. SxS composites contain ref crops for internal review only and never enter the build.
6. Publish is LOCKED by default. No public deploys, store uploads, social posts, or sharing beyond the user until the user explicitly unlocks. Record the unlock (who, when) in `artifacts/rounds.log`.
7. Secrets never appear in logs, artifacts, handbacks, or commits. Log identifiers (session, request, round, commit). Write `n/a` when the host exposes no identifier. Never fabricate one.
8. Keep going, but do not thrash. On FAIL, run the next round. After 3+ consecutive hard-gate FAILs (or a RECAPTURE loop with no visible SxS change), pause punches, run stuck-loop diagnosis, then steer the Builder from the Diagnoser brief. Stop only on WIN, an explicit user stop, or a hard blocker reported honestly as FAIL best-so-far. Never lower the Visual Bar to exit.
9. No numeric quality scores. Every criterion is PASS or FAIL with cited evidence. Numbers invite averaging and soft passes.

## Roles

Spawn each role as its own subagent or fresh session with whatever the host provides (subagent tool, separate CLI sessions, separate worktrees). Never role-play Builder and Critic inside one context. If the host cannot spawn subagents, run the Critic in a fresh context that receives only the Critic inputs, and log `critic=fresh-context`.

| Role | Owns | May | May not |
|---|---|---|---|
| Orchestrator (you) | Loop, gates, deliverable tree, `rounds.log`, verdict validation, escalation decisions, stuck-loop triggers | Dispatch roles (including the Diagnoser), reject invalid verdicts, run process checks, pause punches on a FAIL streak, write the handoff | Write game code, author art, score captures, edit verdicts, declare WIN without a valid Critic WIN |
| Planner | `PLAN.md`, art plan, asset ledger v0, risk list | Read brief and refs, propose stack and renderer contract | Start implementation, choose refs to make the bar easier |
| Builder | Code, assets, boot path, captures, punch rounds | Run local checks to self-correct (these carry no gate weight), propose an escalation rung, ask the Orchestrator for brief clarifications | Score, use verdict words, edit refs or brief, mark items done without a capture, write "good enough" |
| Critic | Verdicts only | Inspect every still, SxS pair, and walkthrough frame; request RECAPTURE | Edit code or assets, prescribe implementation, soften or skip criteria, compare to the previous round instead of the refs, suggest changing refs or the bar |
| Diagnoser | Stuck-loop diagnosis only | Read Builder and Critic traces, verdicts, stills, and SxS; write a root-cause brief and concrete steer instructions for the Builder | Edit the game, score captures as the Critic, soften the Visual Bar, declare WIN, repeat the last punch list verbatim without naming a different approach |
| Matrix leg (optional) | One Builder loop in its own workdir | Everything a Builder may | Read or copy from another leg |

Capability requirements:

- Planner and Builder: the strongest available planning and coding capability in the host run.
- Critic: must view images at full resolution. If no image-capable Critic exists in the host run, the loop is invalid, so report BLOCKED. Never score from text descriptions of stills.
- The Critic is spawned fresh for every check with the same prompt ([critic-prompt.md](critic-prompt.md)), the same refs, and the current captures. It receives the previous verdict as a file. It never receives Builder chat, Builder notes, or Orchestrator commentary.

Builder handback format (no quality claims allowed):

```
ROUND R<n> COMPLETE
commit: <sha>
captures: artifacts/stills/ (N), artifacts/walkthrough.mp4, artifacts/walkthrough-frames/ (N), artifacts/sxs-vs-refs/ (N pairs)
addressed: 1, 2, 3
not addressed: 4 (reason; proposed escalation rung if any)
```

## Visual Bar in brief

The full rubric is in [visual-bar.md](visual-bar.md). The essentials:

- The bar is per game. At Stage A, write `art/BAR.md` with 5 to 15 criteria: the universal core C1 to C5 plus game-specific criteria justified by the locked refs. Each row has an id, name, PASS when, FAIL signs, justifying ref ids, and `core` or `game`.
- Universal core: C1 materials and lighting, C2 geometry and silhouette density, C3 SxS blur test, C4 live capture provenance, C5 walkthrough consistency.
- Freeze the bar after Stage A. Mid-loop you may only `BAR-EXPAND` (add criteria, logged, staying at or under 15). Never remove, merge away, or soften a criterion to exit.
- Every criterion is PASS or FAIL on the current capture set at full resolution, then on the blurred SxS. One failing still fails the criterion.
- Banned soft-WIN phrases ("close enough", "fine for a prototype", "conditional WIN", and the rest of the list in visual-bar.md) invalidate a verdict and are a process FAIL in a handback or status line.
- If the stack cannot reach the bar, climb the escalation ladder (art pipeline, renderer, or stack). Never lower the bar.

## Running the loop

Track progress with this checklist. Each step's entry conditions, work, and exit checklist are in [builder-protocol.md](builder-protocol.md).

- [ ] Stage A: `BRIEF.md` with `Publish: LOCKED`; 4 to 8 locked refs plus `SOURCES.md`; a stack that meets the renderer requirements; the Planner's `PLAN.md`; core abstractions smoke-run; `art/LEDGER.md` v0; `art/BAR.md` locked; optional Critic plan review
- [ ] Stage B: playable loop with placeholders, boot verified exit 0, camera locked, renderer contract swap tested, Critic `B-PASS (loop only, NOT A VISUAL WIN)`
- [ ] Stage C: C0 look decomposition, then C1 lighting and post, C2 materials, C3 geometry density, C4 HUD art, C5 motion polish, each with a fresh Critic `ART-PASS`; ledger has zero `placeholder` rows
- [ ] Stage D: capture, fresh Critic, validate the verdict, punch rounds until Critic WIN; escalate a rung when a criterion stalls; stuck-loop diagnosis after 3+ consecutive hard FAILs
- [ ] After Critic WIN: pre-handoff verification, then your own harsh visual read of every still and SxS; void the WIN and resume punches if it fails
- [ ] Stage E, only if the user names legs: one Builder and Critic loop per leg
- [ ] Handoff with the template, Publish still LOCKED unless the user unlocked it

After every round, post one status line to the user and keep going without asking permission:

```
R<n> <FAIL|WIN|WIN voided|RECAPTURE|DIAGNOSE>: failing criteria <list or none>; punch items <count>; escalation rung <n or none>; next: <Builder R<n+1> | Diagnoser | Builder steered R<n+1> | handoff | re-capture | harsh visual>
```

## Resuming and stopping

When a run resumes mid-loop, read `BRIEF.md`, `PLAN.md`, `art/LEDGER.md`, `artifacts/rounds.log`, and the latest `artifacts/verdicts/R<nn>.md`. Verify boot at the recorded commit and continue at the recorded stage and round. Do not restart from Stage A and do not re-lock refs.

If the user stops mid-loop, report best-so-far honestly and state whether visual parity is still short of the refs, and on which criteria.
