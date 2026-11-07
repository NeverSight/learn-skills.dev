---
name: abap-unit-testing
description: Help with ABAP Unit testing including test class setup, assertions, test doubles, mocking frameworks, dependency injection, CDS test environments, SQL test environments, RAP BO test doubles, and test fixtures. Use when users ask about ABAP unit tests, test classes, test methods, CL_ABAP_UNIT_ASSERT, test doubles, mocking, CDS test environment, SQL test environment, RAP testing, ABAP test injection, test seams, behavior-driven testing, TDD in ABAP, test isolation, or writing automated tests for ABAP code. Triggers include "write a unit test", "create test class", "mock a dependency", "test a CDS view", "test a RAP BO", "test double", "assertion", "test fixture", "test isolation", or "ABAP unit".
---

# ABAP Unit Testing

Guide for writing effective ABAP Unit tests including test class setup, assertions, test doubles, mocking frameworks, and test environments for CDS, SQL, and RAP.

## Workflow

1. **Determine the testing goal**:
   - Testing business logic in a class method
   - Testing a CDS view entity
   - Testing a RAP BO behavior implementation
   - Testing database-dependent logic with SQL test doubles
   - Setting up test doubles for external dependencies

2. **Choose the right approach**:
   - Direct unit test for pure logic (no dependencies)
   - Constructor/setter injection for mockable dependencies
   - CDS test environment for CDS view tests
   - OSQL test environment for SQL-dependent code
   - RAP BO test doubles for RAP behavior tests

3. **Follow the AAA pattern**: Arrange → Act → Assert

4. **Ensure test isolation**: Tests must not depend on persistent data or external systems

## Test Class Fundamentals

### Test Class Definition

```abap
"! Test class for ZCL_MY_CLASS
CLASS ltc_my_class DEFINITION FINAL FOR TESTING
  DURATION SHORT
  RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    DATA cut TYPE REF TO zcl_my_class.  "Class Under Test

    CLASS-METHODS class_setup.    "Once before all tests
    CLASS-METHODS class_teardown. "Once after all tests
    METHODS setup.               "Before each test
    METHODS teardown.            "After each test

    METHODS test_calculate_total FOR TESTING.
    METHODS test_validate_input  FOR TESTING.
    METHODS test_empty_input     FOR TESTING RAISING cx_static_check.
ENDCLASS.

CLASS ltc_my_class IMPLEMENTATION.

  METHOD class_setup.
    " One-time setup for all tests in this class
  ENDMETHOD.

  METHOD class_teardown.
    " One-time cleanup
  ENDMETHOD.

  METHOD setup.
    " Create fresh instance before each test
    cut = NEW #( ).
  ENDMETHOD.

  METHOD teardown.
    " Cleanup after each test
  ENDMETHOD.

  METHOD test_calculate_total.
    " Arrange
    DATA(lv_quantity) = 5.
    DATA(lv_price) = CONV decfloat34( '10.50' ).

    " Act
    DATA(lv_result) = cut->calculate_total(
      iv_quantity = lv_quantity
      iv_price    = lv_price ).

    " Assert
    cl_abap_unit_assert=>assert_equals(
      act = lv_result
      exp = CONV decfloat34( '52.50' )
      msg = 'Total should be quantity * price' ).
  ENDMETHOD.

  METHOD test_validate_input.
    cl_abap_unit_assert=>assert_true(
      act = cut->validate_input( 'VALID_INPUT' )
      msg = 'Valid input should return true' ).
  ENDMETHOD.

  METHOD test_empty_input.
    TRY.
        cut->validate_input( '' ).
        cl_abap_unit_assert=>fail( msg = 'Should have raised exception' ).
      CATCH zcx_validation_error INTO DATA(lx_error).
        cl_abap_unit_assert=>assert_bound(
          act = lx_error
          msg = 'Exception should be raised for empty input' ).
    ENDTRY.
  ENDMETHOD.

ENDCLASS.
```

### Test Class Attributes

| Attribute    | Options                               | Purpose                                                |
| ------------ | ------------------------------------- | ------------------------------------------------------ |
| `DURATION`   | `SHORT` / `MEDIUM` / `LONG`           | Expected execution time; `SHORT` < 1s (default for CI) |
| `RISK LEVEL` | `HARMLESS` / `DANGEROUS` / `CRITICAL` | Impact on system data; `HARMLESS` = no DB changes      |

### Test Method Additions

| Addition                  | Purpose                                                            |
| ------------------------- | ------------------------------------------------------------------ |
| `FOR TESTING`             | Marks method as a test method                                      |
| `RAISING cx_static_check` | Allows exceptions to propagate (test fails on unhandled exception) |

## CL_ABAP_UNIT_ASSERT — Assertion Methods

| Method                      | Purpose                     | Example                                                      |
| --------------------------- | --------------------------- | ------------------------------------------------------------ |
| `assert_equals`             | Value equality              | `assert_equals( act = result exp = 42 )`                     |
| `assert_true`               | Boolean true                | `assert_true( act = lv_flag )`                               |
| `assert_false`              | Boolean false               | `assert_false( act = lv_flag )`                              |
| `assert_initial`            | Value is initial            | `assert_initial( act = lt_table )`                           |
| `assert_not_initial`        | Value is not initial        | `assert_not_initial( act = lt_result )`                      |
| `assert_bound`              | Reference is bound          | `assert_bound( act = lo_instance )`                          |
| `assert_not_bound`          | Reference is not bound      | `assert_not_bound( act = lo_ref )`                           |
| `assert_differs`            | Values are different        | `assert_differs( act = val1 exp = val2 )`                    |
| `assert_char_cp`            | Character pattern match     | `assert_char_cp( act = lv_text exp = '*error*' )`            |
| `assert_char_np`            | Character pattern no match  | `assert_char_np( act = lv_text exp = '*secret*' )`           |
| `assert_number_between`     | Number in range             | `assert_number_between( number = val lower = 1 upper = 10 )` |
| `assert_table_contains`     | Table contains line         | `assert_table_contains( line = wa table = lt_result )`       |
| `assert_table_not_contains` | Table does not contain line | `assert_table_not_contains( line = wa table = lt_result )`   |
| `assert_return_code`        | sy-subrc check              | `assert_return_code( act = sy-subrc exp = 0 )`               |
| `fail`                      | Force test failure          | `fail( msg = 'Should not reach here' )`                      |

### Common Assertion Patterns

```abap
" Check table has expected number of entries
cl_abap_unit_assert=>assert_equals(
  act = lines( lt_result )
  exp = 3
  msg = 'Expected 3 result entries' ).

" Check exception message
TRY.
    cut->some_method( ).
    cl_abap_unit_assert=>fail( msg = 'Expected exception' ).
  CATCH zcx_my_exception INTO DATA(lx).
    cl_abap_unit_assert=>assert_equals(
      act = lx->get_text( )
      exp = 'Expected error message' ).
ENDTRY.

" Check that table contains a specific key
cl_abap_unit_assert=>assert_table_contains(
  line  = VALUE zstructure( key_field = 'ABC' )
  table = lt_result
  msg   = 'Result should contain entry ABC' ).
```

## Dependency Injection & Test Doubles

### Constructor Injection Pattern

```abap
" Production interface
INTERFACE zif_data_provider.
  METHODS get_data
    RETURNING VALUE(rt_data) TYPE ztab_data.
ENDINTERFACE.

" Production class with injectable dependency
CLASS zcl_processor DEFINITION.
  PUBLIC SECTION.
    METHODS constructor
      IMPORTING io_provider TYPE REF TO zif_data_provider OPTIONAL.
    METHODS process
      RETURNING VALUE(rv_result) TYPE string.
  PRIVATE SECTION.
    DATA mo_provider TYPE REF TO zif_data_provider.
ENDCLASS.

CLASS zcl_processor IMPLEMENTATION.
  METHOD constructor.
    mo_provider = COND #(
      WHEN io_provider IS BOUND THEN io_provider
      ELSE NEW zcl_default_provider( ) ).
  ENDMETHOD.

  METHOD process.
    DATA(lt_data) = mo_provider->get_data( ).
    " Process data...
  ENDMETHOD.
ENDCLASS.
```

### Test Double (Manual Mock)

```abap
" Test double implementing the interface
CLASS ltd_data_provider DEFINITION FOR TESTING.
  PUBLIC SECTION.
    INTERFACES zif_data_provider.
    DATA mt_test_data TYPE ztab_data.
ENDCLASS.

CLASS ltd_data_provider IMPLEMENTATION.
  METHOD zif_data_provider~get_data.
    rt_data = mt_test_data.
  ENDMETHOD.
ENDCLASS.

" Test class using the double
CLASS ltc_processor DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.
  PRIVATE SECTION.
    DATA cut        TYPE REF TO zcl_processor.
    DATA mo_provider TYPE REF TO ltd_data_provider.

    METHODS setup.
    METHODS test_process_with_data FOR TESTING.
ENDCLASS.

CLASS ltc_processor IMPLEMENTATION.
  METHOD setup.
    mo_provider = NEW #( ).
    cut = NEW #( io_provider = mo_provider ).
  ENDMETHOD.

  METHOD test_process_with_data.
    " Arrange — configure test double
    mo_provider->mt_test_data = VALUE #(
      ( key = '1' value = 'A' )
      ( key = '2' value = 'B' ) ).

    " Act
    DATA(lv_result) = cut->process( ).

    " Assert
    cl_abap_unit_assert=>assert_not_initial( act = lv_result ).
  ENDMETHOD.
ENDCLASS.
```

## CDS Test Environment

Use `cl_cds_test_environment=>create( i_for_entity = 'ZI_ENTITY' )` to stub all data sources of a CDS view. Insert test data with `insert_test_data( )`, clear with `clear_doubles( )` in `setup`, and call `destroy( )` in `class_teardown`.

## OSQL (Open SQL) Test Environment

Use `cl_osql_test_environment=>create( i_dependency_list = ... )` to stub specific DB tables/views for testing SQL-dependent classes. Same lifecycle pattern as CDS test environment.

## RAP BO Test Doubles

- **Transactional buffer double** (`cl_botd_txbufdbl_bo_test_env`): For testing code that consumes a RAP BO via EML
- **Mock EML API** (`cl_botd_mockemlapi_bo_test_env`): For testing RAP handler method implementations by configuring mock responses

## Test Seams (Legacy Code)

Use `TEST-SEAM` / `END-TEST-SEAM` in production code and `TEST-INJECTION` / `END-TEST-INJECTION` in tests. Prefer constructor injection for new code.

> For full code examples of all the above, read [references/test-environment-examples.md](references/test-environment-examples.md).

## Best Practices

### Test Design

- **One assertion concept per test** — each test should verify one behavior
- **Descriptive test method names** — `test_reject_negative_quantity` not `test_1`
- **Independent tests** — no test should depend on another test's outcome or execution order
- **Fast tests** — use `DURATION SHORT` and avoid unnecessary setup

### Test Isolation

- Always use test doubles for external dependencies (DB, APIs, other BOs)
- Use `setup` / `teardown` to ensure clean state
- Use `class_setup` / `class_teardown` for expensive one-time setup (test environments)
- Always call `clear_doubles( )` in `setup` for test environment classes
- Always call `destroy( )` in `class_teardown`

### Test Structure

- Place test classes in local test include (test classes tab in ADT)
- Prefix test doubles with `ltd_` (local test double)
- Prefix test classes with `ltc_` (local test class)
- Group related tests in the same test class

### What to Test

- Business logic and calculations
- Validation rules and error cases
- Edge cases (empty input, boundary values, null references)
- CDS view calculations and aggregations
- RAP handler logic (actions, validations, determinations)

### What Not to Test

- Framework-provided functionality (managed CRUD in RAP)
- Simple getter/setter methods
- ABAP runtime behavior

## References

- [SAP ABAP Cheat Sheets — ABAP Unit Tests](https://github.com/SAP-samples/abap-cheat-sheets/blob/main/14_ABAP_Unit_Tests.md)
- [SAP Help — ABAP Unit](https://help.sap.com/doc/abapdocu_cp_index_htm/CLOUD/en-US/index.htm?file=abenunit_test.htm)
- [SAP Help — CDS Test Double Framework](https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/cds-test-double-framework)
- [SAP Help — RAP BO Test Doubles](https://help.sap.com/docs/abap-cloud/abap-rap/test)
- [Clean ABAP — Testing](https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#testing)

## Related Skills

- **cds-view-entities**: Use for testing CDS view entities with CDS test environments
- **rap**: Use for testing RAP business objects with RAP test doubles
- **clean-abap**: Use for ensuring test code follows Clean ABAP principles
