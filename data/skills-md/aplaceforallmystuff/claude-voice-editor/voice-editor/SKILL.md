---
name: voice-editor
description: Edit AI-generated or draft content to match a voice profile. Use when transforming generic AI output into authentic voice-matched content, or when editing drafts to sound more like you.
use_when: User wants to edit AI output to match their voice, transform generic content into authentic writing, apply voice profile to a draft, or make content sound more like them.
---

<objective>
Transform generic or AI-generated content into voice-matched writing using a VOICE.md profile.

Voice doesn't live in first drafts - it lives in editing choices. This skill guides the 6-pass editing process that turns AI's generic output into something distinctively yours.
</objective>

<quick_start>
Provide:
1. **Content to edit** (paste or file path)
2. **VOICE.md location** (default: `~/.claude/voice/VOICE.md` or project's `.claude/VOICE.md`)

The skill will:
1. Run slop detection on the content
2. Identify voice mismatches against your profile
3. Perform multi-pass editing (Structure → Voice → Polish)
4. Output edited content with change annotations
5. Suggest VOICE.md updates based on patterns found
</quick_start>

<the_editing_reality>
**The 30-40% Rule:**

Even with a perfect style guide, expect to edit 30-40% of AI output to make it distinctively yours. This isn't a problem—it's the feature.

30-40% editing effort is dramatically less than 100% writing-from-scratch effort, while producing work that sounds more like you than unguided AI ever could.

**If you're editing more than 50%:** Your style guide needs refinement, or your prompts need work.

**If you're editing less than 20%:** You might be accepting too much generic content.
</the_editing_reality>

<editing_workflow>
<pass number="1" name="Structure Check">
**Focus:** Does the organization serve the content?

**Opening Mechanics (from craft-rules):**
- [ ] Does opening create a SPECIFIC question? Not vague mystery - readers need enough context to form a particular question they want answered
- [ ] Does first paragraph contain change or threat of change? Brains notice disruption of status quo
- [ ] Is first paragraph under 50 words / 3 sentences?
- [ ] First line hits 3+ of: question, character, setting, tone, movement?

**Questions to ask:**
- Does the opening hook or just clear throat?
- Is there a clear progression of ideas?
- Does each section earn its place?
- Is anything redundant or missing?
- Does the conclusion land or just stop?

**Scene/Section Structure:**
- Does each section follow Goal → Conflict → Outcome?
- Are transitions connected by "because" not "and then"?
- Are characters/subjects in motion during slow passages?

**Actions:**
- Cut throat-clearing openings ("In this article, we'll explore...")
- Reorder sections for better flow
- Merge redundant sections
- Add missing transitions
- Strengthen weak conclusions
- **Add change to opening** if missing - start with what changed, not background
- **Make question specific** - "Why is the other side of the bed cold?" not "Something is happening"
</pass>

<pass number="2" name="Voice Alignment">
**Focus:** Does this sound like the voice profile?

**Check against VOICE.md:**
- Sentence length patterns (matching variance?)
- Vocabulary fingerprint (right formality level?)
- Tone markers (humor, directness, reader relationship?)
- Structural habits (lists vs prose, formatting?)
- Opinion expression (appropriate confidence level?)

**Actions:**
- Replace formal language with conversational equivalents
- Vary sentence lengths to match profile
- Add characteristic phrases from the voice profile
- Adjust opinion strength to match profile
- Fix paragraph rhythm
</pass>

<pass number="3" name="Slop Removal">
**Focus:** Eliminate AI tells and forbidden phrases

**Scan for:**
- Tier 1 phrases (remove immediately)
- Tier 2 patterns (check context)
- Tier 3 clusters (break up if grouped)
- Structural tells (uniformity, over-balance)
- **Staccato fragment spam** (3+ consecutive short declarative sentences)
- **Comparator sentences** ("This isn't X. It's Y." patterns)

**Actions:**
- Delete or replace all Tier 1 phrases
- Evaluate Tier 2 in context, remove if generic
- Redistribute Tier 3 to avoid clustering
- Vary sentence lengths if too uniform
- Rebalance sections if all equal weight
- **Combine staccato fragments** into flowing prose with commas, em-dashes, or conjunctions
- **Rewrite comparators directly** — just say what something IS, don't waste words on what it isn't
</pass>

<pass number="4" name="Specificity Injection">
**Focus:** Replace generic with specific

**What to cut:**
- Generic superlatives without claims ("game-changing," "revolutionary")
- Hedging that adds no value ("it might be argued that")
- Corporate platitudes ("leverage synergies")
- Anything that sounds like a press release

**What to add:**
- Your actual opinion (not the diplomatic version)
- Specific examples from your experience
- Honest acknowledgment of limitations
- Your characteristic quirks and phrases
- Conversational asides that show how you think
</pass>

<pass number="5" name="Rhythm and Flow">
**Focus:** Does it read naturally aloud?

**The read-aloud test:**
- Read the piece aloud (or use text-to-speech)
- Mark every place you stumble
- Note where you'd naturally pause vs. where punctuation forces pauses
- Identify sentences that feel too long or choppy

**Sentence Craft Checks (from craft-rules):**
- [ ] Active verbs predominate? Search for "was [verb]ed" passive patterns
- [ ] Word order follows action sequence? Actor → Action → Recipient (filmic)
- [ ] Objects have ~3 specific qualities, not abstract adjectives?
- [ ] Sentence length varies deliberately? Short punch, then longer exploration
- [ ] No clichéd metaphors? (Fresh comparisons trigger more brain activity)

**Hemingway Principles:**
- Emphasize nouns
- Choose active verbs
- Adjectives: few but apt
- Short sentences by default
- Long sentences ONLY for: speeding action, describing flow, making short sentences pop

**Actions:**
- Break sentences where you ran out of breath
- Combine choppy sentences that flow together
- Add rhythm variation (short punch, longer exploration)
- Fix awkward transitions
- Smooth unnatural phrasing
- **Convert passive to active** - "The ball was thrown by John" → "John threw the ball"
- **Reorder for transitive flow** - "Jane gave a kitten to her Dad" beats "Jane gave her Dad a kitten"
- **Replace abstract with specific** - "terrible" → details that create terror
</pass>

<pass number="6" name="Final Authenticity Check">
**Focus:** The ultimate test

**Ask yourself:**
"Would someone who knows me recognize this as mine before seeing my name?"

**If no:**
- What's missing? Add it.
- What's wrong? Fix it.
- What's generic? Make it specific.

**If yes:**
- You're done. Ship it.
</pass>
</editing_workflow>

<what_to_cut>
**Always remove:**
- Generic superlatives without specific claims
- Hedging language that softens everything
- Unnecessary qualification that adds no value
- Corporate platitudes that mean nothing
- Anything that sounds like a committee wrote it
- Motivational poster language
- Flattery sandwiches ("While X has merit, Y offers...")

**Examples:**
- ❌ "This groundbreaking approach revolutionizes..."
- ✅ "This cuts processing time from 4 hours to 15 minutes"

- ❌ "It's worth noting that in many cases..."
- ✅ [Just make the point directly]

- ❌ "Unlock your potential with powerful insights"
- ✅ "Stop wasting time on tasks AI handles in seconds"
</what_to_cut>

<what_to_add>
**Voice elements AI misses:**

- **Your actual opinion** - Not the diplomatic version AI produces
- **Specific examples** - From your experience, not generic training data
- **Honest limitations** - Not fake confidence in uncertain claims
- **Characteristic quirks** - Phrases your style guide might have missed
- **Conversational asides** - How you actually think through problems
- **Rough edges** - The imperfections that make writing human

**Examples:**
- Add: "Three hours later (no hyperbole), I finally got it working"
- Add: "Here's where I screwed up the first time..."
- Add: "Look, I'm not sure this is right, but..."
- Add: [Your characteristic phrases from VOICE.md]
</what_to_add>

<output_format>
**For edited content, provide:**

```markdown
## Edited Content

[Full edited content here]

---

## Edit Summary

**Passes completed:** 6/6
**Estimated edit percentage:** [X]%
**Voice match confidence:** [Low/Medium/High]

### Major Changes
1. [Most significant change and why]
2. [Second major change]
3. [Third major change]

### Slop Removed
- [List of AI patterns found and removed]

### Voice Elements Added
- [List of voice-specific additions]

### Remaining Concerns
- [Any areas that still feel off]
- [Suggestions for further refinement]

### VOICE.md Update Suggestions
- [Patterns discovered that should be added to voice profile]
- [Phrases that worked well - consider adding to "use freely" list]
```
</output_format>

<editing_modes>
<mode name="light">
**Use when:** Content is close to voice, just needs polish

**Passes:** 3, 5, 6 (Slop Removal, Rhythm, Final Check)
**Expected edit:** 10-20%
**Time:** 5-10 minutes per 500 words
</mode>

<mode name="standard">
**Use when:** Typical AI output with style guide

**Passes:** All 6
**Expected edit:** 30-40%
**Time:** 15-20 minutes per 500 words
</mode>

<mode name="heavy">
**Use when:** Generic AI output, no style guide used in generation

**Passes:** All 6, possibly multiple iterations
**Expected edit:** 50-70%
**Time:** 25-35 minutes per 500 words

**Consider:** Might be faster to rewrite with better prompts
</mode>

<mode name="rescue">
**Use when:** Content is fundamentally off but has good bones

**Approach:**
1. Extract the core ideas/structure only
2. Rewrite from scratch using voice profile
3. Incorporate any specific facts/examples from original
4. Run standard editing passes on new draft

**This is not editing—it's salvage.**
</mode>
</editing_modes>

<common_problems>
<problem name="too_formal">
**Symptom:** Reads like a corporate memo
**Cause:** AI defaulting to academic/business training data
**Fix:**
- Replace "individuals" → "people"
- Replace "utilize" → "use"
- Replace "implement" → "do/start"
- Add contractions
- Shorten sentences
- Add conversational asides
</problem>

<problem name="too_uniform">
**Symptom:** Every sentence same length, monotonous rhythm
**Cause:** AI optimizing for "clarity" = brevity
**Fix:**
- Vary deliberately: 5-word punch, then 25-word exploration
- Combine related short sentences
- Break long sentences at natural pauses
- Add one-sentence paragraphs for emphasis
</problem>

<problem name="too_hedged">
**Symptom:** Everything qualified, no strong positions
**Cause:** AI avoiding incorrect claims
**Fix:**
- Delete: "it might be argued," "generally speaking," "in some cases"
- Make direct claims you can support
- Replace "might" with "will" where confident
- Add "in my experience" instead of vague hedging
</problem>

<problem name="too_balanced">
**Symptom:** Every section same length, all points equal weight
**Cause:** AI doesn't have opinions/priorities
**Fix:**
- Expand important points, shrink minor ones
- Cut sections that don't earn their space
- Lead with strongest material
- Let structure reflect actual priorities
</problem>

<problem name="voice_drift">
**Symptom:** Starts strong, becomes generic by end
**Cause:** AI loses context over long pieces
**Fix:**
- Edit in 500-word chunks
- Re-inject voice markers every few paragraphs
- Add "personality refreshers" (asides, opinions, humor)
- Check last third especially carefully
</problem>
</common_problems>

<integration_with_other_skills>
**Before voice-editor:**
- Run `slop-detector` for initial assessment
- Ensure `voice-analyzer` has created VOICE.md
- Run `craft-rules` for structural quality audit

**After voice-editor:**
- Run `slop-detector` again to verify cleanup
- Update VOICE.md with new patterns discovered

**Full Workflow:**
```
[Draft] → slop-detector → craft-rules → voice-editor → slop-detector → [Final]
               ↓               ↓              ↓               ↓
         AI tells?      Structure ok?   Voice match      Verify clean
```

**What each skill checks:**
| Skill | Focus | Example Issue |
|-------|-------|---------------|
| slop-detector | AI patterns | "delve," "landscape," "game-changer" |
| craft-rules | Writing mechanics | Weak hook, passive voice, abstract adjectives |
| voice-editor | Personal voice | Too formal, missing characteristic phrases |

**Quick workflow (already clean content):**
```
[Draft] → voice-editor (light mode) → [Final]
```

**Heavy workflow (generic AI output):**
```
[Draft] → slop-detector → craft-rules → voice-editor (heavy/rescue) → slop-detector → [Final]
```
</integration_with_other_skills>

<success_criteria>
Editing is complete when:
- [ ] All 6 passes have been applied (or appropriate subset for mode)
- [ ] No Tier 1 slop phrases remain
- [ ] Sentence length varies naturally
- [ ] Content matches VOICE.md characteristics
- [ ] Read-aloud test passes (no stumbling)
- [ ] The authenticity question is answered "yes"
- [ ] Edit summary documents all changes
- [ ] VOICE.md update suggestions provided if patterns discovered

**The ultimate test:** Would someone who knows the author recognize this as theirs before seeing the name?
</success_criteria>

<core_principle>
The style guide gives AI direction—it helps produce output closer to your voice than generic defaults. Your editing gives the work your actual voice—the quirks, opinions, personality, and rough edges that make it distinctively yours.

This is why "zero effort" AI fails. The promise of finished content without touching it misunderstands what makes writing valuable. Effort isn't the enemy. Wasted effort is.

You're redirecting effort from blank-page generation to voice-preservation editing. That redirection is the entire point.
</core_principle>
