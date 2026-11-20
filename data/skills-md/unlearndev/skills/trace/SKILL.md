---
name: trace
description: Answer a question about how something works in an unfamiliar codebase by tracing one journey end to end and drawing it as a visual flow diagram, with the exact file and line for every hop and a note of what's uncertain. Use when the user asks "how does X work", "where does X happen", "what happens when a user does X", "trace X", or is finding their way around a codebase they didn't write.
argument-hint: "<question about one flow>"
---

Answer one question about the codebase by tracing a single journey through
it and drawing that journey so it can be seen at a glance.

## Question

Raw arguments: $ARGUMENTS

The arguments are the question. If empty, ask what the user wants traced
and stop.

Turn the question into one journey with a starting point: something a
person or system does (submit a form, click a button, hit an endpoint, run
a command, a scheduled job fires) and the thing the question is about.

- If the question is really several journeys ("explain auth"), pick the one
  that answers it most directly.
- If the same thing is checked or done at more than one point (opening a
  form and saving it), trace the one the question is really about and
  mention the others in the answer.

## Trace

Don't read the codebase. Search for the starting point and follow it.

1. **Find the trigger.** Locate where the journey starts for a real user:
   the UI element that sends the request, the route, the command, the
   schedule entry. Before saying there is no trigger, check every place
   one could live: routes, UI, console commands and the schedule, queued
   jobs and event listeners, and the config of any auth or framework
   package that registers its own routes. If none of them reach the code,
   that is the answer. Say so first, then trace what the code would do if
   it were triggered some other way.
2. **Follow each hop** in the order things happen: route → middleware →
   controller → validation / authorization → models, events, observers,
   jobs, notifications → database → response. Follow the call, not the
   folder structure. Include what the framework and database do on their
   own: route model binding, policies found by convention, global scopes,
   model events, foreign key cascades, triggers.
3. **Read every line you cite.** Open the file and confirm the line says
   what you claim, and that every name on a `›` line exists there. A grep
   hit is a lead, not evidence. The report doesn't quote code, so this
   check is what keeps it honest.
4. **Stop at the answer.** Only follow branches that affect the question.

## Report

The report is a diagram first. Output exactly this structure and nothing
else:

1. `## 🔎 <the question, as one line>`
2. If you had to narrow the question down: `_Traced: <the journey>_`.
   Otherwise leave this line out.
3. The flow diagram, in a ```text code block.
4. One legend line in italics, listing only the symbols the diagram uses.
5. `**⚠️ Not sure**`: at most three one-line bullets for anything you
   inferred instead of reading, such as dynamic dispatch, env or config
   that changes behaviour, or code in external services. Say what would
   settle each one. Leave the section out if it's empty.

No preamble, no closing summary, no suggestions or fixes. Change nothing.

### Drawing the diagram

Each hop is a box. Boxes are stacked top to bottom and joined by arrows.

```text
╭─ <ICON> <KIND> ─────────────────────────────────────
│  <what happens, in plain words>
│  › <the names a developer would search for>
│  <file:line>
╰──────┬──────────────────────────────────────────────
       │  <what travels to the next hop, if worth saying>
       ▼
```

- **Technical detail.** Under the plain-words line, add up to two `›`
  lines naming what a developer new to the codebase would search for or
  trip over: class and method, route name, middleware alias, config key,
  table and columns, events fired, job and queue, HTTP status. Give names,
  not code, and skip anything the plain line already makes obvious. Leave
  the `›` lines out when there's nothing worth adding. When the arrow
  carries a request, label it with the method, path and fields.
- **Your code** uses a solid box: `╭─ │ ╰─`.
- **Vendor or framework code** uses a dashed box: `┌┄ ┆ └┄`. Put the
  package name in the header, like `📦 VENDOR · laravel/fortify`. Write
  the path relative to the package's `src/`.
  Collapse a package's internals into one box. Its middle line chains the
  steps with `→`. Split the box only if the question is about the package
  itself.
- **Implicit hops** happen by convention with no line of their own, like a
  policy found by name or route model binding. Add `⚡` after the KIND and
  cite the app line that relies on the hop.
- **Branches** go off the side of the arrow. Put the target's `file:line`
  underneath, then carry on with the main path, marked `✓`:
  ```text
         ├──✗──▶ <what happens instead>
         │       <file:line>
         ▼ ✓
  ```
  Only draw branches that matter to the question.
- **No trigger.** Make the first box `🚫 NO TRIGGER` and list where you
  looked. Join it to the rest with a dashed arrow (`┆`) labelled
  `if it ran anyway`.
- **Kinds and icons.** Use only these, since other emoji may misalign:
  👆 CLICK · 💻 COMMAND · ⏰ SCHEDULE · 🌐 REQUEST · 🔀 ROUTE · 🔒 GUARD
  (middleware, auth, policy, rate limit) · ✅ VALIDATE · 🧩 HANDLER
  (controller, action, job body) · 📣 EVENT (events, jobs dispatched,
  notifications) · 💾 DATABASE · 📦 VENDOR · 🏁 RESPONSE.
- Use **at most 7 boxes.** If the journey needs more, merge hops that do
  the same kind of thing, like three tables cascading, into one box.
- Keep every line under 60 characters so the diagram fits a narrow
  terminal. Paths are repo-relative, apart from the vendor paths described
  above.
- Don't draw a right-hand border. Emoji widths vary between terminals and
  would break it.

### Example

````
## 🔎 How does a user sign in?

```text
╭─ 👆 CLICK ──────────────────────────────────────────
│  "Sign In" posts email + password
│  › Inertia useForm(), password cleared on finish
│  resources/js/pages/Auth/Login.vue:13
╰──────┬─────────────────────────────────────────────
       │  POST /login {email, password} · login.store
       ▼
╭─ 🔒 GUARD ──────────────────────────────────────────
│  Guests only, max 5 tries a minute per email + IP
│  › middleware guest:web, throttle:login (else 429)
│  app/Providers/FortifyServiceProvider.php:43
╰──────┬─────────────────────────────────────────────
       ▼
┌┄ 📦 VENDOR · laravel/fortify ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
┆  validate → lowercase email → check password hash
┆  › LoginRequest → CanonicalizeUsername →
┆    AttemptToAuthenticate; guard fires Login event
┆  Http/Controllers/AuthenticatedSessionController.php:58
└┄┄┄┄┄┄┬┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
       │
       ├──✗──▶ wrong password: auth.failed on email
       │       Actions/AttemptToAuthenticate.php:99
       ▼ ✓
┌┄ 📦 VENDOR · laravel/fortify ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
┆  regenerate session → clear rate limit
┆  Actions/PrepareAuthenticatedSession.php:37
└┄┄┄┄┄┄┬┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
       ▼
╭─ 🏁 RESPONSE ───────────────────────────────────────
│  Redirect to intended page, else /dashboard
│  › 302 from LoginResponse, fortify.redirects.login
│  config/fortify.php:79
╰────────────────────────────────────────────────────
```
_╭─ your code · ┌┄ vendor · ✗ failure branch · ✓ main path_

**⚠️ Not sure**
- `AUTH_MODEL` in `.env` could swap the User model. Check `.env`.
````
