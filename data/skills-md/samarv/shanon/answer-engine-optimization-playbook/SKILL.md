---
name: answer-engine-optimization-playbook
description: Strategies for getting products and content cited within LLM responses (ChatGPT, Perplexity, Claude). Use this when launching a new product, seeing referral traffic from AI agents, or trying to capture high-intent users who have moved from Google search to chat interfaces.
---

Answer Engine Optimization (AEO) is the practice of ensuring your product is cited as the primary answer in Large Language Models (LLMs). Unlike traditional SEO, which focuses on winning a "blue link," AEO focuses on being summarized as a top recommendation across multiple citations.

## The AEO Core Principles
*   **Mentions Over Ranking:** LLMs summarize multiple citations. To "win" an answer, you must be mentioned most frequently across the sources the LLM retrieves.
*   **The Long Tail is Back:** While Google searches average 6 words, LLM prompts average 25 words. Optimize for highly specific, conversational follow-up questions.
*   **Zero Domain Authority Barrier:** Early-stage startups can win AEO immediately by getting mentioned in a single trusted Reddit thread or YouTube video, bypassing the years of authority-building required for Google.

## Step-by-Step AEO Workflow

### 1. Identify High-Intent Questions
Move beyond keywords to full questions.
*   **Mine Sales/Support Data:** Identify the exact questions customers ask on calls or in support tickets. These reflect the "long tail" prompts they use in LLMs.
*   **Convert Paid Search Data:** Take your high-converting PPC keywords and use an LLM to "Turn these keywords into the 10 most common questions a buyer would ask."
*   **Target the "Follow-up":** Anticipate the second and third questions (e.g., "Does this integrate with Looker?", "What is the specific pricing for 50 seats?").

### 2. Optimize On-Site Content (The "Help Center" Strategy)
*   **Subdirectory vs. Subdomain:** Move all help center and documentation content to a subdirectory (e.g., `brand.com/help`) rather than a subdomain (`help.brand.com`) to consolidate authority.
*   **Information Gain Heuristic:** To avoid being filtered as "typical" AI spam, include original research, unique data points, or expert opinions that don't exist in other citations.
*   **Answer the Tail:** Create specific pages for obscure use cases (e.g., "How to use [Product] for [Specific Niche Use Case]"). These often become the sole citation for specific LLM queries.

### 3. Off-Site Citation Building
LLMs rely on Retrieval-Augmented Generation (RAG). You must appear in the "Search" results the LLM pulls.
*   **Reddit Strategy:** Identify active threads related to your category. Provide authentic, high-value answers. Disclose your identity ("I work at Webflow...") to maintain community trust and avoid being banned by anti-spam filters.
*   **YouTube/Vimeo:** Create videos for non-glamorous, high-LTV B2B keywords. LLMs frequently cite video transcripts for technical "how-to" questions.
*   **Tiered Affiliates:** Focus on "Listicle" sites (e.g., Dotdash Meredith, TechRadar, Forbes Advisor). If these sites mention you as #1, LLMs will likely summarize you as #1.

### 4. Setup AEO Tracking
LLM answers are non-deterministic; they change per run.
*   **Share of Voice (SoV):** Track what percentage of the time you appear in the "citation pill" for your top 50 questions.
*   **Distribution Tracking:** Ask the same question 5-10 times to see the distribution of answers.
*   **Post-Conversion Surveys:** Because LLM traffic often looks like "Direct" or "Branded Search" in analytics, ask every new sign-up: "How did you hear about us?" specifically looking for mentions of ChatGPT/Perplexity.

## Measuring Success via Experiments
Do not assume "best practices" work for your niche.
1.  Select 200 target questions.
2.  Split into a **Control Group** (100 questions, no action) and a **Test Group** (100 questions).
3.  Intervene on the Test Group (e.g., add Reddit comments, create YouTube videos, update help docs).
4.  Monitor "Share of Voice" for both groups over 4 weeks.
5.  Scale the tactics that show a statistically significant increase in mentions compared to the control.

## Examples

**Example 1: B2B SaaS Integration**
*   **Context:** A user asks Perplexity, "What meeting transcription tool has a Looker integration?"
*   **Input:** The product doesn't have a native integration, but can use Zapier.
*   **Application:** Create a help center article titled "Visualizing Meeting Sentiment in Looker via Zapier."
*   **Output:** Perplexity retrieves this specific page as the only relevant citation and tells the user: "You can use [Product] via a Zapier workaround to get data into Looker."

**Example 2: Local Marketplace**
*   **Context:** A user asks ChatGPT, "What's the best dog-friendly restaurant in Austin with live music?"
*   **Input:** Traditional SEO targets "Best restaurants Austin."
*   **Application:** Ensure the restaurant is mentioned in a Reddit thread "Dog friendly music spots Austin" and has "Dog Friendly" and "Live Music" tags in Schema.org markup on the site.
*   **Output:** ChatGPT summarizes these attributes and places the restaurant in a clickable "carousel" card at the top of the chat.

## Common Pitfalls
*   **Using 100% AI-Generated Content:** LLMs and search engines increasingly filter for "typicality." Pure AI content without a "human-in-the-loop" for editing and original data usually results in zero citations.
*   **Reddit Identity Faking:** Creating 100 fake accounts to "shill" a product. Communities and LLM search-evaluation teams detect this pattern easily, leading to domain-wide bans.
*   **Ignoring the Conversion Gap:** Thinking AEO isn't working because "Referral" traffic is low. Users often see the answer in ChatGPT, then open a new tab to search for the brand directly. Always use "How did you hear about us?" surveys.
*   **Focusing on RAG vs. Core Model:** Trying to "train" the model on your data. This is impossible for most. Focus entirely on the RAG (Search) citations, as this is what determines the real-time answer.