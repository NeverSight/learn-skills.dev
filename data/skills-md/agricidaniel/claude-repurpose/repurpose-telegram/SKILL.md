---
name: repurpose-telegram
description: >
  Generates Telegram Channel content from content atoms: structured channel posts,
  formatted deep dives, and quiz-ready polls. Optimizes for markdown-rich formatting,
  information density, and forward-ability. Sub-skill of the Content Repurposing
  Engine. Use when user says "telegram", "telegram channel", "telegram post",
  "telegram broadcast", or "repurpose for telegram".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Telegram Channel Content Generator

Generate a channel post, formatted deep dive, and poll from content atoms.

## Inputs

You receive from the orchestrator (`repurpose-broadcast`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `brief_mode` | If true, produce channel post only |

## References

Load before generating:

- `references/platform-specs.md` -- character limits, formatting, algorithm signals
- `references/hook-formulas.md` -- headline and editorial hook formulas
- `references/voice-adaptation.md` -- Telegram tone rules (structured, editorial, dense)

## Platform Rules

| Spec | Value |
|------|-------|
| Channel post limit | 4096 chars |
| Formatting | Full markdown (**bold**, _italic_, `code`, [links](url)) + HTML subset |
| Images | Unlimited per post, any ratio |
| Polls | Up to 10 options, 100 chars each, quiz mode, anonymous/public |
| Buttons | Inline URL buttons (up to 8 per row) |
| Silent messages | Send without notification (supported) |
| Scheduled posts | Native scheduling |
| Forward visibility | Posts forwarded to other channels/groups |
| Best time | 9-11 AM and 7-9 PM |

## Core Principle: Curated Feed

Telegram channels are curated feeds. Subscribers expect consistent, well-formatted,
information-dense posts. Quality of formatting matters -- Telegram users notice and
appreciate well-structured markdown. Forward-ability is a growth lever: design every
post to be worth sharing.

## Output 1: Channel Post

**File:** `telegram/post.md`

**Length:** 500-1000 chars.

**Structure:**
1. **Bold headline** -- Editorial headline using `**bold**`. Must work as standalone hook.
2. **Key insight paragraphs** -- 2-3 short paragraphs from highest-impact atoms.
   Use **bold** key terms, _italic_ for emphasis, `code` for tools/commands.
3. **Takeaway list** -- 3-5 actionable points. Bold the lead phrase of each item.
4. **Link button suggestion** -- Inline URL button for CTA. Button text describes
   outcome, not action.

**Rules:**
- Bold key terms aggressively -- Telegram readers scan
- One idea per paragraph, max 3 sentences
- Every post must deliver standalone value
- Link buttons preferred over inline links for CTAs

## Output 2: Formatted Deep Dive

**File:** `telegram/deep-dive.md`

**Length:** 1000-2000 chars. Only generate for high-value content with 5+ atoms.

**Structure:**
1. **Headline** -- Bold, editorial, slightly longer than channel post headline.
2. **Problem/context** -- 2-3 sentences. Use _italic_ for the key question.
3. **Insight with evidence** -- 2-3 paragraphs from `stat`, `insight`, and
   `contrarian` atoms. Bold data points and key conclusions.
4. **Actionable steps** -- Numbered list (1-5 steps). **Bold lead phrase** +
   one sentence explanation per step. Must be concrete and immediate.
5. **CTA with inline button** -- Suggested URL button ("get the full breakdown").

**Rules:**
- Justify the length with density -- every paragraph adds new information
- Use all available formatting (bold, italic, code, lists)
- Numbered steps mandatory for actionable content
- Should feel like a mini-article, not a stretched post

## Output 3: Poll

**File:** `telegram/poll.md`

| Spec | Constraint |
|------|-----------|
| Options | 3-5 (under 100 chars each) |
| Max options | 10 (platform limit) |
| Quiz mode | Optional -- mark correct answer with explanation |
| Voting | Anonymous for opinions, public for quizzes |

**Poll structure:**
1. **Setup message** -- 1-2 sentences of context posted before the poll.
2. **Question** -- Specific and debatable. From the content's central tension or
   common misconception.
3. **Options** -- Defensible positions. Include one that challenges conventional
   thinking. Order from most to least expected.
4. **Quiz mode** (optional) -- For content with a clear correct answer. Include
   1-sentence explanation for the correct option.

## Tone Rules

| Do | Do NOT |
|----|--------|
| Use editorial, structured voice | Write casually like a text message |
| Bold key terms and data points | Leave text unformatted |
| Use numbered lists for steps | Use bullets for sequential actions |
| Format aggressively (bold, italic, code) | Rely on plain text |
| Write information-dense paragraphs | Pad with filler or pleasantries |
| Design posts worth forwarding | Write self-referential content |
| Use inline button suggestions for CTAs | Bury links in paragraph text |

## Output Format

```markdown
# Telegram Channel Post: [Topic]

**[Bold headline]**

[Formatted post body with markdown]

---
**Posting notes:** [best time, silent message suggestion, button configuration]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 channel post (highest-impact atoms, standard format)
- Skip deep dive and poll

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Shorter post (300-500 chars); skip deep dive |
| No `stat` or `insight` atoms | Use `howto` + `quote` atoms; frame as practical guide |
| `brief_mode` is true | Generate channel post only; skip deep dive and poll |
| Content too casual | Increase structure; add bold formatting and lists |
| Content is promotional | Reframe as editorial insight; strip product mentions |
| Long content (10+ atoms) | Split into channel post + deep dive |
