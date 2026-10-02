---
name: harvard-artifacts-data-engineering-pipeline
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API with SQL storage and Streamlit visualization
triggers:
  - how do I build an ETL pipeline with the Harvard Art Museums API
  - set up a data engineering project with Harvard artifacts collection
  - create analytics dashboard for museum artifact data
  - extract and load Harvard museum data into SQL database
  - build a Streamlit app for artifact data visualization
  - implement ETL pipeline for art museum collections
  - analyze Harvard Art Museums data with SQL queries
  - process Harvard artifacts API data with Python
---

# Harvard Artifacts Data Engineering Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides an end-to-end data engineering solution for collecting, transforming, storing, and analyzing artifact data from the Harvard Art Museums API. It demonstrates production-ready ETL pipelines, relational database design, SQL analytics, and interactive Streamlit dashboards.

## What This Project Does

- **API Integration**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extracts nested JSON, transforms into relational schema, loads into SQL database
- **Database Design**: Implements normalized tables (artifactmetadata, artifactmedia, artifactcolors)
- **SQL Analytics**: Executes 20+ predefined analytical queries
- **Visualization**: Interactive Plotly charts rendered through Streamlit

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

### Required Dependencies

```txt
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### API Key Setup

Get your API key from [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api).

Create a `.env` file:

```bash
HARVARD_API_KEY=your_api_key_here
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

### Database Setup

The project uses MySQL or TiDB Cloud. Create the database schema:

```sql
CREATE DATABASE harvard_artifacts;
USE harvard_artifacts;

CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    period VARCHAR(200),
    century VARCHAR(100),
    division VARCHAR(200),
    department VARCHAR(200),
    classification VARCHAR(200),
    technique VARCHAR(500),
    medium VARCHAR(500),
    url VARCHAR(500),
    dated VARCHAR(200)
);

CREATE TABLE artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    media_url VARCHAR(1000),
    media_type VARCHAR(100),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

CREATE TABLE artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_hex VARCHAR(10),
    color_percent FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Core Components

### ETL Pipeline

#### Extract: Fetch Data from API

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API"""
    api_key = os.getenv('HARVARD_API_KEY')
    url = f"https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.status_code}")

# Fetch multiple pages
def fetch_all_artifacts(max_pages=10):
    """Fetch artifacts with pagination"""
    all_records = []
    
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        data = fetch_artifacts(page=page)
        all_records.extend(data.get('records', []))
        
        # Check if more pages available
        if not data.get('info', {}).get('next'):
            break
    
    return all_records
```

#### Transform: Process JSON to Relational Data

```python
import pandas as pd

def transform_artifacts(raw_data):
    """Transform nested JSON to relational dataframes"""
    
    # Metadata table
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in raw_data:
        # Extract metadata
        metadata_records.append({
            'id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'period': artifact.get('period'),
            'century': artifact.get('century'),
            'division': artifact.get('division'),
            'department': artifact.get('department'),
            'classification': artifact.get('classification'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'url': artifact.get('url'),
            'dated': artifact.get('dated')
        })
        
        # Extract media
        for image in artifact.get('images', []):
            media_records.append({
                'artifact_id': artifact.get('id'),
                'media_url': image.get('baseimageurl'),
                'media_type': 'image'
            })
        
        # Extract colors
        for color in artifact.get('colors', []):
            color_records.append({
                'artifact_id': artifact.get('id'),
                'color_hex': color.get('hex'),
                'color_percent': color.get('percent')
            })
    
    return {
        'metadata': pd.DataFrame(metadata_records),
        'media': pd.DataFrame(media_records),
        'colors': pd.DataFrame(color_records)
    }
```

#### Load: Insert into SQL Database

```python
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def load_to_database(dataframes):
    """Load transformed data to SQL database"""
    connection = create_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Load metadata
        for _, row in dataframes['metadata'].iterrows():
            query = """
                INSERT INTO artifactmetadata 
                (id, title, culture, period, century, division, department, 
                 classification, technique, medium, url, dated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE title=VALUES(title)
            """
            cursor.execute(query, tuple(row))
        
        # Load media
        for _, row in dataframes['media'].iterrows():
            query = """
                INSERT INTO artifactmedia (artifact_id, media_url, media_type)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, tuple(row))
        
        # Load colors
        for _, row in dataframes['colors'].iterrows():
            query = """
                INSERT INTO artifactcolors (artifact_id, color_hex, color_percent)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, tuple(row))
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"Error loading data: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()
```

### Complete ETL Workflow

```python
def run_etl_pipeline(max_pages=5):
    """Execute complete ETL pipeline"""
    print("Starting ETL pipeline...")
    
    # Extract
    print("Extracting data from API...")
    raw_data = fetch_all_artifacts(max_pages=max_pages)
    print(f"Extracted {len(raw_data)} artifacts")
    
    # Transform
    print("Transforming data...")
    dataframes = transform_artifacts(raw_data)
    print(f"Transformed into {len(dataframes['metadata'])} metadata records")
    
    # Load
    print("Loading data to database...")
    success = load_to_database(dataframes)
    
    if success:
        print("ETL pipeline completed successfully!")
    else:
        print("ETL pipeline failed!")
    
    return success
```

## SQL Analytics Queries

### Sample Analytical Queries

```python
# Query 1: Top 10 cultures by artifact count
query_cultures = """
SELECT culture, COUNT(*) as artifact_count
FROM artifactmetadata
WHERE culture IS NOT NULL
GROUP BY culture
ORDER BY artifact_count DESC
LIMIT 10
"""

# Query 2: Artifacts by century
query_century = """
SELECT century, COUNT(*) as count
FROM artifactmetadata
WHERE century IS NOT NULL
GROUP BY century
ORDER BY count DESC
"""

# Query 3: Department distribution
query_departments = """
SELECT department, COUNT(*) as total_artifacts
FROM artifactmetadata
WHERE department IS NOT NULL
GROUP BY department
ORDER BY total_artifacts DESC
"""

# Query 4: Media availability
query_media = """
SELECT 
    CASE 
        WHEN media_count > 0 THEN 'Has Media'
        ELSE 'No Media'
    END as media_status,
    COUNT(*) as artifact_count
FROM (
    SELECT a.id, COUNT(m.id) as media_count
    FROM artifactmetadata a
    LEFT JOIN artifactmedia m ON a.id = m.artifact_id
    GROUP BY a.id
) as media_stats
GROUP BY media_status
"""

# Query 5: Top colors used
query_colors = """
SELECT color_hex, COUNT(*) as usage_count, AVG(color_percent) as avg_percent
FROM artifactcolors
GROUP BY color_hex
ORDER BY usage_count DESC
LIMIT 10
"""

# Query 6: Classification distribution
query_classification = """
SELECT classification, COUNT(*) as count
FROM artifactmetadata
WHERE classification IS NOT NULL
GROUP BY classification
ORDER BY count DESC
LIMIT 15
"""
```

### Execute Queries

```python
def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    connection = create_connection()
    if not connection:
        return None
    
    try:
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        print(f"Query execution error: {e}")
        return None
    finally:
        connection.close()
```

## Streamlit Dashboard

### Main Application

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

st.title("🏛️ Harvard Art Museums - Data Analytics Dashboard")
st.markdown("---")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select Page",
    ["ETL Pipeline", "SQL Analytics", "Visualizations"]
)

if page == "ETL Pipeline":
    st.header("📥 ETL Pipeline")
    
    max_pages = st.slider("Number of pages to fetch", 1, 20, 5)
    
    if st.button("Run ETL Pipeline"):
        with st.spinner("Running ETL pipeline..."):
            success = run_etl_pipeline(max_pages=max_pages)
            
        if success:
            st.success("ETL pipeline completed successfully!")
        else:
            st.error("ETL pipeline failed. Check logs.")

elif page == "SQL Analytics":
    st.header("📊 SQL Analytics")
    
    # Query selector
    queries = {
        "Top Cultures": query_cultures,
        "Century Distribution": query_century,
        "Department Stats": query_departments,
        "Media Availability": query_media,
        "Color Usage": query_colors,
        "Classifications": query_classification
    }
    
    selected_query = st.selectbox("Select Query", list(queries.keys()))
    
    if st.button("Execute Query"):
        with st.spinner("Executing query..."):
            df = execute_query(queries[selected_query])
        
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Auto-generate visualization
            if len(df.columns) >= 2:
                fig = px.bar(
                    df, 
                    x=df.columns[0], 
                    y=df.columns[1],
                    title=f"{selected_query} Analysis"
                )
                st.plotly_chart(fig, use_container_width=True)

elif page == "Visualizations":
    st.header("📈 Data Visualizations")
    
    # Culture distribution
    df_culture = execute_query(query_cultures)
    if df_culture is not None:
        fig1 = px.bar(df_culture, x='culture', y='artifact_count',
                     title='Top 10 Cultures by Artifact Count')
        st.plotly_chart(fig1, use_container_width=True)
    
    # Century timeline
    df_century = execute_query(query_century)
    if df_century is not None:
        fig2 = px.line(df_century, x='century', y='count',
                      title='Artifacts Across Centuries')
        st.plotly_chart(fig2, use_container_width=True)
```

## Common Patterns

### Batch Processing with Rate Limiting

```python
import time

def fetch_with_rate_limit(pages, delay=1):
    """Fetch data with rate limiting"""
    results = []
    
    for page in range(1, pages + 1):
        data = fetch_artifacts(page=page)
        results.extend(data.get('records', []))
        
        # Rate limiting
        if page < pages:
            time.sleep(delay)
    
    return results
```

### Error Handling in ETL

```python
def safe_etl_pipeline(max_pages=5):
    """ETL pipeline with comprehensive error handling"""
    try:
        raw_data = fetch_all_artifacts(max_pages=max_pages)
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False
    
    try:
        dataframes = transform_artifacts(raw_data)
    except Exception as e:
        print(f"Transformation failed: {e}")
        return False
    
    try:
        success = load_to_database(dataframes)
        return success
    except Exception as e:
        print(f"Loading failed: {e}")
        return False
```

## Running the Application

```bash
# Start Streamlit app
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Troubleshooting

### API Connection Issues

```python
# Test API connection
def test_api_connection():
    try:
        data = fetch_artifacts(page=1, size=1)
        print("API connection successful!")
        return True
    except Exception as e:
        print(f"API connection failed: {e}")
        print("Check your API key in .env file")
        return False
```

### Database Connection Issues

```python
# Test database connection
def test_db_connection():
    connection = create_connection()
    if connection:
        print("Database connection successful!")
        connection.close()
        return True
    else:
        print("Database connection failed!")
        print("Check DB credentials in .env file")
        return False
```

### Common Error: Empty Results

```python
# Verify data in database
def check_data_exists():
    query = "SELECT COUNT(*) as total FROM artifactmetadata"
    df = execute_query(query)
    
    if df is not None:
        total = df['total'].iloc[0]
        print(f"Total artifacts in database: {total}")
        return total > 0
    return False
```

This skill enables AI agents to guide developers through building production-ready data engineering pipelines using the Harvard Art Museums API with proper ETL practices, SQL analytics, and interactive visualizations.
