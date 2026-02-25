---
name: maui-data-storage
description: Provides best practices and patterns for data storage in .NET MAUI apps, including SQLite, EF Core, Preferences, SecureStorage, and file system access.
---

# .NET MAUI — Data Storage Skill

## Purpose

This skill provides agents with best practices and patterns for storing, retrieving, and managing data in .NET MAUI applications. It covers SQLite, EF Core, Preferences, SecureStorage, and cross-platform file system access.

The goal is to ensure that all data-related code is secure, maintainable, and aligned with modern MAUI architecture.

## Core Principles

1. **Use the right storage for the right data**
   - Sensitive data → SecureStorage
   - User settings → Preferences
   - Structured relational data → SQLite/EF Core
   - Files and exports → FileSystem.AppDataDirectory
2. **Cross-platform consistency**
   Always use MAUI abstractions for file paths and storage.
3. **Abstraction**
   Wrap storage logic in services and interfaces.
4. **Performance**
   Use a single SQLite connection per app lifecycle.
5. **Safety**
   Never store secrets or tokens in Preferences.

## Supported Storage Mechanisms

- SQLite (raw or EF Core)
- Preferences
- SecureStorage
- File system access
- JSON-based local storage

## Recommended Folder Structure

```text
├─ Services
│  └─ Data
│     ├─ Interfaces
│     └─ Models
└─ Database
```

/Services/Data /Services/Data/Interfaces /Services/Data/Models /Database

## Agent Usage Guidelines

- When generating data models, place them in `/Services/Data/Models`.
- When generating database access, create:
  - `IDatabaseService`
  - `DatabaseService`
  - `AppDbContext` (if using EF Core)
- When asked to “store user settings,” use Preferences.
- When asked to “store sensitive data,” use SecureStorage.
- When asked to “save a file,” use `FileSystem.AppDataDirectory`.

## Out of Scope

- Authentication token storage (covered in `maui-authentication`)
- UI logic
- Cloud sync or remote databases
