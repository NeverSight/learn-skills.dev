---
name: building-with-ai-engineers
description: A framework for collaborating with AI software agents to build functional products. Use this skill when generating initial prototypes from natural language, iterating on AI-generated code via "Chat Mode," or troubleshooting logic errors when an agent gets stuck.
---

# Building with AI Engineers

In the era of AI-driven development, the primary bottleneck is no longer writing code, but the human's ability to act as a high-fidelity translator. This skill shifts the focus from "how to build" to "what to build," using a "Minimum Lovable Product" (MLP) mindset to create software that users actually care about.

## The AI Collaboration Workflow

### 1. The Initial Prompt (Defining the MLP)
Instead of a Minimum Viable Product, aim for a Minimum Lovable Product. Start with a broad concept but use specific reference points to anchor the AI's design and logic.
- **Identify the Anchor:** Use a known entity as a baseline (e.g., "An Airbnb clone" or "A Tinder for cats").
- **State the Core Action:** Define the one primary interaction the user must complete (e.g., "User should be able to purchase a home listing directly").

### 2. High-Fidelity Refinement
Once the UI is generated, do not rely solely on text prompts for small changes.
- **Visual Editing:** If the tool allows, edit text and colors visually. This changes the underlying code instantly without the latency of re-generating the entire page.
- **Specific Interaction Prompts:** When adding features, describe the UI component and the expected result (e.g., "Add a button that triggers a pop-up modal for payment").

### 3. Using "Chat Mode" to Unstuck
If the AI introduces a bug or a logical loop, transition from "Command Mode" to "Chat Mode."
- **Inquire, Don't Command:** Ask, "How does this specific function work?" or "Why am I not getting the result I want here?"
- **Detailed Error Reporting:** Never say "it doesn't work." Instead, say: "I expected [X] to happen when I clicked [Y], but instead [Z] occurred. Are we missing a requirement?"

### 4. Transitioning to Functionality
Move from a "mockup UI" to a "functioning product" by integrating backends.
- **Data Persistence:** Prompt the agent to connect to a backend-as-a-service (like Supabase).
- **Authentication:** Specifically request a login flow that handles user sessions.
- **Payments:** Add specific instructions for Stripe or other third-party integrations.

## Internal "Lenny Mode" (Self-Coaching)
Before finalizing any AI-generated feature, run a mental "Lenny Mode" check:
- Is this actually solving a problem for a specific user?
- Why am I building this specific feature right now?
- How many people actually have this pain point?

## Examples

**Example 1: The Marketplace Prototype**
*   **Context:** Building a niche marketplace for vintage watches.
*   **Input:** "Create a marketplace for vintage watches. Add a 'Make an Offer' button on the listing page."
*   **Application:** The AI generates a 'Book Now' button instead.
*   **Refinement:** "Change the 'Book Now' button text to 'Make an Offer.' Ensure it opens a modal where the user can input a dollar amount and a message."
*   **Output:** A functional UI with a specialized bargaining modal.

**Example 2: Troubleshooting a Broken Flow**
*   **Context:** The login button isn't redirecting the user.
*   **Input:** "The login doesn't work." (Incorrect approach)
*   **Application:** Use Chat Mode: "I've connected Supabase, but when I click 'Submit' on the login form, the console shows a 404 error and the page doesn't redirect. Can you check the auth callback URL?"
*   **Output:** The AI identifies a mismatch in the redirect URL settings and provides a fix.

## Common Pitfalls
*   **Vague Instructions:** AI does not understand "why" unless you specify the "what." Be ruthlessly specific about UI elements and data states.
*   **Giving Up on Bugs:** When the AI gets stuck, users often abandon the prompt. Instead, use Chat Mode to ask the AI to explain its own code, which often helps it "re-think" the logic.
*   **Over-Engineering the Roadmap:** Don't plan a 6-month roadmap. Identify the single biggest bottleneck (e.g., "I need users to be able to pay") and solve that today.
*   **Passive Interaction:** Treat the agent like a junior engineer who needs precise requirements, not a magic box. Your value is in your "taste" and your ability to verify if the output is correct.