---
name: full-stack-ai-product-building
description: Use AI to transform product intent into production-ready software. Use this skill when you need to prototype a new feature, build a functional MVP without engineering resources, or refine a UI/UX layout through rapid iteration.
---

# Full-Stack AI Product Building

Full-stack AI product building enables product managers and designers to move from "yapping" to "shipping" by leveraging LLMs as translation engines. Instead of writing code from scratch, you act as a "product coach," providing direction, defining "taste," and managing the AI through iterative loops to reach production quality.

## Phase 1: Building Product Taste (Exposure Hours)

Before building, you must calibrate your "taste" muscle to recognize high-quality output.

1.  **Quantify Exposure Hours:** Dedicate specific time each week to watching users interact with your product and using the "frontier" apps in your category.
2.  **Deconstruct UX "Tokens":** Identify specific technical elements that create quality (e.g., "Shadcn" components, "Tailwind" styling, "Canvas-based" rendering, or "Responsive" hamburger menus).
3.  **Identify Patterns:** Notice small nuances, such as how an app handles mobile input differently than desktop (e.g., Enter key behavior).

## Phase 2: Intent-First Prompting

Invert the traditional development process by starting with intent rather than implementation details.

1.  **Use High-Level Intent:** Describe the "job to be done" rather than specific CSS properties.
    *   *Example:* "Create a contact sales form for a luxury financial institution" vs. "Make a form with a blue button."
2.  **Leverage Visual Artifacts:** Upload screenshots of inspirations (e.g., a specific dashboard layout) or Figma files to provide the AI with a visual starting point.
3.  **Use the "Enhanced Prompt" Tool:** If experiencing "writer's block," use AI to expand your simple prompt into a detailed specification that includes accessibility guidelines and best practices.
4.  **Community Forking:** Don’t start from scratch. Search community repositories (like v0.dev/community) for a similar architectural pattern and "fork" it to customize.

## Phase 3: The Iterative Coaching Loop

Treat the AI like a "super genius five-year-old PhD." It knows everything but needs constant steering.

1.  **Iterative Refinement:** If the output isn't right, use conversational coaching.
    *   "Try something else."
    *   "Make it more jazzy/pop."
    *   "Apply a Neobrutalist style."
2.  **Style Transfer:** Give the AI a second reference point to modify the first. 
    *   *Example:* "Take this news site layout but apply the sepia color palette and typography from this other screenshot."
3.  **Add Functional Layers:** Start with the "front-end" (the experience) and then prompt for the "back-end" (e.g., "Now connect this form to a database" or "Integrate this map with a live flight data API").

## Phase 4: The "Escape Hatch" (Getting Unstuck)

When the AI hits a reasoning limit or produces a runtime error:

1.  **Cross-Model Validation:** Copy the generated code and paste it into a different high-reasoning model (like OpenAI o1) to debug a specific logic error.
2.  **Prompt for Performance:** If an interface is slow, don't tell it how to fix it. State the problem: "We have tens of thousands of data points; improve the rendering performance."
3.  **Code-Last Mentality:** Use the code view to identify "tokens" or properties you want to change, then go back to the chat to request those specific edits (e.g., "Center that div").

## Examples

**Example 1: The "Flight Radar" Prototype**
*   **Context:** You need a high-performance map showing live assets but have a poor internet connection and no dev help.
*   **Input:** "Build the best flight radar on the planet. Show airplanes on a map."
*   **Iteration:** "The performance is lagging with 10k planes." -> AI implements a Canvas-based overlay.
*   **Final Polish:** "Draw a dashed line between destination airports that accounts for the curvature of the earth."
*   **Output:** A production-ready, interactive map using Mapbox and Leaflet.

**Example 2: The "Bank-Grade" Contact Form**
*   **Context:** You have a rough draft but it looks "cheap."
*   **Input:** "Create a contact sales form."
*   **Application:** Upload a screenshot of Charles Schwab's website.
*   **Refinement:** "Make this more serious. Use bank-grade typography. Apply a sepia filter to all checkboxes."
*   **Output:** A functional React component using Shadcn/UI that matches the institution's brand identity.

## Common Pitfalls

*   **Being Too Prescriptive:** Don't tell the AI which CSS properties to use if you aren't an expert. State the *feeling* or *style* (e.g., "Minimalist" or "Vintage") and let it choose the properties.
*   **The "One-and-Done" Trap:** Accepting the first generation as the final version. High-quality AI products often require 10-100+ iterations.
*   **Ignoring the Code:** Even if you don't code, looking at the code helps you learn the "tokens" (like `filter: sepia()`) that you can use in future prompts to get what you want faster.
*   **Adopting Too Many "Puppies":** Every new AI-generated feature requires maintenance. Use creative restraint; say "no" to features that add complexity without core value.