---
name: bmad-os-skill-to-bundle
description: Convert a BMad skill into a downloadable web bundle (Gemini Gem + ChatGPT Custom GPT) with a persona, install instructions, and knowledge files. Use when a user wants to publish a skill to consumer LLM platforms (Gemini, ChatGPT).
---

# bmad-os-skill-to-bundle

Convert a BMad skill folder into a self-contained web bundle a non-technical user installs as a Gemini Gem or ChatGPT Custom GPT. Canonical example: `assets/example-bundle/`. INSTRUCTIONS scaffold: `assets/instructions-template.md`.

## What the bundle must carry that you cannot derive from the source

- **Persona/protocol split.** The pasted INSTRUCTIONS block defines the voice. The uploaded `SKILL.md` defines the protocol. Both required.
- **Persona inheritance from an owning agent.** If a `bmad-agent-*` peer in the same module owns this work (analyst owns brainstorming, research, brief, PRFAQ; pm owns PRD, epics, stories), lift `name`, `title`, `icon`, `role`, `identity`, `communication_style`, `principles` verbatim from its `customize.toml`. Invent only when no owning agent exists.
- **One methodology master named in the protocol.** Bezos for Working Backwards, Osborn for brainstorming, Cagan for PRD, Kerth for retro, Norman for UX. Persona-level influences stay in the persona; methodology champions live in the protocol. Two max.
- **Canvas-first, visual-first, web-search-biased.** Consumer platforms have no filesystem; anything that accumulates lives in Canvas, updated as content forms. Mermaid (rendered as HTML) and HTML tables beat prose for structural content. Training data is months stale, so the protocol must instruct the persona to web-search rather than recall whenever facts could have moved (people, products, versions, prices, events, regulatory state).
- **Framework dependencies translated, not dropped.** No subagents, scripts, gh/git, filesystem, or skill loading at runtime. Subagents become sequential passes; scripts become prose or inline code; tool calls become asking the user; loaded validation skills become a sibling reference file the protocol loads during polish.
- **No decision logs.** Even if the source skill keeps one. Canvas continuous-update replaces it.
- **`[preferences]` defaults to none.** It earns a slot only for values that persist usefully across sessions (default user name is the classic). Per-session choices (mode, depth, focus) are opening conversation, not preferences.
- **Outcome-driven prompt craft.** Every line in the bundle must pass "would a capable LLM do this correctly without being told?" If yes, cut it. Trust the model: it knows how to coach, mirror, ask follow-ups, honor user steering, avoid hedging, and stay in character. Bundles state goals, non-obvious failure modes, and specifics the LLM cannot derive (named methodologies, capture formats, ID schemes, validation dimensions, Mermaid type names). Source skills often carry ceremonial framing, restated values, and LLM-default coaching advice that earned its place in a framework context but bloats a bundle. Strip it. A bundle 30-50% smaller than its source is normal and good.

## Inputs

- **Skill folder path** (required): contains `SKILL.md` plus optional `references/` and data files.
- **Bundle name / output path** (optional): override the derived slug and `bundles-output/<slug>/`.

## On Activation

Confirm the source path, the derived slug, the owning-agent persona source (if any), and the output destination. Then proceed.

## Operation

1. **Read the source whole.** Source `SKILL.md`, every `references/*.md`, every data file. Identify the methodology master, the owning agent, the data dependencies, and any doc-validation rules the source applies to its own outputs.

2. **Plan the translations.** Map each framework dependency to its persona-executable equivalent before writing. If something is pure deploy automation with no LLM essence, surface it and decide with the user.

3. **Write the bundle `SKILL.md`.** Rewrite the source as standalone instructions a persona can execute on a consumer platform. Inline `references/` content; strip `{project-root}`, customize.toml, file routing, on-activation scaffolding. Bake in: Canvas at start with continuous updates, visual-first via Mermaid/HTML, web-search bias for stale facts. Name the methodology master. Put the polish work (and the validation-file load if any) at the end of the session flow.

4. **Lift validation to its own file** (if the source applies one). Write to `<bundle>/<purpose>-validation.md` and have the protocol load it during polish.

5. **Copy data files** (`.csv`, `.yaml`, `.txt`) unchanged.

6. **Generate the personas.** Default: inherited from the owning agent if one exists; otherwise invented with 1 or 2 named practitioners in `identity` and a `suggested_focus` ending "Mention this focus in the opener as an invitation, not a constraint; the user may steer anywhere." One swap-example: contrasting voice, equal competence, same field shape.

7. **Fill `INSTRUCTIONS.md`** from `assets/instructions-template.md`: title, persona, swap-example, list of files to upload, and the Web Browsing capability line if the protocol uses search. Inside every YAML block scalar (`role: |`, `identity: |`, `communication_style: |`, `suggested_focus: |`), each paragraph must be a single physical line — no hard wraps at any column width. Viewers word-wrap; hard wraps just produce annoying ragged breaks.

8. **Trim pass.** Read the drafted `SKILL.md` and `INSTRUCTIONS.md` end to end and cut every line that fails "would a capable LLM do this correctly without being told?" Specifically hunt for: ceremonial preambles ("This file defines..."), `## Closing Stance` flourishes, restated rules across multiple sections, LLM-default coaching advice (don't hedge, honor user steering, mirror before pushing), anti-patterns that restate the core stance, and INSTRUCTIONS lines like "Do not skim. Do not answer from priors." Compare line count to the source: a 30-50% reduction is normal. If the bundle is the same size or larger than the source, something went wrong; trim again.

9. **Confirm and write.** Show the bundle path and file list; ask before overwriting a non-empty destination.

## Anti-patterns

- Pasting the source `SKILL.md` raw as the bundle protocol. Framework idioms will not translate.
- Inventing a persona when an owning `bmad-agent-*` exists.
- Generating a swap-example that is a near-clone of the default.
- Leaking `bmad-os-`, `{project-root}`, customize.toml, or file routing into bundle output.
- Ceremonial preamble in the bundle ("This file defines... The protocol is binding. The persona is the voice that delivers it."). Open with content, not framing.
- A `## Closing Stance` flourish at the end of the bundle SKILL.md. Cut it.
- Anti-patterns that restate LLM defaults: "do not hedge", "do not flatten the user's voice", "honor user steering", "do not drop the persona's voice", "do not author for them" (after the core stance already said it). Keep only the non-derivable rules.
- Restated rules across multiple sections of the bundle. "Don't pad / don't fabricate / be honest" said in Core Stance, Constraints, Anti-patterns, *and* the template means three of those are bloat.
- "Do not skim. Do not answer from priors." in the INSTRUCTIONS paste body. Plus the 6-clause persona-discipline restatement (fulfill role / embody identity / speak style / hold principles / prefix icon / do not break character). Collapse to one sentence: "Stay in character until the user dismisses the persona."
- Icon-prefix instruction repeated in SKILL.md, INSTRUCTIONS.md paste body, *and* the `communication_style` field. Pick one place; the SKILL.md top is the natural home.
- Em dashes anywhere in generated content.
- Hard-wrapped paragraphs inside YAML block scalars (`role: |`, `identity: |`, etc.) in `INSTRUCTIONS.md`. Each paragraph is a single physical line; viewers handle the wrapping.

## Reference

`assets/example-bundle/` (brainstorming coach) is the canonical bundle to study. `assets/instructions-template.md` is the INSTRUCTIONS scaffold.
