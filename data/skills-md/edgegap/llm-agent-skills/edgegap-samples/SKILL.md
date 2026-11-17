---
name: edgegap-samples
description: 'Find the right public Edgegap sample project, SDK or build tool to learn from or copy: a game already running on Edgegap with the same engine, netcode or backend (Unity with Mirror, NGO, FishNet, PurrNet, Photon Fusion or Netcode for Entities; Unreal and Lyra; Godot; Colyseus; Nakama; PlayFab; Three.js; Supabase; Cocos; relays), how recently each was updated, which ones are verified and which are outdated, and which Edgegap skill walks through it. Use when someone asks for an Edgegap example, sample, demo, template, starter or reference project, wants to see working code before integrating, or asks whether a sample repo is still current. For the integration steps themselves, load the engine skill the catalog points to (edgegap-unity, edgegap-unreal, edgegap-godot, edgegap-colyseus and so on); for picking a server shape, edgegap.'
metadata:
  version: "0.1.5"
---

# Edgegap samples

Edgegap publishes its samples, SDKs and build tools on GitHub under [github.com/edgegap](https://github.com/edgegap). A working sample with the same engine and netcode as the developer's game is often the fastest way to show what "done" looks like, but the repos were written at different times and some are years old. This skill says which one to open and how far to trust it.

The full list is in [references/catalog.md](references/catalog.md): every public repo, its engine and netcode or backend, the date of its last commit, and the skill that covers it.

## Pick a sample

1. **Match the stack first.** Engine, then netcode (or backend), then client platform (desktop, WebGL/browser, mobile). A sample with the right netcode on an older engine version teaches more than one with the right engine and a different netcode.
2. **Prefer a current sample.** "Current" in the catalog means updated in late 2026 and run end to end on Edgegap by the skill that links it. Those match today's plugins, SDKs and the matchmaker. "Legacy" means a 2024 or older repo: written for older Unity versions and plugins, sometimes under Edgegap's old product name (Arbitrium), with docs links that may have moved. Read a legacy sample for the idea, and take the steps from the current engine skill.
3. **Then load the skill the catalog names.** The sample shows one game; the skill has the steps, templates and pitfalls for any game on that stack. When the catalog names no skill, the sample is all there is: say so, and check it against the current engine skill before following it.

## Use a sample safely

- **Check the licence before copying code.** Forks keep their upstream licence (Unity Companion License, Photon's terms, no licence at all for some demos). Photon Fusion samples and Epic's Lyra are licensed content: the Edgegap repos hold only Edgegap's files, and the developer brings the rest from the vendor.
- **Never reuse a sample's Edgegap resources.** App names, versions, matchmaker URLs and tokens in a sample belong to whoever ran it. The developer creates their own (see `skills/edgegap/references/agent-rules.md`).
- **Branches matter.** Several samples keep the Edgegap work on a branch (`feature/edgegap`, `after`, `lyra-edgegap`) rather than the default branch. The catalog notes them; the default branch of a fork may be the untouched upstream game.

## Keep the catalog honest

The dates in the catalog are the last commit on each repo's default branch, checked on 2026-11-04. Refresh them before relying on "current" or "legacy" for a decision:

```bash
gh api repos/edgegap/<repo> --jq .default_branch
gh api "repos/edgegap/<repo>/commits?sha=<branch>&per_page=1" --jq '.[0].commit.committer.date'
```

A sample moves from legacy to current only when someone runs it end to end on Edgegap again, not when a README changes.
