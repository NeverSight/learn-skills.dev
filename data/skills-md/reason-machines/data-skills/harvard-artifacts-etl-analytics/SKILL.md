---
name: harvard-artifacts-etl-analytics
description: Build ETL pipelines and analytics dashboards for Harvard Art Museums API data with Python, SQL, and Streamlit
triggers:
  - how do I extract data from Harvard Art Museums API
  - create an ETL pipeline for museum artifact data
  - build a Streamlit dashboard for art collection analytics
  - query Harvard artifacts database with SQL
  - visualize museum collection data with Plotly
  - set up data engineering pipeline for art museum data
  - transform Harvard API JSON into relational database
  - analyze artifact metadata by culture and century
---

# Harvard Artifacts ETL Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI coding agents to help developers build end-to-end ETL pipelines and analytics applications using the Harvard Art Museums API. The project demonstrates real-world data engineering patterns including API integration, data transformation, SQL database design, and interactive visualization with Streamlit.

## What This Project Does

The Harvard Artifacts Collection application:
- Extracts artifact data from Harvard Art Museums API with pagination and rate limiting
- Transforms nested JSON into normalized relational tables
- Loads data into MySQL/TiDB Cloud databases
- Provides 20+ predefined analytical SQL queries
- Visualizes results with interactive Plotly charts in Streamlit

**Architecture Flow:** API → ETL → SQL → Analytics → Visualization

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required packages:**
```txt
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

# Database Connection
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=harvard_artifacts
```

### Get Harvard API Key

Register at: https://www.harvardartmuseums.org/collections/api

### Database Setup

```sql
-- Create database
CREATE DATABASE harvard_artifacts;
USE harvard_artifacts;

-- Artifact metadata table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    dated VARCHAR(200),
    division VARCHAR(200),
    medium VARCHAR(500),
    technique VARCHAR(500),
    period VARCHAR(200),
    accessionyear INT,
    totalpageviews INT,
    totaluniquepageviews INT
);

-- Artifact media table
CREATE TABLE artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    iiifbaseuri VARCHAR(500),
    baseimageurl VARCHAR(500),
    primaryimageurl VARCHAR(500),
    imagecopyright TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    hue VARCHAR(50),
    percent FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Running the Application

```bash
streamlit run app.py
```

The Streamlit dashboard will open at `http://localhost:8501`

## Key Code Patterns

### API Data Extraction

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(api_key, page=1, size=100):
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    """
    url = "https://api.harvardartmuseums.org/object"
    params = {
        "apikey": api_key,
        "page": page,
        "size": size,
        "hasimage": 1  # Only artifacts with images
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Usage
api_key = os.getenv("HARVARD_API_KEY")
data = fetch_artifacts(api_key, page=1, size=100)
print(f"Total records: {data['info']['totalrecords']}")
print(f"Total pages: {data['info']['pages']}")
```

### ETL Pipeline with Pagination

```python
import pandas as pd
import time

def extract_all_artifacts(api_key, max_pages=10):
    """
    Extract artifacts across multiple pages with rate limiting
    """
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        try:
            data = fetch_artifacts(api_key, page=page)
            artifacts = data.get('records', [])
            all_artifacts.extend(artifacts)
            
            print(f"Extracted page {page}/{max_pages}: {len(artifacts)} artifacts")
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    
    return all_artifacts

def transform_artifacts(raw_artifacts):
    """
    Transform nested JSON into structured DataFrames
    """
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_artifacts:
        # Metadata
        metadata_list.append({
            'id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'division': artifact.get('division'),
            'medium': artifact.get('medium'),
            'technique': artifact.get('technique'),
            'period': artifact.get('period'),
            'accessionyear': artifact.get('accessionyear'),
            'totalpageviews': artifact.get('totalpageviews', 0),
            'totaluniquepageviews': artifact.get('totaluniquepageviews', 0)
        })
        
        # Media
        if artifact.get('primaryimageurl'):
            media_list.append({
                'artifact_id': artifact.get('id'),
                'iiifbaseuri': artifact.get('iiifbaseuri'),
                'baseimageurl': artifact.get('baseimageurl'),
                'primaryimageurl': artifact.get('primaryimageurl'),
                'imagecopyright': artifact.get('imagecopyright')
            })
        
        # Colors
        for color in artifact.get('colors', []):
            colors_list.append({
                'artifact_id': artifact.get('id'),
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'hue': color.get('hue'),
                'percent': color.get('percent')
            })
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### Database Loading

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Create MySQL database connection from environment variables
    """
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def load_metadata(df_metadata):
    """
    Batch insert artifact metadata into database
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO artifactmetadata 
    (id, title, culture, century, classification, department, dated, 
     division, medium, technique, period, accessionyear, 
     totalpageviews, totaluniquepageviews)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    title=VALUES(title), culture=VALUES(culture)
    """
    
    records = df_metadata.to_records(index=False).tolist()
    cursor.executemany(insert_query, records)
    conn.commit()
    
    print(f"Inserted {cursor.rowcount} metadata records")
    cursor.close()
    conn.close()

def load_all_data(df_metadata, df_media, df_colors):
    """
    Load all transformed data into respective tables
    """
    load_metadata(df_metadata)
    # Similar functions for media and colors
    print("ETL pipeline completed successfully")
```

### Streamlit Analytics Dashboard

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

st.title("🎨 Harvard Art Museums Collection Analytics")

# Sidebar for query selection
query_options = {
    "Top 10 Cultures by Artifact Count": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 10
    """,
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    "Most Common Colors": """
        SELECT color, COUNT(*) as usage_count, AVG(percent) as avg_percent
        FROM artifactcolors
        GROUP BY color
        ORDER BY usage_count DESC
        LIMIT 10
    """,
    "Department Distribution": """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY artifact_count DESC
    """
}

selected_query = st.sidebar.selectbox("Select Analysis", list(query_options.keys()))

if st.button("Run Analysis"):
    conn = get_db_connection()
    df_result = pd.read_sql(query_options[selected_query], conn)
    conn.close()
    
    st.subheader(f"Results: {selected_query}")
    st.dataframe(df_result)
    
    # Auto-generate visualization
    if len(df_result.columns) >= 2:
        fig = px.bar(df_result, 
                     x=df_result.columns[0], 
                     y=df_result.columns[1],
                     title=selected_query)
        st.plotly_chart(fig, use_container_width=True)
```

### Complete ETL Workflow

```python
def run_full_etl_pipeline():
    """
    Complete ETL pipeline from API to database
    """
    # Extract
    print("Starting extraction...")
    api_key = os.getenv("HARVARD_API_KEY")
    raw_artifacts = extract_all_artifacts(api_key, max_pages=5)
    
    # Transform
    print("Transforming data...")
    df_metadata, df_media, df_colors = transform_artifacts(raw_artifacts)
    
    # Load
    print("Loading to database...")
    load_all_data(df_metadata, df_media, df_colors)
    
    print(f"Pipeline complete! Processed {len(raw_artifacts)} artifacts")
    return df_metadata, df_media, df_colors

# Execute pipeline
if __name__ == "__main__":
    run_full_etl_pipeline()
```

## Common Analytical Queries

```sql
-- Top viewed artifacts
SELECT title, culture, totalpageviews
FROM artifactmetadata
ORDER BY totalpageviews DESC
LIMIT 20;

-- Artifacts with color data
SELECT a.title, a.culture, c.color, c.percent
FROM artifactmetadata a
JOIN artifactcolors c ON a.id = c.artifact_id
WHERE c.percent > 50
ORDER BY c.percent DESC;

-- Media availability by department
SELECT 
    a.department,
    COUNT(*) as total_artifacts,
    COUNT(m.id) as with_media,
    ROUND(COUNT(m.id) * 100.0 / COUNT(*), 2) as media_percentage
FROM artifactmetadata a
LEFT JOIN artifactmedia m ON a.id = m.artifact_id
GROUP BY a.department
ORDER BY total_artifacts DESC;
```

## Troubleshooting

**API Rate Limits:**
- Add `time.sleep(0.5)` between requests
- Implement exponential backoff for 429 errors

**Database Connection Issues:**
```python
try:
    conn = get_db_connection()
    conn.ping(reconnect=True, attempts=3, delay=5)
except Error as e:
    print(f"Database error: {e}")
```

**Missing Data Fields:**
```python
# Safe field access
culture = artifact.get('culture', 'Unknown')
colors = artifact.get('colors', [])
```

**Streamlit Caching:**
```python
@st.cache_data(ttl=3600)
def load_cached_data(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
```

This skill provides everything needed to build production-ready ETL pipelines and analytics dashboards for museum collection data using modern Python data engineering tools.
