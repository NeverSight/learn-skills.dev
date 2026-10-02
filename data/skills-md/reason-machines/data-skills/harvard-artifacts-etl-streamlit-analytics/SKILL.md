---
name: harvard-artifacts-etl-streamlit-analytics
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API data with Python, SQL, and Streamlit
triggers:
  - how do I build an ETL pipeline with Harvard Art Museums API
  - create a Streamlit dashboard for Harvard artifacts data
  - set up SQL database for Harvard museum collections
  - extract and transform Harvard Art Museums API data
  - build analytics app with museum artifact data
  - query and visualize Harvard museum collection data
  - implement data pipeline for art museum API
  - create artifact analytics with Python and SQL
---

# Harvard Artifacts ETL & Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI coding agents to help developers build end-to-end data engineering and analytics applications using the Harvard Art Museums API. The project demonstrates ETL pipelines, SQL database design, analytical queries, and interactive Streamlit visualizations for museum artifact data.

## What This Project Does

The Harvard Artifacts Collection Data Engineering & Analytics App provides:
- **API Integration**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load artifact metadata, media, and color data into relational SQL tables
- **SQL Analytics**: Pre-built analytical queries for insights on culture, century, media availability, and color patterns
- **Interactive Dashboard**: Streamlit-based UI with Plotly visualizations for query results

## Installation

### Prerequisites
- Python 3.8+
- MySQL or TiDB Cloud database
- Harvard Art Museums API key (get from https://docs.harvardartmuseums.org/api-docs/)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export HARVARD_API_KEY="your_api_key_here"
export DB_HOST="your_db_host"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"
export DB_NAME="harvard_artifacts"

# Run the Streamlit app
streamlit run app.py
```

### Dependencies (requirements.txt)
```txt
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### Database Connection

```python
import mysql.connector
import os

def get_db_connection():
    """Create database connection using environment variables"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'harvard_artifacts'),
        port=int(os.getenv('DB_PORT', 3306))
    )
```

### API Configuration

```python
import os

API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"
```

## Database Schema

### Create Tables

```sql
-- Artifact Metadata Table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    division VARCHAR(255),
    department VARCHAR(255),
    dated VARCHAR(255),
    accessionyear INT,
    url VARCHAR(500)
);

-- Artifact Media Table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    baseimageurl VARCHAR(500),
    iiifbaseuri VARCHAR(500),
    primaryimageurl VARCHAR(500),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact Colors Table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    hue VARCHAR(50),
    percent FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## ETL Pipeline Implementation

### Extract: Fetch Data from API

```python
import requests
import time

def fetch_artifacts(api_key, num_pages=5, page_size=100):
    """
    Fetch artifact data from Harvard Art Museums API with pagination
    
    Args:
        api_key: Harvard API key
        num_pages: Number of pages to fetch
        page_size: Records per page (max 100)
    
    Returns:
        List of artifact records
    """
    artifacts = []
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': api_key,
            'size': page_size,
            'page': page
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            artifacts.extend(data.get('records', []))
            print(f"Fetched page {page}/{num_pages}")
            
            # Rate limiting: API allows 2500 requests/day
            time.sleep(0.5)
        else:
            print(f"Error fetching page {page}: {response.status_code}")
            break
    
    return artifacts
```

### Transform: Clean and Structure Data

```python
import pandas as pd

def transform_artifacts(raw_data):
    """
    Transform raw API data into structured dataframes
    
    Returns:
        Tuple of (metadata_df, media_df, colors_df)
    """
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_data:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title', '')[:500],
            'culture': artifact.get('culture', '')[:255],
            'century': artifact.get('century', '')[:100],
            'classification': artifact.get('classification', '')[:255],
            'division': artifact.get('division', '')[:255],
            'department': artifact.get('department', '')[:255],
            'dated': artifact.get('dated', '')[:255],
            'accessionyear': artifact.get('accessionyear'),
            'url': artifact.get('url', '')[:500]
        }
        metadata_list.append(metadata)
        
        # Extract media information
        if artifact.get('primaryimageurl') or artifact.get('baseimageurl'):
            media = {
                'artifact_id': artifact.get('id'),
                'baseimageurl': artifact.get('baseimageurl', '')[:500],
                'iiifbaseuri': artifact.get('iiifbaseuri', '')[:500],
                'primaryimageurl': artifact.get('primaryimageurl', '')[:500]
            }
            media_list.append(media)
        
        # Extract color data
        for color_obj in artifact.get('colors', []):
            color = {
                'artifact_id': artifact.get('id'),
                'color': color_obj.get('color', '')[:50],
                'spectrum': color_obj.get('spectrum', '')[:50],
                'hue': color_obj.get('hue', '')[:50],
                'percent': color_obj.get('percent')
            }
            colors_list.append(color)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### Load: Insert into SQL Database

```python
def load_to_database(metadata_df, media_df, colors_df, connection):
    """
    Load transformed data into SQL database using batch inserts
    """
    cursor = connection.cursor()
    
    # Insert metadata
    metadata_query = """
        INSERT INTO artifactmetadata 
        (id, title, culture, century, classification, division, department, dated, accessionyear, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
    """
    cursor.executemany(metadata_query, metadata_df.values.tolist())
    
    # Insert media
    media_query = """
        INSERT INTO artifactmedia (artifact_id, baseimageurl, iiifbaseuri, primaryimageurl)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(media_query, media_df.values.tolist())
    
    # Insert colors
    colors_query = """
        INSERT INTO artifactcolors (artifact_id, color, spectrum, hue, percent)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(colors_query, colors_df.values.tolist())
    
    connection.commit()
    cursor.close()
    print(f"Loaded {len(metadata_df)} artifacts, {len(media_df)} media records, {len(colors_df)} color records")
```

## Analytics Queries

### Sample Analytical Queries

```python
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL AND culture != ''
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 20
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL AND century != ''
        GROUP BY century
        ORDER BY count DESC
        LIMIT 15
    """,
    
    "Media Availability": """
        SELECT 
            COUNT(DISTINCT m.artifact_id) as with_media,
            (SELECT COUNT(*) FROM artifactmetadata) as total_artifacts,
            ROUND(COUNT(DISTINCT m.artifact_id) * 100.0 / 
                  (SELECT COUNT(*) FROM artifactmetadata), 2) as percentage
        FROM artifactmedia m
    """,
    
    "Top Colors Used": """
        SELECT color, COUNT(*) as count, AVG(percent) as avg_percent
        FROM artifactcolors
        WHERE color IS NOT NULL
        GROUP BY color
        ORDER BY count DESC
        LIMIT 20
    """,
    
    "Department Distribution": """
        SELECT department, COUNT(*) as count
        FROM artifactmetadata
        WHERE department IS NOT NULL AND department != ''
        GROUP BY department
        ORDER BY count DESC
    """,
    
    "Artifacts with Images by Century": """
        SELECT am.century, COUNT(DISTINCT am.id) as artifact_count
        FROM artifactmetadata am
        JOIN artifactmedia media ON am.id = media.artifact_id
        WHERE am.century IS NOT NULL AND media.primaryimageurl IS NOT NULL
        GROUP BY am.century
        ORDER BY artifact_count DESC
        LIMIT 15
    """
}

def execute_query(query, connection):
    """Execute SQL query and return DataFrame"""
    return pd.read_sql(query, connection)
```

## Streamlit Dashboard Implementation

### Basic App Structure

```python
import streamlit as st
import plotly.express as px

def main():
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Select Page",
        ["Data Collection", "Analytics", "Visualizations"]
    )
    
    if page == "Data Collection":
        show_data_collection_page()
    elif page == "Analytics":
        show_analytics_page()
    else:
        show_visualizations_page()

def show_data_collection_page():
    """Page for ETL operations"""
    st.header("Data Collection & ETL")
    
    api_key = st.text_input("Harvard API Key", type="password", 
                            value=os.getenv('HARVARD_API_KEY', ''))
    num_pages = st.slider("Number of pages to fetch", 1, 10, 5)
    
    if st.button("Run ETL Pipeline"):
        with st.spinner("Fetching data from API..."):
            raw_data = fetch_artifacts(api_key, num_pages)
            st.success(f"Fetched {len(raw_data)} artifacts")
        
        with st.spinner("Transforming data..."):
            metadata_df, media_df, colors_df = transform_artifacts(raw_data)
            st.success("Data transformed")
        
        with st.spinner("Loading to database..."):
            conn = get_db_connection()
            load_to_database(metadata_df, media_df, colors_df, conn)
            conn.close()
            st.success("Data loaded to database")

def show_analytics_page():
    """Page for running SQL queries"""
    st.header("SQL Analytics")
    
    query_name = st.selectbox("Select Query", list(ANALYTICS_QUERIES.keys()))
    
    if st.button("Run Query"):
        conn = get_db_connection()
        df = execute_query(ANALYTICS_QUERIES[query_name], conn)
        conn.close()
        
        st.dataframe(df)
        
        # Auto-generate visualization
        if len(df.columns) == 2 and 'count' in df.columns.str.lower():
            fig = px.bar(df, x=df.columns[0], y='count', 
                        title=query_name)
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
```

## Common Patterns

### Pattern: Incremental Data Loading

```python
def get_last_artifact_id(connection):
    """Get the highest artifact ID already in database"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM artifactmetadata")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] else 0

def fetch_new_artifacts_only(api_key, last_id):
    """Fetch only artifacts newer than last_id"""
    params = {
        'apikey': api_key,
        'size': 100,
        'sort': 'id',
        'sortorder': 'asc',
        'q': f'id:>{last_id}'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json().get('records', [])
```

### Pattern: Data Validation

```python
def validate_artifact_data(df):
    """Validate artifact metadata before loading"""
    required_cols = ['id', 'title']
    
    # Check required columns exist
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Check for null IDs
    if df['id'].isnull().any():
        raise ValueError("Found null artifact IDs")
    
    # Check for duplicates
    duplicates = df[df.duplicated(subset=['id'], keep=False)]
    if not duplicates.empty:
        st.warning(f"Found {len(duplicates)} duplicate artifact IDs")
    
    return True
```

## Troubleshooting

### API Rate Limiting
```python
# Problem: HTTP 429 errors from API
# Solution: Add exponential backoff

import time
from requests.exceptions import RequestException

def fetch_with_retry(url, params, max_retries=3):
    """Fetch with exponential backoff on rate limit"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            return response
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None
```

### Database Connection Issues
```python
# Problem: Lost database connections
# Solution: Use connection pooling

from mysql.connector import pooling

db_pool = pooling.MySQLConnectionPool(
    pool_name="harvard_pool",
    pool_size=5,
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

def get_pooled_connection():
    """Get connection from pool"""
    return db_pool.get_connection()
```

### Memory Issues with Large Datasets
```python
# Problem: Out of memory with large API responses
# Solution: Process in chunks

def load_artifacts_in_chunks(metadata_df, chunk_size=1000):
    """Load data in chunks to avoid memory issues"""
    conn = get_db_connection()
    
    for start_idx in range(0, len(metadata_df), chunk_size):
        end_idx = min(start_idx + chunk_size, len(metadata_df))
        chunk = metadata_df.iloc[start_idx:end_idx]
        
        cursor = conn.cursor()
        cursor.executemany(metadata_query, chunk.values.tolist())
        conn.commit()
        cursor.close()
        
        print(f"Loaded chunk {start_idx}-{end_idx}")
    
    conn.close()
```

### Handling Missing Data
```python
# Problem: NULL values breaking queries
# Solution: Use COALESCE and proper NULL handling

def clean_dataframe(df):
    """Clean dataframe before loading"""
    # Replace empty strings with None for SQL NULL
    df = df.replace('', None)
    
    # Fill NaN values appropriately
    if 'accessionyear' in df.columns:
        df['accessionyear'] = df['accessionyear'].fillna(0).astype(int)
    
    # Truncate long strings
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str[:500]
    
    return df
```

This skill provides comprehensive guidance for building ETL pipelines and analytics dashboards with the Harvard Art Museums API, enabling AI agents to assist developers in data engineering projects.
