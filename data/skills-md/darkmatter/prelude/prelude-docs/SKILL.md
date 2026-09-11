---
name: prelude-docs
description: Manage a consumer repo's Prelude docs viewer content — prelude.docs.pages, groups, mdSplit README hero, and generated nixosOptions pages. Use when adding or fixing project documentation shown by `docs` / `x docs`, wiring the README landing page, or generating option docs.
argument-hint: <docs task>
---

# Prelude docs in a consumer repo

Treat the user's argument as the task description (e.g. "add a recipes page under
a Guides group"), not a shell command. Manage the requested Markdown sources
and existing `prelude.docs.*` configuration; preserve unrelated settings.

Prerequisite: the repo imports `prelude.flakeModules.default` (see the
`prelude-install` skill). The docs viewer has **no enable flag** — it activates
automatically when `prelude.docs.pages` is non-empty, which also installs the
`docs` command, its `x docs` dispatch, and the `d` accelerator.

## Authored pages

`prelude.docs.pages` is a nav tree in declaration order. Every node is exactly
one of leaf / group / generate:

```nix
prelude.docs.pages = [
  { text = ./docs/getting-started.md; }        # leaf
  { title = "Guides";                          # group: nests, renders no body
    children = [ { text = ./docs/guides/a.md; } ]; }
];
```

- Leaf `{ text = <markdown path>; }` — the file's first H1 labels the sidebar;
  an optional `title` overrides it.
- Group `{ title; children; }` — sidebar-only nesting. A hand-written group
  should not set `text` (that field is mdSplit provenance, not a body).
- `text` accepts any store path, so **external dependency docs** need no
  vendoring: `{ text = inputs.some-dep + "/docs/api.md"; }` renders the upstream
  page at your flake's pinned revision.

### README as the landing page

```nix
prelude.docs.rootReadme = ./README.md;
```

When a leaf's `text` equals `rootReadme` (exact path match, not basename), the
viewer styles it as the project hero: FIGlet wordmark of `prelude.project` plus
the HTML intro, with the body kept as authored. To also give the README's H2
sections their own sidebar entries:

```nix
prelude.docs.pages = [
  (inputs.prelude.lib.mdSplit ./README.md)
  { text = ./docs/getting-started.md; }
];
```

`prelude.lib.mdSplit` (the flake's `lib` output) splits one Markdown file at
fence-aware H2 boundaries into `{ title; text; children; }` — preamble first,
one leaf per H2. The preamble leaf is renamed to the project name and gets the
README hero when its provenance matches `rootReadme`. It accepts a path, a
path string, or raw Markdown.

## Generated option docs

Only when the project defines its own module options. Never hand-maintain an
option table — generate it from the evaluated option tree:

```nix
prelude.docs.nixosOptions = {
  inherit (eval) options;   # lib.evalModules side-eval, not the live flake-parts
  transformOptions = o: o // { declarations = []; };  # any nixosOptionsDoc arg
};
prelude.docs.pages = [ /* … */ { generate = "nixosOptions"; title = "Options"; } ];
```

- Side-evaluate options with `lib.evalModules { modules = [ … ]; }` — closing
  over the live flake-parts option tree risks cycles and noise.
- `split = "allLeaves"` (default): nested sidebar, one leaf per terminal
  option. `split = "shallow"`: one full `pkgs.nixosOptionsDoc` page.
- Never JSON-serialize the `nixosOptions` value; it feeds nixosOptionsDoc
  directly and only Markdown store paths enter the bundle.

**Authored vs generated:** authored leaves/groups are prose the repo maintains;
`generate` nodes derive from option definitions at build time and are never
edited by hand. Upstream's checked-in `docs/reference/options.md` is a
maintainer artifact. Do not assume downstream has `x sync-docs`; follow its
own generation workflow when one exists.

## Verify

Make newly referenced files visible to Git-backed flake evaluation by staging
only the intended files; no commit is required. Preserve existing docs pages
when merging the examples above.

From the repo root, without entering the devshell:
```sh
nix build .#prelude-docs   # evaluates the pages tree and builds the bundle
./result/bin/docs 1        # prints leaf 1 non-interactively
```

Inside the devshell (`nix develop`):

- `docs` or `x docs` — TUI: digits 1–9 jump top-level pages, Tab/Shift-Tab
  moves focus, j/k scroll, q quits.
- `docs <page>` prints one window; page is a 1-based depth-first leaf index
  (groups are not pages). `docs next` / `docs prev` page through. Piped output
  strips ANSI, so this works in scripts and CI logs.

Reference (pin to your flake.lock's `github:darkmatter/prelude` revision):
https://github.com/darkmatter/prelude — `docs/your-own-repo.md` (consumer
wiring), `docs/configuration.md`, and `docs/reference/options.md` under
`prelude.docs.*`. For catalogue command edits see the `prelude-just` skill;
`x --list` shows the installed surface.
