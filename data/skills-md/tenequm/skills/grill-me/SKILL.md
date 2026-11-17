---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
metadata:
  version: "0.1.4"
  categories: "agents, productivity"
  topics: "planning, design-review, stress-test, interviewing, decision-making"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/grill-me
    emoji: "🔥"
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Ask each question as plain text in your normal reply - never through a structured question/option-picker UI tool, even if one is available; options and your recommendation belong in the message body itself.

If a question can be answered by exploring the codebase, explore the codebase instead.
