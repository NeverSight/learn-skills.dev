---
name: generating-game-changelogs
description: Generates player-facing game changelogs from implementation plans and git history. Covers thematic intros, system-grouped sections, and concise flavor descriptions. Use when generating a game changelog, writing game release notes, or preparing an update post for itch.io or Steam
---

# Generating Game Changelogs

Generate a player-facing game changelog from a completed implementation plan and git history.

## Reference Files

| File | Read When |
|------|-----------|
| `references/changelog-format.md` | Writing the changelog entry — contains the format template, emoji mapping, tone rules, approved sample, and non-game adaptation guidance |

## Workflow

Copy this checklist and work through it:

```
- [ ] Phase 1: Gather sources
- [ ] Phase 2: Extract & classify changes
- [ ] Phase 3: Version & theme
- [ ] Phase 4: Group into sections
- [ ] Phase 5: Write the entry
- [ ] Phase 6: Save & verify
```

### Phase 1: Gather Sources

Collect all inputs before synthesizing anything.

1. **Read `IMPLEMENTATION_PLAN.md`** (or equivalent plan file) in the project root.
   This is the primary source — it has richer descriptions than git commits.
2. **Read git log** since the last release tag or the previous changelog entry.
   Use `git log --oneline` to get a quick summary; dig into individual commits when the plan doesn't cover something.
3. **Read existing `CHANGELOG.md`** if it exists.
   Note the previous version number and format so the new entry stays consistent.

If no implementation plan exists, fall back to git history as the sole source.

### Phase 2: Extract & Classify Changes

Walk the plan section by section:

- **Completed tasks only** — items marked `[x]`, `✅`, or with status `✅ Done` become changelog candidates.
  Skip anything marked `[ ]`, `⏳`, or `🔄`.
- **Cross-reference git** — check if any commits introduce changes not captured in the plan.
  Add those as additional entries.
- **Filter non-user-facing items** — exclude:
  - Internal refactors with no visible effect
  - Build/tooling changes (CI, linting, dev dependencies)
  - Code comments, documentation-only changes
  - Sprite/asset pipeline details (describe the feature, not how it was made)
- **Classify each item** as one of:
  - **New** — entirely new feature, system, or content
  - **Changed** — existing feature modified, improved, or rebalanced
  - **Fixed** — bug fix or correction

### Phase 3: Version & Theme

**Version number:**

1. Check `package.json` for a `version` field
2. Check git tags (`git tag --sort=-v:refname | head -5`)
3. Check the previous entry in `CHANGELOG.md`

**Subtitle:**

Come up with a short, evocative subtitle that captures the update's theme (e.g., "Dissolution Expands", "The Deeper Dark", "The Final Frontier").
This becomes the quoted string after the version: `v0.2.0 "Dissolution Expands"`.

**Thematic summary:**

Draft 1–2 sentences that capture the feel of the update.
Focus on what players will experience, not what was implemented.
Write in present tense, active voice.

### Phase 4: Group into Sections

Group changes by game system or project area — whatever feels natural for what players/users care about.
For games, think in terms of world, combat, crafting, farming, creatures, abilities, etc.
For non-game projects, see the adaptation guidance in `references/changelog-format.md`.

**Grouping rules:**

1. Group by the system or area where the user experiences the change.
2. Minimum 2 items per section — merge small sections into the closest related one.
3. Maximum ~7 sections — combine if you have too many.
4. **Fixes & Improvements** is always the last section.
5. Order sections by impact — most exciting changes first.
6. Each item appears in exactly one section.

**Spotlight intros:**

For major sections (3+ items, significant new content), write a one-sentence intro line below the section header.
Keep it flavorful and user-facing.
Skip intros for small sections or Fixes & Improvements.

### Phase 5: Write the Entry

Read `references/changelog-format.md` for the full format template.

**Key rules (inline for speed):**

- **Player-facing tone** — describe what the player sees, does, or encounters.
  Not: "Added BiomeManager class with config-driven spawning."
  But: "Four new regions beyond the void ring, each with unique wildlife and resources."
- **No stats** — don't include HP, damage numbers, cooldowns, or growth times.
  Not: "Shadow King has 500 HP and deals 25 damage per bolt."
  But: "A multi-phase boss lurking in the dark forest."
- **No implementation details** — don't mention file names, class names, config changes, or asset pipelines.
- **No empty sections** — if a section has no items after grouping, omit it entirely.
- **Bold item names** — each bullet starts with a bolded feature name, then a dash, then the description.
- **Sub-items use italics** — for lists within a feature (e.g., biome names), use `*italic*` names with a dash and brief description.
- **One emoji per section header** — placed before the section title, not on individual items.

**Format structure:**

```
**{ProjectName} — v{Version} "{Subtitle}"**

_{Thematic summary}_

### {Emoji} {Section Title}
{Optional spotlight intro}

- **{Feature Name}** — {Player-facing description}
  - *{Sub-item}* — {Brief description}

### 🔧 Fixes & Improvements
- {Fix description}
```

### Phase 6: Save & Verify

1. If `CHANGELOG.md` exists, **prepend** the new entry above existing content (keep a blank line separator).
2. If `CHANGELOG.md` doesn't exist, **create it** with the entry.
3. **Read the file back** to verify it was written correctly.

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Including HP, damage, cooldown numbers | Describe the experience: "tough multi-phase boss" |
| Mentioning file paths or class names | Describe the feature players interact with |
| "Added ShadowKingBoss.js with 3 phases" | "A new boss lurks in the dark forest" |
| Empty sections with "None this update" | Omit sections that have no items |
| Listing every commit message | Synthesize related commits into cohesive feature descriptions |
| Mentioning sprite generation or AI tools | Describe the visual result: "new hand-crafted item sprites" |
| Dev diary tone ("We worked hard on...") | Direct, present-tense descriptions of what's new |
| Repeating the same change in multiple sections | Each item appears in exactly one section |
