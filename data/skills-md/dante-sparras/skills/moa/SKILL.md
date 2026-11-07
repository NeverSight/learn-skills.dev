---
name: moa
description: "Mixture of Agents: send one task to several independent proposer agents, possibly on different models, then aggregate their answers into one. For reviews, designs, plans, hard bugs, and choosing between patches."
disable-model-invocation: true
---

# Mixture of Agents

Several **proposers** answer the same task without seeing each other. One **aggregator** reads every proposal and writes the final answer. The gain comes from a strong aggregator that can read several good attempts; it fades when weak proposals dilute the pool.

You are the aggregator unless the user names another model for that seat.

## Arguments

Read these from what the user typed after the skill name. Anything not given takes its default.

| Argument | Default | Example |
| --- | --- | --- |
| Task | The task under discussion in this conversation | `review this branch`, `why does login hang` |
| Mode | From the table in step 2 | `pick`, `critique` |
| Proposers | Step 3 | `with grok, gpt, opus`, `5 proposers` |
| Aggregator | You | `aggregate with gpt-5.5` |
| Rounds | 1 | `2 rounds`, or "deeper". Never more than 2. |

## 1. Build the packet

Proposers start with no history: the **packet** is everything they get. Gather it once and send the same packet to every proposer, so they disagree about approach rather than about facts.

- The task, in the user's words, plus what you know they want from it.
- Constraints: conventions from `AGENTS.md`/`CLAUDE.md`, scope limits, what's already been ruled out.
- Pointers to the material: file paths, the diff command (`git diff main...HEAD`), the failing command and its error, the test command. Proposers share the checkout and can read files themselves; paste only what they can't reach, such as output from this conversation.
- The output shape for the mode, from [references/prompts.md](references/prompts.md).

**Done when** a proposer could do the task from the packet alone, without this conversation.

## 2. Pick the mode

| Mode | Use for | Aggregation |
| --- | --- | --- |
| `synthesize` | Designs, plans, reviews, explanations, open questions | Merge into one answer, leaning on the strongest proposals |
| `pick` | One code change that must apply cleanly: a bugfix, a refactor, a small feature | Check every candidate, then choose one whole patch. Never stitch patches together. |
| `critique` | Hard bugs, risky designs | Proposers each give a hypothesis or design; a second wave attacks each one; synthesize what survives |

When the task fits two modes, prefer `pick` for anything that ends in a code change, and `critique` when a wrong answer is expensive.

## 3. Choose the proposers

Default to **3 proposers**. More than 3 only when the user asks; the gain past 3 is a few points at double the cost.

- **The user named models:** use exactly those.
- **Otherwise, the default trio:**

  | Model | Reasoning effort |
  | --- | --- |
  | Grok 4.7 (`grok-4.7`) | high |
  | GPT 6.1 Sol (`gpt-6.1-sol`) | xhigh |
  | Opus 5.5 (`claude-opus-5-5`) | xhigh |

  Set each model's effort through its provider's option, as [references/spawning.md](references/spawning.md) describes for your host. A default model the host can't run gets replaced by your own model; name the swap in the report. With no model choice at all, all 3 seats are your own model: that's **Self-MoA**, which holds up well when one model is clearly the strongest.

**Done when** every proposer seat has a model, and you can say why each one is there.

## 4. Run the proposers

Launch every proposer at once, in parallel, as [references/spawning.md](references/spawning.md) describes for your host. Each gets the packet and its mode's proposer prompt from [references/prompts.md](references/prompts.md), and nothing from the other proposers.

Proposers leave the shared checkout untouched. In `pick` mode each one works in its own worktree when the host can isolate one, and runs the checks there; otherwise it returns its change as a unified diff in its final message.

If a proposer fails or stalls, aggregate the ones that came back and name the missing one in the report. With fewer than 2 proposals, there is nothing to mix: tell the user, and offer to rerun or to continue with the single answer.

**Done when** every proposer has returned a result or failed, and you hold every proposal verbatim.

## 5. Check and critique

- **`pick`:** every candidate must be checked before you compare them. Where a proposer could not run the checks, apply its diff to a clean tree (`git stash` your own changes first, or use a scratch worktree), run the project's tests, typecheck, and lint, record the result, and restore the tree. A candidate that fails a check that passes on the base drops out.
- **`critique`:** launch a second wave, one critic per proposal, each a different model from that proposal's author where possible. Each critic gets the packet, one proposal, and the critique prompt. Collect the critiques the same way as in step 4.
- **`synthesize`:** nothing to run. Where proposals contradict on a fact you can check (what a function returns, whether a test passes, what a dependency's API is), check it now.

**Done when** every checkable claim the proposals disagree on has a result.

## 6. Aggregate

Use the aggregator prompt for the mode in [references/prompts.md](references/prompts.md). If you are the aggregator, apply it to yourself; if the user named another model, send it that prompt with the original task as a separate message and every proposal, critique, and check result.

Disagreements:

- **Checkable:** the check from step 5 decides. Proposals don't outvote a test.
- **Not checkable** (an API shape, where a boundary goes): pick one with a stated reason, and name what you rejected. A blend that no proposer proposed is the failure to avoid.
- **Unanimous:** still not proof. When the task has a trace or a test, trust that over the agreement.

**2 rounds:** before the final aggregation, send every proposer the packet plus all first-round proposals and the aggregator prompt, so each writes a refined answer. Then aggregate those.

## 7. Report

1. The answer: the synthesis, the chosen patch (apply it now, in the user's checkout), or the surviving hypothesis.
2. One line per proposer: its model, its position in a few words, and whether the answer used it.
3. Disagreements and how each was settled.
4. Proposers that were missing, and checks that couldn't run.
5. Where the raw proposals live (thread links, or a path), so the user can read one in full.
