---
name: hackathon-attendee
model: sonnet
description: Best practices, tips, and tricks for hackathon participants. Use when someone asks how to prepare for, compete in, or make the most of a hackathon as an attendee — covering preparation, ideation, building, presenting, and networking.
activationKeywords:
  - "attending a hackathon"
  - "hackathon tips"
  - "how to win a hackathon"
  - "first hackathon"
  - "hackathon preparation"
  - "hackathon project ideas"
  - "hackathon demo tips"
  - "hackathon attendee"
---

# Hackathon Attendee — Tips & Best Practices

Everything you need to know to prepare for, compete in, and get the most out of a hackathon.

## Reference Files

- `references/building-and-strategy.md` — Technical strategy, MVP approach, tech stack choices, time management
- `references/presenting-and-networking.md` — Demo tips, what judges look for, networking, and post-hackathon follow-up

## When to Activate

- User is preparing for an upcoming hackathon as a participant
- User asks for hackathon tips, strategies, or advice
- User wants to know what to expect at their first hackathon
- User asks how to win or place well at a hackathon
- User asks about hackathon project ideas or demo tips

## When NOT to Activate

- User is organizing a hackathon (use `hackathon-organizer` instead)
- User is managing a hackathon on the Oatmeal platform (use `hackathon-cli` or `hackathon-api`)
- User is writing hackathon platform code

## Before the Hackathon

### What to Bring

- **Laptop + charger** (obvious, but people forget chargers)
- **Phone charger / power bank**
- **Headphones** — essential for focusing in noisy environments
- **Extension cord or power strip** — makes you popular at your table
- **Hoodie or blanket** — venues get cold, especially overnight
- **Toiletries** — toothbrush, deodorant, face wipes if it's overnight
- **Snacks** — your own stash for when you need fuel between meals
- **Water bottle** — stay hydrated
- **Notebook + pen** — for brainstorming and sketching before touching code
- **Business cards or a QR code** to your portfolio/GitHub/LinkedIn

### Pre-Event Preparation

1. **Set up your dev environment before you arrive** — install languages, frameworks, IDEs, and tools. Nothing burns hackathon time like environment setup
2. **Prepare starter templates** — have boilerplate repos for your favorite stacks (Next.js, Flask, React Native, etc.). This is not cheating — it's smart
3. **Explore sponsor APIs in advance** — read docs, get API keys, run test calls. Judges for sponsor prizes love seeing deep integration, not just a hello-world call
4. **Research past winning projects** — look at Devpost galleries for the hackathon or similar ones. Understand what level of polish wins
5. **Have 2-3 project ideas ready** — don't arrive blank. Have ideas you can pitch to potential teammates. But stay flexible — the best idea might come from someone you meet

### Finding a Team

- **Go solo if you can do full-stack** — small teams (2-3) with complementary skills often beat large teams
- **Ideal team composition:** 1 frontend dev, 1 backend dev, 1 designer/presenter. A dedicated presenter is an underrated advantage
- **If you don't have a team:** attend the team formation session, pitch your idea in 30 seconds, and look for complementary skills rather than identical ones
- **Set expectations early:** agree on the idea within the first hour, assign roles, decide on communication tools

## During the Hackathon

### The First Hour Is Critical

1. **Finalize your idea in 30 minutes** — don't spend 3 hours debating. Pick the idea that excites the team most and is feasible
2. **Define your MVP in 15 minutes** — what is the one core feature you must demo? Everything else is stretch goals
3. **Divide work immediately** — who does frontend, backend, design, and presentation? Parallel work from minute one

### Time Management

For a 24-hour hackathon:

| Phase | Hours | What to Do |
|-------|-------|------------|
| **Plan** | 0-1 | Idea, MVP scope, task division |
| **Build core** | 1-8 | Get the main feature working end-to-end |
| **Integrate** | 8-14 | Connect frontend to backend, add sponsor APIs |
| **Polish** | 14-20 | UI cleanup, demo flow, bug fixes |
| **Prepare demo** | 20-22 | Write script, practice presentation, screenshots |
| **Submit** | 22-24 | Submit early, record demo video as backup |

**Golden rule: Have a working demo by the halfway point.** If your core feature doesn't work at hour 12, simplify it.

### Technical Strategy

- **Start with the demo** — build what you'll show first, then fill in the rest. A polished demo of 1 feature beats a broken demo of 5
- **Use what you know** — hackathons are not the time to learn a new framework. Use your strongest tools
- **Deploy early** — get it on a public URL (Vercel, Railway, Netlify) in the first few hours. Judges trust deployed projects more
- **Use AI tools aggressively** — Claude, Copilot, Cursor. Everyone is using them. Speed is everything
- **Git from the start** — commit frequently. You don't want to lose work to a laptop crash at hour 20
- **Don't build auth** — use a mock user or hardcode credentials. Auth adds zero demo value
- **Fake it where it makes sense** — hardcoded data, mock API responses, pre-seeded databases. If it looks real in the demo, it's real enough
- **API integrations should be visible** — if you're going for a sponsor prize, make the API integration prominent and visible in the demo

### What NOT to Do

- **Don't build infrastructure** — no Kubernetes, no custom CI/CD, no microservices. It's a hackathon
- **Don't write tests** — blasphemy in production, pragmatism at a hackathon
- **Don't redesign the landing page 4 times** — pick a design and move on
- **Don't stay up all night if it hurts your performance** — a rested team with 16 hours of focused work beats a zombie team with 24 hours of diminishing returns
- **Don't argue about technology choices for more than 10 minutes** — whoever has the most experience decides

## What Judges Actually Look For

### The Scoring Criteria (Usually)

1. **Does it work?** — A working demo is worth more than a beautiful pitch deck
2. **Is the problem real?** — Judges want to see you identified a genuine pain point
3. **Is the solution novel?** — Not "another todo app" but a fresh angle on a real problem
4. **Is it technically impressive?** — Complex integrations, real-time features, AI/ML pipelines score higher than CRUD apps
5. **Is it polished?** — Good UI, consistent design, smooth demo flow

### What Separates Winners from the Pack

- **The story** — winners tell a compelling story: "We noticed X problem, we built Y to solve it, here's Z impact"
- **The live demo** — working software shown live, not screenshots
- **The "wow" moment** — one feature that makes judges lean forward. Build toward this moment in your demo
- **Technical depth** — mentioning the architecture, challenges overcome, and tradeoffs made shows maturity
- **Team energy** — enthusiasm is infectious. Judges remember teams that were genuinely excited

## Presenting Your Project

### Demo Structure (3 minutes)

```
0:00 - 0:30  The problem (make it relatable)
0:30 - 0:45  Our solution (one sentence)
0:45 - 2:15  Live demo (show, don't tell)
2:15 - 2:45  Technical highlights (architecture, challenges)
2:45 - 3:00  What's next / call to action
```

### Presentation Tips

- **Practice your demo 3+ times** before presenting
- **Have a backup** — screen recording of the demo in case live demo fails
- **Start with the user, not the tech** — "Imagine you're a nurse doing X..." beats "We built a React app with..."
- **One person presents** — don't pass the mic around. Have your best speaker present, others answer technical questions
- **Make it visual** — show the app full-screen. No IDE, no terminal, no code (unless it's a developer tool)
- **End strong** — your last slide or statement should be memorable

### If Things Go Wrong

- **Demo crashes:** switch to the recording. Say "Let me show you the recording we prepared." Judges understand — they respect the preparation
- **Feature doesn't work:** skip it. Show what does work. Never debug live
- **Timer runs out:** you should have shown the wow moment by minute 2. If you get cut off, the important parts were already shown

## Networking

- **Talk to sponsors** — they're there to recruit. Ask about their tech stack, open roles, and what they look for in candidates
- **Talk to judges** — after judging, approach them for feedback. They've seen dozens of projects and can give you perspective
- **Connect with teammates afterward** — exchange LinkedIn/GitHub. Hackathon teammates become lifelong collaborators
- **Attend workshops** — even if they're on tech you know, you'll meet the sponsor engineers running them
- **Help other teams** — if you solve a bug for another team, you've made a friend and demonstrated expertise

## Post-Hackathon

1. **Push your code to GitHub** and write a proper README within 48 hours while it's fresh
2. **Connect with everyone on LinkedIn** — teammates, judges, sponsors, organizers, people you met
3. **Share your project** — post on X/Twitter, LinkedIn, Devpost. Tag the hackathon and sponsors
4. **Keep building** — many successful startups started as hackathon projects. If you're excited about it, keep going
5. **Reflect** — what worked? What would you do differently? Write it down for next time

For detailed building strategies and presentation techniques, see the reference files.
