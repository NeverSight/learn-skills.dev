---
name: harvard-art-museums-data-engineering-pipeline
description: Build end-to-end data engineering pipelines with Harvard Art Museums API, ETL, SQL analytics, and Streamlit dashboards
triggers:
  - how do I build an ETL pipeline with the Harvard Art Museums API
  - set up data engineering project with Harvard artifacts
  - create analytics dashboard for museum collection data
  - extract and transform Harvard Art Museums API data
  - build streamlit app with museum artifact analytics
  - implement SQL analytics for art collection data
  - design relational database for museum artifacts
  - visualize Harvard Art Museums data with plotly
---

# Harvard Art Museums Data Engineering Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App is a complete data engineering solution that demonstrates:

- **API Integration**: Fetching artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extracting, transforming, and loading nested JSON into normalized SQL tables
- **Database Design**: Multi-table relational schema with proper foreign keys
- **SQL Analytics**: 20+ predefined analytical queries for insights
- **Interactive Visualization**: Streamlit dashboards with Plotly charts

This project serves as a reference architecture for building production-grade data pipelines.

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required packages:**
```
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

# Database Configuration
DB_HOST=your_db_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=harvard_artifacts
```

### Getting Harvard API Key

1. Visit https://www.harvardartmuseums.org/collections/api
2. Request an API key (free for non-commercial use)
3. Add to `.env` file

### Database Setup

The application supports MySQL and TiDB Cloud. Create the database:

```sql
CREATE DATABASE harvard_artifacts;
USE harvard_artifacts;
```

Tables are created automatically by the ETL pipeline.

## Running the Application

```bash
# Start Streamlit dashboard
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Core Components

### 1. API Data Extraction

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API"""
    api_key = os.getenv('HARVARD_API_KEY')
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data['records'], data['info']

# Fetch multiple pages with pagination
all_artifacts = []
page = 1
max_pages = 5

while page <= max_pages:
    records, info = fetch_artifacts(page=page)
    all_artifacts.extend(records)
    print(f"Fetched page {page}/{info['pages']}")
    page += 1
```

### 2. ETL Pipeline

**Extract and Transform:**

```python
import pandas as pd

def transform_artifact_metadata(artifacts):
    """Transform artifact JSON to normalized metadata table"""
    metadata = []
    
    for artifact in artifacts:
        metadata.append({
            'objectid': artifact.get('objectid'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'period': artifact.get('period'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'dated': artifact.get('dated'),
            'department': artifact.get('department'),
            'division': artifact.get('division'),
            'creditline': artifact.get('creditline'),
            'accessionyear': artifact.get('accessionyear')
        })
    
    return pd.DataFrame(metadata)

def transform_artifact_media(artifacts):
    """Transform media/images into separate table"""
    media = []
    
    for artifact in artifacts:
        objectid = artifact.get('objectid')
        images = artifact.get('images', [])
        
        for img in images:
            media.append({
                'objectid': objectid,
                'imageid': img.get('imageid'),
                'baseimageurl': img.get('baseimageurl'),
                'width': img.get('width'),
                'height': img.get('height'),
                'format': img.get('format')
            })
    
    return pd.DataFrame(media)

def transform_artifact_colors(artifacts):
    """Transform color data into separate table"""
    colors = []
    
    for artifact in artifacts:
        objectid = artifact.get('objectid')
        color_list = artifact.get('colors', [])
        
        for color in color_list:
            colors.append({
                'objectid': objectid,
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'hue': color.get('hue'),
                'percent': color.get('percent')
            })
    
    return pd.DataFrame(colors)
```

**Load to Database:**

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
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
            medium TEXT,
            dimensions TEXT,
            dated VARCHAR(255),
            department VARCHAR(255),
            division VARCHAR(255),
            creditline TEXT,
            accessionyear INT
        )
    """)
    
    # Media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            objectid INT,
            imageid INT,
            baseimageurl TEXT,
            width INT,
            height INT,
            format VARCHAR(50),
            FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
        )
    """)
    
    # Colors table
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

def load_dataframe_to_sql(df, table_name, connection):
    """Batch insert DataFrame into SQL table"""
    cursor = connection.cursor()
    
    cols = ','.join(df.columns)
    placeholders = ','.join(['%s'] * len(df.columns))
    
    insert_query = f"INSERT IGNORE INTO {table_name} ({cols}) VALUES ({placeholders})"
    
    data_tuples = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data_tuples)
    connection.commit()
    
    print(f"Loaded {cursor.rowcount} rows into {table_name}")
```

### 3. Complete ETL Execution

```python
def run_etl_pipeline():
    """Execute complete ETL pipeline"""
    # Extract
    print("Extracting data from API...")
    all_artifacts = []
    for page in range(1, 6):  # Fetch 5 pages
        records, _ = fetch_artifacts(page=page)
        all_artifacts.extend(records)
    
    # Transform
    print("Transforming data...")
    df_metadata = transform_artifact_metadata(all_artifacts)
    df_media = transform_artifact_media(all_artifacts)
    df_colors = transform_artifact_colors(all_artifacts)
    
    # Load
    print("Loading to database...")
    connection = get_db_connection()
    create_tables(connection)
    
    load_dataframe_to_sql(df_metadata, 'artifactmetadata', connection)
    load_dataframe_to_sql(df_media, 'artifactmedia', connection)
    load_dataframe_to_sql(df_colors, 'artifactcolors', connection)
    
    connection.close()
    print("ETL pipeline complete!")

if __name__ == "__main__":
    run_etl_pipeline()
```

### 4. SQL Analytics Queries

```python
def execute_analytics_query(query_name):
    """Execute predefined analytics queries"""
    
    queries = {
        'top_cultures': """
            SELECT culture, COUNT(*) as artifact_count
            FROM artifactmetadata
            WHERE culture IS NOT NULL
            GROUP BY culture
            ORDER BY artifact_count DESC
            LIMIT 10
        """,
        
        'artifacts_by_century': """
            SELECT century, COUNT(*) as count
            FROM artifactmetadata
            WHERE century IS NOT NULL
            GROUP BY century
            ORDER BY count DESC
        """,
        
        'media_availability': """
            SELECT 
                COUNT(DISTINCT am.objectid) as artifacts_with_media,
                (SELECT COUNT(*) FROM artifactmetadata) as total_artifacts,
                ROUND(COUNT(DISTINCT am.objectid) * 100.0 / 
                      (SELECT COUNT(*) FROM artifactmetadata), 2) as percentage
            FROM artifactmedia am
        """,
        
        'top_colors': """
            SELECT color, COUNT(*) as usage_count, AVG(percent) as avg_percent
            FROM artifactcolors
            WHERE color IS NOT NULL
            GROUP BY color
            ORDER BY usage_count DESC
            LIMIT 15
        """,
        
        'department_distribution': """
            SELECT department, COUNT(*) as count
            FROM artifactmetadata
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY count DESC
        """,
        
        'artifacts_with_accession_year': """
            SELECT accessionyear, COUNT(*) as count
            FROM artifactmetadata
            WHERE accessionyear IS NOT NULL
            GROUP BY accessionyear
            ORDER BY accessionyear DESC
            LIMIT 20
        """
    }
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(queries[query_name])
    results = cursor.fetchall()
    connection.close()
    
    return pd.DataFrame(results)
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select Page",
        ["ETL Pipeline", "SQL Analytics", "Visualizations"]
    )
    
    if page == "ETL Pipeline":
        st.header("Extract, Transform, Load")
        
        if st.button("Run ETL Pipeline"):
            with st.spinner("Running ETL..."):
                run_etl_pipeline()
                st.success("ETL completed successfully!")
    
    elif page == "SQL Analytics":
        st.header("SQL Query Analytics")
        
        query_options = {
            "Top Cultures": "top_cultures",
            "Artifacts by Century": "artifacts_by_century",
            "Media Availability": "media_availability",
            "Top Colors": "top_colors",
            "Department Distribution": "department_distribution"
        }
        
        selected_query = st.selectbox("Select Query", list(query_options.keys()))
        
        if st.button("Execute Query"):
            df_results = execute_analytics_query(query_options[selected_query])
            st.dataframe(df_results)
            
            # Auto-generate visualization
            if len(df_results.columns) >= 2:
                fig = px.bar(
                    df_results,
                    x=df_results.columns[0],
                    y=df_results.columns[1],
                    title=selected_query
                )
                st.plotly_chart(fig)
    
    elif page == "Visualizations":
        st.header("Interactive Visualizations")
        
        # Culture distribution
        df_cultures = execute_analytics_query('top_cultures')
        fig1 = px.pie(
            df_cultures,
            values='artifact_count',
            names='culture',
            title='Artifact Distribution by Culture'
        )
        st.plotly_chart(fig1)
        
        # Color analysis
        df_colors = execute_analytics_query('top_colors')
        fig2 = px.bar(
            df_colors,
            x='color',
            y='usage_count',
            color='avg_percent',
            title='Most Common Colors in Artifacts'
        )
        st.plotly_chart(fig2)

if __name__ == "__main__":
    main()
```

## Common Patterns

### Rate Limiting API Requests

```python
import time

def fetch_with_rate_limit(page, delay=0.5):
    """Fetch data with rate limiting"""
    records, info = fetch_artifacts(page=page)
    time.sleep(delay)  # Respect API rate limits
    return records, info
```

### Incremental Data Loading

```python
def get_latest_objectid(connection):
    """Get the latest objectid in database"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(objectid) FROM artifactmetadata")
    result = cursor.fetchone()
    return result[0] if result[0] else 0

def incremental_etl(connection):
    """Load only new artifacts"""
    latest_id = get_latest_objectid(connection)
    
    # Fetch only artifacts with objectid > latest_id
    # Process and load new records
    pass
```

### Error Handling in ETL

```python
def safe_etl_pipeline():
    """ETL with error handling and logging"""
    try:
        connection = get_db_connection()
        all_artifacts = []
        
        for page in range(1, 6):
            try:
                records, _ = fetch_artifacts(page=page)
                all_artifacts.extend(records)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                continue
        
        df_metadata = transform_artifact_metadata(all_artifacts)
        load_dataframe_to_sql(df_metadata, 'artifactmetadata', connection)
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
```

## Troubleshooting

### API Key Issues

```python
# Verify API key is loaded
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('HARVARD_API_KEY')
if not api_key:
    raise ValueError("HARVARD_API_KEY not found in environment variables")
```

### Database Connection Errors

```python
# Test database connection
def test_db_connection():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            print("✓ Database connection successful")
            connection.close()
    except Error as e:
        print(f"✗ Database connection failed: {e}")
```

### Missing Dependencies

```bash
# If import errors occur
pip install --upgrade streamlit pandas mysql-connector-python plotly requests python-dotenv
```

### Streamlit Port Already in Use

```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Large Dataset Memory Issues

```python
# Use chunked processing
def chunked_etl(chunk_size=100):
    """Process data in chunks to manage memory"""
    connection = get_db_connection()
    
    for page in range(1, 50):
        records, _ = fetch_artifacts(page=page, size=chunk_size)
        df = transform_artifact_metadata(records)
        load_dataframe_to_sql(df, 'artifactmetadata', connection)
        
    connection.close()
```

This skill enables AI agents to help developers build complete data engineering pipelines using the Harvard Art Museums API, from data extraction through visualization.
