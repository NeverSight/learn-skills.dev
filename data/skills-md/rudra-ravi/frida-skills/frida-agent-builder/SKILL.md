---
name: frida-agent-builder
description: Build maintainable Frida agent projects with TypeScript, frida-compile, RPC exports, helpers, logging, version checks, and multi-hook organization.
---

# Frida Agent Builder

Use this skill for reusable Frida agents and multi-script projects.

## Project Shape

Prefer a small TypeScript agent when scripts will grow beyond a single hook:

```text
agent/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── log.ts
│   └── hooks/
└── dist/
```

For Frida 17 and Java APIs in bundled agents, include `frida-java-bridge` when required by the build/runtime style.

## Build Rules

- Keep one hook family per file.
- Export an `init()` function per hook family and call it from `src/index.ts`.
- Use structured logging with tags and JSON for complex values.
- Add `rpc.exports` only for host-controlled actions or test probes.
- Avoid global broad hooks unless the task explicitly requires discovery.
- Keep generated artifacts out of source control unless the repository convention includes them.

## Scaffold Script

Use `scripts/scaffold-frida-agent.py` to create a minimal TypeScript Frida agent:

```bash
python3 /path/to/frida-agent-builder/scripts/scaffold-frida-agent.py ./agent --java
```

Then install and build:

```bash
npm install
npm run build
```

## References

Read `references/agent-patterns.md` for project conventions, RPC patterns, host command examples, and packaging notes.
