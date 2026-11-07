---
name: viral-carousel
description: >
  Finds the carousels that actually went viral in your niche, fetches every slide, breaks down why each
  one worked, and builds your own carousel on that proven structure in your words and your design.
  Use when the user says "find viral carousels", "what carousels are working in my niche",
  "make a carousel like this one", "copy the structure of this carousel", or before posting any carousel.
user-invokable: true
argument-hint: "[your niche, a few @handles, or carousel links]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Viral Carousel - find the winners, then build yours on their structure

Making a carousel with Claude is the easy part.
Knowing which carousel to make is the hard part.
This skill does the hard part first: it finds what your niche is already saving, then builds yours on that shape.

## When to use
Before you post any carousel.
Also when a carousel in your niche blew up and you want yours built the same way.

## What you'll need
Your niche, 5-10 accounts you compete with (or carousel links), and your topic.
For live numbers: the Instagram connector (Composio, or Ootto at ootto.ai) so Claude can read posts and counts.

## Instructions

1. **Find.** Pull the last 30-50 posts of each account (Instagram Graph API `business_discovery`, the Composio
   Instagram tools, or the links the user pastes). Keep only carousels.
2. **Rank.** For each account, compute its median likes + comments.
   Mark a carousel **viral** when it beats its own account median by 3x or more.
   A small account's 3x beats a big account's average, because it proves the post, not the follower count.
3. **Fetch.** For the top 3-5 viral carousels, download every slide and the caption.
4. **Break down.** Run this on each one:

```
You are my carousel analyst. Here are the slides and caption of a carousel that went viral: [SLIDES + CAPTION].

For every slide give me: its job (hook / payoff / proof / step / summary / ask), the words on it, and why it is there.
Then tell me:
- Slide 1: what makes it stop the scroll (claim, number, contrast, question).
- Where the proof sits, and what kind it is (a result, a screenshot, a number).
- The slide people save, and why they would.
- Where the ask is, and what it asks for.
- The slide count and the reading rhythm (one idea per slide or not).
Finish with the STRUCTURE as a numbered list of slide jobs, with no topic words in it.
```

5. **Build.** Hand the structure to [carousel-builder](../carousel-builder/SKILL.md):

```
Build my carousel on this proven structure: [STRUCTURE].
My topic: [TOPIC]. My audience: [WHO]. My ask: [save / follow / comment WORD].
Keep every slide's job. Write every word fresh in my voice. Use my colours, fonts and handle.
```

6. **Render and post.** Render the slides in your own design (HTML to PNG, or your design tool), then post.
   With Ootto connected, Claude designs the slides and posts them to your Instagram for you.

## Output
- The viral carousels it found, each with its multiple over its account median.
- A slide-by-slide breakdown of each one.
- The reusable structure.
- Your carousel, written on that structure, ready to render.

**Honesty:** Copy the structure, never the slides.
Every word, image and design on your carousel must be yours, and Instagram's originality checks bury reposted slides.
Numbers come from the API or the user, never from a guess.

**Next:** [carousel-builder](../carousel-builder/SKILL.md) → [caption-and-hashtags](../caption-and-hashtags/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** - the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
