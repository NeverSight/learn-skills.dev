---
name: sb-hub
description: "Hub for the Storybook CSF3 bundle — diagnose a repo, orchestrate the audit→stories pipeline, or name the next sb-* step. Use for 'set up Storybook', 'audit my app', 'where do I start', 'what's next'."
compatibility: "Requires bash and python3 (read-only stack/readiness probes). node optional — report-issue.sh reads node/storybook versions and degrades cleanly if absent. Standard POSIX grep/sed/find."
allowed-tools: Bash Read Glob Grep
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    scripts: [report-issue.sh]
    wrappers: false
    references: [runbook.md, end-to-end-flow.md]
---

# sb-hub — onboarding check · orchestrator · navigator

The hub. You don't author here — you **inspect state and route**. Three read-only modes; pick by
intent. Read `CONTEXT.md` once for shared vocabulary, the storage map, and the resume protocol.

**Load by mode (don't pull both refs up front):**
- **`references/runbook.md`** — the navigator engine (state detection → one next step). Load it for
  **Mode 0 / Mode 2** (diagnose / "what's next").
- **`references/end-to-end-flow.md`** (~220 lines) — the full pipeline worked example for "messy app →
  design system". Load it **only for Mode 1 (orchestrate a full audit)**. **Do NOT load it** for a
  Mode-0 onboarding check or a Mode-2 next-step lookup — `runbook.md` is all those need.

**Canonical context (one source).** The bundle has exactly **one** `CONTEXT.md` (shared vocab · STORAGE
MAP · resume). It's never hand-duplicated: in the bundle/plugin install every skill reads this one file
(`CONTEXT.md` / `${CLAUDE_PLUGIN_ROOT}/CONTEXT.md`); a standalone `npx skills add <skill>` ships a
byte-identical *copy* the build vendors, refreshed on update. **`sb-hub` is the orchestrator** — if skills
are installed separately, route through `sb-hub` so the pipeline + shared vocabulary stay authoritative.

## Resolve the bundle

Scripts live in `scripts/`. In this repo: `${CLAUDE_PLUGIN_ROOT}/scripts/`.
When installed as a plugin, use `${CLAUDE_PLUGIN_ROOT}/scripts/`.

```bash
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}   # shared scripts: "$CORE/scripts/<name>"
```

## Pick the mode

| User intent | Mode |
|---|---|
| "is this ready", "where do I start", fresh/unknown repo | **0 · Onboarding check** |
| "audit this app", "do the whole thing", "build Storybook for this app" | **1 · Orchestrate** |
| "what's next", or after any verb appends to the ledger | **2 · Navigate** (default) |
| "this is wrong", "strange behavior", "report a bug", a skill misfired | **3 · Report** |

---

## Mode 0 — Onboarding check (phase-0 diagnose, read-only)

A fresh messy app: probe the stack + readiness **before** any verb, print a report, recommend the
first step. No prompts, no writes — re-runnable.

```bash
echo "━━ Phase 0 — readiness ━━"
grep -q '"react"' package.json 2>/dev/null && echo "  [ok]   React" || echo "  [warn] no React in package.json"
grep -qE '"vite"|"@vitejs' package.json 2>/dev/null && echo "  [ok]   Vite" || echo "  [info] not Vite (skill targets React+Vite)"
test -d .storybook && grep -q '"storybook"' package.json 2>/dev/null && echo "  [ok]   Storybook present" || echo "  [warn] NO_STORYBOOK → start with sb-setup"
test -d node_modules && echo "  [ok]   node_modules present" || echo "  [warn] deps not installed — run your package-manager install"
lock=$(ls package-lock.json pnpm-lock.yaml yarn.lock 2>/dev/null | head -1); echo "  [info] lockfile: ${lock:-none}"
grep -q '@storybook/addon-mcp' package.json 2>/dev/null && test -f .mcp.json && echo "  [info] MCP wired → sb-stories uses with-mcp" || echo "  [info] no addon-mcp → without-mcp path"
if find .storybook -maxdepth 1 -name '*.json' 2>/dev/null | grep -q .; then
  find .storybook -maxdepth 1 -name '*.json' | sed 's/^/  [ok]   discovery: /'
else echo "  [info] no discovery JSON yet → sb-inventory not run"; fi
grep -q 'storiesLocation:' .storybook/audit/status.md 2>/dev/null && echo "  [ok]   stories location decided" || echo "  [warn] stories location undecided → sb-setup must ASK (isolated .storybook/stories/ vs co-located) before sb-stories"
```

**Worked example — a half-migrated app** (Storybook installed, nothing audited yet):

```
━━ Phase 0 — readiness ━━
  [ok]   React
  [ok]   Vite
  [ok]   Storybook present
  [ok]   node_modules present
  [info] lockfile: pnpm-lock.yaml
  [info] no addon-mcp → without-mcp path
  [info] no discovery JSON yet → sb-inventory not run
  [warn] stories location undecided → sb-setup must ASK …
```
→ Storybook exists but no discovery JSON and location undecided, so **don't** jump to `sb-stories`.
Name **`sb-setup`** first (to record the stories location), then **`sb-inventory`**. That ordering —
*setup before inventory before stories* — is the whole point of the gate: the `[info]`/`[warn]` lines
are the routing signal, not noise.

Everything the bundle writes lives under `.storybook/` (CONTEXT.md STORAGE MAP) — flag if you ever see
outputs elsewhere. The one decision is **where stories go**; if undecided, name `sb-setup` (it asks).

> **Discovery is precomputed.** The discovery layers are JSON under `.storybook/`:
> `project-inventory` (+ `tokens.map`, `storyCoverage`) · `component-usage` · `flows` ·
> `design-system-health` · `component-states` · `prop-shapes` · `page-patterns` · `runtime`.
> The first four are **rendered** in Storybook (autodocs embeds + wrappers) and refreshed *together* by
> `refresh-usage.sh`; the rest are authoring inputs (regenerated on demand). **Never re-derive by shell
> scan what a script already wrote to `.storybook/*.json`** — Read the field.

Then print **`→ Start: <first verb>`** — `sb-setup` if `NO_STORYBOOK`, else `sb-inventory`. Don't run
the verb; name it and stop. For the full new-project arc, hand to Mode 1.

## Mode 1 — Orchestrate (run the whole audit → stories)

"Audit this app end to end." Run the pipeline **in order, gating between phases** — never advance
until the prior artifact exists (the discovery scripts write atomically, so an existing JSON is
complete). You don't run sibling scripts directly; you invoke each focused skill and verify its output.

1. **`sb-setup`** — if Mode 0 reported `NO_STORYBOOK`, **or** stories location is undecided. GATE: `.storybook/` + `"storybook"` in package.json, AND `storiesLocation` recorded in `.storybook/audit/status.md` (sb-setup asks the user — isolated `.storybook/stories/` vs co-located), AND `.storybook/runtime.json` exists (`discover-runtime.py` — provider tree / root-CSS / portals / MSW the shared preview must supply), before step 2.
2. **`sb-inventory`** — real-vs-slop + dominant design system. GATE: `.storybook/project-inventory.json` exists.
3. **`sb-health`** — design-system health. GATE: `.storybook/design-system-health.json` exists; if `designSystem.mixed` / heavy raw-hex, surface the `/ds-runbook` handoff before authoring.
4. **`sb-flows`** — route map + nav edges. GATE: `.storybook/flows.json` exists.
5. **`sb-stories <Component>`** — author a story for each component that **needs** one: work down
   `components.storyCoverage.needsStory[]` (own components without a story, top-imported first), each
   self-gating with `validate-stories.sh`. The honest progress meter is `storyCoverage.withRegisteredStory/
   needsCount` when `storyCoverage.source == "storybook-index"` (reconciled against Storybook's `index.json`
   — the stories Storybook actually registers); otherwise `withColocatedStory/needsCount` (heuristic; `withStory`
   is a loose upper bound — it also counts components a story merely imports to mock). Re-run `sb-inventory`
   (or `sb-audit`) after authoring to refresh coverage from the index and shrink `needsStory[]` — iterate until empty.
6. **`sb-wrappers`** — render each step's output as a view: `ProjectInventory` (after step 2), `DesignSystemHealth`/`TokenMatrix` (after step 3's health), `AppFlowGraph`/`JourneyGraph` (after step 4), and `StateGrid`/`StateMatrix` while authoring stories (step 5). The data wrappers need their step's JSON first — see sb-wrappers "When in the flow".
7. **`sb-audit`** — periodic drift survey + decision board once stories land; runs `refresh-usage.sh` (below).

**Figma-originated design system (optional branch, after step 1).** The pipeline above is *code-first*
(audit what exists). When the source of truth is an **approved Figma file**, insert **`sb-figma`** to
establish foundation-token parity before authoring: it captures the Figma MCP variables to
`.storybook/figma/`, writes `.storybook/figma-token-parity.json` (color/spacing/type, OKLCH→hex), wires the
`Foundations/Colors|Tokens|Type` stories' `figmaVar`/`figmaHex`, and reports drift. It feeds — doesn't
replace — `sb-health` (step 3): health checks the code-internal token set; `sb-figma` adds the design↔code
axis health can't see. (Delivering approved *components* from Figma is also `sb-figma`, authored via
`sb-stories`; *iterating undecided* designs stays `sb-explore`.)

Append a one-line finding to `.storybook/audit/findings.md` after each phase. Stop on the first GATE
that fails and tell the user which verb to fix. (Pattern: ordered pipeline with hard gates, like `lfg`.)

**Keep rendered data fresh (the usage layer).** The four rendered JSONs (inventory · component-usage ·
flows · design-system-health) feed the autodocs **usage embed** — `UsageSection` wired once into
`preview.ts` `docs.page` adds "Real usage in this app" to every component's Docs **and** each Foundation
(Colors/Semantic/Typography/Scales = token tables, Health = audit findings). `refresh-usage.sh --docs`
re-runs all four together so a rebuild reflects reality; `sb-audit` does this each pass, and it belongs in
CI before `storybook build`. (Setup wires the `docs.page` composition — see `sb-setup` install-wizard.)

## Mode 2 — Navigate (default — name the single next step)

Inspect state + ledger, recommend **exactly one** next surgical skill (whose prerequisites are met).

```bash
test -d .storybook && grep -q '"storybook"' package.json 2>/dev/null && echo STORYBOOK_PRESENT || echo NO_STORYBOOK
ls .storybook/*.json 2>/dev/null            # which discovery JSONs exist
cat .storybook/audit/status.md 2>/dev/null  # ledger / resume point
# DRIFT — source/story files changed since the last discovery (newer than the inventory JSON). Plain
# `find -newer` → cross-agent (no git, no Claude hook), works on uncommitted/untracked files. Lists the
# exact files that moved this session; if any, the discovery JSONs are stale → refresh before routing.
if [ -f .storybook/project-inventory.json ]; then
  find src app components .storybook/stories \( -name '*.tsx' -o -name '*.ts' \) \
    -newer .storybook/project-inventory.json 2>/dev/null | grep -v '\.storybook/.*\.json' | head -20
fi
# COVERAGE — READ the field the script already wrote (CONTEXT.md doctrine: never re-derive). Extract
# ONLY storyCoverage so the FULL object surfaces complete — never a truncated dump of the whole
# inventory. Prefer the authoritative `withRegisteredStory` (source=storybook-index, reconciled against
# index.json); fall back to the heuristic `withColocatedStory`. needsStory[] is the iterate list.
if [ -f .storybook/project-inventory.json ]; then
  python3 - <<'PY'
import json
try: c = json.load(open(".storybook/project-inventory.json"))["components"]["storyCoverage"]
except Exception: raise SystemExit
src = c.get("source", "heuristic")
done = c.get("withRegisteredStory") if src == "storybook-index" else c.get("withColocatedStory", 0)
print(f"coverage: {done}/{c.get('real',0)} components have a story [{src}] · {c.get('needsCount',0)} need one")
if c.get("needsStory"):
    extra = " …" if c.get("needsCount", 0) > 8 else ""
    print("iterate next (sb-stories): " + ", ".join(c["needsStory"][:8]) + extra)
PY
fi
```

If DRIFT lists files, the discovery JSONs no longer match the code — route to **`sb-inventory`** (or
**`sb-audit`** for a periodic pass) to refresh before naming the next step: its `refresh-usage.sh` re-runs
inventory/usage/flows AND reconciles story coverage against Storybook's own `index.json` (authoritative,
not a basename guess). Then route — **name exactly one**:

| State | Next step | Skill |
|---|---|---|
| `NO_STORYBOOK` | defer bootstrap to `npx storybook ai setup`, then align | `sb-setup` |
| No `project-inventory.json` | discover real-vs-slop first | **`sb-inventory`** |
| Inventory done, no `design-system-health.json` | check health before authoring | `sb-health` |
| Health done, no `flows.json` | capture navigation + app-map | `sb-flows` |
| Inventory clean, want stories | author ONE component | `sb-stories <Component>` |
| New/redesigned component, **undecided** — iterating options | sandboxed iteration (+ Figma node) | `sb-explore` |
| **Approved** Figma design — map foundation tokens (color/spacing/type) or deliver an approved component | Figma → production Storybook | **`sb-figma`** |
| Check Figma↔code token parity / "is the design system in sync with Figma" | parity + drift report | **`sb-figma`** |
| Connect components back to Figma (Code Connect) / "show my code in Figma Dev Mode" | code → design (reverse) | **`sb-figma`** |
| Periodic check | drift survey + decision board | `sb-audit` |
| Explore meets graduation gate | propagate to production | `sb-ship` |

> **EXPLORE vs DELIVER (both are Figma-aware — route by stage, not by "uses Figma"):** *undecided / trying
> options* → `sb-explore` (Lab) → `sb-ship` (graduate). *Already approved in Figma* → `sb-figma` (deliver
> direct to prod). `sb-figma` writes the Foundation token stories itself; for an approved **component** it
> extracts the design then authors via `sb-stories`' rules. It captures every Figma MCP output to
> `.storybook/figma/` (manifest + per-tool files) so the pipeline is reproducible/iterable, not MCP-bound.

**Resume rule (CONTEXT.md):** read `status.md` + check which JSONs exist; resume from the first
incomplete step. Never treat a file half-written in a prior session as complete — re-run that step.

## Mode 3 — Report (a skill misfired / strange behavior)

When the user says a skill did something wrong, surprising, or broken, help them file a useful report —
don't just apologize. Draft it with the agent-native reporter, then hand them the submit command.

```bash
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
"$CORE/scripts/report-issue.sh" --asked "<what they asked>" --observed "<what happened>" --expected "<what they wanted>"
```

It writes a **sanitized** draft (versions + `.storybook/*.json` shapes/counts only — never source, token
values, or component names) and prints a `gh issue create …` command + a blank-issue URL. It makes **no
network call** — the user submits. Fill `--asked/--observed/--expected` from the conversation, show them
the draft path + the `gh` line, and (only if they ask) offer to run `gh` for them. To target a different
repo: `SB_ISSUE_REPO=owner/name`. A good report becomes a reproduction → a new eval case → a fix → a
`field-learnings.md` entry — the loop that keeps the next run from re-hitting the same bug.

## Never (orchestration failure modes, and why)

- **NEVER advance past a failed/empty gate** in Mode 1 — each phase's `.storybook/*.json` is the
  *precondition* for the next (foundation tokens before components, flows before the app map). Skip one
  and every later phase builds on missing ground truth and silently under-delivers.
- **NEVER re-derive CONTEXT by shell-scanning** what a script already wrote — the `.storybook/*.json`
  files ARE the state. Hand-grepping drifts from what the scripts captured and what the wrappers render;
  cite the field, don't recompute it.
- **NEVER treat a half-written prior-session artifact as complete** — writes are atomic per file, but an
  interrupted *run* may have stopped mid-pipeline. Check `status.md` and re-run the first incomplete step.
- **NEVER author here** — the hub inspects and routes. Writing a story/wrapper from the hub bypasses the
  focused skill's own checks and anti-patterns; invoke the skill instead.
- **NEVER hand-duplicate `CONTEXT.md`** — every skill reads the one canonical file (`CONTEXT.md`);
  a copy is drift waiting to happen.

## Cross-agent

- Claude: this skill is `/sb-hub` (Mode 2 / "what's next" is the default; `/sb-hub onboard` or
  `/sb-hub audit this app` selects Mode 0 / 1).
- Codex: `$sb-hub what's next` · `$sb-hub onboard` · `$sb-hub audit this app`.
- The loop: a verb runs → appends to `.storybook/audit/findings.md` → ask `sb-hub` again (Mode 2)
  → it names the next surgical skill → run it.
