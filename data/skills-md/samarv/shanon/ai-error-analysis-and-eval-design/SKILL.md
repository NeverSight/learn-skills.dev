---
name: ai-error-analysis-and-eval-design
description: A systematic workflow to move AI products beyond "vibe checks" by identifying specific failure modes and building automated LLM judges. Use this when your AI outputs feel "janky," when you need a feedback signal for prompt engineering, or when monitoring production performance at scale.
---

To build great AI products, you must transition from subjective "vibe checks" to systematic measurement. This process identifies exactly where an LLM is failing and creates a feedback loop for continuous improvement.

## Phase 1: Open Coding (The "Benevolent Dictator" Phase)
Before automating, you must manually ground yourself in the data. Appoint one "Benevolent Dictator"—typically the Product Manager or domain expert—to define "good" taste.

1.  **Sample the Data:** Extract 50–100 "traces" (logs of full LLM interactions) from your observability tool (e.g., Braintrust, LangSmith, Phoenix).
2.  **Note the Upstream Error:** Read each trace. If something is wrong, write a brief, informal note (an "Open Code") describing the first thing that went wrong.
    *   *Rule:* Don't overthink it. Use specific language (e.g., "hallucinated virtual tour," "didn't confirm call transfer") rather than just "bad."
3.  **Stop at Saturation:** Continue until you stop learning new ways the system fails (Theoretical Saturation).

## Phase 2: Axial Coding (Categorization)
Synthesize your mess of notes into actionable categories using an LLM.

1.  **Export Notes:** Put your open codes into a CSV or spreadsheet.
2.  **Synthesize Failure Modes:** Use an LLM (Claude or ChatGPT) to group your notes into 5–7 "Axial Codes" (failure categories).
    *   *Prompt Pattern:* "Analyze these manual notes from AI traces and group them into actionable failure categories (Axial Codes). Each category should represent a specific product problem."
3.  **Map Back:** Use a spreadsheet formula or LLM to categorize every trace into one of these buckets.
4.  **Prioritize:** Create a pivot table to count the frequency of each category. Focus your engineering efforts on the highest-frequency or highest-risk buckets.

## Phase 3: Build the "LLM as Judge"
For complex, subjective failures (like "human handoff quality"), create an automated evaluator.

1.  **Write the Judge Prompt:** Create a separate prompt for an LLM whose only job is to evaluate one specific failure mode.
2.  **Enforce Binary Scoring:** Require the judge to output only **True** or **False**.
    *   *Note:* Avoid 1–5 or 1–10 scales. They result in "weasel" metrics (e.g., a score of 3.7) that provide no clear direction for improvement.
3.  **Define Rules:** Include specific criteria from your "Benevolent Dictator" notes.
    *   *Example:* "Output True if the user explicitly asked for a human and the assistant responded with a tool call without acknowledging the request."

## Phase 4: Alignment & Validation
Never ship an eval until you know the judge matches human judgment.

1.  **Create an Agreement Matrix:** Compare the Judge's True/False labels against your manual labels from Phase 1.
2.  **Review Mismatches:** Specifically look at:
    *   **False Positives:** Judge said error, Human said no error.
    *   **False Negatives:** Human said error, Judge said no error.
3.  **Iterate:** Refine the Judge's prompt until it aligns with the "Benevolent Dictator" at least 80–90% of the time.

## Examples

**Example 1: Real Estate AI Assistant**
*   **Context:** AI is supposed to book apartment tours.
*   **Open Code:** "AI told the user a virtual tour was available when the property only offers in-person tours."
*   **Axial Code:** "Capability Misrepresentation."
*   **Judge Logic:** "Check the 'Property Context' tool output. If 'virtual_tour' is False, but the LLM response contains 'virtual tour,' output True (Error)."

**Example 2: Customer Support Handoff**
*   **Context:** AI should hand off to a human for sensitive issues.
*   **Open Code:** "User said they were frustrated with a leak, AI just gave a generic maintenance link."
*   **Axial Code:** "Handoff Protocol Violation."
*   **Judge Logic:** "Search for sentiment indicating frustration or emergency. If found, did the AI offer a human transfer? If no, output True (Error)."

## Common Pitfalls
*   **Likert Scales:** Using 1–5 scales makes it impossible to know if a change in score is meaningful. Use binary True/False.
*   **Automating Too Early:** Do not let an LLM do the initial "Open Coding." It lacks the product context to know what "janky" looks like for your specific business.
*   **Committee Judging:** Don't use a committee to define "good." Appoint one person with the best domain taste to be the final arbiter (The Benevolent Dictator).
*   **Chasing Generic Metrics:** Don't rely on generic evals like "hallucination score" or "cosine similarity." They rarely correlate with product-specific success.