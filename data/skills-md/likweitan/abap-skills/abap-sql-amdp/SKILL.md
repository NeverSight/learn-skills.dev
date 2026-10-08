---
name: abap-sql-amdp
description: Help with modern ABAP SQL features and AMDP (ABAP Managed Database Procedures) including inline declarations, window functions, GROUP BY, HAVING, PRIVILEGED ACCESS, string functions, aggregate expressions, common table expressions (CTE), AMDP classes, AMDP procedures, AMDP table functions, CDS table functions, and AMDP scalar functions. Use when users ask about ABAP SQL, modern SQL, SELECT, window functions, CTE, common table expression, AMDP, SQLScript, AMDP table function, CDS table function, aggregate, GROUP BY, HAVING, UNION, INTERSECT, EXCEPT, PRIVILEGED ACCESS, ABAP SQL expressions, built-in SQL functions, or database procedures. Triggers include "ABAP SQL query", "window function", "CTE", "AMDP", "table function", "GROUP BY", "aggregate", "PRIVILEGED ACCESS", "inline SELECT", or "SQLScript".
---

# ABAP SQL & AMDP

Guide for writing modern ABAP SQL statements and ABAP Managed Database Procedures (AMDP) in ABAP Cloud and Standard ABAP.

> **Clean core context**: `SELECT` from a released CDS view is **Level A**. Direct **read** access to an SAP database table is **Level C** (ATC priority 2); direct **write** access is **Level D** (ATC priority 1). `EXEC SQL` (native SQL) is a **critical statement → Level D**. `SYCM_USAGE_OF_APIS` reports SQL statements on SAP database tables and views. See the `abap-cloud` skill for level details.

## Workflow

1. **Determine the user's goal**:
   - Writing or optimizing ABAP SQL queries
   - Using advanced SQL features (window functions, CTEs, aggregates)
   - Creating AMDP procedures or functions
   - Implementing CDS table functions via AMDP
   - Understanding PRIVILEGED ACCESS for authorization bypass

2. **Identify the context**:
   - ABAP for Cloud Development vs. Standard ABAP (affects available syntax)
   - Performance optimization needs
   - Whether AMDP is justified (prefer ABAP SQL when possible)

3. **Guide implementation** using modern ABAP SQL syntax

## Modern ABAP SQL Quick Reference

### Basic SELECT with Inline Declaration

```abap
"Single record
SELECT SINGLE FROM ztravel
  FIELDS travel_id, description, total_price, currency_code
  WHERE travel_id = @lv_travel_id
  INTO @DATA(ls_travel).

"Multiple records into internal table
SELECT FROM ztravel
  FIELDS travel_id, description, total_price, currency_code
  WHERE status = 'O'
  ORDER BY total_price DESCENDING
  INTO TABLE @DATA(lt_travels)
  UP TO 100 ROWS.
```

### Expressions in SELECT List

```abap
SELECT FROM zflight
  FIELDS carrier_id,
         connection_id,
         flight_date,
         seats_max - seats_occupied AS seats_free,
         CASE WHEN seats_occupied > seats_max * 80 / 100
              THEN 'FULL'
              ELSE 'AVAILABLE'
         END AS availability,
         CAST( price AS DECFLOAT34 ) AS price_dec,
         CONCAT( carrier_id, connection_id ) AS flight_key
  INTO TABLE @DATA(lt_flights).
```

### Aggregate Functions and GROUP BY

```abap
SELECT FROM zflight
  FIELDS carrier_id,
         COUNT(*) AS flight_count,
         SUM( seats_occupied ) AS total_passengers,
         AVG( price ) AS avg_price,
         MIN( flight_date ) AS first_flight,
         MAX( flight_date ) AS last_flight
  GROUP BY carrier_id
  HAVING COUNT(*) > 10
  INTO TABLE @DATA(lt_stats).
```

### Window Functions

```abap
SELECT FROM zflight
  FIELDS carrier_id,
         connection_id,
         flight_date,
         price,
         "Running total
         SUM( price ) OVER( PARTITION BY carrier_id
                            ORDER BY flight_date
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ) AS running_total,
         "Row number within partition
         ROW_NUMBER( ) OVER( PARTITION BY carrier_id
                             ORDER BY flight_date DESCENDING ) AS row_num,
         "Ranking
         RANK( ) OVER( PARTITION BY carrier_id ORDER BY price DESCENDING ) AS price_rank,
         "Lead/Lag
         LAG( price, 1 ) OVER( PARTITION BY carrier_id ORDER BY flight_date ) AS prev_price,
         LEAD( price, 1 ) OVER( PARTITION BY carrier_id ORDER BY flight_date ) AS next_price
  INTO TABLE @DATA(lt_window).
```

### Common Table Expressions (CTE)

```abap
WITH
  +connections AS (
    SELECT FROM zflsch
      FIELDS carrier_id, connection_id, city_from, city_to
      WHERE carrier_id IN @lt_carriers ),
  +flight_counts AS (
    SELECT FROM zflight
      FIELDS carrier_id, connection_id,
             COUNT(*) AS cnt
      GROUP BY carrier_id, connection_id ),
  +result AS (
    SELECT FROM +connections AS c
      INNER JOIN +flight_counts AS f
        ON c~carrier_id = f~carrier_id AND c~connection_id = f~connection_id
      FIELDS c~carrier_id, c~city_from, c~city_to, f~cnt )
  SELECT FROM +result
    FIELDS *
    ORDER BY cnt DESCENDING
    INTO TABLE @DATA(lt_result).
```

### Set Operations (UNION, INTERSECT, EXCEPT)

```abap
"UNION ALL (keeps duplicates) / UNION (removes duplicates)
SELECT FROM ztable1 FIELDS col1, col2
UNION ALL
SELECT FROM ztable2 FIELDS col1, col2
INTO TABLE @DATA(lt_union).

"INTERSECT — rows in both
SELECT FROM ztable1 FIELDS col1
INTERSECT
SELECT FROM ztable2 FIELDS col1
INTO TABLE @DATA(lt_intersect).

"EXCEPT — rows in first but not second
SELECT FROM ztable1 FIELDS col1
EXCEPT
SELECT FROM ztable2 FIELDS col1
INTO TABLE @DATA(lt_except).
```

### PRIVILEGED ACCESS

Bypasses CDS access control (DCL) — use with care:

```abap
"Skips access control defined in CDS DCL
SELECT FROM zi_travel
  FIELDS travel_id, description
  WHERE status = 'O'
  INTO TABLE @DATA(lt_all_travels)
  PRIVILEGED ACCESS.
```

### Built-in SQL Functions

| Category       | Functions                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| **String**     | `CONCAT`, `SUBSTRING`, `LENGTH`, `LEFT`, `RIGHT`, `LTRIM`, `RTRIM`, `UPPER`, `LOWER`, `REPLACE`, `LPAD`, `RPAD` |
| **Numeric**    | `ABS`, `CEIL`, `FLOOR`, `ROUND`, `MOD`, `DIV`, `DIVISION`                                                       |
| **Date/Time**  | `DATS_ADD_DAYS`, `DATS_DAYS_BETWEEN`, `TSTMP_ADD_SECONDS`, `TSTMP_CURRENT_UTCTIMESTAMP`, `DATN_ADD_MONTHS`      |
| **Conversion** | `CAST`, `COALESCE`, `CURRENCY_CONVERSION`, `UNIT_CONVERSION`                                                    |
| **Null**       | `COALESCE`, `CASE WHEN ... IS NULL`                                                                             |
| **Aggregate**  | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`                                                               |

### Subqueries

```abap
"Scalar subquery
SELECT FROM ztravel
  FIELDS travel_id,
         total_price,
         ( SELECT AVG( total_price ) FROM ztravel ) AS avg_price
  INTO TABLE @DATA(lt_with_avg).

"EXISTS subquery
SELECT FROM ztravel AS t
  FIELDS t~travel_id, t~description
  WHERE EXISTS ( SELECT FROM zbooking AS b
                   WHERE b~travel_id = t~travel_id
                     AND b~flight_date > @sy-datum )
  INTO TABLE @DATA(lt_with_bookings).
```

## AMDP (ABAP Managed Database Procedures)

### When to Use AMDP

- Prefer ABAP SQL for most scenarios
- Use AMDP when: complex calculations benefit from SQLScript, CDS table functions are needed, or mass data processing requires database-level optimization

### AMDP Class Structure

```abap
CLASS zcl_my_amdp DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_amdp_marker_hdb.  "Mandatory for AMDP

    TYPES: BEGIN OF ty_result,
             carrier_id TYPE s_carr_id,
             total      TYPE i,
           END OF ty_result,
           tt_result TYPE STANDARD TABLE OF ty_result WITH EMPTY KEY.

    "AMDP procedure
    METHODS get_carrier_stats
      AMDP OPTIONS READ-ONLY CDS SESSION CLIENT DEPENDENT
      EXPORTING VALUE(et_result) TYPE tt_result.

    "AMDP table function for CDS table function
    CLASS-METHODS get_data FOR TABLE FUNCTION zdemo_amdp_tf.
ENDCLASS.
```

### AMDP Procedure Implementation

```abap
METHOD get_carrier_stats
  BY DATABASE PROCEDURE
  FOR HDB
  LANGUAGE SQLSCRIPT
  OPTIONS READ-ONLY
  USING zflight_ve.

  et_result = SELECT carrier_id,
                     COUNT(*) AS total
              FROM zflight_ve
              GROUP BY carrier_id
              ORDER BY total DESC;
ENDMETHOD.
```

### AMDP Table Function for CDS Table Function

CDS table function definition:

```cds
@ClientHandling.type: #CLIENT_DEPENDENT
@ClientHandling.algorithm: #SESSION_VARIABLE
define table function ZDEMO_AMDP_TF
  with parameters @Environment.systemField: #SYSTEM_LANGUAGE p_lang : abap.lang
  returns {
    key carrier_id : s_carr_id;
    carrier_name   : s_carrname;
    flight_count   : abap.int4;
  }
  implemented by method zcl_my_amdp=>get_data;
```

AMDP implementation:

```abap
METHOD get_data
  BY DATABASE FUNCTION
  FOR HDB
  LANGUAGE SQLSCRIPT
  OPTIONS READ-ONLY
  USING zcarrier_ve zflight_ve.

  RETURN SELECT c.carrier_id,
                c.carrier_name,
                COUNT(*) AS flight_count
         FROM zcarrier_ve AS c
         INNER JOIN zflight_ve AS f
           ON c.carrier_id = f.carrier_id
         GROUP BY c.carrier_id, c.carrier_name;
ENDMETHOD.
```

### AMDP Client Safety (ABAP Cloud)

| Addition                       | Use Case                                      |
| ------------------------------ | --------------------------------------------- |
| `CDS SESSION CLIENT DEPENDENT` | Uses client-dependent CDS views (most common) |
| `CLIENT INDEPENDENT`           | Uses only client-independent objects          |
| `AMDP OPTIONS READ-ONLY`       | Mandatory in ABAP for Cloud Development       |

## Output Format

When helping with ABAP SQL or AMDP topics, structure responses as:

```markdown
## ABAP SQL / AMDP Guidance

### Query

[The ABAP SQL statement or AMDP implementation]

### Explanation

[Key features used and why]

### Performance Notes

[Optimization considerations if relevant]
```

## References

- ABAP SQL Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets
- AMDP Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets/blob/main/12_AMDP.md
- ABAP SQL Reference: https://help.sap.com/doc/abapdocu_cp_index_htm/CLOUD/en-US/index.htm?file=abenabap_sql.htm

## Clean Core Level Notes for SQL and AMDP

| Scenario                                            | Level | Notes                                                    |
| --------------------------------------------------- | ----- | -------------------------------------------------------- |
| `SELECT` from a released CDS view (`I_*`)            | **A** | Target state                                             |
| `SELECT` from your own custom tables                | **A** | Allowed within the same software component               |
| `SELECT` from a classic (nominated) SAP CDS view    | **B** | Acceptable in classic ABAP development                   |
| Direct **read** from an SAP database table          | **C** | ATC priority 2 — use a released CDS view instead         |
| Direct **write** to an SAP database table           | **D** | ATC priority 1 — use released or classic APIs            |
| `EXEC SQL` (native SQL)                             | **D** | Critical statement — use ABAP SQL or AMDP                |
| Database hints                                      | **D** | Critical statement                                       |
| AMDP over released CDS views                        | **A** | Keep `USING` restricted to released entities             |
| AMDP over SAP tables                                | **C/D** | Read → C, write → D                                    |
| CDS table function via AMDP over released entities  | **A** | Valid Level A pushdown technique                         |

**Performance remediation**: when adapting legacy code, use SQL Monitor to detect optimization candidates, then apply code pushdown with CDS, AMDP and ABAP SQL rather than reaching for native SQL or database hints.

## Related Skills

- **cds-view-entities**: Use for CDS data modeling that works with ABAP SQL
- **abap-cloud**: Use for clean core levels and SQL-related restrictions
- **rap**: Use for understanding RAP data models that use CDS views
- **abap-cloud-migration**: Use for replacing direct table access and `EXEC SQL` during remediation
- **atc-cloudification**: Use for configuring `SYCM_USAGE_OF_APIS` and `CI_CRITICAL_STATEMENTS`
