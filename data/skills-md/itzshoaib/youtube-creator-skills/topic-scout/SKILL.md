---
name: topic-scout
description: Deeply research and rank YouTube video topic opportunities using current channel, audience, search, and competition evidence. Use before Video Kit for topic discovery; not for scripting or channel-memory maintenance.
---

# Topic Scout

Find promising YouTube video topics for a specific channel, then show why each is worth considering. Treat research as evidence about opportunity, not a forecast of views or growth.

## Workflow

1. **Load channel context.** Read the active `CHANNEL_MEMORY.md` and relevant style references. If the user asks for channel-specific ideas and no channel or memory is identifiable, ask only for the channel URL or handle. If context is unavailable but a topic is supplied, research it and label channel fit as unknown rather than blocking.
2. **Inspect current channel state.** Review recent uploads and relevant back-catalogue videos. Read recent `analytics/` performance reviews if present, and use only their dated, scoped findings. Identify established topics, formats, audience promises, repeatable strengths, recent changes, and ideas already covered. Treat public views and comments as partial clues, not private analytics or representative audience research. Do not compare raw views across videos of very different ages or formats as if they were equivalent.
3. **Research opportunities.** Follow [opportunity-research.md](references/opportunity-research.md). Use current, channel-specific evidence for both Search and recommendation-led viewing. Browse current sources, record links and checked dates, and distinguish observed facts from inference. Use private Studio information only when it is already accessible or the creator supplies it; never ask for credentials.
4. **Develop and rank ideas.** Make ideas specific to an audience, need, promise, and channel angle. Include a balanced mix of evergreen, timely, search-led, or recommendation-led ideas only where evidence supports them. Rank by audience/channel fit, demand evidence, quality of the opportunity gap, creator's ability to deliver, and production/timing constraints. Explain trade-offs; do not present a keyword score or ranking as objective certainty.
5. **Deliver a usable shortlist.** Unless the user asks for another scope, return up to five prioritized idea briefs with evidence, a distinct angle, and an honest confidence level. Give one clear recommendation and identify assumptions or facts that would change the ranking. Read the reference for the required evidence and idea-card format.
6. **Hand off cleanly.** For a selected idea that needs topic facts, an outline/script, or upload assets, continue with Video Kit (`video-kit`) when available. Keep the research brief as supporting evidence; Video Kit owns the per-video deliverables.

## Boundaries

- Channel-wide positioning, broad strategy, and quick ideation belong to YouTube Manager (`youtube-manager`). Use Topic Scout when deeper, current opportunity research or a ranked shortlist is wanted.
- Do not claim access to private analytics, exact search volume, guaranteed rankings, or likely view counts without reliable supplied evidence. Never promise channel growth.
- Do not keyword-stuff, copy competitors, or recommend a topic solely because it is trending. A viable idea needs a clear viewer benefit, channel fit, credible proof or demonstration, and an accurate packaging promise.
- Return ideas in chat by default. If asked to save a scan and no ideas convention exists, create `ideas/YYYY-MM-DD-<scan-slug>.md` in the channel workspace. When a concept is selected, let Video Kit put the needed research in that video's project; do not create a video project for an unselected idea.
