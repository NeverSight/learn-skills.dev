---
name: iblai-marketing-form-cro
description: When the user wants to optimize any form that is NOT signup/registration — including lead capture forms, contact forms, demo request forms, application forms, survey forms, or checkout forms. Also use when the user mentions "form optimization," "lead form conversions," "form friction," "form fields," "form completion rate," "contact form," "nobody fills out our form," "form abandonment," "too many fields," "demo request form," or "lead form isn't converting." Use this for any non-signup form that captures information. For signup/registration forms, see iblai-marketing-signup-flow-cro. For popups containing forms, see iblai-marketing-popup-cro.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-form-cro

Maximize form completion rates while capturing only the data that matters.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Identify before optimizing:

1. **Form type**
   - Lead capture (gated content, newsletter)
   - Contact
   - Demo/sales request
   - Application
   - Survey/feedback
   - Checkout
   - Quote request

2. **Current state**
   - Field count
   - Current completion rate
   - Mobile vs. desktop split
   - Where users abandon

3. **Business context**
   - What happens with submissions
   - Which fields actually get used in follow-up
   - Compliance / legal requirements

---

## Core Principles

### 1. Every Field Has a Cost

Each field reduces completion. Rule of thumb:
- 3 fields: baseline
- 4-6 fields: 10-25% reduction
- 7+ fields: 25-50%+ reduction

Per field, ask:
- Absolutely necessary before we can help them?
- Can we get this info another way?
- Can we ask for it later?

### 2. Value Must Exceed Effort

- Clear value prop above the form
- Make what they get obvious
- Reduce perceived effort (field count, labels)

### 3. Reduce Cognitive Load

- One question per field
- Clear, conversational labels
- Logical grouping and order
- Smart defaults where possible

---

## Field-by-Field Optimization

### Email
- Single field, no confirmation
- Inline validation
- Typo detection ("did you mean gmail.com?")
- Proper mobile keyboard

### Name
- Single "Name" vs. First/Last — test it
- Single field reduces friction
- Split only if personalization requires it

### Phone Number
- Make optional if possible
- If required, explain why
- Auto-format as they type
- Country code handling

### Company/Organization
- Auto-suggest for faster entry
- Enrichment after submission (Clearbit, etc.)
- Consider inferring from email domain

### Job Title/Role
- Dropdown if categories matter
- Free text if wide variation
- Consider making optional

### Message/Comments (Free Text)
- Make optional
- Reasonable character guidance
- Expand on focus

### Dropdown Selects
- "Select one..." placeholder
- Searchable if many options
- Radio buttons if < 5 options
- "Other" option with text field

### Checkboxes (Multi-Select)
- Clear, parallel labels
- Reasonable number of options
- "Select all that apply" instruction

---

## Form Layout

### Field Order

1. Start with easiest fields (name, email)
2. Build commitment before asking more
3. Sensitive fields last (phone, company size)
4. Logical grouping when many fields

### Labels and Placeholders

- Labels: keep visible (not just placeholder) — placeholders disappear when typing, leaving users unsure what they're filling
- Placeholders: examples, not labels
- Help text: only when genuinely helpful

**Good:**
```
Email
[name@company.com]
```

**Bad:**
```
[Enter your email address]  ← Disappears on focus
```

### Visual Design

- Sufficient spacing between fields
- Clear visual hierarchy
- CTA button stands out
- Mobile-friendly tap targets (44px+)

### Single Column vs. Multi-Column

- Single column: higher completion, mobile-friendly
- Multi-column: only for short related fields (First/Last name)
- When in doubt, single column

---

## Multi-Step Forms

### When to Use

- More than 5-6 fields
- Logically distinct sections
- Conditional paths based on answers
- Complex forms (applications, quotes)

### Best Practices

- Progress indicator (step X of Y)
- Start easy, end sensitive
- One topic per step
- Allow back navigation
- Save progress (don't lose data on refresh)
- Indicate required vs. optional clearly

### Progressive Commitment Pattern

1. Low-friction start (just email)
2. More detail (name, company)
3. Qualifying questions
4. Contact preferences

---

## Error Handling

### Inline Validation

- Validate as they leave a field
- Don't validate too aggressively while typing
- Clear visual indicators (green check, red border)

### Error Messages

- Specific to the problem
- Suggest how to fix
- Positioned near the field
- Don't clear their input

**Good:** "Please enter a valid email address (e.g., name@company.com)"
**Bad:** "Invalid input"

### On Submit

- Focus on first error field
- Summarize errors if multiple
- Preserve all entered data
- Don't clear the form on error

---

## Submit Button

### Copy

Weak: "Submit" | "Send"
Strong: "[Action] + [What they get]"

Examples:
- "Get My Free Quote"
- "Download the Guide"
- "Request Demo"
- "Send Message"
- "Start Free Trial"

### Placement

- Immediately after the last field
- Left-aligned with fields
- Sufficient size and contrast
- Mobile: sticky or clearly visible

### Post-Submit States

- Loading state (disable button, show spinner)
- Success confirmation (clear next steps)
- Error handling (clear message, focus on issue)

---

## Trust and Friction Reduction

### Near the Form

- Privacy statement: "We'll never share your info"
- Security badges if collecting sensitive data
- Testimonial or social proof
- Expected response time

### Reducing Perceived Effort

- "Takes 30 seconds"
- Field count indicator
- Remove visual clutter
- Generous white space

### Addressing Objections

- "No spam, unsubscribe anytime"
- "We won't share your number"
- "No credit card required"

---

## Form Types: Specific Guidance

### Lead Capture (Gated Content)

- Minimum viable fields (often just email)
- Clear value prop for what they get
- Ask enrichment questions post-download
- Test email-only vs. email + name

### Contact Form

- Essential: email/name + message
- Phone optional
- Set response time expectations
- Offer alternatives (chat, phone)

### Demo Request

- Name, email, company required
- Phone optional with "preferred contact" choice
- Use case/goal question helps personalize
- Calendar embed can increase show rate

### Quote/Estimate Request

- Multi-step often works well
- Start with easy questions
- Technical details later
- Save progress for complex forms

### Survey Forms

- Progress bar essential
- One question per screen
- Skip logic for relevance
- Consider an incentive for completion

---

## Mobile

- Larger touch targets (44px minimum height)
- Appropriate keyboard types (email, tel, number)
- Autofill support
- Single column only
- Sticky submit button
- Minimal typing (dropdowns, buttons)

---

## Measurement

### Key Metrics

- **Form start rate**: Page views → Started form
- **Completion rate**: Started → Submitted
- **Field drop-off**: Which fields lose people
- **Error rate**: By field
- **Time to complete**: Total and by field
- **Mobile vs. desktop**: Completion by device

### What to Track

- Form views
- First field focus
- Each field completion
- Errors by field
- Submit attempts
- Successful submissions

---

## Output Format

### Form Audit

Per issue:
- **Issue**: what's wrong
- **Impact**: estimated effect on conversions
- **Fix**: specific recommendation
- **Priority**: High/Medium/Low

### Recommended Form Design

- **Required fields**: justified list
- **Optional fields**: with rationale
- **Field order**: recommended sequence
- **Copy**: labels, placeholders, button
- **Error messages**: per field
- **Layout**: visual guidance

### Test Hypotheses
Ideas to A/B test with expected outcomes.

---

## Experiment Ideas

### Form Structure

**Layout & Flow**
- Single-step vs. multi-step with progress bar
- 1-column vs. 2-column field layout
- Form embedded on page vs. separate page
- Vertical vs. horizontal field alignment
- Form above fold vs. after content

**Field Optimization**
- Reduce to minimum viable fields
- Add or remove phone number
- Add or remove company/organization
- Required vs. optional balance
- Field enrichment to auto-fill known data
- Hide fields for returning/known visitors

**Smart Forms**
- Real-time validation for emails and phone numbers
- Progressive profiling (ask more over time)
- Conditional fields based on earlier answers
- Auto-suggest for company names

---

### Copy & Design

**Labels & Microcopy**
- Field label clarity and length
- Placeholder text optimization
- Help text: show vs. hide vs. on-hover
- Error message tone (friendly vs. direct)

**CTAs & Buttons**
- Button text variations ("Submit" vs. "Get My Quote" vs. specific action)
- Button color and size
- Button placement relative to fields

**Trust Elements**
- Privacy assurance near form
- Trust badges next to submit
- Testimonial near form
- Expected response time

---

### Form Type-Specific

**Demo Request Forms**
- With/without phone number requirement
- "Preferred contact method" choice
- "What's your biggest challenge?" question
- Calendar embed vs. form submission

**Lead Capture Forms**
- Email-only vs. email + name
- Value proposition messaging above form
- Gated vs. ungated content strategies
- Post-submission enrichment questions

**Contact Forms**
- Department/topic routing dropdown
- With/without message field requirement
- Alternative contact methods (chat, phone)
- Expected response time messaging

---

### Mobile & UX

- Larger touch targets for mobile
- Appropriate keyboard types by field
- Sticky submit button on mobile
- Auto-focus first field on page load
- Form container styling (card vs. minimal)

---

## Task-Specific Questions

1. Current form completion rate?
2. Field-level analytics?
3. What happens with the data after submission?
4. Which fields actually used in follow-up?
5. Compliance/legal requirements?
6. Mobile vs. desktop split?

---

## Related Skills

- **iblai-marketing-signup-flow-cro**: Account creation forms
- **iblai-marketing-popup-cro**: Forms inside popups/modals
- **iblai-marketing-page-cro**: The page containing the form
- **iblai-marketing-ab-test-setup**: Testing form changes
