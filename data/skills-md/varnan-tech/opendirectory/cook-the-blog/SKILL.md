---
name: cook-the-blog
description: "Generate high-converting, deep-dive growth case studies in MDX format. Use this skill when asked to write a case study or blog post about a company's growth, tech stack, or product-led strategy. It handles the full pipeline (researching the company via Tavily, generating a 16:9 cover image, quality checking the draft, uploading assets to cloud storage, and pushing directly to the target repository)."
author: OpenDirectory
version: 1.0.0
---

# cook-the-blog Workflow

Follow these steps exactly when asked to generate a case study for a company.

**MANDATORY SETUP CHECK:** Before starting, ensure you have the required environment variables and target destinations configured (Target Repo, Image Bucket/Storage, Author Email, etc.). If any are missing, STOP and ask the user for them.

**MANDATORY QA CHECK AT EACH STEP:** After completing every single step below, you MUST perform a strict, self-critical QA check. If a step fails or is hallucinated, you MUST retry until it succeeds. Do not fake success.

## 1. Deep Research (Tavily)
- Use the `tavily` tool (via MCP) and standard web searches to deeply research the company. **Note:** Always check if the registered business name differs from the product name. Search Reddit and other relevant forums for authentic developer insights.
- **QA Tester:** Did you actually extract real, hard metrics and specific details about their GTM strategy, or is it generic fluff? If fluff, research deeper.

## 2. SEO Keyword Research (Google Trends via SerpApi)
- Run the python script: `export SERPAPI_KEY="[YOUR_SERPAPI_KEY]" && python3 [PATH_TO_SEO_SCRIPT] "[Company Name]"`
- Identify the breakout and high-growth keywords from the output.
- **QA Tester:** Did the script succeed? Are the keywords real and high-volume? If not, retry or adjust the query.

## 3. Title & Cover Generation
- **Title:** Format: `"How [Company] [Achieved X] by [Core Strategy]"`. Make it specific and highly descriptive.
- **Cover:** Use the `blog-cover-cli generate` command to generate the cover image. **CRITICAL: The title passed to the cover image generator using the `-t` flag should contain around 7-10 words total. Do NOT use newlines (`\n`) in the string. Just provide a normal, single-line string and let the CLI handle the text wrapping automatically! Write a concise, aggressive title (e.g., `blog-cover-cli generate -t "How Baseten Scaled AI Infrastructure To a 5 Billion Valuation" -l "domain.com" -o "./cover.png"`).**
- **QA Tester:** Was the image actually generated and saved? Verify the file exists.

## 4. MDX Assembly
Synthesize the research and write the case study in a strict MDX format.
**Writing Rules (Use the `stop-slop` skill):**
- Tone: Sharp, analytical, founder-focused. No fluff. Every sentence should teach something.
- Audience: Early-stage startup founders, AI/developer tool builders, product-led growth enthusiasts.
- Length: 1,200-1,800 words.
- POV: Third-person analysis, like a smart investor memo written for a builder audience.
- Do not ever use em-dashes (—).
- Always use simple and conversational English with connector words. Avoid corporate jargon ("synergy," "leverage," "ecosystem play," "disruption" -> replace with plain language).
- Every claim must feel backed by evidence or logic. Use specific numbers.
- Each H3 sub-section should start with a concept sentence, then explain the mechanism, then give 1 example.
- **Do not repeat the title in the MDX body.** The title should only exist in the frontmatter. Do NOT include an `<h1>` or `# [Title]` just before the TL;DR.
- Never write a conclusion section. End on the takeaway paragraph or the FAQ.

The MDX must follow this exact structure:

```mdx
---
title: "How [Company] [Achieved X] by [Core Strategy]"
description: "[1-2 sentence compelling summary with hard numbers]"
date: "YYYY-MM-DD"
slug: "[URL-friendly-slug-e.g.-company-name-case-study]"
image: "[PUBLIC_IMAGE_URL]"
readingTime: "[X] Min"
published: true
---

<div style={{ textAlign: 'left' }}>

**TL;DR**
* **Challenge:** [The core painful problem in the market they addressed]
* **Solution:** [What they specifically built or did differently]
* **Results:** [2–3 hard metrics — downloads, revenue, users, growth %]
* **Investment/Strategy:** [The one key strategic bet they made]

## The Problem
[Paint the before-state: What was the world like before this company's solution? Who was suffering, and what were they forced to do instead? Make it visceral use developer/founder language. Length: 2-3 paragraphs. No bullet points.]

## The Execution & GTM Strategy
[Break into 2–4 H3 sub-sections picking from: a) THE DISTRIBUTION STRATEGY, b) THE MONETIZATION LAYER, c) THE TECHNICAL / PRODUCT MOAT, d) THE INTERNAL DOGFOODING MOMENT, e) THE TIMING INSIGHT]
### [H3 Sub-section]
[Concept sentence. Mechanism. 1 Example.]

## The Results & Takeaways
[3–5 hard metrics in bullet points (downloads, revenue, customers, conversions, time saved)]

**What a small startup can take from them:**
[Actionable and specific takeaway connected directly to the target audience. Tie the lesson directly to the company's specific strategy. No generic advice.]

---

## Frequently Asked Questions

<FAQSection>
  <FAQItem question="[AEO Question 1 - e.g., What was their primary growth strategy?]">
    [Fully answered in 2-4 sentences. Never leave blank.]
  </FAQItem>

  <FAQItem question="[AEO Question 2 - e.g., How do they monetize?]">
    [Fully answered in 2-4 sentences. Never leave blank.]
  </FAQItem>
  
  <FAQItem question="[Promotion Question - e.g., How can my startup replicate this?]">
    [Answer explaining the strategy, followed by a subtle pitch for your brand/product: "If you are looking to build a predictable distribution engine like [Company], [YourBrand](https://yourdomain.com) specializes in engineering these exact growth loops. Book a strategy call to see if you are a fit."]
  </FAQItem>
</FAQSection>

</div>
```
- **QA Tester:** Are there 0 em-dashes? Is it 1200-1800 words? Are there hard metrics? If not, rewrite.

## 5. Quality Assurance (QA) Check
Before proceeding, self-audit the draft again:
- **MDX Rules:** Is it strictly following the MDX format? Are there exactly zero em-dashes?
- **Tone:** Is it punchy and analytical?
- **Cover Image:** Is the image generated and ready?

## 6. Asset Upload
- Upload the cover image to the user's preferred storage bucket (e.g., GCS, AWS S3, Cloudinary).
- Command: Use the appropriate CLI tool (e.g., `gsutil cp ./cover.png [TARGET_BUCKET]`).
- Verify the public URL matches the `image:` field in the MDX.
- **QA Tester:** Did the upload succeed? Verify the public URL exists.

## 7. GitHub Publishing (Direct Push)
- Use `git` CLI to clone the target repository: `[TARGET_REPO_URL]`
- Move the generated MDX file into the target directory (e.g., `blogs/`).
- **Build Check:** Before committing, run the project's build command (e.g., `npm install && npm run build`) inside the repo to ensure the MDX syntax doesn't break the build.
- **Git Config:** Ensure you are pushing with the correct author details. Run `git config user.name "[GIT_USER_NAME]"` and `git config user.email "[GIT_USER_EMAIL]"` before committing.
- Commit the changes and push directly to the remote branch of `[TARGET_REPO_URL]` using `git pull upstream main --rebase && git push upstream main` (or the equivalent remote structure).
- **QA Tester:** Did the build pass? Did the git push succeed? If not, fix the errors.

## 8. Verification & Delivery
- **DO NOT SKIP THIS:** Before completing the task, you MUST run `git log -1` and `git status` inside the repo to prove the file was committed and pushed.
- Your final response to the user MUST include:
  1. A detailed summary of the SerpAPI (Google Trends) research.
  2. The public URL of the uploaded cover image.
  3. The actual output of the `git log -1` command proving the work is done.
- **Email Notification:** You MUST also send this exact same final summary via email to `[ADMIN_EMAIL]`. You can quickly write and execute a Python script using `smtplib` to send it from the configured sender email using an App Password.
- **Final QA Tester:** Did you send the email? Did you include the git log in the final message? If not, you have failed the entire pipeline.


