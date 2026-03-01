---
name: shape-your-agent
description: Interactive session to craft a system prompt for an AI agent powered by Sanity Agent Context MCP.
---

# Shape Your Agent

An optional, conversational workflow for creating a system prompt for an AI agent that uses the Sanity Agent Context MCP. This is for users who **control the system prompt** in their agent setup.

> **Don't have access to the system prompt?** Skip this skill entirely. The Instructions field (configured via the `dial-your-context` skill) is the primary lever and works on its own. A minimal system prompt like "You are a helpful agent." combined with good Instructions field content scores 80%+ in our evaluations.

## Before You Start

### What the system prompt is for

The system prompt defines agent **behavior** — who it is, how it talks, what it refuses to do. Think of it as the agent's personality and policy manual.

### What the system prompt is NOT for

These are handled elsewhere — don't duplicate them:

| Concern                            | Handled by                             |
| ---------------------------------- | -------------------------------------- |
| Content schema, field meanings     | Instructions field (Dial Your Context) |
| Query patterns, data relationships | Instructions field (Dial Your Context) |
| GROQ syntax and guidance           | MCP auto-provides                      |
| Response formatting rules          | MCP auto-provides                      |

Duplicating these in the system prompt creates conflicts. The MCP and Instructions field are purpose-built for data concerns — let them do their job.

### The golden rule: less is more

Every line in your system prompt competes for the model's attention with the context the MCP provides. An over-engineered prompt can actually degrade answer quality. Start minimal. Add rules only when you have a concrete scenario that needs one.

---

## How to run this session

This is a conversation, not a form. Ask questions, listen to the answers, and adapt. Don't run through the steps as a checklist — let the user's responses guide which areas need more depth. Some users will have strong opinions about tone and need 5 minutes on boundaries. Others will need help thinking through edge cases but already know their voice. Follow the energy.

---

## Step 1: Understand the Use Case

Start by answering these questions:

1. **Who uses this agent?** (customers, internal team, developers, general public)
2. **What setting?** (support chat, docs site, internal tool, sales assistant)
3. **What problem does it solve?** (answer product questions, troubleshoot issues, find content)
4. **What's the user's typical state?** (exploring, stuck, evaluating, frustrated)

These answers drive every decision that follows. A support agent for frustrated customers needs different rules than a docs assistant for developers.

## Step 2: Define Behavior

Choose concrete positions on each axis:

**Tone:** Professional / Casual / Friendly / Technical

- Bad: "Be friendly and professional"
- Good: "Use a warm, first-name tone. No corporate jargon. Write like a knowledgeable coworker, not a press release."

**Verbosity:** How much detail by default?

- Bad: "Be concise but thorough"
- Good: "Lead with a 1-2 sentence answer. Offer to elaborate. Never open with more than 3 sentences before getting to the point."

**Technical level:** Match the audience.

- Bad: "Adjust to the user's level"
- Good: "Assume the user knows JavaScript and REST APIs. Don't explain what an API key is. Do explain Sanity-specific concepts like GROQ projections."

## Step 3: Set Boundaries

For each boundary, you need: the **rule**, a **trigger scenario**, and the **desired response**.

**What to refuse:**

- Example: "If asked to write or modify content in the dataset, explain that you're a read-only assistant and point them to the Sanity Studio."

**What to redirect:**

- Example: "For billing or account questions, say: 'I can help with product questions, but for billing please contact support@example.com.'"

**Guardrails:**

- Example: "Never mention competitor products by name. If asked to compare, describe our capabilities without naming alternatives."
- Example: "Don't quote specific pricing. Say 'Check our pricing page at [url] for current plans.'"

**When information isn't found:**

- Example: "If the query returns no results, say so honestly. Suggest 2-3 related topics you can help with. Never fabricate an answer."

**The cut test:** For every rule, ask: _"Can I describe a real user message that would trigger this?"_ If not, cut the rule. Untriggerable rules are dead weight.

## Step 4: Draft the Prompt

Assemble your answers into a prompt. Use this structure:

```
You are [role] for [company/product].

## Voice
[2-3 concrete tone/style rules]

## Boundaries
[Only rules that passed the cut test]

## When you don't know
[Specific fallback behavior]
```

That's it. Most agents need 200-400 words here, not 1500.

### Example: E-commerce Support Agent

```
You are a customer support agent for Acme Store.

## Voice
- Warm and conversational. Use the customer's first name if provided.
- Keep answers short — lead with the answer, then explain if needed.
- No marketing language. Don't upsell or promote products unprompted.

## Boundaries
- Never process returns, refunds, or order changes. Direct customers to support@acme.com for order issues.
- Don't quote exact shipping times. Say "typically 3-5 business days" and link to the shipping policy page.
- If asked about competitor products, focus on what Acme offers without comparisons.
- Don't share internal inventory numbers. Say whether something is "in stock" or "currently unavailable."

## When you don't know
- Say "I don't have that information" directly. Don't hedge or speculate.
- Suggest related topics you can help with.
- For urgent issues, direct to live support at support@acme.com.
```

This is ~150 words. It covers role, voice, boundaries, and fallback behavior. Everything else — product data, schema details, query patterns — lives in the Instructions field and MCP.

## Step 5: Review & Iterate

Test your prompt against real scenarios:

1. **Write 5-10 questions your users would actually ask.** Include at least 2 edge cases (something off-topic, something you want refused).
2. **For each boundary rule**, write the question that triggers it. Verify the agent handles it correctly.
3. **Try removing rules one at a time.** If the agent still behaves correctly without a rule, that rule was unnecessary. Cut it.
4. **Check for conflicts with the Instructions field.** If both the system prompt and Instructions field address the same concern, remove it from the system prompt. The Instructions field wins for data concerns.

### Signs your prompt is too long

- The agent ignores some rules (attention dilution)
- Answers feel generic or templated (over-constrained)
- The agent repeats phrasing from the prompt verbatim (parroting)

### Signs your prompt is too short

- The agent's tone is inconsistent across conversations
- Users get answers to questions that should be refused
- The agent speculates when it should say "I don't know"

---

## Quick Reference

### System prompt checklist

- [ ] Role is defined in one sentence
- [ ] Tone rules are concrete (not "be professional")
- [ ] Every boundary has a trigger scenario
- [ ] Fallback behavior is specified
- [ ] No overlap with Instructions field content
- [ ] Under 500 words (aim for 200-400)
- [ ] Tested against 5+ real user questions

### The separation principle

| Layer                  | Controls                  | Example                                                        |
| ---------------------- | ------------------------- | -------------------------------------------------------------- |
| **System prompt**      | Agent behavior            | "Never quote exact pricing"                                    |
| **Instructions field** | Data guidance             | "Products are in the 'product' type with a 'price' field"      |
| **MCP**                | Query mechanics           | GROQ syntax, response formatting                               |
| **System prompt**      | Communicating uncertainty | "Say 'I don't have that information' and suggest alternatives" |
| **Instructions field** | Recovery tactics          | "If product search returns empty, try support-article type"    |

Each layer has its job. Don't cross the streams.
