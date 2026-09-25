---
name: medium-seo-publisher
description: Use when researching, drafting, revising, or publishing a Medium article that needs search-demand validation, title protection, author-voice editing, or outcome measurement.
license: MIT
metadata:
  version: "1.1.0"
  editorial-profile: "1"
---

# Medium SEO Publisher

Turn a topic into an evidence-backed Medium article and a measurable publishing experiment. Default to preparing a reviewable package. Publishing requires an explicit request in the current task; creating or invoking this skill does not grant that permission.

## Agent compatibility

These are portable Markdown instructions. Use the current host's tools for files, search, browser interaction, and scheduling; no particular agent API, filesystem root, or slash-command syntax is required. The optional agents/openai.yaml file only supplies UI metadata for hosts that understand it; other hosts may ignore it.

On hosts without skill discovery, the user can provide SKILL.md and its relative reference files directly. Resolve references relative to this package. If a required tool is absent, complete only the supported mode and state the precise limitation. Text-only agents can revise prose or work from compatible evidence produced by an approved provider; live research requires web and provider access, and publishing requires an authenticated browser tool. Do not claim every host has been tested.

## Choose the mode

- **SEO validation is the default for every new or existing Medium article.** A supplied topic, title, outline, or draft is input to the research; it is not permission to skip it. Unless the user explicitly asks for **editorial-only** or **prose-only** work, run measurement preflight, the provider metric gate, current SERP inspection, keyword selection, source research, writing or revision, and SEO title validation.
- Modes compose in the order requested. For writing, revising, refreshing, or publishing, complete the default SEO workflow before delivery or publication. If the provider gate blocks research, stop before selecting a keyword, validating a title, drafting, revising, or publishing.
- **Create or revise an SEO-led article:** use the default SEO workflow for a new idea and for an existing article, including when the user supplies the subject, title, or draft.
- **Refresh an SEO title or direction:** run the provider gate, inspect the current SERP, select the supported keyword, and validate the SEO title. Reuse compatible evidence only when [research.md](references/research.md) considers it current.
- **Create an editorial-only article:** use this exception only when the user explicitly asks for editorial-only work. Draft and source the article without SEO research, and state that no keyword winner or SEO title was validated.
- **Revise prose only:** use this exception only when the user explicitly asks for prose-only work. Preserve the existing title decision, make no SEO claims, and state that search demand, keyword selection, the current SERP, and the title were not validated.
- **Publish an approved draft:** unless the user explicitly chose an editorial-only or prose-only exception, complete the default SEO workflow in the current task before the Medium policy, field, destination, and submission checks.

## Quick preflight

Reuse session context. Check only what affects the next action; keep routine checks out of the conversation.

- Read [measurement.md](references/measurement.md). Establish the topic or existing article, audience, language, and primary outcome. Unless the user explicitly chose an editorial-only or prose-only exception, also establish the search engine and market and explain a proposed market briefly to a novice. Establish the canonical destination when publication or cross-posting makes it relevant. Infer safe defaults and recommend engaged reads as the novice outcome; ask one bundled question only when missing values would change the research or publication.
- For every new or existing article outside an explicit editorial-only or prose-only exception, inventory access to the providers in [provider-options.md](references/provider-options.md) before declaring the metric gate blocked: connected tools or APIs, compatible exports, existing authenticated provider tabs, controllable browser sessions, and first-party public interfaces. A website login is not API access, but its normal UI is a valid research route when the host can operate it.
- Reuse user-provided access and already logged-in sessions. When the live provider page documents additional free usage after login, explain the allowance in plain language and ask the user to sign in or create the free account. Also state that a trial or paid plan is available and link to current official terms. Do not sign up, start a trial, subscribe, spend credits, or bypass access controls without the user's explicit choice.
- If the user declines payment or Semrush remains unavailable, continue through the free-first provider order in [provider-options.md](references/provider-options.md). Ask before any login or trial required by the next provider, but do not ask again about a payment option the user rejected. After the usable free options are exhausted, present the paid list once and stop if the user declines it. Only an explicit editorial-only or prose-only request bypasses the metric gate.
- Locate an available Humanizer through the host's skill catalog or configured skill directories. Prefer the host-configured skill, then the closest capability match; do not ask the user unless the choices would materially change the output. Constrain it to prose editing: this skill retains control of research, citations, factual preservation, title validation, and publishing. Read [editorial.md](references/editorial.md) and load missing guidance before one integrated rewrite. No automatic download or replacement.
- Check Medium account identity only for requested editor work. Before publication, verify the actual destination and current publish settings.

## Research with bounded effort

This section applies by default to every new or existing Medium article, including requests that supply only a topic, title, outline, or draft and requests to revise or publish. Skip it only when the user explicitly asks for editorial-only or prose-only work.

Read [research.md](references/research.md). Reuse recent compatible observations when appropriate; date them and refresh finalists when the decision depends on current competition.

Prefer one bulk discovery request and one bulk metrics request when the available route supports them, then inspect the viable finalists. A connector is an optional way to reach the provider, not a prerequisite: an approved provider may instead be available through a logged-in browser UI, including an agent's in-app browser. Discover a connected tool's current schema and limits rather than assuming commands. Follow the provider gate in [research.md](references/research.md).

Triangulate the final three candidates, or all candidates if fewer, with a second approved provider when available. Treat this as independent vendor/model corroboration, record known upstream overlap, and retain provider-specific scales. If only one provider is accessible, report single-provider evidence and the uncertainty.

Do not stop before the minimum research floor is complete: every candidate eligible to win has both required metrics for the target market, a current localized SERP was inspected, the evidence record is complete, and a second-provider check was performed whenever accessible. Further research may stop when it is unlikely to change the decision.

Select one winner and explain the competitive opening, reader intent, original contribution, and limitations. Include a title brief that states which search question the recommended title serves, what it promises, and why the current results leave room for this article. A high volume or low difficulty badge is insufficient. If user thresholds are unmet, say so; do not silently lower them.

## Prepare the article

Read [editorial.md](references/editorial.md) and [sourcing.md](references/sourcing.md). If a writing sample exists, read it before drafting; later explicit corrections override habits in the sample.

Author the complete article unless the user asks only for research, an outline, or editing. Build it around the selected reader question and answer that question early. Preserve the author's interpretation while distinguishing it from factual claims. Use verified sources; never invent personal experiences, research, numbers, or quotes. Source research is separate from keyword research.

Prepare the article, story title/subtitle, preview-card title/subtitle, up to five relevant topics, image direction/alt-text draft, and material-claim source record together. By default, also include the proposed search snippet and keyword evidence. After an explicit editorial-only or prose-only request, mark search metadata as not researched instead of inventing it. Treat fields not observed in Medium as deliverable metadata rather than controls that were set. Make headings and FAQs serve the reader; do not force a template into an essay. Preserve user edits when rereading the final file.

Run one integrated editorial pass followed by a whole-document factual and voice review. Rewrite affected paragraphs rather than repeatedly swapping phrases. Do not certify prose as human or mistake a clean word scan for editorial quality.

## Keep the title tied to the research

By default, treat the recommended title as part of the research decision, not as decoration added after drafting. Validate it against the selected keyword and current SERP, then present it with a short plain-language rationale covering the search question, likely reader, competitive opening, article promise, and how the draft fulfills that promise. After an explicit editorial-only or prose-only request, give an editorial rationale covering the likely reader, article promise, and how the draft fulfills it; do not claim a search question or competitive opening was validated.

For an SEO-led title, evaluate a proposed replacement instead of accepting or rejecting it mechanically:

- If it preserves the same reader intent and factual promise, refine it if useful and recheck its clarity against the research.
- If a more literary Medium headline can coexist with a separate search title, use both only when they describe the same article honestly. Explain the role of each.
- If it changes the topic, intent, or promised answer, do not call it the researched winner. Explain the mismatch and retain the supported title, or run a focused research refresh for the new direction.
- If the user explicitly chooses a materially changed title, preserve their editorial decision but do not publish or describe it as SEO-validated until a focused refresh passes the metric and SERP floor. If they explicitly choose an editorial-only or prose-only path, mark the earlier title conclusion as superseded, omit researched-winner claims, and re-baseline measurement.

After an explicit editorial-only or prose-only request, compare a replacement title with the article's reader and promise without claiming SEO validation. In every other case, a replacement title stays in the default SEO workflow.

Research on one query does not automatically validate nearby topics. Related queries can suggest an article cluster, but each materially different article needs its own intent and competition check. Search research improves the choice; it does not guarantee ranking, readership, or that every nearby topic is suitable for the author.

## Deliver or publish

Prepare mode ends with a reviewable article and metadata, evidence gaps, and a measurement plan. Use a task folder supplied by the user or a clearly named local output folder. Reuse existing artifacts instead of creating redundant reports.

When publication is explicitly requested, read [publishing.md](references/publishing.md). Use the live editor, preserve attribution and access settings, verify all publish controls, and confirm the public result. Subscriber email notification is a separate setting; do not infer permission from permission to publish.

Include a proportional follow-up schedule in the deliverable, anchored to publication or the material-update date. Create actual scheduled jobs only when requested.

## Completion standard

- Unless the user explicitly requested editorial-only or prose-only work, completion requires a passed provider metric gate, a selected keyword, a current localized SERP inspection, and an SEO title validated against that evidence. Supplying a topic, title, outline, or draft does not satisfy or waive these checks.
- For an explicit editorial-only or prose-only exception, report that provider metrics, the current SERP, keyword selection, and SEO title validation were not performed.
- Every winning candidate has provider, market, metric dates, volume, organic difficulty, and uncertainty; incomplete rows remain unvalidated leads.
- Every material factual claim is sourced, qualified, or removed.
- Article and title fulfill the same reader promise and preserve factual meaning and author voice.
- Metadata agrees with the article; references and image attribution survive editing.
- Prepare mode reports readiness and gaps. Publish mode reports the verified URL and observed access/notification state.
- Never promise rankings, conversion, earnings, or stars. Package validity and editorial scores are not outcome evidence.
