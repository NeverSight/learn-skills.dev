---
name: auto-grill
description: Self-driving version of grill-me. Interrogates a plan or design one question at a time, but for each question offers three answers (A/B/C) with one marked Recommended, then answers it itself by taking the recommended option — looping down the decision tree until the plan is fully resolved. Use when the user wants a plan stress-tested and auto-decided, says "auto-grill", "auto-grill this plan", "grill it and decide", or invokes /auto-grill.
---

# Auto Grill

Grill a plan relentlessly — but drive the interview yourself. Walk down each branch of the decision tree one question at a time. For every question, lay out three options and **take the recommended one automatically**, then move on. The output is a fully-resolved plan the user can review and override in one pass, instead of a slow back-and-forth.

## Find the plan

Grill the plan that already exists — in this conversation, a `PLAN.md`, an issue, or a PRD. If none is clear, ask what to grill. Never invent a plan.

## The loop

Repeat until the decision tree is resolved:

1. **Pick the next open question** — the most important unresolved decision, respecting dependencies (answer what later decisions hang on first).
2. **If the codebase can answer it, explore instead of asking.** Use the real answer; never guess what you can look up.
3. **Offer three answers**, labelled:
   - **A.** …
   - **B.** …
   - **C.** …
   Mark exactly one **✅ Recommended** and give a one-line reason.
4. **Answer it yourself** — take the recommended option and record it as the decision.
5. **Continue** to the next question, now informed by that decision.

Run on autopilot. Show every question, its three options, and the answer you picked, so the user can follow the reasoning and veto any choice.

## Stop when

- No meaningful open questions remain — what's left is trivial or cosmetic, or
- Further questions would not change the plan.

Do not loop forever. When decisions stop adding value, stop.

## Output

End with a clean recap so the user can review and override in one pass:

- **Decisions** — a numbered list of `Question → chosen answer (A/B/C)`, each with its one-line reason.
- **Resolved plan** — the plan rewritten with every decision baked in.
- **Override?** — invite the user to flip any letter; re-resolve anything downstream that depended on it.

## Rules

- One question at a time, dependency-ordered — never branch before resolving what it rests on.
- Exactly three options, exactly one recommended, every recommendation justified in one line.
- Recommend the option you would actually choose — not the safe-sounding one. Be opinionated.
- Explore the codebase over guessing whenever the answer lives there.
