---
name: enterprise-data-engineering-pipeline-ssis-pyspark
description: End-to-end ELT pipeline using SSIS, SQL Server, and PySpark for enterprise data warehousing and analytics
triggers:
  - "set up an enterprise ETL pipeline with SSIS"
  - "create a star schema data warehouse in SQL Server"
  - "build a data engineering pipeline with SSIS and PySpark"
  - "implement ETL with SQL Server Integration Services"
  - "process enterprise data with PySpark analytics"
  - "design a fact and dimension table warehouse"
  - "run data quality audits on SQL Server warehouse"
  - "scale data processing with PySpark for millions of rows"
---

# Enterprise Data Engineering Pipeline (SSIS + PySpark)

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project provides a complete enterprise data engineering solution that combines:
- **SSIS (SQL Server Integration Services)** for ETL orchestration
- **SQL Server** with Star Schema data warehouse design (fact and dimension tables)
- **Python (Pandas)** for data quality audits and visualization
- **PySpark** for big data analytics and aggregation

The pipeline ingests raw CSV files (Sales, Products, Customers), transforms them through SSIS, loads into a dimensional model, and performs analytics at scale.

## Architecture Components

1. **Source Layer**: Raw CSV files containing transactional and master data
2. **ETL Layer**: SSIS packages handle extraction, transformation, error handling
3. **Storage Layer**: SQL Server Data Warehouse with Star Schema
4. **Analytics Layer**: Python/PySpark scripts for business intelligence

## Installation & Setup

### Prerequisites

```bash
# Required software
- SQL Server 2019+ (Developer or Enterprise Edition)
- SQL Server Integration Services (SSIS)
- Visual Studio with SQL Server Data Tools (SSDT)
- Python 3.10+
- Java 8+ (for PySpark)
```

### Python Dependencies

```bash
pip install pandas sqlalchemy pyodbc pyspark matplotlib
```

### Database Setup

```sql
-- 01_Schema_Setup.sql
-- Create the data warehouse database
CREATE DATABASE EnterpriseDataWarehouse;
GO

USE EnterpriseDataWarehouse;
GO

-- Dimension: Customers
CREATE TABLE dim_Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(100),
    Email NVARCHAR(100),
    Region NVARCHAR(50),
    RegistrationDate DATE
);

-- Dimension: Products
CREATE TABLE dim_Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Category NVARCHAR(50),
    UnitPrice DECIMAL(10, 2)
);

-- Fact: Sales
CREATE TABLE fact_Sales (
    SaleID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES dim_Customers(CustomerID),
    ProductID INT FOREIGN KEY REFERENCES dim_Products(ProductID),
    Quantity INT,
    SaleDate DATE,
    TotalAmount DECIMAL(10, 2)
);

-- Business Intelligence View: Revenue by Product
CREATE VIEW vw_RevenueByProduct AS
SELECT 
    p.ProductName,
    p.Category,
    SUM(s.TotalAmount) AS TotalRevenue,
    SUM(s.Quantity) AS TotalQuantity
FROM fact_Sales s
INNER JOIN dim_Products p ON s.ProductID = p.ProductID
GROUP BY p.ProductName, p.Category;

-- Business Intelligence View: Customer Lifetime Value
CREATE VIEW vw_CustomerLTV AS
SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Region,
    COUNT(s.SaleID) AS TotalPurchases,
    SUM(s.TotalAmount) AS LifetimeValue
FROM dim_Customers c
LEFT JOIN fact_Sales s ON c.CustomerID = s.CustomerID
GROUP BY c.CustomerID, c.CustomerName, c.Region;
```

## SSIS Package Configuration

### Creating the SSIS Project

1. Open Visual Studio with SSDT
2. Create new Integration Services Project: `EnterpriseETL.sln`
3. Add Connection Managers:
   - **Source_FlatFile**: Points to CSV directory
   - **Destination_OLEDB**: SQL Server connection string

### SSIS Package Flow

```xml
<!-- Key SSIS Components -->
<!-- Data Flow Task: Load dim_Customers -->
- Flat File Source (Customers.csv)
- Data Conversion (handle Unicode, trim strings)
- Derived Column (add audit columns)
- OLEDB Destination (dim_Customers)

<!-- Data Flow Task: Load dim_Products -->
- Flat File Source (Products.csv)
- Data Conversion (decimal precision for prices)
- OLEDB Destination (dim_Products)

<!-- Data Flow Task: Load fact_Sales -->
- Flat File Source (Sales.csv)
- Lookup Transformation (validate CustomerID, ProductID)
- Derived Column (calculate TotalAmount = Quantity * UnitPrice)
- OLEDB Destination (fact_Sales)
```

### Error Handling in SSIS

```sql
-- Create error logging table
CREATE TABLE ETL_ErrorLog (
    ErrorID INT IDENTITY(1,1) PRIMARY KEY,
    PackageName NVARCHAR(100),
    TaskName NVARCHAR(100),
    ErrorDescription NVARCHAR(MAX),
    ErrorDate DATETIME DEFAULT GETDATE()
);
```

## Python Analytics

### Data Quality Audit Script

```python
# project_audit.py
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Database connection
def get_connection():
    conn_str = (
        "mssql+pyodbc:///?odbc_connect="
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        "Trusted_Connection=yes;"
    )
    return create_engine(conn_str)

# Data Quality Checks
def run_audit():
    engine = get_connection()
    
    # Check 1: Null values in critical columns
    query_nulls = """
    SELECT 
        'dim_Customers' AS TableName,
        SUM(CASE WHEN CustomerName IS NULL THEN 1 ELSE 0 END) AS NullCustomerName,
        SUM(CASE WHEN Email IS NULL THEN 1 ELSE 0 END) AS NullEmail
    FROM dim_Customers
    UNION ALL
    SELECT 
        'fact_Sales',
        SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END),
        SUM(CASE WHEN ProductID IS NULL THEN 1 ELSE 0 END)
    FROM fact_Sales
    """
    df_nulls = pd.read_sql(query_nulls, engine)
    print("Null Value Audit:")
    print(df_nulls)
    
    # Check 2: Orphaned records (referential integrity)
    query_orphans = """
    SELECT COUNT(*) AS OrphanedSales
    FROM fact_Sales s
    WHERE NOT EXISTS (SELECT 1 FROM dim_Customers c WHERE c.CustomerID = s.CustomerID)
       OR NOT EXISTS (SELECT 1 FROM dim_Products p WHERE p.ProductID = s.ProductID)
    """
    df_orphans = pd.read_sql(query_orphans, engine)
    print("\nOrphaned Records:")
    print(df_orphans)
    
    # Check 3: Revenue distribution
    query_revenue = "SELECT * FROM vw_RevenueByProduct ORDER BY TotalRevenue DESC"
    df_revenue = pd.read_sql(query_revenue, engine)
    
    # Visualization
    plt.figure(figsize=(10, 6))
    plt.bar(df_revenue['ProductName'][:10], df_revenue['TotalRevenue'][:10])
    plt.xlabel('Product')
    plt.ylabel('Total Revenue')
    plt.title('Top 10 Products by Revenue')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('revenue_analysis.png')
    print("\nRevenue chart saved to revenue_analysis.png")

if __name__ == "__main__":
    run_audit()
```

### Customer Segmentation Analysis

```python
# customer_segmentation.py
import pandas as pd
from sqlalchemy import create_engine
import os

def segment_customers():
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect="
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        f"Trusted_Connection=yes;"
    )
    
    # Load customer LTV data
    df = pd.read_sql("SELECT * FROM vw_CustomerLTV", engine)
    
    # RFM-style segmentation
    df['Segment'] = pd.cut(
        df['LifetimeValue'],
        bins=[0, 1000, 5000, float('inf')],
        labels=['Bronze', 'Silver', 'Gold']
    )
    
    # Aggregate by segment
    segment_summary = df.groupby('Segment').agg({
        'CustomerID': 'count',
        'LifetimeValue': 'sum',
        'TotalPurchases': 'mean'
    }).reset_index()
    
    print(segment_summary)
    return segment_summary
```

## PySpark Big Data Processing

### High-Volume Sales Aggregation

```python
# pyspark_analytics.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count, avg, year, month
import os

# Initialize Spark
spark = SparkSession.builder \
    .appName("EnterpriseSalesAnalytics") \
    .config("spark.jars", "mssql-jdbc-9.4.0.jre8.jar") \
    .getOrCreate()

# JDBC connection properties
jdbc_url = f"jdbc:sqlserver://{os.getenv('SQL_SERVER')}:1433;databaseName={os.getenv('SQL_DATABASE')}"
connection_properties = {
    "user": os.getenv('SQL_USER'),
    "password": os.getenv('SQL_PASSWORD'),
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Load data from SQL Server
df_sales = spark.read.jdbc(
    url=jdbc_url,
    table="fact_Sales",
    properties=connection_properties
)

df_customers = spark.read.jdbc(
    url=jdbc_url,
    table="dim_Customers",
    properties=connection_properties
)

df_products = spark.read.jdbc(
    url=jdbc_url,
    table="dim_Products",
    properties=connection_properties
)

# Join and aggregate
df_combined = df_sales \
    .join(df_customers, "CustomerID") \
    .join(df_products, "ProductID")

# Monthly revenue analysis
df_monthly = df_combined \
    .withColumn("Year", year(col("SaleDate"))) \
    .withColumn("Month", month(col("SaleDate"))) \
    .groupBy("Year", "Month", "Region") \
    .agg(
        _sum("TotalAmount").alias("MonthlyRevenue"),
        count("SaleID").alias("TransactionCount"),
        avg("TotalAmount").alias("AvgTransactionValue")
    ) \
    .orderBy("Year", "Month", "Region")

df_monthly.show(20)

# Write results back to SQL Server
df_monthly.write.jdbc(
    url=jdbc_url,
    table="analytics_MonthlyRevenue",
    mode="overwrite",
    properties=connection_properties
)

# Product performance by category
df_category = df_combined \
    .groupBy("Category") \
    .agg(
        _sum("TotalAmount").alias("CategoryRevenue"),
        _sum("Quantity").alias("TotalUnitsSold"),
        count("CustomerID").distinct().alias("UniqueCustomers")
    ) \
    .orderBy(col("CategoryRevenue").desc())

df_category.show()

spark.stop()
```

### Parallel Processing for Large Datasets

```python
# batch_processing.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder \
    .appName("BatchDataProcessing") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

# Read large CSV files
df_raw = spark.read.csv(
    "hdfs://data/sales/*.csv",
    header=True,
    inferSchema=True
)

# Data quality transformations
df_cleaned = df_raw \
    .filter(col("TotalAmount").isNotNull()) \
    .filter(col("Quantity") > 0) \
    .withColumn(
        "IsHighValue",
        when(col("TotalAmount") > 1000, "Yes").otherwise("No")
    ) \
    .dropDuplicates(["SaleID"])

# Partition by date for efficient querying
df_cleaned.write \
    .partitionBy("SaleDate") \
    .mode("overwrite") \
    .parquet("hdfs://data/processed/sales_cleaned")

print(f"Processed {df_cleaned.count()} records")
```

## Common Patterns

### Incremental ETL (Load Only New Records)

```sql
-- Create staging table
CREATE TABLE stg_Sales (
    SaleID INT,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    SaleDate DATE,
    TotalAmount DECIMAL(10, 2),
    LoadDate DATETIME DEFAULT GETDATE()
);

-- Merge statement for incremental load
MERGE INTO fact_Sales AS target
USING stg_Sales AS source
ON target.SaleID = source.SaleID
WHEN MATCHED THEN
    UPDATE SET
        Quantity = source.Quantity,
        TotalAmount = source.TotalAmount
WHEN NOT MATCHED THEN
    INSERT (SaleID, CustomerID, ProductID, Quantity, SaleDate, TotalAmount)
    VALUES (source.SaleID, source.CustomerID, source.ProductID, 
            source.Quantity, source.SaleDate, source.TotalAmount);
```

### Automated Data Refresh

```python
# scheduled_refresh.py
import subprocess
import os
from datetime import datetime

def run_ssis_package():
    """Execute SSIS package via dtexec"""
    package_path = r"C:\SSIS\EnterpriseETL\EnterpriseETL\Package.dtsx"
    
    cmd = [
        "dtexec",
        "/FILE", package_path,
        "/REPORTING", "E"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    log_file = f"etl_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_file, 'w') as f:
        f.write(result.stdout)
        f.write(result.stderr)
    
    return result.returncode == 0

def run_analytics():
    """Execute Python analytics after ETL"""
    subprocess.run(["python", "project_audit.py"])
    subprocess.run(["python", "pyspark_analytics.py"])

if __name__ == "__main__":
    if run_ssis_package():
        print("ETL completed successfully")
        run_analytics()
    else:
        print("ETL failed - check logs")
```

## Troubleshooting

### SSIS Connection Issues

```plaintext
Error: "Cannot acquire connection to SQL Server"
Solution:
1. Verify SQL Server service is running
2. Check Windows Authentication vs SQL Authentication
3. Update connection string in Connection Manager
4. Enable TCP/IP protocol in SQL Server Configuration Manager
```

### Unicode/Encoding Errors

```plaintext
Error: "Cannot convert between unicode and non-unicode string data types"
Solution in SSIS:
1. Add Data Conversion task
2. Convert DT_STR to DT_WSTR for Unicode columns
3. Set CodePage to 1252 (Windows Latin 1) in Flat File Connection
```

### PySpark JDBC Driver Not Found

```bash
# Download Microsoft JDBC driver
wget https://github.com/microsoft/mssql-jdbc/releases/download/v9.4.0/mssql-jdbc-9.4.0.jre8.jar

# Add to Spark session
spark = SparkSession.builder \
    .config("spark.jars", "/path/to/mssql-jdbc-9.4.0.jre8.jar") \
    .getOrCreate()
```

### Performance Optimization

```python
# Enable broadcast join for small dimension tables
from pyspark.sql.functions import broadcast

df_result = df_sales.join(
    broadcast(df_products),
    "ProductID"
)

# Cache frequently accessed DataFrames
df_sales.cache()
df_sales.count()  # Trigger caching
```

## Environment Variables

```bash
# .env file
SQL_SERVER=localhost
SQL_DATABASE=EnterpriseDataWarehouse
SQL_USER=your_username
SQL_PASSWORD=your_password

# For PySpark
SPARK_HOME=/path/to/spark
JAVA_HOME=/path/to/java
```

## Running the Complete Pipeline

```bash
# Step 1: Setup database
sqlcmd -S localhost -i 01_Schema_Setup.sql

# Step 2: Run SSIS package (via Visual Studio or dtexec)
dtexec /FILE "EnterpriseETL\Package.dtsx"

# Step 3: Run data quality audit
python project_audit.py

# Step 4: Run PySpark analytics
spark-submit --jars mssql-jdbc-9.4.0.jre8.jar pyspark_analytics.py
```

This enterprise pipeline provides a complete solution for data warehousing, ETL automation, and big data analytics using industry-standard Microsoft and Apache technologies.
