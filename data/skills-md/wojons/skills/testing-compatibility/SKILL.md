---
name: testing-compatibility
description: Test application compatibility across browsers, devices, and platforms
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Compatibility Testing

Test application compatibility across browsers, devices, operating systems, and environments, coordinating with functional and visual testing.

## When to use me

Use this skill when:
- Developing web applications for multiple browsers
- Supporting various devices (mobile, tablet, desktop)
- Targeting different operating systems
- Handling diverse network conditions
- Ensuring responsive design works correctly
- Validating internationalization and localization

## What I do

- **Cross-browser testing**:
  - Test on Chrome, Firefox, Safari, Edge, and others
  - Validate JavaScript compatibility
  - Check CSS rendering differences
  - Verify polyfill requirements

- **Cross-platform testing**:
  - Windows, macOS, Linux compatibility
  - iOS and Android mobile platforms
  - Tablet and responsive design validation
  - Desktop application compatibility

- **Device and environment testing**:
  - Different screen sizes and resolutions
  - Touch vs mouse interactions
  - Network conditions (3G, 4G, WiFi)
  - Printer compatibility and PDF generation

- **Coordinate with other test types**:
  - Run functional tests across all supported platforms
  - Perform visual regression testing for UI consistency
  - Validate accessibility across different environments
  - Check performance metrics per platform

## Examples

```bash
# Cross-browser testing
npm run test:compatibility:browsers  # All supported browsers
npx playwright test --browser=all    # Playwright multi-browser
npx cypress run --browser chrome --browser firefox

# Device testing
npm run test:compatibility:devices   # Responsive testing
npx playwright test --device="iPhone 13"
npx lighthouse https://app.example.com --screenEmulation.mobile=true

# Platform testing
npm run test:compatibility:os        # OS-specific testing
# Use CI with different OS runners

# Network condition testing
npm run test:compatibility:network   # Simulate network conditions
npx lighthouse --throttling.cpuSlowdownMultiplier=4

# Coordinate with functional tests
npm run test:compatibility -- --grep "functional"
npm run test:e2e:compatibility       # E2E across platforms
```

## Output format

```
Compatibility Test Results:
──────────────────────────────
Test Matrix: 15 combinations (browsers × devices × OS)

Browser Compatibility:
  ✅ Chrome 120+: All functional tests pass
  ✅ Firefox 115+: All functional tests pass  
  ✅ Safari 16+: 42/45 tests pass
    ⚠️ 3 tests fail due to WebRTC differences
  ✅ Edge 119+: All functional tests pass

Device Compatibility:
  ✅ Desktop (1920×1080): All tests pass
  ✅ Tablet (iPad): 38/40 tests pass
    ⚠️ 2 touch gesture tests need adjustment
  ✅ Mobile (iPhone/Android): 35/40 tests pass
    ❌ 5 tests fail due to viewport issues

Operating Systems:
  ✅ Windows 10/11: All tests pass
  ✅ macOS 12+: All tests pass
  ✅ Linux (Ubuntu): All tests pass
  ✅ iOS 15+: 40/45 tests pass
  ✅ Android 11+: 42/45 tests pass

Network Conditions:
  ✅ WiFi: All tests pass
  ✅ 4G: 45/50 tests pass
  ✅ 3G: 30/50 tests pass (expected performance degradation)

Integration with Other Tests:
  - Functional tests: Compatible across 85% of matrix
  - Visual tests: 95% consistency across browsers
  - Accessibility tests: WCAG compliance maintained
  - Performance tests: Metrics vary by platform (documented)

Recommendation:
  - Fix Safari WebRTC and mobile viewport issues
  - Add polyfills for older browser support if needed
  - Document known compatibility limitations
```

## Notes

- Prioritize testing based on user analytics data
- Use cloud testing services for extensive device matrices
- Implement responsive design testing early
- Consider progressive enhancement for broader compatibility
- Test with real devices when possible, not just emulators
- Document browser-specific workarounds
- Track compatibility regressions over time
- Use feature detection rather than browser detection
- Consider international users with different default browsers
