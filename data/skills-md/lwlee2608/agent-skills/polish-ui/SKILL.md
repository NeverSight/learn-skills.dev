---
name: polish-ui
description: Use when asked to improve, polish, or audit the UI, UX, or look of an existing app in the current repo. Asks what to improve and which pages, screenshots the running app, then applies the fixes the user picks.
user-invocable: true
---

# Polish UI

Improve an existing app's interface without rewriting it. The user picks the focus and scope. The agent brings screenshots and suggestions.

## Rules

1. **Map the routes first.** Read the code. List the pages, framework, shared components, and design tokens. The scope question needs real page names.

2. **Ask focus, scope, and data in one batch.** Use the question tool:
   - **Focus** (multi-select): UI, UX, aesthetic, or all.
     - UI: layout, components, states, accessibility.
     - UX: flows, navigation, feedback, friction.
     - Aesthetic: color, type, spacing, polish.
   - **Scope**: pages from rule 1. For example, the landing page, one page, or the whole app.
   - **Data**: fake data (default) or a real record the user names, like a production ID. Real data shows what fake data hides, like long names. Read only; keep copies outside the repo.

   Ask before inspecting. This avoids work on areas the user does not care about.

3. **Inspect the running app in a browser.** Launch the app. Use any browser automation tool you have (Claude in Chrome, Playwright, browser-use). Screenshot each page at desktop and mobile widths. Save each to a temp dir outside the repo, named by page and width. The user cannot see screenshots in your context, only saved files. Walk the main flows for UX. Some problems only show when rendered, like overflow, contrast, and dead clicks. If the app cannot run, say so and review the code.

4. **Show each finding as real options, one at a time.** Users cannot judge UI changes from words, or many findings at once. Per finding, build each option in a throwaway git worktree. Screenshot it with the same data, cropped to the affected area. Mark the change so the eye finds it fast: inject a bright outline on the changed element before each shot, including the same spot in the before shot, and caption what changed, like "top bar: icon and title added". Never commit the outline. Add before and options side by side to an HTML compare page outside the repo, and open it. Explain the problem plainly and give 2-4 options, your pick first. Also ask taste questions the code cannot answer, like "keep this style or refresh it?"

5. **Reuse the design system.** Use existing components and tokens. Never hardcode a value the theme defines. Add new tokens or components only with user approval.

6. **Make one change per finding.** Then the user can reject one and keep the rest.

7. **Avoid the AI-generated look.** It reads as cheap, generic, and low effort. The goal is a design that looks premium and well thought out. Flag these in existing pages, and never add them:
   - Em dashes in copy. Use a period, comma, or colon.
   - Punctuation at the end of a hero title.
   - Buzzwords like "unlock", "elevate", "seamless", "supercharge".
   - Purple-blue gradients, glassmorphism, and glowing blobs.
   - Emoji as icons or bullets.
   - Pills everywhere: badges, tags, and buttons all rounded-full.
   - Every section as a centered grid of icon, title, and blurb cards.

   Prefer specific copy, real product screenshots, one accent color, and a clear visual hierarchy.

   If a pattern comes from the design system itself, do not override it. Raise it as a rule 4 question. Rule 5 wins until the user picks a change.

## Verification procedure

1. Re-screenshot each changed page at the same widths and with the same data. List before and after paths in pairs.
2. Run the repo's lint, type check, and tests.
