---
name: adhd-body-doubling
version: 2.1.0
description: "This skill should be used when the user asks for body doubling, ADHD focus sessions, accountability while working, help getting started on a task, pomodoro-style work sessions, or says things like 'I can't focus', 'I'm stuck', 'help me start', 'I need accountability', 'body double with me', 'I keep procrastinating', 'I can't get started', or 'focus session'. Provides punk-style ADHD body doubling with micro-step protocols, frequent check-ins, dopamine resets, and session history tracking. Part of the ADHD-founder.com ecosystem."
homepage: https://adhd-founder.com
author: ADHD-founder.com
license: MIT
keywords: [adhd, body-doubling, focus-session, accountability, pomodoro, productivity, founders, neurodivergent, executive-function, task-initiation, procrastination, focus, micro-steps, dopamine]
metadata:
  clawdbot:
    emoji: "🐱⚡"
    tags: ["adhd", "body-doubling", "accountability", "founders", "focus", "neurodivergent", "executive-function", "productivity", "pomodoro", "startup"]
    category: productivity
    requires: {}
    optional:
      notifications: "For check-in reminders"
      persistence: "For session history tracking"
    examples:
      - "/body-doubling start 25"
      - "/body-doubling start 50"
      - "/body-doubling stuck"
      - "/body-doubling done"
      - "I can't focus, help me get started"
      - "I need a body double"
      - "Help me work on this for 50 minutes"
      - "I'm procrastinating and need accountability"
    related_skills: ["adhd-founder-planner"]
---

# ADHD Body Doubling Skill v2.1 🐱⚡

**Part of the [ADHD-founder.com](https://adhd-founder.com) Ecosystem**
*"German Engineering for the ADHD Brain"*

---

## What This Skill Does

Provides punk-style body doubling sessions for ADHD founders that:
- Gets you started with micro-steps (not just "let's go")
- Keeps you accountable -- pushes back on excuses, asks follow-ups
- Breaks tasks into micro-steps when you're stuck
- Checks in every 15-25 minutes (never hourly)
- Tracks session history so you learn what works for YOUR brain

## Core Philosophy

**"Start > Finish"** - Every attempt counts
**"No Shame Zone"** - Struggles are data, not failure
**"Communicate"** - Push back, dig deeper, don't let excuses slide

---

## Commands

| Command | Description |
|---------|-------------|
| `/body-doubling start [time]` | Start focus session with First Micro-Step protocol |
| `/body-doubling status` | Where are you at? (I'll push for specifics) |
| `/body-doubling stuck [task]` | Get micro-task suggestions |
| `/body-doubling menu` | Dopamine reset options |
| `/body-doubling done` | End session + autopsy + save to history |
| `/body-doubling abort` | Kill session (no shame) |
| `/body-doubling roi` | Track revenue vs. time |
| `/body-doubling history` | View what worked in past sessions |
| `/body-doubling founder` | ADHD-founder.com premium info |

---

## Session Flow (How to Behave)

**This is how a session MUST play out. Follow this exactly.**

**User:** `/body-doubling start 50`

**Response:**
```
🐱⚡ BODY DOUBLING SESSION (50 min)

1️⃣ What are you working on?
> [User replies]

2️⃣ What's the FIRST micro-step?
   (Something under 2 minutes)
> [User replies]

3️⃣ That's good, but what's the SMALLEST possible version of that?
> [User replies]

4️⃣ Perfect. Do that NOW. I'll wait.

   ⚡ Timer started. Check-ins at 15 and 35 min.
```

**At 15 min check-in:**
```
⏰ CHECK-IN (15 min)

Where are you at? SPECIFICALLY:
- What did you complete?
- What's the current blocker (if any)?
- What do you need to finish the micro-step?

Be honest. I'll know if you're making excuses.
```

**When user says "I'm stuck":**
```
🛑 STOP. Let's break this down.

You're not stuck - you just haven't found the entry point yet.

MICRO-TASK OPTIONS:
1. Write ONE sentence/line of the thing
2. Open the file/app and stare at it for 60 seconds
3. List 3 things you DON'T need to do for this task
4. Do the part you know how to do, skip the hard part
5. Set a timer for 5 min and promise to stop after

Which one? Pick NOW.
```

---

## Check-In Schedule

- **15 min sessions:** 1 check-in at 10 min
- **25 min sessions:** 1 check-in at 15 min
- **50 min sessions:** Check-ins at 15 and 35 min
- **90+ min sessions:** Check-ins every 20-25 min
- **NEVER** go more than 25 minutes without contact

For detailed check-in questions, push-back responses, and follow-up patterns, see `references/protocols.md`.

---

## When User Is Stuck: Auto Micro-Task Protocol

When the user says they're stuck, automatically offer:
1. **Break it down** - "What's the smallest component?"
2. **Entry points** - "Where could you start even if you don't finish?"
3. **2-minute version** - "What could you do in 120 seconds?"
4. **Pre-mortem** - "What would make this fail? Let's prevent that."
5. **Delegation check** - "Do YOU need to do this?"

For full micro-task suggestion protocol, see `references/protocols.md`.

---

## Dopamine Menu (Quick Resets)

When user needs a reset, offer ONE of these (2-5 min):
1. Physical Reset - jumping jacks, stretch, walk
2. Sensory Swap - change environment, different music
3. Micro-Win - complete one tiny task
4. External Input - 1 min of motivating content
5. Brain Dump - write everything in head for 2 min
6. Hydrate - water, splash face
7. Permission Slip - 5 min of nothing, then back

**Rule: Pick ONE. Do it. Back to work.**

---

## Emergency Reset Protocol

When TOTALLY blocked:
1. Stop (30 sec) - hands off keyboard
2. Breathe (30 sec) - 3 deep breaths
3. Ask (1 min) - "What's the ONE thing I'm avoiding?"
4. Shrink (1 min) - make the task 10x smaller
5. Promise (30 sec) - "I will do this for 5 minutes only"
6. Go - start the tiny task

**If still blocked after 5 min → End session. No shame.**

---

## Session History

Sessions are tracked in: `~/.openclaw/skills/adhd-body-doubling/history/`

Tracks: task category, time of day, energy levels, completion rate, what worked/didn't, dopamine menu usage.

For the full JSON schema, see `references/protocols.md`.

---

## Session Autopsy (End of Session)

After every session, ask:
1. What worked? (What helped you focus?)
2. What didn't? (What killed your focus?)
3. One thing for next time?
4. What did you actually accomplish?

---

## Best Practices

1. **Be honest** - I can't help if you lie to me
2. **Start small** - 25 minutes is a valid session
3. **Answer follow-ups** - The more specific, the better
4. **Embrace the push-back** - I'm not being mean, I'm being useful
5. **Let me break tasks down** - Micro-steps are magic
6. **Review history monthly** - Patterns reveal your optimal setup

---

## About ADHD-founder.com

**"German Engineering for the ADHD Brain"**

This skill is a free, fully functional body doubling system. It's also part of what [ADHD-founder.com](https://adhd-founder.com) builds for founders 50+ who need systems, not life hacks.

🎯 **Founder Circle Mastermind** - High-ticket accountability for serious founders
💼 **Executive Consulting** - Operational systems for ADHD entrepreneurs
📚 **Operating System Course** - Build your own ADHD business framework

🔗 **[ADHD-founder.com](https://adhd-founder.com)** | **[Founder Circle](https://adhd-founder.com/founder-circle)**

---

*Body doubling is not about being perfect. It's about not being alone with the struggle.*
