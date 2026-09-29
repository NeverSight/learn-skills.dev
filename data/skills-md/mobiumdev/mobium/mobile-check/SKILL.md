---
name: mobile-check
description: Automate native mobile apps with the Mobium CLI, on Android emulators and phones and iOS simulators and iPhones. Use to launch and drive an app, fill forms, read the screen, answer system dialogs, reach into WebViews, capture screenshots and recordings, or confirm that a mobile change actually works.
---

# Mobium Mobile Automation — CLI Reference

The `mobium` CLI automates **native apps** on Android emulators and phones, and
iOS simulators and iPhones.
A background daemon keeps the device session alive between commands, so each
command is fast after the first.

```
mobium launch com.example.shop && mobium map && mobium tap @e5 && mobium map
```

If you need a *browser* rather than an app, use vibium instead. Mobium drives
apps; a WebView inside an app is covered here, a browser is not.

## Core Workflow

Every automation follows the same loop:

1. **Map**: `mobium map` — lists what is on screen as `@e1`, `@e2`, …
2. **Act**: `mobium tap @e5`, `mobium type @e2 "text"`, `mobium swipe up`
3. **Re-map**: after anything that changes the screen, run `mobium map` again

**Refs are only valid for the screen they were taken from.** A ref is
re-resolved against a fresh snapshot before every action, so a stale one fails
loudly rather than tapping the wrong thing — but that means you must re-map
after navigating.

## Binary Resolution

Resolve the `mobium` binary path once before running commands:

1. Try `mobium` directly (works if it is on PATH)
2. Fall back to `./bin/mobium` (dev environment, in the project root)

Run `mobium --help` to confirm, then use the resolved path throughout.

## First: check there is a device

```sh
mobium devices
# emulator-5554   device   (android emulator, model: sdk_gphone64_arm64)
```

If nothing is listed, the user needs to start an emulator or simulator, or plug
in a phone (Android with USB debugging on; an iPhone trusted and unlocked) —
you cannot do it for them from mobium. Say so rather than retrying.

## Commands

### Getting to the screen you want
- `mobium current` — which app is in the foreground
- `mobium state <package|bundle-id>` — any app: not installed, not running,
  background or foreground
- `mobium shake` — shake an emulator or simulator (shake-to-undo, a debug
  menu); a real phone refuses. Check the screen after: whether the app
  reacts is its own detector's business
- `mobium background 5` — send the app in front away for 5 seconds and bring
  it back where it was: how a resume path is tested
- `mobium launch <package|bundle-id>` — open an app
- `mobium terminate <package|bundle-id>` — stop it, to start a flow clean
- `mobium open <url>` — a URL or deep link, the quickest route to a screen
- `mobium install <path>` — install a local .apk or .app
- `mobium apps` — what is installed; `--system` includes the platform's own
- `mobium uninstall <package|bundle-id>` — remove one, verified by listing
  afterwards, because `adb uninstall` reports success when it has only removed
  the updates to a system app

**Refs do not survive these.** Launching, terminating or opening a link
discards the previous screen's refs; run `mobium map` afterwards.

Use `mobium current` to check a tap went where you expected:

```sh
mobium tap @e5 && mobium current
```

### When something fails for no good reason

`mobium doctor` checks the environment and needs no device — that is the
point. Several of the toolchain's own errors name the wrong cause, so run it
before believing one of them. It exits non-zero if it found anything.

### Discovery
- `mobium map` — actionable elements with `@refs` (run this before interacting)
- `mobium find <locator>` — matching elements, without tapping
- `mobium text` — everything readable on screen
- `mobium text @e3` — the text of one element

### Waiting

Never sleep. Every action already retries for two seconds while the screen
settles, so a tap straight after a launch or another tap is fine. When
something takes longer than that — a login, a network fetch — wait for the
thing itself rather than for a duration:

- `mobium wait "text=Welcome back"` — until it is on screen
- `mobium wait role=progressbar --for hidden` — until a spinner goes
- `mobium wait @e4 --for text --text "Sent"` — until its text says so
- `mobium wait testid=submit --for enabled` — until a control can be used
  (`--for disabled` for the other way)
- `mobium wait testid=terms --for checked` — a checkbox, radio or switch
  (`--for unchecked` for the other way)
- `mobium wait testid=search --for value --text ""` — until a field holds
  exactly that (here: nothing); `--for text` matches part of what it says
- `mobium wait testid=email --for focused` — until the field has the cursor
- `mobium wait "text=Done" --timeout 30s` — default is 10s

A wait that succeeds remaps the screen, so the element it found already has a
ref and can be tapped without a `mobium map` in between. A wait that fails
says what was on screen instead, which is usually the answer.

### Reaching things below the fold

`mobium map` only sees what is currently on screen. Tap, type and long-press
already scroll to a target that is not, so most of the time nothing extra is
needed — reach for `scroll-to` to look without acting, or to go back up:

- `mobium scroll-to "text=Sign out"` — bring it into view and get a ref
- `mobium scroll-to "text=Network & internet" --direction up`

Vertical lists only. For a horizontal pager or carousel use `mobium swipe
left`. If a scroll reports that the swipe changed the screen instead of
scrolling it, the thing being swiped was not a vertical list.

### Permissions

A first-launch permission dialog will stop a flow dead. Grant before you start
rather than trying to tap through it:

- `mobium grant com.example.shop all` — everything the app declares
- `mobium grant com.example.shop camera location` — just these
- `mobium revoke com.example.shop location` — test the app without it
- `mobium reset-permissions com.example.shop` — that app back to prompting,
  "don't ask again" included; with no app, every app on the device

Names are the same on both platforms where both have the thing. Where they do
not — `camera` and `notifications` have no iOS simulator equivalent,
`reminders` and `siri` have no Android one — you get an error saying so rather
than a silent no-op. On Android the grant is verified by reading the state
back, and anything the app never declared is reported as skipped.

### Battery and clock

- `mobium battery` — level, charging state, and on Android what powers it; an
  iOS simulator has no battery and says so
- `mobium time` — the device's clock in its own zone; a simulator's is the
  Mac's, and the answer says so

### Tests

`mobium test` runs `*.test.json` files: each test is a list of the same
steps `app_batch` takes — `{"name": "app_tap", "arguments": {...}}` — and its
assertions are `app_wait_for` steps (`not`, `exact` and `count` included) or
`{"expect": {"tool": ..., "field": ..., "equals": ...}}` on a tool that only
reads. Projects in `mobium.config.json` are devices — or, with
`MOBIUM_GRID` set, a `platform` each, and every project leases its own
device from the grid for the run. `-g`, `--project`,
`--retries`, `--last-failed`, `--reporter list,junit,html`, then
`mobium show-report`. A failure keeps the step, its error code, a screenshot
and the map. `tests/` in the repository is a worked example.

### Network

- `mobium network` — what is in place: online or offline, and any shaping
- `mobium network --offline` / `--online` — airplane mode, waited for until
  the network is really gone or back; an emulator or a real Android phone
- `mobium network --latency 300 --download 1600 --upload 750` — shape the
  traffic, replacing any shaping before; an emulator only (it needs root)
- `mobium network --reset` — no shaping, airplane mode off. The end of the
  session does this for you, back to how it found the device
- iOS refuses all of it: nothing outside it controls its network

### Light and dark

Dark mode is a different rendering of every screen and is where contrast and
hard-coded colors break, so a flow is worth running in both:

- `mobium appearance` — what is it now?
- `mobium appearance dark` / `light` — switch, confirmed by reading it back
- `mobium appearance auto` — Android only; iOS says it has no such thing

Switching discards the refs from the last map, so map again afterwards.

Accessibility settings are the same kind of rendering change, and each lasts
only for the session — the device is put back exactly as it was when it ends:

- `mobium accessibility` — every setting the device has, as it is now
- `mobium accessibility bold_text on` — reduce_motion, bold_text,
  increase_contrast, invert_colors, grayscale and the rest take on or off
- `mobium accessibility text_size accessibility-large` (iOS) /
  `text_scale 1.3` (Android) — text size is a category on one and a scale on
  the other, and each says so if given the other's

On a real iPhone, where nothing outside can change them, Mobium goes through
the Settings app and comes back to the app that was in front — about ten
seconds a change. The six switches work there; invert_colors, grayscale and
text size are refused, naming the Settings screen. On Android a text-size
change restarts the running app's screen, so map again afterwards.

### Acting

Every action waits, for up to two seconds, until its target is on screen,
**enabled** and holding still, and refuses — with a reason and a remedy —
rather than tapping something a user could not: a target under a system
dialog or under the keyboard, a control that stays disabled, or a button
passed to `type`.

- `mobium tap @e5` — tap a ref
- `mobium tap "text=Sign In"` — tap by locator, no map needed
- `mobium tap 540 1200` — tap raw device coordinates
- `mobium type @e2 "hello@example.com"` — type into an element, after what it holds
- `mobium type @e2 ""` — clear a field
- `mobium fill @e2 "new"` — replace the contents (Vibium's fill; `type` adds to them)
- `mobium swipe up` — scroll down the page (the finger moves up)
- `mobium swipe left` — next pager screen
- `mobium swipe 540 1800 540 600` — exact drag
- `mobium long-press @e4` — open a context menu
- `mobium screenshot -o shot.png` — capture the screen

### Several steps in one call

- `mobium batch steps.json` (or `-` for stdin) — run a known sequence in one
  call: `[{"name": "app_tap", "arguments": {"target": "text=Sign in"}}, ...]`,
  each step a tool and the arguments it takes on its own

Every step is checked before the first runs, and the batch stops at the
first failure with that step's own error and exit status. Use it for steps
whose outcome you do not need to read before choosing the next; after an
`app_map` step, prefer locators to refs, since the map replaces them.

### Locators

Locators work the same on both platforms, so one script targets either:

| Locator | Android | iOS |
| --- | --- | --- |
| `text=Sign In` | element text | element value |
| `label=Email` | content-desc | accessibility label |
| `testid=submit` | resource-id | accessibility identifier |
| `role=button` | widget class | XCUIElementType |
| `class=RecyclerView` | exact class | exact type |

Roles: `button`, `input`, `password`, `checkbox`, `switch`, `radio`, `link`,
`image`, `list`, `tab`, `text`.

Add `,role=button` to narrow an ambiguous locator: `text=Continue,role=button`.

**`role=password` is how you address a password field.** Mobium never prints
its contents — `map` shows the field's resource id and reads come back as
`•••••••••••• (12 characters, hidden: …)` — so there is no visible text to
match on. `password` is a narrower `input`: `role=input` matches these too.

### Hybrid apps (WebViews)

Web content inside an app is a separate context:

```sh
mobium contexts                      # NATIVE_APP, WEBVIEW_com.example
mobium context WEBVIEW_com.example   # map and tap now work on the page
mobium context NATIVE_APP            # back to the native shell
```

This works on **both platforms**. Android WebViews must be debuggable
(`setWebContentsDebuggingEnabled(true)`) and iOS WKWebViews must be inspectable
(`webView.isInspectable = true` on iOS 16.4+). If a WebView does not appear in
`contexts`, that is a property of the app — do not keep retrying.

```sh
mobium logs                  # what has the page logged since the last read?
mobium logs --level error    # uncaught errors and rejections
mobium eval "document.title" # ask the page directly
```

`logs` drains what it returns, so it reports what happened since the last call —
which is how you assert "nothing was logged during this step". Capture starts
when you enter the context, so a page's initial load is already over.

Two things that look like bugs and are not:

- **`map` may say "these elements cannot be tapped".** The page's position
  inside its host element is unknowable there — mobile Safari is the usual
  cause. The refs, labels and `mobium text` are still correct; only acting on a
  coordinate is refused. Read the page, act natively, or use a deep link.
- **"the page never announced a target"** means another debugger already holds
  that page. Ask the user to close Safari's Web Inspector, or run
  `mobium daemon stop` if a previous session is still switched into it.

Switch back to `NATIVE_APP` when finished with a page. Leaving a session inside
one keeps it locked away from everything else.

### Device state

```sh
mobium orientation                  # which way, and is it pinned?
mobium orientation landscape        # turn it and pin it
mobium orientation auto             # follow the sensor again
mobium locale org.wikipedia ja-JP   # run one app in Japanese
mobium locale org.wikipedia ""      # back to the device language
```

Both invalidate the refs from the last `map` — a rotation re-lays out every
screen and a language change re-renders it, so map again before acting.

Two honest limits worth knowing, because neither platform will tell you:

- **An activity that pins its own orientation cannot be turned from outside.**
  Mobium reports that rather than claiming success.
- **Setting a language confirms the device stored the tag, not that the app
  speaks it.** Android accepts a tag the app has no translation for and the app
  then renders in its default language. Look at the screen.

Relaunch an app after changing its language, or it keeps the old one.

### Interruptions and hardware buttons

```sh
mobium press back                  # primary navigation on Android
mobium press home                  # the one press mobium can confirm
mobium lock lock                   # a state, not a toggle
mobium call ring                   # then accept, or hang
mobium sms "your code is 123456"
mobium timezone Asia/Tokyo
mobium notifications               # what is in the shade?
mobium notifications --post "your code is 123456"
mobium notifications --shade open  # now the notification can be tapped
```

Every one of these can move the screen, so map again before acting.

- **iOS has no back button.** Mobium refuses rather than sending an edge
  swipe — a different event an app can tell apart. Map the app's own back
  chevron and tap it.
- **Calls and messages are emulator-only.** A real phone cannot be made to ring
  from outside. Mobium says which it is rather than failing obscurely.
- **A notification cannot be tapped until the shade is open.** Until then it is
  not on screen and `map` cannot see it: `notifications --shade open`, then
  `map`, then tap it. Close the shade when finished, or every later locator
  fails against a panel covering the app.
- **Only `press home` reports a confirmed outcome.** What `back` does is the
  app's business; re-map to see where you ended up.

### Dialogs

- `mobium alert` — is a system or app dialog up, and what does it say
- `mobium alert accept` / `dismiss` — answer it. **These do not choose an
  outcome**: which button each presses depends on the platform and the dialog
  (on a three-button iOS alert, `accept` pressed Cancel). To choose, tap the
  button by its caption: `mobium tap "text=Allow,role=button"` (iOS captions
  are labels: `label=Allow`).
- `mobium dialogs --when "Save Password" --press "Not Now"` — declare an
  answer for a dialog that turns up on its own schedule. An action that meets
  it presses that button, confirms the dialog went, carries on, and says so
  in its result. `mobium dialogs` lists the rules, `--clear` removes them.

### Choosing a device or backend
- `--device <serial>` — when more than one device is running
- `--driver uiautomator` — Android without installing anything (slower, and
  it cannot type)
- `--driver wda` — iOS simulators and iPhones
- `--driver <anything else>` — a third-party driver the user installed, as an
  executable named `mobium-driver-<name>`. `mobium doctor` lists the ones it
  can find. Such a driver may not support everything: if it refuses something,
  it never advertised that capability and retrying will not help.

## Reading map output

```
@e1 Search (input)
@e2 Sign In (button)
@e3 Remember me (checkbox)
```

Each line is `@ref label (role)`. Pick by the label, act with the ref.

**Prefer the `@ref` to retyping the label.** Many labels are composed from
several elements — a search result's title plus its description, say — so no
single element carries that text and `text=<the whole label>` will not match
it. A label ending in `…` has been shortened for readability and will not match
either. The ref always works; it is printed for that reason.

`map` lists only what is actionable **and on screen**. Something a locator can
resolve may still be absent from the map — scrolled out of its container, or
reported by the platform as not visible. That is why an element you can see in
a screenshot but not in `map` is usually a scroll away, not a bug.

## Command Chaining

Chain with `&&` when the steps are independent of each other's output:

```sh
mobium map && mobium tap @e2 && mobium map
```

Do **not** chain when you need to read the output to decide what to do next —
run those separately so you can look at the map before choosing a ref.

## When things fail

Mobium's errors say what to do; read them rather than retrying blindly.

Every failure also carries a **code**, so you can act on the kind without
parsing the sentence: `--json` prints it (`"code": "no_such_element"`, with a
`remedy` and `details`), and the exit status groups it:

| Exit | Codes | What to do |
| --- | --- | --- |
| 2 | `invalid_argument` | fix the command; retrying it unchanged cannot help |
| 3 | `no_device`, `device_not_ready`, `toolchain_missing` | ask the user: start or unlock a device, install a tool |
| 4 | `no_such_element`, `ambiguous_locator`, `element_not_reachable`, `no_such_context`, `no_such_alert` | re-map, narrow the locator, or scroll |
| 5 | `unsupported` | this device or backend cannot; do not retry |
| 6 | `timeout` | the one kind worth retrying as it is |
| 7 | `not_confirmed` | the command claimed success and the device disagrees — report it, it is a finding |
| 1 | anything else | read the message |

- `no element matches … — the screen may have changed, run map again`
  The screen moved. Re-map and pick a fresh ref.
- `… matches N elements — narrow it by appending ",role=button" …`
  Ambiguous locator. Add a role or map and use a ref.
- `the uiautomator backend cannot type into an element`
  Drop `--driver uiautomator`; the default backend can type.
- `the <name> backend cannot …`
  That backend never advertised the capability. Switch backends; do not retry.
- `a dialog is over the app — "…" — and nothing on it matches …`
  Answer the dialog first (`mobium alert`, or tap its button), or declare a
  rule with `mobium dialogs`.
- `… failed check <check>: <reason> — <what to do>`
  The target is there and an action refused to touch it. The check is in
  the error's details too; decide by it, not by the wording:
  - `visible` — off screen: `mobium scroll-to` it.
  - `enabled` — disabled: do what enables it, or
    `mobium wait <target> --for enabled`.
  - `stable` — still moving: wait, or tap by coordinates if it animates on
    purpose.
  - `receivesEvents` — something is over it: a dialog (answer it), the
    keyboard (`mobium keyboard --hide`, or on an iPhone
    `mobium keyboard --key enter`), or the app's own control (dismiss it, wait
    for it to go, or tap it if it is what you meant).
  - `editable` — not a text field: use `tap` for it; `type` is for fields.
- `no Android device or emulator is running`
  Ask the user to start one. Mobium cannot.
- `"…" is a locator, and locators do not work inside a WebView`
  You are in a web context. Use a `@ref` from `map`, or `mobium context
  NATIVE_APP` to get back to the app shell.

## Verifying your work

A command reporting success is not evidence the app did anything. After an
action that should change the screen, confirm it:

```sh
mobium tap @e5 && mobium map        # did the screen change as expected?
mobium screenshot -o after.png      # look at it when the map is ambiguous
```
