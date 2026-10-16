---
name: visual-debug
description: "Diagnose why an existing implementation differs from reference evidence using AE/SSIM, pixel, section, computed-style, and transition diffs. Use for post-implementation mismatch or repair guidance; not baseline capture or full clone generation."
metadata:
  filePattern:
    - "**/tmp/ref/**/static/**"
    - "**/tmp/ref/**/frames/**"
    - "**/tmp/ref/**/diff/**"
    - "**/side-by-side/**"
  bashPattern:
    - "compare.*metric"
    - "ffmpeg.*ssim"
    - "ae-compare"
    - "batch-compare"
    - "batch-scroll"
    - "computed-diff"
    - "auto-diagnose"
  priority: 90
---

# Visual Debug

Diagnose an existing implementation against captured reference evidence with structural, AE, DSSIM, runtime, and transition checks.

## Boundary and return contract

- Use this skill when reference and implementation evidence already exist. Route missing baseline evidence to `ui-capture`; route implementation, regeneration, and full clone orchestration to `ui-reverse-engineering` or the active caller.
- Diagnose and return the failing artifact, selector or region, likely root cause, recommended fix, and exact verification command. The caller owns source edits unless it explicitly delegated repair.
- Read `brief/WORKER_BRIEF.md` or `evidence-pack.json` first when present, then only the summaries and named drill-down artifacts needed for the failing hotspot.
- If repair was delegated to you, read [`../ui-reverse-engineering/iteration-discipline.md`](../ui-reverse-engineering/iteration-discipline.md) before the repair loop. Attempt history and stop conditions survive delegation and compaction. Report checker defects with a reproducer unless shared-tool repair is already authorized; never edit an installed cache.
- Matching text, heights, fired events, or a successful build does not prove appearance or trajectory parity. Compare background and foreground, media fit, and intermediate motion states.

## Required invariants

**Do not read ref/impl images for routine comparison.** Start with summaries and AE/SSIM tools. For a failing position, run `auto-diagnose.sh`; read a diff image only if automated diagnosis finds nothing. Phase E is the required exception and must run in a delegated context.

Pin the reference during iteration. Dynamic sites otherwise compare against a moving target: after the first complete reference capture, use frozen reference crops (`RECATCH_REF=0`) until evidence is genuinely stale. After any implementation edit, produce fresh implementation evidence before judging the fix.

When evidence contains `window.scrollTo`, `scrollYProgress`, `setTimeout`, velocity, a guard ref around scroll-stop logic, or ScrollTrigger pin/scrub, require scroll state-machine proof of `initial → active/expanded → settled/returned`; a single endpoint frame is insufficient.

Do not weaken thresholds or mask unexplained regions to clear a failure. Classify each failure as implementation, reference/capture, checker, or unknown before editing.

Close every browser session you opened on success, failure, or interruption:

```bash
agent-browser --session <session-name> close
```

Never use `close --all`; other agents may own sessions.

## Start once per session

Check required tools. If anything is missing, stop and surface the bootstrap command; do not execute a remote installer automatically.

```bash
miss=""
for c in agent-browser ffmpeg dssim; do command -v "$c" >/dev/null 2>&1 || miss+=" $c"; done
{ command -v magick >/dev/null 2>&1 || command -v convert >/dev/null 2>&1; } || miss+=" imagemagick"
if [ -n "$miss" ]; then
  printf 'Missing system deps:%s\nBootstrap:\n  tmp=$(mktemp) && curl -LsSf -o "$tmp" https://raw.githubusercontent.com/voidmatcha/ui-clone-skills/main/install.sh && bash "$tmp" && rm -f "$tmp"\n' "$miss"
  exit 1
fi
```

Resolve scripts from the active plugin or checkout:

```bash
SCRIPTS_DIR="${VISUAL_DEBUG_SCRIPTS_DIR:-}"
if [ -z "$SCRIPTS_DIR" ]; then
  for root in "${PLUGIN_ROOT:-}" "${CODEX_PLUGIN_ROOT:-}" "${CLAUDE_PLUGIN_ROOT:-}" "${UI_CLONE_ROOT:-}" "$PWD" "$PWD/.." "$PWD/../.." "${INSTALL_DIR:-$HOME/.local/share/ui-clone-skills}"; do
    [ -n "$root" ] && [ -f "$root/skills/visual-debug/scripts/ae-compare.sh" ] && SCRIPTS_DIR=$(cd "$root/skills/visual-debug/scripts" && pwd) && break
  done
fi
[ -n "$SCRIPTS_DIR" ] || { echo "Set VISUAL_DEBUG_SCRIPTS_DIR or PLUGIN_ROOT" >&2; exit 1; }
```

Run the scripts as `bash "$SCRIPTS_DIR/<script>.sh" ...`. On hosts without a Skill event (Codex), the first such call is what tells the plugin hooks that this session owns the diagnosis.

Pipe large browser JSON to files; do not print it into the model context. Every `agent-browser` command needs `--session <name>`, and every JS eval must be an IIFE.

## Choose the route

1. Read the smallest existing summary first: `sections/result.txt`, `pipeline-state.json`, `_summary.json`, `pixel-perfect-diff.json`, or the failing gate artifact.
2. Run cheap structural checks before pixels: implementation chrome scan, `stray-absolute-check.sh`, relevant transition/spec coverage, reveal/breakpoint checks, then a narrow `computed-diff.sh`.
3. Use `section-compare.sh` for routed post-generation verification and `batch-scroll.sh` plus `batch-compare.sh` for a standalone broad sweep. The section command requires the fourth ref-dir argument because the gate reads its `sections/result.txt`.
4. Diagnose only failing rows with `auto-diagnose.sh`. Escalate unresolved failures in order to `tree-diff.sh`, `layout-tree-diff.sh`, `hover-tree-diff.sh`, or `keyframes-diff.sh` according to the symptom.
5. Re-run the affected check and its dependency closure. Use scoped or standard verification during iteration; canonical closeout still requires the caller's full comprehensive verification.

Read [tool-routing.md](tool-routing.md) only when you need exact commands, `ONLY_IF_CHANGED`, masking rules, or tool selection. Read [common-selectors.md](common-selectors.md) only for domain selector sets. Read [verification.md](verification.md) only for standalone full capture/verification mechanics. Read [comparison-fix.md](comparison-fix.md) only when entering the repair loop or dispatching Phase E. Do not load all references up front.

## Three-axis completion

Every position requires all three axes:

| Axis | Tool | Pass condition |
|---|---|---|
| Pixel | AE | AE per image ≤ 500 |
| Perceptual | DSSIM / frame SSIM | SSIM per frame ≥ 0.995 |
| Semantic | delegated Phase E review | PASS, or explicit approval of a known difference |

Computed-style comparison passes with 0 mismatches. AE=500 permits antialiasing variance; dynamic content may use AE=2000 only through the documented dynamic route. These thresholds are contracts and may change only with explicit user approval and recorded rationale.

Phase E is mandatory for full verification and reviews every ref/impl position after AE and DSSIM. Delegate it to the host-native `visual-debug-reviewer` (a Codex native subagent where available); otherwise use a generic delegated worker with the same contract. Do not retry a rejected role name. Only the verdict table returns to the coordinator. A bounded diagnostic Phase E may inspect representative existing pairs early, but its noncanonical artifact cannot replace final all-position review. See [comparison-fix.md](comparison-fix.md#phase-e-llm-structural-review-mandatory-all-positions).

Return PASS only when all three axes agree and every required row is measured. `FAIL`, `INCOMPLETE`, `UNMEASURED`, stale evidence, or missing artifacts remain incomplete. Then resume the caller's pipeline for implementation and canonical closeout.
