---
name: folder-structure
description: Folder structure practices.
---

# Folder structure

## Organization

- Organize by capability first; keep technical subdivisions inside their owning capability.
- Name folders by responsibility; avoid catch-all `utils`, `helpers`, `common`, and `misc` directories.
- Use the same internal organization for modules with equivalent responsibilities.
- Create directories for existing responsibilities, not anticipated architecture.

## Ownership

- Keep capability-specific code with its owner, even when other capabilities consume it.
- Place contracts with the module that owns their meaning.
- Share code only when multiple existing capabilities require the same behavior and contract.
- Keep shared modules independent of the capabilities that consume them.

## Dependencies

- Expose explicit module entry points; prohibit imports into another module's internals.
- Keep module dependencies acyclic; do not move code into shared folders merely to break cycles.
- Keep domain rules independent of frameworks, storage, and transport.
- Select and wire concrete integrations at application composition points.
