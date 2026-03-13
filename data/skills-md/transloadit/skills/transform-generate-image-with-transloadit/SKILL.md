---
name: transform-generate-image-with-transloadit
description: One-off image generation (prompt -> image file) using Transloadit via the `transloadit` CLI. Prefer builtin templates (`builtin/generate-image@latest`) and download outputs locally via `-o`.
---

# Run (No Input File)

Do not use `--watch` for inputless templates.

```bash
npx -y @transloadit/node assemblies create \
  --template builtin/generate-image@latest \
  -f prompt='A minimal product photo of a chameleon on white background' \
  -o ./out/ \
  -j
```

Footnote (discover more builtin templates):
```bash
npx -y @transloadit/node templates list --include-builtin exclusively-latest --fields id,name --json
```

# Debug If It Fails

```bash
npx -y @transloadit/node assemblies get <assemblyIdOrUrl> -j
```

Notes:
- Some generator/AI robots can be account-gated; if the assembly fails with capability/availability errors, switch templates or confirm the feature is enabled for your account.
