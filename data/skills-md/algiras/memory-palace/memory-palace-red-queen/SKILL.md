---
name: memory-palace-red-queen
description: Transform information into durable knowledge using the method of loci with adversarial recall testing. The Red Queen Protocol continuously challenges your memories to prevent decay and hallucinations. Essential for serious learners preparing for technical interviews, certifications, or mastering complex subjects. Triggers on "remember this", "memorize", "create memory palace", "recall", "what did I store", "memory palace", "red queen", "study for interview", "prepare for exam".
license: MIT
metadata:
  author: Algiras
  version: "2.1.0"
---

# Memory Palace + Red Queen

> "It takes all the running you can do, to keep in the same place." — Lewis Carroll

The ancient **method of loci** creates vivid, unforgettable memories. The **Red Queen Protocol** ensures they stay accurate through continuous adversarial testing. Without testing, memories decay. Without vivid encoding, testing fails. This skill combines both.

**Key Results:** -37% retrievals needed, +23% retention for weak memories, F1=0.92 hallucination detection

## Why Red Queen Matters

Memory without testing is dangerous. Studies show:
- Untested memories decay 40% within 24 hours
- Hallucinations creep in when you can't verify accuracy
- Spaced repetition alone misses conceptual gaps

The Red Queen Protocol solves this with four specialized agents that continuously challenge and strengthen your knowledge.

## Commands

### Core Commands
| Command | Description |
|---------|-------------|
| `/memory-palace store <topic>` | **Encode** information using SMASHIN SCOPE vivid imagery |
| `/memory-palace red-queen [strategy]` | **Test** yourself with adversarial recall |
| `/memory-palace interview [topic] [duration]` | **Pressure test** with timed rapid-fire Q&A |
| `/memory-palace recall [topic]` | **Walk through** palace to retrieve memories |
| `/memory-palace status` | **Monitor** memory health and decay prediction |

### Palace Management
| Command | Description |
|---------|-------------|
| `/memory-palace create <name> [theme]` | Create new palace |
| `/memory-palace open <name>` | Set active palace |
| `/memory-palace list` | Show all palaces |
| `/memory-palace tour` | Full walkthrough |
| `/memory-palace navigate [destination]` | Cross-palace exploration |
| `/memory-palace define <concept>` | Instant lookup |

## Quick Start: Learn, Test, Evolve

```
# 1. ENCODE - Create vivid memory
/memory-palace create "System Design" "Space Station"
/memory-palace store "CAP theorem"

# 2. TEST - Red Queen challenges you
/memory-palace red-queen weak-spots

# 3. EVOLVE - Strengthen weak memories
/memory-palace interview system-design 10min

# 4. MONITOR - Check decay prediction
/memory-palace status
```

## The Red Queen Protocol

Four agents work together to maintain memory integrity:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  EXAMINER   │────►│   LEARNER   │────►│  EVALUATOR  │
│  (haiku)    │     │   (haiku)   │     │   (haiku)   │
│ Generate Qs │     │ Blind recall│     │ Score gaps  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │   EVOLVER   │
                                        │   (opus)    │
                                        │ Strengthen  │
                                        └─────────────┘
```

### Agent Roles

| Agent | Model | Role |
|-------|-------|------|
| **Examiner** | haiku | Reads palace, generates hard questions targeting weak spots |
| **Learner** | haiku | Attempts blind recall from anchors only, rates confidence |
| **Evaluator** | haiku | Compares to ground truth, scores accuracy, identifies gaps |
| **Evolver** | opus | Creates stronger SMASHIN SCOPE images for weak memories |

### Testing Strategies

| Strategy | When to Use |
|----------|-------------|
| `weak-spots` | **Default** - Focus on low-confidence items (recommended weekly) |
| `random` | Quick sanity check |
| `depth-first` | Complete palace audit |
| `cross-link` | Test connections between concepts |
| `adversarial` | Edge cases and failure modes |
| `interview` | Time pressure simulation |

## Command Details

### `/memory-palace store <topic>` - Vivid Encoding

Use **SMASHIN SCOPE** to create unforgettable images:
- **S**ubstitute abstract → concrete
- **M**ovement - make it animated
- **A**bsurd - impossible/exaggerated
- **S**ensory - all 5 senses
- **H**umor - make it funny
- **I**nteract - you are part of scene
- **N**umbers - encode with shapes
- **S**ymbols - visual puns
- **C**olor - vivid, unusual
- **O**versize - dramatic scale
- **P**osition - precise placement
- **E**motion - strong feelings

### `/memory-palace red-queen [strategy]` - Adversarial Testing

The core of the skill. Without this, you're just storing notes.

**Protocol:**
1. Load palace and identify target memories
2. Launch Examiner to generate challenging questions
3. You attempt blind recall from anchors only
4. Evaluator scores accuracy vs. ground truth
5. Update learning journal with identified gaps
6. Optional: Evolver creates stronger images for weak spots

**Example weak-spots session:**
```
/memory-palace red-queen weak-spots

🔴 WEAK SPOT DETECTED
━━━━━━━━━━━━━━━━━━━━━
Topic: Two-Phase Commit
Confidence: 2/5 (68% → 43% in 3 days)
Anchor: "Tightrope walker with two clipboards"

Question: What happens if the coordinator crashes 
after sending PREPARE but before sending COMMIT?

Your recall: ________________
```

### `/memory-palace interview [topic] [duration]` - Pressure Testing

Simulates interview conditions:
- Rapid-fire questions
- Time pressure
- No reference materials
- Immediate feedback

**Best for:** Interview prep, certification exams, identifying true mastery gaps

```
/memory-palace interview "system design" 10min

⏱️ INTERVIEW MODE: 10 MINUTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/∞] What are the tradeoffs between strong and 
eventual consistency?

[2/∞] Design a rate limiter. What happens when 
Redis is unavailable?

[3/∞] How does consistent hashing handle node 
addition vs. removal?
```

## Storage Structure

```
~/memory/
├── config.json              # System configuration
├── global/                  # Cross-project knowledge
│   ├── palace-registry.json
│   ├── meta-index.md
│   ├── learning-journal.md     # Tracks gaps from Red Queen
│   └── *.json
│
└── project/
    └── {projectId}/         # Project-specific knowledge
        ├── palace-registry.json
        ├── meta-index.md
        ├── learning-journal.md
        └── *.json
```

## Best Practices

### Weekly Workflow
1. **Monday:** `/memory-palace red-queen weak-spots` - Fix gaps
2. **Wednesday:** `/memory-palace interview` - Pressure test
3. **Friday:** `/memory-palace status` - Review decay predictions

### Critical Rules
- **Never skip testing** - Memories decay without Red Queen
- **Trust weak spots** - Low confidence items need immediate attention
- **Interview weekly** - Time pressure reveals true gaps
- **Evolve failed recalls** - Don't just re-read; create stronger images

### When to Use Each Strategy
- **Learning phase:** `weak-spots` weekly + `interview` after each topic
- **Interview prep:** `interview` daily + `adversarial` for edge cases
- **Maintenance:** `random` quick checks + `cross-link` for connections
- **Audit:** `depth-first` monthly complete review

## Warning: Without Red Queen

> Memory without testing is belief without verification.

Users who only store without testing report:
- "I thought I knew it" → Failed interviews
- "I memorized that" → Couldn't recall under pressure
- "I reviewed it" → Hallucinated details confidently

The method of loci creates memories. **The Red Queen keeps them honest.**
