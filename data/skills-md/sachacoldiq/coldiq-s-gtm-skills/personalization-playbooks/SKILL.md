---
name: personalization-playbooks
description: Camp Personalization vs No Personalization playbooks by outreach category - Inbound, Postbound, Bridgebound, and Outbound. Use when deciding personalization level, building automated sequences, or creating messaging templates.
---

# Personalization Playbooks

## Camp Personalization Playbook (Manual/High-Touch)

### INBOUND
```
First Line: Trigger-Based Relevance ONLY
Second Line: CTA to Book Time (Optional: Core-Static Relevance)
```

**Example:**
```
Thanks for downloading the Cold Email Playbook.

Got 15 minutes to discuss how to apply it at {{company}}?
```

### POSTBOUND/BRIDGEBOUND
```
First Line: Trigger-Based Relevance + ("but more importantly") Personalization
Second Line: Personalization "Hook" + Core-Static Relevance
```

**Example:**
```
Saw you attended our webinar on signal-based outbound—but more importantly, your recent post about "outbound being dead" caught my attention.

You mentioned reply rates dropping below 1%. We've been helping B2B SaaS companies hit 15%+ with signal-first targeting.

Worth a quick chat?
```

### OUTBOUND
```
First Line: Personalization Title or Summary + Personalization Excerpt
Second Line: Personalization "Hook" + Core-Static Relevance
```

**Example:**
```
Your post on SDR burnout—specifically the line "throwing bodies at the problem doesn't scale"—resonated.

We work with SaaS companies doing $5-20M who've hit that wall. Most are shifting from volume to signal-based.

Curious if that's on your radar?
```

---

## Camp No Personalization Playbook (Automated/Scale)

### INBOUND
```
First Line: Trigger-Based Relevance ONLY
Second Line: CTA to Book Time (Optional: Core-Static Relevance)
```

**Example:**
```
Thanks for requesting a demo.

Let's find 15 minutes to walk through how {{product}} works for {{industry}} companies.

[Calendar link]
```

### POSTBOUND/BRIDGEBOUND
```
First Line: Trigger-Based Relevance
Second Line: Core-Static Relevance
```

**Example:**
```
Noticed you've been checking out our pricing page.

We work with B2B SaaS companies doing $5-20M ARR on outbound.

Worth a quick call to see if there's a fit?
```

### OUTBOUND
```
First Line: Core-Static Relevance (Lean on Pattern Interruptive Opener)
Second Line: Core-Static Relevance ("We work with...")
```

**Example:**
```
Quick question: How's your team handling pipeline predictability right now?

We work with B2B SaaS companies doing $5-20M who struggle with inconsistent lead flow.

Worth exploring?
```

---

## Decision Matrix

| Factor | Use Personalization | Skip Personalization |
|--------|---------------------|---------------------|
| Deal size | >$25K ACV | <$25K ACV |
| Volume | <50/day | >100/day |
| ICP fit | Tier 1 accounts | Tier 2-3 accounts |
| Signal strength | Weak signals | Strong signals |
| Competitive | High competition | Low competition |

---

## Combines with

| Skill | Why |
|-------|-----|
| `outreach-4-categories` | Match playbook to lead category |
| `personalization-6-buckets` | Find data for personalization |
| `personalization-hooks` | Create hooks for Camp Personalization |
| `cold-email-4-sequence` | Apply playbook to sequence |

## Example prompts

```
Which playbook should I use for a $15K ACV deal with strong intent signal?
```

```
Write a Camp Personalization Bridgebound email for this prospect: [details]
```

```
Create a No Personalization Outbound template for targeting DevOps managers.
```
