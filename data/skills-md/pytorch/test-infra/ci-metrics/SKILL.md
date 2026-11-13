---
name: ci-metrics
description: Fallback loader for the canonical PyTorch ci-metrics skill. Use for CI duration, failures, queue times, workflow trends, runner health, or dashboard data only when the canonical instructions are not already loaded and no accessible pytorch/pytorch checkout contains them.
---

# PyTorch CI Metrics Loader

The canonical skill is `pytorch/pytorch/.claude/skills/ci-metrics/SKILL.md`; this loader does not count. Choose one instruction source in this order:

1. If the canonical instructions are already loaded in the current agent context, follow them directly. A skill catalog entry alone does not count as loaded instructions.
2. If an accessible `pytorch/pytorch` checkout contains `.claude/skills/ci-metrics/SKILL.md`, read and follow that file, resolving relative paths from its directory. Check the current workspace and already-known checkout locations; do not crawl the filesystem looking for a clone.
3. Otherwise, fetch a fresh temporary copy from `pytorch/pytorch` as shown below. Never reuse a previous download or another vendored copy.

```bash
dir=$(mktemp -d)
base=https://raw.githubusercontent.com/pytorch/pytorch/main/.claude/skills/ci-metrics
curl -fsSL "$base/SKILL.md" -o "$dir/SKILL.md"
curl -fsSL "$base/gcx-wrapper.sh" -o "$dir/gcx-wrapper.sh"
chmod +x "$dir/gcx-wrapper.sh" && echo "$dir"
```

Read the selected `SKILL.md` as a file and follow it as the authoritative instructions; do not invoke a skill named `ci-metrics` from this loader, because that may select this loader again. For a downloaded copy, resolve paths such as `gcx-wrapper.sh` against the printed directory. If it references a file not fetched above, download it from `$base/<path>`. If any download fails, stop and report the error instead of falling back to stale instructions.
