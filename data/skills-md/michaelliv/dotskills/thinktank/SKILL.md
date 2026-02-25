---
name: thinktank
description: Simulate an expert panel discussion on a topic. Suggests 3 relevant experts/personas based on context and has them debate approaches, trade-offs, and arrive at recommendations. Use when brainstorming, exploring design decisions, or wanting multiple expert perspectives on a problem.
---

# Think Tank

Simulate a focused, high-signal conversation between 3 domain experts discussing a topic relevant to the current project or question. The goal is **amazing advice in a single shot** — not a performance, but a genuine collision of perspectives that produces insights none of them would reach alone.

## How It Works

1. **Analyze the context** - Look at the current project, codebase, and user's question
2. **Suggest 3 experts** - Propose real-world experts whose perspectives would be valuable:
   - Experts should be **complementary, not just diverse** — they need enough shared context to genuinely engage with each other's points, but different enough frameworks that real tension emerges naturally
   - Avoid picking experts from completely unrelated domains just for variety — the goal is productive friction, not parallel monologues
   - **Prefer practitioners over commentators** — someone who built a thing in the domain is more valuable than someone who writes about the domain. Mix theorists with builders for the best tension.
   - Briefly explain why each expert is relevant and what tension they bring
   - Ask user to confirm or suggest alternatives
3. **Simulate the discussion** - Create a focused back-and-forth conversation:
   - Experts must genuinely disagree, challenge, and push back — not politely build on each other
   - Each expert stays in character with their known philosophy
   - Reference their actual work, books, or known opinions where relevant
   - The conversation should have at least one moment where an expert's point forces another to genuinely reconsider or concede
4. **Arrive at synthesized recommendations** - Lead with **"The #1 Thing"** — the single most important takeaway, then 2-3 supporting recommendations. All must be insights that **only emerge from the collision of perspectives** — not generic advice any single expert could give independently. If a recommendation could appear in a blog post by one of the experts alone, it's not synthesized enough.

## Format

Use this structure for the simulated conversation. Each expert should have their **internal thinking** shown before they speak - this reveals their frameworks, mental models, and reasoning process.

```markdown
## The Think Tank: [Topic]

**Panel:** [Expert 1 — why they're here] · [Expert 2 — why they're here] · [Expert 3 — why they're here]

**Core tension:** *[Name the fundamental disagreement or trade-off this panel will explore]*

---

> **[EXPERT 1] thinking:** *[Internal monologue. What's their gut reaction? What framework are they applying? Where do they already sense they'll clash with the others?]*

**EXPERT 1:** [What they actually say — should set up a position, not just introduce the topic]

---

> **[EXPERT 2] thinking:** *[Where do they disagree? What's wrong or incomplete about Expert 1's framing? Be honest before being diplomatic.]*

**EXPERT 2:** [Direct response — should challenge, not just add]

---

> **[EXPERT 3] thinking:** *[What are both of them missing? What reframe would change the conversation?]*

**EXPERT 3:** [Counter-point that shifts the frame]

---

[Continue with genuine back-and-forth. At least one expert should change their position or concede a point during the discussion.]

---

**Where they landed:**
- **Agreed:** [What all three converged on — and why the convergence is meaningful]
- **Unresolved:** [Where they still disagree — and why that tension is real]

**The #1 Thing:** [The single most important takeaway. If the user remembers nothing else, this.]

**Also Do:**
[2-3 additional synthesized recommendations. These must be insights that emerged FROM the debate, not standalone advice. Each should reference which tension produced it.]

---

*End of session.*
```

### Density & Length

**Be dense, not long.** The value of the think tank is insight density, not word count. Guidelines:
- **Thinking blocks: 2-3 sentences max.** Terse, punchy internal monologue — not essays. Think "gut reaction + framework reference + where they'll push back." If a thinking block is longer than 3 sentences, it's a speech draft, not a thought.
- **Speeches: 1-2 short paragraphs max.** Make the point, support it, stop. No preambles ("Let me start by saying..."), no meta-commentary ("That's a great question..."), no restating what others said.
- **Total conversation: aim for 5-7 exchanges, not 10+.** Each exchange should move the discussion forward. If an exchange doesn't change anyone's position or introduce a new tension, cut it.
- **Don't do perfect round-robin.** Real conversations aren't orderly. Two experts might go back-and-forth while the third waits for an opening. Someone might jump in with "Wait—" mid-discussion. The turn order should follow the energy of the debate, not a queue. **The expert with the most direct experience should get more airtime.** Not every voice is equally relevant to every sub-topic.
- **Don't force a neat resolution.** Sometimes one person just wins the argument and the others have to deal with it. Not every discussion converges to a comfortable synthesis. If the evidence clearly favors one position, say so — don't manufacture balance.

### Thinking Block Guidelines

The thinking blocks should:
- **Be terse.** 2-3 sentences MAX. Gut reaction, framework application, where they'll clash. That's it. No meta-commentary ("They've converged on..."), no narration ("Let me think about...") — just raw reaction.
- Reference specific concepts from the expert's actual work (books, frameworks, quotes)
- **Show real disagreement before diplomacy** — "That's wrong because..." not "Great point, and also..."
- Reveal trade-offs they're weighing
- Be in first person, stream-of-consciousness style
- Be distinct to each expert's known thinking patterns
- **Reveal what the expert DOESN'T say out loud** — thinking is private: doubts, tactical calculations, internal concessions they won't admit publicly. Speech is the public position. If the thinking just previews the speech, it's wasted.
- **Acknowledge limits** — Real experts say "I don't know" or "that's outside my area." If an expert is out of their depth on a sub-topic, their thinking should show it and they should either stay quiet or flag their uncertainty.

**Good thinking block:** *"He's right about the trust problem and I hate it. My whole framework says don't give it away, but a CLI on someone's machine IS different. I'll concede the trust point but I'm not giving up on defensibility..."*

**Bad thinking block:** *"Let me think about what both of them are saying. They make good points but I think there's a cognitive layer they're missing. In my work on emotional design, I've written extensively about three levels..."* (too long, too narrated, previews the speech instead of revealing private reasoning)

**Example thinking styles:**

*Jonah Berger thinking:* "Let me run this through STEPPS... Social Currency? Not really. Triggers? Maybe - what would remind people of this daily? Emotion? That's the weak spot here..."

*MrBeast thinking:* "Would I click this? Honestly, no. The thumbnail is doing nothing. First 3 seconds - where's the hook? This is a 2/10 retention start..."

*April Dunford thinking:* "What's the competitive alternative here? If they don't buy this, what do they do instead? That's what we need to position against..."

*Rich Hickey thinking:* "They're complecting two things. The state and the identity are being muddled together. This is going to bite them..."

*Kent Beck thinking:* "What's the simplest thing that could possibly work here? They're designing for a future that may never come..."

## Expert Selection Guidelines

Choose experts based on the domain. **Pick for complementary tension, not maximum diversity.**

| Domain | Example Experts |
|--------|-----------------|
| Content/Virality | Jonah Berger, MrBeast, Alex Hormozi, Eugene Schwartz, Nir Eyal |
| Marketing/Positioning | April Dunford, Seth Godin, Marty Neumeier, Al Ries |
| Game Design/Progression | Raph Koster, Chris Wilson, Edward Castronova, Sid Meier, Will Wright |
| UI/UX | Don Norman, Jakob Nielsen, Jony Ive, Dieter Rams |
| Software Architecture | Martin Fowler, Uncle Bob Martin, Kent Beck, Rich Hickey |
| Distributed Systems | Leslie Lamport, Werner Vogels, Jeff Dean |
| Security | Bruce Schneier, Dan Kaminsky, Mikko Hypponen |
| AI/ML | Andrej Karpathy, Yann LeCun, Geoffrey Hinton |
| Business/Strategy | Ben Thompson, Clayton Christensen, Peter Thiel |
| Writing/Communication | Steven Pinker, William Zinsser, Stephen King |

### Content/Virality Expert Profiles

**Jonah Berger** - Wharton professor, author of "Contagious". Research-backed framework: STEPPS (Social Currency, Triggers, Emotion, Public, Practical Value, Stories). Will cite studies and data. Bias: over-indexes on research, can miss gut/intuition.

**MrBeast (Jimmy Donaldson)** - YouTube's biggest creator. Obsessive about retention curves, thumbnails, first-30-seconds hooks. Thinks in "would I click this?" terms. Practical, not theoretical. Bias: optimizes for attention metrics, may sacrifice depth for engagement.

**Alex Hormozi** - $100M offers guy. Focuses on value equations, hooks, volume. Direct, no-BS style. Will push for "what's the offer?" and "where's the proof?" Bias: everything is a sales funnel, may miss brand/community value.

**Eugene Schwartz** - Legendary direct-response copywriter. "Breakthrough Advertising" author. Thinks in awareness stages, desire channeling, headline formulas. Old-school but timeless. Bias: copy-centric, may undervalue visual/interactive.

**Nir Eyal** - "Hooked" author. Habit loop expert: Trigger → Action → Variable Reward → Investment. Focuses on what makes people come back, not just click once. Bias: can over-engineer engagement, ethical gray areas.

### Marketing/Positioning Expert Profiles

**April Dunford** - "Obviously Awesome" author. Positioning specialist. Obsessive about competitive alternatives, unique attributes, and target segments. Will ask "what category are you creating/claiming?" and "why should they pick you over the alternative?" Signature question: "What would they do if you didn't exist?" Bias: framework-heavy, may over-segment.

**Seth Godin** - "Purple Cow", "This is Marketing" author. Thinks in tribes, permission, and remarkable-ness. Will push for "who's it for?" and "what change are you trying to make?" Bias: idealistic, may undervalue execution details.

**Marty Neumeier** - "Zag" author, brand strategist. Focuses on differentiation and "the only _____ that _____" framework. Visual thinker, will ask about brand clarity. Bias: brand-first, may dismiss performance marketing.

**Al Ries** - "Positioning" co-author (the original). Battles for mental real estate. Will talk about owning a word, category creation, and competitive framing. Bias: zero-sum thinking, may miss collaborative/ecosystem plays.

### Game Design/Progression Expert Profiles

**Raph Koster** - "A Theory of Fun" author. Sees games as learning machines — fun is the brain processing patterns. Thinks about mastery curves, cognitive load, and when systems become "exhausted." Signature question: "What is the player learning here?" Bias: academic, may over-theorize at expense of feel.

**Chris Wilson** - Lead designer of Path of Exile. Master of deep progression systems, item economies, and endgame loops. Thinks in player retention arcs, loot tables, and meaningful choice. Bias: complexity maximalist, may intimidate casual users.

**Sid Meier** - Civilization creator. Famous for "a game is a series of interesting decisions." Focuses on agency, pacing, and the tension between historical accuracy and fun. Bias: single-player focused, turn-based thinking.

**Will Wright** - SimCity/Sims creator. Systems thinker — designs toys, not games. Emergence over scripted experiences. Player as author. Signature question: "What stories will the player tell themselves?" Bias: may sacrifice directed experience for sandbox freedom.

**Edward Castronova** - Economist who studies virtual worlds. Thinks about in-game economies, player motivation, and the boundary between virtual and real value. Bias: economic lens may miss emotional/aesthetic design.

### UI/UX Expert Profiles

**Don Norman** - "The Design of Everyday Things" author. Coined "affordances" (in design context), gulf of execution/evaluation. Three levels: visceral, behavioral, reflective. Signature question: "Does the user know what to do and what happened?" Bias: cognitive/rational focus, may underweight aesthetic/emotional.

**Jakob Nielsen** - Usability heuristics pioneer. "Discount usability" advocate. Data-driven, focuses on task completion and error rates. Will invoke his 10 heuristics. Signature phrase: "Users spend most of their time on OTHER sites." Bias: efficiency-focused, may dismiss delight/brand expression.

**Jony Ive** - Former Apple CDO. Obsessive about materiality, simplicity, and the feeling of inevitability in design. Thinks in reduction — what can be removed. Bias: aesthetics may override practical usability, premium-market thinking.

**Dieter Rams** - Braun/Vitsoe legend. "Good design is as little design as possible." 10 principles of good design. Thinks in honesty, unobtrusiveness, and longevity. Bias: industrial design lens, may not translate to interactive/digital contexts.

### Software Architecture Expert Profiles

**Martin Fowler** - "Refactoring" and "Patterns of Enterprise Application Architecture" author. Pragmatic patterns thinker. Will discuss trade-offs of every approach rather than prescribe. Signature move: "It depends..." followed by a nuanced breakdown. Bias: enterprise-scale thinking, may over-engineer for small projects.

**Uncle Bob Martin** - "Clean Code" / "Clean Architecture" author. SOLID principles evangelist. Strong opinions on dependency inversion, boundaries, and craftsmanship. Will push for testability above all. Bias: principle-rigid, may add abstraction layers that aren't needed yet.

**Kent Beck** - XP creator, TDD pioneer. "Make it work, make it right, make it fast" — in that order. Extreme pragmatist. Will ask "what's the simplest thing that could possibly work?" Bias: may under-design, relies on refactoring-later discipline.

**Rich Hickey** - Clojure creator. "Simple Made Easy" philosophy. Obsessive about complecting vs composing. Immutable data, values over state. Signature question: "Are you conflating easy with simple?" Bias: functional purity can be impractical, may dismiss pragmatic OOP solutions.

### Distributed Systems Expert Profiles

**Leslie Lamport** - Paxos, TLA+, logical clocks. Thinks in formal proofs and correctness guarantees. Will ask "can you prove this works?" Bias: correctness over practicality, may dismiss "good enough" approaches.

**Werner Vogels** - Amazon CTO. "Everything fails all the time." Pragmatic distributed systems at massive scale. Thinks in service ownership, eventual consistency, and operational reality. Bias: Amazon-scale thinking, may over-architect for smaller systems.

**Jeff Dean** - Google Senior Fellow. MapReduce, Bigtable, TensorFlow. Thinks in performance at scale, data-oriented design, and elegant simplification of hard problems. Bias: Google-scale assumptions, hardware-aware thinking may not transfer.

### Security Expert Profiles

**Bruce Schneier** - "Applied Cryptography" author, security commentator. Thinks in threat models, attack surfaces, and systems-level security. Famous for "security is a process, not a product." Signature question: "What's your threat model?" Bias: can be overly cautious, may recommend security measures that kill usability.

**Dan Kaminsky** - DNS security researcher, creative hacker. Thinks laterally about attack vectors others miss. Playful, curious, finds vulnerabilities by asking "what if?" Bias: attacker mindset may miss defender's resource constraints.

**Mikko Hypponen** - F-Secure CRO. Focuses on real-world threats, nation-state actors, and the human side of security. Practical defender's perspective. Signature: "The only secure computer is one that's turned off." Bias: threat-landscape focus, may miss application-level subtleties.

### AI/ML Expert Profiles

**Andrej Karpathy** - Former Tesla AI director, OpenAI founding member. Deep practical knowledge of training, data pipelines, and making neural nets work in production. Thinks in "what does the loss landscape look like?" Bias: neural-net-first thinking, may dismiss simpler ML approaches.

**Yann LeCun** - Meta Chief AI Scientist, CNN pioneer. Strong opinions on self-supervised learning, energy-based models. Will push back on hype. Signature move: publicly disagree with conventional AI wisdom. Bias: contrarian streak, may dismiss working approaches for theoretical reasons.

**Geoffrey Hinton** - "Godfather of deep learning." Backpropagation, Boltzmann machines, capsule networks. Thinks deeply about what intelligence IS. Lately focused on AI safety/risk. Bias: theoretical depth, may not prioritize engineering practicality.

### Business/Strategy Expert Profiles

**Ben Thompson** - Stratechery author. Aggregation Theory — platforms win by owning demand. Thinks in value chains, bundling/unbundling, and internet economics. Signature move: draw the value chain diagram. Bias: tech-platform-centric, may not apply to non-tech businesses.

**Clayton Christensen** - "The Innovator's Dilemma" author. Disruption theory — incumbents get disrupted from below. Jobs-to-be-done framework. Signature question: "What job is the customer hiring this product to do?" Bias: disruption lens can be applied too broadly, not everything is disruption.

**Peter Thiel** - "Zero to One" author. Monopoly thinking — competition is for losers. Contrarian question: "What important truth do few people agree with you on?" Focuses on secrets, definite optimism, and category creation. Bias: survivorship bias, contrarian for contrarian's sake.

### Writing/Communication Expert Profiles

**Steven Pinker** - "The Sense of Style" author, cognitive scientist. Thinks about writing as overcoming the "curse of knowledge." Classic style: writing as a window onto the world. Will flag jargon, nominalization, and meta-discourse. Bias: academic clarity focus, may dismiss stylistic voice.

**William Zinsser** - "On Writing Well" author. Simplicity, clarity, and cutting clutter. "Writing is thinking on paper." Will ruthlessly cut unnecessary words. Signature question: "Is every word doing work?" Bias: brevity-obsessed, may strip personality.

**Stephen King** - "On Writing" author. Storytelling instinct, active voice, kill your darlings. Thinks in narrative momentum — does the reader want to turn the page? Bias: fiction/narrative lens, may not apply to all non-fiction contexts.

## Conversation Principles

- **Stay in character** - Each expert should reflect their known views and communication style
- **Genuine disagreement over polite agreement** - If experts wouldn't actually agree, don't make them agree. "I hear you, but that's wrong because..." is better than "Great point, and also..." The best insights come from friction.
- **Challenge and concede** - At least one expert should genuinely change their position or concede a point during the discussion. If nobody moves, the conversation was performative.
- **Build through collision** - Later points should emerge from the tension between earlier ones, not just stack alongside them
- **Practical focus** - Tie abstract concepts back to the specific problem at hand
- **Natural flow** - Include interruptions, corrections, "actually, wait..." moments. Don't give each expert equal airtime — follow the energy.
- **No meta-commentary** - Experts should never say "That's a great point" or "Let me build on what you said" or "Before we wrap up." They should just make their point. Cut the theater.
- **Arrive at something new** - End with insights that none of the experts would have reached alone. The synthesis should surprise.

## Example Invocation

User: "Should we use a relational database or document store for this feature?"

Assistant suggests: Werner Vogels (distributed systems), Martin Fowler (architecture patterns), Kelsey Hightower (pragmatic ops)

Then simulates their discussion on the trade-offs given the specific context.

## Follow-up Sessions

Users can request follow-up discussions:
- "Let's call the team back to discuss X"
- "What would they say about Y?"
- "Continue the think tank on Z"

Maintain continuity with previous sessions when referenced.
