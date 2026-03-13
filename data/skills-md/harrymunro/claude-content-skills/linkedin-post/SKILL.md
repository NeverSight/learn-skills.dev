---
name: linkedin-post
description: Create LinkedIn posts using your brand voice. Use when asked to write a LinkedIn post, social media content, or professional social content. Triggers on "linkedin", "post", "social media".
---

# LinkedIn Post Creator

Create engaging LinkedIn posts in your authentic brand voice.

## Before Writing

1. **Run the rhetoric selector** to get your rhetorical devices:
   ```bash
   python shared/rhetoric_selector.py --type linkedin_technical
   # or --type linkedin_provocative
   # or --type linkedin_personal
   ```

2. **Review the voice guide**: See [VOICE_GUIDE.md](../../config/VOICE_GUIDE.md)

3. **Check content pillars**: See [CONTENT_PILLARS.md](../../config/CONTENT_PILLARS.md)

## Post Structure

### The Hook (First 2-3 lines)
- This is what shows before "...see more"
- Must stop the scroll
- Use a provocative statement, surprising fact, or bold claim
- Rhetorical devices work brilliantly here (antithesis, hyperbaton)

### The Body
- Short paragraphs (1-3 sentences each)
- Use line breaks liberally - walls of text don't work
- Include specifics: numbers, real examples, code snippets if relevant
- Build your argument or tell your story
- This is where anaphora, tricolon, and anadiplosis shine

### The Closing
- End with a question, takeaway, or soft CTA
- Questions drive comments
- Epistrophe and chiasmus work well for memorable endings
- ONE CTA maximum (if any)

## Formatting Rules

- **Optimal length**: 1,000-1,300 characters
- **Maximum**: 3,000 characters (but shorter is usually better)
- **Line breaks**: After every 1-2 sentences
- **Emojis**: Use sparingly if at all (max 1-2, and only if natural)
- **Hashtags**: 3-5 at the end, relevant to topic

## Templates by Content Type

See templates folder:
- [Technical Tip](templates/technical-tip.md)
- [Industry Take](templates/industry-take.md)
- [Personal Story](templates/personal-story.md)

## Voice Reminders

From your [VOICE_GUIDE.md](../../config/VOICE_GUIDE.md):
- Write in your authentic voice as defined in the guide
- Use the phrases and patterns you've identified
- Avoid the words and phrases on your "avoid" list
- Maintain the spelling conventions you've chosen

### Phrases that often work well
- "Here's the thing..."
- "Look," (to start a provocative point)
- "The uncomfortable truth is..."
- "Nobody talks about this, but..."
- "I was wrong about..."

### Generally avoid
- "Excited to announce..."
- "Game-changer" / "Revolutionary"
- "Thought leader"
- Corporate jargon

## Example Post Structures

### Technical (with tricolon and litotes)
```
[HOOK: What nobody tells you about X]

[Brief context - why this matters]

[The insight - short, punchy sentences]

[Example - real numbers, real code if relevant]

[Takeaway - what to do with this]

[Closing question to drive comments]

#YourHashtags #Here
```

### Provocative (with antithesis and anaphora)
```
[HOOK: Bold claim or contrarian statement]

[Context that sets up the contrast]

[Build your argument using repetition]
You don't need X. You don't need Y. You don't need Z.

[The uncomfortable truth]

[Your stance - what you believe]

[Invitation for discussion]

#YourHashtags #Here
```

## Quality Checklist

Before posting, verify:
- [ ] Hook stops the scroll (would YOU click "see more"?)
- [ ] Voice is authentically yours (check against your guide)
- [ ] At least one rhetorical device used naturally
- [ ] Specific examples or numbers included
- [ ] No corporate jargon
- [ ] Under 1,500 characters (ideally)
- [ ] CTA is soft and earned (if present)
- [ ] 3-5 relevant hashtags
