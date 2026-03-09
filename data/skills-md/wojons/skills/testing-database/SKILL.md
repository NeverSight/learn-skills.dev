---
name: testing-database
description: Test database interactions, schemas, and data integrity
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Database Testing

Test database interactions, schemas, data integrity, and performance, coordinating with integration and data layer testing.

## When to use me

Use this skill when:
- Developing applications with database dependencies
- Testing data persistence and retrieval
- Validating database schema migrations
- Ensuring data integrity and consistency
- Testing database performance and optimization
- Verifying transaction handling and rollbacks
- Testing backup and recovery procedures

## What I do

- **Schema and migration testing**:
  - Test database schema changes
  - Validate migration scripts
  - Check backward compatibility
  - Test rollback procedures

- **Data integrity testing**:
  - Verify CRUD operations work correctly
  - Test transaction atomicity (ACID properties)
  - Check referential integrity and constraints
  - Validate data types and conversions

- **Performance testing**:
  - Query optimization and indexing
  - Connection pooling and resource management
  - Load testing with concurrent database access
  - Long-running transaction testing

- **Integration coordination**:
  - Coordinate with integration testing for data layer
  - Support unit testing with test database setup
  - Enable end-to-end testing with realistic data
  - Complement API testing with database validation

## Examples

```bash
# Database schema testing
npm run test:database:schema       # Schema validation
npm run test:database:migrations   # Migration testing
npm run test:database:rollback     # Rollback procedure testing

# Data integrity testing
npm run test:database:crud         # CRUD operation testing
npm run test:database:transactions # Transaction testing
npm run test:database:constraints  # Constraint validation

# Performance testing
npm run test:database:performance  # Query performance
npm run test:database:load         # Concurrent load testing
npm run test:database:indexing     # Index optimization testing

# Integration with other tests
npm run test:integration -- --database # Integration tests with database
npm run test:e2e -- --data-persistence # E2E with data validation

# Test database setup
npm run test:database:setup        # Create test databases
npm run test:database:teardown     # Clean up test data
npm run test:database:fixtures     # Load test fixtures
```

## Output format

```
Database Test Results:
──────────────────────────────
Database System: PostgreSQL 15
Test Environment: Isolated test database

Schema Testing:
  ✅ Current schema matches ORM definitions
  ✅ Migration scripts apply correctly
  ✅ Rollback scripts revert successfully
  ✅ Indexes created as expected

Data Integrity:
  ✅ CRUD operations: 100% success
  ✅ Transactions: ACID properties verified
  ✅ Constraints: Foreign keys, unique, check constraints enforced
  ✅ Data types: Proper type handling and conversion

Performance Testing:
  ✅ Query Optimization: 45/50 queries optimized
    ⚠️ 5 complex queries need indexing review
  ✅ Connection Pooling: 100 concurrent connections handled
  ✅ Load Testing: 1000 transactions/minute sustained
  ✅ Response Times: 95% < 100ms

Integration with Other Tests:
  - Unit tests: Use in-memory database or mocks
  - Integration tests: Use test database with transactions
  - API tests: Validate database interactions through API
  - E2E tests: Full data flow from UI to database
  - Performance tests: Include database performance metrics

Security Testing Integration:
  ✅ SQL injection prevention verified
  ✅ Access controls enforced at database level
  ✅ Sensitive data encryption tested
  ✅ Audit logging of database operations

Data Migration Testing:
  ✅ Migration from v1 to v2 successful
  ✅ Data loss: 0 records
  ✅ Downtime: 15 minutes (within SLA)
  ✅ Rollback tested and verified

Recommendation:
  - Review 5 complex queries for indexing opportunities
  - Implement connection health checks
  - Add more comprehensive backup/restore testing
  - Monitor database performance in production
```

## Notes

- Use test databases separate from development/production
- Implement database transaction wrapping for test isolation
- Consider using database containers for consistent testing
- Test with realistic data volumes, not just small samples
- Include database performance in application performance testing
- Test backup and restore procedures regularly
- Consider database-specific features (triggers, stored procedures)
- Coordinate with DevOps for database infrastructure testing
- Document database testing strategy and coverage
