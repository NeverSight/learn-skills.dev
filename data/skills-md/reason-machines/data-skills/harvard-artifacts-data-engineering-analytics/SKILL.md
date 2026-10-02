---
name: harvard-artifacts-data-engineering-analytics
description: Build end-to-end ETL pipelines and analytics dashboards using the Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - how do I build a data pipeline with Harvard Art Museums API
  - create an ETL pipeline for museum artifacts data
  - set up analytics dashboard for Harvard art collection
  - extract and transform Harvard museum data into SQL
  - build Streamlit app for art artifacts analytics
  - visualize Harvard Art Museums data with SQL queries
  - implement artifact collection data engineering pipeline
  - analyze museum artifact metadata with Python and SQL
---

# Harvard Artifacts Data Engineering Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection

This project provides an end-to-end data engineering and analytics application for the Harvard Art Museums API. It demonstrates real-world ETL pipelines, SQL database design, analytical queries, and interactive visualization using Streamlit.

## What This Project Does

The application implements a complete data pipeline:
- **Extract**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
- **Transform**: Processes nested JSON into relational database tables (metadata, media, colors)
- **Load**: Batch inserts transformed data into MySQL/TiDB Cloud
- **Analyze**: Executes 20+ predefined SQL queries for insights
- **Visualize**: Renders interactive dashboards with Plotly charts in Streamlit

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
export DB_NAME="harvard_artifacts"
```

## Configuration

### API Key Setup

Obtain an API key from [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api):

```python
import os
import requests

API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"

# Test API connection
response = requests.get(f"{BASE_URL}?apikey={API_KEY}&size=1")
if response.status_code == 200:
    print("API connection successful")
```

### Database Configuration

```python
import mysql.connector
import os

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
```

## Database Schema

The project uses three main tables:

```sql
-- Artifact metadata table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    department VARCHAR(255),
    dated VARCHAR(255),
    technique VARCHAR(500),
    medium VARCHAR(500),
    period VARCHAR(255),
    provenance TEXT,
    creditline TEXT,
    accession_number VARCHAR(255),
    division VARCHAR(255)
);

-- Artifact media table
CREATE TABLE artifactmedia (
    artifact_id INT,
    baseimageurl VARCHAR(500),
    primaryimageurl VARCHAR(500),
    has_image BOOLEAN,
    total_images INT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    artifact_id INT,
    color VARCHAR(50),
    percentage FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## ETL Pipeline Implementation

### Extract Phase

```python
import requests
import time

def fetch_artifacts(api_key, page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API with pagination"""
    url = f"https://api.harvardartmuseums.org/object"
    params = {
        'apikey': api_key,
        'page': page,
        'size': size
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    # Rate limiting
    time.sleep(0.5)
    
    return response.json()

def extract_all_artifacts(api_key, max_pages=10):
    """Extract multiple pages of artifact data"""
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        data = fetch_artifacts(api_key, page=page)
        artifacts = data.get('records', [])
        all_artifacts.extend(artifacts)
        
        if not artifacts:
            break
    
    return all_artifacts
```

### Transform Phase

```python
import pandas as pd

def transform_artifacts(raw_artifacts):
    """Transform raw API data into structured dataframes"""
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_artifacts:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'period': artifact.get('period'),
            'provenance': artifact.get('provenance'),
            'creditline': artifact.get('creditline'),
            'accession_number': artifact.get('accessionyear'),
            'division': artifact.get('division')
        }
        metadata_list.append(metadata)
        
        # Extract media information
        media = {
            'artifact_id': artifact.get('id'),
            'baseimageurl': artifact.get('baseimageurl'),
            'primaryimageurl': artifact.get('primaryimageurl'),
            'has_image': 1 if artifact.get('primaryimageurl') else 0,
            'total_images': artifact.get('totalpageviews', 0)
        }
        media_list.append(media)
        
        # Extract color data
        colors = artifact.get('colors', [])
        for color in colors:
            color_data = {
                'artifact_id': artifact.get('id'),
                'color': color.get('color'),
                'percentage': color.get('percent')
            }
            colors_list.append(color_data)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### Load Phase

```python
def load_to_database(metadata_df, media_df, colors_df, db_config):
    """Batch insert dataframes into MySQL database"""
    import mysql.connector
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Load metadata
    for _, row in metadata_df.iterrows():
        query = """
        INSERT INTO artifactmetadata 
        (id, title, culture, century, classification, department, dated, 
         technique, medium, period, provenance, creditline, accession_number, division)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        cursor.execute(query, tuple(row))
    
    # Load media
    for _, row in media_df.iterrows():
        query = """
        INSERT INTO artifactmedia 
        (artifact_id, baseimageurl, primaryimageurl, has_image, total_images)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, tuple(row))
    
    # Load colors
    for _, row in colors_df.iterrows():
        query = """
        INSERT INTO artifactcolors 
        (artifact_id, color, percentage)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()
```

## Streamlit Application

### Main App Structure

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import os

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

# Sidebar configuration
st.sidebar.title("Harvard Art Museums Analytics")
st.sidebar.markdown("### Configuration")

# Database connection
@st.cache_resource
def get_database_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    conn = get_database_connection()
    df = pd.read_sql(query, conn)
    return df

# Main content
st.title("🎨 Harvard Art Museums Collection Analytics")

# ETL Pipeline Section
if st.sidebar.button("Run ETL Pipeline"):
    with st.spinner("Fetching data from API..."):
        api_key = os.getenv('HARVARD_API_KEY')
        artifacts = extract_all_artifacts(api_key, max_pages=5)
        st.success(f"Extracted {len(artifacts)} artifacts")
    
    with st.spinner("Transforming data..."):
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        st.success("Data transformation complete")
    
    with st.spinner("Loading to database..."):
        db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }
        load_to_database(metadata_df, media_df, colors_df, db_config)
        st.success("Data loaded successfully!")
```

### Analytics Queries

```python
# Predefined analytical queries
QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 15
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Top Colors Used": """
        SELECT color, COUNT(*) as frequency, AVG(percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color
        ORDER BY frequency DESC
        LIMIT 10
    """,
    
    "Media Availability": """
        SELECT 
            has_image,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
        FROM artifactmedia
        GROUP BY has_image
    """,
    
    "Artifacts by Department": """
        SELECT department, COUNT(*) as total_artifacts
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY total_artifacts DESC
    """
}

# Query selector
query_name = st.selectbox("Select Analysis", list(QUERIES.keys()))

if st.button("Run Query"):
    df = execute_query(QUERIES[query_name])
    
    # Display results
    st.dataframe(df)
    
    # Auto-generate visualization
    if len(df.columns) >= 2:
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                     title=query_name)
        st.plotly_chart(fig, use_container_width=True)
```

## Common Patterns

### Pattern 1: Incremental Data Loading

```python
def get_latest_artifact_id(cursor):
    """Get the most recent artifact ID in database"""
    cursor.execute("SELECT MAX(id) FROM artifactmetadata")
    result = cursor.fetchone()
    return result[0] if result[0] else 0

def incremental_etl(api_key, db_config):
    """Load only new artifacts since last ETL run"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    latest_id = get_latest_artifact_id(cursor)
    
    # Fetch only newer artifacts
    artifacts = fetch_artifacts(api_key, size=100)
    new_artifacts = [a for a in artifacts if a.get('id', 0) > latest_id]
    
    if new_artifacts:
        metadata_df, media_df, colors_df = transform_artifacts(new_artifacts)
        load_to_database(metadata_df, media_df, colors_df, db_config)
    
    cursor.close()
    conn.close()
```

### Pattern 2: Error Handling and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_fetch_artifacts(api_key, page=1, max_retries=3):
    """Fetch with retry logic"""
    for attempt in range(max_retries):
        try:
            data = fetch_artifacts(api_key, page)
            logger.info(f"Successfully fetched page {page}")
            return data
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# Access the dashboard at http://localhost:8501
```

## Troubleshooting

**API Rate Limiting**: If you encounter 429 errors, increase the sleep time between requests:
```python
time.sleep(1)  # Increase from 0.5 to 1 second
```

**Database Connection Issues**: Verify environment variables are set:
```python
import os
print(f"DB Host: {os.getenv('DB_HOST')}")
print(f"DB User: {os.getenv('DB_USER')}")
```

**Missing Data Fields**: Handle None values in transformations:
```python
metadata = {
    'title': artifact.get('title', 'Unknown'),
    'culture': artifact.get('culture') or 'Unknown'
}
```

**Memory Issues with Large Datasets**: Use batch processing:
```python
BATCH_SIZE = 1000
for i in range(0, len(metadata_df), BATCH_SIZE):
    batch = metadata_df.iloc[i:i+BATCH_SIZE]
    load_batch(batch, db_config)
```
