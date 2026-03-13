---
name: validating-ui-features
description: Provides step-by-step procedures for validating UI features - theme toggle, new chat, cancel stream, markdown rendering, and token usage info.
---

# Validating UI Features

**CRITICAL**: Load this skill before running any UI validation tests.

## Prerequisites

- [ ] Local dev servers running (Backend: 8080, Frontend: 5173)
- [ ] Playwright MCP tools available
- [ ] Authenticated user session (MSAL popup completed)

## Quick Test Commands

| Test | Command |
|------|---------|
| Start servers | VS Code task: `Start Dev (VS Code Terminals)` |
| Navigate | `browser_navigate` to `http://localhost:5173` |
| Check state | Look for `🔄` entries in browser console |

---

## Test 1: Theme Toggle (Settings Panel)

### Purpose
Verify the Settings panel opens and theme switching works correctly.

### UI Flow
```text
ChatInput toolbar → Settings button (gear) → SettingsPanel drawer → ThemePicker dropdown
```

### Steps

1. **Navigate** to `http://localhost:5173`
2. **Wait** for authentication and agent metadata load
3. **Find** Settings button in ChatInput toolbar (gear icon, aria-label="Settings")
4. **Click** Settings button
5. **Verify** SettingsPanel drawer opens from right side
6. **Verify** "Appearance" section visible with ThemePicker
7. **Click** ThemePicker dropdown (currently shows "Light" or saved preference)
8. **Select** "Dark" option
9. **Verify** Theme changes:
   - Background becomes dark (≈ `rgb(32, 31, 30)`)
   - Text becomes light
   - No console errors
10. **Select** "Light" option
11. **Verify** Theme changes back:
    - Background becomes light (≈ `rgb(255, 255, 255)`)
    - Text becomes dark
12. **Select** "System" option
13. **Verify** Theme matches OS preference
14. **Close** Settings panel (X button or click outside)

### Console Evidence
```javascript
// No errors should appear
// LocalStorage updated:
localStorage.getItem('ai-foundry-theme') // "Dark", "Light", or "System"
```

### DOM Changes
- `<body>` FluentProvider styles update
- CSS variables change: `--colorNeutralBackground1`, `--colorNeutralForeground1`

### Pass Criteria
- [ ] Settings panel opens/closes without errors
- [ ] All three theme options selectable
- [ ] Visual theme changes immediately on selection
- [ ] Theme persists after closing panel

---

## Test 2: New Chat Button

### Purpose
Verify the New Chat button clears messages and resets conversation state.

### UI Flow
```text
Send message → Wait for response → Click New Chat button → Verify reset
```

### Prerequisites
- At least one message exchange completed

### Steps

1. **Send** a test message: `"Hello, testing new chat button"`
2. **Wait** for assistant response to complete (status: `idle`)
3. **Verify** New Chat button is **enabled** (not grayed out)
4. **Click** New Chat button (ChatAdd icon, aria-label="New chat")
5. **Verify** immediate changes:
   - Messages array cleared (empty chat area)
   - StarterMessages component visible (agent intro + prompts)
   - Input field focused and empty
   - New Chat button now **disabled** (no messages to clear)

### Console Evidence
```javascript
🔄 [timestamp] CHAT_CLEAR
Action: {type: CHAT_CLEAR}
Changes: {
  chat.messages.length: N → 0
}
```

### Pass Criteria
- [ ] Button disabled when no messages
- [ ] Button enabled after first message
- [ ] Click clears all messages instantly
- [ ] StarterMessages reappear
- [ ] conversationId reset to null
- [ ] Input field receives focus
- [ ] No console errors

---

## Test 3: Cancel Stream (Stop Button)

### Purpose
Verify streaming can be cancelled mid-response.

### UI Flow
```text
Send long prompt → While streaming → Click Stop button → Verify cancellation
```

### Steps

1. **Start** a new chat (or use existing)
2. **Send** a prompt that triggers a long code response:
   ```text
   Write a comprehensive Python script that calculates Fibonacci numbers using 5 different methods: recursive, memoized, iterative, matrix exponentiation, and Binet's formula. Include detailed docstrings, type hints, performance benchmarks, and unit tests for each method.
   ```
3. **Immediately observe**:
   - Status changes to `streaming`
   - Stop button becomes **enabled** (aria-label="Cancel response")
   - Send button becomes **disabled**
   - Text chunks appearing in assistant message
4. **Click** Stop button while streaming is active
5. **Verify** cancellation:
   - Streaming stops immediately
   - Partial response preserved (not deleted)
   - Status returns to `idle`
   - Send button re-enabled
   - Stop button disabled again

### Keyboard Shortcut
- Press `Escape` key during streaming → should also cancel

### Console Evidence
```javascript
🔄 [timestamp] CHAT_CANCEL_STREAM
Action: {type: CHAT_CANCEL_STREAM}
Changes: {
  chat.status: streaming → idle,
  chat.streamingMessageId: "xxx" → undefined
}
```

### Edge Cases
- Very fast response may complete before cancel → OK, not an error
- Multiple rapid clicks → should be idempotent

### Pass Criteria
- [ ] Stop button disabled when not streaming
- [ ] Stop button enabled during streaming
- [ ] Click stops stream immediately
- [ ] Partial response text preserved
- [ ] Status returns to idle
- [ ] Escape key works as shortcut
- [ ] No errors in console

---

## Test 4: Markdown Code Block Rendering

### Purpose
Verify code blocks render with syntax highlighting, line numbers, and copy button.

### UI Flow
```text
Send code request → Wait for response → Verify code block UI
```

### Steps

1. **Start** a new chat
2. **Send** a code generation prompt:
   ```text
   Write a Python function to calculate fibonacci numbers with proper type hints
   ```
3. **Wait** for response to complete
4. **Verify** code block structure:
   - Container with dark background
   - Header bar showing "python" language label
   - "Copy" button in header
   - Line numbers on left side
   - Syntax highlighting (keywords, strings, comments in different colors)
5. **Click** "Copy" button
6. **Verify** code copied (paste somewhere to confirm)

### Additional Test Prompts
From `test-files/test-prompts.json`:
```json
[
  "Create a TypeScript interface for a user profile with nested preferences",
  "Show me a bash script to backup a PostgreSQL database",
  "Write a SQL query with a CTE to find duplicate customer records"
]
```

### Expected Code Block DOM
```html
<div class="codeBlock">
  <div class="codeHeader">
    <span class="codeLanguage">python</span>
    <button>Copy</button>
  </div>
  <div> <!-- SyntaxHighlighter -->
    <!-- Line numbers + highlighted code -->
  </div>
</div>
```

### Syntax Highlighting Colors (vscDarkPlus theme)
| Element | Color |
|---------|-------|
| Keywords (`def`, `return`, `if`) | Purple/Blue |
| Strings | Orange |
| Comments | Green |
| Function names | Yellow |
| Types | Cyan |

### Pass Criteria
- [ ] Language label displayed correctly
- [ ] Copy button present and functional
- [ ] Syntax highlighting applied
- [ ] Line numbers visible
- [ ] Long lines wrap (no horizontal overflow)
- [ ] Multiple code blocks render independently

---

## Test 5: Complex Markdown Rendering

### Purpose
Verify tables, lists, headings, and text formatting render correctly.

### Steps

1. **Send** a complex markdown prompt:
   ```text
   Create a comprehensive guide with:
   - A comparison table of React, Vue, and Angular
   - Numbered installation steps
   - A code example
   - Bold and italic text formatting
   - A blockquote with a tip
   ```
2. **Wait** for response to complete
3. **Verify** each element:

### Expected Elements

| Element | Verification |
|---------|--------------|
| Table | Borders visible, headers bold, rows alternate |
| Ordered list | Numbers 1, 2, 3... with proper indentation |
| Unordered list | Bullets with proper indentation |
| Nested list | Sub-items indented further |
| Bold text | **text** renders with heavier weight |
| Italic text | *text* renders with slant |
| Inline code | `code` has background highlight |
| Blockquote | Left border, indented, lighter text |
| Links | Underlined, opens in new tab |

### Pass Criteria
- [ ] Tables render with visible structure
- [ ] Lists have proper indentation
- [ ] Text formatting (bold/italic) applied
- [ ] Inline code visually distinct
- [ ] Links functional and styled
- [ ] No raw markdown visible

---

## Test 6: Token Usage Info

### Purpose
Verify response footer shows timing, token counts, and expandable usage details.

### UI Flow
```text
Send message → Wait for response → Verify footer → Click expand → Verify breakdown
```

### Steps

1. **Send** any message and wait for response to complete
2. **Verify** response footer displays:
   - Response time (e.g., `3575ms`)
   - Total token count (e.g., `848 tokens`)
   - Info icon button (aria-label="Show token usage details")
3. **Hover** over info icon
4. **Verify** usage details panel shows:
   - "Usage Information" header
   - Input tokens (e.g., `Input: 799 tokens`)
   - Output tokens (e.g., `Output: 49 tokens`)

### Console Evidence
```javascript
Action: {type: CHAT_STREAM_COMPLETE, usage: Object}
// usage object: { promptTokens, completionTokens, totalTokens }
```

### Pass Criteria
- [ ] Response time displayed after completion
- [ ] Total token count displayed
- [ ] Info icon button present
- [ ] Input/Output breakdown shows on hover
- [ ] Values are non-zero numbers

---

## Test Files Reference

| File | Purpose |
|------|---------|
| `test-files/test-prompts.json` | Prompts for each test scenario |
| `test-files/code-sample.md` | Expected code block rendering |
| `test-files/complex-response.md` | Expected complex markdown |
| `test-files/test.txt` | Plain text upload test |
| `test-files/test.png` | Image upload test |

---

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Theme not changing | ThemeContext not receiving update | Check FluentProvider wrapping |
| New chat button always disabled | `hasMessages` prop false | Check messages array binding |
| Cancel not working | AbortController not set | Check `currentStreamAbort` in ChatService |
| Code not highlighted | Language not detected | Check regex pattern in Markdown.tsx |
| Copy button not working | `copy-to-clipboard` import | Check package installed |
| Table not rendering | GFM plugin missing | Check `remarkGfm` in Markdown.tsx |

---

## Quick Validation Checklist

```text
□ Theme Toggle
  □ Settings opens
  □ Dark theme works
  □ Light theme works
  □ System theme works
  □ Persists on refresh

□ New Chat
  □ Button disabled initially
  □ Enabled after message
  □ Clears messages
  □ Resets conversation

□ Cancel Stream
  □ Stop enabled during stream
  □ Cancels immediately
  □ Preserves partial response
  □ Escape key works

□ Code Blocks
  □ Language label
  □ Copy button works
  □ Syntax highlighting
  □ Line numbers

□ Complex Markdown
  □ Tables
  □ Lists
  □ Formatting
  □ Links

□ Token Usage
  □ Response time shown
  □ Token count shown
  □ Info icon present
  □ Input/Output breakdown on hover
```
