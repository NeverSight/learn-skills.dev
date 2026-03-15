---
name: tanstack-db
description: This skill should be used when users need to work with TanStack DB for building reactive data layers in applications. It provides comprehensive guidance on collections, live queries, mutations, schema validation, error handling, and various integrations including LocalStorage and ElectricSQL.
---

# TanStack DB

TanStack DB is a reactive client store for APIs that provides normalized collections, sub-millisecond live queries, and instant optimistic writes. It solves endpoint sprawl and network waterfalls through type-safe data management with automatic updates when underlying data changes.

## Core Functionality

TanStack DB enables building reactive data layers through:
- **Normalized Collections**: Centralized data management with schema validation and type safety
- **Live Queries**: SQL-like queries that automatically update when data changes
- **Optimistic Mutations**: Instant UI updates with automatic rollback on errors
- **Storage Integrations**: Built-in support for LocalStorage, ElectricSQL, and custom backends

## When to Use

Use this skill when working with TanStack DB for building reactive data layers in applications. It provides comprehensive guidance on collections, live queries, mutations, schema validation, error handling, and various integrations including LocalStorage and ElectricSQL.

## Module Overview

### Core Concepts Module
- **Functionality**: TanStack DB provides a reactive client store for APIs with normalized collections, live queries, and optimistic mutations
- **Key APIs**: `createCollection`, `useLiveQuery`, `useLiveSuspenseQuery`, `queryCollectionOptions`, `electricCollectionOptions`, `localStorageCollectionOptions`
- **Detailed Documentation**: `references/TanStack DB Overview.md`

### Live Queries Module
- **Functionality**: Build type-safe, SQL-like queries with automatic updates when underlying data changes
- **Key APIs**: `liveQueryCollectionOptions`, `from`, `where`, `select`, `join`, `groupBy`, `findOne`, `orderBy`, `limit`
- **Detailed Documentation**: `references/TanStack DB Live Queries.md`

### Mutations Module
- **Functionality**: Implement optimistic updates with automatic state management and error recovery
- **Key APIs**: `collection.insert`, `collection.update`, `collection.delete`, `createOptimisticAction`, `createTransaction`
- **Detailed Documentation**: `references/TanStack DB Mutations.md`

### Schema Validation Module
- **Functionality**: Validate data and implement type-safe transformations using TInput/TOutput type system
- **Key APIs**: Schema validation with Zod, `z.transform()`, `z.default()`, `SchemaValidationError`
- **Detailed Documentation**: `references/Schema Validation and Type Transformations.md`

### Error Handling Module
- **Functionality**: Handle errors through named error classes, collection status tracking, and transaction recovery patterns
- **Key APIs**: `SchemaValidationError`, `CollectionInErrorStateError`, `TransactionError`, `createTransaction`
- **Detailed Documentation**: `references/Error Handling.md`

### LocalStorage Integration Module
- **Functionality**: Persist data to localStorage/sessionStorage with cross-tab synchronization and direct local mutations
- **Key APIs**: `localStorageCollectionOptions`, `collection.insert()`, `collection.update()`, `collection.delete()`
- **Detailed Documentation**: `references/LocalStorage Collection.md`

### ElectricSQL Integration Module
- **Functionality**: Real-time data synchronization with Postgres databases using transaction-based optimistic updates
- **Key APIs**: `electricCollectionOptions`, `onInsert`, `onUpdate`, `onDelete`, `awaitTxId`, `awaitMatch`
- **Detailed Documentation**: `references/Electric Collection.md`

### Custom Collection Module
- **Functionality**: Create custom collection options creators for integrating different sync engines and data sources
- **Key APIs**: `CollectionConfig`, `SyncConfig`, `begin`, `write`, `commit`, mutation handlers
- **Detailed Documentation**: `references/Creating a Collection Options Creator.md`

## Workflow

### Creating Collections
1. Define a schema using Zod or other supported validation libraries
2. Create a collection using `createCollection` with appropriate options (query, electric, localStorage, or custom)
3. Configure sync modes (eager, on-demand, or progressive) based on data access patterns
4. For detailed schema patterns and validation, see `references/Schema Validation and Type Transformations.md`

### Building Live Queries
1. Use `useLiveQuery` or `useLiveSuspenseQuery` to create reactive queries
2. Chain query builder methods: `from()`, `where()`, `select()`, `join()`, `groupBy()`, `orderBy()`
3. Leverage type inference for compile-time type safety
4. For comprehensive query syntax and examples, see `references/TanStack DB Live Queries.md`

### Implementing Mutations
1. Use collection methods: `collection.insert()`, `collection.update()`, `collection.delete()` for simple operations
2. Use `createOptimisticAction` for intent-based mutations with automatic rollback
3. Use `createTransaction` for manual control over mutation batching
4. For advanced patterns like paced mutations and merging, see `references/TanStack DB Mutations.md`

### Integrating Storage Backends
1. **LocalStorage**: Use `localStorageCollectionOptions` for browser-based persistence with cross-tab sync
2. **ElectricSQL**: Use `electricCollectionOptions` for real-time Postgres synchronization
3. **Custom**: Create custom collection options for specific sync engines (WebSocket, RxDB, TrailBase)
4. For integration-specific configuration, see `references/LocalStorage Collection.md` or `references/Electric Collection.md`

### Handling Errors
1. Wrap live queries in React Error Boundaries to handle collection error states
2. Use try/catch blocks with transactions for mutation error handling
3. Check collection status before operations using query collection error tracking
4. For comprehensive error patterns and recovery strategies, see `references/Error Handling.md`

## Resource References

- **Overview and Core Concepts**: `references/TanStack DB Overview.md`
- **Live Query Syntax and Examples**: `references/TanStack DB Live Queries.md`
- **Mutation Patterns and Transactions**: `references/TanStack DB Mutations.md`
- **Schema Validation and Types**: `references/Schema Validation and Type Transformations.md`
- **Error Handling Patterns**: `references/Error Handling.md`
- **LocalStorage Integration**: `references/LocalStorage Collection.md`
- **ElectricSQL Integration**: `references/Electric Collection.md`
- **Custom Collection Creation**: `references/Creating a Collection Options Creator.md`
