---
name: transform-encode-hls-video-with-transloadit
description: One-off HLS encoding (local video -> HLS renditions + playlist) using Transloadit via the `transloadit` CLI. Prefer builtin templates (`builtin/encode-hls-video@latest`) and download outputs locally via `-o`.
---

# Run (Local Input Video)

```bash
npx -y @transloadit/node assemblies create \
  --template builtin/encode-hls-video@latest \
  -i ./input.mp4 \
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
