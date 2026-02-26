---
name: unit-testing
description: Use when writing or reviewing Java unit tests. Enforces Mockito/JUnit 5 best practices - strict stubbing, no lenient mode, specific matchers, complete flow stubbing, Arrange-Act-Assert structure, and clear test naming.
license: Apache-2.0
metadata:
  author: folio-org
  version: "1.0.0"
---

# Unit Testing Guidelines

## General Principles

### 1. Test Independence
- Each test must be independent and self-contained
- Tests must not rely on execution order
- Use local variables within test methods instead of shared instance variables when possible

### 2. Clear Test Names
Follow the pattern: `methodName_scenario_expectedBehavior`

Examples: `tableExists_positive_tableIsPresent`, `deleteTimer_negative_timerDescriptorIdIsNull`

### 3. Test Organization
Structure every test with: **Arrange** → **Act** → **Assert**

## Mockito Best Practices

### 1. Never Use Lenient Mode
❌ Never add `@MockitoSettings(strictness = Strictness.LENIENT)` — write precise tests instead.

### 2. Avoid Unnecessary Stubbing
Only stub (`when()`) what is actually used in the test. Use helper methods called only by tests that need them:

```java
private void setupContextMocks() {
    when(context.getFolioModuleMetadata()).thenReturn(moduleMetadata);
    when(context.getTenantId()).thenReturn(TENANT_ID);
    when(moduleMetadata.getDBSchemaName(TENANT_ID)).thenReturn(SCHEMA_NAME);
}
```

### 3. Remove Redundant Verify Statements
Only verify interactions that are **not** mocked with `when()`:

```java
verify(connection).close();        // ✅ not mocked
verify(dataSource).getConnection(); // ❌ redundant — already mocked
```

### 4. Prefer Specific Object Stubs Over `any()` Matchers
Use specific objects when you control test data:

```java
when(mapper.convert(input)).thenReturn(output);           // ✅
when(mapper.convert(any(InputType.class))).thenReturn(output); // ❌
```

Use `any()` only when: the service mutates the object unpredictably, multiple different objects may be passed, or when using argument captors.

### 5. Use Simple `when().thenReturn()` for Basic Returns
```java
when(service.process(data)).thenReturn(true);       // ✅
doAnswer(inv -> true).when(service).process(data);  // ❌
```

Use `thenAnswer()` only for computed return values, conditional logic, or side effects.

### 6. Stub the Complete Service Flow
Stub every external call in the code path being tested:

```java
when(repository.findByKey(key)).thenReturn(Optional.empty());
when(repository.save(entity)).thenReturn(entity);
when(repository.findById(id)).thenReturn(Optional.of(entity));
```

### 7. Use verifyNoMoreInteractions Carefully
Only include mocks that should be fully accounted for:

```java
@AfterEach
void tearDown() {
    verifyNoMoreInteractions(dataSource, connection, databaseMetaData, resultSet);
}
```

## Test Structure

### 1. Class Setup
```java
@UnitTest
@ExtendWith(MockitoExtension.class)
class MyServiceTest {

    private static final String CONSTANT_VALUE = "test-value";

    @Mock
    private Dependency1 dependency1;

    @AfterEach
    void tearDown() {
        verifyNoMoreInteractions(dependency1);
    }
}
```

### 2. Individual Test
```java
@Test
void methodName_scenario_expectedBehavior() throws Exception {
    // Arrange
    setupCommonMocks();
    var service = new MyService(dependency1);
    when(dependency1.doSomething()).thenReturn(expectedValue);

    // Act
    var result = service.methodUnderTest();

    // Assert
    assertThat(result).isEqualTo(expectedValue);
    verify(dependency1).close();
}
```

## Verification Patterns

### 1. Successful Operations
```java
@Test
void operation_positive_success() throws Exception {
    setupRequiredMocks();
    when(repository.find()).thenReturn(entity);

    var result = service.operation();

    assertThat(result).isNotNull();
    verify(connection).close();
}
```

### 2. Exception Scenarios
```java
@Test
void operation_negative_throwsException() throws Exception {
    var expectedException = new SQLException("Connection failed");
    when(dataSource.getConnection()).thenThrow(expectedException);

    assertThatThrownBy(() -> service.operation())
        .isInstanceOf(DataRetrievalFailureException.class)
        .hasMessageContaining("Failed to perform operation")
        .hasCause(expectedException);
}
```

## Common Patterns

### 1. Constants for Test Data
Define at class level for reuse across tests:
```java
private static final String MODULE_ID = "mod-foo-1.0.0";
private static final String TENANT_ID = "test-tenant";
```

### 2. Helper Methods
Extract `private static` methods for object creation, assertions, finding objects, and mock setup when the same code appears in 2+ tests.

For advanced patterns (parameterized tests, deep copy stubbing, fluent API, exact matching, explicit lambda types), see [references/patterns.md](references/patterns.md).

For complete test class examples, see [references/examples.md](references/examples.md).

## Checklist

- [ ] No `@MockitoSettings(strictness = Strictness.LENIENT)`
- [ ] No unnecessary stubbing — all `when()` statements are used
- [ ] Only verify methods that are NOT mocked
- [ ] Specific object stubs over `any()` when test data is controlled
- [ ] Simple `when().thenReturn()` for basic returns
- [ ] All repository/service interactions in the code path are stubbed
- [ ] Copy operations stubbed when service creates internal copies
- [ ] Test names follow `methodName_scenario_expectedBehavior`
- [ ] Each test is independent
- [ ] Resources (connections, streams) verified to be closed
- [ ] Exception tests verify type, message, and cause
- [ ] Constants used for reusable test data
- [ ] Helper methods eliminate code duplication
- [ ] Clear Arrange-Act-Assert sections
- [ ] Fluent API used for test data creation
- [ ] Parameterized tests use `Stream<Type>` for single parameters
- [ ] Explicit type declarations for lambdas when var inference fails
- [ ] Exact matching tests include similar non-matching values
- [ ] All error paths from utility methods covered
- [ ] Unused imports removed
