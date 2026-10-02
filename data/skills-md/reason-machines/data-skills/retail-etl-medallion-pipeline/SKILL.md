---
name: retail-etl-medallion-pipeline
description: End-to-end retail ETL pipeline using Medallion Architecture (Bronze/Silver/Gold) with TSQL, PySpark, and Airflow for inventory, sales, and supplier data processing
triggers:
  - build a retail data warehouse with medallion architecture
  - create bronze silver gold layers for retail analytics
  - set up retail ETL pipeline with inventory tracking
  - implement medallion architecture for sales data
  - process retail data with bronze silver gold pattern
  - design data warehouse for hypermarket or retail business
  - transform retail sales and inventory data by layers
  - orchestrate retail ETL with airflow and spark
---

# Retail ETL Medallion Pipeline Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project implements a production-grade **Medallion Architecture** ETL pipeline for retail/hypermarket data, handling complex business logic like inventory shrinkage, meat/poultry recipe conversions, supplier rebate tiers, and multi-branch sales consolidation. The architecture follows three data quality layers:

- **Bronze Layer**: Raw data ingestion from CSV sources (sales, stock, products)
- **Silver Layer**: Cleaned, standardized, and business-rule-applied data
- **Gold Layer**: Aggregated, analytics-ready dimensional models

The pipeline processes:
- Multi-branch sales transactions (Alex, Cairo, Giza)
- Product catalogs with recipe/yield conversions
- Stock/inventory tracking across locations
- Supplier rebate calculations

## Project Structure

```
Retail-Data-Warehouse/
├── data_source/              # Raw CSV files (CRM/ERP exports)
│   ├── 000.Hypermarket Products.csv
│   ├── 001-003.*.Branch Sales.csv
│   └── 004-006.*.Stock.csv
├── sql_scripts/              # TSQL stored procedures for each layer
│   ├── 00_create_database_and_schemas.sql
│   ├── 01-04_bronze_*.sql
│   ├── 05-08_silver_*.sql
│   └── 09-12_gold_*.sql
├── BI_Team_Analysis/         # Power BI dashboards
└── docker-compose.yml        # SQL Server container setup
```

## Installation & Setup

### 1. Infrastructure Setup (SQL Server)

Using Docker:

```bash
# Start SQL Server container
docker-compose up -d

# Verify container is running
docker ps | grep sqlserver
```

Or use an existing SQL Server instance (2017+).

### 2. Database Initialization

```bash
# Connect to SQL Server and create database structure
sqlcmd -S localhost -U sa -P $SQL_SA_PASSWORD -i sql_scripts/00_create_database_and_schemas.sql
```

This creates:
- Database: `RetailDataWarehouse`
- Schemas: `bronze`, `silver`, `gold`, `staging`

### 3. Load Raw Data to Bronze Layer

Place CSV files in accessible location, then run:

```sql
-- Execute Bronze layer ingestion procedures
EXEC bronze.usp_LoadProducts;
EXEC bronze.usp_LoadSales;
EXEC bronze.usp_LoadStock;
```

Or execute all Bronze scripts sequentially:

```bash
for script in sql_scripts/01_bronze_*.sql sql_scripts/02_bronze_*.sql sql_scripts/03_bronze_*.sql sql_scripts/04_bronze_*.sql; do
    sqlcmd -S localhost -U sa -P $SQL_SA_PASSWORD -i "$script"
done
```

## Key Architecture Patterns

### Bronze Layer (Raw Ingestion)

**Purpose**: Land raw data with minimal transformation. Add audit columns only.

```sql
-- Example: Bronze Products Table Structure
CREATE TABLE bronze.Products (
    ProductID INT,
    ProductName NVARCHAR(255),
    Category NVARCHAR(100),
    SubCategory NVARCHAR(100),
    UnitPrice DECIMAL(10,2),
    SupplierID INT,
    RecipeYield DECIMAL(5,2),  -- For meat/poultry conversions
    LoadTimestamp DATETIME2 DEFAULT GETDATE(),
    SourceFile NVARCHAR(500)
);

-- Bronze Load Pattern
CREATE PROCEDURE bronze.usp_LoadProducts
AS
BEGIN
    TRUNCATE TABLE bronze.Products;
    
    BULK INSERT bronze.Products
    FROM '/data/000.Hypermarket Products.csv'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        FIRSTROW = 2,
        ERRORFILE = '/logs/products_errors.txt'
    );
    
    -- Add audit metadata
    UPDATE bronze.Products
    SET LoadTimestamp = GETDATE(),
        SourceFile = '000.Hypermarket Products.csv';
END;
```

### Silver Layer (Cleaned & Standardized)

**Purpose**: Apply data quality rules, deduplication, and business transformations.

```sql
-- Example: Silver Sales with Business Rules
CREATE PROCEDURE silver.usp_TransformSales
AS
BEGIN
    TRUNCATE TABLE silver.Sales;
    
    INSERT INTO silver.Sales (
        SaleID,
        BranchID,
        ProductID,
        SaleDate,
        Quantity,
        UnitPrice,
        TotalAmount,
        AdjustedQuantity,  -- Recipe conversion applied
        DataQualityScore
    )
    SELECT 
        s.SaleID,
        s.BranchID,
        s.ProductID,
        CAST(s.SaleDate AS DATE) AS SaleDate,
        s.Quantity,
        s.UnitPrice,
        s.Quantity * s.UnitPrice AS TotalAmount,
        -- Apply recipe yield for meat/poultry
        CASE 
            WHEN p.Category = 'Meat & Poultry' 
            THEN s.Quantity * ISNULL(p.RecipeYield, 1.0)
            ELSE s.Quantity
        END AS AdjustedQuantity,
        -- Data quality scoring
        CASE 
            WHEN s.Quantity > 0 AND s.UnitPrice > 0 THEN 100
            WHEN s.Quantity IS NULL OR s.UnitPrice IS NULL THEN 0
            ELSE 50
        END AS DataQualityScore
    FROM bronze.Sales s
    INNER JOIN bronze.Products p ON s.ProductID = p.ProductID
    WHERE s.Quantity > 0  -- Filter invalid records
      AND s.SaleDate >= DATEADD(YEAR, -2, GETDATE());  -- Keep 2 years
END;
```

**Key Silver Transformations**:
- Date standardization
- Recipe yield conversions for perishables
- Duplicate removal
- Null handling and imputation
- Data quality scoring

### Gold Layer (Analytics-Ready Aggregates)

**Purpose**: Create dimensional models and pre-aggregated metrics for BI tools.

```sql
-- Example: Gold Inventory Turnover Metrics
CREATE PROCEDURE gold.usp_BuildInventoryMetrics
AS
BEGIN
    TRUNCATE TABLE gold.InventoryTurnover;
    
    INSERT INTO gold.InventoryTurnover (
        ProductID,
        ProductName,
        Category,
        BranchID,
        Month,
        TotalSalesQty,
        AvgStockLevel,
        TurnoverRatio,
        ShrinkagePercent,
        ReorderAlert
    )
    SELECT 
        p.ProductID,
        p.ProductName,
        p.Category,
        s.BranchID,
        DATEPART(MONTH, s.SaleDate) AS Month,
        SUM(s.AdjustedQuantity) AS TotalSalesQty,
        AVG(st.StockQuantity) AS AvgStockLevel,
        -- Turnover = Sales / Avg Stock
        CASE 
            WHEN AVG(st.StockQuantity) > 0 
            THEN SUM(s.AdjustedQuantity) / AVG(st.StockQuantity)
            ELSE 0
        END AS TurnoverRatio,
        -- Shrinkage = (Expected - Actual) / Expected
        CASE 
            WHEN SUM(st.ExpectedStock) > 0
            THEN ((SUM(st.ExpectedStock) - SUM(st.StockQuantity)) * 100.0) / SUM(st.ExpectedStock)
            ELSE 0
        END AS ShrinkagePercent,
        -- Alert if turnover < 2 (slow-moving inventory)
        CASE 
            WHEN SUM(s.AdjustedQuantity) / NULLIF(AVG(st.StockQuantity), 0) < 2 
            THEN 'Reorder Needed'
            ELSE 'OK'
        END AS ReorderAlert
    FROM silver.Sales s
    INNER JOIN silver.Products p ON s.ProductID = p.ProductID
    LEFT JOIN silver.Stock st ON s.ProductID = st.ProductID AND s.BranchID = st.BranchID
    GROUP BY p.ProductID, p.ProductName, p.Category, s.BranchID, DATEPART(MONTH, s.SaleDate);
END;
```

**Gold Layer Tables**:
- `InventoryTurnover`: Stock efficiency metrics
- `SalesPerformance`: Revenue aggregates by branch/category
- `SupplierRebates`: Tiered rebate calculations
- `ProductMargins`: Profit analysis dimensions

## Complete Pipeline Execution

### Manual Execution (Sequential)

```sql
-- 1. Bronze: Load raw data
EXEC bronze.usp_LoadProducts;
EXEC bronze.usp_LoadSales;
EXEC bronze.usp_LoadStock;

-- 2. Silver: Apply transformations
EXEC silver.usp_TransformProducts;
EXEC silver.usp_TransformSales;
EXEC silver.usp_TransformStock;

-- 3. Gold: Build analytics aggregates
EXEC gold.usp_BuildInventoryMetrics;
EXEC gold.usp_BuildSalesPerformance;
EXEC gold.usp_BuildSupplierRebates;

-- 4. Verify row counts
SELECT 'Bronze Products' AS Layer, COUNT(*) AS RowCount FROM bronze.Products
UNION ALL
SELECT 'Silver Products', COUNT(*) FROM silver.Products
UNION ALL
SELECT 'Gold Inventory', COUNT(*) FROM gold.InventoryTurnover;
```

### Automated Pipeline Script

```bash
#!/bin/bash
# run_etl_pipeline.sh

set -e

SQL_SERVER="${SQL_SERVER:-localhost}"
SQL_USER="${SQL_USER:-sa}"
SQL_PASSWORD="${SQL_PASSWORD}"

echo "Starting Retail ETL Pipeline..."

# Bronze Layer
echo "[1/3] Loading Bronze Layer..."
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC bronze.usp_LoadProducts;"
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC bronze.usp_LoadSales;"
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC bronze.usp_LoadStock;"

# Silver Layer
echo "[2/3] Transforming Silver Layer..."
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC silver.usp_TransformProducts;"
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC silver.usp_TransformSales;"
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC silver.usp_TransformStock;"

# Gold Layer
echo "[3/3] Building Gold Layer..."
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC gold.usp_BuildInventoryMetrics;"
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d RetailDataWarehouse -Q "EXEC gold.usp_BuildSalesPerformance;"

echo "Pipeline completed successfully!"
```

## Configuration

### Environment Variables

```bash
# .env file for pipeline configuration
SQL_SERVER=localhost
SQL_USER=sa
SQL_PASSWORD=${SQL_SA_PASSWORD}
SQL_DATABASE=RetailDataWarehouse

# Data source paths
DATA_SOURCE_PATH=/path/to/data_source
LOGS_PATH=/var/log/retail-etl

# Airflow (if using orchestration)
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__DAGS_FOLDER=${AIRFLOW_HOME}/dags
```

### Docker Compose Configuration

```yaml
version: '3.8'
services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2019-latest
    environment:
      ACCEPT_EULA: Y
      SA_PASSWORD: ${SQL_SA_PASSWORD}
      MSSQL_PID: Developer
    ports:
      - "1433:1433"
    volumes:
      - ./data_source:/data
      - ./sql_scripts:/scripts
      - sqlserver_data:/var/opt/mssql
    restart: unless-stopped

volumes:
  sqlserver_data:
```

## Business Logic Examples

### Recipe Conversion for Meat Products

```sql
-- Handle meat/poultry yield conversions
-- Example: 1kg raw chicken → 0.65kg cooked meat
CREATE FUNCTION dbo.fn_ApplyRecipeYield(
    @Quantity DECIMAL(10,2),
    @RecipeYield DECIMAL(5,2),
    @Category NVARCHAR(100)
)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @AdjustedQty DECIMAL(10,2);
    
    IF @Category IN ('Meat & Poultry', 'Seafood')
        SET @AdjustedQty = @Quantity * ISNULL(@RecipeYield, 1.0);
    ELSE
        SET @AdjustedQty = @Quantity;
    
    RETURN @AdjustedQty;
END;
```

### Supplier Rebate Tiers

```sql
-- Calculate dynamic rebate percentages based on purchase volume
CREATE PROCEDURE gold.usp_CalculateSupplierRebates
AS
BEGIN
    INSERT INTO gold.SupplierRebates (
        SupplierID,
        TotalPurchaseAmount,
        RebateTier,
        RebatePercent,
        RebateAmount
    )
    SELECT 
        SupplierID,
        SUM(TotalAmount) AS TotalPurchaseAmount,
        CASE 
            WHEN SUM(TotalAmount) >= 100000 THEN 'Platinum'
            WHEN SUM(TotalAmount) >= 50000 THEN 'Gold'
            WHEN SUM(TotalAmount) >= 25000 THEN 'Silver'
            ELSE 'Bronze'
        END AS RebateTier,
        CASE 
            WHEN SUM(TotalAmount) >= 100000 THEN 5.0
            WHEN SUM(TotalAmount) >= 50000 THEN 3.0
            WHEN SUM(TotalAmount) >= 25000 THEN 1.5
            ELSE 0.0
        END AS RebatePercent,
        SUM(TotalAmount) * 
        CASE 
            WHEN SUM(TotalAmount) >= 100000 THEN 0.05
            WHEN SUM(TotalAmount) >= 50000 THEN 0.03
            WHEN SUM(TotalAmount) >= 25000 THEN 0.015
            ELSE 0.0
        END AS RebateAmount
    FROM silver.Sales s
    INNER JOIN silver.Products p ON s.ProductID = p.ProductID
    GROUP BY SupplierID;
END;
```

### Inventory Shrinkage Detection

```sql
-- Identify products with abnormal shrinkage
SELECT 
    p.ProductName,
    p.Category,
    st.BranchID,
    st.ExpectedStock,
    st.StockQuantity AS ActualStock,
    ((st.ExpectedStock - st.StockQuantity) * 100.0) / st.ExpectedStock AS ShrinkagePercent
FROM silver.Stock st
INNER JOIN silver.Products p ON st.ProductID = p.ProductID
WHERE st.ExpectedStock > 0
  AND ((st.ExpectedStock - st.StockQuantity) * 100.0) / st.ExpectedStock > 5.0  -- >5% shrinkage threshold
ORDER BY ShrinkagePercent DESC;
```

## Data Quality Checks

### Validation Queries

```sql
-- Check for duplicate sales records
SELECT SaleID, COUNT(*) AS Duplicates
FROM bronze.Sales
GROUP BY SaleID
HAVING COUNT(*) > 1;

-- Validate price consistency
SELECT 
    p.ProductID,
    p.ProductName,
    COUNT(DISTINCT s.UnitPrice) AS PriceVariations
FROM silver.Products p
INNER JOIN silver.Sales s ON p.ProductID = s.ProductID
GROUP BY p.ProductID, p.ProductName
HAVING COUNT(DISTINCT s.UnitPrice) > 3;  -- More than 3 price points

-- Check for negative stock
SELECT ProductID, BranchID, StockQuantity
FROM silver.Stock
WHERE StockQuantity < 0;

-- Data completeness metrics
SELECT 
    'Products' AS TableName,
    COUNT(*) AS TotalRows,
    SUM(CASE WHEN ProductName IS NULL THEN 1 ELSE 0 END) AS NullProductNames,
    SUM(CASE WHEN UnitPrice IS NULL THEN 1 ELSE 0 END) AS NullPrices
FROM silver.Products;
```

## Troubleshooting

### Common Issues

**Issue**: BULK INSERT fails with permission error
```sql
-- Solution: Grant read permissions to SQL Server service account
-- Or use OPENROWSET with explicit credentials
INSERT INTO bronze.Products
SELECT * FROM OPENROWSET(
    BULK '/data/000.Hypermarket Products.csv',
    FORMATFILE = '/data/products_format.xml',
    ERRORFILE = '/logs/errors.txt'
) AS DataFile;
```

**Issue**: Recipe yield conversions producing NULL values
```sql
-- Check for missing RecipeYield in Products table
SELECT ProductID, ProductName, Category, RecipeYield
FROM bronze.Products
WHERE Category IN ('Meat & Poultry', 'Seafood')
  AND RecipeYield IS NULL;

-- Fix: Set default yield to 1.0
UPDATE bronze.Products
SET RecipeYield = 1.0
WHERE RecipeYield IS NULL;
```

**Issue**: Silver layer procedure times out on large datasets
```sql
-- Solution: Add batch processing with cursor or temp tables
CREATE PROCEDURE silver.usp_TransformSalesBatch
    @BatchSize INT = 10000
AS
BEGIN
    DECLARE @MinID INT, @MaxID INT;
    
    SELECT @MinID = MIN(SaleID), @MaxID = MAX(SaleID) FROM bronze.Sales;
    
    WHILE @MinID <= @MaxID
    BEGIN
        INSERT INTO silver.Sales (...)
        SELECT ...
        FROM bronze.Sales
        WHERE SaleID BETWEEN @MinID AND (@MinID + @BatchSize - 1);
        
        SET @MinID = @MinID + @BatchSize;
    END;
END;
```

**Issue**: Gold aggregates not updating incrementally
```sql
-- Solution: Implement incremental load with watermark
CREATE TABLE gold.ETL_Watermark (
    TableName NVARCHAR(100),
    LastProcessedDate DATETIME2
);

CREATE PROCEDURE gold.usp_IncrementalInventoryMetrics
AS
BEGIN
    DECLARE @LastRun DATETIME2;
    SELECT @LastRun = LastProcessedDate FROM gold.ETL_Watermark WHERE TableName = 'InventoryMetrics';
    
    -- Delete and recalculate only changed data
    DELETE FROM gold.InventoryTurnover
    WHERE Month >= DATEPART(MONTH, @LastRun);
    
    INSERT INTO gold.InventoryTurnover (...)
    SELECT ...
    FROM silver.Sales
    WHERE SaleDate >= @LastRun;
    
    -- Update watermark
    UPDATE gold.ETL_Watermark 
    SET LastProcessedDate = GETDATE()
    WHERE TableName = 'InventoryMetrics';
END;
```

### Performance Optimization

```sql
-- Add indexes for Bronze layer queries
CREATE CLUSTERED INDEX IX_Sales_SaleID ON bronze.Sales(SaleID);
CREATE NONCLUSTERED INDEX IX_Sales_ProductID ON bronze.Sales(ProductID);
CREATE NONCLUSTERED INDEX IX_Sales_SaleDate ON bronze.Sales(SaleDate);

-- Partition Gold tables by month for faster queries
CREATE PARTITION FUNCTION pf_MonthPartition (INT)
AS RANGE RIGHT FOR VALUES (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);

CREATE PARTITION SCHEME ps_MonthPartition
AS PARTITION pf_MonthPartition ALL TO ([PRIMARY]);

CREATE TABLE gold.InventoryTurnover (
    ...
    Month INT
) ON ps_MonthPartition(Month);

-- Enable query store for performance monitoring
ALTER DATABASE RetailDataWarehouse SET QUERY_STORE = ON;
```

## Integration with BI Tools

### Power BI Connection

```sql
-- Create view optimized for Power BI
CREATE VIEW gold.vw_SalesDashboard AS
SELECT 
    s.SaleDate,
    p.ProductName,
    p.Category,
    b.BranchName,
    s.Quantity,
    s.UnitPrice,
    s.TotalAmount,
    i.TurnoverRatio,
    i.ShrinkagePercent
FROM gold.InventoryTurnover i
INNER JOIN silver.Sales s ON i.ProductID = s.ProductID AND i.BranchID = s.BranchID
INNER JOIN silver.Products p ON s.ProductID = p.ProductID
INNER JOIN silver.Branches b ON s.BranchID = b.BranchID;

-- Grant read-only access to BI service account
CREATE USER [bi_service] WITH PASSWORD = '${BI_SERVICE_PASSWORD}';
GRANT SELECT ON SCHEMA::gold TO [bi_service];
```

## Monitoring & Logging

```sql
-- Create audit log table
CREATE TABLE dbo.ETL_AuditLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    ProcedureName NVARCHAR(255),
    LayerName NVARCHAR(50),
    StartTime DATETIME2,
    EndTime DATETIME2,
    RowsProcessed INT,
    Status NVARCHAR(50),
    ErrorMessage NVARCHAR(MAX)
);

-- Example audit logging in procedures
CREATE PROCEDURE silver.usp_TransformSalesWithLogging
AS
BEGIN
    DECLARE @StartTime DATETIME2 = GETDATE();
    DECLARE @RowCount INT;
    
    BEGIN TRY
        -- Transform logic
        INSERT INTO silver.Sales (...) SELECT ...;
        SET @RowCount = @@ROWCOUNT;
        
        -- Log success
        INSERT INTO dbo.ETL_AuditLog (ProcedureName, LayerName, StartTime, EndTime, RowsProcessed, Status)
        VALUES ('usp_TransformSales', 'Silver', @StartTime, GETDATE(), @RowCount, 'Success');
    END TRY
    BEGIN CATCH
        -- Log failure
        INSERT INTO dbo.ETL_AuditLog (ProcedureName, LayerName, StartTime, EndTime, Status, ErrorMessage)
        VALUES ('usp_TransformSales', 'Silver', @StartTime, GETDATE(), 'Failed', ERROR_MESSAGE());
        
        THROW;
    END CATCH;
END;
```

This skill provides comprehensive guidance for implementing and extending the Retail ETL Medallion Pipeline with real-world business logic and production-ready patterns.
