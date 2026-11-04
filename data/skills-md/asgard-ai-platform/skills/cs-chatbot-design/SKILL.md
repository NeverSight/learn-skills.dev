---
name: "cs-chatbot-design"
description: "Design conversational AI chatbots including intent recognition, slot filling, dialogue flow, and response generation. Use this skill when the user needs to build a chatbot, design conversation flows, implement intent classification, or improve chatbot accuracy — even if they say 'build a chatbot', 'our bot doesn't understand users', 'design a FAQ bot', or 'improve our chatbot's responses'."
metadata:
  category: "WP-06 Agent通訊+客服"
  tags: ["chatbot", "conversational-ai", "nlu", "dialogue"]
---

# Chatbot Design

## Framework

```
IRON LAW: Intent First, Response Second

A chatbot must UNDERSTAND what the user wants (intent) before crafting
a response. Building response templates without intent classification
produces a keyword-matching FAQ, not a chatbot.

Flow: User message → Intent classification → Slot extraction → Response
```

### Core NLU Pipeline

| Stage | What It Does | Example |
|-------|-------------|---------|
| **Intent Classification** | Identify what the user wants to do | "What time do you close?" → intent: `check_hours` |
| **Entity/Slot Extraction** | Extract key information from the message | "Book a table for 4 on Friday" → slots: {party_size: 4, date: Friday} |
| **Dialogue Management** | Decide the next action (ask for missing info, confirm, execute) | Missing slot `time` → ask "What time would you like?" |
| **Response Generation** | Produce the reply | "I've booked a table for 4 on Friday at 7pm. See you then!" |

### Intent Design

- **Start with 10-15 core intents** covering 80% of user queries
- Each intent needs 10-20 training examples (varied phrasings)
- Include a `fallback` intent for unrecognized inputs
- Group related intents: `order_status`, `order_cancel`, `order_modify` under "Order Management"

### Dialogue Flow Patterns

| Pattern | When to Use | Example |
|---------|-----------|---------|
| **Single-turn** | Simple Q&A, no context needed | "What are your hours?" → respond immediately |
| **Multi-turn (slot filling)** | Need multiple pieces of info | "Book a table" → ask party size → ask date → ask time → confirm |
| **Branching** | Different paths based on user's answer | "Do you have an account?" → Yes: login flow / No: registration flow |
| **Confirmation** | Before executing actions | "I'll cancel order #12345. Is that correct?" |
| **Handoff** | Bot can't handle the request | "Let me connect you with a human agent" |

### Response Design Principles

1. **Acknowledge first**: "Got it, you want to check your order status."
2. **Be concise**: Answer the question, then stop. Don't add unnecessary information.
3. **Offer next steps**: "Is there anything else I can help with?" or suggest related actions.
4. **Use quick replies/buttons**: Reduce typing, guide the conversation.
5. **Personality**: Define a consistent tone (friendly, professional, casual) and stick to it.

### Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| **Intent accuracy** | % correctly classified intents | > 85% |
| **Containment rate** | % resolved without human handoff | > 60-70% |
| **CSAT** | Customer satisfaction score | > 4.0/5 |
| **Fallback rate** | % triggering fallback/unknown intent | < 15% |
| **Resolution time** | Average time to resolve | < 2 minutes |

## Output Format

```markdown
# Chatbot Design: {Use Case}

## Intent Catalog
| Intent | Description | Example Utterances | Priority |
|--------|-----------|-------------------|---------|
| {intent} | {what it means} | "{example 1}", "{example 2}" | H/M/L |

## Dialogue Flows
### {Flow Name}
1. User: {trigger utterance}
2. Bot: {response + slot question if needed}
3. User: {provides info}
4. Bot: {confirmation or action}

## Fallback Strategy
- After 1 miss: rephrase + suggest options
- After 2 misses: offer human handoff

## Metrics Targets
| Metric | Target |
|--------|--------|
| Intent accuracy | > {X%} |
| Containment | > {X%} |
```

## Gotchas

- **Users don't follow your flow**: People type in unexpected ways, change topics mid-conversation, and give incomplete information. Design for messiness, not just the happy path.
- **Fallback is your most important intent**: A good fallback ("I'm not sure I understood. Did you mean X, Y, or Z?") is better than a bad guess.
- **LLM-powered bots still need guardrails**: Using GPT/Claude for response generation? Add intent classification as a first layer to route and constrain, preventing hallucination and off-topic responses.
- **Test with real users, not team members**: Your team knows how the bot works and phrases things "correctly." Real users don't. Test with 10+ real users before launch.
- **Conversation logs are gold**: Review conversation logs weekly. Failed conversations reveal missing intents, confusing flows, and training data gaps.

## References

- For NLU training data best practices, see `references/nlu-training.md`
- For LINE/Messenger platform integration, see the ecom-conversational skill
