---
name: backend-development
description: Guide for Backend API design, database architecture, and Rust service patterns in Tauri. Use when creating new Commands, Services, or DB Schemas.
---

# Backend Development Skill

Rules for the Rust "Engine" of EMMM2.

## 1. Core Architecture (The 3-Layer Standard)

Follow **Clean Architecture** to keep logic testable and decoupled.

1.  **Presentation (Commands)**: `src-tauri/src/commands/`. Thin wrapper. Deserializes input -> Calls Service -> Serializes Output. **NO LOGIC HERE.**
2.  **Domain (Services)**: `src-tauri/src/services/`. Pure Business Logic. Agnostic of Tauri or UI.
3.  **Infrastructure (Repositories)**: `src-tauri/src/database/`. SQLx queries and OS File I/O.

## 2. API Design (Tauri Commands)

Treat Commands like REST Endpoints.

- **Input**: Use DTO structs (Data Transfer Objects), not long argument lists.
- **Output**: Always return `Result<T, AppError>`.
- **Async**: All Commands must be `async`.

## 3. Database Patterns (SQLite + SQLx)

- **Schema**: managed via `migrations/*.sql`.
- **ID**: Use UUID v4 (Text) for universal uniqueness.
- **Optimization**: Use WAL mode and `PRAGMA synchronous = NORMAL`.

## References

- [Service Pattern](references/service_pattern.md)
- [Database & Schema](references/db_patterns.md)
- [API Style Guide](references/api_design.md)
