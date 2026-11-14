---
name: expert-test
description: "Run the decision at hand through the best expert in its field, kill the choice that expert would reject, and state every trade-off."
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Expert test

Apply to the decision named in the arguments, or to every decision at hand.

For every decision, ask what the best expert in that field would do and why they would reject your current choice; if you can name that reason, don't make the choice. Optimize for what that expert would judge correct, never for what satisfies the stated constraints most cheaply. Every trade-off you take must be stated to the user, never absorbed.
