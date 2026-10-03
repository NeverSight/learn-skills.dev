---
name: harvard-art-museum-data-pipeline
description: Build ETL pipelines and analytics dashboards using the Harvard Art Museums API with Streamlit, MySQL, and Python
triggers:
  - how do I set up a data pipeline for Harvard Art Museums API
  - build an ETL workflow for museum artifact data
  - create analytics dashboard with Harvard Art Museums data
  - extract and transform Harvard Art Museums API data
  - set up SQL database for museum artifacts collection
  - visualize Harvard Art Museums data with Streamlit
  - query Harvard Art Museums API with pagination
  - design relational schema for museum artifact data
---

# Harvard Art Museum Data Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides an end-to-end data engineering solution for collecting, transforming, storing, and analyzing artifact data from the Harvard Art Museums API. It demonstrates production-ready ETL pipelines, SQL analytics, and interactive visualization using Streamlit.

## What It Does

The Harvard Art Museum Data Pipeline:

- **Extracts** artifact data from the Harvard Art Museums API with pagination and rate limiting
- **Transforms** nested JSON into normalized relational tables (metadata, media, colors)
- **Loads** data into MySQL/TiDB Cloud with batch inserts for performance
- **Analyzes** data using predefined SQL queries for business insights
- **Visualizes** results through interactive Streamlit dashboards with Plotly charts

## Architecture

```
Harvard Art Museums API → Python ETL → MySQL/TiDB → SQL Analytics → Streamlit Dashboard
```

**Key Components:**
- API integration with secure key management
- Three-table relational schema: `artifactmetadata`, `artifactmedia`, `artifactcolors`
- 20+ analytical SQL queries
- Real-time interactive visualizations

## Installation

### Prerequisites

- Python 3.8+
- MySQL or TiDB Cloud account
- Harvard Art Museums API key (obtain from https://harvardartmuseums.org/collections/api)

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

Configure your MySQL/TiDB connection in your application:

```python
import mysql.connector
import os

def get_db_connection():
    """Create database connection using environment variables"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
```

### API Configuration

Set up the Harvard Art Museums API client:

```python
import os
import requests

class HarvardMuseumAPI:
    def __init__(self):
        self.api_key = os.getenv('HARVARD_API_KEY')
        self.base_url = "https://api.harvardartmuseums.org"
        
    def get_objects(self, page=1, size=100):
        """Fetch objects with pagination"""
        url = f"{self.base_url}/object"
        params = {
            'apikey': self.api_key,
            'page': page,
            'size': size
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
```

## Database Schema

### Create Tables

```sql
-- Artifact Metadata
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    department VARCHAR(255),
    technique VARCHAR(500),
    medium VARCHAR(500),
    dated VARCHAR(255),
    accession_number VARCHAR(100),
    url VARCHAR(500)
);

-- Artifact Media
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    image_url VARCHAR(1000),
    alt_text TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact Colors
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_name VARCHAR(100),
    hex_code VARCHAR(10),
    percentage DECIMAL(5,2),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## ETL Pipeline

### Extract Phase

```python
import requests
import time

def extract_artifacts(api_key, num_pages=10, page_size=100):
    """
    Extract artifacts from Harvard Art Museums API with pagination
    """
    base_url = "https://api.harvardartmuseums.org/object"
    all_records = []
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': api_key,
            'page': page,
            'size': page_size
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'records' in data:
                all_records.extend(data['records'])
            
            # Rate limiting
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"Error on page {page}: {e}")
            continue
    
    return all_records
```

### Transform Phase

```python
import pandas as pd

def transform_metadata(records):
    """Transform artifact records into metadata DataFrame"""
    metadata = []
    
    for record in records:
        metadata.append({
            'id': record.get('id'),
            'title': record.get('title', '')[:500],
            'culture': record.get('culture', '')[:255],
            'century': record.get('century', '')[:100],
            'classification': record.get('classification', '')[:255],
            'department': record.get('department', '')[:255],
            'technique': record.get('technique', '')[:500],
            'medium': record.get('medium', '')[:500],
            'dated': record.get('dated', '')[:255],
            'accession_number': record.get('accessionyear', '')[:100],
            'url': record.get('url', '')[:500]
        })
    
    return pd.DataFrame(metadata)

def transform_media(records):
    """Extract media information from artifacts"""
    media = []
    
    for record in records:
        artifact_id = record.get('id')
        images = record.get('images', [])
        
        for image in images:
            media.append({
                'artifact_id': artifact_id,
                'image_url': image.get('baseimageurl', '')[:1000],
                'alt_text': image.get('alttext', '')
            })
    
    return pd.DataFrame(media)

def transform_colors(records):
    """Extract color data from artifacts"""
    colors = []
    
    for record in records:
        artifact_id = record.get('id')
        color_list = record.get('colors', [])
        
        for color in color_list:
            colors.append({
                'artifact_id': artifact_id,
                'color_name': color.get('color', '')[:100],
                'hex_code': color.get('hex', '')[:10],
                'percentage': color.get('percent', 0.0)
            })
    
    return pd.DataFrame(colors)
```

### Load Phase

```python
def load_to_database(df, table_name, connection):
    """
    Batch insert DataFrame into MySQL table
    """
    cursor = connection.cursor()
    
    # Generate INSERT statement
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Batch insert
    data_tuples = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data_tuples)
    connection.commit()
    
    print(f"Inserted {cursor.rowcount} rows into {table_name}")
    cursor.close()
```

### Complete ETL Workflow

```python
def run_etl_pipeline(api_key, db_connection, num_pages=10):
    """
    Execute complete ETL pipeline
    """
    # Extract
    print("Extracting data from API...")
    records = extract_artifacts(api_key, num_pages=num_pages)
    
    # Transform
    print("Transforming data...")
    metadata_df = transform_metadata(records)
    media_df = transform_media(records)
    colors_df = transform_colors(records)
    
    # Load
    print("Loading data to database...")
    load_to_database(metadata_df, 'artifactmetadata', db_connection)
    load_to_database(media_df, 'artifactmedia', db_connection)
    load_to_database(colors_df, 'artifactcolors', db_connection)
    
    print("ETL pipeline completed successfully!")
```

## SQL Analytics Queries

### Common Analytics Patterns

```python
# Top cultures by artifact count
query_cultures = """
SELECT culture, COUNT(*) as artifact_count
FROM artifactmetadata
WHERE culture IS NOT NULL AND culture != ''
GROUP BY culture
ORDER BY artifact_count DESC
LIMIT 10;
"""

# Artifacts by century
query_centuries = """
SELECT century, COUNT(*) as count
FROM artifactmetadata
WHERE century IS NOT NULL
GROUP BY century
ORDER BY count DESC;
"""

# Media availability analysis
query_media = """
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM artifactmedia WHERE artifactmedia.artifact_id = artifactmetadata.id)
        THEN 'Has Media'
        ELSE 'No Media'
    END as media_status,
    COUNT(*) as count
FROM artifactmetadata
GROUP BY media_status;
"""

# Color distribution
query_colors = """
SELECT color_name, COUNT(*) as usage_count, AVG(percentage) as avg_percentage
FROM artifactcolors
GROUP BY color_name
ORDER BY usage_count DESC
LIMIT 15;
"""

# Department breakdown
query_departments = """
SELECT department, COUNT(*) as artifact_count
FROM artifactmetadata
WHERE department IS NOT NULL
GROUP BY department
ORDER BY artifact_count DESC;
"""
```

## Streamlit Dashboard

### Main Application Structure

```python
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Harvard Art Museums Analytics", layout="wide")
    
    st.title("🏛️ Harvard Art Museums Data Analytics")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        if st.button("Run ETL Pipeline"):
            run_etl_with_progress()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🗄️ Data Explorer", "📈 Visualizations"])
    
    with tab1:
        show_analytics_dashboard()
    
    with tab2:
        show_data_explorer()
    
    with tab3:
        show_visualizations()

def run_etl_with_progress():
    """Run ETL with progress bar"""
    with st.spinner("Running ETL pipeline..."):
        connection = get_db_connection()
        api_key = os.getenv('HARVARD_API_KEY')
        run_etl_pipeline(api_key, connection, num_pages=5)
        st.success("ETL completed successfully!")

def show_analytics_dashboard():
    """Display predefined analytics queries"""
    st.subheader("Analytical Insights")
    
    queries = {
        "Top Cultures": query_cultures,
        "Artifacts by Century": query_centuries,
        "Media Availability": query_media,
        "Color Distribution": query_colors,
        "Department Breakdown": query_departments
    }
    
    query_choice = st.selectbox("Select Analysis", list(queries.keys()))
    
    if st.button("Run Query"):
        connection = get_db_connection()
        df = pd.read_sql(queries[query_choice], connection)
        
        st.dataframe(df)
        
        # Auto-generate visualization
        if len(df.columns) == 2:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                        title=query_choice)
            st.plotly_chart(fig, use_container_width=True)

def show_data_explorer():
    """Interactive data exploration"""
    st.subheader("Data Explorer")
    
    table = st.selectbox("Select Table", 
                        ["artifactmetadata", "artifactmedia", "artifactcolors"])
    
    connection = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 100", connection)
    
    st.dataframe(df)
    st.caption(f"Showing first 100 rows from {table}")

if __name__ == "__main__":
    main()
```

### Running the Dashboard

```bash
streamlit run app.py
```

## Common Patterns

### Pagination Handler

```python
def fetch_all_pages(api_key, max_pages=None):
    """
    Fetch all available pages from API
    """
    page = 1
    all_records = []
    
    while True:
        data = get_objects(api_key, page=page)
        records = data.get('records', [])
        
        if not records:
            break
        
        all_records.extend(records)
        
        info = data.get('info', {})
        if page >= info.get('pages', 0):
            break
        
        if max_pages and page >= max_pages:
            break
        
        page += 1
        time.sleep(0.5)  # Rate limiting
    
    return all_records
```

### Error Handling

```python
def safe_etl_execution():
    """ETL with comprehensive error handling"""
    try:
        connection = get_db_connection()
        api_key = os.getenv('HARVARD_API_KEY')
        
        if not api_key:
            raise ValueError("HARVARD_API_KEY not set")
        
        run_etl_pipeline(api_key, connection)
        
    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        # Implement retry logic or alerting
        
    except requests.exceptions.RequestException as api_error:
        print(f"API error: {api_error}")
        # Log and retry
        
    finally:
        if connection.is_connected():
            connection.close()
```

## Troubleshooting

### API Rate Limiting

If you encounter rate limit errors:

```python
import time
from functools import wraps

def rate_limited(max_per_second=2):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / max_per_second
    
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator

@rate_limited(max_per_second=2)
def fetch_data(url, params):
    return requests.get(url, params=params)
```

### Database Connection Issues

```python
def get_db_connection_with_retry(max_retries=3):
    """Database connection with retry logic"""
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                connect_timeout=10
            )
            return connection
        except mysql.connector.Error as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Memory Optimization for Large Datasets

```python
def batch_process_records(records, batch_size=1000):
    """Process large datasets in batches"""
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        metadata_df = transform_metadata(batch)
        media_df = transform_media(batch)
        colors_df = transform_colors(batch)
        
        connection = get_db_connection()
        load_to_database(metadata_df, 'artifactmetadata', connection)
        load_to_database(media_df, 'artifactmedia', connection)
        load_to_database(colors_df, 'artifactcolors', connection)
        connection.close()
        
        print(f"Processed batch {i//batch_size + 1}")
```

### Handling Missing Data

```python
def clean_record(record):
    """Clean and validate record data"""
    return {
        'id': record.get('id'),
        'title': (record.get('title') or 'Unknown')[:500],
        'culture': (record.get('culture') or '')[:255],
        'century': (record.get('century') or '')[:100],
        # Use empty string instead of None for NOT NULL fields
        'classification': (record.get('classification') or '')[:255],
        'department': (record.get('department') or '')[:255],
    }
```

This skill provides everything needed to build production-ready data pipelines using the Harvard Art Museums API with proper ETL practices, SQL analytics, and interactive dashboards.
