---
name: web-pwa-push-notifications
description: Add Web Push to a PWA - VAPID key generation, a permission flow that asks after a user action instead of on load, `pushManager.subscribe`, the service worker `push` and `notificationclick` handlers, and a Node sender with pinned `web-push` package. Use when a user says "push notifications", "notify users when", "send alerts to the app", "notification permission" or "web push".
---

# Push notifications

Web Push has three parts: the page subscribes (after the user says yes), your server stores the subscription and later signs a message with your VAPID private key, and the service worker shows it. Support is good in 2026: Chrome, Edge, Firefox and Samsung Internet on desktop and Android, Safari on macOS 13+, and Safari on iOS 16.4+ only when the app was added to the Home Screen. The permission prompt is the dangerous part: a browser-level "Block" is nearly permanent, so put your own explanation and button in front of it.

## Pattern

```bash
npm i web-push@3.6.7
npx web-push generate-vapid-keys        # once; keep the private key on the server only
# Public Key:  BNc...   -> VAPID_PUBLIC in the page
# Private Key: 7Hq...   -> VAPID_PRIVATE in server env, never in the repo
```

```html
<section class="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
  <h2 class="font-semibold">Get told when a report is approved</h2>
  <p class="mt-1 text-sm text-slate-600 dark:text-slate-300">One notification per report, nothing else.</p>
  <button data-push-toggle type="button" aria-pressed="false" class="mt-3 rounded-lg bg-teal-700 px-4 py-2 text-sm font-medium text-white hover:bg-teal-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-600">Turn on notifications</button>
  <p data-push-status class="mt-2 text-sm text-slate-500" aria-live="polite"></p>
</section>
```

```js
// /js/push.js
const VAPID_PUBLIC = 'BNc...';                 // the public key from generate-vapid-keys
const btn = document.querySelector('[data-push-toggle]');
const status = document.querySelector('[data-push-status]');
const supported = 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;

const toKey = (b64) => {                       // base64url -> Uint8Array (older browsers reject the raw string)
  const pad = '='.repeat((4 - (b64.length % 4)) % 4);
  const raw = atob((b64 + pad).replace(/-/g, '+').replace(/_/g, '/'));
  return Uint8Array.from(raw, (c) => c.charCodeAt(0));
};

async function current() { return (await navigator.serviceWorker.ready).pushManager.getSubscription(); }

async function subscribe() {
  const permission = await Notification.requestPermission();   // inside the click handler
  if (permission !== 'granted') { status.textContent = 'Notifications stay off. You can change this in site settings.'; return; }
  const reg = await navigator.serviceWorker.ready;
  const sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: toKey(VAPID_PUBLIC) });
  const res = await fetch('/api/push/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(sub) });
  if (!res.ok) { await sub.unsubscribe(); throw new Error('server rejected subscription'); }
}

async function unsubscribe() {
  const sub = await current(); if (!sub) return;
  await fetch('/api/push/unsubscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ endpoint: sub.endpoint }) });
  await sub.unsubscribe();
}

async function render() {
  if (!supported) { btn.hidden = true; status.textContent = /iphone|ipad/i.test(navigator.userAgent) ? 'On iPhone, add this app to your Home Screen first to enable notifications.' : 'Notifications are not supported in this browser.'; return; }
  const on = Boolean(await current());
  btn.setAttribute('aria-pressed', String(on));
  btn.textContent = on ? 'Turn off notifications' : 'Turn on notifications';
  status.textContent = Notification.permission === 'denied' ? 'Blocked in browser settings for this site.' : '';
}

btn.addEventListener('click', async () => {
  btn.disabled = true;
  try { (await current()) ? await unsubscribe() : await subscribe(); } catch (e) { status.textContent = 'Could not change notifications. Try again.'; console.warn(e); }
  btn.disabled = false; render();
});
render();
```

```js
// in sw.js
self.addEventListener('push', (e) => {
  const data = e.data?.json() ?? { title: 'Fieldbook', body: 'You have an update.' };
  e.waitUntil(self.registration.showNotification(data.title, {
    body: data.body, icon: '/icons/icon-192.png', badge: '/icons/badge-96.png',   // badge: monochrome, Android status bar
    tag: data.tag ?? 'general', renotify: Boolean(data.tag), data: { url: data.url ?? '/' },
  }));
});
self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const url = new URL(e.notification.data.url, self.location.origin).href;
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((wins) => {
    const open = wins.find((w) => w.url === url) ?? wins[0];
    return open ? open.focus().then((w) => (w.url === url ? w : w.navigate(url))) : self.clients.openWindow(url);
  }));
});
self.addEventListener('pushsubscriptionchange', (e) => {   // browser rotated the subscription; re-register it
  e.waitUntil(self.registration.pushManager.subscribe(e.oldSubscription?.options ?? { userVisibleOnly: true })
    .then((sub) => fetch('/api/push/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(sub) })));
});
```

```js
// server/send.mjs - node server/send.mjs  (Node 18+, web-push@3.6.7)
import webpush from 'web-push';
webpush.setVapidDetails('mailto:ops@example.com', process.env.VAPID_PUBLIC, process.env.VAPID_PRIVATE);
export async function sendToAll(subscriptions, payload, { remove }) {
  const body = JSON.stringify(payload);                      // { title, body, url, tag }  keep under 4 KB
  await Promise.allSettled(subscriptions.map((sub) =>
    webpush.sendNotification(sub, body, { TTL: 60 * 60, urgency: 'normal' }).catch((err) => {
      if (err.statusCode === 404 || err.statusCode === 410) return remove(sub.endpoint);   // gone: delete it
      throw err;
    })));
}
```

## Variations

- **Topic subscriptions**: store `{ endpoint, keys, topics: ['approvals'] }` server-side and filter before sending; the browser subscription itself is one per origin per user.
- **Silent data refresh**: not possible with `userVisibleOnly: true` (the only mode browsers accept); every push must show a notification or Chrome shows a generic one. Fetch fresh data inside the `push` handler before `showNotification` instead.
- **Actions**: `actions: [{ action: 'approve', title: 'Approve' }]` (Chromium only, max two) and branch on `e.action` in `notificationclick`.
- **Badge count**: `navigator.setAppBadge(n)` on the installed app icon (Chromium, Safari 16.4+ on Home Screen); clear with `clearAppBadge()` when the user opens the list.

## Pitfalls

- Asking for permission on page load is the fastest route to a permanent block and, in Chrome and Firefox, to a quieter prompt UI for your whole origin. Always behind a button with a sentence of context.
- Subscriptions expire and rotate; without `pushsubscriptionchange` handling and 404/410 cleanup, your list fills with dead endpoints and a provider may throttle you.
- The payload is encrypted by `web-push`; you still should not send secrets, and keep it under about 4 KB or some push services drop it.
- iOS: no support in a Safari tab, only in a Home Screen app, and a user who deletes the icon silently kills the subscription. Show the "add to Home Screen first" copy (`web-pwa-install-prompt`).
- `showNotification` from the page (`new Notification()`) is not the same API and does not work on Android Chrome; always go through the registration.
- VAPID keys are per app for life: rotating them invalidates every subscription. Back up the private key with your other secrets.

## Related skills

- `web-pwa-install-prompt`
- `web-pwa-service-worker-offline`
- `web-ui-toast-notifications`
- `web-form-submit-with-fetch`
- `web-ship-analytics-and-privacy`
