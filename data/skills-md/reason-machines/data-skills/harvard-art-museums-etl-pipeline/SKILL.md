---
name: harvard-art-museums-etl-pipeline
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - how do I extract data from Harvard Art Museums API
  - build an ETL pipeline for museum artifacts
  - create a Streamlit dashboard for art collection data
  - query Harvard Art Museums API with pagination
  - design SQL schema for artifact metadata
  - visualize museum collection analytics with Plotly
  - transform nested JSON art data into relational tables
  - set up data engineering pipeline for cultural heritage data
---

# Harvard Art Museums ETL Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides an end-to-end data engineering solution for extracting, transforming, and analyzing artifacts from the Harvard Art Museums API. It demonstrates real-world ETL patterns, SQL analytics, and interactive visualization using Streamlit.

## What It Does

- **Extracts** artifact data from Harvard Art Museums API with pagination and rate limiting
- **Transforms** nested JSON into normalized relational tables (metadata, media, colors)
- **Loads** data into MySQL/TiDB Cloud with proper foreign key relationships
- **Analyzes** data using predefined SQL queries for cultural insights
- **Visualizes** results through interactive Plotly charts in a Streamlit dashboard

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Required packages
pip install streamlit pandas requests mysql-connector-python plotly python-dotenv
```

## Configuration

### API Key Setup

Get your Harvard Art Museums API key from: https://www.harvardartmuseums.org/collections/api

```python
# Store in environment variables
# .env file
HARVARD_API_KEY=your_api_key_here
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=harvard_artifacts
```

### Database Connection

```python
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create MySQL database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
```

## Database Schema

### Create Tables

```sql
-- Artifact Metadata Table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    period VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    department VARCHAR(255),
    dated VARCHAR(255),
    accession_year INT,
    primary_image_url TEXT,
    url TEXT
);

-- Artifact Media Table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    media_type VARCHAR(100),
    base_url TEXT,
    image_url TEXT,
    description TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id) ON DELETE CASCADE
);

-- Artifact Colors Table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    hex_code VARCHAR(10),
    percentage DECIMAL(5,2),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id) ON DELETE CASCADE
);
```

## Key API Patterns

### Extract: Fetch Artifacts with Pagination

```python
import requests
import os
from typing import List, Dict

def fetch_artifacts(api_key: str, num_pages: int = 5, page_size: int = 100) -> List[Dict]:
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    
    Args:
        api_key: Harvard API key from environment
        num_pages: Number of pages to fetch
        page_size: Records per page (max 100)
    
    Returns:
        List of artifact dictionaries
    """
    base_url = "https://api.harvardartmuseums.org/object"
    all_artifacts = []
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': api_key,
            'size': page_size,
            'page': page,
            'hasimage': 1  # Only artifacts with images
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            records = data.get('records', [])
            all_artifacts.extend(records)
            
            print(f"Fetched page {page}: {len(records)} artifacts")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    return all_artifacts
```

### Transform: Normalize Nested JSON

```python
import pandas as pd
from typing import List, Dict, Tuple

def transform_artifacts(raw_data: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Transform raw API data into normalized dataframes
    
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
            'period': artifact.get('period', '')[:255],
            'century': artifact.get('century', '')[:100],
            'classification': artifact.get('classification', '')[:255],
            'department': artifact.get('department', '')[:255],
            'dated': artifact.get('dated', '')[:255],
            'accession_year': artifact.get('accessionyear'),
            'primary_image_url': artifact.get('primaryimageurl', ''),
            'url': artifact.get('url', '')
        }
        metadata_list.append(metadata)
        
        # Extract media
        images = artifact.get('images', [])
        for img in images:
            media = {
                'artifact_id': artifact.get('id'),
                'media_type': 'image',
                'base_url': img.get('baseimageurl', ''),
                'image_url': img.get('iiifbaseuri', ''),
                'description': img.get('description', '')[:1000] if img.get('description') else None
            }
            media_list.append(media)
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_data = {
                'artifact_id': artifact.get('id'),
                'color': color.get('color', ''),
                'hex_code': color.get('hex', ''),
                'percentage': color.get('percent', 0)
            }
            colors_list.append(color_data)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### Load: Batch Insert into Database

```python
from typing import List
import mysql.connector

def load_metadata(df: pd.DataFrame, connection):
    """Load artifact metadata with batch insert"""
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO artifactmetadata 
    (id, title, culture, period, century, classification, department, 
     dated, accession_year, primary_image_url, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    title=VALUES(title), culture=VALUES(culture), period=VALUES(period)
    """
    
    # Convert dataframe to list of tuples
    data = [tuple(row) for row in df.values]
    
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Inserted {cursor.rowcount} metadata records")

def load_media(df: pd.DataFrame, connection):
    """Load artifact media"""
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO artifactmedia 
    (artifact_id, media_type, base_url, image_url, description)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    data = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Inserted {cursor.rowcount} media records")

def load_colors(df: pd.DataFrame, connection):
    """Load artifact colors"""
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO artifactcolors 
    (artifact_id, color, hex_code, percentage)
    VALUES (%s, %s, %s, %s)
    """
    
    data = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Inserted {cursor.rowcount} color records")
```

## Streamlit Dashboard

### Main Application Structure

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Harvard Art Museums Analytics",
    page_icon="🎨",
    layout="wide"
)

def main():
    st.title("🎨 Harvard Art Museums Analytics Dashboard")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["ETL Pipeline", "SQL Analytics", "Visualizations"]
    )
    
    if page == "ETL Pipeline":
        show_etl_page()
    elif page == "SQL Analytics":
        show_analytics_page()
    else:
        show_visualizations_page()

if __name__ == "__main__":
    main()
```

### ETL Pipeline Page

```python
def show_etl_page():
    st.header("ETL Pipeline")
    
    api_key = st.text_input("Harvard API Key", type="password", 
                            value=os.getenv('HARVARD_API_KEY', ''))
    
    col1, col2 = st.columns(2)
    with col1:
        num_pages = st.number_input("Number of pages", min_value=1, max_value=100, value=5)
    with col2:
        page_size = st.number_input("Page size", min_value=10, max_value=100, value=100)
    
    if st.button("🚀 Run ETL Pipeline"):
        with st.spinner("Extracting data from API..."):
            raw_data = fetch_artifacts(api_key, num_pages, page_size)
            st.success(f"✅ Extracted {len(raw_data)} artifacts")
        
        with st.spinner("Transforming data..."):
            metadata_df, media_df, colors_df = transform_artifacts(raw_data)
            st.success(f"✅ Transformed into {len(metadata_df)} metadata, {len(media_df)} media, {len(colors_df)} color records")
        
        with st.spinner("Loading into database..."):
            conn = get_db_connection()
            load_metadata(metadata_df, conn)
            load_media(media_df, conn)
            load_colors(colors_df, conn)
            conn.close()
            st.success("✅ Data loaded successfully!")
        
        # Show preview
        st.subheader("Data Preview")
        st.dataframe(metadata_df.head(10))
```

## Analytics Queries

### Common SQL Query Patterns

```python
# Top 10 cultures by artifact count
QUERY_TOP_CULTURES = """
SELECT culture, COUNT(*) as artifact_count
FROM artifactmetadata
WHERE culture IS NOT NULL AND culture != ''
GROUP BY culture
ORDER BY artifact_count DESC
LIMIT 10;
"""

# Artifacts by century
QUERY_BY_CENTURY = """
SELECT century, COUNT(*) as count
FROM artifactmetadata
WHERE century IS NOT NULL
GROUP BY century
ORDER BY count DESC;
"""

# Department distribution
QUERY_BY_DEPARTMENT = """
SELECT department, COUNT(*) as count
FROM artifactmetadata
WHERE department IS NOT NULL
GROUP BY department
ORDER BY count DESC;
"""

# Most common colors
QUERY_TOP_COLORS = """
SELECT color, COUNT(*) as frequency, AVG(percentage) as avg_percentage
FROM artifactcolors
GROUP BY color
ORDER BY frequency DESC
LIMIT 15;
"""

# Artifacts with most images
QUERY_MOST_IMAGES = """
SELECT m.title, m.culture, COUNT(med.media_id) as image_count
FROM artifactmetadata m
JOIN artifactmedia med ON m.id = med.artifact_id
GROUP BY m.id, m.title, m.culture
ORDER BY image_count DESC
LIMIT 10;
"""

def execute_query(query: str, connection) -> pd.DataFrame:
    """Execute SQL query and return results as DataFrame"""
    return pd.read_sql(query, connection)
```

### Analytics Dashboard Page

```python
def show_analytics_page():
    st.header("📊 SQL Analytics")
    
    queries = {
        "Top 10 Cultures": QUERY_TOP_CULTURES,
        "Artifacts by Century": QUERY_BY_CENTURY,
        "Department Distribution": QUERY_BY_DEPARTMENT,
        "Most Common Colors": QUERY_TOP_COLORS,
        "Artifacts with Most Images": QUERY_MOST_IMAGES
    }
    
    selected_query = st.selectbox("Select Analysis", list(queries.keys()))
    
    if st.button("Run Query"):
        conn = get_db_connection()
        df = execute_query(queries[selected_query], conn)
        conn.close()
        
        st.subheader("Query Results")
        st.dataframe(df)
        
        # Auto-generate visualization
        if len(df.columns) >= 2:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                        title=selected_query)
            st.plotly_chart(fig, use_container_width=True)
```

## Visualization Patterns

### Create Interactive Charts

```python
import plotly.express as px
import plotly.graph_objects as go

def create_culture_chart(df: pd.DataFrame):
    """Bar chart for culture distribution"""
    fig = px.bar(
        df, 
        x='culture', 
        y='artifact_count',
        title='Top Cultures in Collection',
        labels={'artifact_count': 'Number of Artifacts', 'culture': 'Culture'},
        color='artifact_count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_century_timeline(df: pd.DataFrame):
    """Timeline visualization for centuries"""
    fig = px.line(
        df, 
        x='century', 
        y='count',
        title='Artifact Distribution Across Centuries',
        markers=True
    )
    return fig

def create_color_pie_chart(df: pd.DataFrame):
    """Pie chart for color distribution"""
    fig = px.pie(
        df, 
        values='frequency', 
        names='color',
        title='Most Common Colors in Artifacts',
        hole=0.3
    )
    return fig
```

## Complete ETL Workflow

```python
from dotenv import load_dotenv
import os

def run_complete_etl():
    """Complete ETL pipeline execution"""
    load_dotenv()
    
    # 1. Extract
    print("Starting extraction...")
    api_key = os.getenv('HARVARD_API_KEY')
    raw_data = fetch_artifacts(api_key, num_pages=10, page_size=100)
    print(f"Extracted {len(raw_data)} artifacts")
    
    # 2. Transform
    print("Transforming data...")
    metadata_df, media_df, colors_df = transform_artifacts(raw_data)
    
    # Data quality checks
    print(f"Metadata records: {len(metadata_df)}")
    print(f"Media records: {len(media_df)}")
    print(f"Color records: {len(colors_df)}")
    print(f"Null values in metadata:\n{metadata_df.isnull().sum()}")
    
    # 3. Load
    print("Loading to database...")
    conn = get_db_connection()
    
    try:
        load_metadata(metadata_df, conn)
        load_media(media_df, conn)
        load_colors(colors_df, conn)
        print("ETL pipeline completed successfully!")
    except Exception as e:
        print(f"Error during load: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_complete_etl()
```

## Troubleshooting

### API Rate Limiting

```python
import time
from requests.exceptions import HTTPError

def fetch_with_retry(url, params, max_retries=3):
    """Fetch with exponential backoff for rate limiting"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                wait_time = (2 ** attempt) * 5  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Database Connection Issues

```python
import mysql.connector
from mysql.connector import Error

def safe_db_connection():
    """Create database connection with error handling"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            connect_timeout=10,
            autocommit=False
        )
        if connection.is_connected():
            print("Database connection successful")
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None
```

### Handling Missing Data

```python
def clean_artifact_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate artifact data"""
    # Replace empty strings with None
    df = df.replace('', None)
    
    # Handle missing titles
    df['title'] = df['title'].fillna('Untitled')
    
    # Ensure numeric fields
    df['accession_year'] = pd.to_numeric(df['accession_year'], errors='coerce')
    
    # Truncate long text fields
    df['title'] = df['title'].str[:500]
    df['culture'] = df['culture'].str[:255]
    
    return df
```

## Running the Application

```bash
# Start Streamlit dashboard
streamlit run app.py

# Run ETL pipeline only
python etl_pipeline.py

# Run with custom configuration
HARVARD_API_KEY=your_key DB_HOST=localhost streamlit run app.py
```

This skill enables AI agents to help developers build complete ETL pipelines for cultural heritage data, from API extraction through SQL analytics to interactive visualization.
