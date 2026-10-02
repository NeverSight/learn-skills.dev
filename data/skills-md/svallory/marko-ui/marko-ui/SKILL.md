---
name: marko-ui
description: Use when a project has a components.json from marko-ui, or when installing, using, editing, or debugging marko-ui components (shadcn-style components for Marko 6 backed by Zag.js) — finding a component, reading its API, adding it with the marko-ui CLI, fixing a component that renders but misbehaves, or setting marko-ui up in a new project. Not for general Marko 6 syntax (see marko6) or routing (see marko-run).
---

# marko-ui

[marko-ui](https://marko-ui.saulo.tech) is shadcn/ui for Marko 6: accessible components whose behavior comes from Zag.js state machines and whose styling is Tailwind v4. **Use the `marko-ui` CLI for everything below — do not hand-write a component that the registry already ships, and do not guess a component's props.**

Run the CLI with the project's package runner (`bunx marko-ui`, `npx marko-ui`, `pnpm dlx marko-ui`). Every command is non-interactive when stdin is not a TTY: confirmations are taken as yes, `init` uses its defaults, and `add` with no component names exits 2 instead of opening a picker.

## First: which distribution is this project on?

Read `distribution` in `components.json` (absent means `copy`). It changes how components are obtained and customized.

| | `copy` (default) | `import` |
|---|---|---|
| Components live in | the project, under the `ui` alias (`src/components/ui/<name>/`) | `node_modules/@marko-ui/shadcn` |
| Get a component | `marko-ui add <name> -y` | nothing to add — import `@marko-ui/shadcn/ui/<name>/<name>.marko` |
| Customize | edit the component file (it is the project's code) | override `mu-*` hook classes from the project stylesheet |

No `components.json` means marko-ui is not set up: run `marko-ui init` (add `--agents` to also write the agent docs).

## Workflow

1. `marko-ui search -q <query>` — find a component (`--json` for machine output). The installed ones are listed in the project's `AGENTS.md`.
2. `marko-ui docs <name>` — usage, props, keyboard contract, and examples as markdown. **Read this before writing markup for a component you have not used in this session.** `marko-ui docs --list` prints the index.
3. `marko-ui show <name>` — the registry item as JSON; `--files` lists what would be written, `--deps` lists npm and registry dependencies.
4. `marko-ui add <name> -y` — install (copy distribution). `--dry-run` previews the file changes; `--overwrite` replaces local files.
5. `marko-ui diff <name>` — compare local edits against the registry version.
6. `marko-ui doctor --json` — health checks; exit code 3 means something is broken and each failed check names its fix. Run it after `init`/`add` and before reporting the work done.
7. `marko-ui agents sync` — refresh the component list in `AGENTS.md` after adding or removing components.

`marko-ui manifest` prints every command, flag, exit code, and error code as JSON when you need the exact surface.

## Using components

```marko
import Dialog from "../components/ui/dialog/dialog.marko";
import Button from "../components/ui/button/button.marko";

<let/open=false/>

<Dialog open:=open>
  <@trigger|props|>
    <Button ...props>Edit profile</Button>
  </@trigger>
  <@title>Edit profile</@title>
  <@description>Make changes to your profile here.</@description>
  <p>Form fields go here.</p>
</Dialog>
```

- **Parts are attribute tags** (`<@trigger>`, `<@title>`), not separately imported subcomponents. `marko-ui docs <name>` lists each component's parts.
- **`<@trigger|props|>` hands you the machine props** to spread onto whatever element you render. It is the equivalent of Radix's `asChild`.
- **State binds with `:=`** (`open:=open`, `value:=value`, `checked:=checked`), or pass the value plus its `xChange` handler (`open=open openChange=(v) => { open = v }`).
- **On the copy distribution `add` also generates a taglib** (`marko.json`), unless the project already has its own `marko.json`, so installed components are usable as tags without an import (`<Button>`, `<CardHeader>`). An explicit import always works too.
- **Never import a component as `Input`.** It shadows Marko's reserved props type. The input component is imported as `TextInput`.

## Pitfalls that break components silently

Each of these has caused a real bug. Check your code against the list before finishing.

1. **Controlled props pin the machine.** `open=` / `value=` / `checked=` WITHOUT the matching `openChange` / `valueChange` / `checkedChange` (or the `:=` bind) freezes the component in that state. For an initial value only, use `defaultOpen=` / `defaultValue=` / `defaultChecked=`.
2. **Boolean `aria-*` / `data-*` attributes serialize wrong.** Marko renders boolean `true` as a bare attribute: `aria-selected=(bool)` emits `aria-selected=""` and `data-active=(bool)` never matches a `data-[active=true]:` Tailwind variant. Wrap in `String(...)`.
3. **Nothing from Zag crosses a tag boundary or lives in state.** Machine services and `api` objects contain functions and cannot be serialized for resume. Pass plain data, or a closure written in the template (`parentApi=() => api()`), and call `api()` at the use site.
4. **Do not read a parent component's `api()` inside a child's attribute-tag body.** Route it through the child's input as a closure instead. The symptom is `TypeError: ... is not a function` after an overlay opens.
5. **Overrides that do nothing (import distribution).** The style layer must be imported with `layer(components)` and the matching `@custom-variant style-<name>` line must exist in the project's stylesheet. Both fail silently.
6. **Unstyled components (copy distribution).** The theme stylesheet is not loading. Check that the file recorded as `tailwind.css` in `components.json` is imported by the root layout and that `@tailwindcss/vite` is in the Vite config. `marko-ui init` wires both; a hand-rolled setup often misses one.
7. **`"Cannot find module @zag-js/..."` or `marko-zag`.** A component's npm dependencies are missing. `marko-ui add` installs them; `marko-ui show <name> --deps` lists them.

For Marko 6 language rules (`<let>`, `<const>`, `<for>`, event handlers, TypeScript in templates) use the `marko6` skill; for `@marko/run` routing use `marko-run`.

## Editing a component (copy distribution)

The file is project code. Each `.marko` file starts with a `static const styles = { ... }` block holding the Tailwind classes per part: change classes there. Interactive components wire their machine with one tag, `<zag/api=() => machine from=input/>`, which picks the machine's props out of `input` and returns the `api` getter; keyboard handling, focus management, and ARIA come from the machine, so restyling cannot break accessibility. After editing, `marko-ui diff <name>` shows what diverged from the registry.

## More

- Docs: https://marko-ui.saulo.tech/docs (component pages as markdown: `/docs/components/<name>.md`)
- Writing a new component: https://marko-ui.saulo.tech/docs/creating-components
- Agent setup and troubleshooting: https://marko-ui.saulo.tech/docs/working-with-ai
