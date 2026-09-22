---
name: jev
description: Write and improve programs that call Jev, TypeSafe's System One model. Use when designing TypeSafe questions (Choice, Score, Noul), structuring state, composing answers in code, setting confidence thresholds, or diagnosing a Jev question that answers wrong or with low confidence.
---

# Writing and improving Jev programs

Jev is a judgment model. It reads one `state`, answers every question in the request independently and in parallel, and returns a probability distribution over the answers you defined. It does not reason in steps and it does not generate text. Code owns the control flow, the arithmetic, and the policy. Jev owns the snap judgments.

A good Jev question is one a knowledgeable person answers in a second, given the right context. "Does this message convey urgency?" fits. "Analyze this message and decide what to do" does not fit. Break that task into small questions and compose the answers in code.

This guidance applies to `jev-1.13`. The docs mark several limits as likely to improve in later versions, so recheck the jaggedness page when the model changes.

## Workflow

1. List the decisions your code must make. Write each as a branch, a threshold, or a ranking.
2. Write one question per judgment. Split any question that weighs two properties.
3. Pick the primitive whose answer your code acts on directly.
4. Build the smallest state that answers every question. Compute in code whatever code can compute.
5. Put every question that shares the state into one request, including questions that matter for only some inputs.
6. Combine the answers in code: branches, weights, and confidence gates.
7. Test against labeled examples. Read `probabilities` on the misses, then revise one or two questions at a time.

## Choose the primitive

| Primitive | Use it when | Returns | Code acts on it with |
| --- | --- | --- | --- |
| Choice | The answer is one of a known set with no order | `choice`, `probabilities`, `confidence` | a branch per option |
| Score | The answer is a position on a spectrum you can describe in steps | `score`, `probabilities`, `confidence`, `legend` | a threshold, a rank, or a weight |
| Noul | The answer is a clean yes or no and the probability is the signal | `noul`, from 0 to 1 | an `if` on a threshold |

- Add an `other` or `none of the above` option to a Choice whose list may not cover every input.
- A Noul of 0.5 means Jev is unsure. It does not mean "medium". Use a Score to measure a degree.
- A Noul needs a crisp condition. "Is this candidate strong in Python?" is vague. "Does the resume state that the candidate used Python at work?" is crisp.
- Use a Choice or several Nouls when the answer has no in-between.

## Write the instructions

- State the exact condition. Jev answers the words you wrote. It reads scoping words, negations, and implied conditions at face value.
- Ask one property per question. Hidden second judgments lower accuracy and confidence.
- Name the part of the state the question judges, with a backticked path: `` `ticket.messages[0].text` ``.
- Write directly. Avoid double negatives, a property of a property, and any question that needs several hops.
- Keep numerals that stand for levels out of the instructions. "Rate from 0 to 2" gives Jev nothing to match.
- Write the full question in `instructions`. The question ID never reaches the model.
- Keep decision policy out of the question. "A shared address cannot override a name conflict" belongs in code.
- When you explain what you really meant after a wrong answer, that explanation is the missing half of the instruction. Add it.

Instructions accept a string, an object, or an array. Use an object when the question has labeled parts or needs supporting data. Pass a schema, taxonomy, or row as JSON. Do not serialize it into a string template.

```json
"instructions": {
  "question": "Does the `message` ask the recipient to disclose a sensitive credential?",
  "inspect": "message",
  "focus": "Look for a request to send the credential itself, not a request to change or reset it."
}
```

Useful keys from the docs: `question`, `focus`, `inspect`, `note`, `compare` (a list of state paths), and `field` (a `name`, `type`, `unit`, `description` record that several questions share).

## Write the criteria

Treat criteria as an extension of the instruction. The two must ask for the same thing, in the same direction. A Noul whose `true` side describes "no" performs worse.

**Choice.** Map each option to a description. Make the descriptions contrastive when options sit close together:

```json
"billing": {
  "what": "Charges, invoices, refunds, or subscriptions",
  "not_for": "Order tracking or account access",
  "examples": ["I was charged twice", "Where is my refund?"]
}
```

**Score.** List the levels from low to high. Use two to ten levels, and only as many as you can describe distinctly.

- Describe situations. "Broken feature, but a workaround exists" works. "Moderately severe" does not.
- Make each level stand alone. Jev judges each level separately and sees neither its number nor its neighbors. "Worse than the previous level" means nothing to it.
- Keep each Score to one dimension. "Punctual and smart and experienced" measures three things.
- Give a rare extreme its own level when your code must treat it differently.
- A level may be an object: `{"summary": "One change, clearly stated", "signals": ["A single fix or feature", "..."]}`.

**Noul.** Criteria are optional. Add `true` and `false` sides, each with `what` and `examples`, when the boundary is subtle. Put the neighboring case in the description of the side it belongs to.

**Examples.** Write short concrete instances, such as "I was charged twice". Do not write a description of an instance, such as "a message about a billing problem".

## Build the state

- Send only the fields the questions need. Unrelated detail lowers accuracy, and a large state hides which input caused a wrong answer.
- Retrieve and filter in code first. When code cannot filter, ask a relevance Noul per passage and keep the passages that pass.
- Keep the state structured so questions can point into it by path.
- Convert numeric encodings to words before sending them. Send a color name in place of a hex value. Send a computed number or a named bucket in place of raw figures.
- Compute date order, duration, windows, counts, and sums in code. Send the result.
- Budget: the state and all questions share 64k tokens. The state plus the longest single question must fit in 32k tokens.
- Treat text in the state as able to steer the answer. Jev does not treat state as hostile. State in the criteria what counts, and test injected and self-describing content before deployment.

## Compose the answers in code

**Speculative fan-out.** Ask every question your code might need in one request, including questions that matter only on some branches. Questions run in parallel, so extra questions add little latency and few tokens. Code ignores the answers it does not need.

**Second requests.** Make a second request only when code cannot build it without the first answer, such as when the answer decides what data to fetch. Questions in one request never see each other's answers.

**Confidence-gated routing.** The answer says what. Confidence says whether to act. Set a floor below which no action runs, then set a threshold per action that rises with the cost of a wrong call. The docs use floors of 0.5 to 0.6 and 0.85 to 0.9 for high-stakes actions. Start conservative and tune on your data. The three standard paths are: act, confirm or flag, and hand off.

**Composite scoring.** Split a complex judgment into one Score per dimension. Normalize each score by `len(criteria) - 1`, then combine with weights in code. Change a weight when priorities shift. Do not rewrite a question to change policy.

**Intent routing.** Classify with a Choice, and add a complexity Score beside it. Route each intent to deterministic code, a specialist LLM, or a person. Send low-confidence classifications to a person.

**Taxonomy walk.** Ask one Choice per tree level and walk the tree in code. Give each option its subtree as the criteria value, so Jev sees what lives under a branch. Trim large subtrees to direct children and a sample of leaves. Follow several branches when the probabilities are close.

**Counting.** Jev does not count. Ask one Noul per item in a single request, then sum the answers that pass your threshold.

**Dates.** Extract each date part with a Choice over enumerated options, including a "not stated" option. Assemble and compare the date in code.

**Extraction.** Generate candidates with a regex or a generative model. Ask Jev to pick among them with a Choice, or to verify one with a Noul.

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

SEVERITY = [
    "Cosmetic; no impact to functionality",
    "Broken or degraded feature; a workaround exists",
    "Blocking issue; no workaround exists",
]

with TypeSafeClient() as client:
    response = client.system_one(
        state={"ticket": ticket_text},
        questions={
            "category": Choice(
                instructions="Which category fits the main request in `ticket`?",
                criteria={
                    "bug_report": "Something is broken or producing errors",
                    "billing": "Charges, invoices, refunds, or subscriptions",
                    "other": "Anything else",
                },
            ),
            # Speculative: only used when the ticket is a bug report.
            "severity": Score(instructions="How severe is the issue reported in `ticket`?", criteria=SEVERITY),
            "refund_requested": Noul(instructions="Does `ticket` explicitly ask for a refund or credit?"),
        },
    )

category = response.answers["category"]
severity = response.answers["severity"]
if category.confidence < 0.6:
    route_to_human(ticket_id)
elif category.choice == "bug_report":
    normalized = severity.score / (len(SEVERITY) - 1)
    if normalized > 0.75 and severity.confidence > 0.5:
        escalate(ticket_id)
    else:
        add_to_backlog(ticket_id)
elif category.choice == "billing" and response.answers["refund_requested"].noul > 0.7:
    route_to_billing(ticket_id, refund_likely=True)
```

## Read the answers

- `score` is the probability-weighted mean of the level numbers. A score of 1.0 can mean certainty on level 1 or an even split between levels 0 and 2. Read `probabilities` with it.
- Threshold a score, rank by it, or round it to the nearest level. Do not interpolate a quantity from it. Jev's levels are weakly calibrated as numbers.
- `confidence` measures how peaked the distribution is. It describes the model's answer and does not guarantee a correct one. The full `probabilities` are there when you need a different statistic.
- A Noul has no `confidence`. Its distance from 0.5 plays that role.
- Every answer stays inside the options you supplied, so code never parses prose.

## Improve a program

Find the question that fails before changing anything. Collect labeled examples, run them, and compare each question's answers and probabilities against the labels.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Wrong answers with high confidence | Jev read the instruction literally | State the exact condition. Put the boundary case in the criteria. |
| Low confidence on a Choice | Options overlap, or no option fits | Add `what`, `not_for`, and `examples`. Add an `other` option. |
| Low confidence on a Score | Levels overlap, the question measures two things, or the state says too little | Rewrite levels as distinct situations. Split the question. Add the missing field to the state. |
| Scores cluster in the middle | Levels are degrees or numbers | Describe a concrete situation per level. Remove numerals. |
| Top-of-scale cases look alike | The extreme case has no level | Add a level for the extreme. |
| A Noul hovers near 0.5 | The condition is vague | Define the condition. Add `true` and `false` criteria with examples. |
| Accuracy falls as inputs grow | The state carries irrelevant detail | Filter in code. Send only the needed fields. |
| Errors on counts, sums, dates, or numeric nearness | Jev is doing arithmetic | Move the arithmetic to code. Ask Jev only for extraction or per-item judgments. |
| Errors on nested or negated questions | Too much indirection | Ask the direct question. Name the state path. Split into two literal questions and combine in code. |
| The answer follows text inside the state | The content steers the model | Tighten the criteria. Test adversarial cases. Gate the action on confidence. |
| Rewording one question trades one error for another | One question weighs several properties | Split it into atomic questions and combine them in code. |
| The final decision is wrong while each answer is right | The policy is wrong | Change the weights or thresholds in code. Leave the questions alone. |
| The program is slow or costly | Questions are spread over sequential calls | Merge them into one request. Keep a second request only when it truly depends on the first answer. |

Rules for revising:

- Change one or two questions per revision. Jev's probabilities shift in ways that are hard to predict, so leave questions that discriminate well untouched.
- Judge a revision on labeled data. Higher confidence alone does not show a better question, and two wordings of one scale can behave differently on your data.
- Keep the answer space stable once code depends on it. Adding or removing a level or an option changes what every earlier answer meant.
- Write general rules in instructions and criteria. Put specific names and values only in `examples`.

## Checklist

- [ ] Each question asks one property and a person could answer it in a second.
- [ ] The primitive matches how code uses the answer.
- [ ] Instructions state the exact condition and name state paths in backticks.
- [ ] Criteria agree with the instructions and point the same direction.
- [ ] Score levels describe situations, stand alone, and carry no numerals.
- [ ] Choices that may not cover every input have an `other` option.
- [ ] Code does all counting, arithmetic, and date comparison.
- [ ] The state holds only what the questions need and fits the token limits.
- [ ] All questions on the same state travel in one request.
- [ ] Every action has a confidence threshold matched to its risk, and low confidence has a fallback.
- [ ] Weights and thresholds live in code.
- [ ] Labeled examples back every revision.

## Sources

- https://docs.typesafe.ai/model-jaggedness/jev-1.13
- https://docs.typesafe.ai/primitives/advanced
- https://docs.typesafe.ai/patterns, with `/fan-out`, `/confidence-routing`, `/composite-scoring`, and `/intent-routing`
- https://docs.typesafe.ai/primitives, https://docs.typesafe.ai/primitives/score, and https://docs.typesafe.ai/confidence, which the patterns pages assume
- https://docs.typesafe.ai/llms.txt lists every page. Append `.md` to a docs URL for raw markdown.
