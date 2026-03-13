---
name: writing-typescript-code
description: Provides TypeScript and React coding standards for this repository. Use when writing or modifying TypeScript code, creating React components, implementing MSAL authentication, or working with the frontend.
---

# TypeScript Coding Standards

**Goal**: Write type-safe React components with proper MSAL integration

## Hot Module Replacement (HMR) Workflow

**The frontend runs with Vite HMR**. When you edit TypeScript/React code:

1. **Save the file** - Vite instantly updates the browser (no refresh needed)
2. **Check the terminal** - Look for HMR updates in the "Frontend: React Vite" terminal
3. **State is preserved** - React state persists through most edits

**VS Code Tasks** (use `Run Task` command or check terminal panel):
- `Frontend: React Vite` - Runs `npm run dev` with HMR enabled
- Logs are visible directly in VS Code terminal

**No restart needed** - Just edit, save, and see changes instantly in the browser.

**Testing changes**: Use Playwright browser tools to:
- Navigate to http://localhost:5173
- Check browser console logs for state transitions and errors
- Inspect network requests for API validation

## TypeScript Config

Enable strict mode + explicit types (avoid `any`):

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

## React Components

Use functional components + hooks + typed props:

```typescript
interface MessageProps {
  message: string;
  sender: 'user' | 'agent';
}

function Message({ message, sender }: MessageProps) {
  return <div className={`msg-${sender}`}>{message}</div>;
}
```

## MSAL Pattern

**Always**: Try silent first, fallback to popup:

```typescript
try {
  const { accessToken } = await instance.acquireTokenSilent({
    ...tokenRequest,
    account: accounts[0]
  });
  return accessToken;
} catch {
  const { accessToken } = await instance.acquireTokenPopup(tokenRequest);
  return accessToken;
}
```

## Environment Variables

**CRITICAL**: Access at module level only (build-time replacement):

```typescript
// ✅ Correct - module level
const clientId = import.meta.env.VITE_ENTRA_SPA_CLIENT_ID;

// ❌ Wrong - inside function (won't work after build)
function getClientId() {
  return import.meta.env.VITE_ENTRA_SPA_CLIENT_ID;
}
```

**Available variables**:
- `VITE_ENTRA_SPA_CLIENT_ID` - Entra app client ID
- `VITE_ENTRA_TENANT_ID` - Azure tenant ID

## State Management

Use `useState` (local) or Context API (shared):

```typescript
const [messages, setMessages] = useState<Message[]>([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<Error | null>(null);
```

## Memoization Patterns

Use `useMemo` and `useCallback` for expensive computations and stable references:

```typescript
// Memoize computed values
const isAuthenticated = useMemo(
  () => accounts.length > 0,
  [accounts.length]
);

// Memoize callbacks to prevent child re-renders
const getAccessToken = useCallback(async () => {
  // ... token acquisition logic
}, [instance, accounts]);

// Return memoized object for stable reference
return useMemo(
  () => ({ getAccessToken, isAuthenticated, user }),
  [getAccessToken, isAuthenticated, user]
);
```

## API Calls

Include `Authorization` header + use `async/await`:

```typescript
const response = await fetch('/api/endpoint', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});

if (!response.ok) throw new Error(`API error: ${response.status}`);
```

## npm Dependencies

`frontend/.npmrc` sets `legacy-peer-deps=true` automatically — no flag needed when running from `frontend/`.

**Gotcha**: `legacy-peer-deps` skips automatic peer dependency installation. If a package requires peer deps, add them explicitly to `package.json`.

**Example**: `@lexical/yjs` requires `yjs` as a peer dependency. Since peer deps aren't auto-installed, `yjs` must be in `package.json` directly.

**Before committing package changes**, verify with:
```bash
npm ci  # Fails if lock file is out of sync with package.json
```

## Common Mistakes

- ❌ Accessing `import.meta.env.*` in functions
- ❌ Calling hooks conditionally or in loops
- ❌ Using `any` type
- ❌ Storing tokens in component state
- ❌ Running `npm install` outside `frontend/` (misses `.npmrc` config)
- ❌ Missing memoization in custom hooks (causes infinite re-renders)
- ❌ Returning new objects from hooks without `useMemo`

---

## Project-Specific: Architecture

| Concern | Implementation |
|---------|----------------|
| **State Management** | Centralized Context + `useReducer` (`AppContext`) with discriminated action union |
| **Authentication** | MSAL redirect flow; silent token refresh; `useAuth` hook |
| **Chat Streaming** | SSE in `ChatService` with abort controllers for cancellation |
| **Accessibility** | Live region (`aria-live`), aria labels, focus management |
| **Logging** | Dev-only diff-based logger |

## Project-Specific: Key Components

| Component | Purpose |
|-----------|---------|
| `AgentChat.tsx` | Container wiring chat state to controlled `ChatInterface` |
| `ChatInterface.tsx` | Stateless controlled UI; renders messages, input, errors, BuiltWithBadge |
| `chat/AssistantMessage.tsx` | Memoized assistant message with streaming + citation footnotes |
| `chat/UserMessage.tsx` | Memoized user message with image thumbnail previews |
| `chat/ChatInput.tsx` | File uploads, character counter, cancel streaming button |
| `chat/CitationMarker.tsx` | Inline superscript citation badge with tooltip + click handler |
| `core/Markdown.tsx` | Renders markdown with inline citation markers via `ContentWithCitations` |
| `core/BuiltWithBadge.tsx` | \"Built with Microsoft Foundry\" link badge (centered under input) |

## Project-Specific: Citation System

**Parser**: `frontend/src/utils/citationParser.ts`

Handles Azure AI Agent citation formats:
- Assistants/Responses API: `【4:0†source】`, `【13†myfile.pdf】`
- Azure OpenAI On Your Data: `[doc1]`, `[doc2]`

**Flow**:
1. `parseContentWithCitations()` replaces placeholders with `[N]` markers
2. `Markdown.tsx` renders `CitationMarker` components for each `[N]`
3. Clicking inline marker scrolls to footnote (with highlight animation) or opens URL
4. `AssistantMessage.tsx` renders footnote list with icons by type (URI/file/document)

**Key Types** (`frontend/src/types/chat.ts`):
- `IAnnotation` - Citation metadata (type, label, url, fileId, quote, textToReplace)
- `IndexedCitation` - Parsed citation with display index

## Project-Specific: File Upload Validation

**Limits**: 5MB per file, max 5 files total

**See**: `frontend/src/utils/fileAttachments.ts` for `validateImageFile()` and `validateFileCount()`

## Project-Specific: ChatService

**File**: `frontend/src/services/chatService.ts`

Key patterns:
- Class-based service with `Dispatch<AppAction>` for state updates
- `AbortController` for stream cancellation (`cancelStream()`)
- `retryWithBackoff()` for resilient API calls (3 retries, 1s initial delay)
- SSE parsing via `parseSseLine()` and `splitSseBuffer()` utilities
- Duplicate chunk suppression to prevent UI flicker

**Methods**:
| Method | Purpose |
|--------|---------|
| `sendMessage()` | Orchestrates auth, file conversion, streaming |
| `cancelStream()` | Aborts active stream, dispatches `CHAT_CANCEL_STREAM` |
| `clearChat()` | Resets conversation state |
| `clearError()` | Clears error without affecting chat |

## Project-Specific: Adding Features

1. **Extend state**: Add discriminated action to `AppAction` union in `frontend/src/types/appState.ts`
2. **Handle in reducer**: Update `frontend/src/reducers/appReducer.ts` (keep pure, no side effects)
3. **Create service method**: Add to `ChatService` if network interaction needed
4. **Wire container**: Update `AgentChat.tsx` to dispatch actions
5. **Update UI**: Pass callbacks to controlled component

## Project-Specific: Accessibility Checklist

- ✅ Live region announces latest assistant message
- ✅ `aria-busy` attribute on messages container during streaming
- ✅ Buttons have `aria-label` when icon-only
- ✅ Focus returns to input after sending
- ✅ Character counter linked via `aria-describedby`

## Related Skills

- **implementing-chat-streaming** - SSE streaming patterns and frontend state flow
- **troubleshooting-authentication** - MSAL popup issues and token debugging
- **testing-with-playwright** - Browser testing and accessibility validation
