---
name: realtime-and-subscriptions
description: >-
  Use when adding Supabase Realtime, live updates, chat, notifications, or
  postgres_changes subscriptions. Not for one-time fetches (use data hooks) or
  polling unless Realtime is unavailable.
---

# Realtime and subscriptions

Use Supabase Realtime for live data; pair with existing query cache (SWR/React Query) for initial load.

## Setup

1. Enable Realtime on the table in Supabase (publication / replica identity as required).
2. RLS must allow the subscriber to `SELECT` rows they receive.

## Subscription pattern

```ts
useEffect(() => {
  if (!channelId) return;

  const channel = supabase
    .channel(`room:${channelId}`)
    .on(
      "postgres_changes",
      { event: "*", schema: "public", table: "messages", filter: `room_id=eq.${channelId}` },
      (payload) => {
        // merge into local state or call mutate() on SWR/React Query key
      }
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}, [channelId]);
```

## Rules

- **Always unsubscribe** on unmount (`removeChannel`).
- Prefer **narrow filters** (`filter: \`room_id=eq.${id}\``) over subscribing to whole tables.
- On `INSERT`/`UPDATE`/`DELETE`, update cache via `mutate` / `queryClient.setQueryData` — avoid full refetch storms.
- Show connection status if UX needs it (optional reconnect banner).

## Presence / broadcast (chat typing)

Use `channel.on("presence", ...)` or `broadcast` only when product requires it; keep payloads small.

## Reconnect and offline

- Supabase Realtime auto-reconnects, but **stale state** is your problem: on `SUBSCRIBED` after a disconnect, refetch the initial query so missed events are reconciled.

```ts
.subscribe((status) => {
  if (status === "SUBSCRIBED") refetch();
});
```

- Optionally show a small "Reconnecting…" indicator if the channel disconnects.

## Avoid

- Leaving channels open after navigation away.
- Subscribing without RLS (leaks data).
- Duplicating Realtime + 1s polling for the same data.
- Subscribing to high-traffic tables without a filter.

## Checklist

- [ ] Cleanup in `useEffect` return.
- [ ] RLS verified for subscribed rows.
- [ ] Cache stays consistent with hook layer.
