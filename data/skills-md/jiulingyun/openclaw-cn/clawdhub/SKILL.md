---
name: ClawdHub
description: 使用ClawdHub命令行工具从clawdhub.com搜索、安装、更新和发布代理技能。当你需要即时获取新技能、将已安装的技能同步到最新版本或特定版本，或使用npm安装的clawdhub CLI发布新/更新的技能文件夹时使用。
metadata: {"clawdbot":{"requires":{"bins":["clawdhub"]},"install":[{"id":"node","kind":"node","package":"clawdhub","bins":["clawdhub"],"label":"Install ClawdHub CLI (npm)"}]}}
---

# ClawdHub CLI

Install
```bash
npm i -g clawdhub
```

Auth (publish)
```bash
clawdhub login
clawdhub whoami
```

Search
```bash
clawdhub search "postgres backups"
```

Install
```bash
clawdhub install my-skill
clawdhub install my-skill --version 1.2.3
```

Update (hash-based match + upgrade)
```bash
clawdhub update my-skill
clawdhub update my-skill --version 1.2.3
clawdhub update --all
clawdhub update my-skill --force
clawdhub update --all --no-input --force
```

List
```bash
clawdhub list
```

Publish
```bash
clawdhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

Notes
- Default registry: https://clawdhub.com (override with CLAWDHUB_REGISTRY or --registry)
- Default workdir: cwd (falls back to Clawdbot workspace); install dir: ./skills (override with --workdir / --dir / CLAWDHUB_WORKDIR)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
