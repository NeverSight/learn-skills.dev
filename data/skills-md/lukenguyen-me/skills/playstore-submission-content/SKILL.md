---
name: playstore-submission-content
description: Generate ready-to-paste Google Play Store text content for Android app submissions. Analyzes project context and produces all required text fields with Play Store character rules enforced.
---

# Play Store Submission Content

Generate polished, Play Store-ready text content for your Android app submission. This skill handles all localizable fields, enforces Google's character and formatting rules, and outputs clean markdown organized by language.

## When to Use

Users ask things like:
- "Generate Play Store description for my app"
- "Write Play Store listing content"
- "Create Play Console text fields"
- "Help with Google Play Store submission"
- "Generate app listing content for Android"

Your job: gather app details, generate compelling content for all fields, and output structured markdown ready to copy-paste into Play Console.

## What Makes Strong Play Store Content

The Google Play Store has different rules than Apple's App Store. Understanding these differences is critical for rejection-free submissions.

**App Title (30 chars)**
- Weak: "My Great Task Manager App 2024"
- Strong: "Mint: Budget & Money"

**Short Description (80 chars)**
- Weak: "The best todo list app ever made with amazing features"
- Strong: "Track spending, set budgets, and reach your financial goals."

**Full Description (4000 chars)**
- Weak: "This app has many features. You can add tasks. You can check them off."
- Strong: "Mint replaces your scattered finances with a single, elegant system. Track expenses in seconds, set budgets that actually work, and get alerts when it matters. 💰 No subscription required."

**What's New (500 chars)**
- Weak: "Bug fixes and improvements"
- Strong: "Redesigned home screen with quick-add widget. Fixed bank sync issues. Added dark mode support."

## Field Reference

### Localizable Fields (per language)

| Field | Max Characters | Key Rules |
|-------|----------------|-----------|
| App Title | 30 | No emojis, no ★☆, no ALL CAPS (unless brand), no repeated punctuation, no line breaks |
| Short Description | 80 | No emojis, no symbols — first text users see in search results |
| Full Description | 4000 | **Emojis ALLOWED** — plain text only, no HTML; first ~167 chars shown before "Read More" |
| What's New | 500 | Short release notes for existing users deciding to update |

### Global Fields (not localized)

| Field | Format | Notes |
|-------|--------|-------|
| Primary Category | From category list | Required. Apps or Games subcategory |
| Secondary Category | From category list | Optional |
| Content Rating | Suggested rating | AI suggests; developer must complete IARC questionnaire in Play Console |
| Tags | Up to 5 tags | Optional, helps with discoverability |

> **Key Difference:** Play Store has NO Keywords field. The store indexes your description text directly.

## Character Rules

Your content must follow Play Store formatting rules:

### Forbidden in App Title and Short Description

| Category | Forbidden |
|----------|-----------|
| Emoji | All emojis (U+1F300+) — will be stripped or cause rejection |
| Symbols | ★ ☆ and similar |
| Repeated chars | `??` `!!` `?!` `!?!` `<>` `\\` `---` `***` `+_+` `((` `$%^` `~&~` `~~~` |
| ALL CAPS | Words in all caps (unless established brand name) |
| Line breaks | Not allowed in these fields |

### Forbidden Everywhere (including Full Description)

| Category | Forbidden |
|----------|-----------|
| HTML | Any HTML tags (`<br>`, `<b>`, `<ul>`, etc.) — shown as raw text |
| Performance claims | "Ranked #1", "Most downloaded", store rankings |

### Allowed in Full Description Only

- Emojis (encouraged as visual bullets)
- Line breaks and blank lines between sections
- Unicode symbols: ✓ ✔ • →

## Supported Languages

The Play Store supports 51 languages across 77 locales. Generate content in these languages as needed:

| Code | Language | Code | Language |
|------|----------|------|----------|
| af | Afrikaans | kn | Kannada |
| ar | Arabic | ko | Korean |
| be | Belarusian | lt | Lithuanian |
| bg | Bulgarian | lv | Latvian |
| bn | Bengali | ms | Malay |
| ca | Catalan | ml | Malayalam |
| cs | Czech | mr | Marathi |
| da | Danish | nl | Dutch |
| de | German | no | Norwegian |
| el | Greek | fa | Persian |
| en-US | English (US) | pl | Polish |
| es-ES | Spanish (Spain) | pt-BR | Portuguese (Brazil) |
| es-419 | Spanish (Latin America) | pt-PT | Portuguese (Portugal) |
| et | Estonian | ro | Romanian |
| fa | Persian | ru | Russian |
| fi | Finnish | sk | Slovak |
| fr-FR | French (France) | sl | Slovenian |
| fr-CA | French (Canada) | sr | Serbian |
| gl | Galician | sv | Swedish |
| gu | Gujarati | sw | Swahili |
| hi | Hindi | ta | Tamil |
| hr | Croatian | te | Telugu |
| hu | Hungarian | th | Thai |
| id | Indonesian | tr | Turkish |
| it | Italian | uk | Ukrainian |
| iw | Hebrew | ur | Urdu |
| ja | Japanese | vi | Vietnamese |
| ja-JP | Japanese (Japan) | zh-CN | Chinese (Simplified) |
| ko | Korean | zh-TW | Chinese (Traditional) |

## Multi-Language Detection

### How to Detect Localization in a Project

1. **Android Native:**
   - `res/values-*/strings.xml` files
   - `res/values/strings.xml` for default

2. **Flutter:**
   - `lib/l10n/*.arb` files

3. **React Native / Generic:**
   - `i18n/`, `locales/`, `translations/` directories

4. **Kotlin Multiplatform:**
   - `commonMain/resources/MR/` directory

5. **Fastlane:**
   - `fastlane/metadata/android/` subdirectories (one per locale)

### Multi-Language Workflow

1. Scan project for localization signals using the paths above
2. If localization detected → report found languages, ask user to confirm multi-language output (recommend yes)
3. If confirmed → generate all localizable fields for each detected language
4. If no localization detected → default to English (US) only

## Project Analysis Guide

### What to Extract

Before generating content, analyze the codebase to gather:

| Source | What to Look For |
|--------|-----------------|
| `build.gradle`, `app/build.gradle` | App name, package name, version |
| `AndroidManifest.xml` | App name, permissions |
| `README.md` | App description, key features |
| Source code comments | Unique selling points |
| Existing marketing materials | Brand voice, key phrases |
| `pubspec.yaml` (Flutter) | App name, description |

### Questions to Ask User

If information is missing, ask:
- What is the app's primary purpose?
- Who is the target audience?
- What are the top 3 features?
- Is there existing copy you'd like to adapt?
- What category should the app be listed under?

## Per-Field Writing Guidance

### App Title

**Weak:** Contains keywords, too long, generic, uses emojis
**Strong:** Memorable, distinctive, fits 30-char limit, no prohibited characters

| Weak | Strong |
|------|--------|
| "Best Task Manager Todo List 2024" | "Done - Simple Tasks" |
| "💰 Free Budget Tracker App" | "Mint: Budget & Money" |
| "PROFESSIONAL CALENDAR SCHEDULER" | "Cal" |

**Rules:**
- 30 characters maximum
- No emojis
- No ★ or ☆ symbols
- No ALL CAPS (unless established brand)
- No repeated punctuation
- No line breaks

### Short Description

**Weak:** Generic praise, too long, uses emojis
**Strong:** Specific benefit, fits 80 chars, no prohibited characters

| Weak | Strong |
|------|--------|
| "The best productivity app ever!!" | "Track spending, set budgets, and reach your financial goals." |
| "📱 Organize your life with this amazing app" | "Your tasks, organized beautifully" |

**Rules:**
- 80 characters maximum
- No emojis
- No symbols
- No repeated characters
- First text users see in search results — make it count

### Full Description

**Weak:** Feature list without context, generic claims
**Strong:** Benefit-driven opening, emoji-bulleted features, specific benefits, CTA

Structure:
1. Opening hook (1-2 sentences) — What problem do you solve?
2. Key benefits (2-3 sentences) — Why should someone care?
3. Features (3-6 bullet-style lines with emojis) — What can they do?
4. Call to action (1 sentence) — Download now

**Rules:**
- 4000 characters maximum
- **Emojis ALLOWED and encouraged** as visual bullets
- Plain text only — no HTML (will display as raw text)
- First ~167 characters shown before "Read More"
- Use line breaks between sections for readability

**Weak:**
"This app has many features. You can add tasks. You can organize them into lists. You can set due dates. You can get reminders. It is very useful. Download now."

**Strong:**
"Mint replaces your scattered finances with a single, elegant system. Track expenses in seconds, set budgets that actually work, and get alerts when it matters. 💰

• Track all your accounts in one place
• Set personalized budgets and savings goals
• Get bill reminders before due dates
• Beautiful charts and spending insights
• Works completely offline 🔒

Download Mint today and take control of your money."

### What's New

**Weak:** Generic "bug fixes", meaningless improvements
**Strong:** Specific changes users care about, new feature names

| Weak | Strong |
|------|--------|
| "Bug fixes and improvements" | "Redesigned home screen with quick-add widget. Fixed crash when syncing with your bank." |
| "Performance improvements" | "App now launches 2x faster. Reduced battery usage by 30%." |

**Rules:**
- 500 characters maximum
- Write for users deciding whether to update
- Highlight meaningful changes, not just "bug fixes"
- Include new features by name when possible

## Output Format

Generate structured markdown with one section per language, then global fields:

```markdown
## English (US)

### App Title
[Your app title - 30 chars max]

### Short Description
[Your short description - 80 chars max, no emojis]

### Full Description
[Your full description - 4000 chars max, emojis allowed, no HTML]

### What's New
[Your what's new - 500 chars max]

---

## French (France)

### App Title
[Your app title in French]

### Short Description
[Your short description in French]

### Full Description
[Your full description in French]

### What's New
[Your what's new in French]

---

## Global Fields

### Primary Category
[Category - see Quick Reference]

### Secondary Category
[Category or "None"]

### Content Rating
Suggested: [Everyone / Teen / Mature 17+]

Note: Complete the IARC questionnaire in Play Console to finalize your content rating.

### Tags
[tag1, tag2, tag3, tag4, tag5]
```

## Example: Finance App

```
## English (US)

### App Title
Mint: Budget & Money

### Short Description
Track spending, set budgets, and reach your financial goals.

### Full Description
Mint: Budget & Money replaces your scattered finances with a single, elegant system. Track expenses in seconds, set budgets that actually work, and get alerts when it matters. 💰

• Track all your accounts in one place
• Set personalized budgets and savings goals
• Get bill reminders before due dates
• Beautiful charts and spending insights
• Free credit score and identity protection 🔒

Join over 30 million users who trust Mint to manage their money. Download now!

### What's New
Redesigned home screen with quick-add widget. Fixed bank sync issues with major institutions. Added dark mode support. Improved budget tracking accuracy.

---

## Global Fields

### Primary Category
Finance

### Secondary Category
None

### Content Rating
Suggested: Everyone

Note: Complete the IARC questionnaire in Play Console to finalize your content rating.

### Tags
budget, finance, money, expense tracker, savings
```

## Example: Fitness App (Multi-Language)

```
## English (US)

### App Title
FitLog - Workout Tracker

### Short Description
Track workouts, set goals, and crush your fitness targets.

### Full Description
FitLog is your ultimate workout companion. Track exercises, set personalized goals, and see your progress with beautiful charts. 💪

• Log 200+ exercises with ease
• Create custom workout routines
• Track progress with detailed analytics
• Get motivated with achievements
• Works offline, syncs when online 📱

Download FitLog and start crushing your fitness goals today!

### What's New
New exercise library with video tutorials. Improved workout logging flow. Fixed issues with sync. Added German language support.

---

## German (Germany)

### App Title
FitLog - Workout Tracker

### Short Description
Trainings aufzeichnen, Ziele setzen, Fitnessziele erreichen.

### Full Description
FitLog ist dein ultimativer Trainingsbegleiter. Zeichne Übungen auf, setze persönliche Ziele und verfolge deinen Fortschritt mit tollen Charts. 💪

• Über 200 Übungen einfach protokollieren
• Erstelle eigene Trainingspläne
• Verfolge Fortschritte mit detaillierten Analysen
• Bleib motiviert mit Errungenschaften
• Funktioniert offline, synchronisiert online 📱

Lade FitLog herunter und erreiche deine Fitnessziele!

### What's New
Neue Übungsbibliothek mit Video-Tutorials. Verbesserter Workout-Protokoll-Flow. Behobene Synchronisierungsprobleme.

---

## Global Fields

### Primary Category
Health & Fitness

### Secondary Category
Sports

### Content Rating
Suggested: Everyone

Note: Complete the IARC questionnaire in Play Console to finalize your content rating.

### Tags
fitness, workout, exercise, training, health
```

## Quick Reference

### Character Limits

| Field | Limit |
|-------|-------|
| App Title | 30 |
| Short Description | 80 |
| Full Description | 4000 |
| What's New | 500 |

### Forbidden Characters

**In App Title and Short Description:**
- All emoji
- ★ ☆ symbols
- Repeated punctuation
- ALL CAPS (unless brand)
- Line breaks

**Everywhere:**
- HTML tags
- Store rankings ("#1 app")

**Only in Full Description:**
- Emojis (allowed and encouraged)
- Line breaks
- Unicode symbols ✓ • →

### Play Store Categories

**Apps (31):**
- Art & Design
- Auto & Vehicles
- Beauty
- Books & Reference
- Business
- Comics
- Communication
- Dating
- Education
- Entertainment
- Events
- Finance
- Food & Drink
- Health & Fitness
- House & Home
- Libraries & Demo
- Lifestyle
- Maps & Navigation
- Medical
- Music & Audio
- News & Magazines
- Parenting
- Personalization
- Photography
- Productivity
- Shopping
- Social
- Sports
- Tools
- Travel & Local
- Video Players & Editors
- Weather

**Games (17):**
- Action
- Adventure
- Arcade
- Board
- Card
- Casino
- Casual
- Educational
- Music
- Puzzle
- Racing
- Role Playing
- Simulation
- Sports
- Strategy
- Trivia
- Word

### Key Differences vs App Store

| Aspect | App Store | Play Store |
|--------|-----------|------------|
| Subtitle/Short Desc | Subtitle, 30 chars | Short Description, 80 chars |
| Keywords field | Yes, 100 chars | **No keywords field** |
| Emojis in description | Forbidden | **Allowed and encouraged** |
| What's New limit | 4000 chars | **500 chars** |
| HTML in description | No | No |
| Copyright field | Yes | No |
| App Review Notes | Yes | No |
| Content Rating | No | **Yes (suggest + IARC note)** |
| Tags | No | **Yes (up to 5)** |
| Language count | 39 locales | 51 languages / 77 locales |
| Fastlane detection | iOS paths | `fastlane/metadata/android/` |
