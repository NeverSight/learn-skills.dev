---
name: email-response-simulation
description: >
  Deep persona simulation and skeptical buyer review for cold emails.
  Builds a full prospect "world" from LinkedIn + company data, defines their
  professional reality (KPIs, pain points, inbox behavior), then runs a
  skeptical buyer roast — emotional reaction first, business evaluation second.
  One prospect at a time, Tier 1 only.
  Triggers on: "review email", "copy feedback", "email feedback",
  "would they reply", "persona review", "check this email", "review this draft",
  "roast this email", "skeptical buyer".
---

# Copy Feedback

Simulate a real prospect reading your cold email. Build their world, then roast the email through their eyes.

## Related Skills

```
email-generation → email-response-simulation → campaign-sending
```

Run this for Tier 1 prospects only — the ones worth individual attention. For Tier 2, use templates from `email-generation` directly.

## When to Use

- After `email-generation` produces a draft for a Tier 1 company
- When you want to validate whether a specific person would reply
- When you're training your instinct for a new audience before automating
- When the user says "would [name] reply to this?" or "roast this email"

## Environment

Provider selection and credentials are handled in Phase 1 of the workflow. If LinkedIn data is not available from the Extruct people table, a deep research provider is needed — the skill will ask which one to use.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| Draft email text | yes | User pastes or from `email-generation` output |
| Prospect name | yes | From contacts CSV or user input |
| Prospect company | yes | From contacts CSV or user input |
| Prospect job title | yes | From contacts CSV or user input |
| Prospect LinkedIn URL | strongly recommended | From `people-search` output |
| Hypothesis matched | recommended | From `list-segmentation` output |
| Extruct people table data | optional | LinkedIn Data column from `people-search` |

## Workflow

### Phase 1: Data Enrichment and World Building

Gather as much public data as possible, then simulate the prospect's full world.

**Step 1a: Scrape public data**

If LinkedIn data is available from the Extruct people table (linkedin_data column), use it directly. Otherwise, run research queries via the chosen deep research provider (from Environment).

**Query 1 — Professional identity:**

"Research [Name], [Title] at [Company]. Find their LinkedIn About section, career history, previous companies and roles, education, and any professional accomplishments. Include their full career arc — where they started, how they got to this role. Look at LinkedIn, company bios, conference speaker pages, and press mentions."

**Query 2 — Public voice and positions:**

"Has [Name] from [Company] written or said anything publicly? Look for LinkedIn posts, blog posts, podcast appearances, conference talks, interviews, or published articles. What topics do they engage with? What language do they use? Include direct quotes if available."

**Query 3 — Company and role context:**

"What is [Company] doing right now? Recent news, strategic initiatives, funding, product launches, or hiring signals from the last 12 months. What challenges would a [Title] at this type of company be dealing with? What does their team likely look like?"

**Step 1b: Simulate their world**

Using the research, build a vivid simulation of this person's professional reality. Go deep — the goal is to predict how they think, not just what they do.

```markdown
## World Simulation: [Name]

### Daily Reality
- **What their day looks like:** [Meetings, priorities, where they spend time]
- **Tools they live in:** [CRM, Slack, email volume, dashboards]
- **What keeps them up at night:** [The 1-2 problems they can't solve yet]

### Psychology and Decision-Making
- **Decision style:** [Data-driven / gut / consensus-seeker / authority-based]
- **Communication preference:** [Terse / detailed / formal / casual / story-driven]
- **Risk appetite:** [Early adopter / wait for proof / only buys market leaders]
- **Trust signals:** [What makes them trust a vendor — referrals, data, case studies, free trial]

### Inbox Behavior
- **Email volume:** [Estimate — 50/day? 200/day?]
- **Cold email tolerance:** [Opens most? Deletes by subject? Has assistant filter?]
- **Reply-blocking mindset:** [What makes them NOT reply even if interested]
- **What triggers a reply:** [Specific enough to feel researched, not so specific it feels creepy]
```

### Phase 2: Professional Reality

Define the parameters that determine whether your email hits or misses.

```markdown
## Professional Reality

### KPIs and Motivators
- **Measured on:** [The 2-3 KPIs their boss actually evaluates them on]
- **Career motivator:** [What they're trying to achieve — promotion, build something, stability]
- **Internal politics:** [Who do they need buy-in from? Budget authority?]

### Pain Points (ranked by severity)
1. [Most acute pain — the thing that wastes their time or blocks their goals]
2. [Second pain]
3. [Third pain]

### Relationship to Your Solution
- **Awareness level:** [Never heard of tools like this / aware of category / tried competitors]
- **Current workaround:** [How they solve this problem today without you]
- **Switching cost:** [What would they have to give up or change to use you]
```

### Phase 3: Skeptical Buyer Roast

Now put on the prospect's hat and read the email cold. Two distinct passes:

**Pass 1: Emotional Reaction (2 seconds)**

This is the gut response — before any rational evaluation. Read the email as if you're this person, scanning your inbox between meetings.

```markdown
## Emotional Reaction

**Subject line gut feel:** [What they think in 0.5 seconds]
**First sentence gut feel:** [Do they keep reading or move on?]
**Overall vibe:** [Feels like spam / feels like a human / feels like someone who gets my world]
**Immediate red flags:** [Anything that triggers "delete" instinct]
```

**Pass 2: Business Evaluation (10 seconds)**

If they made it past the emotional filter, they now evaluate the substance. This is the more calculated read.

```markdown
## Business Evaluation

**Does this hit my KPIs?** [Yes/no — and which one specifically]
**Priority level:** [Would I deal with this today, this week, this quarter, or never?]
**Bridge quality:** [How strong is the connection between my pain and their solution?]
**Credibility check:** [Do I believe this person/company can deliver?]
**Effort-to-value ratio:** [Is the CTA worth my time? What am I risking by replying?]
```

### Phase 4: Risk Flags and Refinement

Identify specific issues in the copy that reduce reply probability.

```markdown
## Risk Flags

| Flag | Location | Severity | Issue |
|------|----------|----------|-------|
| [flag type] | [P1/P2/P3/P4/subject] | [High/Med/Low] | [what's wrong] |
```

**Flag types to check:**
- **Spam trigger** — phrasing that sounds like mass email, not personal
- **Wrong pain** — opener references a problem this person doesn't actually have
- **Weak bridge** — gap between their pain and your solution is too big or too vague
- **Bad personalization** — mentions something generic disguised as personal
- **CTA mismatch** — ask is too big (meeting) or too small (nothing) for this prospect
- **Tone clash** — email tone doesn't match how this person communicates
- **Credibility gap** — proof point doesn't resonate with this type of buyer
- **Length violation** — too long for their inbox behavior

### Phase 5: Output

Present the full analysis and rewrite.

```markdown
## Copy Feedback: [Name] at [Company]

### Verdict
**Would they reply?** [Yes / Maybe / No]
**Reasoning:** [1-2 sentences — the real reason, not a polite version]

### Emotional Reaction Summary
[2-3 sentences — what they feel in the first 2 seconds]

### Business Evaluation Summary
[2-3 sentences — does it hit their KPIs, is the bridge strong]

### Risk Flags
[Table from Phase 4]

### Ranked Changes
1. **[Highest impact]**
   - Current: "[exact text]"
   - Problem: [why it fails for THIS person]
   - Rewrite: "[new text]"

2. **[Second]**
   - Current: ...
   - Problem: ...
   - Rewrite: ...

3. **[Third]**
   ...

### Rewritten Email
[Full email with all changes applied]
```

### Phase 6: Iterate

After presenting, ask:
- "Want to adjust any of the changes?"
- "Want to run another prospect through the same email template?"
- "Ready to finalize?"

Repeat Phases 3-5 until the user is satisfied.

## Running One by One vs. Template Training

**One by one (primary use):** Run this for each Tier 1 prospect individually. The value prop, opener, and CTA should be tailored to their specific role and world.

**Template training (secondary use):** Even running 3-5 prospects through this process teaches you patterns about the audience. After a few roasts, you'll notice:
- Which pain points consistently hit
- Which CTAs work for which seniority
- Which proof points resonate with which role type
- What inbox behavior looks like for this ICP

Use these patterns to improve the base template in `email-generation` for Tier 2 prospects.

## Guidelines

- **Never invent persona details.** If research doesn't find something, say "unknown" and reason from the role/title instead.
- **Be brutally honest.** If the email will be deleted, say so. Sugarcoating wastes the user's time.
- **The emotional reaction is primary.** Most cold emails are killed in 2 seconds. The business case only matters if they survive the gut check.
- **Respect the voice rules.** All rewrites must stay within the voice constraints from `email-generation` / `email-prompt-building`.
- **One email, one prospect.** Never run in bulk. The whole point is depth.
- **The bridge is everything.** The gap between "their pain" and "your solution" is where most emails fail. If the bridge is weak, no amount of copywriting fixes it — the hypothesis match might be wrong.

## Reference

See [references/persona-review-template.md](references/persona-review-template.md) for the full output template and red flag checklist.
