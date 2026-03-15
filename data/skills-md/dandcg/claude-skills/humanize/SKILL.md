---
name: humanize
description: Rewrite AI-generated text to sound natural and human. Use for humanizing text, making AI writing undetectable, rewriting to pass AI detectors. Trigger on phrases like "humanize", "make this sound human", "rewrite naturally", "humanize text", "sound more natural", "pass AI detection".
---

# Humanize Text

Rewrite AI-generated text to sound natural and pass AI detection tools while preserving meaning exactly.

## Prerequisites

- No setup required for Claude engine (default)
- For commercial API engine: run setup first

### Optional: Commercial API Setup

```bash
~/.claude/skills/humanize/scripts/setup.sh
```

## Usage

Humanize text by providing it inline, from a file, or from clipboard. Options are expressed in natural language.

### Input Methods

- **Inline:** "humanize this: [text]"
- **File:** "humanize the text in draft.md"
- **Clipboard:** "humanize my clipboard"

### Options

- **Tone:** neutral (default), casual, professional, academic
- **Aggressiveness:** light, moderate (default), heavy
- **Engine:** Claude (default) or "using undetectable" for commercial API
- **Output:** conversation (default) or "save to [filename]"

### Examples

- "humanize this: The implementation of machine learning algorithms has significantly transformed..."
- "humanize draft.md in a casual tone"
- "humanize essay.md with heavy rewriting"
- "humanize report.md using undetectable"
- "humanize draft.md and save to final.md"

## Claude Engine: Humanization Workflow

When humanizing text with the Claude engine (default), follow this exact 4-pass workflow. Execute all passes internally and return only the final result.

### Tone Presets

Apply the selected tone throughout all passes:

- **Neutral** (default): clean, natural prose. No slang, no stiffness.
- **Casual**: contractions everywhere, shorter sentences, conversational asides ("honestly", "look", "the thing is"), occasional sentence fragments.
- **Professional**: formal but not robotic. Varied but polished. Allow occasional first-person.
- **Academic**: discipline-appropriate vocabulary, longer sentences allowed but with varied structure. Cite-ready.

### Aggressiveness Levels

- **Light**: only fix obvious AI patterns (banned words, em dashes, uniform structure). Preserve original sentence structure where possible.
- **Moderate** (default): full 4-pass workflow as described below.
- **Heavy**: aggressive restructuring. Reorder paragraphs if it improves flow. Rewrite most sentences from scratch while preserving all meaning. Change voice, perspective shifts, add rhetorical questions.

### Pass 1: Structural Deconstruction (targets burstiness)

AI detectors measure "burstiness" - how much sentence length and complexity varies. AI text is uniform. Human text is jagged.

Do this:
- Break predictable paragraph patterns. Don't keep the same paragraph count if it hurts flow.
- Start mid-action or with a bold claim. Never open with a generic intro like "In today's world" or "When it comes to".
- Mix very short punchy sentences (3-7 words) with longer flowing clauses (20-30 words). Aim for high variance.
- Vary paragraph lengths. Some paragraphs should be a single sentence. Others 4-5 sentences.
- Occasionally use a sentence fragment for emphasis. On purpose.
- Break up any list-like structure into flowing prose unless the original explicitly needs to be a list.

### Pass 2: Diction & Voice (targets perplexity)

AI detectors measure "perplexity" - how predictable word choices are. AI picks the statistically most likely word. Humans are messier.

Do this:
- Replace generic adjectives ("effective", "significant", "comprehensive", "robust") with precise, domain-specific terms or concrete descriptions.
- Use subjective framing: "I've found that..." or "What works here is..." not "It has been observed that..." or "Research suggests..."
- Use conversational connectors: "Here's the thing", "So what does this actually mean?", "The short version:", "Put differently" instead of "Moreover", "Furthermore", "Additionally", "In addition".
- Use contractions naturally: "it's", "don't", "won't", "that's", "there's".
- Replace broad generalizations with specific examples or concrete scenarios.
- Occasionally address the reader directly: "you", "your", "notice how".
- Vary vocabulary - don't use the same adjective or transition twice in nearby paragraphs.

### Pass 3: Banned Patterns Purge

Scan the rewritten text and remove or replace ALL of the following. These are the most common AI-detection triggers:

**Banned words and phrases:**
delve, tapestry, leverage, utilize, realm, game-changer, unlock, embark, illuminate, unveil, pivotal, intricate, elucidate, hence, furthermore, moreover, however, harness, groundbreaking, cutting-edge, remarkable, navigate, landscape, testament, ever-evolving, shed light, dive deep, treasure trove, craft/crafting, imagine, skyrocket, revolutionize, disruptive, exciting, powerful, inquiries, remains to be seen, glimpse into, stark, certainly, probably, basically, it's important to note, it's worth mentioning, in today's world, in today's digital landscape, in today's era, in conclusion, in summary, in closing, this comprehensive guide, let's explore, not just X but also Y, when it comes to, at the end of the day, on the other hand, having said that, with that being said, needless to say, it goes without saying, as a matter of fact, the fact of the matter is, it should be noted

**Banned formatting patterns:**
- Em dashes (-) - replace with commas, periods, or semicolons
- Perfect parallel structure in consecutive sentences or paragraphs
- Consecutive paragraphs starting the same way
- Every paragraph being the same length
- Bullet points where prose would be more natural

### Pass 4: Self-Audit

Re-read the full output one final time:
- Flag and fix any remaining uniform sentence patterns (3+ consecutive sentences of similar length)
- Verify ALL facts, numbers, names, dates, and technical terms are preserved exactly from the original
- Verify no meaning was lost, added, or distorted
- Verify no statistics, examples, or credentials were invented
- If any illustrative examples were added, they must be clearly marked as hypothetical
- Check that technical terms were NOT swapped for synonyms
- Confirm the logical flow and argument structure matches the original

### Hard Constraints (NEVER violate)

1. All facts, numbers, names, dates survive unchanged
2. Technical terms must not be swapped for synonyms
3. Do not invent statistics, examples, or credentials
4. Logical flow and argument structure must be maintained
5. Any added illustrative examples must be labeled as hypothetical

## Commercial API Engine

When the user requests "using undetectable", call the API script:

```bash
~/.claude/skills/humanize/.venv/bin/python ~/.claude/skills/humanize/scripts/humanize-api.py --text "THE_TEXT_HERE"
```

For file input:
```bash
~/.claude/skills/humanize/.venv/bin/python ~/.claude/skills/humanize/scripts/humanize-api.py --file path/to/file.txt
```

The script returns humanized text to stdout. Present it to the user.
