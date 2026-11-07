---
name: setup-pstack
description: Configure potetos-for-everyone model roles and capability preferences for the current agent/runtime. Use during initial setup or routing changes.
---
# Setup pstack, portable

1. Detect host capabilities and available model/delegation options. Do not assume model names.
2. Explain the optional roles: fast mechanical worker, strongest judgment worker, prose/document worker, and review panel.
3. If the host has native delegation, record only routing preferences. If it lacks delegation but agent CLIs are available, configure portable runner profiles using `runtime/config.example.json`; keep secrets in environment variables, not the config file.
4. Write only explicit overrides to `.potetos/config.json`. Missing roles/runners mean inherit the host/parent behavior.
5. Validate the config as JSON and make sure canonical skills remain model-agnostic.
6. Run the installer doctor and a dry invocation of `poteto-mode` discovery. If external runners were configured, run a harmless one-line delegate smoke test.
