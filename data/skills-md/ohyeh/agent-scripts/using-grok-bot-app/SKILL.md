---
name: using-grok-bot-app
description: Read and drive the "Grok Bot" macOS desktop app (an Electron app) over CDP with agent-browser — list its bots and folders, read a conversation transcript, or check what a bot last said. Use this whenever the user mentions Grok Bot, "the bot app", NOVA, BOT_FACTORY, or a bot named in that app's sidebar, asks what one of those bots replied or is working on, or wants a message read from or drafted into that app — even when they only say "the bot app" without naming it. Not for the `grok-bot` deploy host (a Tailscale SSH machine that happens to share the name) and not for xAI's Grok API.
allowed-tools: Bash(agent-browser:*), Bash(pgrep:*), Bash(lsof:*)
---

# Using the Grok Bot app

`/Applications/Grok Bot.app` is an Electron app, so it is a Chromium renderer
wearing a native window: everything CDP does to a web page works here. Drive it
with `agent-browser`, never with Computer Use or synthetic clicks — those are
slower, unreliable, and unnecessary when a real DOM is one port away.

**Identity caveat.** The bundle identifier is `com.anysphere.sand` (Anysphere,
the Cursor vendor), not xAI. The name is a costume. Do not infer xAI API
semantics, model names, or rate limits from it.

**Name collision.** `box@grok-bot` in this fleet is a Tailscale deploy host, a
completely different thing. If the task is SSH, deployment, or port 5173, this
skill is the wrong one.

## Connect

The `--remote-debugging-port` flag only takes effect at launch, so an
already-running instance has no port to attach to and must be restarted. That
restart drops whatever is typed in the composer, which is why it needs the
user's OK before you pull the trigger.

```sh
pgrep -xl "Grok Bot"                                   # running?
lsof -nP -iTCP:9231 -sTCP:LISTEN                       # already debuggable?
pkill -x "Grok Bot"                                    # only with user approval
open -a "Grok Bot" --args --remote-debugging-port=9231
agent-browser connect 9231
agent-browser tab      # expect one target: file://…/app.asar/dist/renderer/index.html
```

If the port is already listening, skip straight to `connect` — no restart, no
approval needed, nothing lost.

## Address bots by UUID, never by name

Every sidebar entry is `button[data-agent-id="<uuid>"]` with the human-readable
name in `aria-label`. Names repeat — several bots are literally called `座位` —
so an `aria-label` selector silently picks whichever one the DOM happened to
order first. The UUID is the only stable key, and it has survived app upgrades
(observed across 0.29.0 → 0.39.0), so it is safe to remember one between
sessions and resolve it back to a name at run time.

## Read

Take one `snapshot -i` to see the shape of the tree, then switch to `eval` for
everything after that. Snapshots pour the whole accessibility tree into
context; `eval` returns exactly the JSON you asked for, which is the difference
between a cheap session and an expensive one.

Bot roster and folder structure, no clicking required:

```sh
agent-browser eval '(() => JSON.stringify({
  bots: [...document.querySelectorAll("button[data-agent-id]")]
    .map(b => ({id: b.getAttribute("data-agent-id").slice(0,8), name: b.getAttribute("aria-label")})),
  sidebar: document.querySelector("[aria-label=\"Bot list\"]")?.innerText.replace(/\n+/g,"|").slice(0,800)
}))()'
```

The sidebar text carries each bot's **last message preview and timestamp**, so
"what did RULES last say" and "which bots moved today" are answerable without
opening anything. Reach for the full transcript only when the preview is not
enough.

Full transcript of one bot — this requires selecting it, which changes what the
user sees on screen. The active bot is marked `aria-current="page"`, so capture
it in the same call that navigates away, and you can restore it afterwards
without guessing. Substitute the target UUID prefix for `<uuid8>`:

```sh
agent-browser eval '(async () => {
  const prev = document.querySelector("button[data-agent-id][aria-current=\"page\"]")
    ?.getAttribute("data-agent-id");
  document.querySelector("button[data-agent-id^=\"<uuid8>\"]").click();
  await new Promise(r => setTimeout(r, 2500));
  const g = [...document.querySelectorAll("[role=group][aria-label$=\"message\"]")];
  return JSON.stringify({prev, count: g.length, msgs: g.slice(-5).map(m =>
    m.getAttribute("aria-label") + ": " + (m.innerText||"").replace(/\s+/g," ").slice(0,200))});
})()'
```

Messages live in `[role=group]` nodes whose `aria-label` is `"<bot> message"`
or `"Your message"`, nested in `article` elements. Slice the text — a long
transcript will otherwise dump tens of thousands of characters into context for
no gain.

**Put the screen back.** Selecting a bot is a visible change to the user's app,
so click the captured `prev` UUID when you are done, and say that you did.
Restore by UUID rather than by name — names repeat, and there is no reliable
heading to read the state back from (`main h2` came back empty in practice).
Confirm with the whole panel's text instead:

```sh
agent-browser eval '(async () => {
  document.querySelector("button[data-agent-id^=\"<prev8>\"]").click();
  await new Promise(r => setTimeout(r, 1500));
  return (document.querySelector("main")?.innerText || "").replace(/\s+/g," ").slice(0,80);
})()'
```

## Sending is gated

Typing into the composer works: it is a single `div[contenteditable=true]` with
placeholder `Prompt`, and Enter submits. But a sent message is an irreversible
external side effect — another agent reads it and acts. So draft the text,
show it to the user verbatim, and send only after they approve that text.

## What will bite you

- **Element refs go stale.** `agent-browser click @e5` fails with
  `Could not locate element with role=button name=…` once React re-renders,
  because `@eN` means "the Nth node of that particular snapshot". Re-snapshot
  immediately before interacting, or bypass refs entirely with `eval` and a DOM
  attribute selector — the latter is what the recipes above do.
- **No local storage to shortcut through.** `localStorage`, `sessionStorage`,
  and `indexedDB.databases()` are all empty. The DOM is the only source, so
  there is no "just query the database" path; a full export costs one click and
  one wait per bot.
- **The two message counts disagree.** One conversation showed a header of
  "3 messages with 2 Bots" while the DOM held 7 `[role=group]` nodes. Which one
  is authoritative, and why they differ, is `UNCONFIRMED` — the header may count
  threads rather than messages, or the DOM may hold rendered system entries.
  Neither number is a safe answer on its own: if a transcript looks short or the
  counts disagree, scroll the `log "Conversation transcript"` container, re-read,
  and report what you actually saw.
- **`article` counts lie.** One `eval` returned a single `article` while the
  snapshot showed dozens. When dumping a whole transcript, prefer the union
  selector `'[role=article],article,[role=group]'`.
- **一趟抓不全，而且捲到頂會刪資料。** 對話串是虛擬化清單：`scrollTop = 0`
  一跳到頂，底部節點就被回收，等於邊讀邊刪（一次擷取因此掉了整天份的最新訊息）。
  可靠做法是兩種獨立方法各跑一趟再取聯集：**錨點法**（抓最頂那則
  `[role=group]`，`scrollIntoView({block:"start"})`，直到頂端訊息連續數次不變
  **且**總數不再增長——兩個條件要同時成立，只看一個會把「捲不動」誤判成「到頂」）
  與**像素法**（`[role=log][aria-label="Conversation transcript"]` 的 `scrollTop`
  由頂往下每次 0.8 屏）。去重鍵用 `aria-label + 前 120 字`，不要用 DOM 節點參照——
  同一則訊息被回收重建後是不同節點，內容才是穩定的身分。
  **兩法數字一致才算抓全**：五個 bot 兩法各自給出 151/151、53/53、38/38、10/10、
  7/7，那是可信的完整性證據；另一個 bot 兩法給 277 vs 132、聯集 372，就只能標
  `UNCONFIRMED`。
- **對話串短，先懷疑擷取方法，不要當成「這個 bot 沒在動」。** 一個每天回報的 bot
  曾被單趟擷取抓成 24 則、內容全是幾週前的設定過程，據此推論「它從沒回報過」——
  重抓後是 151 則，日報一直都在它自己的直接對話串上。另外，跨 bot 的往來還有獨立的
  exchange 串（側欄與訊息裡的 `button[aria-label^="Open exchange with"]`），
  那是**另一個**容器，不是日報的所在地；要讀跨 bot 對話才需要展開它。

## Where this came from

Everything above was executed against version `0.39.0` on macOS. The app ships
an embedded `Grok Bot's Computer` panel (a bot can hand its screen over for
interactive login and take it back) which is visible in the tree but unexplored
— if a task needs it, expect to map it yourself and write down what you find.
