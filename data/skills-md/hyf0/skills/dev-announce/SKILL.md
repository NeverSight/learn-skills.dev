---
name: dev-announce
description: "Generates developer tool feature announcement tweets in an understated, data-driven style. Use when drafting tweets to announce new features, performance improvements, or API additions for projects like Rolldown. Do NOT use for general social media posts, blog writing, or non-technical announcements."
metadata:
  author: yunfeihe
  version: "1.0.0"
  category: content-creation
  tags: [tweets, announcements, developer-tools]
---

# dev-announce

Generate developer tool feature announcement tweets that are understated, proof-driven, and technically credible. Inspired by the style used in Bun's feature announcements.

## Workflow

Copy this checklist and check off each step:

```
- [ ] Step 1: Understand the feature (read code/PR/commits if available)
- [ ] Step 2: Classify the feature type
- [ ] Step 3: Gather input details
- [ ] Step 4: Draft main tweet
- [ ] Step 5: Draft thread replies (optional)
- [ ] Step 6: Suggest visual proof
- [ ] Step 7: Verify against anti-patterns
```

### Step 1: Understand the Feature

Before writing anything, build a real understanding of the feature. If the user provides a PR, commit, branch, issue, or file path:

- Read the relevant code changes, PR description, or commit messages
- Understand what the feature actually does at a technical level
- Identify the key insight, what makes this interesting or useful
- Look for benchmark data, test results, or before/after comparisons in the codebase

If the user only provides a brief description, ask clarifying questions to fill gaps in understanding. A good tweet requires genuinely understanding the feature. Surface-level descriptions produce surface-level tweets.

### Step 2: Classify the Feature Type

Determine which category the feature falls into:

| Type | Signal |
|---|---|
| **New API** | New function, class, or module being introduced |
| **Performance** | Speed, memory, or size improvement with measurable data |
| **CLI feature** | New command, flag, or workflow |
| **Compatibility** | Standards support, new format, ecosystem integration |
| **Bundled feature** | Multiple things combined into one simple experience |

### Step 3: Gather Input Details

Ask the user for (if not already provided):
- Product name (e.g., "Rolldown")
- Feature description, what it does
- Numbers/benchmarks if performance-related
- Contributors to credit (optional)
- Upstream projects to credit (optional)
- Known limitations or future plans (optional)

### Step 4: Draft the Main Tweet

**Opening:** Always use "In the next version of [Product]"

**Body** (pick the format matching the feature type):

| Feature type | Body format |
|---|---|
| New API | Function signature in backticks + one-sentence plain-English description |
| Performance | Short description of what area improved + the key number. Details go in replies |
| CLI feature | "You can:" + 2-3 escalating CLI examples in backticks |
| Compatibility | Simple statement: "[Product] gets [X] support" |
| Bundled feature | Description + punchy tagline ("One file, zero dependencies.") |

**Rules:**
- Plain English, minimal jargon
- If there is a number, include it -- "2x faster", "reduce objects by 10%"
- For performance tweets, explain what improved in terms any web dev would understand. Avoid implementation details like type names, data structures, or internal APIs.
- Use "up to X%" instead of ranges like "3-9%". Lead with the peak number.
- Don't mention dependency version bumps. Frame improvements as your own work.
- Keep it scannable. Use short paragraphs (1-2 sentences) with line breaks between them. A dense block of text is unreadable in tweet form. Put the key number or punchline on its own line.
- For performance tweets, lead with the number/result in the main tweet. Move detailed explanation of what changed into an optional reply.
- Keep under 280 characters when possible (exclude image placeholders)
- End with either a punchy tagline, inline benchmark, or note that an image is attached

### Step 5: Draft Thread Replies (Optional)

Thread replies are optional. Only add a reply if it provides genuinely useful context that doesn't fit in the main tweet. A standalone tweet is often better than a forced thread.

If adding replies, each should provide a different useful angle. Pick what fits:
- Practical impact or use cases
- Context on how it works or why it matters
- Proof (benchmarks, test results, before/after data)
- Credit to contributors or upstream projects
- Roadmap tease or scoping ("This was unrelated to X")

Replies can be longer and more conversational than the main tweet. They're where you explain the "why" and "how" in a natural, human tone. Don't compress them into robotic bullet points.

**Rules for replies:**
- Each reply should stand on its own, a reader might see it without the main tweet
- 3 replies max, never more
- Credit contributors with @mentions, credit upstream projects by name

### Step 6: Suggest Visual Proof

For each tweet/reply that would benefit from an image, add a bracketed suggestion:

| Scenario | Suggested visual |
|---|---|
| New API | Polished code screenshot with syntax highlighting and comments explaining usage |
| Performance claim | Benchmark table or terminal output with before/after/delta |
| Feature works | Terminal showing command + output |
| Test rigor | Wall of green checkmarks (pass/fail count) |
| Comparison | A/B bar charts (red=old, green=new) |
| CLI feature | Video demo or cheat sheet with usage variations |

Principle: the image should be self-contained proof. Someone seeing only the image should understand the claim.

### Step 7: Verify Against Anti-Patterns

Check the draft against these, if any match, revise:

- [ ] No "we're excited to announce..." preamble
- [ ] No "check out our blog post for more", the tweet IS the content
- [ ] No vague claims without data, every performance claim has numbers
- [ ] No superlatives ("blazingly fast", "revolutionary"), the numbers speak
- [ ] No engagement bait ("what do you think?", "RT if you agree")
- [ ] No thread longer than 3 replies
- [ ] No overselling, use understated language ("very slightly faster", "a little")
- [ ] Numbers are specific and reproducible (test scenario described, hardware noted if relevant)
- [ ] No em dashes. Use commas, periods, or conjunctions instead.
- [ ] No "no X, no Y, just Z" constructions (e.g., "No config changes, no API changes. Just faster.")
- [ ] Don't start sentences with bare past participles ("Optimized...", "Reduced...", "Improved..."). Use "We optimized..." or rephrase.
- [ ] No awkward specificity ("all 8 benchmarks"). Use natural phrasing ("across our benchmarks").
- [ ] Don't mention internal dependency names/versions. Frame as your own work.
- [ ] Be genuine. If the draft reads like an ad or press release, rewrite it.
- [ ] No walls of text. Use short paragraphs (1-2 sentences) with line breaks. Put the key number on its own line.

## Voice Guide

-> See [voice-guide](reference/voice-guide.md) for tone rules and examples

## Examples

-> See [examples](reference/examples.md) for 13 full tweet threads to reference

## Output Format

Present the final output as:

```
**Main tweet:**

[tweet text]

**Visual:** [describe what image/video to create, be specific about content, layout, and what to highlight]
```

Replies are optional. Only include them if they add genuinely useful context. If including replies, add them after the main tweet:

```
---

**Reply 1:**

[reply text]

**Visual:** [describe what image/video to create, or "None" if text-only reply]
```

### Visual Description Rules

Every visual suggestion must be actionable. Describe it so the user can go create it:

- **What to capture:** terminal output, code in editor, benchmark run, etc.
- **What to highlight:** which numbers to emphasize, what to annotate (red underlines, "winner" labels, Before/After labels)
- **Layout:** single screenshot, side-by-side comparison, table format, etc.
- **Style:** plain terminal screenshot vs polished code screenshot (gradient background, syntax highlighting)
- **Format:** image (screenshot) vs video (for interactive/workflow demos)

Example visual descriptions:
- "Screenshot of terminal running `rolldown build` showing output. Highlight the bundle size and time in the output."
- "Side-by-side polished code screenshot: left shows the config input, right shows the optimized output. Use gradient background with syntax highlighting."
- "Before/after benchmark table comparing Rolldown vs esbuild vs webpack. Columns: Bundler, Time, Bundle Size. Bold the Rolldown row."
- "Short video demo: run `rolldown --watch`, edit a file, show the rebuild time in terminal."
