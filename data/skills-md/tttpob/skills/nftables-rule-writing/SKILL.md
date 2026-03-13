---
name: nftables-rule-writing
description: Write, review, and lint nftables rulesets for coding-agent generated configs. Use for quickstarts, rule authoring, audits, and troubleshooting, especially chain type/hook constraints, statement validity (nat/reject/tproxy/redirect), inet IPv4/IPv6 pitfalls, and source-informed validation with nft -c.
---

# nftables Rule Writing (Quickstart, Pitfalls, Constraints)

Use this skill when generating, reviewing, or debugging `nftables` rulesets, especially when an LLM may produce rules that are syntactically valid but semantically invalid for a specific chain type, hook, or family.

## When to Use

Trigger on requests like:

- "Write an `nftables.conf`"
- "Review this `.nft` file"
- "Why does `nft -f` / `nft -c` fail?"
- "Which actions are valid on which hooks?"
- "How do I write IPv4 + IPv6 rules in `table inet`?"
- "Create a lint checklist for generated nftables rules"

## What This Skill Covers

- Quickstart ruleset patterns (safe defaults and common base chains)
- Reusable nftables patterns for common host/router scenarios
- Ops workflows (validate/apply/list/monitor/reload)
- Persistence discovery (including systemd units and drop-ins that may load custom `.nft` files)
- Hook / chain-type / family constraints
- Statement-specific constraints (`dnat`, `snat`, `masquerade`, `redirect`, `reject`, `tproxy`, `queue`)
- `inet` family IPv4/IPv6 pitfalls
- Debugging workflow with `nft -c` and `--debug`
- Source map to official docs and userspace code (`nftables` project)

## Workflow (Authoring + Review)

1. Identify the ruleset shape first:
   - `family` (`ip`, `ip6`, `inet`, `bridge`, `netdev`)
   - table purpose (`filter`, `nat`, etc.)
   - chain `type`, `hook`, `priority`, `policy`
   - whether `device` is required (`netdev`, `inet` + `ingress`)
2. If starting from scratch, use `references/quickstart.md` and `references/nftables-patterns.md` to pick a known-good template.
3. Check structural legality in `references/constraints-matrix.md`:
   - chain definition validity
   - statement vs hook compatibility
4. Check common LLM mistakes in `references/common-pitfalls.md`.
5. For fast triage, use `references/hook-action-cheatsheet.md`.
6. If `nft` is available, run:
   - `nft -c -f <file>`
   - `nft -c -d parser,eval,netlink -f <file>` (when error cause is unclear)
7. For deployment/runtime concerns, use `references/nftables-ops-cheatsheet.md` and `references/nftables-troubleshooting.md`.
8. If needed, use `references/source-map.md` to trace the constraint back to official docs or `src/evaluate.c`.

## Quickstart First (Important)

Do not start by writing isolated rules. Start from a valid chain declaration and then add rules.

For common starting points:

- Minimal host firewall: `references/quickstart.md`
- Reusable practical patterns: `references/nftables-patterns.md`
- NAT placement reminders: `references/hook-action-cheatsheet.md`
- `inet` dual-stack gotchas: `references/common-pitfalls.md`

## Review / Lint Output Format (Recommended)

When reviewing LLM-generated rules, output findings in this order:

1. `Issue` (specific chain/rule)
2. `Why it is invalid or risky` (hook/family/statement constraint)
3. `Fix` (replacement snippet)
4. `Validation` (`nft -c` / version-sensitive caveat)

## Core Principles

- Legality is layered:
  - parser (`scanner.l` / `parser_bison.y`)
  - userspace semantic checks (`src/evaluate.c`)
  - kernel `nf_tables` support (final authority)
- Many failures are not syntax errors. Common real causes:
  - wrong chain type/hook
  - invalid statement in that chain/hook
  - missing `device` on `netdev` or `inet` ingress base chains
  - `inet` NAT address missing explicit `ip`/`ip6`
  - conflicting protocol contexts (`ip` + `ip6` in one rule)
- If the target environment is unknown, say so explicitly and require `nft -c -f` on the target host.

## Reference Navigation (Load Only What You Need)

- `references/quickstart.md`
  - Minimal and common ruleset templates to start from
- `references/hook-action-cheatsheet.md`
  - Fast hook/action legality reminders
- `references/nftables-patterns.md`
  - Reusable host/router patterns (sets, NAT, port forwarding, egress)
- `references/constraints-matrix.md`
  - Detailed constraints with doc/source rationale
- `references/common-pitfalls.md`
  - LLM-heavy mistakes and corrected examples
- `references/nftables-ops-cheatsheet.md`
  - Operational commands, persistence, systemd unit/drop-in scanning
- `references/debug-workflow.md`
  - `nft -c`, debug flags, and triage workflow
- `references/nftables-troubleshooting.md`
  - Runtime troubleshooting and multi-source persistence debugging
- `references/reference-index.md`
  - Topic map for this skill (what to open for what task)
- `references/source-map.md`
  - Official docs/source file map and search keywords
- `examples/nftables/`
  - Ready-to-edit example rulesets (web server, router NAT, dual-stack host)

## Authoring Guardrails for Agents

- Prefer explicit protocol context (`tcp`, `udp`, `icmp`, `icmpv6`) over ambiguous shorthand when generating code.
- In `table inet`, prefer separate IPv4 and IPv6 rules unless there is a strong reason to merge.
- Do not invent hook support. If unsure, check the matrix and verify with `nft -c`.
- Treat wiki examples as useful examples, not the sole source of truth.
