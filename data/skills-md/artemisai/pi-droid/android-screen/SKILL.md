---
name: android-screen
description: Perceive Android device state — screenshots, annotated UI views, OCR, activity detection, screen state queries
---

## When to use

Use this skill when you need to understand what's currently displayed on the Android device. This includes seeing the screen, identifying UI elements, reading text via OCR, or checking which app/activity is in the foreground.

## Tools

| Tool | Purpose | Context cost |
|------|---------|-------------|
| `android_look` | Annotated screenshot with numbered element index — primary perception tool | Low |
| `android_screen_state` | Current activity, package, orientation, lock state as JSON | ~0 |
| `android_screenshot` | Raw screenshot image — use for failure diagnosis only | HIGH |
| `android_ui_dump` | Raw UI tree XML — use when you need full element hierarchy | Medium |
| `android_ocr` | Tesseract OCR on current screen or saved screenshot | Medium |
| `android_observe` | Continuous screen state observation | Low |

## Preferred order

1. Start with `android_screen_state` to check activity/package (zero context cost)
2. Use `android_look` to see the screen with labeled elements (low cost, high utility)
3. Fall back to `android_ocr` if UI tree doesn't capture text (dynamic/WebView content)
4. Use `android_screenshot` only for final confirmation or debugging failures

## Examples

```
"What app is open?" → android_screen_state
"What's on the screen?" → android_look
"Read the text in this image" → android_ocr
"Is the screen locked?" → android_screen_state
```
