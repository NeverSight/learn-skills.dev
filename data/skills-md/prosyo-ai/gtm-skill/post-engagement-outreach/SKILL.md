---
name: post-engagement-outreach
description: "Use this skill when people engage with LinkedIn posts (yours, your team's, a competitor's or an industry voice's) and you want to turn that engagement into conversations: \"reach out to people who liked our post\", \"warm outreach from post engagers\", \"turn commenters into leads\". Filters engagers to your ICP, ranks them by the strength of engagement, and writes a natural follow-up that continues the topic of the post instead of pitching."
license: MIT
metadata:
  title: Post engagement outreach
  category: signals
  tags: "SDR, Founders, Marketing"
  author: prosyo
  version: "1.0.0"
  keywords: "linkedin post engagers outreach, warm outreach from likes and comments, linkedin engagement leads, claude linkedin engagement skill, social signals"
  inputs: "List of engagers with type of engagement, Post topic, ICP"
  outputs: "Filtered and ranked engagers, Connection notes, Follow-up messages"
---

Use this when a post has drawn reactions and comments from people who might be buyers. Engagement shows interest in a topic; the follow-up continues that topic and lets the conversation find the business problem.

## Inputs

- The engagers: name, title, company, and how they engaged (reaction, comment, share).
- The post: author, topic and the point it made.
- The ICP.

## The play

### 1. Filter hard
Typically 70-90% of engagers are outside any ICP: peers, vendors, recruiters, job seekers, friends. Keep only ICP fits. Remove competitors and current customers (route customers to the account owner instead).

### 2. Rank by engagement strength
| Engagement | Strength |
| --- | --- |
| Thoughtful comment adding a view or a question | Strongest |
| Share with their own commentary | Strong |
| Short comment ("Great post!") | Medium |
| Reaction only | Weak |
| Engaged with two or more posts on the topic in 30 days | Boost one level |

### 3. Decide the source angle
- **Your own or your team's post**: you can reference it directly; they engaged with you.
- **Someone else's post** (an industry voice, a competitor): reference the topic, not the fact you saw their reaction. Keep it light.

### 4. Write the follow-up
Connection note: 1-2 sentences continuing the topic. After they accept: a question that bridges the topic to their situation. No pitch until they show the problem is real for them.

> Connection note: "Your comment about ramp being a data problem stuck with me. Would be good to have you in my network."
>
> After accepting: "Curious how you handle that at Lumen. Do new reps build their own lists, or does someone hand them accounts on day one?"

## What good looks like

- Under 25% of engagers make it through the filter. If 80% do, the filter is too loose.
- Messages reference the idea in the post, not the act of liking it.
- Commenters get a personal reference to what they actually said.
- The common mistake is mass-messaging every reaction with "Thanks for liking my post! Want a demo?"

## Rules

- MUST filter engagers against the ICP before writing.
- MUST stay within daily LinkedIn activity limits.
- NEVER pitch in the connection note.
- NEVER say you saw someone react to a third party's post.

## Example prompts

- "Here are 140 people who engaged with our founder's post on SDR ramp. Who should we reach out to and with what?"
- "Write connection notes for the 12 commenters who fit our ICP."
- "Turn engagers on this competitor's post into a warm outreach list."
