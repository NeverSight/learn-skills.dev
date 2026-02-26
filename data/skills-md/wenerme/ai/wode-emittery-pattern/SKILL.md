---
name: wode-emittery-pattern
description: 'Use when implementing event-driven communication between React components using Emittery, including event types, sidecar components, or subscription hooks'
---

# Wode Emittery Event-Driven Pattern

You are strictly required to follow this event-driven architecture when implementing inter-component communication or side-effect handling. This pattern decouples state management (Zustand) from side-effects (event handlers).

## 1. Core Rules (MUST FOLLOW)

1. **Event Types:** MUST use `as const` objects named `XxxEventType`. NEVER use TypeScript enums.
2. **Event Naming:** MUST use `Module:Action` format (e.g., `FileSystem:Open`, `User:Login`).
3. **Typed Emitter:** MUST define `type XxxEmitter = Emittery<XxxEventData>` for full type safety.
4. **Sidecar Pattern:** Side-effects (toast, confirm dialogs, network requests) MUST be handled in Sidecar components, NEVER inside Store actions.
5. **Store Decoupling:** Store actions MUST only emit events. They MUST NOT care who handles them.

## 2. Event Type Definition

```typescript
// MUST use as const, NEVER enum
export const FileSystemEventType = {
  Open: 'FileSystem:Open',
  Goto: 'FileSystem:Goto',
  Refresh: 'FileSystem:Refresh',
  Download: 'FileSystem:Download',
  Delete: 'FileSystem:Delete',
} as const;

// Event data types
type FileSystemEventData = {
  [FileSystemEventType.Open]: { fs: IFileSystem; file: IFileStat };
  [FileSystemEventType.Goto]: { path: string };
  [FileSystemEventType.Refresh]: {};
  [FileSystemEventType.Download]: { fs: IFileSystem; files: IFileStat[] };
  [FileSystemEventType.Delete]: { fs: IFileSystem; files: IFileStat[] | string[] };
};

// Emitter type
export type FileSystemEmitter = Emittery<FileSystemEventData>;
```

## 3. Emitter Factory & Store Integration

```typescript
import Emittery from 'emittery';

export function createEmitter<EventData = Record<string, any>>(name: string) {
  return new Emittery<EventData>({ debug: { name } });
}

// In Store — actions MUST only emit events
const events: FileSystemEmitter = createEmitter('FileSystemEmitter');

actions: {
  open: async (item) => {
    // Emit event, let Sidecar handle the rest
    return events.emit(FileSystemEventType.Open, { fs: getState().fs, file: item });
  },
  refresh: () => events.emit(FileSystemEventType.Refresh, {}),
}
```

## 4. useEmitteryListen Hook

```typescript
export function useEmitteryListen<E>(
  e: Emittery<E>,
  handle: { [K in keyof E]?: (data: E[K]) => void },
) {
  const ref = useRef<any>(handle);
  ref.current = handle;

  useEffect(() => {
    const unsub = Object.keys(ref.current).map((event) => {
      return e.on(event as any, (data) => ref.current[event]?.(data));
    });
    return () => unsub.forEach((fn) => fn());
  }, [e, ...Object.keys(handle).sort()]);
}
```

## 5. Sidecar Component

```tsx
export const FileManagerSidecar = () => {
  const { events, actions } = useFileManagerStore(
    useShallow((s) => ({ events: s.events, actions: s.actions }))
  );

  useEmitteryListen(events, {
    [FileSystemEventType.Refresh]: async () => {
      await load();
    },
    [FileSystemEventType.Delete]: async ({ fs, files }) => {
      const ok = await showConfirm({ title: '删除确认' });
      if (!ok) return;
      for (const file of files) await fs.rm(file.path);
      actions.refresh();
    },
  });

  return null; // Renders no UI
};

// Mount inside Provider
<FileManagerProvider>
  <FileManagerSidecar /> {/* Event handler */}
  {children}
</FileManagerProvider>
```

## 6. Advanced Patterns

For complete Sidecar implementation examples (upload, rename, move, mkdir, error handling) and best practices, read: [references/events-pattern.md](references/events-pattern.md)
