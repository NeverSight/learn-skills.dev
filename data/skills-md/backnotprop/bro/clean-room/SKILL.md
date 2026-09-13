---
name: clean-room
description: >-
  Get an independent decision from a fresh agent that receives a neutral brief
  and none of the current conversation. 
disable-model-invocation: true
---

# Clean room

Launch a smart, independent agent to give us an unbiased third-party decision analysis.

You carry this conversation's bias. Write a neutral brief, start a fresh agent, and return its verdict without steering it.

1. Frame one decision per run. Separate “should we” from “how should we.”
2. Start a new agent, task, thread, pane, or session with no inherited conversation.
   - Use the most capable isolated option at your disposal.
   - Prefer a smarter agent when the decision is complex, consequential, or difficult to reverse.
   - Never use a fork, continuation, or handoff that copies this conversation.
   - Start every rerun fresh. Do not include a previous clean-room verdict.
3. Give the agent only the context needed to make the decision.
   - Include verified facts, fixed constraints, open questions, and enough direct evidence to check your summary.
   - Remove opinions, prior conclusions, sentiment, leading language, and clues about the preferred answer.
   - Present the known choices fairly, including “recommend against” or “no action.”
   - Pass the brief through a bias filter: could a reader guess the hoped-for answer? If yes, rewrite it.
4. Tell the agent to think independently, challenge any premise(s), consider other choices, and search for evidence against its conclusion.
   - Let it gather missing facts. Prefer direct sources; use other sources to fill factual gaps, label unverified claims, and take observations rather than opinions.
   - Require one verdict, its reasons, the strongest opposing case, why that case loses, and what would change the verdict. Do not accept “it depends.”
   - Ensure your instructions do not reward reaching an expected answer or encourage the agent to seek context that reveals prior preferences or conclusions unless that context is required for the decision.
5. Return the response unchanged, even when it contradicts you or the user.
   - Check the verdict for unsupported assumptions. If one drives the answer, correct the neutral brief and rerun with a fresh agent.
