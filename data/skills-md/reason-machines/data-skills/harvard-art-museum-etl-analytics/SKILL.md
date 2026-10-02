---
name: harvard-art-museum-etl-analytics
description: Build end-to-end data engineering pipelines with Harvard Art Museums API, ETL workflows, SQL analytics, and Streamlit visualization.
triggers:
  - create an ETL pipeline for Harvard Art Museums data
  - build a data analytics app with Harvard API
  - fetch and analyze art museum artifacts
  - set up Harvard Art Museums API integration
  - create SQL analytics for museum collections
  - build streamlit dashboard for art data
  - extract Harvard museum data into database
  - analyze art artifacts with SQL queries
---

# Harvard Art Museum ETL Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables you to build end-to-end data engineering and analytics applications using the Harvard Art Museums API. The project demonstrates real-world ETL pipelines, SQL database design, analytical queries, and interactive Streamlit dashboards for artifact collections.

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App provides:

- **API Integration**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load artifact metadata, media, and color data into relational databases
- **SQL Analytics**: Pre-built analytical queries for insights on culture, century, media, colors, and departments
- **Visualization**: Interactive Plotly charts and Streamlit dashboards for data exploration
- **Database Design**: Properly structured relational schema with foreign key relationships

Architecture flow: **API → ETL → SQL → Analytics → Visualization**

## Installation

### Prerequisites

- Python 3.8+
- MySQL or TiDB Cloud account
- Harvard Art Museums API key (get free at: https://www.harvardartmuseums.org/collections/api)

### Setup

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
export DB_NAME="harvard_artifacts"
```

### Required Dependencies

```python
# requirements.txt contents
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
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establish connection to MySQL/TiDB Cloud"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    return connection
```

### API Configuration

```python
import requests
import os

API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API"""
    params = {
        'apikey': API_KEY,
        'page': page,
        'size': size
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
```

## Database Schema

### Create Tables

```python
def create_tables(connection):
    """Create relational database schema"""
    cursor = connection.cursor()
    
    # Artifact metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            objectid INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(255),
            century VARCHAR(100),
            classification VARCHAR(255),
            division VARCHAR(255),
            department VARCHAR(255),
            dated VARCHAR(255),
            accessionyear INT,
            period VARCHAR(255),
            technique VARCHAR(500),
            medium VARCHAR(500),
            dimensions VARCHAR(500),
            creditline TEXT,
            url VARCHAR(500),
            verificationlevel INT,
            totalpageviews INT,
            totaluniquepageviews INT
        )
    """)
    
    # Artifact media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            objectid INT,
            mediacount INT,
            primaryimageurl VARCHAR(500),
            FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
        )
    """)
    
    # Artifact colors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            objectid INT,
            color VARCHAR(50),
            spectrum VARCHAR(50),
            hue VARCHAR(50),
            percent FLOAT,
            FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
        )
    """)
    
    connection.commit()
    cursor.close()
```

## ETL Pipeline Implementation

### Extract: Fetch Data from API

```python
import time

def extract_all_artifacts(max_pages=10):
    """Extract artifacts with pagination and rate limiting"""
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        try:
            data = fetch_artifacts(page=page, size=100)
            artifacts = data.get('records', [])
            all_artifacts.extend(artifacts)
            
            print(f"Fetched page {page}: {len(artifacts)} artifacts")
            
            # Rate limiting
            time.sleep(1)
            
            # Check if there are more pages
            if data['info']['page'] >= data['info']['pages']:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    return all_artifacts
```

### Transform: Process JSON to Relational Format

```python
import pandas as pd

def transform_artifacts(artifacts):
    """Transform nested JSON into relational dataframes"""
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata = {
            'objectid': artifact.get('objectid'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'division': artifact.get('division'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'accessionyear': artifact.get('accessionyear'),
            'period': artifact.get('period'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'creditline': artifact.get('creditline'),
            'url': artifact.get('url'),
            'verificationlevel': artifact.get('verificationlevel'),
            'totalpageviews': artifact.get('totalpageviews'),
            'totaluniquepageviews': artifact.get('totaluniquepageviews')
        }
        metadata_records.append(metadata)
        
        # Extract media
        media = {
            'objectid': artifact.get('objectid'),
            'mediacount': artifact.get('mediacount', 0),
            'primaryimageurl': artifact.get('primaryimageurl')
        }
        media_records.append(media)
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_record = {
                'objectid': artifact.get('objectid'),
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'hue': color.get('hue'),
                'percent': color.get('percent')
            }
            color_records.append(color_record)
    
    return (
        pd.DataFrame(metadata_records),
        pd.DataFrame(media_records),
        pd.DataFrame(color_records)
    )
```

### Load: Insert into Database

```python
def load_to_database(metadata_df, media_df, colors_df, connection):
    """Load transformed data into SQL database with batch inserts"""
    cursor = connection.cursor()
    
    # Insert metadata
    metadata_query = """
        INSERT INTO artifactmetadata 
        (objectid, title, culture, century, classification, division, 
         department, dated, accessionyear, period, technique, medium, 
         dimensions, creditline, url, verificationlevel, 
         totalpageviews, totaluniquepageviews)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
    """
    cursor.executemany(metadata_query, metadata_df.values.tolist())
    
    # Insert media
    media_query = """
        INSERT INTO artifactmedia (objectid, mediacount, primaryimageurl)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(media_query, media_df.values.tolist())
    
    # Insert colors
    if not colors_df.empty:
        colors_query = """
            INSERT INTO artifactcolors (objectid, color, spectrum, hue, percent)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(colors_query, colors_df.values.tolist())
    
    connection.commit()
    cursor.close()
    print(f"Loaded {len(metadata_df)} artifacts successfully")
```

## Complete ETL Workflow

```python
def run_etl_pipeline():
    """Execute complete ETL pipeline"""
    # Extract
    print("Starting extraction...")
    artifacts = extract_all_artifacts(max_pages=10)
    print(f"Extracted {len(artifacts)} total artifacts")
    
    # Transform
    print("Starting transformation...")
    metadata_df, media_df, colors_df = transform_artifacts(artifacts)
    print(f"Transformed into {len(metadata_df)} metadata, {len(media_df)} media, {len(colors_df)} color records")
    
    # Load
    print("Starting load...")
    connection = get_db_connection()
    create_tables(connection)
    load_to_database(metadata_df, media_df, colors_df, connection)
    connection.close()
    print("ETL pipeline completed successfully")

# Execute pipeline
if __name__ == "__main__":
    run_etl_pipeline()
```

## SQL Analytics Queries

### Analytical Query Examples

```python
# Query 1: Artifact distribution by culture
QUERIES = {
    "artifacts_by_culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 10
    """,
    
    "artifacts_by_century": """
        SELECT century, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY artifact_count DESC
    """,
    
    "media_availability": """
        SELECT 
            CASE 
                WHEN mediacount > 0 THEN 'Has Media'
                ELSE 'No Media'
            END as media_status,
            COUNT(*) as count
        FROM artifactmedia
        GROUP BY media_status
    """,
    
    "top_colors": """
        SELECT color, spectrum, COUNT(*) as usage_count
        FROM artifactcolors
        GROUP BY color, spectrum
        ORDER BY usage_count DESC
        LIMIT 10
    """,
    
    "artifacts_by_department": """
        SELECT department, COUNT(*) as count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY count DESC
    """,
    
    "popular_artifacts": """
        SELECT title, culture, century, totalpageviews
        FROM artifactmetadata
        WHERE totalpageviews IS NOT NULL
        ORDER BY totalpageviews DESC
        LIMIT 20
    """,
    
    "artifacts_with_images": """
        SELECT 
            am.culture,
            COUNT(DISTINCT am.objectid) as artifacts_with_images
        FROM artifactmetadata am
        INNER JOIN artifactmedia med ON am.objectid = med.objectid
        WHERE med.primaryimageurl IS NOT NULL
        GROUP BY am.culture
        ORDER BY artifacts_with_images DESC
        LIMIT 10
    """
}

def execute_query(query_name, connection):
    """Execute analytical query and return results"""
    cursor = connection.cursor()
    cursor.execute(QUERIES[query_name])
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    cursor.close()
    
    return pd.DataFrame(results, columns=columns)
```

## Streamlit Dashboard Implementation

### Main Application

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(page_title="Harvard Art Analytics", layout="wide")
    
    st.title("🎨 Harvard Art Museums Analytics Dashboard")
    st.markdown("Explore artifact collections through data analytics")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose Analysis",
        ["ETL Pipeline", "SQL Analytics", "Visualizations"]
    )
    
    connection = get_db_connection()
    
    if page == "ETL Pipeline":
        show_etl_page()
    elif page == "SQL Analytics":
        show_analytics_page(connection)
    elif page == "Visualizations":
        show_visualizations_page(connection)
    
    connection.close()

def show_etl_page():
    """ETL control page"""
    st.header("ETL Pipeline Control")
    
    max_pages = st.number_input("Number of pages to fetch", min_value=1, max_value=100, value=5)
    
    if st.button("Run ETL Pipeline"):
        with st.spinner("Running ETL pipeline..."):
            try:
                run_etl_pipeline()
                st.success("ETL completed successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

def show_analytics_page(connection):
    """SQL analytics page"""
    st.header("SQL Analytics")
    
    query_choice = st.selectbox(
        "Select Analysis Query",
        list(QUERIES.keys())
    )
    
    if st.button("Execute Query"):
        with st.spinner("Executing query..."):
            df = execute_query(query_choice, connection)
            st.dataframe(df)
            
            # Auto-generate visualization
            if len(df.columns) >= 2:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1])
                st.plotly_chart(fig, use_container_width=True)

def show_visualizations_page(connection):
    """Interactive visualizations page"""
    st.header("Data Visualizations")
    
    # Culture distribution
    st.subheader("Top Cultures by Artifact Count")
    df_culture = execute_query("artifacts_by_culture", connection)
    fig = px.bar(df_culture, x='culture', y='artifact_count', 
                 title="Artifacts by Culture")
    st.plotly_chart(fig, use_container_width=True)
    
    # Century distribution
    st.subheader("Artifacts by Century")
    df_century = execute_query("artifacts_by_century", connection)
    fig = px.pie(df_century, names='century', values='artifact_count',
                 title="Century Distribution")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

### Run the Application

```bash
streamlit run app.py
```

## Common Patterns

### Error Handling in ETL

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_etl_pipeline():
    """ETL pipeline with comprehensive error handling"""
    try:
        # Extract with retry logic
        artifacts = []
        for attempt in range(3):
            try:
                artifacts = extract_all_artifacts(max_pages=10)
                break
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)
        
        if not artifacts:
            raise ValueError("No artifacts extracted")
        
        # Transform with validation
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        
        if metadata_df.empty:
            raise ValueError("Transformation resulted in empty dataframe")
        
        # Load with transaction
        connection = get_db_connection()
        try:
            load_to_database(metadata_df, media_df, colors_df, connection)
            logger.info("ETL completed successfully")
        finally:
            connection.close()
            
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise
```

### Incremental Data Loading

```python
def incremental_load(since_date):
    """Load only new artifacts since last run"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get last loaded object ID
    cursor.execute("SELECT MAX(objectid) FROM artifactmetadata")
    last_id = cursor.fetchone()[0] or 0
    
    # Fetch only newer artifacts
    params = {
        'apikey': os.getenv('HARVARD_API_KEY'),
        'q': f'objectid:>{last_id}',
        'size': 100
    }
    
    response = requests.get(BASE_URL, params=params)
    new_artifacts = response.json().get('records', [])
    
    # Transform and load
    if new_artifacts:
        metadata_df, media_df, colors_df = transform_artifacts(new_artifacts)
        load_to_database(metadata_df, media_df, colors_df, connection)
    
    connection.close()
```

## Troubleshooting

### API Rate Limiting

If you encounter rate limit errors:

```python
import time
from functools import wraps

def rate_limited(max_per_second=1):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / max_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limited(max_per_second=1)
def fetch_artifacts_safe(page=1, size=100):
    """Rate-limited artifact fetching"""
    return fetch_artifacts(page, size)
```

### Database Connection Pool

For better performance:

```python
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

### Memory Management for Large Datasets

```python
def batch_etl(batch_size=1000):
    """Process artifacts in batches to manage memory"""
    page = 1
    connection = get_db_connection()
    
    while True:
        artifacts = fetch_artifacts(page=page, size=100)
        if not artifacts:
            break
        
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        load_to_database(metadata_df, media_df, colors_df, connection)
        
        page += 1
        
        # Clear memory every 10 pages
        if page % 10 == 0:
            import gc
            gc.collect()
    
    connection.close()
```

This skill provides comprehensive coverage of building ETL pipelines, SQL analytics, and data visualization dashboards using the Harvard Art Museums API with Python, Streamlit, and SQL databases.
