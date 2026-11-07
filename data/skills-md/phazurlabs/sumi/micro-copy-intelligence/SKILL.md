---
name: micro-copy-intelligence
description: "1000+ microcopy and UX-writing templates by component, tone and sector: button labels, every error message and failure state, empty states, tooltips, confirmations, permission requests and notifications. Use when writing any interface string — robotic copy is the loudest slop tell."
---

# Micro-Copy Intelligence

## Why Microcopy Matters

Microcopy is the most underestimated layer of product design. A single word on a button can change conversion by 30%. A poorly written error message causes support tickets. A delightful empty state turns a dead-end into activation. A confusing permission request tanks opt-in rates.

Most products fail at microcopy not because the words are "wrong" but because they are written by developers in a rush, never reviewed by a writer, and never tested with users. The result: vague buttons ("Submit"), hostile errors ("Invalid input"), lifeless empty states ("No data"), and permission requests that give users no reason to say yes.

This skill gives Sumi a production-grade microcopy library — 1000+ templates across every UI component, every state, every tone, and every major industry sector. Every template is copy-paste ready, with tone variants, character counts, accessibility notes, and i18n considerations.

## Core Principle: Clear > Clever

The single most important rule in UX writing: **clarity beats cleverness every time**. Users are not reading your interface for entertainment. They are trying to accomplish a task. Every word should reduce cognitive load, not add to it.

| Principle | Description | Example |
|-----------|-------------|---------|
| Clear > Clever | Plain language over puns or jargon | "Save changes" not "Commit your brilliance" |
| Specific > Generic | Tell them exactly what happens | "Delete 3 photos" not "Delete items" |
| Human > Robotic | Write like a helpful person, not a machine | "We couldn't find that page" not "Error 404: Resource not located" |
| Short > Long | Every extra word is cognitive cost | "Saved" not "Your changes have been successfully saved" |
| Active > Passive | Direct the user with active voice | "Enter your email" not "Email should be entered" |
| Consistent > Creative | Same action = same word everywhere | Always "Remove" or always "Delete", never both |
| Helpful > Blaming | Guide, don't accuse | "That password is too short" not "You entered an invalid password" |

## Voice and Tone Framework

**Voice** is your product's personality — it stays constant. **Tone** adapts to context.

### Voice Spectrum (Pick Your Position)

```
Formal ←————————————————→ Casual
  |                           |
  Banking, Legal,         Social, Gaming,
  Enterprise              Consumer

Serious ←————————————————→ Playful
  |                           |
  Healthcare, Finance     Entertainment,
  Security                Kids, Social

Respectful ←—————————————→ Irreverent
  |                           |
  Government, Medical     Startup, Youth
  Enterprise              Consumer

Matter-of-fact ←—————————→ Enthusiastic
  |                           |
  Utilities, Tools        E-commerce,
  Productivity            Fitness, Social
```

### Tone Adaptation by Context

The same product shifts tone based on what the user is experiencing:

| Context | Tone Shift | Why |
|---------|------------|-----|
| **Errors** | Empathetic, calm, helpful | User is frustrated — don't add to it |
| **Success** | Warm, affirming, brief | User accomplished something — celebrate proportionally |
| **Empty states** | Encouraging, instructional | User sees nothing — guide them to value |
| **Destructive actions** | Cautious, specific, clear | High stakes — no ambiguity allowed |
| **Onboarding** | Welcoming, motivating | First impressions — build confidence |
| **Loading/waiting** | Light, reassuring | User is stuck — ease anxiety |
| **Permission requests** | Transparent, benefit-led | User must trust you — explain why |
| **Pricing/payment** | Trustworthy, precise | Money is involved — no vagueness |
| **Legal/compliance** | Plain, clear, accessible | Required info — make it readable |

## Content Hierarchy in UI

Every UI moment has three layers of information. Not all three are always needed.

| Layer | Purpose | Example (File Upload) |
|-------|---------|----------------------|
| **Primary** | What to do | "Upload your photo" |
| **Secondary** | Why or context | "This will be your profile picture" |
| **Tertiary** | How or constraints | "JPG or PNG, max 5 MB" |

**Rules:**
- Primary copy is always visible
- Secondary copy appears when context is unclear
- Tertiary copy appears on hover, in helper text, or when errors occur
- Mobile: reduce to primary + tertiary (space is precious)

## The Microcopy Formula

For any UI element, apply this structure:

```
[Action Verb] + [Object] + [Benefit/Context]
```

**Examples:**
- "Save changes" = action + object
- "Upload photo to complete your profile" = action + object + benefit
- "Delete this project permanently" = action + object + context
- "Invite teammates to collaborate" = action + object + benefit

**When to add benefit/context:**
- The action is unfamiliar (onboarding)
- The action is irreversible (destructive)
- The action requires trust (permissions, payments)
- The action has a non-obvious outcome

## Readability Scoring for UI

Target readability for UI text:

| Component | Flesch-Kincaid Grade | Max Words | Max Characters |
|-----------|---------------------|-----------|----------------|
| Button label | Grade 3-5 | 1-4 | 25 |
| Tooltip | Grade 5-7 | 5-15 | 80 |
| Error headline | Grade 4-6 | 3-8 | 50 |
| Error body | Grade 5-7 | 10-25 | 150 |
| Empty state headline | Grade 4-6 | 3-8 | 50 |
| Empty state body | Grade 5-8 | 10-30 | 180 |
| Toast message | Grade 4-6 | 3-10 | 60 |
| Notification title | Grade 4-6 | 3-10 | 65 |
| Notification body | Grade 5-7 | 10-25 | 150 |
| Onboarding headline | Grade 3-5 | 3-8 | 50 |
| Onboarding body | Grade 5-7 | 15-40 | 250 |
| Helper text | Grade 5-7 | 5-15 | 100 |
| Confirmation dialog title | Grade 4-6 | 3-8 | 50 |
| Confirmation dialog body | Grade 5-7 | 10-30 | 180 |
| Permission request body | Grade 5-7 | 15-35 | 200 |
| Loading message | Grade 3-5 | 2-8 | 50 |

**Testing readability:** Paste your copy into Hemingway Editor or use the Flesch-Kincaid formula. If a 12-year-old cannot understand it instantly, rewrite it.

## Inclusive Language Checklist

Before shipping any microcopy:

- [ ] **Gender-neutral:** "They" not "he/she". "Spouse" not "husband/wife". "Parent" not "mother/father" (unless context-specific).
- [ ] **Ability-neutral:** "Select" not "Click". "View" not "See". "Enter" not "Type". Avoid "simple", "easy", "just" (what is easy for you may not be for them).
- [ ] **Age-neutral:** Avoid generational slang. "Download" not "Yeet this to your device".
- [ ] **Culture-neutral:** Avoid idioms that do not translate ("break a leg", "piece of cake"). No sports metaphors as primary copy.
- [ ] **Jargon-free:** "Sign in" not "Authenticate". "Save" not "Persist". "Error" not "Exception".
- [ ] **No assumptions:** Do not assume family structure, location, device, connection speed, or technical literacy.
- [ ] **Respectful defaults:** "Preferred name" not "Nickname". "Phone number (optional)" not "Mobile number (required)".
- [ ] **Error messages blame the system, not the user:** "We couldn't process that" not "You made an error".

## i18n Considerations for Microcopy

Microcopy that works in English may break in translation. Plan ahead:

### Text Expansion

| Language | Expansion vs. English |
|----------|----------------------|
| German | +30-35% |
| French | +15-20% |
| Spanish | +20-25% |
| Italian | +15-20% |
| Portuguese | +20-30% |
| Russian | +15-20% |
| Japanese | -10-20% (character count, but wider glyphs) |
| Chinese | -20-30% (character count) |
| Arabic | +20-25% (plus RTL layout) |
| Korean | -10-15% |

**Rules:**
- Buttons: Allow 40% extra width or use auto-sizing
- Tooltips: Max 60% of container width in English to allow expansion
- Never hard-code string widths
- Test with German and Arabic (longest expansion + RTL)

### Cultural Sensitivity

- **Humor:** Puns and wordplay rarely translate. Stick to clear language.
- **Formality:** German, Japanese, Korean require formal register by default. "Du" vs "Sie" in German matters enormously.
- **Color of language:** "Red" means danger in the West, luck in China. Do not rely on color words alone.
- **Dates and numbers:** "1/2/2026" is January 2 (US) or February 1 (most of the world). Use explicit formats.
- **Names:** Not everyone has a first + last name structure. "Full name" is safer than "First name / Last name".
- **Icons with text:** Thumbs-up is offensive in parts of the Middle East. Always pair icons with text labels.

### String Externalization

- Every user-facing string must be in a localization file, never hard-coded
- Use ICU MessageFormat for plurals: `{count, plural, one {# item} other {# items}}`
- Avoid string concatenation: `"Welcome, " + name + "!"` breaks in languages with different word order
- Use full sentences as translation units, not fragments

## Sector Tone Guides

### Fintech / Banking
- **Voice:** Trustworthy, precise, confident
- **Tone keywords:** Secure, clear, straightforward, reliable
- **Do:** "Your transfer of $500 to Alex is complete" / "Verify your identity to protect your account"
- **Don't:** "Woohoo, money sent!" / "We need to make sure you're really you lol"
- **Button style:** "Transfer funds", "Review statement", "Verify identity"
- **Error style:** "We couldn't complete this transfer. Your account has not been charged. [Try again]"

### Healthcare / Wellness
- **Voice:** Empathetic, clear, reassuring
- **Tone keywords:** Caring, supportive, plain, calm
- **Do:** "Your appointment with Dr. Chen is confirmed for March 15 at 2:00 PM" / "Your results are ready. Tap to view."
- **Don't:** "Awesome, you're booked!" / "RESULTS ARE IN!!!"
- **Button style:** "Schedule appointment", "View results", "Message your care team"
- **Error style:** "We couldn't schedule your appointment. Dr. Chen is available at these other times: [alternatives]"

### SaaS / Productivity
- **Voice:** Efficient, empowering, knowledgeable
- **Tone keywords:** Smart, capable, streamlined, no-nonsense
- **Do:** "Project created. Invite your team to get started." / "3 tasks due today"
- **Don't:** "YAY, new project!" / "You've got stuff to do"
- **Button style:** "Create project", "Invite team", "Start timer"
- **Error style:** "This project name is already taken. Try a different name. [Rename]"

### Social / Community
- **Voice:** Warm, expressive, conversational
- **Tone keywords:** Friendly, personal, inclusive, fun
- **Do:** "Alex liked your photo" / "Share what's on your mind"
- **Don't:** "User 4829 interacted with your content" / "Compose a status update"
- **Button style:** "Share", "Like", "Comment", "Send a message"
- **Error style:** "We couldn't post that right now. Your draft is saved. [Try again]"

### E-commerce / Marketplace
- **Voice:** Helpful, enthusiastic, trustworthy
- **Tone keywords:** Exciting, confident, reassuring, action-oriented
- **Do:** "Free shipping on orders over $50" / "Only 3 left in stock"
- **Don't:** "Shipping fees may apply based on various factors" / "Limited inventory warning"
- **Button style:** "Add to cart", "Buy now", "Apply code", "Complete purchase"
- **Error style:** "This item just sold out. We'll notify you when it's back. [Get notified]"

### Education / EdTech
- **Voice:** Encouraging, patient, clear
- **Tone keywords:** Supportive, motivating, structured, approachable
- **Do:** "Great work! You completed 3 of 5 lessons." / "Pick up where you left off"
- **Don't:** "CRUSHING IT" / "Resume incomplete module"
- **Button style:** "Start lesson", "Continue learning", "Take quiz", "Review answers"
- **Error style:** "That answer didn't match. Review the hint and try again. [Show hint]"

### Developer Tools
- **Voice:** Direct, precise, technical (but not jargon-heavy)
- **Tone keywords:** Efficient, accurate, no-fluff, respectful of expertise
- **Do:** "Build succeeded in 2.3s" / "API key created. Copy it now — it won't be shown again."
- **Don't:** "Yay, your build worked!" / "Here's your secret key thingy"
- **Button style:** "Deploy", "Create API key", "View logs", "Run tests"
- **Error style:** "Build failed: missing dependency `lodash@4.17`. Run `npm install lodash` to fix. [View full log]"

### Gaming / Entertainment
- **Voice:** Energetic, immersive, personality-forward
- **Tone keywords:** Exciting, playful, dramatic, rewarding
- **Do:** "New high score! You beat your record by 200 points." / "Ready for the next challenge?"
- **Don't:** "Score updated in database" / "Proceed to next level"
- **Button style:** "Play now", "Challenge a friend", "Claim reward", "Continue quest"
- **Error style:** "Connection lost. Your progress is saved. [Reconnect]"

### Real Estate / Property
- **Voice:** Professional, informative, aspirational
- **Tone keywords:** Trustworthy, detailed, approachable, knowledgeable
- **Do:** "3 new listings match your search" / "Schedule a tour of 123 Oak Street"
- **Don't:** "OMG new houses!" / "Initiate property viewing request"
- **Button style:** "Schedule tour", "Save listing", "Contact agent", "Get pre-approved"
- **Error style:** "This listing is no longer available. Here are similar homes nearby. [View similar]"

### Travel / Hospitality
- **Voice:** Inspiring, helpful, warm
- **Tone keywords:** Adventurous, reassuring, personal, anticipatory
- **Do:** "Your trip to Tokyo is confirmed. 14 days to go!" / "Explore things to do near your hotel"
- **Don't:** "Booking reference confirmed" / "Ancillary activity discovery module"
- **Button style:** "Book now", "Explore destinations", "Check availability", "Add to trip"
- **Error style:** "These dates just got booked. Try nearby dates — we found 5 options. [View alternatives]"

## Reference Architecture

| File | Contents | Use When |
|------|----------|----------|
| `references/button-label-templates.md` | 200+ button label templates organized by action type: primary, destructive, navigation, toggle, social, commerce, file, communication. Each with tone variants, character counts, when-to-use guidance, anti-patterns, and i18n notes. | Writing button labels. Choosing between "Save" vs "Save changes" vs "Update". Standardizing CTAs across a product. |
| `references/error-success-messages.md` | 200+ error and success message templates: validation, system, permission, business logic errors. Success confirmations for every common action. Each with headline + body + recovery action + ARIA announcement. | Writing error messages. Creating success confirmations. Building a toast/notification system. Ensuring accessible error handling. |
| `references/empty-state-copy.md` | 150+ empty state copy templates: first-use, no-results, cleared, error, permission states. By component: inbox, dashboard, list, table, search, notifications, activity, calendar, kanban, files, chat. Each with headline, body, CTA, illustration suggestion, tone variants. | Designing empty states. Writing first-use experiences. Creating no-results messages. Handling permission-gated blank screens. |
| `references/onboarding-permission-copy.md` | 150+ onboarding and permission copy templates: welcome screens, profile setup, feature tours, permission requests (notifications, location, camera, etc.), pre-permission priming, progressive disclosure, activation prompts. Each with headline, body, primary/secondary CTA, visual suggestion. | Designing onboarding flows. Writing permission request screens. Creating feature tours. Building activation sequences. |
| `references/notification-tooltip-copy.md` | 200+ notification, tooltip, and contextual help templates: push notifications, in-app notifications, toasts, tooltips, helper text, confirmation dialogs, loading messages, changelog entries. Each with text template, character limit, tone, timing. | Writing push notifications. Creating tooltip copy. Building confirmation dialogs. Writing loading states. Composing changelog entries. |

## How to Use This Skill

### Quick Lookup
"I need a button label for [action]" — Go to `button-label-templates.md`, find the action type, pick the tone variant that matches your product voice.

### Full Screen Copy
"I'm designing a [screen type] and need all the copy" — Combine templates from multiple reference files: buttons from `button-label-templates.md`, errors from `error-success-messages.md`, empty states from `empty-state-copy.md`, tooltips from `notification-tooltip-copy.md`.

### Tone Calibration
"My product is a [sector] app with a [formal/casual] voice" — Use the Sector Tone Guides above to set your voice, then filter all templates through that tone.

### Copy Audit
"Review my existing copy for quality" — Check against the principles (Clear > Clever), readability scores, inclusive language checklist, and anti-patterns in each reference file.

### i18n Preparation
"We're localizing to [language]" — Check text expansion ratios, review cultural sensitivity notes, verify string externalization patterns.

## Quality Checklist for Any Microcopy

Before shipping any piece of UI text, verify:

- [ ] Is it clear on first read? (No re-reading needed)
- [ ] Is it specific? (User knows exactly what will happen)
- [ ] Is it actionable? (User knows what to do next)
- [ ] Is it consistent? (Same terms used across the product)
- [ ] Is it concise? (No unnecessary words)
- [ ] Is it inclusive? (No gendered, ableist, or culturally specific language)
- [ ] Is it translatable? (No idioms, puns, concatenated strings)
- [ ] Is it accessible? (Works with screen readers, announced properly)
- [ ] Does it match the product voice? (Tone is appropriate for context)
- [ ] Is it tested? (Real users understood it without explanation)

## Microcopy Decision Tree

```
User encounters UI element
  |
  +-- Is it an action? (button, link, CTA)
  |     -> button-label-templates.md
  |
  +-- Is something wrong? (error, failure, warning)
  |     -> error-success-messages.md (error section)
  |
  +-- Did something succeed? (confirmation, completion)
  |     -> error-success-messages.md (success section)
  |
  +-- Is it empty? (no content, no results, first use)
  |     -> empty-state-copy.md
  |
  +-- Is it onboarding? (first launch, feature tour, setup)
  |     -> onboarding-permission-copy.md
  |
  +-- Is it asking permission? (notifications, camera, location)
  |     -> onboarding-permission-copy.md (permissions section)
  |
  +-- Is it contextual help? (tooltip, helper text, hint)
  |     -> notification-tooltip-copy.md
  |
  +-- Is it a notification? (push, in-app, toast)
  |     -> notification-tooltip-copy.md
  |
  +-- Is it a confirmation? (delete, cancel, destructive)
  |     -> notification-tooltip-copy.md (confirmation section)
```

## Anti-Pattern Encyclopedia (Top 25)

| # | Anti-Pattern | Example | Fix |
|---|-------------|---------|-----|
| 1 | Vague button | "Submit" | "Create account" / "Send message" |
| 2 | "Click here" | "Click here to learn more" | "Learn more about pricing" |
| 3 | Blaming the user | "You entered an invalid email" | "That doesn't look like an email address" |
| 4 | ALL CAPS buttons | "DELETE ACCOUNT" | "Delete account" (sentence case) |
| 5 | Technical jargon | "Error 500: Internal Server Error" | "Something went wrong. We're looking into it." |
| 6 | Double negatives | "Don't forget to not leave blank" | "This field is required" |
| 7 | Inconsistent terms | "Save" here, "Update" there, "Submit" elsewhere | Pick one term per action type |
| 8 | Wall of text in modal | 200-word confirmation dialog | 2 sentences max in dialog body |
| 9 | No recovery action | "Payment failed." (full stop, nothing else) | "Payment failed. Check your card details and try again. [Update payment]" |
| 10 | Forced enthusiasm | "AMAZING! You signed up!!!" | "Welcome. Your account is ready." |
| 11 | Guilt-tripping | "No thanks, I don't want to save money" | "No thanks" / "Skip" / "Maybe later" |
| 12 | Ambiguous "OK" | Dialog with only "OK" and "Cancel" | "Delete photo" and "Keep photo" |
| 13 | Placeholder as label | Input with only "Email" as placeholder | Persistent label above + placeholder example |
| 14 | Disappearing feedback | Toast that vanishes in 1 second | Minimum 4 seconds + dismiss button |
| 15 | Generic empty state | "No items" | "No projects yet. Create your first project to get started. [Create project]" |
| 16 | Permission without context | System dialog with no pre-screen | Pre-permission screen explaining benefit first |
| 17 | Error with no specifics | "Invalid" (entire message) | "Password must be at least 8 characters" |
| 18 | Cute over clear | "Oopsie daisy! Something went wrong uwu" | "Something went wrong. Try refreshing the page." |
| 19 | Hidden destructive action | Delete styled as primary action | Red text, confirmation dialog, clear consequences |
| 20 | Loading with no context | Spinner with no message forever | "Loading your dashboard..." with progress indicator |
| 21 | Overloaded button | "Save, publish, and notify team" | Three separate actions or a split button |
| 22 | Negative framing | "You have 0 connections" | "Start connecting with people you know" |
| 23 | Passive voice error | "An error was encountered" | "We hit a snag" or "Something went wrong" |
| 24 | Unexplained restriction | "This action is not allowed" | "Only workspace admins can delete projects. Ask your admin for access." |
| 25 | Untranslatable idiom | "Piece of cake!" as success message | "Done!" or "All set!" |

## Writing Microcopy: Step-by-Step Process

1. **Identify the moment.** What is the user doing right now? What just happened? What emotional state are they likely in?
2. **Determine the goal.** What do you need the user to understand or do next?
3. **Pick the tone.** Use the tone adaptation table — match the context, not your default voice.
4. **Draft with the formula.** [Action] + [Object] + [Benefit/Context] as needed.
5. **Cut ruthlessly.** Remove every word that is not doing work. Read it aloud — if you stumble, simplify.
6. **Check the checklist.** Inclusive? Translatable? Accessible? Consistent? Specific?
7. **Test with real users.** Show it out of context — can they tell what it means? Show it in context — do they do the right thing?

## Accessibility Requirements for Microcopy

- **ARIA live regions:** Error messages and success confirmations must be announced to screen readers via `aria-live="polite"` (success) or `aria-live="assertive"` (errors).
- **Error association:** Every error message must be programmatically associated with its input via `aria-describedby`.
- **Button labels:** If a button uses only an icon, provide `aria-label` with the full text label.
- **Tooltip accessibility:** Tooltips must be reachable via keyboard (focus, not just hover) and announced by screen readers.
- **Loading announcements:** Announce loading start and completion to screen readers.
- **Confirmation dialogs:** Focus must move to the dialog when it opens and return to the trigger when it closes.
- **Status messages:** Use `role="status"` for non-critical updates and `role="alert"` for urgent messages.
- **No time pressure:** If a toast auto-dismisses, the information must be available elsewhere (notification center, status area).
