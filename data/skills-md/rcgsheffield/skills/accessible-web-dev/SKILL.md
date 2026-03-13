---
name: accessible-web-dev
description: "Build WCAG 2.1 AA compliant web applications for University of Sheffield. Covers semantic HTML, ARIA patterns, form accessibility, keyboard navigation, color contrast, alt text, captions, and automated testing. Use when creating websites, web apps, forms, interactive components, or auditing accessibility for WCAG compliance, screen readers, keyboard access, or inclusive design."
version: 0.1.0
domain: web-development, accessibility, compliance
---

# University of Sheffield Web Accessibility Skill

Build web applications that meet WCAG 2.1 Level AA standards and University of Sheffield accessibility requirements.

## When to Use This Skill

Trigger this skill when working on:
- Building new web applications, sites, or digital platforms
- Creating forms, interactive components, or custom widgets
- Reviewing content for accessibility compliance
- Auditing existing websites for WCAG violations
- User mentions: accessibility, WCAG, screen reader, keyboard navigation, alt text, ARIA, captions, color contrast, inclusive design

## Core Requirements

**Compliance Standard:** WCAG 2.1 Level AA minimum across all University of Sheffield digital platforms

**Everyone's Responsibility:** Accessibility is not just for developers—product owners, designers, content creators, and communications specialists all play critical roles.

---

## Quick Start Workflow

### 1. Planning Phase
- Define accessibility requirements in acceptance criteria
- Identify content types (text, images, video, interactive elements)
- Establish responsibility matrix across team roles
- Budget for testing and remediation

### 2. Design Phase
- **Color Contrast:** 4.5:1 minimum for normal text, 3:1 for large text
- **Focus Indicators:** Clear, visible focus states for all interactive elements
- **Touch Targets:** Minimum 44×44 CSS pixels
- **Color Alone:** Never use color as sole indicator (add patterns, labels, icons)
- Test designs with contrast checker: `python scripts/contrast_checker.py "#foreground" "#background"`

### 3. Development Phase

**Semantic HTML First:**
```html
<!-- Good: Native HTML -->
<button type="button">Click me</button>
<nav aria-label="Main navigation">
  <ul><li><a href="/research">Research</a></li></ul>
</nav>

<!-- Bad: Div soup -->
<div onclick="...">Click me</div>
<div class="nav">...</div>
```

**Heading Hierarchy:**
- One `<h1>` per page
- Never skip levels (h1 → h2 → h3, not h1 → h3)
- Headings describe content structure, not styling

**Form Accessibility:**
- Associate labels with inputs using `for`/`id`
- Mark required fields with `required` and `aria-required="true"`
- Provide error messages via `aria-describedby` and `role="alert"`
- Use `autocomplete` attributes for common fields
- See: `assets/templates/form-template.html`

**Keyboard Navigation:**
- All functionality available via keyboard (Tab, Enter, Space, Arrows)
- Logical focus order
- No keyboard traps
- Visible focus indicators
- Skip links for main content

**ARIA Usage:**
- **Rule 1:** Use native HTML when possible (don't use `<div role="button">`, use `<button>`)
- **Rule 2:** Only add ARIA when native HTML insufficient
- For complex widgets (tabs, modals, accordions), see: `references/aria_patterns.md`

### 4. Content Phase

**Alternative Text Decision Tree:**
```
Is image meaningful?
├─ YES: Conveys information? → Write descriptive alt text
│   └─ Redundant with surrounding text? → alt=""
└─ NO: Purely decorative? → alt=""

Functional images (buttons, links): Describe function, not appearance
Complex images (charts): Brief alt + detailed description
```

**Examples:**
```html
<!-- Decorative -->
<img src="border.png" alt="">

<!-- Informative -->
<img src="campus.jpg" alt="Students working in Diamond building collaborative space">

<!-- Functional -->
<a href="/search"><img src="search.svg" alt="Search"></a>

<!-- Complex -->
<img src="chart.png"
     alt="Enrollment trends 2020-2024"
     aria-describedby="chart-details">
<div id="chart-details">
  Enrollment increased from 28,000 to 32,000,
  with largest growth in Engineering (15%)...
</div>
```

**Video/Audio Requirements:**
- **Captions:** All video content (prerecorded and live)
- **Transcripts:** All audio/video content
- **Audio Description:** Instructional and informational videos
- Upload captions as SRT files (Kaltura for UoS content)

### 5. Testing Phase

**Automated Testing:**
```bash
# HTML audit
python scripts/accessibility_audit.py path/to/file.html

# Color contrast check
python scripts/contrast_checker.py "#ffffff" "#000000"
```

**Manual Testing:**
- Keyboard-only navigation (disconnect mouse)
- Screen reader testing (NVDA on Windows, VoiceOver on Mac)
- Zoom to 200% (content must remain functional)
- Mobile screen reader (TalkBack/VoiceOver)

**Testing Checklist:**
- [ ] All images have alt text or alt=""
- [ ] All form inputs have associated labels
- [ ] Headings follow logical hierarchy
- [ ] All functionality keyboard accessible
- [ ] Focus indicators visible
- [ ] Color contrast meets 4.5:1 (normal text)
- [ ] No keyboard traps
- [ ] Dynamic updates announced by screen readers
- [ ] Link text descriptive out of context

---

## Common Patterns & Templates

### Accessible Modal Dialog
See: `assets/templates/modal-template.html`

**Key Requirements:**
- `role="dialog"` and `aria-modal="true"`
- Focus trap within modal
- Escape key closes modal
- Focus returns to trigger element on close
- Prevent background scroll when open

**React Example:** `assets/examples/AccessibleTabs.jsx`

### Accessible Forms
See: `assets/templates/form-template.html`

**Key Requirements:**
- Label/input associations
- Error messaging with `role="alert"`
- Required field indicators
- Validation feedback
- Autocomplete attributes

**React Components:** `assets/examples/AccessibleForm.jsx`

### Accessible Tabs
**Keyboard Navigation:**
- Arrow Left/Right: Navigate tabs
- Home/End: First/last tab
- Tab: Exit tab list

**Implementation:** See `assets/examples/AccessibleTabs.jsx`

---

## Quick Reference

### WCAG 2.1 AA Priority Checks

**Level A (Critical):**
- 1.1.1: Alt text for images
- 2.1.1: Keyboard accessible
- 2.1.2: No keyboard traps
- 2.4.1: Skip links
- 2.4.2: Page titles
- 3.1.1: Page language (lang attribute)
- 4.1.2: Name, role, value for components

**Level AA (UoS Requirement):**
- 1.2.4: Live captions
- 1.2.5: Audio descriptions
- 1.4.3: Color contrast 4.5:1
- 1.4.5: Avoid images of text
- 2.4.7: Visible focus
- 3.3.3: Error suggestions
- 4.1.3: Status messages

**Full details:** See `references/wcag_detailed.md`

### ARIA Patterns Reference

For implementing complex widgets:
- Accordion, Alert Dialog, Breadcrumb
- Button (Toggle), Combobox, Dialog (Modal)
- Disclosure, Menu, Tabs, Tooltip
- Tree View, Live Regions

**Full patterns with code:** See `references/aria_patterns.md`

### Color Contrast Quick Check

**Minimum Ratios:**
- Normal text: 4.5:1
- Large text (18pt+ or 14pt+ bold): 3:1
- UI components/graphics: 3:1

**Common UoS Colors:**
- White on UoS blue (#009ADE): 3.2:1 ✗ Fails for normal text
- Black on UoS yellow (#FECB00): 10:1 ✓ Passes

**Tool:** `python scripts/contrast_checker.py "#color1" "#color2" --level AA`

---

## Common Pitfalls & Solutions

### Pitfall 1: Generic Link Text
❌ **Bad:** "Click here" or "Read more"
✅ **Good:** "Annual Research Report 2024 (PDF, 2.3MB)"

### Pitfall 2: Missing Form Labels
❌ **Bad:** `<input type="text" placeholder="Email">`
✅ **Good:** `<label for="email">Email</label><input id="email" type="email">`

### Pitfall 3: Div/Span Buttons
❌ **Bad:** `<div onclick="submit()">Submit</div>`
✅ **Good:** `<button type="button" onclick="submit()">Submit</button>`

### Pitfall 4: Low Color Contrast
❌ **Bad:** Light gray (#CCC) on white (1.7:1)
✅ **Good:** Dark gray (#767676) on white (4.5:1)

### Pitfall 5: Auto-Playing Media
❌ **Bad:** `<video autoplay>`
✅ **Good:** `<video controls><track kind="captions" src="captions.vtt"></video>`

### Pitfall 6: Missing Page Titles
❌ **Bad:** `<title>University of Sheffield</title>` (on every page)
✅ **Good:** `<title>Computer Science MSc - Courses - University of Sheffield</title>`

---

## Tools & Scripts

### Included Scripts

**Accessibility Auditor:**
```bash
# Audit single file
python scripts/accessibility_audit.py file.html

# Audit directory
python scripts/accessibility_audit.py src/

# JSON output
python scripts/accessibility_audit.py file.html --format json
```

Checks: Images, headings, links, forms, page structure, semantic HTML, tables, buttons, ARIA usage

**Contrast Checker:**
```bash
# Basic check
python scripts/contrast_checker.py "#ffffff" "#000000"

# Check for AAA
python scripts/contrast_checker.py "#ffffff" "#000000" --level AAA

# Large text
python scripts/contrast_checker.py "#999999" "#ffffff" --large-text

# Show suggestions
python scripts/contrast_checker.py "#cccccc" "#ffffff" --suggest
```

### External Tools

**Browser Extensions:**
- WAVE (WebAIM): Visual accessibility feedback
- axe DevTools: Comprehensive automated testing
- Lighthouse: Built into Chrome DevTools

**Screen Readers:**
- NVDA (Windows): Free, nvaccess.org
- JAWS (Windows): Commercial, enterprise standard
- VoiceOver (Mac/iOS): Built-in (Cmd+F5)
- TalkBack (Android): Built-in

**Online Tools:**
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- WAVE Web Accessibility Evaluation: https://wave.webaim.org/

---

## University of Sheffield Specific

**Content Tone:**
- Active voice over passive
- Plain English (avoid jargon)
- Short paragraphs for scannability
- Sentence case (not title case/capitals)

**Platform Requirements:**
- Kaltura for video hosting and captioning
- Standard SRT format for captions
- Accessibility statement required on all sites
- Diverse representation in all visual content

**Documentation:**
- Must document any exceptions with justification
- Standards apply unless clear reason why not possible
- Regular audits required

---

## Implementation Example

**Scenario: Building a student portal**

```javascript
// 1. Use this skill to generate accessible component
"I need to build a course enrollment form for University of Sheffield
student portal. Include name, email, course selection dropdown, and
accessibility preferences checkboxes."

// 2. Skill will:
// - Use semantic HTML form structure
// - Add proper label associations
// - Include error handling with aria-live
// - Implement keyboard navigation
// - Ensure color contrast compliance
// - Add autocomplete attributes
// - Reference form template from assets/

// 3. Test with provided tools
python scripts/accessibility_audit.py enrollment-form.html
python scripts/contrast_checker.py "#005eb8" "#ffffff"

// 4. Manual verification
// - Tab through form with keyboard only
// - Test with NVDA screen reader
// - Verify error messages announced
// - Check focus indicators visible
```

---

## Resources

**Detailed References:**
- Full WCAG 2.1 criteria: `references/wcag_detailed.md`
- Complete ARIA patterns: `references/aria_patterns.md`

**Templates & Examples:**
- HTML form template: `assets/templates/form-template.html`
- HTML modal template: `assets/templates/modal-template.html`
- React tabs component: `assets/examples/AccessibleTabs.jsx`
- React form components: `assets/examples/AccessibleForm.jsx`

**Official Guidelines:**
- WCAG 2.1: https://www.w3.org/TR/WCAG21/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- UK Public Sector Requirements: https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps

**Learning Resources:**
- WebAIM: https://webaim.org/
- A11y Project: https://www.a11yproject.com/
- Inclusive Components: https://inclusive-components.design/

---

## Success Criteria

**Technical:**
- 100% WCAG 2.1 AA compliance
- Zero critical errors in automated testing
- All pages pass keyboard-only navigation
- All content announced correctly by screen readers

**User Experience:**
- Users with disabilities can complete all tasks
- Equivalent experience regardless of ability
- Positive feedback from assistive technology users
- No accessibility-related support issues

**Process:**
- Accessibility in all acceptance criteria
- Testing integrated into CI/CD pipeline
- Team trained on accessibility standards
- Regular audits completed and documented
