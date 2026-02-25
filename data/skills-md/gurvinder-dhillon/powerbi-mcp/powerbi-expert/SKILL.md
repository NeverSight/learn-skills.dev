---
name: powerbi-expert
version: 1.0.0
description: Expert-level Power BI, DAX, M language, data modeling, Power Query, report design, and paginated reports
category: data
author: PCL Team
license: Apache-2.0
tags:
  - powerbi
  - dax
  - power-query
  - bi
  - microsoft
  - analytics
  - data-modeling
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
requirements:
  powerbicli: ">=3.0.0"
---

# Power BI Expert

You are an expert in Power BI with deep knowledge of DAX (Data Analysis Expressions), M language (Power Query), data modeling, relationships, measures, calculated columns, row-level security, and report design. You create performant, maintainable analytical solutions in Power BI.

## Core Expertise

### Data Modeling

**Star Schema Design:**
```
Fact Tables:
  - FactSales (OrderID, ProductKey, CustomerKey, DateKey, Quantity, Amount)
  - FactInventory (ProductKey, DateKey, StockLevel, ReorderPoint)

Dimension Tables:
  - DimProduct (ProductKey, ProductName, Category, SubCategory, Price)
  - DimCustomer (CustomerKey, CustomerName, Segment, Region, Country)
  - DimDate (DateKey, Date, Year, Quarter, Month, MonthName, Week, Day)
  - DimStore (StoreKey, StoreName, Region, Manager)

Relationships:
  FactSales[ProductKey] -> DimProduct[ProductKey] (Many-to-One)
  FactSales[CustomerKey] -> DimCustomer[CustomerKey] (Many-to-One)
  FactSales[DateKey] -> DimDate[DateKey] (Many-to-One)
  FactSales[StoreKey] -> DimStore[StoreKey] (Many-to-One)

Cardinality: Many-to-One (*:1)
Cross Filter Direction: Single (default) or Both (use sparingly)
Active Relationship: Yes
```

**Relationship Types:**
```dax
// One-to-Many (most common)
DimProduct[ProductKey] (1) -> FactSales[ProductKey] (*)

// Many-to-Many (use carefully)
FactSales (*) <-> BridgeTable (*) <-> DimPromotion (*)

// Inactive relationships (use USERELATIONSHIP)
FactSales[OrderDateKey] -> DimDate[DateKey] (Active)
FactSales[ShipDateKey] -> DimDate[DateKey] (Inactive)

// Use inactive relationship in measure
Sales by Ship Date = CALCULATE(
    [Total Sales],
    USERELATIONSHIP(FactSales[ShipDateKey], DimDate[DateKey])
)
```

**Date Table (Essential):**
```dax
// Calendar table using DAX
DimDate =
ADDCOLUMNS(
    CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31)),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "QuarterNum", QUARTER([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNum", MONTH([Date]),
    "MonthYear", FORMAT([Date], "MMM YYYY"),
    "Week", WEEKNUM([Date]),
    "Day", DAY([Date]),
    "DayOfWeek", FORMAT([Date], "dddd"),
    "DayOfWeekNum", WEEKDAY([Date]),
    "IsWeekend", WEEKDAY([Date]) IN {1, 7},
    "FiscalYear", IF(MONTH([Date]) <= 6, YEAR([Date]), YEAR([Date]) + 1),
    "FiscalQuarter", IF(MONTH([Date]) <= 6, QUARTER([Date]) + 2, QUARTER([Date]) - 2)
)

// Mark as date table
// Table Tools -> Mark as Date Table -> Date column: [Date]

// Alternative: Auto date table (not recommended for production)
// File -> Options -> Data Load -> Auto Date/Time
```

### DAX Fundamentals

**Basic Measures:**
```dax
// Simple aggregations
Total Sales = SUM(FactSales[Amount])

Total Quantity = SUM(FactSales[Quantity])

Average Sale = AVERAGE(FactSales[Amount])

Distinct Customers = DISTINCTCOUNT(FactSales[CustomerKey])

// Count rows
Total Orders = COUNTROWS(FactSales)

// Conditional sum
Sales Above 100 = SUMX(
    FILTER(FactSales, FactSales[Amount] > 100),
    FactSales[Amount]
)

// Alternative with CALCULATE
Sales Above 100 = CALCULATE(
    [Total Sales],
    FactSales[Amount] > 100
)
```

**CALCULATE - The Most Important Function:**
```dax
// Basic filter
Sales USA = CALCULATE(
    [Total Sales],
    DimCustomer[Country] = "USA"
)

// Multiple filters (AND logic)
Sales USA Electronics = CALCULATE(
    [Total Sales],
    DimCustomer[Country] = "USA",
    DimProduct[Category] = "Electronics"
)

// OR logic using ||
Sales USA or Canada = CALCULATE(
    [Total Sales],
    DimCustomer[Country] = "USA" || DimCustomer[Country] = "Canada"
)

// Using IN for multiple values
Sales North America = CALCULATE(
    [Total Sales],
    DimCustomer[Country] IN {"USA", "Canada", "Mexico"}
)

// Remove filters with ALL
Total Sales All Countries = CALCULATE(
    [Total Sales],
    ALL(DimCustomer[Country])
)

// Keep only specific filter
Sales Ignoring Other Filters = CALCULATE(
    [Total Sales],
    ALL(DimCustomer),
    DimCustomer[Country] = "USA"
)

// Remove all filters
Grand Total = CALCULATE(
    [Total Sales],
    ALL(FactSales)
)
```

**Time Intelligence:**
```dax
// Year to date
YTD Sales = TOTALYTD(
    [Total Sales],
    DimDate[Date]
)

// Quarter to date
QTD Sales = TOTALQTD(
    [Total Sales],
    DimDate[Date]
)

// Month to date
MTD Sales = TOTALMTD(
    [Total Sales],
    DimDate[Date]
)

// Previous year
Sales PY = CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

// Year over year growth
YoY Growth =
VAR CurrentYearSales = [Total Sales]
VAR PreviousYearSales = [Sales PY]
RETURN
    DIVIDE(CurrentYearSales - PreviousYearSales, PreviousYearSales)

// Previous month
Sales PM = CALCULATE(
    [Total Sales],
    DATEADD(DimDate[Date], -1, MONTH)
)

// Month over month growth
MoM Growth =
DIVIDE(
    [Total Sales] - [Sales PM],
    [Sales PM]
)

// Last N days
Sales Last 30 Days = CALCULATE(
    [Total Sales],
    DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -30, DAY)
)

// Moving average
Sales MA 3 Months =
CALCULATE(
    [Total Sales],
    DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -3, MONTH)
) / 3

// Same period last year
Sales SPLY = CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

// Parallel period (previous complete period)
Sales Previous Quarter = CALCULATE(
    [Total Sales],
    PARALLELPERIOD(DimDate[Date], -1, QUARTER)
)
```

**Iterator Functions:**
```dax
// SUMX - row by row calculation
Total Revenue = SUMX(
    FactSales,
    FactSales[Quantity] * FactSales[UnitPrice]
)

// AVERAGEX
Average Order Value = AVERAGEX(
    VALUES(FactSales[OrderID]),
    [Total Sales]
)

// COUNTX with condition
Orders Above 1000 = COUNTX(
    FILTER(FactSales, [Total Sales] > 1000),
    FactSales[OrderID]
)

// RANKX
Product Rank = RANKX(
    ALL(DimProduct[ProductName]),
    [Total Sales],
    ,
    DESC,
    DENSE
)

// MINX / MAXX
Lowest Product Price = MINX(
    DimProduct,
    DimProduct[Price]
)

// Combining iterators
Weighted Average =
DIVIDE(
    SUMX(DimProduct, DimProduct[Price] * DimProduct[Weight]),
    SUM(DimProduct[Weight])
)
```

**Filter Context and Row Context:**
```dax
// Understanding context
// Filter context: Applied by slicers, filters, rows/columns in visual

// This measure changes with filter context
Total Sales = SUM(FactSales[Amount])

// This measure ignores filter context on Country
Total Sales All Countries = CALCULATE(
    SUM(FactSales[Amount]),
    ALL(DimCustomer[Country])
)

// Row context: When iterating through rows
// Calculated column (has row context)
Profit = FactSales[Amount] - FactSales[Cost]

// To use measure in row context, use iterator
Total Profit = SUMX(
    FactSales,
    [Total Sales] - [Total Cost]
)

// Converting row context to filter context
// Calculated column
Customer Sales = CALCULATE(
    [Total Sales],
    ALLEXCEPT(FactSales, FactSales[CustomerKey])
)
```

### Advanced DAX

**Variables (VAR):**
```dax
// Using variables for clarity and performance
Sales vs Target =
VAR ActualSales = [Total Sales]
VAR TargetSales = [Sales Target]
VAR Variance = ActualSales - TargetSales
VAR VariancePct = DIVIDE(Variance, TargetSales)
RETURN
    IF(
        ISBLANK(TargetSales),
        BLANK(),
        VariancePct
    )

// Variables are evaluated once
Customer Lifetime Value =
VAR FirstPurchase =
    CALCULATE(
        MIN(FactSales[Date]),
        ALLEXCEPT(FactSales, FactSales[CustomerKey])
    )
VAR LastPurchase =
    CALCULATE(
        MAX(FactSales[Date]),
        ALLEXCEPT(FactSales, FactSales[CustomerKey])
    )
VAR DaysBetween = DATEDIFF(FirstPurchase, LastPurchase, DAY)
VAR TotalSpend =
    CALCULATE(
        [Total Sales],
        ALLEXCEPT(FactSales, FactSales[CustomerKey])
    )
RETURN
    DIVIDE(TotalSpend, DIVIDE(DaysBetween, 365), 0)
```

**SWITCH and Complex Logic:**
```dax
// SWITCH for multiple conditions
Metric Selector =
SWITCH(
    SELECTEDVALUE(MetricParameter[Metric]),
    "Revenue", [Total Sales],
    "Profit", [Total Profit],
    "Quantity", [Total Quantity],
    "Orders", [Total Orders],
    BLANK()
)

// Nested IF vs SWITCH
Customer Tier =
VAR LTV = [Customer Lifetime Value]
RETURN
    SWITCH(
        TRUE(),
        LTV >= 10000, "VIP",
        LTV >= 5000, "Gold",
        LTV >= 1000, "Silver",
        "Bronze"
    )

// Complex business logic
Sales Performance =
VAR CurrentSales = [Total Sales]
VAR TargetSales = [Sales Target]
VAR GrowthRate = [YoY Growth]
RETURN
    SWITCH(
        TRUE(),
        ISBLANK(CurrentSales), "No Data",
        CurrentSales >= TargetSales && GrowthRate >= 0.1, "Exceeding",
        CurrentSales >= TargetSales, "Meeting Target",
        CurrentSales >= TargetSales * 0.9, "Close to Target",
        "Below Target"
    )
```

**ALL Family Functions:**
```dax
// ALL - removes all filters
All Sales = CALCULATE([Total Sales], ALL(FactSales))

// ALLSELECTED - removes filters but keeps external filters
Sales % of Selected =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALLSELECTED())
)

// ALLEXCEPT - removes all filters except specified
Sales Same Customer = CALCULATE(
    [Total Sales],
    ALLEXCEPT(FactSales, FactSales[CustomerKey])
)

// REMOVEFILTERS (modern alternative to ALL)
Sales All Products = CALCULATE(
    [Total Sales],
    REMOVEFILTERS(DimProduct)
)

// VALUES vs ALL
// VALUES - returns filtered distinct values
// ALL - returns all distinct values (ignores filters)

Filtered Product Count = COUNTROWS(VALUES(DimProduct[ProductName]))
All Product Count = COUNTROWS(ALL(DimProduct[ProductName]))
```

**CALCULATE Modifiers:**
```dax
// KEEPFILTERS - adds filter without removing existing
Sales With Filter = CALCULATE(
    [Total Sales],
    KEEPFILTERS(DimProduct[Category] = "Electronics")
)

// USERELATIONSHIP - activate inactive relationship
Sales by Ship Date = CALCULATE(
    [Total Sales],
    USERELATIONSHIP(FactSales[ShipDateKey], DimDate[DateKey])
)

// CROSSFILTER - change relationship direction
Sales Both Ways = CALCULATE(
    [Total Sales],
    CROSSFILTER(FactSales[ProductKey], DimProduct[ProductKey], BOTH)
)

// ALL - remove filter
Sales All Regions = CALCULATE(
    [Total Sales],
    ALL(DimCustomer[Region])
)
```

**Virtual Tables:**
```dax
// SUMMARIZE - create virtual summary table
Sales by Category =
SUMX(
    SUMMARIZE(
        FactSales,
        DimProduct[Category],
        "CategorySales", [Total Sales]
    ),
    [CategorySales]
)

// ADDCOLUMNS - add calculated columns to table
Top Customers =
TOPN(
    10,
    ADDCOLUMNS(
        VALUES(DimCustomer[CustomerName]),
        "CustomerSales", [Total Sales]
    ),
    [CustomerSales],
    DESC
)

// SELECTCOLUMNS - select specific columns
Customer List =
SELECTCOLUMNS(
    DimCustomer,
    "Name", DimCustomer[CustomerName],
    "Country", DimCustomer[Country]
)

// GENERATE - cartesian product
Date Product Combinations =
GENERATE(
    VALUES(DimDate[Date]),
    VALUES(DimProduct[ProductName])
)
```

### Power Query (M Language)

**Data Transformation:**
```m
// Basic transformations
let
    Source = Sql.Database("server", "database"),
    FactSales = Source{[Schema="dbo",Item="FactSales"]}[Data],

    // Remove columns
    RemovedColumns = Table.RemoveColumns(FactSales, {"UnneededColumn1", "UnneededColumn2"}),

    // Rename columns
    RenamedColumns = Table.RenameColumns(RemovedColumns, {
        {"old_name", "NewName"},
        {"order_date", "OrderDate"}
    }),

    // Change data types
    ChangedTypes = Table.TransformColumnTypes(RenamedColumns, {
        {"OrderDate", type date},
        {"Amount", type number},
        {"Quantity", Int64.Type}
    }),

    // Filter rows
    FilteredRows = Table.SelectRows(ChangedTypes, each [OrderDate] >= #date(2020, 1, 1)),

    // Add custom column
    AddedCustom = Table.AddColumn(FilteredRows, "Revenue",
        each [Quantity] * [UnitPrice], type number),

    // Replace values
    ReplacedValues = Table.ReplaceValue(FilteredRows, null, 0,
        Replacer.ReplaceValue, {"Discount"}),

    // Remove duplicates
    RemovedDuplicates = Table.Distinct(AddedCustom, {"OrderID"})
in
    RemovedDuplicates
```

**Advanced M Functions:**
```m
// Custom function
let
    GetSalesByDate = (startDate as date, endDate as date) as table =>
    let
        Source = Sql.Database("server", "database"),
        FactSales = Source{[Schema="dbo",Item="FactSales"]}[Data],
        FilteredRows = Table.SelectRows(FactSales,
            each [OrderDate] >= startDate and [OrderDate] <= endDate)
    in
        FilteredRows
in
    GetSalesByDate

// Invoke function
Sales2024 = GetSalesByDate(#date(2024, 1, 1), #date(2024, 12, 31))

// Conditional column
AddedConditional = Table.AddColumn(Source, "Segment",
    each if [Amount] >= 1000 then "High"
         else if [Amount] >= 500 then "Medium"
         else "Low")

// Group by (aggregation)
GroupedRows = Table.Group(Source, {"CustomerID"}, {
    {"TotalSales", each List.Sum([Amount]), type number},
    {"OrderCount", each Table.RowCount(_), Int64.Type},
    {"AvgAmount", each List.Average([Amount]), type number}
})

// Merge queries (joins)
Merged = Table.NestedJoin(
    FactSales, {"ProductKey"},
    DimProduct, {"ProductKey"},
    "Product",
    JoinKind.LeftOuter
)

// Expand merged table
Expanded = Table.ExpandTableColumn(Merged, "Product",
    {"ProductName", "Category"},
    {"ProductName", "Category"})

// Append queries (union)
Appended = Table.Combine({Sales2023, Sales2024})

// Pivot
Pivoted = Table.Pivot(Source,
    List.Distinct(Source[Category]),
    "Category",
    "Amount",
    List.Sum)

// Unpivot
Unpivoted = Table.UnpivotOtherColumns(Source,
    {"Date", "Product"},
    "Attribute",
    "Value")
```

**Parameters and Dynamic Queries:**
```m
// Parameter
EnvironmentParameter = "Production" meta [IsParameterQuery=true, Type="Text", AllowedValues={"Development", "Production"}]

// Use in connection string
let
    Server = if EnvironmentParameter = "Production"
             then "prod-server.database.windows.net"
             else "dev-server.database.windows.net",
    Source = Sql.Database(Server, "database")
in
    Source

// Date range parameters
StartDate = #date(2024, 1, 1) meta [IsParameterQuery=true, Type="Date"]
EndDate = #date(2024, 12, 31) meta [IsParameterQuery=true, Type="Date"]

// Query folding check
Table.View(null, [
    GetType = () => type table [OrderID = Int64.Type, Amount = number],
    GetRows = () => #table(
        {"OrderID", "Amount"},
        {{1, 100}, {2, 200}}
    ),
    OnTake = (count as number) => ...,
    OnSkip = (count as number) => ...
])
```

### Row-Level Security (RLS)

**Role-Based Security:**
```dax
// Create role: Sales_USA
[Country] = "USA"

// Create role: Regional_Manager
[Region] = USERPRINCIPALNAME()

// Dynamic RLS using security table
// SecurityTable: Email | Region
[Region] IN
    CALCULATETABLE(
        VALUES(SecurityTable[Region]),
        SecurityTable[Email] = USERPRINCIPALNAME()
    )

// Manager hierarchy
// EmployeeTable: EmployeeID | ManagerID
VAR CurrentUser = USERPRINCIPALNAME()
VAR CurrentEmployeeID =
    LOOKUPVALUE(
        EmployeeTable[EmployeeID],
        EmployeeTable[Email], CurrentUser
    )
RETURN
    PATHCONTAINS(
        EmployeeTable[Path],
        CurrentEmployeeID
    )

// Multiple conditions (OR)
[Region] = "North" || [Region] = "South"

// Exclude admin users
[Region] = "North" ||
USERPRINCIPALNAME() = "admin@company.com"
```

**Object-Level Security:**
```dax
// Hide entire table from role
// Manage Roles -> Advanced -> Object-level security
// Table: SensitiveData -> Unchecked for standard users

// Hide specific columns using RLS
// Can't directly hide columns, but can obfuscate values
SensitiveColumn =
IF(
    USERPRINCIPALNAME() IN {"admin@company.com", "manager@company.com"},
    [ActualSensitiveColumn],
    BLANK()
)
```

### Report Design

**Visualizations:**
```
// KPI Cards
Card: Total Sales
- Format: $#,##0.0K
- Conditional formatting based on target

// Charts
Line chart: Sales trend by month
- X-axis: Date (month)
- Y-axis: Total Sales
- Legend: Category
- Tooltips: Custom with additional metrics

Bar chart: Sales by product
- Y-axis: Product Name
- X-axis: Total Sales
- Data labels: On
- Top N filter: 10

// Matrix
Rows: Category, SubCategory, Product
Columns: Year, Quarter, Month
Values: Sales, Profit, Margin %
Conditional formatting: Data bars, color scales

// Map
Map: Sales by country
- Location: Country
- Bubble size: Total Sales
- Color: Profit Margin

// Decomposition Tree
Decomp: Analyze sales
- Root: Total Sales
- Explain by: Category, Region, Product

// Key Influencers
Influencers: What drives high sales
- Analyze: Total Sales
- Explain by: Product, Region, Customer Segment
```

**Bookmarks and Drill-Through:**
```
// Bookmarks
Bookmark 1: Sales View
- Visible: Sales chart, Sales KPIs
- Hidden: Profit details

Bookmark 2: Profit View
- Visible: Profit chart, Profit KPIs
- Hidden: Sales details

// Drill-through page
Page: Product Details
- Drillthrough from: Sales by Category
- Required fields: Product Name
- Content: Product metrics, related products, trend

// Buttons with actions
Button: Show Profit Details
- Action: Bookmark -> Profit View
- Tooltip: "Click to see profit analysis"
```

## Best Practices

### 1. Data Modeling
- Use star schema (fact and dimension tables)
- Create proper date table and mark it
- Set correct cardinality and filter direction
- Hide columns not needed in reports
- Create relationships on integer keys, not strings
- Avoid bidirectional relationships unless necessary

### 2. DAX Performance
- Use variables to avoid recalculation
- Prefer CALCULATE over iterators when possible
- Use COUNTROWS instead of COUNT
- Avoid calculated columns; use measures instead
- Use SELECTEDVALUE for single-value columns
- Filter on dimension tables, not fact tables

### 3. Report Design
- Limit visuals per page (5-7 optimal)
- Use bookmarks for complex navigation
- Implement drill-through for details
- Use consistent colors and formatting
- Optimize visual types for mobile
- Test performance with large datasets

### 4. Power Query
- Enable query folding when possible
- Perform filtering early in transformation
- Use parameters for reusable queries
- Disable "Include in report refresh" for reference queries
- Document custom functions
- Use native queries for complex SQL

### 5. Security
- Implement row-level security at table level
- Test RLS with "View as" feature
- Use dynamic RLS with security tables
- Document security roles
- Avoid bypassing RLS in measures

## Anti-Patterns

### 1. Calculated Columns vs Measures
```dax
// Bad: Calculated column (stored, consumes memory)
TotalRevenue = FactSales[Quantity] * FactSales[UnitPrice]

// Good: Measure (calculated on demand)
Total Revenue = SUMX(FactSales, FactSales[Quantity] * FactSales[UnitPrice])
```

### 2. Bidirectional Relationships
```dax
// Bad: Bidirectional filter on all relationships
// Can cause ambiguity and performance issues

// Good: Use specific relationships
Sales with Both Filters = CALCULATE(
    [Total Sales],
    CROSSFILTER(FactSales[ProductKey], DimProduct[ProductKey], BOTH)
)
```

### 3. Not Using Variables
```dax
// Bad: Repeated calculation
Margin % = ([Total Sales] - [Total Cost]) / [Total Sales]

// Good: Use variables
Margin % =
VAR Sales = [Total Sales]
VAR Cost = [Total Cost]
VAR Margin = Sales - Cost
RETURN DIVIDE(Margin, Sales)
```

### 4. Ignoring Query Folding
```m
// Bad: Filtering after loading all data
Source = Sql.Database("server", "database"),
AllData = Source{[Schema="dbo",Item="FactSales"]}[Data],
FilteredRows = Table.SelectRows(AllData, each [Year] = 2024)

// Good: Filter at source (query folding)
Source = Sql.Database("server", "database"),
FilteredData = Table.SelectRows(Source{[Schema="dbo",Item="FactSales"]}[Data],
    each [Year] = 2024)
```

## Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Guide](https://dax.guide/)
- [SQLBI](https://www.sqlbi.com/)
- [Power BI Community](https://community.powerbi.com/)
- [DAX Formatter](https://www.daxformatter.com/)
- [Power BI Best Practices](https://docs.microsoft.com/power-bi/guidance/)
- [M Language Reference](https://docs.microsoft.com/powerquery-m/)
