---
name: marketing-strategy
description: Build a custom marketing strategy through an interactive interview. Develops business positioning, audience targeting, channel selection, and customer journey—then exports as a reusable JSON profile.
allowed-tools: Read Write Edit AskUserQuestion
---

# Marketing Strategy Builder

A world-class marketing strategist interview that creates a comprehensive marketing strategy for your business through step-by-step discovery.

## How This Skill Works

This skill conducts an interactive interview to understand your business deeply, then synthesizes everything into a structured marketing strategy profile in JSON format.

**Process:**
1. Ask one question at a time
2. Wait for your input before moving to the next step
3. Analyze each answer deeply and refine the next question accordingly
4. At the end, synthesize everything into a clear JSON profile

## Begin the Strategy Session

Say:

> "Let's build your custom marketing strategy. I'll ask you a series of questions to understand your business, target audience, goals, and messaging. Ready?"

Then proceed through the phases below.

---

## Phase 1: Business Foundation

Ask these in sequence, one at a time:

1. **Business Description** - What's your business or product? Describe it in one paragraph.
2. **Ideal Customers** - Who are your ideal customers? (Be specific—age, interests, job titles, problems)
3. **Unique Value Proposition** - What's your unique value proposition? (What makes your offer different or better?)
4. **Business Goals** - What are your primary business goals in the next 3–6 months?

---

## Phase 2: Positioning & Messaging

Ask these in sequence, one at a time:

1. **Pain Points/Desires** - What pain points or desires does your product solve?
2. **Current Solutions** - How does your audience currently solve this problem (if at all)?
3. **Emotional Response** - What emotions do you want to evoke in your audience?
4. **Brand Values** - What are 3-5 brand values or personality traits you want your marketing to express?

---

## Phase 3: Channels & Content

Ask these in sequence, one at a time:

1. **Audience Platforms** - Which platforms does your audience spend time on? (e.g., Twitter, LinkedIn, TikTok, email, etc.)
2. **Current Channels** - What marketing channels are you currently using (if any)?
3. **Resonant Content** - What kind of content resonates most with your audience? (e.g., value, personal stories, memes, video, etc.)
4. **Creator Comfort** - What type of content are you most comfortable creating?

---

## Phase 4: Strategy Design

Ask these in sequence, one at a time:

1. **Customer Journey** - What is your customer journey from awareness to purchase? (e.g., social post -> email list -> webinar -> product)
2. **Lead Capture** - What is your lead capture strategy? (e.g., free lead magnet, quiz, waitlist, etc.)
3. **Offers & Pricing** - What offer(s) do you want to promote and how will you price them?
4. **Upcoming Campaigns** - Do you have any campaigns, launches, or events planned soon?

---

## Final Step: Export

Once all questions are answered, say:

> "I'm now generating your marketing strategy profile as a JSON file you can reuse or feed into future prompts."

Then output the JSON in this format:

```json
{
  "business": {
    "description": "...",
    "goals": "..."
  },
  "audience": {
    "persona": "...",
    "pain_points": "...",
    "desires": "..."
  },
  "positioning": {
    "unique_value": "...",
    "emotions": "...",
    "brand_values": ["..."]
  },
  "channels": {
    "current": ["..."],
    "audience_prefers": ["..."],
    "content_types": ["..."],
    "creator_preferences": ["..."]
  },
  "strategy": {
    "customer_journey": "...",
    "lead_capture": "...",
    "offers": ["..."],
    "pricing": "...",
    "upcoming_campaigns": ["..."]
  }
}
```

Then end by saying:

> "This JSON profile can be used to train future prompts, align marketing decisions, or hand off to a team. Would you like to do a deep dive into any section next?"

---

## Quick Reference

For users who want to provide all information upfront instead of the interview:

| Section | Key Questions |
|---------|---------------|
| Business | Description, Goals (3-6 months) |
| Audience | Persona, Pain points, Desires |
| Positioning | Unique value, Emotions, Brand values |
| Channels | Current, Audience prefers, Content types, Creator comfort |
| Strategy | Customer journey, Lead capture, Offers, Pricing, Campaigns |

Collect all answers and generate the JSON profile directly.
