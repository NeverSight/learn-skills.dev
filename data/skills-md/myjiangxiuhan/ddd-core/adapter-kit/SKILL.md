---
name: adapter-kit
description: Map an approved domain contract to replaceable backend, database, transport, or UI conventions.
---

# adapter-kit

This skill is available only after ddd-core's design-confirmation point and the separate approval to implement one named slice. Never read or invoke adapter-kit for ordinary requirements, while the design is a draft, or before the implementation approval. Do not auto-chain skills or infer either approval.

1. Read the project stack configuration (for example `.ddd/project.yaml`) and one selected, versioned profile only after the gate; infer existing settings before asking.
2. Keep domain meaning independent of framework, database, transport, and UI; display wording stays at the presentation edge.
3. Reuse existing repository patterns, record unknown conventions as pending, and allow an explicit per-task profile override without changing defaults.
4. Match a profile exactly on `framework`, `component_library`, `variant`, and `target`. Bare React + Ant Design selects `react-antd`; never upgrade it to `react-antd-pro`; admin must explicitly select `react-antd-pro`.
5. Verify adapters with focused contract tests and one observable path for the approved slice.
6. Report unsupported capabilities; never drop or reinterpret a core rule. Do not add or implement a cloud-drive adapter unless a separate, explicit slice approval authorizes it.

Do not add a generic abstraction without a second concrete consumer or pre-generate unused adapters. Stop if the approval or profile is missing instead of routing to another skill.

