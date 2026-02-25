---
name: ux-writing
description: Master UX writing - microcopy, voice and tone, error messages, CTAs, content strategy
sasmp_version: "1.3.0"
bonded_agent: 07-ux-writing
bond_type: PRIMARY_BOND
---

# UX Writing Skill

> **Atomic Skill**: Craft clear, concise, and helpful content that guides users through experiences

## Purpose

This skill provides frameworks for writing effective interface copy and establishing content systems.

## Skill Invocation

```
Skill("custom-plugin-ux-design:ux-writing")
```

## Parameter Schema

### Input Parameters
```typescript
interface UXWritingParams {
  // Required
  task: "microcopy" | "voice_tone" | "errors" | "ctas" | "audit";
  context: string;

  // Optional
  brand_voice?: {
    personality: string[];
    formality: "formal" | "neutral" | "casual";
  };
  constraints?: {
    character_limit?: number;
    localization?: string[];
  };
  emotional_context?: "neutral" | "frustrated" | "excited" | "confused";
}
```

### Validation Rules
```yaml
task:
  type: enum
  required: true
  values: [microcopy, voice_tone, errors, ctas, audit]

context:
  type: string
  required: true
  min_length: 10

constraints.character_limit:
  type: number
  min: 1
  max: 500
```

## Execution Flow

```
UX WRITING EXECUTION
────────────────────────────────────────────

Step 1: UNDERSTAND CONTEXT
├── Identify user goal
├── Define emotional context
└── Note constraints

Step 2: APPLY VOICE
├── Match brand voice
├── Adjust tone for context
└── Consider localization

Step 3: DRAFT CONTENT
├── Write initial version
├── Create alternatives
└── Check constraints

Step 4: REFINE
├── Simplify language
├── Remove jargon
├── Verify clarity

Step 5: VALIDATE
├── Test with users
├── Check accessibility
└── Document patterns

────────────────────────────────────────────
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff_type: linear
  initial_delay_ms: 500
  max_delay_ms: 3000
  retryable_errors:
    - TONE_MISMATCH
    - LIMIT_EXCEEDED
```

## Logging Hooks

```typescript
interface UXWritingLog {
  timestamp: string;
  event: "draft_created" | "refined" | "approved";
  content_type: string;
  character_count: number;
  readability_score: number;
  alternatives_generated: number;
}
```

## Learning Modules

### Module 1: Microcopy Fundamentals
```
MICROCOPY TYPES
├── Button labels
├── Form labels
├── Placeholder text
├── Helper text
├── Error messages
├── Success messages
├── Loading states
├── Empty states
├── Tooltips
└── Notifications

WRITING PRINCIPLES
├── Clarity over cleverness
├── Concise but complete
├── Action-oriented
├── User-focused
└── Consistent
```

### Module 2: Voice & Tone
```
VOICE DIMENSIONS
├── Personality traits
│   ├── Friendly vs Professional
│   ├── Playful vs Serious
│   └── Casual vs Formal
├── Vocabulary choices
│   ├── Technical level
│   ├── Brand-specific terms
│   └── Inclusive language
└── Sentence structure
    ├── Active voice
    ├── Sentence length
    └── Punctuation style

TONE ADAPTATION
├── Neutral context: Standard voice
├── Frustrated user: Empathetic, helpful
├── Excited user: Match energy
├── Confused user: Clear, guiding
└── Error situation: Calm, actionable
```

### Module 3: Error Messages
```
ERROR MESSAGE STRUCTURE
├── What happened (clear, honest)
├── Why it happened (if helpful)
└── What to do next (actionable)

ERROR TONE GUIDELINES
├── Never blame the user
├── Be specific, not vague
├── Offer a solution
├── Use plain language
└── Keep it brief

EXAMPLES
Bad: "Error 500"
Good: "We couldn't save your changes. Please try again."

Bad: "Invalid input"
Good: "Email addresses need an @ symbol"

Bad: "Something went wrong"
Good: "We couldn't load your files. Check your connection and refresh."
```

### Module 4: CTAs & Buttons
```
CTA PRINCIPLES
├── Start with action verb
├── Be specific about outcome
├── Keep it short (2-4 words)
├── Match user expectation
└── Create appropriate urgency

ACTION VERBS BY CONTEXT
├── Creation: Create, Add, New
├── Continuation: Continue, Next
├── Confirmation: Save, Submit, Confirm
├── Navigation: Go, Open, View
├── Communication: Send, Share, Invite
└── Removal: Delete, Remove, Cancel

PRIMARY vs SECONDARY
├── Primary: Main action (emphasized)
├── Secondary: Alternative action
└── Tertiary: Escape/cancel
```

### Module 5: Content Strategy
```
CONTENT PATTERNS
├── Consistent terminology
├── Reusable content blocks
├── Scalable voice system
└── Localization-ready

CONTENT GOVERNANCE
├── Style guide
├── Terminology glossary
├── Approval workflow
├── Update process
└── Quality metrics
```

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `UXW-001` | Jargon detected | Suggest plain language |
| `UXW-002` | Tone mismatch | Realign with voice |
| `UXW-003` | CTA unclear | Strengthen verb |
| `UXW-004` | Error unhelpful | Add action steps |
| `UXW-005` | Limit exceeded | Prioritize, truncate |

## Writing Formulas

### Error Messages
```
[Acknowledge] + [Explain (if helpful)] + [Action]

"We couldn't save your file. It may be too large.
Try reducing the size or contact support."
```

### Empty States
```
[What would be here] + [How to add it]

"No messages yet. Start a conversation by tapping New Message."
```

### Loading States
```
[What's happening] + [Progress (if known)]

"Loading your dashboard..."
"Uploading file (3 of 5)..."
```

## Troubleshooting

### Problem: Users misunderstand labels
```
Diagnosis:
├── Check: Jargon usage
├── Check: Context clarity
├── Check: Consistency
└── Solution: Simplify

Steps:
1. Test with real users
2. Replace technical terms
3. Add helper text
4. A/B test alternatives
```

### Problem: CTAs have low engagement
```
Diagnosis:
├── Check: Verb strength
├── Check: Value clarity
├── Check: Visual prominence
└── Solution: Optimize copy

Steps:
1. Use stronger action verbs
2. Clarify the outcome
3. Test alternatives
4. Consider placement
```

## Unit Test Templates

```typescript
describe("UXWritingSkill", () => {
  describe("microcopy generation", () => {
    it("should meet character limit", async () => {
      const result = await invoke({
        task: "microcopy",
        context: "button label",
        constraints: { character_limit: 20 }
      });
      expect(result.text.length).toBeLessThanOrEqual(20);
    });
  });

  describe("error messages", () => {
    it("should include actionable step", async () => {
      const result = await invoke({
        task: "errors",
        context: "file upload failed"
      });
      expect(result.message).toMatch(/try|check|contact/i);
    });

    it("should not blame user", async () => {
      const result = await invoke({
        task: "errors",
        context: "invalid input"
      });
      expect(result.message).not.toMatch(/you|your mistake/i);
    });
  });

  describe("readability", () => {
    it("should score grade 8 or lower", async () => {
      const result = await invoke({
        task: "microcopy",
        context: "onboarding instructions"
      });
      expect(result.readability.grade_level).toBeLessThanOrEqual(8);
    });
  });
});
```

## Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Readability | Grade 8 | Flesch-Kincaid |
| Task completion | > 95% | User testing |
| Error recovery | > 90% | Recovery rate |
| Consistency | 100% | Terminology audit |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-30 | Production-grade upgrade |
