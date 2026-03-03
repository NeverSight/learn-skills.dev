---
name: mentoring-developers
description: Frameworks for effective mentoring and knowledge transfer. Use for 1:1 meetings, pair programming, onboarding, teaching technical concepts, and developing junior engineers.
allowed-tools: Read, Glob, Grep
---

# Mentoring Developers

This skill provides frameworks for effective mentoring, knowledge transfer, and developing other engineers.

## When to Use This Skill

- Starting a formal or informal mentoring relationship
- Onboarding a new team member
- Teaching technical concepts to junior engineers
- Running effective 1:1 meetings
- Pair programming with less experienced developers
- Helping someone navigate their career

## Core Frameworks

### Crawl-Walk-Run Progression

A framework for teaching new skills progressively:

| Phase | Mentor Role | Mentee Role | Duration |
| ----- | ----------- | ----------- | -------- |
| **Crawl** | Do, they observe | Watch and ask questions | Until they understand the "what" |
| **Walk** | Guide heavily | They try, you correct | Until they can do it with help |
| **Run** | Provide guardrails | They lead, you advise | Ongoing with decreasing support |

#### Example: Teaching Code Review

**Crawl:** You review PRs together, thinking aloud about what you look for, why things matter, what makes good/bad code.

**Walk:** They do the review, you watch. You ask questions: "What about this section?" You course-correct in real-time.

**Run:** They review independently. You spot-check occasionally and discuss any disagreements. They come to you with edge cases.

**Key principle:** Stay in each phase long enough. Rushing to "Run" creates gaps.

### Socratic Questioning

Instead of giving answers, ask questions that lead to understanding:

| Instead of... | Ask... |
| ------------- | ------ |
| "Use a hash map here" | "What data structure would give us O(1) lookups?" |
| "You need to handle null" | "What happens if this value is null?" |
| "That's inefficient" | "What's the time complexity here? Could we do better?" |
| "Don't do it that way" | "What are the trade-offs of this approach?" |

#### Benefits

- They learn to think, not just memorize
- Builds problem-solving muscles
- They discover answers themselves (more memorable)
- You understand their thought process

**When NOT to use Socratic questioning:**

- Production incident - just tell them the fix
- Simple factual questions - don't make them guess
- When they're frustrated or overwhelmed

### Building Trust

Trust is the foundation of effective mentoring:

#### Trust-Building Practices

1. **Show genuine interest in their goals**
   - Ask about career aspirations
   - Remember and follow up on personal details
   - Celebrate their wins publicly

2. **Create psychological safety**
   - Normalize mistakes: "I make these too"
   - Share your own failures and learnings
   - Never shame, even privately

3. **Maintain confidentiality**
   - What they share stays between you
   - Don't mention their struggles to others
   - Ask before sharing their work as examples

4. **Be consistent and reliable**
   - Show up to 1:1s on time
   - Follow through on commitments
   - Be honest about your own limitations

5. **Acknowledge when they teach you**
   - Mentoring is bidirectional
   - Let them know when you learned from them
   - Builds their confidence and equalizes the relationship

### Tailoring to Learning Styles

People learn differently. Adapt your approach:

| Style | Signs | Approach |
| ----- | ----- | -------- |
| **Visual** | Asks for diagrams, draws things out | Use whiteboarding, architecture diagrams, code walkthroughs |
| **Auditory** | Learns from discussion, podcasts | Talk through concepts, think-aloud, verbal explanations |
| **Kinesthetic** | Prefers hands-on practice | Pair programming, experiments, building things |
| **Reading/Writing** | Prefers documentation | Point to docs, have them write summaries |

**Most people are a mix.** Start with all approaches, then observe what clicks.

## Pair Programming for Mentoring

Pair programming is a powerful mentoring tool when done well. See `references/pair-programming-guide.md` for detailed guidance.

### Key Principles

- Rotate driver/navigator roles
- Narrate your thinking when driving
- Let them struggle (productively)
- Never grab the keyboard without permission

## 1:1 Meeting Structure

Effective 1:1s are the backbone of mentoring. See `references/one-on-one-structure.md` for detailed templates.

### Basic Structure (30 min)

- Progress check (5 min)
- Challenges/blockers (10 min)
- Development goals (10 min)
- Open discussion (5 min)

### Key Principles for 1:1s

- Their agenda, not yours
- Consistent cadence (weekly ideal)
- Take notes and follow up
- Occasionally skip status and go deep on growth

## Common Mentoring Mistakes

### Taking Over

❌ Grabbing the keyboard when they struggle
✅ Ask guiding questions, let them try

### Assuming Knowledge

❌ "You know what a REST API is, right?"
✅ "What's your experience with REST APIs?"

### Overwhelming with Information

❌ Explaining everything about microservices at once
✅ Focus on what they need now, save rest for later

### Neglecting the Relationship

❌ Only discussing technical work
✅ Check in on how they're doing personally

### Doing vs. Teaching

❌ "I'll just fix this, it's faster"
✅ "Let's fix this together so you see how"

## Measuring Progress

Track mentee development over time:

### Technical Progress

- PRs requiring less revision
- Taking on more complex tasks
- Helping others with areas you taught

### Professional Progress

- More confident in meetings
- Asking better questions
- Navigating team dynamics effectively

### Relationship Health

- They bring you problems early
- Honest about struggles
- Proactive about scheduling time

## Related Resources

- `references/pair-programming-guide.md` - Communication during pairing
- `references/one-on-one-structure.md` - 1:1 meeting frameworks
- `/soft-skills:write-1on1-agenda` command - Generate 1:1 agendas
- `feedback-conversations` skill - Giving developmental feedback
- `professional-communication` skill - General communication patterns

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
