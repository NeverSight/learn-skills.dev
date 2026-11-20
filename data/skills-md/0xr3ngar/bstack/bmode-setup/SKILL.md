---
name: bmode-setup
description: "Set up models and swarm reviewers, and tune the user's bStack skill files from conversation history and their answers during setup."
license: MIT
compatibility: "Model and swarm setup requires T3 Code and its MCP server `t3-code`. Skill tuning requires writable personal skill files and can use local history."
---

# Bmode-setup

Read the [defaults and T3 Code tools](references/defaults.md) and the user's existing settings. If the t3-code MCP server is unavailable, explain which model settings you cannot check and continue with skill tuning.

Before asking the model setup questions, check the [three provider catalogs](references/defaults.md#swarm-presets) and their release notes for the latest models, including providers disabled locally. Show what's current for each provider and link the source. If a lookup fails, say which provider's latest releases you could not verify. Offer newer models as alternatives. Keep the listed defaults and the user's saved choices until they choose a change.

Check local availability with `orchestrator_capabilities`. Use its `search` option for models missing from the shortlist. Match each model to its serving provider and use the effort options that provider exposes. Show disabled providers and missing models as unavailable. If the user requests an unavailable model, let them choose a replacement.

For full setup, use [skill-retro](../skill-retro/SKILL.md) in analysis-only mode before the interview. Bring its findings into question 5. If the skill or history is missing, use the user's answers to that question. Ask the applicable questions together. For a request limited to one setting, change just that setting. During feature work, use saved settings and ask only for a choice the current phase needs.

1. Which model should orchestrate features? Suggest Fable 5.2 at high effort.
2. Which model should implement changes? Suggest Opus 5.5 at high effort.
3. Which reviewers should a plain `/swarm` use by default? Show the user's saved lineup first and let them keep it. They can combine any [provider presets](references/defaults.md#swarm-presets), choose **All recommended** across all three, or pick individual models. Show **Claude Code + Cursor** and **Claude Code + Codex** as shortcuts when available. Expand each choice into its available reviewers, flag any missing models, and let the user add or remove members before saving. A lineup needs at least two models.
4. Which other settings should change? Show each current value. Build mode accepts `threads` or `inline`.
5. Which skill behaviors should change or stay as they are? For each recurring correction, show the decision it affected, the skill file and the proposed wording. Let the user accept, revise, skip, or add a preference from their own experience.

Write the operating settings from questions 1–4 to `~/.config/bstack/preferences.md`, one line per override. Always save each selected member's provider instance and model ID on the swarm line. Omit other values that match a default.

Apply the user's choices from question 5 directly to the relevant `SKILL.md` or playbook in their own bStack skills, using skill-retro's ownership check and replay steps. If skill-retro is unavailable, verify each target resolves inside a skill from the bStack checkout, the user's bStack fork, or an installation with a matching source record. Skip unverified targets and check each approved edit against an example request. Show the changed files and what the agent will do differently next time.

Before launching delegates, announce their models and effort. Start each message with `Read <absolute path>/delegates.md before anything else.` Use the absolute path of the [delegate instructions](references/delegates.md). Check claims before using them. Start fresh delegates for a new round and pass earlier reports as files.
