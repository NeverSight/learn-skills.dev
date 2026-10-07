---
name: melech-consult
description: Get an independent verdict on an AI-proposed plan, fix, architecture, or claim by verifying its premises against the real artifact, then dispatching a panel of fresh models from different providers that answer independently. Use for "double check", "proof this", "are you sure", "second opinion", "am I right or is he right", "this still isn't working", or "not sure this is the right approach".
disable-model-invocation: true
---

# Consult

Asking the *same* thread *"are you sure?"* fails. It self-grades, it is trapped in the assumptions that produced the proposal, and it agrees with whatever direction was already discussed.

Consult buys back independence. It is a **machloket l'shem shamayim** — disagreement in service of what is true and useful, not winning — but the disagreement has to be earned by looking, not staged by assigning sides.

You are the clerk, not a party. Verify what can be verified, get real independent reads, then deliver a **psak**: the answer, what it costs, and the one thing to do next.

---

## When Consult Gets Invoked

Always by a deliberate human act, mid-flow, with someone waiting. Usually terse, often irritated:

- *"double check this plan before we build"* / *"proof this"* / *"are you sure?"*
- *"it's still bad, something isn't working"*
- *"not sure that's the correct approach"*
- *"am I right or is he right?"*
- *"what should we do before continuing?"*

Read that as **the developer has lost confidence in this thread** and wants escape velocity — a fact or a verdict. It is rarely a request for a symposium.

Infer the target from the thread and the files. State your reading in one line and proceed. Do not open with a list of clarifying questions; the human is mid-task. Ask at most one question, and only if you genuinely cannot identify what is being questioned.

**Refuse cheaply.** If the answer is knowable in a couple of tool calls, or there is one obviously right answer, say so and answer it. `"This doesn't need a panel — [answer]."` Spending five agents on a settled question is the failure mode users notice first.

---

## Non-Negotiables

These four rules are the skill. Everything below is procedure.

1. **Consultants get the artifact, never the narration.** Send the file, diff, page, log, or schema plus the question and the hard constraints. Never send the conversation, your summary of it, or your proposed answer. Pasting thread history is how you get three models agreeing with a mistake and mistake it for corroboration.
2. **Verify before you consult.** Any premise that decides the outcome and is checkable now gets checked against code, data, or logs. Report which premises were **verified** and which remain **assumed**.
3. **Nobody is assigned a side.** Each consultant answers the question and says what it actually concludes. Assigned advocacy destroys the only signal worth having.
4. **Different models from different providers.** Same-model panels share blind spots and produce confident agreement on shared errors. Never `inherit`. Never the model that authored the proposal, when known.

---

## Workflow

### 1. Name the target

One line: what specifically is in doubt, and who holds which position — the AI's proposal, the user's position, a colleague's position, or a claim about how the system behaves.

If two humans disagree, record both positions in their own words. Do not merge them into one axis; that conflation is how a consult ends up restating someone's own view back to them.

Also name **what has to leave the room**: a decision, a fact, a fix, a comment to post, a measurement. The answer is shaped by the deliverable.

### 2. Ground it

Before framing anything, spend a few tool calls on the premises the answer turns on. Read the code path the proposal assumes. Check whether the constraint actually holds. Look at the data instead of estimating it.

External facts are the only thing that breaks correlated model error. Models arguing with each other cannot get you out of a shared wrong belief; evidence can.

**Consult may end here**, and often should: *"Your premise is wrong — here's the evidence. The question dissolves."* That is the best available outcome, not a fallback.

### 3. Build the packet

One neutral packet, identical for every consultant:

- **Question** — the decision or claim, stated without a preferred answer.
- **Artifact** — the actual code, diff, doc, or data. Inline it or give exact paths.
- **Verified facts** — what grounding established, with how it was established.
- **Hard constraints** — invariants, compatibility, deadlines, scale.
- **Already ruled out** — with the reason, so nobody re-proposes it.

Never lead the witness.

- **DON'T**: *"I proposed a Redis queue because it's fast — good idea?"*
- **DO**: *"Durable task execution under constraints [X, Y]. Volume measured at 900 jobs/day (verified, see logs). What should this use, and why?"*

### 4. Dispatch the panel

**Default — three consultants, concurrently, in one call.** Different providers. Isolated; no consultant sees another's answer. Each returns:

1. Its answer, and the reasoning that produced it.
2. Whether it rejects the question's framing, and why — this is explicitly invited.
3. **Confidence, 1–10**, and the one thing that would change it.
4. The strongest case against its own answer.

Optionally give each a distinct **reasoning method** to decorrelate further — one inverts (assume it shipped and broke, trace back), one decomposes (list the load-bearing assumptions, test each), one traces dependencies and base rates (what blocks what, how have similar efforts actually gone). Methods and models decorrelate; personas and job titles do not.

Every consultant prompt carries: *"Do not defer to the answer the framing seems to expect. Reason to wherever it leads. If your conclusion is that the question is wrong, say that."*

**Escalate only on disagreement.** If the three converge, stop — that convergence is your evidence. If they split materially, spawn **one** devil's advocate on a strong model, aimed at the *emerging* answer: *"The panel is converging on X. Make the strongest case that following X is a mistake. Name the one thing that, if unrebutted, should change the verdict."* Then rebut or concede it explicitly.

**Weaker configurations, honestly labeled:**

| Situation | Do | Call it |
|---|---|---|
| Only one fresh provider available | One fresh model, one read | single-model second opinion |
| No subagents available | Reason it out in-thread | thread-local — does not solve self-grading bias |
| Panel is same-model | Run it, flag it | shared-blind-spot panel, not independent corroboration |

A weaker honest consultation beats a fake independent one. Report the actual dispatch — which models answered, and whether provider independence was achieved. Never imply independence you did not get.

### 5. Answer

Lead with the claim. Scale length to the question — a naming call gets a paragraph, a migration gets the full treatment. Pick the shape the finding earned:

**Settled by evidence** — grounding or the panel resolved it.
> The claim, the evidence that settles it, what to do now.

**Panel converged** — all consultants landed together.
> The answer. Confidence, and whether it was unanimous or weighted. What would have to be true for this to be wrong. The one next step.

**Split on a fact** — they disagree about what is true.
> The competing claims, the measurement that separates them, and the result if it was cheap enough to just go take. Do not turn a factual gap into a philosophical dispute.

**Split on values** — a real tradeoff; both paths satisfy the requirements.
> The tension in one sentence. Each position with what it protects and the price it accepts. The psak for present constraints. What you give up by taking it. The observable condition that should reopen it.

Always close with **one** concrete next action, and — where it applies — how to tell later whether the call was right.

Report agreement honestly. If the panel converged only because it shared an assumption, say so and downgrade confidence. Unanimity on a shared blind spot is not strength.

The user still rules. A psak is a recommendation, not permission to implement.

---

## Do / Don't

**Do:**
- Answer directly and skip the panel when the question doesn't need one.
- Verify the load-bearing premises first, and label verified versus assumed.
- Send artifacts; withhold the thread.
- Let consultants reject the question and propose an option nobody named.
- Require calibrated confidence and weight it over eloquence and length.
- Escalate to a devil's advocate only after an answer emerges, and aim it at that answer.
- Disclose the real dispatch, including when independence failed.

**Don't:**
- Assign anyone a side to defend.
- Paste conversation history into consultant prompts.
- Reuse the author's model, duplicate models, or `inherit`, then call it independent.
- Manufacture a two-sided tradeoff when evidence settles it, or when the honest answer is "we don't know yet — go measure."
- Present a hedge as a verdict, or bury the answer under structure.
- Dump raw subagent transcripts into the chat.
- Run five agents on a question one grep would have closed.
