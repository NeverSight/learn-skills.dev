---
name: harvard-artifacts-collection-etl-analytics
description: Build ETL pipelines and analytics dashboards for Harvard Art Museums API data using Python, SQL, and Streamlit
triggers:
  - how do I fetch Harvard Art Museums data
  - build an ETL pipeline for museum artifacts
  - create analytics dashboard with Streamlit and museum API
  - extract and transform Harvard artifacts data
  - set up SQL database for art collection data
  - query Harvard Art Museums API with pagination
  - visualize museum artifact data with Plotly
  - build data engineering pipeline for cultural heritage data
---

# Harvard Artifacts Collection ETL Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides a complete data engineering and analytics solution for the Harvard Art Museums API. It demonstrates ETL pipeline construction, relational database design, SQL analytics, and interactive visualization using Streamlit. The application extracts artifact metadata, transforms nested JSON into structured tables, loads data into SQL databases, and provides 20+ analytical queries with auto-generated visualizations.

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export HARVARD_API_KEY="your_api_key_here"
export DB_HOST="your_database_host"
export DB_USER="your_database_user"
export DB_PASSWORD="your_database_password"
export DB_NAME="your_database_name"
```

## Project Architecture

**API → ETL → SQL → Analytics → Visualization**

- **Data Source**: Harvard Art Museums API
- **ETL Engine**: Python (requests, pandas)
- **Database**: MySQL / TiDB Cloud
- **Visualization**: Streamlit + Plotly

## Getting Harvard API Key

1. Visit [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)
2. Register for a free API key
3. Store in environment variable: `HARVARD_API_KEY`

## Core Components

### 1. API Data Collection

Fetch artifacts with pagination and rate limiting:

```python
import requests
import time
import os

def fetch_artifacts(api_key, page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API with pagination"""
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")

# Collect multiple pages with rate limiting
def collect_artifacts(num_pages=10):
    api_key = os.getenv('HARVARD_API_KEY')
    all_artifacts = []
    
    for page in range(1, num_pages + 1):
        print(f"Fetching page {page}...")
        data = fetch_artifacts(api_key, page=page)
        all_artifacts.extend(data.get('records', []))
        time.sleep(1)  # Rate limiting
    
    return all_artifacts
```

### 2. ETL Pipeline

Transform nested JSON into relational tables:

```python
import pandas as pd
import json

def extract_artifact_metadata(artifacts):
    """Extract main artifact metadata"""
    metadata = []
    
    for artifact in artifacts:
        metadata.append({
            'objectid': artifact.get('objectid'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'period': artifact.get('period'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'division': artifact.get('division'),
            'dated': artifact.get('dated'),
            'description': artifact.get('description'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'creditline': artifact.get('creditline'),
            'accessionyear': artifact.get('accessionyear')
        })
    
    return pd.DataFrame(metadata)

def extract_artifact_media(artifacts):
    """Extract media/image data"""
    media = []
    
    for artifact in artifacts:
        objectid = artifact.get('objectid')
        images = artifact.get('images', [])
        
        for img in images:
            media.append({
                'objectid': objectid,
                'imageid': img.get('imageid'),
                'baseimageurl': img.get('baseimageurl'),
                'iiifbaseuri': img.get('iiifbaseuri'),
                'height': img.get('height'),
                'width': img.get('width'),
                'format': img.get('format')
            })
    
    return pd.DataFrame(media)

def extract_artifact_colors(artifacts):
    """Extract color palette data"""
    colors = []
    
    for artifact in artifacts:
        objectid = artifact.get('objectid')
        color_data = artifact.get('colors', [])
        
        for color in color_data:
            colors.append({
                'objectid': objectid,
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'hue': color.get('hue'),
                'percent': color.get('percent')
            })
    
    return pd.DataFrame(colors)

# Complete ETL process
def run_etl():
    print("Starting ETL pipeline...")
    
    # Extract
    artifacts = collect_artifacts(num_pages=5)
    
    # Transform
    df_metadata = extract_artifact_metadata(artifacts)
    df_media = extract_artifact_media(artifacts)
    df_colors = extract_artifact_colors(artifacts)
    
    print(f"Extracted {len(df_metadata)} artifacts")
    print(f"Extracted {len(df_media)} media records")
    print(f"Extracted {len(df_colors)} color records")
    
    return df_metadata, df_media, df_colors
```

### 3. Database Schema and Loading

```python
import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    """Create database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def create_tables(connection):
    """Create database schema"""
    cursor = connection.cursor()
    
    # Artifact metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifactmetadata (
        objectid INT PRIMARY KEY,
        title TEXT,
        culture VARCHAR(255),
        period VARCHAR(255),
        century VARCHAR(100),
        classification VARCHAR(255),
        department VARCHAR(255),
        division VARCHAR(255),
        dated VARCHAR(255),
        description TEXT,
        technique TEXT,
        medium TEXT,
        dimensions TEXT,
        creditline TEXT,
        accessionyear INT
    )
    """)
    
    # Artifact media table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifactmedia (
        id INT AUTO_INCREMENT PRIMARY KEY,
        objectid INT,
        imageid INT,
        baseimageurl TEXT,
        iiifbaseuri TEXT,
        height INT,
        width INT,
        format VARCHAR(50),
        FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
    )
    """)
    
    # Artifact colors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifactcolors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        objectid INT,
        color VARCHAR(100),
        spectrum VARCHAR(100),
        hue VARCHAR(100),
        percent FLOAT,
        FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
    )
    """)
    
    connection.commit()
    print("Tables created successfully")

def load_dataframe_to_sql(df, table_name, connection):
    """Batch insert dataframe into SQL table"""
    cursor = connection.cursor()
    
    # Prepare column names and placeholders
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Convert dataframe to list of tuples
    data = [tuple(x) for x in df.to_numpy()]
    
    # Batch insert
    cursor.executemany(insert_query, data)
    connection.commit()
    
    print(f"Loaded {len(df)} records into {table_name}")

# Complete load process
def load_to_database(df_metadata, df_media, df_colors):
    connection = get_db_connection()
    
    create_tables(connection)
    
    load_dataframe_to_sql(df_metadata, 'artifactmetadata', connection)
    load_dataframe_to_sql(df_media, 'artifactmedia', connection)
    load_dataframe_to_sql(df_colors, 'artifactcolors', connection)
    
    connection.close()
    print("Data loading complete!")
```

### 4. SQL Analytics Queries

```python
def execute_query(query, connection):
    """Execute SQL query and return results as DataFrame"""
    return pd.read_sql(query, connection)

# Sample analytical queries
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 10
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Top Departments": """
        SELECT department, COUNT(*) as total_artifacts
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY total_artifacts DESC
        LIMIT 10
    """,
    
    "Media Availability": """
        SELECT 
            CASE WHEN m.objectid IS NOT NULL THEN 'Has Media' ELSE 'No Media' END as media_status,
            COUNT(*) as count
        FROM artifactmetadata a
        LEFT JOIN artifactmedia m ON a.objectid = m.objectid
        GROUP BY media_status
    """,
    
    "Color Distribution": """
        SELECT color, COUNT(*) as frequency, AVG(percent) as avg_percent
        FROM artifactcolors
        GROUP BY color
        ORDER BY frequency DESC
        LIMIT 15
    """,
    
    "Artifacts by Classification": """
        SELECT classification, COUNT(*) as count
        FROM artifactmetadata
        WHERE classification IS NOT NULL
        GROUP BY classification
        ORDER BY count DESC
        LIMIT 10
    """,
    
    "Average Image Dimensions": """
        SELECT 
            AVG(height) as avg_height,
            AVG(width) as avg_width,
            COUNT(*) as total_images
        FROM artifactmedia
    """
}
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    st.markdown("### ETL Pipeline & Analytics Application")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # ETL Section
    st.header("📊 ETL Pipeline")
    
    if st.button("Run ETL Pipeline"):
        with st.spinner("Running ETL..."):
            df_metadata, df_media, df_colors = run_etl()
            load_to_database(df_metadata, df_media, df_colors)
            st.success("ETL pipeline completed successfully!")
    
    # Analytics Section
    st.header("📈 Analytics Queries")
    
    query_name = st.selectbox("Select Query", list(ANALYTICS_QUERIES.keys()))
    
    if st.button("Execute Query"):
        connection = get_db_connection()
        query = ANALYTICS_QUERIES[query_name]
        
        with st.spinner("Executing query..."):
            results = execute_query(query, connection)
            
            st.subheader("Query Results")
            st.dataframe(results)
            
            # Auto-generate visualization
            if len(results.columns) >= 2:
                fig = px.bar(
                    results,
                    x=results.columns[0],
                    y=results.columns[1],
                    title=query_name
                )
                st.plotly_chart(fig)
        
        connection.close()

if __name__ == "__main__":
    main()
```

## Running the Application

```bash
# Start Streamlit dashboard
streamlit run app.py

# Access at http://localhost:8501
```

## Common Patterns

### Incremental Data Loading

```python
def get_max_objectid(connection):
    """Get the latest objectid to avoid duplicates"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(objectid) FROM artifactmetadata")
    result = cursor.fetchone()[0]
    return result if result else 0

def incremental_etl():
    """Only fetch new artifacts"""
    connection = get_db_connection()
    max_id = get_max_objectid(connection)
    
    # Fetch artifacts with objectid > max_id
    # ... implement filtering logic
    
    connection.close()
```

### Error Handling and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_etl():
    """ETL with error handling"""
    try:
        artifacts = collect_artifacts(num_pages=5)
        df_metadata, df_media, df_colors = run_etl()
        load_to_database(df_metadata, df_media, df_colors)
        logger.info("ETL completed successfully")
    except Exception as e:
        logger.error(f"ETL failed: {str(e)}")
        raise
```

## Troubleshooting

**API Rate Limiting**: Add `time.sleep(1)` between requests or reduce page size

**Database Connection Errors**: Verify environment variables and database credentials

**Missing Data**: Check API response structure; use `.get()` with defaults for optional fields

**Memory Issues**: Process data in smaller batches; use chunked DataFrame operations

**Foreign Key Violations**: Ensure parent records exist before inserting child records; use transactions

This skill enables AI agents to help developers build complete data engineering pipelines from API to analytics dashboard.
