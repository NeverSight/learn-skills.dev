---
name: testing-nonfunctional-suite
description: Run comprehensive non-functional test suite
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Non-Functional Test Suite

Run comprehensive non-functional testing covering performance, security, accessibility, and other quality attributes.

## When to use me

Use this skill when:
- Preparing applications for production deployment
- Validating quality attributes beyond functionality
- Complying with performance SLAs or security standards
- Testing under realistic load and stress conditions
- Ensuring inclusive design and accessibility
- Validating deployment and operational readiness

## What I do

1. **Performance Testing**
   - Load testing with expected user traffic
   - Stress testing to find breaking points
   - Endurance testing for memory leaks
   - Scalability testing for growth planning

2. **Security Testing**
   - Vulnerability scanning and penetration testing
   - Authentication and authorization testing
   - Input validation and injection testing
   - Security configuration review

3. **Accessibility Testing**
   - WCAG compliance validation
   - Screen reader and keyboard navigation testing
   - Color contrast and visual accessibility
   - Assistive technology compatibility

4. **Compatibility Testing**
   - Cross-browser and cross-platform testing
   - Mobile device and responsive design testing
   - Network condition simulation

5. **Usability Testing**
   - User experience evaluation
   - Navigation and workflow testing
   - Error message clarity and helpfulness

## Examples

```bash
# Run non-functional test suite
npm run test:nonfunctional       # Custom non-functional suite

# Performance testing
npm run test:performance
npx autocannon -c 100 -d 60 https://app.example.com

# Security scanning
npm run test:security
npm audit
npx snyk test

# Accessibility testing
npm run test:accessibility
npx pa11y https://app.example.com

# Compatibility testing
npm run test:compatibility
npx playwright test --browser=all
```

## Output format

```
Non-Functional Test Suite Results:
──────────────────────────────
Performance (Load: 1000 users, 10 minutes):
  ✅ Response Time: Avg 320ms (target < 500ms)
  ✅ Throughput: 2.1k req/sec
  ⚠️ CPU Usage: 92% (near limit)
  ✅ Error Rate: 0.05%

Security Assessment:
  ✅ No critical vulnerabilities found
  ⚠️ 3 medium severity issues
  ✅ Dependencies up to date
  ⚠️ Missing security headers (CSP, HSTS)

Accessibility (WCAG 2.1 AA):
  ✅ 42/58 criteria passed
  ⚠️ 12 criteria partially met
  ❌ 4 criteria failed (color contrast, form labels)

Compatibility:
  ✅ Chrome, Firefox, Safari (latest)
  ⚠️ Edge: Minor layout issues
  ✅ Mobile: iOS & Android responsive

Usability:
  ✅ Navigation intuitive
  ⚠️ Error messages could be clearer
  ✅ Forms accessible and clear

Overall: Meets most non-functional requirements
Priority Fixes: Accessibility issues, security headers
```

## Notes

- Non-functional requirements are often overlooked but critical
- Establish clear acceptance criteria for each quality attribute
- Test in environments as close to production as possible
- Consider user demographics for accessibility testing
- Security testing should be ongoing, not one-time
- Performance testing should include realistic user behavior patterns
- Document non-functional requirements alongside functional ones
- Automate regression testing for non-functional aspects where possible
