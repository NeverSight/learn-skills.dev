---
name: prompt-engineering
description: "Use this skill when crafting, reviewing, or improving prompts for LLM pipelines — including task prompts, system prompts, and LLM-as-Judge prompts. Triggers include: requests to write or refine a prompt, diagnose why an LLM produces inconsistent or incorrect outputs, bridge the gap between intent and model behavior, reduce ambiguity in instructions, add few-shot examples, structure complex prompts, or improve output formatting. Also use when the user needs help distinguishing specification failures (unclear instructions) from generalization failures (model limitations), or when iterating on prompts based on observed failure modes. Do NOT use for general coding tasks, document creation, or non-LLM writing."
---

# Prompt Engineering for LLM Pipelines

## Core Philosophy: Bridging the Two Gulfs

Effective prompt engineering is fundamentally about closing two gaps between human intent and model behavior. Understanding which gap you're dealing with determines whether prompt refinement will actually solve your problem.

### The Gulf of Specification (Developer → LLM)

This gulf separates **what you mean** from **what you actually wrote** in the prompt. Your intent — the task you want the LLM to perform — is often only loosely captured by the words you write. Specifying tasks precisely in natural language is surprisingly hard.

Even prompts that seem clear often leave crucial details unstated. For example:

> "Extract the sender's name and summarize the key requests in this email."

This sounds specific, but critical questions are left unanswered:
- Should the summary be a paragraph or a bulleted list?
- Should the sender be the display name, the full email address, or both?
- Should the summary include implicit requests, or only explicit ones?
- How concise or detailed should the summary be?

Without complete instructions, the model is forced to **guess** your true intent, producing inconsistent outputs. Underspecified prompts are usually a direct result of not looking at real data — you don't know what edge cases and ambiguities exist until you see them.

**Key insight**: Prompt clarity often matters as much as task complexity. Many teams rush to build evaluators for preferences they never specified in the prompt (like concise responses or a specific structure). The better approach is to first include such instructions explicitly, and only create an evaluator if the LLM still fails to follow them.

### The Gulf of Generalization (Data → LLM)

This gulf separates your data from the model's actual behavior across diverse inputs. Even if prompts are carefully written, LLMs may behave inconsistently on different inputs.

Example: An email processing pipeline might encounter an email mentioning a public figure like "Elon Musk" in the body. The model might mistakenly extract that name as the sender, even though it's unrelated to the actual email metadata. This is **not a prompting error** — it's a generalization failure where the model applies instructions incorrectly on unusual inputs.

The Gulf of Generalization will always exist to some degree. No model will ever be perfectly accurate on all inputs.

### Why This Distinction Matters

**Fix specification first, then measure generalization.** There are two reasons:

1. **Efficiency**: Many specification failures can be resolved rapidly by simply adding clarity or detail to an existing prompt. It's wasteful to build an automated evaluator for a failure mode that a prompt edit would fix.

2. **Measurement validity**: You want evaluations to reflect the LLM's ability to generalize from clear instructions, not its capacity to decipher your ambiguous intent. Evaluating poorly specified tasks essentially measures how well the LLM can "read your mind," which isn't reliable.

**Decision framework when you see a failure:**
- Ask: "Did I clearly specify what I wanted?" If no → fix the prompt (Specification issue).
- Ask: "Were the instructions clear but the model still got it wrong?" If yes → this is a Generalization issue worth building an evaluator for.

---

## Prompt Structure: Seven Components

A well-structured prompt typically includes several key pieces. Not every prompt needs all of them, but knowing the full toolkit helps you decide what's needed.

### 1. Role and Objective

Clearly define the persona or role the LLM should adopt and its overall goal. This sets the stage for desired behavior and helps guide tone and reasoning style, especially for open-ended tasks.

```
You are an expert technical writer tasked with explaining complex AI concepts to a non-technical audience.
```

```
You are a careful tax advisor reviewing client filings for potential issues.
```

### 2. Instructions / Response Rules

This is the core component. Provide clear, specific, and unambiguous directives. Modern models interpret instructions literally, so be explicit about what to do **and what not to do**.

Use bullet points or numbered lists for multiple instructions. For complex instruction sets, break them into sub-categories.

```
### Task
Summarize the following research paper abstract.

### Constraints
- The summary must be exactly three sentences long.
- Avoid using technical jargon above a high-school reading level.
- Do not include any personal opinions or interpretations.

### Tone and Style
- Use active voice.
- Write for a general audience.
```

### 3. Context

The relevant background information, data, or text the LLM needs. This could be a customer email, a document to summarize, a code snippet to debug, or user dialogue history.

When providing multiple documents or long context, **clear delimiters are crucial** (see Component 7).

```
<customer_email>
[Insert the full text of the customer email here]
</customer_email>
```

### 4. Examples (Few-Shot Prompting)

Provide one or more examples of desired input-output pairs. This is highly effective for guiding the model towards the correct format, style, and level of detail. Examples can also clarify nuanced instructions or demonstrate complex tool usage.

**Critical rule**: Ensure that any important behavior demonstrated in your examples is **also explicitly stated** in your rules/instructions. Examples illustrate; rules specify.

```
### Example

Input email:
"Hi team, can we move the Thursday standup to 2pm? Also, please review the Q3 deck before Friday."

Output:
{
  "sender": "Unknown (no signature)",
  "requests": [
    "Reschedule Thursday standup to 2pm",
    "Review Q3 deck before Friday"
  ],
  "urgency": "medium"
}
```

### 5. Reasoning Steps (Chain-of-Thought)

For complex problems, instruct the model to think step-by-step or outline a specific reasoning process. This encourages the model to break down the problem and leads to more accurate outputs.

```
Before generating the summary, first identify the main hypothesis, then list the key supporting evidence, and finally explain the primary conclusion. Then, write the summary.
```

### 6. Output Formatting Constraints

Explicitly define the desired structure, format, or constraints for the response. This is critical for programmatic use of the output.

```
Respond using only JSON format with the following keys:
- sender_name (string)
- main_issue (string) 
- suggested_action_items (array of strings)
```

```
Ensure your response is a single paragraph and ends with a question to the user.
```

### 7. Delimiters and Structure

Use clear delimiters (Markdown headers, triple backticks, XML tags) to separate different parts of your prompt. This helps the model understand distinct components, especially in long or complex prompts.

**Recommended organization for complex prompts:**
1. Overarching instructions or role definitions at the **beginning**
2. Context and examples in the **middle**
3. Reiterate key instructions or output format requirements at the **end**

**For cache efficiency**: Place static instructions **before** any user-provided or changing data. This maximizes KV cache reuse across requests and reduces inference cost.

---

## The Iterative Refinement Process

Finding the perfect prompt is rarely immediate. It's an iterative cycle:

1. **Write** a prompt
2. **Test** it on various inputs (especially real data when available)
3. **Analyze** the outputs — identify failure modes
4. **Classify** each failure: Specification or Generalization?
5. **Refine** the prompt for Specification failures
6. **Repeat**

### Important Warning on Prompt Optimization Tools

Avoid automated prompt-writing and optimization tools in the early stages of development. Writing the prompt yourself forces you to externalize your specification and clarify your thinking. People who delegate prompt writing to a black box too aggressively struggle to fully understand their failure modes. After you have experience looking at your data and understanding failures, you can introduce these tools — but do so carefully.

---

## Quick Wins for Prompt Improvement

When a prompt isn't working well, try these low-effort, high-impact changes first:

1. **Clarify ambiguous wording.** If the model gets confused about phrasing (e.g., "West Berkeley" vs. "Berkeley West"), update the prompt to be more explicit.

2. **Add a few examples.** Include 2–3 representative input/output pairs targeting observed failure cases.

3. **Use role-based guidance.** A persona like "You are a careful tax advisor..." can guide tone and reasoning, especially for open-ended tasks.

4. **Ask for step-by-step reasoning.** For tasks involving logic or multiple steps, explicitly asking the model to "think step by step" improves correctness and completeness.

5. **Specify what NOT to do.** Often, failures come from the model doing something you didn't want but also didn't explicitly prohibit.

6. **Break complex tasks into subtasks.** Instead of one massive prompt, decompose into sequential steps (extract → filter → summarize → format).

---

## LLM-as-Judge Prompt Design

When building automated evaluators that use an LLM to judge outputs, the same principles apply — but with additional structure. Each evaluator should target a **single failure mode** with a **binary Pass/Fail** judgment.

### Four Essential Components

1. **Clear task and evaluation criterion.** Focus on one well-scoped failure mode. Vague criteria lead to unreliable judgments. Instead of asking whether an email is "good," ask whether "the tone is appropriate for a luxury buyer persona."

2. **Precise Pass/Fail definitions.** Define exactly what counts as Pass (failure absent) and Fail (failure present), grounded in your observed failure descriptions.

3. **Few-shot examples.** Include labeled outputs that clearly Pass and clearly Fail. Draw these from human-labeled traces when possible. If using finer-grained scales (e.g., 1–3 severity), include examples for every point on the scale.

4. **Structured output format.** The judge should respond in a consistent, machine-readable format — typically JSON with `reasoning` (1–2 sentence explanation) and `answer` ("Pass" or "Fail").

### Example Judge Prompt

```
You are an expert evaluator assessing outputs from a real estate assistant chatbot.

Your Task: Determine if the assistant-generated email to a client uses a tone appropriate for the specified client persona.

Evaluation Criterion: Tone Appropriateness

Definition of Pass/Fail:
- Fail: The email's tone, language, or level of formality is inconsistent with or unsuitable for the described client persona.
- Pass: The email's tone, language, and formality align well with the client persona's expectations.

Client Personas Overview:
- Luxury Buyers: Expect polished, highly professional, and deferential language. Avoid slang or excessive casualness.
- First-Time Homebuyers: Benefit from a friendly, reassuring, and patient tone. Avoid overly complex jargon.
- Investors: Prefer concise, data-driven, and direct communication. Avoid effusiveness.

Output Format: Return your evaluation as a JSON object with two keys:
1. reasoning: A brief explanation (1-2 sentences) for your decision.
2. answer: Either "Pass" or "Fail".

Examples:
---
Input:
Client Persona: Luxury Buyer
Generated Email: "Hey there! Got some awesome listings for you. Super views, totally posh. Wanna check 'em out?"

Evaluation: {"reasoning": "Uses excessive slang and an overly casual tone unsuitable for a Luxury Buyer persona.", "answer": "Fail"}
---
Input:
Client Persona: First-Time Homebuyer
Generated Email: "Good morning! I've found a few properties that seem like a great fit for getting started in the market, keeping your budget in mind."

Evaluation: {"reasoning": "The tone is friendly, reassuring, and avoids jargon — appropriate for a first-time homebuyer.", "answer": "Pass"}
---

Now evaluate the following:

Client Persona: {persona}
Generated Email: {email}
```

---

## Anti-Patterns to Avoid

- **Vague instructions**: "Make it good" or "summarize well" — these force the model to guess your criteria.
- **Missing edge case handling**: Not specifying what to do when expected data is absent (e.g., no sender signature in an email).
- **Likert scales in evaluation**: Complex scoring scales (1-5) are harder to calibrate than binary Pass/Fail. Prefer binary judgments.
- **Examples without rules**: Demonstrating behavior in examples that isn't also stated in the instructions. The model may not generalize from examples alone.
- **Overly long monolithic prompts**: When a prompt exceeds a few hundred words, consider decomposing the task into steps.
- **Evaluating unspecified behavior**: Building evaluators for things you never told the model to do. Fix the prompt first.

---

## Workflow: Applying This Skill

When asked to help with a prompt, follow this process:

1. **Understand the task**: What is the LLM supposed to do? What data does it operate on?
2. **Identify the current failure**: Is the output wrong? Inconsistent? In the wrong format?
3. **Classify the failure**: Is this a Specification gap (unclear instructions) or a Generalization gap (model limitation)?
4. **For Specification failures**: Apply the seven components framework. Which components are missing or underspecified?
5. **For Generalization failures**: Consider task decomposition, adding examples targeting the failure case, or recommending an evaluator.
6. **Review against anti-patterns**: Check the prompt doesn't fall into common traps.
7. **Recommend iteration**: Suggest testing the revised prompt on diverse inputs, especially edge cases from real data.

When writing prompts from scratch, start with Components 1 (Role), 2 (Instructions), and 6 (Output Format) as the minimum viable prompt, then layer in Context, Examples, Reasoning Steps, and Delimiters as complexity demands.
