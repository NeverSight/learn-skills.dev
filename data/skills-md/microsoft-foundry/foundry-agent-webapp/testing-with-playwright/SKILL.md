---
name: testing-with-playwright
description: Provides Playwright MCP testing workflow for the web application. Use when testing UI changes, verifying chat functionality, debugging frontend issues, or validating state transitions in the browser.
---

# Testing with Playwright MCP

**CRITICAL**: Always test changes before completion.

## Subagent Delegation for Testing

**Screenshot operations blow up context fast** (~2000-5000 tokens each). Delegate to subagent for:
- Multi-step UI test scenarios
- Visual regression verification
- Accessibility audits
- Screenshot-heavy debugging

### Delegation Pattern

```text
runSubagent(
  prompt: "TESTING task with Playwright MCP.
    
    **Servers**: Frontend at localhost:5173, Backend at localhost:8080
    
    **Test Scenario**: [describe what to verify]
    
    **Steps**:
    1. Navigate to http://localhost:5173
    2. [specific actions to perform]
    
    **Check in priority order** (stop when answer found):
    1. Browser console logs - look for errors, state transitions (🔄)
    2. Network requests - verify API calls and status codes
    3. Accessibility snapshot - check element presence
    4. Screenshot - ONLY if visual verification essential
    
    **Return**:
    - Pass/Fail result
    - Specific evidence (error messages, status codes, element presence)
    - Console action log if relevant (🔄 ACTION_TYPE entries)
    
    Do NOT include raw screenshots or full accessibility dumps.",
  description: "Test: [what being verified]"
)
```

### When to Delegate vs Inline

| Delegate to Subagent | Keep Inline |
|----------------------|-------------|
| Multi-page flows | Single console check |
| Visual verification needed | Network status check |
| Accessibility audit | Element presence (single) |
| Error reproduction | Quick state verification |
| Screenshot required | Reading console logs |

## Testing Priority (Token efficiency)

1. **Browser console logs** - Check console messages for state transitions and errors
2. **VS Code terminal logs** - Check terminal output for backend/frontend server logs
3. **Network requests** - Inspect API calls and status codes
4. **Accessibility snapshot** - Get DOM structure for element verification
5. **Screenshots** - Visual verification (use sparingly, high token cost)

**Key insight**: Browser console shows React state changes (🔄 ACTION_TYPE), errors, and warnings. VS Code terminals show server logs and compilation output.

## Workflow

**Start servers in VS Code terminals** (preferred - logs visible to AI agent):
```powershell
# Run these VS Code tasks:
# - "Backend: ASP.NET Core API" (dotnet watch, port 8080)
# - "Frontend: React Vite" (npm run dev, port 5173)
# Or use compound task: "Start Dev (VS Code Terminals)"
```

**Then test with Playwright MCP**:
1. Navigate to http://localhost:5173
2. Check browser console for state transitions and errors
3. Verify network requests for API calls
4. Take accessibility snapshot for DOM validation

**Check server logs**:
- Check VS Code terminal output for backend compilation and request logs
- Backend terminal shows: request handling, errors, recompilation status
- Frontend terminal shows: HMR updates, build warnings, Vite output

## When to Test

- After UI component or API endpoint changes
- Before committing multi-step implementations
- When user reports issues

## Validation Checklist

- [ ] Console shows expected actions (🔄 [timestamp] ACTION_TYPE)
- [ ] No console errors/warnings
- [ ] Network tab shows correct status codes (200/400/401/500)
- [ ] DOM elements present in accessibility snapshot

## State Logging (Dev Mode)

Each state change prints:
```text
🔄 [HH:MM:SS] ACTION_TYPE
Action: { … }
Changes: { field: before → after }
```

## Project-Specific: Key Test Scenarios

| Scenario | What to Verify |
|----------|----------------|
| Initial load | Auth redirect, agent metadata loads |
| Send message | User message appears, streaming starts |
| Streaming | Text chunks append, no flicker |
| Annotations | Citations render with links |
| Cancel stream | Input re-enabled, status → idle |
| Error recovery | Retry button works, error clears |

## Project-Specific: Network Verification

| Endpoint | Success | Failure |
|----------|---------|---------|
| `POST /api/chat/stream` | 200 + SSE events | 401 (auth), 400 (validation) |
| `GET /api/agent/info` | 200 + JSON metadata | 500 (agent not found) |

## Playwright MCP

| Capability | Token Cost |
|------------|------------|
| Navigate | Low |
| Console logs | Low |
| Click / Type | Low |
| Accessibility snapshot | Medium |
| Screenshot | High |

Use console logs for state verification. Use snapshots for element presence. Avoid screenshots unless visual check required.

## Related Skills

- **validating-ui-features** - Detailed test procedures for specific features
- **writing-typescript-code** - Frontend patterns and state management
- **implementing-chat-streaming** - SSE flow verification
