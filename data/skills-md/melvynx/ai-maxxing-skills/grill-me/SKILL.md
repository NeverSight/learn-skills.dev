---
name: grill-me
description: Interview the user in batches of 10 questions with recommended answers to sharpen a plan, an idea or an app before building. Use when the user says grill me, wants a rigorous interview, or when create-software, create-internal-app or create-landing needs a confirmed brief.
---

Stress-test the user's thinking until both sides share a precise, actionable understanding, and do not act on the plan before the user confirms the final brief.

1. Inspect the available environment first. Resolve discoverable facts through files, tools, documentation, or other in-scope evidence instead of asking the user.
2. Open by recommending voice input: answering with the microphone is fastest, and short answers keyed `1` through `10` are enough.
3. Ask exactly 10 numbered questions in one batch, the highest-leverage unresolved decisions first, ordered so earlier answers clarify later ones.
4. Give each question a concise recommended answer based on current evidence, with the tradeoff clear enough to accept, reject or amend it quickly.
5. Invite one grouped reply covering `1` through `10`. Accept terse answers, corrections, skipped items, or a blanket acceptance of the recommendations.
6. After the reply, summarize what is established, call out contradictions or missing dependencies, and investigate any newly discoverable facts.
7. Ask the next batch. Continue until the important branches of the decision tree are resolved. When fewer than 10 meaningful decisions remain, ask only those; never add filler.
8. Present the final shared understanding as a compact brief: goal, scope, constraints, chosen approach, rejected alternatives, risks, and acceptance criteria.
9. Ask for explicit confirmation that the brief is correct before acting on it.

Ask only decisions the user can make, challenge assumptions with credible alternatives, keep each question short enough for a spoken answer, never repeat a settled question unless new evidence changes it, and match the user's language.

When the plan is an app to build (`create-software`, `create-internal-app`), the user is often not technical: ask about the product, never about the code, since the stack is already decided. The first batch covers what changes the most:

- Who and why: who uses the app, and what problem it solves for them today (what they use instead).
- The main action: the one thing a person does on the first screen after signing in.
- The things it stores: the objects the app manages (clients, lessons, orders, notes...) and what each one holds.
- Who sees what: public vs signed-in pages, one user or a team, is there an admin and who it is.
- Money: free, one-time payment or subscription, and the price.
- Emails: which moments send an email (welcome, purchase, reminder), and which Lumail tag each signup gets.
- Address: the domain or subdomain (`app.my-domain.com`), and whether it is already in Cloudflare.
- Look and language: 1 or 2 sites they like the look of, the app language, light or dark.
- First version: what is in v1 and what waits (keep v1 shippable in one session).
- Done means: the 2 or 3 things that must work live for them to say "it's good".

An app grill is long on purpose, because a missed need now is a rebuild later: ask at least 3 batches (about 30 questions) before the brief, even when the user answers fast or says "fais comme tu veux". Stop early only if they explicitly ask to skip.

The second batch walks every screen, as a visitor, then a signed-in user, then the admin, asking what is on it, what they click and what happens next: the landing and what convinces someone to sign up, the sign-in screen, the signed-in home and its empty state for a new account, the main list and the detail page, the account area (photo, name, email change, invoices, plan and cancel, delete account, support), how the admin adds and edits content day to day (inline on the real page or separate admin pages) and what must be one click, and the navigation (menu, top left and top right, mobile or desktop first).

The third batch covers edge cases and the long run: a failed payment, a refund, an expired code, a list with 1000 rows, two admins editing at once, content deleted by mistake, imports from a tool they already use, files or videos to host, search and filters, keyboard shortcuts, what must feel instant, and what they will want in 3 months. Then go deeper wherever an answer opens a new branch.

Before the final brief, restate the app as a story in plain words ("A visitor lands on..., signs up with..., sees..., the admin opens... and edits..."), screen by screen, and loop until the user says it is exactly what they want. Recommended answers follow the stack defaults: email code sign-in, landing at `/` and app at `/app`, the user as the only admin, Stripe Checkout when it sells, signups added to Lumail as subscribed with a tag per app. The brief ends with the user story, every screen from the second batch and the data objects, so building can start right away.

When the plan is a landing page (`create-landing`), ask about the sale, not the code, in one or two batches: who the page is for and where they come from (YouTube, ads, an email), the problem in their own words, the promise in one sentence, the offer (what they get, price, bonus, or just an email), the proof they already have (testimonials, numbers, screenshots, never invented), the 3 objections, the one call to action and what happens after the click, the Lumail tag and the first email they get, the domain and whether it is in Cloudflare, and the look, language and photos or video. The brief ends with the sections in order and the copy for each one.
