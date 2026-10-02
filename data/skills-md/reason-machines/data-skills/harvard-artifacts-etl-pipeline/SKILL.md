---
name: harvard-artifacts-etl-pipeline
description: Build ETL pipelines and analytics dashboards using the Harvard Art Museums API with Streamlit, SQL, and Plotly
triggers:
  - how do I fetch data from Harvard Art Museums API
  - build an ETL pipeline for museum artifacts
  - create a Streamlit dashboard for art collection data
  - query Harvard museum artifacts with SQL
  - set up TiDB database for artifact metadata
  - visualize museum collection analytics
  - paginate through Harvard API results
  - transform nested JSON museum data to SQL tables
---

# Harvard Artifacts ETL Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI coding agents to help developers build end-to-end data engineering pipelines using the Harvard Art Museums API. The project demonstrates real-world ETL patterns, SQL database design, analytical queries, and interactive visualization using Streamlit.

## What This Project Does

The Harvard Artifacts Collection application:
- Fetches artifact data from Harvard Art Museums API with pagination
- Transforms nested JSON into relational database tables
- Loads data into MySQL/TiDB Cloud databases
- Executes analytical SQL queries on artifact metadata, media, and colors
- Visualizes results through interactive Plotly charts in Streamlit

**Architecture:** API → ETL → SQL → Analytics → Visualization

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
# Harvard API
HARVARD_API_KEY=your_api_key_here

# Database credentials
DB_HOST=gateway01.your-region.prod.aws.tidbcloud.com
DB_PORT=4000
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=artifacts_db
```

### Database Setup

```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Create database connection
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    department VARCHAR(200),
    classification VARCHAR(200),
    dated VARCHAR(200),
    url TEXT,
    totalpageviews INT,
    totaluniquepageviews INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    baseimageurl VARCHAR(500),
    format VARCHAR(50),
    height INT,
    width INT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    hue VARCHAR(50),
    percent FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
)
""")

conn.commit()
```

## Key API Patterns

### Fetching Artifacts with Pagination

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard API with pagination"""
    api_key = os.getenv('HARVARD_API_KEY')
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['records'], data['info']
    else:
        raise Exception(f"API Error: {response.status_code}")

# Fetch multiple pages
def fetch_all_artifacts(max_pages=10):
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        artifacts, info = fetch_artifacts(page=page)
        all_artifacts.extend(artifacts)
        
        # Check if more pages exist
        if page >= info['pages']:
            break
    
    return all_artifacts
```

### ETL Pipeline Implementation

```python
import pandas as pd

def extract_metadata(artifacts):
    """Extract artifact metadata"""
    metadata = []
    
    for artifact in artifacts:
        metadata.append({
            'id': artifact.get('id'),
            'title': artifact.get('title', '')[:500],
            'culture': artifact.get('culture', '')[:200],
            'century': artifact.get('century', '')[:100],
            'department': artifact.get('department', '')[:200],
            'classification': artifact.get('classification', '')[:200],
            'dated': artifact.get('dated', '')[:200],
            'url': artifact.get('url', ''),
            'totalpageviews': artifact.get('totalpageviews', 0),
            'totaluniquepageviews': artifact.get('totaluniquepageviews', 0)
        })
    
    return pd.DataFrame(metadata)

def extract_media(artifacts):
    """Extract media information"""
    media = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        primary_image = artifact.get('primaryimageurl')
        
        if primary_image:
            media.append({
                'artifact_id': artifact_id,
                'baseimageurl': primary_image,
                'format': 'image',
                'height': None,
                'width': None
            })
        
        # Extract images from images array
        for img in artifact.get('images', []):
            media.append({
                'artifact_id': artifact_id,
                'baseimageurl': img.get('baseimageurl', ''),
                'format': img.get('format', ''),
                'height': img.get('height'),
                'width': img.get('width')
            })
    
    return pd.DataFrame(media)

def extract_colors(artifacts):
    """Extract color information"""
    colors = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        
        for color in artifact.get('colors', []):
            colors.append({
                'artifact_id': artifact_id,
                'color': color.get('color', ''),
                'spectrum': color.get('spectrum', ''),
                'hue': color.get('hue', ''),
                'percent': color.get('percent', 0.0)
            })
    
    return pd.DataFrame(colors)
```

### Loading Data to SQL

```python
def load_to_sql(df, table_name, conn):
    """Batch insert DataFrame into SQL table"""
    cursor = conn.cursor()
    
    if df.empty:
        return
    
    # Build INSERT statement
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    
    insert_query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f"{col}=VALUES({col})" for col in df.columns if col != 'id'])}
    """
    
    # Convert DataFrame to list of tuples
    data = [tuple(row) for row in df.values]
    
    # Batch insert
    cursor.executemany(insert_query, data)
    conn.commit()
    
    print(f"Loaded {len(data)} records into {table_name}")

# Complete ETL process
def run_etl_pipeline(max_pages=5):
    artifacts = fetch_all_artifacts(max_pages=max_pages)
    
    # Extract
    metadata_df = extract_metadata(artifacts)
    media_df = extract_media(artifacts)
    colors_df = extract_colors(artifacts)
    
    # Load
    load_to_sql(metadata_df, 'artifactmetadata', conn)
    load_to_sql(media_df, 'artifactmedia', conn)
    load_to_sql(colors_df, 'artifactcolors', conn)
```

## Streamlit Dashboard Implementation

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

st.title("🏛️ Harvard Art Museums Analytics")

# Sidebar for ETL operations
st.sidebar.header("Data Collection")
pages_to_fetch = st.sidebar.slider("Pages to fetch", 1, 50, 5)

if st.sidebar.button("Run ETL Pipeline"):
    with st.spinner("Fetching and processing data..."):
        run_etl_pipeline(max_pages=pages_to_fetch)
        st.success("ETL completed successfully!")

# Analytics queries
st.header("📊 Analytics Dashboard")

queries = {
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL AND century != ''
        GROUP BY century
        ORDER BY count DESC
        LIMIT 20
    """,
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL AND culture != ''
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 15
    """,
    "Color Distribution": """
        SELECT color, COUNT(*) as count, AVG(percent) as avg_percent
        FROM artifactcolors
        GROUP BY color
        ORDER BY count DESC
        LIMIT 10
    """,
    "Media Availability": """
        SELECT 
            CASE WHEN m.artifact_id IS NOT NULL THEN 'Has Media' ELSE 'No Media' END as media_status,
            COUNT(*) as count
        FROM artifactmetadata a
        LEFT JOIN artifactmedia m ON a.id = m.artifact_id
        GROUP BY media_status
    """,
    "Top Viewed Artifacts": """
        SELECT title, totalpageviews, culture, century
        FROM artifactmetadata
        WHERE totalpageviews > 0
        ORDER BY totalpageviews DESC
        LIMIT 10
    """
}

query_choice = st.selectbox("Select Analysis", list(queries.keys()))

if st.button("Run Query"):
    cursor = conn.cursor()
    cursor.execute(queries[query_choice])
    
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    df = pd.DataFrame(results, columns=columns)
    
    st.subheader("Results")
    st.dataframe(df)
    
    # Auto-generate visualization
    if len(df.columns) >= 2:
        fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                     title=query_choice)
        st.plotly_chart(fig, use_container_width=True)
```

## Common Analytical Queries

```python
# Query: Artifacts with most colors
"""
SELECT a.title, COUNT(c.id) as color_count
FROM artifactmetadata a
JOIN artifactcolors c ON a.id = c.artifact_id
GROUP BY a.id, a.title
ORDER BY color_count DESC
LIMIT 10
"""

# Query: Department breakdown
"""
SELECT department, COUNT(*) as count,
       AVG(totalpageviews) as avg_views
FROM artifactmetadata
WHERE department IS NOT NULL
GROUP BY department
ORDER BY count DESC
"""

# Query: Dominant color per culture
"""
SELECT culture, color, SUM(percent) as total_percent
FROM artifactmetadata a
JOIN artifactcolors c ON a.id = c.artifact_id
WHERE culture IS NOT NULL
GROUP BY culture, color
ORDER BY culture, total_percent DESC
"""
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_retry(page, max_retries=3):
    for attempt in range(max_retries):
        try:
            return fetch_artifacts(page=page)
        except Exception as e:
            if "429" in str(e):  # Rate limit
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Database Connection Issues

```python
def get_connection():
    """Create database connection with error handling"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            connect_timeout=10
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None
```

### Handling Missing Data

```python
def safe_extract(artifact, key, default=''):
    """Safely extract nested data"""
    value = artifact.get(key, default)
    return value if value is not None else default

# Use in extraction
metadata.append({
    'id': artifact.get('id'),
    'title': safe_extract(artifact, 'title', 'Unknown'),
    'culture': safe_extract(artifact, 'culture', 'Unknown'),
    # ...
})
```

## Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will open at http://localhost:8501
```

This skill provides comprehensive guidance for building ETL pipelines with museum APIs, implementing SQL analytics, and creating interactive dashboards with Streamlit.
