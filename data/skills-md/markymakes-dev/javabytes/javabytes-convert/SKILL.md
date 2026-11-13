---
name: javabytes-convert
description: Convert or translate JavaScript, TypeScript or a web app to Java using JavaBytes' honest-subset pipeline. Use when the user asks to convert, translate, or port JS/TS code to Java, or pastes a GitHub repo URL expecting a Java version.
---

# Converting JavaScript to Java with JavaBytes

The translation tools emit a bounded, typed, compilable subset — never a
finished port. Your job is to run the pipeline in order and to keep the
manual-work inventory honest.

## Get the code where the tools can read it

The tools take local paths inside the sandbox (the roots the client
advertised, or `JAVABYTES_ALLOWED_DIRS`). A pasted GitHub URL is not yet code:

1. Shallow-clone it into the workspace: `git clone --depth 1 <url>` into the
   working directory or a subdirectory the user agrees to.
2. Name the cloned path in every later step.
3. If the repo cannot be cloned (private, or the sandbox forbids writes), ask
   for a zip or the relevant files. Never promise conversion of code you
   cannot read.

## Scope before tools

- Single file or a small set: `analyze_javascript`, then
  `translate_javascript` per unit.
- Multi-file web app (`package.json`, framework directories):
  `translate_webapp`, and say upfront that the output is Java sources plus a
  manual-work inventory — not a running application.
- If the user expects "paste a URL, get a working Java app", reset that
  expectation before running anything. Frameworks without a Java counterpart
  come out as manual work, not as magic.

## Pipeline

1. `analyze_javascript` on the target path. Read every finding: what analysis
   flags as unverifiable or dynamic **is** the manual-work list. Do not
   re-derive it after translating.
2. `translate_javascript` or `translate_webapp` on the units analysis deemed
   expressible.
3. Compile-check the emitted sources with `javac` when a JDK is available. If
   no JDK is on the machine, state that compilation is unverified — do not
   imply it compiled.

## Report format

Every conversion ends with three lists:

- **Converted** — files and classes emitted, and where they were written.
- **Manual work** — each skipped or approximated construct, with the reason
  analysis gave.
- **Unverified** — anything that was not compile-checked.

Never silently drop a construct, and never present plausible-but-non-compiling
code as done.

## Refusals

- Do not run `translate_*` before `analyze_javascript` on the same target.
- Do not convert what analysis cannot type. When the code leans on dynamic
  behaviour — `eval`, prototype mutation, heavy metaprogramming — name
  coexistence options (GraalJS, Rhino, JSweet, GWT) instead of forcing a
  rewrite.
- Do not call the migration complete while manual items remain.

Done when analysis ran on the target, every emitted file either compiles or is
listed as unverified, and the manual-work inventory covers every skipped
construct.

See also `javabytes-tool-routing` for the rest of the catalog, and
`javabytes-setup` if the server is not connected.
