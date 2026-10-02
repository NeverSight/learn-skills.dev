---
name: harvard-art-museums-data-pipeline
description: Build end-to-end data engineering pipelines with the Harvard Art Museums API, ETL processes, SQL analytics, and Streamlit visualization
triggers:
  - build a data pipeline for museum artifacts
  - create ETL workflow for Harvard Art Museums API
  - set up artifact data collection and analytics
  - implement museum data engineering pipeline
  - build streamlit dashboard for art museum data
  - create SQL analytics for artifact collections
  - extract and analyze Harvard museum artifacts
  - design data warehouse for art collections
---

# Harvard Art Museums Data Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables you to build production-ready data engineering pipelines using the Harvard Art Museums API. It covers ETL workflows, relational database design, SQL analytics, and interactive Streamlit dashboards for artifact data visualization.

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App demonstrates a complete data pipeline:

1. **Extract**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
2. **Transform**: Converts nested JSON into normalized relational tables
3. **Load**: Batch inserts data into MySQL/TiDB Cloud databases
4. **Analyze**: Executes analytical SQL queries for insights
5. **Visualize**: Renders interactive dashboards with Plotly and Streamlit

The architecture follows: `API → ETL → SQL → Analytics → Visualization`

## Installation

```bash
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```text
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
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=harvard_artifacts
```

### Get Harvard API Key

1. Visit [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)
2. Register for a free API key
3. Add to `.env` file

### Database Setup

```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Create tables
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Artifact metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(255),
            century VARCHAR(100),
            classification VARCHAR(255),
            department VARCHAR(255),
            technique VARCHAR(255),
            medium VARCHAR(500),
            dated VARCHAR(255),
            url TEXT,
            totalpageviews INT,
            totaluniquepageviews INT
        )
    """)
    
    # Artifact media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            iiifbaseuri VARCHAR(500),
            baseimageurl TEXT,
            primaryimageurl TEXT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    # Artifact colors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color VARCHAR(50),
            spectrum VARCHAR(50),
            hue VARCHAR(50),
            percent DECIMAL(5,2),
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
```

## API Integration

### Basic API Request

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
    return response.json()
```

### Paginated Data Collection

```python
def collect_all_artifacts(max_records=1000):
    """Collect artifacts with pagination handling"""
    all_artifacts = []
    page = 1
    size = 100
    
    while len(all_artifacts) < max_records:
        try:
            data = fetch_artifacts(page=page, size=size)
            records = data.get('records', [])
            
            if not records:
                break
                
            all_artifacts.extend(records)
            
            # Check if more pages available
            if data['info']['next'] is None:
                break
                
            page += 1
            
            # Rate limiting
            import time
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    return all_artifacts[:max_records]
```

## ETL Pipeline

### Extract and Transform

```python
import pandas as pd

def transform_artifact_metadata(artifacts):
    """Transform artifacts into metadata DataFrame"""
    metadata = []
    
    for artifact in artifacts:
        metadata.append({
            'id': artifact.get('id'),
            'title': artifact.get('title', 'Unknown')[:500],
            'culture': artifact.get('culture', 'Unknown')[:255],
            'century': artifact.get('century', 'Unknown')[:100],
            'classification': artifact.get('classification', 'Unknown')[:255],
            'department': artifact.get('department', 'Unknown')[:255],
            'technique': artifact.get('technique', 'Unknown')[:255],
            'medium': artifact.get('medium', 'Unknown')[:500],
            'dated': artifact.get('dated', 'Unknown')[:255],
            'url': artifact.get('url', ''),
            'totalpageviews': artifact.get('totalpageviews', 0),
            'totaluniquepageviews': artifact.get('totaluniquepageviews', 0)
        })
    
    return pd.DataFrame(metadata)

def transform_artifact_media(artifacts):
    """Transform artifacts into media DataFrame"""
    media = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        images = artifact.get('images', [])
        
        if images:
            primary_image = images[0]
            media.append({
                'artifact_id': artifact_id,
                'iiifbaseuri': primary_image.get('iiifbaseuri', ''),
                'baseimageurl': primary_image.get('baseimageurl', ''),
                'primaryimageurl': artifact.get('primaryimageurl', '')
            })
    
    return pd.DataFrame(media)

def transform_artifact_colors(artifacts):
    """Transform artifacts into colors DataFrame"""
    colors = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        color_list = artifact.get('colors', [])
        
        for color in color_list:
            colors.append({
                'artifact_id': artifact_id,
                'color': color.get('color', ''),
                'spectrum': color.get('spectrum', ''),
                'hue': color.get('hue', ''),
                'percent': color.get('percent', 0.0)
            })
    
    return pd.DataFrame(colors)
```

### Load into Database

```python
def load_metadata(df, conn):
    """Batch insert metadata into database"""
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO artifactmetadata 
        (id, title, culture, century, classification, department, 
         technique, medium, dated, url, totalpageviews, totaluniquepageviews)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title=VALUES(title), culture=VALUES(culture)
    """
    
    data = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data)
    conn.commit()
    cursor.close()

def run_etl_pipeline(max_records=1000):
    """Execute complete ETL pipeline"""
    # Extract
    print("Extracting artifacts from API...")
    artifacts = collect_all_artifacts(max_records)
    
    # Transform
    print("Transforming data...")
    df_metadata = transform_artifact_metadata(artifacts)
    df_media = transform_artifact_media(artifacts)
    df_colors = transform_artifact_colors(artifacts)
    
    # Load
    print("Loading into database...")
    conn = get_db_connection()
    load_metadata(df_metadata, conn)
    load_metadata(df_media, conn)  # Similar function for media
    load_metadata(df_colors, conn)  # Similar function for colors
    conn.close()
    
    print(f"ETL complete: {len(artifacts)} artifacts processed")
```

## SQL Analytics

### Sample Analytical Queries

```python
# Query 1: Artifacts by culture
QUERY_BY_CULTURE = """
    SELECT culture, COUNT(*) as count
    FROM artifactmetadata
    WHERE culture != 'Unknown'
    GROUP BY culture
    ORDER BY count DESC
    LIMIT 20
"""

# Query 2: Most viewed artifacts
QUERY_TOP_VIEWED = """
    SELECT title, culture, totalpageviews
    FROM artifactmetadata
    ORDER BY totalpageviews DESC
    LIMIT 10
"""

# Query 3: Artifacts by century
QUERY_BY_CENTURY = """
    SELECT century, COUNT(*) as count
    FROM artifactmetadata
    WHERE century != 'Unknown'
    GROUP BY century
    ORDER BY count DESC
"""

# Query 4: Color distribution
QUERY_COLOR_DISTRIBUTION = """
    SELECT color, COUNT(*) as count, AVG(percent) as avg_percent
    FROM artifactcolors
    GROUP BY color
    ORDER BY count DESC
    LIMIT 15
"""

# Query 5: Department statistics
QUERY_DEPARTMENT_STATS = """
    SELECT 
        department,
        COUNT(*) as total_artifacts,
        AVG(totalpageviews) as avg_views
    FROM artifactmetadata
    WHERE department != 'Unknown'
    GROUP BY department
    ORDER BY total_artifacts DESC
"""

def execute_query(query):
    """Execute SQL query and return DataFrame"""
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
```

## Streamlit Dashboard

### Main Application

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(
        page_title="Harvard Artifacts Analytics",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Data Collection", "SQL Analytics", "Visualizations"]
    )
    
    if page == "Data Collection":
        show_data_collection()
    elif page == "SQL Analytics":
        show_sql_analytics()
    elif page == "Visualizations":
        show_visualizations()

def show_data_collection():
    st.header("📥 Data Collection")
    
    num_records = st.number_input(
        "Number of records to collect",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100
    )
    
    if st.button("Start ETL Pipeline"):
        with st.spinner("Running ETL pipeline..."):
            run_etl_pipeline(num_records)
        st.success(f"Successfully collected {num_records} artifacts!")

def show_sql_analytics():
    st.header("📊 SQL Analytics")
    
    queries = {
        "Artifacts by Culture": QUERY_BY_CULTURE,
        "Most Viewed Artifacts": QUERY_TOP_VIEWED,
        "Artifacts by Century": QUERY_BY_CENTURY,
        "Color Distribution": QUERY_COLOR_DISTRIBUTION,
        "Department Statistics": QUERY_DEPARTMENT_STATS
    }
    
    selected_query = st.selectbox("Select Query", list(queries.keys()))
    
    if st.button("Execute Query"):
        df = execute_query(queries[selected_query])
        st.dataframe(df, use_container_width=True)
        
        # Auto-generate visualization
        if len(df.columns) >= 2:
            fig = px.bar(
                df, 
                x=df.columns[0], 
                y=df.columns[1],
                title=selected_query
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

### Run the Dashboard

```bash
streamlit run app.py
```

## Common Patterns

### Rate Limiting API Requests

```python
import time
from functools import wraps

def rate_limit(calls_per_second=2):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def fetch_artifact_by_id(artifact_id):
    """Fetch single artifact with rate limiting"""
    api_key = os.getenv('HARVARD_API_KEY')
    url = f"https://api.harvardartmuseums.org/object/{artifact_id}"
    response = requests.get(url, params={'apikey': api_key})
    return response.json()
```

### Error Handling and Retries

```python
from requests.exceptions import RequestException

def fetch_with_retry(url, params, max_retries=3):
    """Fetch with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            time.sleep(wait_time)
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("Database connection successful")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
```

### Memory Issues with Large Datasets

```python
def batch_process_artifacts(total_records, batch_size=100):
    """Process artifacts in batches to manage memory"""
    num_batches = (total_records + batch_size - 1) // batch_size
    
    for batch_num in range(num_batches):
        page = batch_num + 1
        artifacts = fetch_artifacts(page=page, size=batch_size)
        
        # Process batch
        df = transform_artifact_metadata(artifacts['records'])
        conn = get_db_connection()
        load_metadata(df, conn)
        conn.close()
        
        print(f"Processed batch {batch_num + 1}/{num_batches}")
```

### Streamlit Caching for Performance

```python
@st.cache_data(ttl=3600)
def cached_query_execution(query):
    """Cache query results for 1 hour"""
    return execute_query(query)

# Use in dashboard
df = cached_query_execution(QUERY_BY_CULTURE)
st.dataframe(df)
```
