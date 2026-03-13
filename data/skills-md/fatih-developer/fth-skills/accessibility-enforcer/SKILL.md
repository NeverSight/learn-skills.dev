---
name: accessibility-enforcer
description: Ensure mobile app UI complies with iOS VoiceOver, Android TalkBack, and WCAG mobile criteria. Detect missing labels, contrast issues, and propose accessible alternatives.
---

# Accessibility Enforcer Protocol

Accessibility (a11y) on mobile is not a nice-to-have; it's a legal and moral requirement. A screen reader user should be able to navigate, understand, and interact with the app as easily as a sighted user. This skill acts as an automated a11y auditor.

**Core principle:** If VoiceOver or TalkBack can't read it, the button doesn't exist for that user.

---

## Workflow

```
1. Identify the UI component / interaction pattern
2. Analyze for specific platform screen reader requirements
3. Check WCAG contrast and touch target sizes
4. Recommend code-level implementations
```

---

## Step 1: Component Identification
Identify the elements being used:
- Core UI (Buttons, Images, TextInputs)
- Complex UI (Modals, Carousels, Custom Drawers)
- State changes (Loading spinners, Error messages)

## Step 2: Screen Reader Analysis
Screen readers need three things from an element:
1. **Focusability:** Can the user navigate to it?
2. **Label:** What is it called? (e.g., "Submit")
3. **Role/Trait:** What does it do? (e.g., "Button")
4. **State:** Is it active? (e.g., "Selected", "Disabled")

*Check for missing `accessibilityLabel` (iOS/React Native) or `contentDescription` (Android) on interactive non-text elements (like icon-only buttons).*

## Step 3: Interaction & Visual Checks
- **Touch Target Size:** Minimum 44x44pt (iOS) or 48x48dp (Android).
- **Color Contrast:** WCAG AA requires 4.5:1 for normal text and 3:1 for large text/icons.
- **Focus Order:** Does the reading order make logical sense? Does a modal trap focus so the screen reader doesn't read the background?

## Step 4: Implementation Recommendation
Provide exact code snippets for the specific platform to fix the identified issues.

---

## Output Format

```markdown
# ♿ Accessibility Audit Report

**Component / View:** [e.g., Custom Icon Button Navbar]

## 🚨 Critical VoiceOver/TalkBack Issues
*Issues blocking screen reader users from using the feature.*

1. **[Issue Name]** (e.g., Unlabeled Icon Button)
   - **Problem:** [E.g., The search icon button has no label. VoiceOver will just read "Button", leaving the user confused.]
   - **Fix:** [Give the exact code fix, such as adding `accessibilityLabel="Search"` and `accessibilityRole="button"`.]

## ⚠️ UX / Interaction Warnings
*Issues failing WCAG but not completely broken.*

1. **[Warning Area]** (e.g., Touch Target Too Small)
   - **Problem:** [Explanation]
   - **Mitigation:** [Solution, e.g., Add `hitSlop` to increase the touchable area without visually changing the design.]

## 💡 Code Implementation

```javascript/swift/kotlin
// Before (Inaccessible):
<TouchableOpacity onPress={search}>
   <Icon name="search" />
</TouchableOpacity>

// After (Accessible):
<TouchableOpacity 
   onPress={search}
   accessibilityRole="button"
   accessibilityState={{disabled: false}}
   accessibilityLabel="Search"
   accessibilityHint="Opens the search bar to find users"
   hitSlop={{top: 10, bottom: 10, left: 10, right: 10}}
>
   <Icon name="search" />
</TouchableOpacity>
```

---

## When to Skip
- The task is entirely backend logic or database schema design.

---

## Guardrails
- **Beware Redundant Data:** Never tell a dev to add the word "button" into the `accessibilityLabel` (e.g., "Search Button"). The screen reader will announce "Search Button Button" because of the element's trait.
- **Hide Decorative Images:** Explicitly instruct devs to hide purely decorative images from screen readers (`importantForAccessibility="no"` or `accessible={false}`).
- **Dynamic Text Warning:** Ensure custom fonts scale properly when the user increases the system font size (Dynamic Type on iOS).

---

## References
See `references/EXAMPLES.md` for a worked case.

---

## 🔗 Next Steps & Handoffs
If you are executing the **Pre-Release Audit Flow** as defined in the Mobile ECOSYSTEM guide, and this accessibility audit passes, the next mandatory skill in the sequence is:
- `@mobile-perf-auditor`
