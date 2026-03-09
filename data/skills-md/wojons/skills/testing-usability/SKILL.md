---
name: testing-usability
description: Test application usability and user experience
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Usability Testing

Test application usability, user experience, and interaction design, complementing functional and accessibility testing.

## When to use me

Use this skill when:
- Evaluating user interface design effectiveness
- Testing intuitive navigation and workflows
- Gathering qualitative user feedback
- Improving user satisfaction and engagement
- Validating information architecture
- Testing learnability for new users

## What I do

- **User experience evaluation**:
  - Task success rate measurement
  - Time to complete tasks
  - Error rate and recovery analysis
  - User satisfaction scoring

- **Interaction design testing**:
  - Navigation intuitiveness
  - Form design and workflow
  - Information hierarchy
  - Visual design effectiveness

- **User research methods**:
  - User interviews and observations
  - Think-aloud protocols
  - Card sorting for information architecture
  - A/B testing for design variations

- **Coordinate with other test types**:
  - Builds on functional testing (features work)
  - Complements accessibility testing (usable by all)
  - Informs visual design testing (aesthetics + usability)
  - Provides context for performance testing (perceived speed)

## Examples

```bash
# Usability testing tools and methods
npm run test:usability:survey      # User satisfaction surveys
npm run test:usability:analytics    # Analytics-based usability metrics

# User testing coordination
# Manual process typically, but can coordinate with:
npm run test:e2e:usability         # E2E tests with usability focus
npm run test:accessibility         # Accessibility complements usability

# Heatmap and session recording setup
# Tools: Hotjar, FullStory, Microsoft Clarity

# A/B testing framework
npm run test:ab:deploy             # Deploy A/B test variations
npm run test:ab:analyze            # Analyze A/B test results

# Coordinate with functional testing
npm run test:usability -- --functional-coverage
npm run test:e2e -- --usability-focus
```

## Output format

```
Usability Test Results:
──────────────────────────────
Test Method: Remote unmoderated testing with 15 participants
Testing Period: 2 weeks

Task Completion Rates:
  ✅ User Registration: 93% success (14/15)
  ✅ Product Search: 87% success (13/15)
  ⚠️ Checkout Process: 73% success (11/15)
    - 3 users confused by shipping options
    - 1 user abandoned due to form length

Time to Complete Key Tasks:
  - Registration: 2.1 minutes (target < 3 minutes)
  - Find Product: 1.4 minutes (target < 2 minutes)  
  - Complete Purchase: 4.7 minutes (target < 5 minutes)

Error Rates and Recovery:
  - Form errors: 22 total, 18 self-corrected
  - Navigation errors: 8, all recovered
  - Critical errors: 2 (checkout abandonment)

User Satisfaction (1-5 scale):
  - Ease of use: 4.2
  - Navigation: 3.8  
  - Visual design: 4.5
  - Overall satisfaction: 4.1

Integration with Other Testing:
  - Functional tests pass, but usability reveals workflow issues
  - Accessibility compliant, but not optimally usable
  - Performance acceptable, but perceived speed could improve
  - Security features add friction to user experience

Key Findings:
  1. Checkout process needs simplification
  2. Search functionality effective but could be more prominent
  3. Mobile navigation needs improvement
  4. Users appreciate clean design but want more guidance

Recommendations:
  - Simplify checkout form (reduce fields by 30%)
  - Improve mobile hamburger menu discoverability
  - Add progress indicators to multi-step processes
  - Implement tooltips for complex features
```

## Notes

- Usability testing is qualitative, complementing quantitative testing
- Test with real users, not just developers or testers
- Consider different user personas and skill levels
- Usability testing should be iterative, not one-time
- Combine with analytics data for complete picture
- Document user pain points and success stories
- Prioritize usability fixes based on impact and effort
- Consider cultural differences in usability expectations
- Balance usability with security, performance, and other requirements
