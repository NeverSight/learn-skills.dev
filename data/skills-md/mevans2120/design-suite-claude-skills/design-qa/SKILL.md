---
name: design-qa
description: Reviews finished and in-progress digital products to assess adherence to design specifications and discover potential issues. Use when user says "design review", "design QA", "QA review", "check implementation", "visual bugs", "compare to design", "match the specs", "review the build", "before launch", "pre-launch review", "implementation review", "verify design", "design validation", "spacing issues", "visual discrepancies", "accessibility review", "WCAG compliance", or "responsive testing". Validates implementation against design intent, identifies visual and interaction discrepancies, and provides actionable feedback. Do NOT use when still designing concepts (use design-concepts), need to understand users (use design-research), or nothing has been built yet.
---

# Design - QA

This skill guides Claude through systematic design quality assurance - reviewing implemented products against design specifications, brand guidelines, and best practices to ensure high-quality execution.

## Core Methodology

### Purpose of Design QA
Design QA serves multiple purposes:
- **Validation**: Confirm implementation matches design specifications
- **Quality Control**: Catch visual and interaction bugs before users do
- **Spec Improvement**: Identify gaps or ambiguities in design documentation
- **Consistency**: Ensure brand and design system adherence
- **Accessibility**: Verify WCAG compliance and inclusive design

### Design QA is NOT User Testing
This skill focuses on design implementation, not user experience validation:
- ✅ "Does this button match the spec?"
- ✅ "Is spacing consistent across screens?"
- ✅ "Do hover states work correctly?"
- ❌ "Do users understand this flow?" (That's user research)

### Design QA Process
1. **Review Preparation**: Gather specs, guidelines, context
2. **Systematic Review**: Check implementation against specifications
3. **Issue Documentation**: Log discrepancies with clear evidence
4. **Severity Assessment**: Prioritize issues by impact
5. **Feedback Delivery**: Provide actionable recommendations
6. **Validation**: Confirm fixes meet specifications

## Tool Usage Patterns

### Initial Setup & Context Gathering

**Step 1: Collect Reference Materials**
```
Questions to ask user:
1. What product/feature are we reviewing?
2. Where can I access it? (URL, staging link, screenshots)
3. Do you have design specs or Figma files?
4. Are there brand guidelines to check against?
5. Any specific concerns or focus areas?
6. What's the review scope? (specific screens/flows or full product)

Use `view` to read:
- Design specification documents
- Design system documentation
- Brand guidelines
- Previous QA reports (if any)

Use `web_fetch` to:
- Load the live product/staging site
- Analyze HTML, CSS, interactions
- Test responsive behavior
```

**Step 2: Understand the Specification**
Before reviewing implementation:
- Read design specs completely
- Note all specified states (hover, active, focus, disabled, loading, error)
- Identify defined interactions and animations
- Review responsive breakpoints
- Check accessibility requirements
- List any open questions or ambiguities

### Conducting Systematic Review

**Visual Design Review**:
```
For each screen/component:
1. Layout & Spacing
   - Compare actual spacing to spec
   - Check alignment and grid adherence
   - Verify padding and margins

2. Typography
   - Font family, size, weight, line height
   - Text color and contrast
   - Hierarchy and consistency

3. Colors
   - Background colors match design tokens
   - Text colors meet contrast requirements
   - Interactive elements use correct states

4. Visual Elements
   - Icons correct size and style
   - Images display at correct resolution
   - Borders, shadows, radius match spec

5. Components
   - Match design system patterns
   - Consistent across screens
   - All variants implemented correctly
```

**Interaction Review**:
```
For each interactive element:
1. States
   - Default, hover, active, focus, disabled
   - Loading and success states
   - Error states and validation

2. Animations & Transitions
   - Duration matches spec
   - Easing function correct
   - Performance (no jank or lag)

3. Behavior
   - Click/tap responses correctly
   - Keyboard navigation works
   - Focus order logical
   - Modals/overlays function properly
```

**Responsive Design Review**:
```
Test at multiple breakpoints:
- Mobile (320px, 375px, 414px)
- Tablet (768px, 1024px)
- Desktop (1280px, 1440px, 1920px)

Check for:
- Layout adaptation matches spec
- Content reflow works properly
- Touch targets adequate on mobile (min 44x44 / 48x48)
- No horizontal scrolling (unless intentional)
- Images scale appropriately
```

**Accessibility Review**:
```
Keyboard Navigation:
- Tab order logical
- All interactive elements focusable
- Focus indicators visible
- Escape/Enter work as expected

Screen Reader:
- Alt text on images
- Form labels associated
- ARIA labels where needed
- Error messages announced

Color & Contrast:
- Text contrast 4.5:1 minimum
- UI elements 3:1 minimum
- Test with color blindness simulation
- Don't rely on color alone

Content:
- Headings hierarchical (h1, h2, h3)
- Links descriptive
- Button text meaningful
- Form errors clear
```

### Issue Documentation

**Issue Report Structure**:
```markdown
## [Issue Title] - [Severity]

**Location**: [Screen name / Component name / URL]

**Expected** (per spec):
[What the design spec says should happen]
[Include screenshot from Figma or design file]

**Actual** (implementation):
[What actually appears/happens]
[Include screenshot or video of implementation]

**Discrepancy**:
[Specific difference, with measurements if applicable]
Example: "Button padding is 8px instead of specified 12px"

**Impact**: [How this affects user experience or brand]

**Recommendation**: [Specific fix needed]

**Severity**: [Critical / High / Medium / Low]

**Device/Browser**: [Where issue was observed]
```

### Severity Assessment

**Critical** (Must fix before launch):
- Broken functionality (buttons don't work, forms don't submit)
- Accessibility violations preventing use (keyboard trap, missing alt text on critical images)
- Major brand violations (wrong logo, off-brand colors prominently)
- Data loss or security issues

**High** (Should fix before launch):
- Significant visual discrepancies (wrong colors, incorrect spacing system-wide)
- Inconsistent component usage (different button styles for same actions)
- Accessibility issues affecting many users (poor contrast, confusing navigation)
- Broken responsive behavior on common devices

**Medium** (Fix in next sprint):
- Minor visual discrepancies (slightly off spacing on one screen)
- Missing micro-interactions specified in design
- Inconsistent hover states
- Accessibility improvements (better focus indicators)

**Low** (Nice to have):
- Very minor spacing tweaks
- Animation polish
- Edge case visual issues
- Non-critical enhancement suggestions

## Quality Criteria

### Excellent Design QA Reports:
- **Systematic**: Reviews all aspects (visual, interaction, responsive, accessibility)
- **Evidence-based**: Screenshots, measurements, specific examples
- **Actionable**: Clear recommendations, not just "doesn't match"
- **Prioritized**: Severity levels help teams focus on what matters
- **Fair**: Acknowledges spec gaps, doesn't blame implementation for unclear designs
- **Complete**: Covers all specified screens and states
- **Constructive**: Frames issues as opportunities to improve

### Excellent Issue Documentation:
- **Specific**: "Padding 8px instead of 12px" not "spacing is wrong"
- **Visual**: Screenshots showing expected vs. actual
- **Contextual**: Explains why it matters, not just that it's different
- **Solution-oriented**: Suggests fix, not just problem
- **Traceable**: Links back to specific line in design spec

## Deliverable Formats

### File Organization

**IMPORTANT: Organize all deliverables by feature/assignment in dated folders.**

Each QA review project should be saved in its own folder with the feature name:
`docs/design/{feature-name}-qa-{MMDDYY}/`

**Feature Name Guidelines:**
- Use kebab-case (lowercase with hyphens)
- Examples: `checkout-flow`, `user-profile`, `dashboard-redesign`, `search-filters`
- Ask the user for the feature name if not provided
- Suggest a name based on their description if needed

**Examples:**
- Checkout flow QA review on Oct 24, 2025: `docs/design/checkout-flow-qa-102425/`
- Checkout flow post-fixes QA on Nov 1, 2025: `docs/design/checkout-flow-qa-110125/`
- User profile QA on Nov 10, 2025: `docs/design/user-profile-qa-111025/`

**Rationale:**
- **Immediate clarity**: Know what feature each QA review relates to
- **Version history**: Same feature can have multiple dated QA reviews
- **No conflicts**: Different features can have same-named files
- **Clear tracking**: Which issues correspond to which feature/build
- **Organized**: All QA artifacts for one feature stay together

**Folder structure:**
```
docs/design/{feature-name}-qa-{MMDDYY}/
├── {feature-name}-qa-report.md
├── {feature-name}-issues.csv
├── {feature-name}-spec-improvements.md
└── {feature-name}-screenshots/
    ├── issue-001-button-spacing.png
    ├── issue-002-color-contrast.png
    └── expected-vs-actual-comparison.png
```

### Design QA Report
**Location**: `docs/design/{feature-name}-qa-{MMDDYY}/`
**File**: `{feature-name}-qa-report.md`
**Format**: Markdown with embedded screenshots
**Structure**:
```markdown
# Design QA Report: [Feature Name]
**Date**: [Date]
**Reviewer**: Claude (Design QA Skill)
**Scope**: [What was reviewed]

## Executive Summary
- Total issues found: [Number]
- Critical: [Number]
- High: [Number]
- Medium: [Number]
- Low: [Number]
- Overall assessment: [Ready to ship / Needs work / Major issues]

## Key Findings
1. [Most important issue or pattern]
2. [Second most important]
3. [Third most important]

## Detailed Issues

### Critical Issues
[List of critical issues with full documentation]

### High Priority Issues
[List of high priority issues]

### Medium Priority Issues
[List of medium priority issues]

### Low Priority Issues
[List of low priority issues]

## Specification Gaps
[Issues caused by ambiguous or missing specs]

## Positive Observations
[Things that were implemented well]

## Recommendations
1. [Top recommendation]
2. [Second recommendation]
3. [Third recommendation]

## Next Steps
- [ ] Address critical issues
- [ ] Review high priority fixes
- [ ] Update design specs based on gaps found
- [ ] Schedule follow-up QA review
```

### Issue Tracking Spreadsheet
**Location**: `docs/design/{feature-name}-qa-{MMDDYY}/`
**File**: `{feature-name}-issues.csv`
**Format**: CSV for import to project management tools
**Columns**:
- Issue ID
- Severity
- Status (Open/In Progress/Fixed/Won't Fix)
- Screen/Component
- Issue Description
- Expected Behavior
- Actual Behavior
- Assigned To
- Date Found
- Date Fixed

### Design Specification Feedback
**Location**: `docs/design/{feature-name}-qa-{MMDDYY}/`
**File**: `{feature-name}-spec-improvements.md`
**Format**: Markdown with specific suggestions
**Purpose**: Help improve design documentation for future projects

## Examples

### Good vs. Poor Issue Documentation

❌ **Poor Issue**:
```
The button is wrong
- Doesn't look right
- Fix it
```

✅ **Good Issue**:
```markdown
## Primary CTA Button Padding Incorrect - High

**Location**: Checkout page, "Complete Purchase" button

**Expected** (per spec):
- Padding: 12px vertical, 24px horizontal
- Button height: 48px

**Actual** (implementation):
- Padding: 8px vertical, 16px horizontal  
- Button height: 40px

**Discrepancy**:
Button is 8px shorter and appears cramped. Touch target falls below recommended 44x44px minimum for mobile.

**Impact**: 
- Reduced tappability on mobile devices
- Inconsistent with other primary CTAs
- Less visual prominence for primary action

**Recommendation**: 
Update button CSS to use design token `py-3 px-6` (12px/24px) to match specification and design system.

**Severity**: High (affects primary conversion action and mobile usability)

**Device/Browser**: All devices, Chrome 118
```

### Good Pattern Recognition Example

```markdown
## Pattern Found: Inconsistent Spacing System

**Observation**:
Multiple screens use spacing values outside the design system:
- Profile page: 14px gap between fields (should be 12px or 16px)
- Settings: 20px section margin (should be 16px or 24px)
- Dashboard: 10px card padding (should be 12px or 16px)

**Root Cause**:
Design specification didn't explicitly reference the 4px/8px spacing scale.

**Impact**:
Visual inconsistency, harder to maintain, accessibility issues with unpredictable spacing.

**Recommendation**:
1. Update all spacing to use design tokens (spacing scale)
2. Add spacing scale reference to design spec
3. Create CSS variables for spacing tokens
```

## Common Pitfalls to Avoid

### ❌ Nitpicking Minor Differences
**Problem**: Logging dozens of 1px differences that don't matter
**Instead**: Focus on issues that affect user experience or brand consistency

### ❌ Blaming Without Context
**Problem**: "Engineer did it wrong" without checking if spec was clear
**Instead**: Ask "Was the spec clear?" and improve documentation

### ❌ Vague Issue Descriptions
**Problem**: "Doesn't look right" or "spacing is off"
**Instead**: Provide specific measurements and comparisons

### ❌ Missing Screenshots/Evidence
**Problem**: Describing issues in text only
**Instead**: Show expected vs. actual with visual evidence

### ❌ Ignoring Accessibility
**Problem**: Only checking visual appearance
**Instead**: Always review keyboard navigation, screen reader, and contrast

### ❌ No Prioritization
**Problem**: All issues treated equally, overwhelming dev team
**Instead**: Use clear severity levels to guide prioritization

### ❌ Reviewing in Only One Context
**Problem**: Only testing on desktop Chrome
**Instead**: Review across devices, browsers, and screen sizes

### ❌ Not Acknowledging Good Work
**Problem**: Only pointing out problems
**Instead**: Note what was implemented well, builds morale

### ❌ Unrealistic Expectations
**Problem**: Expecting pixel-perfect match on all browsers/devices
**Instead**: Understand technical constraints and browser differences

## Integration Points

### Inputs from Other Teams
- **Design Specs**: Design specifications, Figma files, brand guidelines
- **Engineering**: Staging/development URLs, build status, technical constraints
- **Product/PM**: Feature requirements, business priorities, launch timeline
- **Design Research**: User needs context (to assess impact of issues)

### Outputs for Other Teams
- **Engineering**: Prioritized issue list with specific fixes needed
- **Product/PM**: Go/no-go recommendation based on issue severity
- **Leadership**: Summary of quality status and risks

### Related Skills
- May surface issues requiring **design-concepts** rethinking
- Uses **design-research** insights to assess user impact of issues

## Review Checklists

### Pre-Review Checklist
Before starting QA review:
- [ ] Design specifications gathered and reviewed
- [ ] Design system documentation available
- [ ] Brand guidelines referenced
- [ ] Access to product/staging environment confirmed
- [ ] Review scope clearly defined
- [ ] Previous QA reports reviewed (if any)

### Visual Design Checklist
For each screen:
- [ ] Layout matches specification
- [ ] Spacing uses design system scale
- [ ] Typography correct (family, size, weight, line height)
- [ ] Colors match design tokens
- [ ] Alignment and grid adherence
- [ ] Icons correct size and style
- [ ] Images display correctly
- [ ] Borders, shadows, radius match spec
- [ ] Component consistency across screens

### Interaction Checklist
For each interactive element:
- [ ] Default state correct
- [ ] Hover state works
- [ ] Active/pressed state works
- [ ] Focus state visible
- [ ] Disabled state correct
- [ ] Loading state implemented
- [ ] Error state implemented
- [ ] Success state implemented
- [ ] Transitions/animations match spec
- [ ] Performance smooth (no jank)

### Responsive Checklist
At each breakpoint:
- [ ] Layout adapts correctly
- [ ] Content reflows properly
- [ ] Touch targets adequate (mobile)
- [ ] No horizontal scroll (unless intentional)
- [ ] Images scale appropriately
- [ ] Navigation works on mobile
- [ ] Forms usable on small screens
- [ ] Modals/overlays responsive

### Accessibility Checklist
- [ ] Keyboard navigation works
- [ ] Tab order logical
- [ ] Focus indicators visible
- [ ] Escape/Enter function correctly
- [ ] Alt text on images
- [ ] Form labels associated
- [ ] ARIA labels where needed
- [ ] Error messages clear and announced
- [ ] Text contrast 4.5:1 minimum
- [ ] UI element contrast 3:1 minimum
- [ ] Headings hierarchical
- [ ] Links descriptive
- [ ] No color-only information

### Browser/Device Testing Checklist
Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)
- [ ] Common screen sizes (320px, 768px, 1440px)

## Tips for Best Results

1. **Review with design specs open** - Don't rely on memory
2. **Use browser dev tools** - Measure actual spacing, check CSS
3. **Test all interactive states** - Don't assume if you can't see it
4. **Check responsive behavior** - Use dev tools device simulation
5. **Use accessibility testing tools** - Lighthouse, WAVE, axe DevTools
6. **Take lots of screenshots** - Visual evidence is compelling
7. **Be systematic** - Follow checklist, don't skip screens
8. **Focus on user impact** - Prioritize issues that matter most
9. **Be constructive** - Frame issues as improvement opportunities
10. **Document spec gaps** - Help improve design documentation

## Advanced Techniques

### Automated Checks (when possible)
```bash
# Use Lighthouse for accessibility and performance
npm install -g lighthouse
lighthouse [URL] --output=html --view

# Use Percy or Chromatic for visual regression testing
# (requires setup and integration)

# Check color contrast programmatically
# Use tools like Colorable or Contrast Checker
```

### Pattern Analysis
Look for systemic issues:
- Are all buttons inconsistent, or just one?
- Is spacing wrong everywhere, or specific screens?
- Are issues concentrated in one area (e.g., forms)?

This helps identify root causes vs. one-off bugs.

### Comparative Review
Compare against:
- Design system examples
- Previous versions of the product
- Competitor implementations
- Platform conventions (iOS HIG, Material Design)

## Validation Checklist

Before submitting QA report:
- [ ] All in-scope screens reviewed
- [ ] All interactive elements tested
- [ ] Responsive behavior checked
- [ ] Accessibility reviewed
- [ ] Issues documented with evidence
- [ ] Severity levels assigned
- [ ] Recommendations provided
- [ ] Specification gaps noted
- [ ] Positive observations included
- [ ] Report is actionable and constructive
- [ ] Files saved to project's `docs/design/` directory
- [ ] CSV issue tracker included (if requested)

## Sample QA Report Excerpt

```markdown
# Design QA Report: E-commerce Checkout Flow

**Date**: October 22, 2025
**Reviewer**: Claude (Design QA Skill)
**Scope**: Complete checkout flow (cart → shipping → payment → confirmation)

## Executive Summary
- **Total issues found**: 23
- **Critical**: 1
- **High**: 4
- **Medium**: 12
- **Low**: 6
- **Overall assessment**: Needs work - address critical and high issues before launch

## Key Findings
1. Payment form submit button non-functional on mobile Safari (Critical)
2. Inconsistent spacing throughout flow - not using design system scale
3. Missing error states for invalid payment info
4. Color contrast issues on several form labels

## Detailed Issues

### Critical Issues

#### 1. Payment Submit Button Non-Functional on Mobile Safari - CRITICAL

**Location**: Payment page, "Complete Purchase" button (iOS Safari 17)

**Expected**: Button triggers payment processing when tapped

**Actual**: Button does not respond to tap on mobile Safari. Works on desktop and Chrome mobile.

**Evidence**: [Screenshot showing button]

**Impact**: Complete checkout flow blocker for iOS users (approximately 30% of mobile traffic).

**Recommendation**: 
- Check for JavaScript errors in Safari console
- Verify touch event handlers attached correctly
- Test with minimal CSS to isolate issue
- May need `-webkit-appearance: none` or explicit touch event handling

**Severity**: CRITICAL - breaks core functionality for large user segment

---

### High Priority Issues

#### 2. Shipping Form Spacing Inconsistent - HIGH

**Location**: Shipping address form

**Expected** (per design spec):
- Form field spacing: 16px vertical gap
- Label to input: 4px gap
- Section spacing: 24px

**Actual**:
- Form field spacing: 14px, 18px, 12px (varies)
- Label to input: 6px, 8px (inconsistent)
- Section spacing: 20px

**Evidence**: [Screenshot with measurements]

**Impact**: 
- Visual inconsistency reduces polish
- Harder to maintain (no systematic spacing)
- Misalignment with design system used elsewhere

**Recommendation**: 
Update CSS to use design tokens:
- `space-y-4` for form fields (16px)
- `space-y-1` for label-to-input (4px)
- `space-y-6` for sections (24px)

**Severity**: HIGH - affects visual consistency system-wide
```

---

End of Design - QA Skill Specification
