---
name: pasteboard-textinsertion
description: Inserting text into other macOS applications via clipboard simulation, CGEvent keystroke typing, and Accessibility API direct text field access. Covers NSPasteboard read/write with clipboard preserve/restore, CGEvent keystroke simulation (Cmd+V paste, character-by-character typing), AXUIElement for direct text field manipulation, variable/placeholder expansion ({{clipboard}}, {{date}}, {{cursor}}), user-prompted variables ({{?name:prompt:default}}), cursor positioning after insertion, and insertion method fallback chains. Use when building prompt managers, text expanders, snippet tools, or any app that needs to insert text into other applications.
---

# Pasteboard & Text Insertion

Insert text INTO other applications. The core capability of prompt managers and text expanders.

## Critical Constraints

- ❌ DO NOT forget to save/restore clipboard contents → ✅ Preserve user's clipboard before overwriting
- ❌ DO NOT skip the delay between clipboard set and paste simulation → ✅ Add 50ms delay minimum
- ❌ DO NOT use only one insertion method → ✅ Build a fallback chain: Paste → Typing → Accessibility
- ❌ DO NOT use Accessibility API without permission check → ✅ Always check `AXIsProcessTrusted()` first

## Insertion Methods (Ranked)

| Method | Reliability | Speed | Sandbox | Best For |
|--------|-------------|-------|---------|----------|
| Clipboard + Paste | ★★★★★ | Fast | ✅ | Default method |
| CGEvent Typing | ★★★★☆ | Slow | ⚠️ Needs Accessibility | Paste-blocking apps |
| Accessibility API | ★★★☆☆ | Fast | ⚠️ Needs Accessibility | Text fields only |

## Method 1: Clipboard + Simulated Paste (Default)
```swift
import AppKit
import Carbon

class TextInserter {
    func insertViaPaste(_ text: String, completion: (() -> Void)? = nil) {
        let pasteboard = NSPasteboard.general
        let previousContents = pasteboard.string(forType: .string)

        pasteboard.clearContents()
        pasteboard.setString(text, forType: .string)

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
            self.simulateKeyPress(keyCode: 0x09, modifiers: .maskCommand)  // Cmd+V

            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                if let previous = previousContents {
                    pasteboard.clearContents()
                    pasteboard.setString(previous, forType: .string)
                }
                completion?()
            }
        }
    }

    func simulateKeyPress(keyCode: CGKeyCode, modifiers: CGEventFlags) {
        let source = CGEventSource(stateID: .hidSystemState)
        let keyDown = CGEvent(keyboardEventSource: source, virtualKey: keyCode, keyDown: true)
        keyDown?.flags = modifiers
        keyDown?.post(tap: .cghidEventTap)
        let keyUp = CGEvent(keyboardEventSource: source, virtualKey: keyCode, keyDown: false)
        keyUp?.flags = modifiers
        keyUp?.post(tap: .cghidEventTap)
    }
}
```

## Method 2: CGEvent Character Typing (Fallback)
```swift
extension TextInserter {
    func insertViaTyping(_ text: String, delayPerChar: TimeInterval = 0.01) {
        let source = CGEventSource(stateID: .hidSystemState)
        for char in text {
            let str = String(char)
            if let event = CGEvent(keyboardEventSource: source, virtualKey: 0, keyDown: true) {
                var unichar = str.utf16.first!
                event.keyboardSetUnicodeString(stringLength: 1, unicodeString: &unichar)
                event.post(tap: .cghidEventTap)
            }
            if let event = CGEvent(keyboardEventSource: source, virtualKey: 0, keyDown: false) {
                event.post(tap: .cghidEventTap)
            }
            Thread.sleep(forTimeInterval: delayPerChar)
        }
    }
}
```

## Method 3: Accessibility API (Direct)
```swift
import ApplicationServices

extension TextInserter {
    func insertViaAccessibility(_ text: String) -> Bool {
        guard AXIsProcessTrusted() else { return false }
        let systemWide = AXUIElementCreateSystemWide()
        var focusedElement: CFTypeRef?
        guard AXUIElementCopyAttributeValue(systemWide, kAXFocusedUIElementAttribute as CFString,
                                            &focusedElement) == .success,
              let element = focusedElement as! AXUIElement? else { return false }

        // Verify it's a text field
        var role: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXRoleAttribute as CFString, &role)
        guard let roleStr = role as? String,
              roleStr == kAXTextFieldRole || roleStr == kAXTextAreaRole else { return false }

        // Get current value + selection, insert at selection
        var currentValue: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXValueAttribute as CFString, &currentValue)
        let current = (currentValue as? String) ?? ""

        var selectedRange: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXSelectedTextRangeAttribute as CFString, &selectedRange)

        var newValue = current
        if let range = selectedRange as? AXValue {
            var cfRange = CFRange()
            AXValueGetValue(range, .cfRange, &cfRange)
            let start = current.index(current.startIndex, offsetBy: cfRange.location)
            let end = current.index(start, offsetBy: cfRange.length)
            newValue.replaceSubrange(start..<end, with: text)
        } else {
            newValue += text
        }

        return AXUIElementSetAttributeValue(element, kAXValueAttribute as CFString,
                                            newValue as CFTypeRef) == .success
    }
}
```

## Variable Expansion System
```swift
class VariableExpander {
    static let builtInVariables: [(pattern: String, replacement: () -> String)] = [
        ("{{cursor}}", { "" }),  // Handled specially for cursor positioning
        ("{{clipboard}}", { NSPasteboard.general.string(forType: .string) ?? "" }),
        ("{{date}}", { DateFormatter.localizedString(from: Date(), dateStyle: .medium, timeStyle: .none) }),
        ("{{time}}", { DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .short) }),
        ("{{datetime}}", { DateFormatter.localizedString(from: Date(), dateStyle: .medium, timeStyle: .short) }),
        ("{{iso_date}}", { ISO8601DateFormatter().string(from: Date()) }),
        ("{{username}}", { NSFullUserName() }),
        ("{{uuid}}", { UUID().uuidString }),
    ]

    func expand(_ text: String) -> (text: String, cursorOffset: Int?) {
        var result = text
        var cursorOffset: Int? = nil

        for (pattern, replacement) in Self.builtInVariables {
            if pattern == "{{cursor}}" {
                if let range = result.range(of: pattern) {
                    cursorOffset = result.distance(from: result.startIndex, to: range.lowerBound)
                    result.replaceSubrange(range, with: "")
                }
            } else {
                result = result.replacingOccurrences(of: pattern, with: replacement())
            }
        }
        return (result, cursorOffset)
    }
}
```

## User-Prompted Variables
```swift
// Format: {{?variableName:Enter your name:DefaultValue}}
func findUserVariables(in text: String) -> [(name: String, prompt: String, defaultValue: String)] {
    let pattern = #"\{\{\?(\w+):([^:]+):?([^}]*)\}\}"#
    let regex = try! NSRegularExpression(pattern: pattern)
    return regex.matches(in: text, range: NSRange(text.startIndex..., in: text)).compactMap { match in
        guard let nameRange = Range(match.range(at: 1), in: text),
              let promptRange = Range(match.range(at: 2), in: text) else { return nil }
        let defaultRange = Range(match.range(at: 3), in: text)
        return (String(text[nameRange]), String(text[promptRange]), defaultRange.map { String(text[$0]) } ?? "")
    }
}
```

## Cursor Positioning After Insertion
```swift
func insertWithCursor(_ text: String, inserter: TextInserter) {
    let (expanded, cursorOffset) = VariableExpander().expand(text)
    inserter.insertViaPaste(expanded) {
        if let offset = cursorOffset {
            let moveCount = expanded.count - offset
            for _ in 0..<moveCount {
                inserter.simulateKeyPress(keyCode: 0x7B, modifiers: [])  // Left arrow
            }
        }
    }
}
```

## References

- [NSPasteboard](https://developer.apple.com/documentation/appkit/nspasteboard)
- [CGEvent](https://developer.apple.com/documentation/coregraphics/cgevent)
- [Accessibility API](https://developer.apple.com/documentation/applicationservices/axuielement_h)
