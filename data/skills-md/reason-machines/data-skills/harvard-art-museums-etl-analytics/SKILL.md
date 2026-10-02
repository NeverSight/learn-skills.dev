---
name: harvard-art-museums-etl-analytics
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - build an ETL pipeline for Harvard Art Museums data
  - create analytics dashboard with museum artifact data
  - extract and transform Harvard museum API data
  - set up data engineering pipeline for art collections
  - visualize Harvard Art Museums data with Streamlit
  - query and analyze museum artifacts with SQL
  - implement data pipeline for cultural heritage data
  - process Harvard Art Museums API with Python
---

# Harvard Art Museums ETL Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI coding agents to build end-to-end data engineering and analytics applications using the Harvard Art Museums API. The project demonstrates real-world ETL pipelines, SQL analytics, and interactive data visualization using Streamlit.

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App provides:

- **API Integration**: Collect artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load artifact metadata, media details, and color data
- **SQL Storage**: Store structured data in MySQL/TiDB Cloud with proper relational schema
- **Analytics Engine**: Execute 20+ predefined analytical SQL queries
- **Interactive Dashboards**: Visualize query results using Streamlit and Plotly

The architecture follows: **API → ETL → SQL → Analytics → Visualization**

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

### Environment Variables

Create a `.env` file in the project root:

```bash
# Harvard Art Museums API
HARVARD_API_KEY=your_api_key_here

# Database Configuration
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=harvard_artifacts
```

### Database Setup

```python
import mysql.connector
from mysql.connector import Error

def create_database_schema():
    """Initialize database schema for Harvard artifacts"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = connection.cursor()
    
    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
    cursor.execute(f"USE {os.getenv('DB_NAME')}")
    
    # Create artifact metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(255),
            century VARCHAR(100),
            classification VARCHAR(255),
            department VARCHAR(255),
            dated VARCHAR(255),
            period VARCHAR(255),
            technique VARCHAR(500),
            description TEXT,
            url VARCHAR(500),
            dated_end INT,
            dated_begin INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create artifact media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            media_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            image_url VARCHAR(500),
            media_type VARCHAR(100),
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    # Create artifact colors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            color_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color_hex VARCHAR(10),
            color_percentage FLOAT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
```

## ETL Pipeline Implementation

### Extract: Fetch Data from API

```python
import requests
import os
from typing import List, Dict

def fetch_artifacts(page: int = 1, size: int = 100) -> Dict:
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    
    Args:
        page: Page number (1-indexed)
        size: Number of records per page (max 100)
    
    Returns:
        JSON response containing artifact records
    """
    api_key = os.getenv('HARVARD_API_KEY')
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only fetch artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()

def extract_all_artifacts(max_records: int = 1000) -> List[Dict]:
    """
    Extract multiple pages of artifacts with rate limiting
    
    Args:
        max_records: Maximum number of records to fetch
    
    Returns:
        List of artifact dictionaries
    """
    import time
    
    artifacts = []
    page = 1
    page_size = 100
    
    while len(artifacts) < max_records:
        try:
            data = fetch_artifacts(page=page, size=page_size)
            
            if 'records' not in data or len(data['records']) == 0:
                break
            
            artifacts.extend(data['records'])
            page += 1
            
            # Rate limiting: Harvard API allows 2500 requests/day
            time.sleep(0.5)
            
            print(f"Fetched {len(artifacts)} artifacts...")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    return artifacts[:max_records]
```

### Transform: Clean and Structure Data

```python
import pandas as pd

def transform_artifacts(raw_artifacts: List[Dict]) -> tuple:
    """
    Transform raw API data into structured dataframes
    
    Returns:
        Tuple of (metadata_df, media_df, colors_df)
    """
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in raw_artifacts:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title', ''),
            'culture': artifact.get('culture', ''),
            'century': artifact.get('century', ''),
            'classification': artifact.get('classification', ''),
            'department': artifact.get('department', ''),
            'dated': artifact.get('dated', ''),
            'period': artifact.get('period', ''),
            'technique': artifact.get('technique', ''),
            'description': artifact.get('description', ''),
            'url': artifact.get('url', ''),
            'dated_begin': artifact.get('datebegin'),
            'dated_end': artifact.get('dateend')
        }
        metadata_records.append(metadata)
        
        # Extract media/images
        if 'images' in artifact and artifact['images']:
            for image in artifact['images']:
                media_records.append({
                    'artifact_id': artifact.get('id'),
                    'image_url': image.get('baseimageurl', ''),
                    'media_type': 'image'
                })
        
        # Extract color data
        if 'colors' in artifact and artifact['colors']:
            for color in artifact['colors']:
                color_records.append({
                    'artifact_id': artifact.get('id'),
                    'color_hex': color.get('hex', ''),
                    'color_percentage': color.get('percent', 0.0)
                })
    
    metadata_df = pd.DataFrame(metadata_records)
    media_df = pd.DataFrame(media_records)
    colors_df = pd.DataFrame(color_records)
    
    return metadata_df, media_df, colors_df
```

### Load: Insert into SQL Database

```python
def load_to_database(metadata_df: pd.DataFrame, 
                     media_df: pd.DataFrame, 
                     colors_df: pd.DataFrame):
    """
    Load transformed data into MySQL database using batch inserts
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
    cursor = connection.cursor()
    
    # Load metadata (batch insert)
    metadata_query = """
        INSERT INTO artifactmetadata 
        (id, title, culture, century, classification, department, 
         dated, period, technique, description, url, dated_begin, dated_end)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title=VALUES(title), culture=VALUES(culture)
    """
    
    metadata_values = [tuple(row) for row in metadata_df.values]
    cursor.executemany(metadata_query, metadata_values)
    
    # Load media
    if not media_df.empty:
        media_query = """
            INSERT INTO artifactmedia (artifact_id, image_url, media_type)
            VALUES (%s, %s, %s)
        """
        media_values = [tuple(row) for row in media_df.values]
        cursor.executemany(media_query, media_values)
    
    # Load colors
    if not colors_df.empty:
        colors_query = """
            INSERT INTO artifactcolors (artifact_id, color_hex, color_percentage)
            VALUES (%s, %s, %s)
        """
        colors_values = [tuple(row) for row in colors_df.values]
        cursor.executemany(colors_query, colors_values)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"Loaded {len(metadata_df)} artifacts to database")
```

## Analytics Queries

### Sample SQL Queries

```python
ANALYTICS_QUERIES = {
    "artifacts_by_culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL AND culture != ''
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 15
    """,
    
    "artifacts_by_century": """
        SELECT century, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE century IS NOT NULL AND century != ''
        GROUP BY century
        ORDER BY artifact_count DESC
    """,
    
    "department_distribution": """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY artifact_count DESC
    """,
    
    "top_colors": """
        SELECT color_hex, COUNT(*) as usage_count,
               AVG(color_percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color_hex
        ORDER BY usage_count DESC
        LIMIT 20
    """,
    
    "media_availability": """
        SELECT 
            COUNT(DISTINCT m.artifact_id) as artifacts_with_media,
            COUNT(*) as total_media_items,
            AVG(images_per_artifact) as avg_images_per_artifact
        FROM (
            SELECT artifact_id, COUNT(*) as images_per_artifact
            FROM artifactmedia
            GROUP BY artifact_id
        ) as images_count
        JOIN artifactmedia m ON m.artifact_id = images_count.artifact_id
    """,
    
    "temporal_analysis": """
        SELECT 
            FLOOR(dated_begin / 100) * 100 as century_start,
            COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE dated_begin IS NOT NULL
        GROUP BY century_start
        ORDER BY century_start
    """
}

def execute_analytics_query(query_name: str) -> pd.DataFrame:
    """Execute a predefined analytics query and return results"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    query = ANALYTICS_QUERIES.get(query_name)
    df = pd.read_sql(query, connection)
    connection.close()
    
    return df
```

## Streamlit Application

### Main Application Structure

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(
        page_title="Harvard Art Museums Analytics",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Harvard Art Museums - Data Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Data Collection", "Analytics Dashboard", "Query Explorer"]
    )
    
    if page == "Data Collection":
        show_data_collection_page()
    elif page == "Analytics Dashboard":
        show_analytics_dashboard()
    else:
        show_query_explorer()

def show_data_collection_page():
    """Page for triggering ETL pipeline"""
    st.header("📥 Data Collection")
    
    num_records = st.number_input(
        "Number of artifacts to collect",
        min_value=100,
        max_value=5000,
        value=500,
        step=100
    )
    
    if st.button("Start ETL Pipeline"):
        with st.spinner("Extracting data from API..."):
            raw_data = extract_all_artifacts(max_records=num_records)
            st.success(f"✅ Extracted {len(raw_data)} artifacts")
        
        with st.spinner("Transforming data..."):
            metadata_df, media_df, colors_df = transform_artifacts(raw_data)
            st.success(f"✅ Transformed into {len(metadata_df)} metadata records")
        
        with st.spinner("Loading into database..."):
            load_to_database(metadata_df, media_df, colors_df)
            st.success("✅ Data loaded successfully!")
        
        # Show sample data
        st.subheader("Sample Data Preview")
        st.dataframe(metadata_df.head(10))

def show_analytics_dashboard():
    """Pre-built analytics visualizations"""
    st.header("📊 Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Artifacts by Culture")
        df = execute_analytics_query("artifacts_by_culture")
        fig = px.bar(df, x='culture', y='artifact_count', 
                     color='artifact_count', color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Department Distribution")
        df = execute_analytics_query("department_distribution")
        fig = px.pie(df, names='department', values='artifact_count')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Temporal Distribution")
    df = execute_analytics_query("temporal_analysis")
    fig = px.line(df, x='century_start', y='artifact_count',
                  markers=True, line_shape='spline')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top Colors in Collection")
    df = execute_analytics_query("top_colors")
    fig = go.Figure(data=[go.Bar(
        x=df['color_hex'],
        y=df['usage_count'],
        marker_color=['#' + hex for hex in df['color_hex']]
    )])
    st.plotly_chart(fig, use_container_width=True)

def show_query_explorer():
    """Custom query execution interface"""
    st.header("🔍 Query Explorer")
    
    query_choice = st.selectbox(
        "Select a query",
        list(ANALYTICS_QUERIES.keys())
    )
    
    st.code(ANALYTICS_QUERIES[query_choice], language='sql')
    
    if st.button("Execute Query"):
        df = execute_analytics_query(query_choice)
        st.dataframe(df)
        
        # Auto-generate visualization if appropriate
        if len(df.columns) == 2 and df.shape[0] > 0:
            col1_name, col2_name = df.columns
            fig = px.bar(df, x=col1_name, y=col2_name)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

### Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# Access at http://localhost:8501
```

## Common Patterns

### Rate-Limited API Calls

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=120):
    """Decorator to rate limit API calls"""
    min_interval = 60.0 / calls_per_minute
    
    def decorator(func):
        last_called = [0.0]
        
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

@rate_limit(calls_per_minute=100)
def fetch_artifact_by_id(artifact_id: int) -> Dict:
    """Fetch single artifact with rate limiting"""
    api_key = os.getenv('HARVARD_API_KEY')
    url = f"https://api.harvardartmuseums.org/object/{artifact_id}"
    response = requests.get(url, params={'apikey': api_key})
    return response.json()
```

### Incremental Data Loading

```python
def get_last_loaded_id() -> int:
    """Get the highest artifact ID already in database"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM artifactmetadata")
    result = cursor.fetchone()[0]
    connection.close()
    
    return result if result else 0

def incremental_etl():
    """Load only new artifacts since last run"""
    last_id = get_last_loaded_id()
    
    # Fetch artifacts with ID > last_id
    new_artifacts = fetch_artifacts_after_id(last_id)
    
    if new_artifacts:
        metadata_df, media_df, colors_df = transform_artifacts(new_artifacts)
        load_to_database(metadata_df, media_df, colors_df)
        print(f"Loaded {len(new_artifacts)} new artifacts")
    else:
        print("No new artifacts to load")
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

# Test API connection
response = requests.get(
    "https://api.harvardartmuseums.org/object",
    params={'apikey': api_key, 'size': 1}
)
print(f"API Status: {response.status_code}")
```

### Database Connection Errors

```python
def test_database_connection():
    """Test database connectivity"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            connect_timeout=10
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        print("✅ Database connection successful")
        return True
        
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
```

### Handling Missing Data

```python
def safe_transform(artifact: Dict) -> Dict:
    """Transform with null handling"""
    return {
        'id': artifact.get('id'),
        'title': artifact.get('title') or 'Untitled',
        'culture': artifact.get('culture') or 'Unknown',
        'century': artifact.get('century') or 'Unknown',
        'classification': artifact.get('classification') or 'Unclassified',
        'department': artifact.get('department') or 'General Collection',
        'description': (artifact.get('description') or '')[:5000],  # Truncate long text
        'dated_begin': artifact.get('datebegin') if isinstance(artifact.get('datebegin'), int) else None,
        'dated_end': artifact.get('dateend') if isinstance(artifact.get('dateend'), int) else None
    }
```

### Memory Management for Large Datasets

```python
def chunked_etl(total_records: int, chunk_size: int = 500):
    """Process large datasets in chunks to manage memory"""
    num_chunks = (total_records + chunk_size - 1) // chunk_size
    
    for chunk_num in range(num_chunks):
        start_idx = chunk_num * chunk_size
        end_idx = min(start_idx + chunk_size, total_records)
        
        print(f"Processing chunk {chunk_num + 1}/{num_chunks}")
        
        # Extract chunk
        artifacts = extract_all_artifacts_range(start_idx, end_idx)
        
        # Transform and load immediately
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        load_to_database(metadata_df, media_df, colors_df)
        
        # Clear memory
        del artifacts, metadata_df, media_df, colors_df
```

This skill provides comprehensive guidance for building ETL pipelines and analytics applications with the Harvard Art Museums API using Python, SQL, and Streamlit.
