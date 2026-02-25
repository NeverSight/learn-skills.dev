---
name: converting-minikit-to-farcaster
description: Converts Mini Apps from MiniKit (OnchainKit) to native Farcaster SDK. Use when migrating from @coinbase/onchainkit/minikit, converting MiniKit hooks, removing MiniKitProvider, or when user mentions MiniKit, OnchainKit, or Farcaster SDK migration.
---

# MiniKit to Farcaster SDK

## Breaking Changes (SDK v0.2.0+)

1. `sdk.context` is a **Promise** — must await
2. `sdk.isInMiniApp()` accepts **no parameters**
3. `sdk.actions.setPrimaryButton()` has no onClick callback

Check version: `npm list @farcaster/miniapp-sdk`

## Quick Reference

| MiniKit | Farcaster SDK | Notes |
|---------|---------------|-------|
| `useMiniKit().setFrameReady()` | `await sdk.actions.ready()` | |
| `useMiniKit().context` | `await sdk.context` | **Async** |
| `useMiniKit().isSDKLoaded` | `await sdk.isInMiniApp()` | No params |
| `useClose()` | `await sdk.actions.close()` | |
| `useOpenUrl(url)` | `await sdk.actions.openUrl(url)` | |
| `useViewProfile(fid)` | `await sdk.actions.viewProfile({ fid })` | |
| `useViewCast(hash)` | `await sdk.actions.viewCast({ hash })` | |
| `useComposeCast()` | `await sdk.actions.composeCast({ text, embeds })` | |
| `useAddFrame()` | `await sdk.actions.addMiniApp()` | |
| `usePrimaryButton(opts, cb)` | `await sdk.actions.setPrimaryButton(opts)` | No callback |
| `useAuthenticate()` | `sdk.quickAuth.getToken()` | See [AUTH.md](AUTH.md) |

## Context Access Pattern

```typescript
// WRONG
const fid = sdk.context?.user?.fid;

// CORRECT
const context = await sdk.context;
const fid = context?.user?.fid;
```

In React components, use state:

```typescript
const [context, setContext] = useState(null);

useEffect(() => {
  const load = async () => {
    const ctx = await sdk.context;
    setContext(ctx);
  };
  load();
}, []);
```

## Conversion Workflow

1. Verify Node.js >= 22.11.0
2. Update dependencies — see [DEPENDENCIES.md](DEPENDENCIES.md)
3. Replace imports: `@coinbase/onchainkit/minikit` → `@farcaster/miniapp-sdk`
4. Convert hooks using reference above
5. Add FrameProvider — see [PROVIDER.md](PROVIDER.md)
6. Update manifest: `frame` → `miniapp` — see [MANIFEST.md](MANIFEST.md)

## Common Errors

**"Property 'user' does not exist on type 'Promise<MiniAppContext>'"**
→ Await `sdk.context` before accessing properties

**"Expected 0 arguments, but got 1"**
→ Remove parameters from `sdk.isInMiniApp()`

**Context is null in components**
→ Ensure FrameProvider is in your provider chain

## References

- [MAPPING.md](MAPPING.md) — Complete hook-by-hook conversion reference
- [EXAMPLES.md](EXAMPLES.md) — Before/after code examples
- [PROVIDER.md](PROVIDER.md) — Provider setup with FrameProvider
- [PITFALLS.md](PITFALLS.md) — Common errors and solutions
- [DEPENDENCIES.md](DEPENDENCIES.md) — Package updates
- [AUTH.md](AUTH.md) — Quick Auth migration
- [MANIFEST.md](MANIFEST.md) — farcaster.json changes
