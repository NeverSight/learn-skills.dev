---
name: harvard-artifacts-collection-analytics-pipeline
description: End-to-end data engineering pipeline for Harvard Art Museums API with ETL, SQL analytics, and Streamlit visualization
triggers:
  - build a data pipeline for Harvard Art Museums API
  - create ETL workflow for museum artifacts data
  - set up artifact collection analytics with Streamlit
  - implement Harvard museums data engineering pipeline
  - analyze art museum data with SQL and visualization
  - extract and transform Harvard API artifact data
  - build interactive dashboard for museum collection data
  - create SQL analytics for art artifacts
---

# Harvard Artifacts Collection Analytics Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project provides a complete data engineering solution for the Harvard Art Museums API, featuring:
- ETL pipeline for artifact metadata, media, and color data
- SQL database storage (MySQL/TiDB Cloud)
- 20+ analytical SQL queries
- Interactive Streamlit dashboard with Plotly visualizations

The architecture follows: **API → ETL → SQL → Analytics → Visualization**

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

### Required Dependencies

```python
# requirements.txt typically includes:
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Harvard Art Museums API
HARVARD_API_KEY=your_api_key_here

# MySQL/TiDB Cloud Connection
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=harvard_artifacts
```

### Database Setup

```python
import mysql.connector
from mysql.connector import Error

def create_database_connection():
    """Establish MySQL/TiDB connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables(connection):
    """Create database schema"""
    cursor = connection.cursor()
    
    # Artifact Metadata Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            artifact_id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(200),
            century VARCHAR(100),
            classification VARCHAR(200),
            department VARCHAR(200),
            dated VARCHAR(200),
            period VARCHAR(200),
            technique VARCHAR(500),
            medium VARCHAR(500),
            dimensions VARCHAR(500),
            creditline TEXT,
            url VARCHAR(500)
        )
    """)
    
    # Artifact Media Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            media_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            image_url VARCHAR(1000),
            caption TEXT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
        )
    """)
    
    # Artifact Colors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            color_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color_hex VARCHAR(10),
            color_name VARCHAR(100),
            percentage FLOAT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
        )
    """)
    
    connection.commit()
    cursor.close()
```

## ETL Pipeline

### Extract: Fetch Data from Harvard API

```python
import requests
import time

def fetch_artifacts_from_api(api_key, size=100, page=1):
    """Extract artifacts from Harvard Art Museums API"""
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'size': size,
        'page': page,
        'hasimage': 1  # Only artifacts with images
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Handle rate limiting
        time.sleep(0.5)
        
        return data.get('records', []), data.get('info', {})
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return [], {}

def paginate_api_collection(api_key, max_pages=10):
    """Collect multiple pages of artifacts"""
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        records, info = fetch_artifacts_from_api(api_key, page=page)
        if not records:
            break
        all_artifacts.extend(records)
        print(f"Fetched page {page}, total artifacts: {len(all_artifacts)}")
        
    return all_artifacts
```

### Transform: Process JSON Data

```python
import pandas as pd

def transform_artifact_metadata(artifacts):
    """Transform artifact data into structured format"""
    metadata = []
    
    for artifact in artifacts:
        metadata.append({
            'artifact_id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'period': artifact.get('period'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'creditline': artifact.get('creditline'),
            'url': artifact.get('url')
        })
    
    return pd.DataFrame(metadata)

def transform_artifact_media(artifacts):
    """Extract media/image data"""
    media_data = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        images = artifact.get('images', [])
        
        for image in images:
            media_data.append({
                'artifact_id': artifact_id,
                'image_url': image.get('baseimageurl'),
                'caption': image.get('caption')
            })
    
    return pd.DataFrame(media_data)

def transform_artifact_colors(artifacts):
    """Extract color information"""
    color_data = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        colors = artifact.get('colors', [])
        
        for color in colors:
            color_data.append({
                'artifact_id': artifact_id,
                'color_hex': color.get('hex'),
                'color_name': color.get('color'),
                'percentage': color.get('percent')
            })
    
    return pd.DataFrame(color_data)
```

### Load: Insert into Database

```python
def load_dataframe_to_sql(df, table_name, connection):
    """Batch insert DataFrame into SQL table"""
    cursor = connection.cursor()
    
    # Generate INSERT statement
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Batch insert
    data_tuples = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data_tuples)
    
    connection.commit()
    cursor.close()
    print(f"Inserted {len(df)} records into {table_name}")

def run_etl_pipeline(api_key, connection, max_pages=5):
    """Execute complete ETL pipeline"""
    # Extract
    artifacts = paginate_api_collection(api_key, max_pages)
    
    # Transform
    metadata_df = transform_artifact_metadata(artifacts)
    media_df = transform_artifact_media(artifacts)
    colors_df = transform_artifact_colors(artifacts)
    
    # Load
    load_dataframe_to_sql(metadata_df, 'artifactmetadata', connection)
    load_dataframe_to_sql(media_df, 'artifactmedia', connection)
    load_dataframe_to_sql(colors_df, 'artifactcolors', connection)
    
    return len(artifacts)
```

## SQL Analytics Queries

### Sample Analytical Queries

```python
ANALYTICAL_QUERIES = {
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
    
    "Department Distribution": """
        SELECT department, COUNT(*) as total_artifacts
        FROM artifactmetadata
        GROUP BY department
        ORDER BY total_artifacts DESC
    """,
    
    "Most Common Colors": """
        SELECT color_name, COUNT(*) as usage_count, AVG(percentage) as avg_percentage
        FROM artifactcolors
        WHERE color_name IS NOT NULL
        GROUP BY color_name
        ORDER BY usage_count DESC
        LIMIT 15
    """,
    
    "Media Availability": """
        SELECT 
            COUNT(DISTINCT m.artifact_id) as artifacts_with_media,
            COUNT(*) as total_images
        FROM artifactmedia m
    """,
    
    "Classification Analysis": """
        SELECT classification, COUNT(*) as count, 
               GROUP_CONCAT(DISTINCT culture SEPARATOR ', ') as cultures
        FROM artifactmetadata
        WHERE classification IS NOT NULL
        GROUP BY classification
        ORDER BY count DESC
        LIMIT 10
    """
}

def execute_query(connection, query_name):
    """Run analytical query and return results"""
    cursor = connection.cursor(dictionary=True)
    query = ANALYTICAL_QUERIES[query_name]
    
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    
    return pd.DataFrame(results)
```

## Streamlit Dashboard

### Main Application Structure

```python
import streamlit as st
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    st.set_page_config(
        page_title="Harvard Artifacts Analytics",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Harvard API Key",
            value=os.getenv('HARVARD_API_KEY', ''),
            type="password"
        )
        
        # Database connection
        if st.button("Connect to Database"):
            connection = create_database_connection()
            if connection:
                st.success("✅ Database connected!")
                st.session_state['db_connection'] = connection
            else:
                st.error("❌ Connection failed")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📥 ETL Pipeline", "📊 Analytics", "📈 Visualizations"])
    
    with tab1:
        render_etl_tab(api_key)
    
    with tab2:
        render_analytics_tab()
    
    with tab3:
        render_visualization_tab()

def render_etl_tab(api_key):
    """ETL Pipeline interface"""
    st.header("Extract, Transform, Load")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_pages = st.slider("Number of pages to fetch", 1, 20, 5)
    
    with col2:
        if st.button("🚀 Run ETL Pipeline", type="primary"):
            if not api_key:
                st.error("Please provide API key")
                return
            
            connection = st.session_state.get('db_connection')
            if not connection:
                st.error("Database not connected")
                return
            
            with st.spinner("Running ETL pipeline..."):
                try:
                    # Create tables
                    create_tables(connection)
                    
                    # Run pipeline
                    total_artifacts = run_etl_pipeline(api_key, connection, max_pages)
                    
                    st.success(f"✅ Successfully loaded {total_artifacts} artifacts!")
                except Exception as e:
                    st.error(f"ETL Error: {e}")

def render_analytics_tab():
    """SQL Analytics interface"""
    st.header("SQL Analytics Dashboard")
    
    connection = st.session_state.get('db_connection')
    if not connection:
        st.warning("Connect to database first")
        return
    
    # Query selector
    selected_query = st.selectbox(
        "Select Analysis",
        list(ANALYTICAL_QUERIES.keys())
    )
    
    if st.button("Run Query"):
        with st.spinner("Executing query..."):
            try:
                df_results = execute_query(connection, selected_query)
                
                st.subheader("Query Results")
                st.dataframe(df_results, use_container_width=True)
                
                # Auto-generate visualization
                if len(df_results) > 0:
                    st.session_state['query_results'] = df_results
                    st.session_state['query_name'] = selected_query
                    
            except Exception as e:
                st.error(f"Query error: {e}")

def render_visualization_tab():
    """Visualization interface"""
    st.header("Data Visualizations")
    
    if 'query_results' not in st.session_state:
        st.info("Run a query in the Analytics tab first")
        return
    
    df = st.session_state['query_results']
    query_name = st.session_state['query_name']
    
    # Auto-detect chart type based on columns
    if len(df.columns) >= 2:
        x_col = df.columns[0]
        y_col = df.columns[1]
        
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=query_name,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

### Running the Dashboard

```bash
# Start Streamlit application
streamlit run app.py

# Access at http://localhost:8501
```

## Common Patterns

### Incremental Data Loading

```python
def get_max_artifact_id(connection):
    """Get highest artifact ID in database"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(artifact_id) FROM artifactmetadata")
    result = cursor.fetchone()
    cursor.close()
    return result[0] or 0

def incremental_etl(api_key, connection):
    """Load only new artifacts"""
    max_id = get_max_artifact_id(connection)
    
    # Fetch artifacts with ID > max_id
    params = {'apikey': api_key, 'q': f'id:>{max_id}'}
    # ... continue with ETL
```

### Error Handling and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_etl_execution(api_key, connection, max_pages):
    """ETL with comprehensive error handling"""
    try:
        artifacts = paginate_api_collection(api_key, max_pages)
        logger.info(f"Extracted {len(artifacts)} artifacts")
        
        metadata_df = transform_artifact_metadata(artifacts)
        logger.info(f"Transformed {len(metadata_df)} metadata records")
        
        load_dataframe_to_sql(metadata_df, 'artifactmetadata', connection)
        logger.info("Successfully loaded to database")
        
        return True
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        return False
```

## Troubleshooting

### API Rate Limiting

```python
# Add exponential backoff
import time
from functools import wraps

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:  # Rate limit
                        sleep_time = backoff_in_seconds * (2 ** x)
                        time.sleep(sleep_time)
                        x += 1
                    else:
                        raise
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_with_backoff(retries=5)
def fetch_with_retry(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
```

### Database Connection Issues

```python
# Connection pooling for reliability
from mysql.connector import pooling

def create_connection_pool():
    """Create reusable connection pool"""
    return pooling.MySQLConnectionPool(
        pool_name="harvard_pool",
        pool_size=5,
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Use in application
pool = create_connection_pool()
connection = pool.get_connection()
```

### Memory Management for Large Datasets

```python
def chunked_data_load(artifacts, chunk_size=100):
    """Process large datasets in chunks"""
    for i in range(0, len(artifacts), chunk_size):
        chunk = artifacts[i:i + chunk_size]
        
        metadata_df = transform_artifact_metadata(chunk)
        load_dataframe_to_sql(metadata_df, 'artifactmetadata', connection)
        
        # Clear memory
        del metadata_df
```

## Key Features Summary

- **ETL Pipeline**: Automated data collection with pagination and rate limiting
- **SQL Storage**: Normalized schema with foreign key relationships
- **Analytics**: 20+ pre-built queries for artifact insights
- **Visualization**: Interactive Plotly charts in Streamlit
- **Scalability**: Handles batch processing and incremental loads
